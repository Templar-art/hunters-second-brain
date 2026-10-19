#!/usr/bin/env python3
"""Magnific money gate.

PreToolUse (matcher mcp__magnific__.*):
  Read-only / cost-check tools pass silently. Every other Magnific tool —
  generations, upscales, video, audio, 3D, flow/space runs, and anything
  Magnific adds later — is gated:
    * normal modes (default/acceptEdits/auto/plan): permissionDecision "ask",
      so Claude Code shows its own approval prompt.
    * bypassPermissions: "ask" is silently auto-approved there (tested
      2026-10-20), so the call is DENIED unless Hunter's most recent chat
      message starts with an approval word, within APPROVAL_TTL seconds.

UserPromptSubmit (`--record-prompt`):
  Records whether Hunter's latest message is an approval. Only Hunter's typed
  messages reach this hook, so Claude cannot approve its own spend through
  it. Claude must never write the state file by hand.

Fails closed: unreadable input -> ask (normal) / deny (bypass unknown -> deny).
"""
import json, os, re, sys, time

STATE = os.path.expanduser("~/.claude/magnific-gate-approval.json")
APPROVAL_TTL = 20 * 60
APPROVAL = re.compile(r"^\s*(yes|yep|yeah|go|go ahead|approved|approve|do it|run it|send it|ok go)\b", re.I)

# Exact allowlist (no wildcards): only these pass ungated. New Magnific tools are gated
# until someone checks they are free and adds them here.
READ_ONLY = {"mcp__magnific__" + n for n in """
account_balance account_profile audio_timing_get audio_voices_list audio_voices_show
brand_kit_get brand_kit_list brand_kit_list_creations brand_kit_list_rules
brand_kit_list_user_presets brand_kit_process_status creation_status creations_comments_list
creations_get creations_list creations_search creations_show creations_tags creations_upload_show
creations_wait design_auto_resize_show feed_view_options flows_get flows_list flows_show
flows_wait folders_get folders_list folders_show guides_get guides_list images_models_list
images_models_settings images_models_show images_upscale_modes_list images_upscale_presets_list
library_list library_show models3d_models_list project_report projects_share_candidates
projects_shares_get retouch_models_list scene3d_state scene3d_search_library_objects
simulate_cost simulate_flows simulate_spaces spaces_get_nodes spaces_list spaces_run_status
spaces_show spaces_state spaces_templates_search spaces_node_types_search stock_get
stock_search stock_show tags_list video_luts_list video_metadata video_models_list
video_vfx_list""".split()}

NORMAL_MODES = {"default", "acceptEdits", "plan"}  # auto + bypass may auto-approve "ask", so they get the deny path


def out(event, **fields):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, **fields}}))


def record_prompt(data):
    prompt = data.get("prompt", "") or ""
    state = {"approved": bool(APPROVAL.match(prompt)), "at": time.time()}
    with open(STATE, "w") as f:
        json.dump(state, f)


def approved_recently():
    try:
        with open(STATE) as f:
            s = json.load(f)
        return s.get("approved") and time.time() - s.get("at", 0) < APPROVAL_TTL
    except Exception:
        return False


def guard_state_file(data):
    """Bash/Write/Edit: block anything that touches the approval state file."""
    if "magnific-gate-approval" in json.dumps(data.get("tool_input", {})):
        out("PreToolUse", permissionDecision="deny",
            permissionDecisionReason="Magnific gate: the approval state file is written only by "
                                     "Hunter's own messages. Do not touch it.")


def gate(data):
    tool = data.get("tool_name", "")
    if not tool.startswith("mcp__magnific__"):
        return guard_state_file(data)
    if tool in READ_ONLY:
        return
    short = tool.removeprefix("mcp__magnific__")
    if data.get("permission_mode") in NORMAL_MODES:  # unknown/missing mode = treat as bypass
        out("PreToolUse", permissionDecision="ask",
            permissionDecisionReason=f"Magnific gate: {short} may spend credits.")
        return
    if approved_recently():
        return
    out("PreToolUse", permissionDecision="deny",
        permissionDecisionReason=(
            f"Magnific gate: {short} may spend credits and Hunter has not approved it. "
            "Run simulate_cost, quote the cost in chat, and wait for Hunter to reply "
            "starting with yes/go/approved. Never write the gate state file yourself."))


try:
    data = json.load(sys.stdin)
except Exception:
    if "--record-prompt" not in sys.argv:
        out("PreToolUse", permissionDecision="deny",
            permissionDecisionReason="Magnific gate: could not read tool call.")
    sys.exit(0)

try:
    if "--record-prompt" in sys.argv:
        record_prompt(data)
    else:
        gate(data)
except Exception:
    if "--record-prompt" not in sys.argv:
        out("PreToolUse", permissionDecision="deny",
            permissionDecisionReason="Magnific gate: internal error, blocking to be safe.")
