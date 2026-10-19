#!/usr/bin/env python3
"""Magnific money gate (PreToolUse).

Approval source: Hunter's own latest typed message, read from the session
transcript (`transcript_path`) — there is no approval file to forge.
An "approval" = his latest real message starts with yes/go/approved/…
and is under APPROVAL_TTL old.

Rules:
  * Magnific read-only / cost-check tools (exact allowlist) pass.
  * Any other Magnific tool (generations, upscales, video, audio, 3D, runs,
    and anything added later):
      - default / acceptEdits / plan mode -> "ask" (native prompt)
      - bypass / auto / unknown mode      -> deny unless approved
        (tested 2026-10-20: "ask" is silently auto-approved under bypass)
  * Bash/Write/Edit/MultiEdit/NotebookEdit touching the gate itself
    (.claude/hooks, .claude/settings*.json, session transcripts) -> deny
    unless approved, so the gate can't be quietly switched off.
  * Any error -> deny (fail closed).

Threat model: a careless or over-eager agent, not a hostile one. An agent
with a full shell can always find some way around an in-process check; this
makes spending or disabling the gate require Hunter's typed go-ahead.
"""
import json, re, sys
from datetime import datetime, timezone

APPROVAL_TTL = 20 * 60
APPROVAL = re.compile(r"^\s*(yes|yep|yeah|go|go ahead|approved|approve|do it|run it|send it|ok go)\b", re.I)
INJECTED = re.compile(r"<(system-reminder|task-notification|side-sessions-event)>.*?</\1>", re.S)
PROTECTED = re.compile(r"\.claude/hooks|\.claude/settings[^/\s\"']*\.json|\.claude/projects/[^\s\"']*\.jsonl|magnific-gate")
NORMAL_MODES = {"default", "acceptEdits", "plan"}
WRITE_TOOLS = {"Bash", "Write", "Edit", "MultiEdit", "NotebookEdit"}

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


def decide(decision, reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": decision,
                                             "permissionDecisionReason": reason}}))


def last_human_message(transcript_path):
    """(text, timestamp) of Hunter's latest typed message, skipping tool results
    and harness-injected blocks."""
    last = (None, None)
    with open(transcript_path) as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("type") != "user" or r.get("isMeta"):
                continue
            c = r.get("message", {}).get("content")
            if isinstance(c, list):
                if any(isinstance(x, dict) and x.get("type") == "tool_result" for x in c):
                    continue
                c = " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
            text = INJECTED.sub("", c or "").strip()
            if text:
                last = (text, r.get("timestamp"))
    return last


def approved(data):
    text, ts = last_human_message(data["transcript_path"])
    if not text or not ts or not APPROVAL.match(text):
        return False
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(ts.replace("Z", "+00:00"))).total_seconds()
    return 0 <= age < APPROVAL_TTL


def gate(data):
    tool = data.get("tool_name", "")
    if tool in WRITE_TOOLS:
        if PROTECTED.search(json.dumps(data.get("tool_input", {}))) and not approved(data):
            decide("deny", "Magnific gate: this touches the gate's own hook/settings/transcripts. "
                           "Ask Hunter; it needs his reply starting with yes/go/approved.")
        return
    if not tool.startswith("mcp__magnific__") or tool in READ_ONLY:
        return
    short = tool.removeprefix("mcp__magnific__")
    if data.get("permission_mode") in NORMAL_MODES:
        return decide("ask", f"Magnific gate: {short} may spend credits.")
    if not approved(data):
        decide("deny", f"Magnific gate: {short} may spend credits and Hunter has not approved it. "
                       "Run simulate_cost, quote the cost in chat, and wait for Hunter to reply "
                       "starting with yes/go/approved.")


try:
    gate(json.load(sys.stdin))
except Exception as e:
    decide("deny", f"Magnific gate: internal error ({type(e).__name__}), blocking to be safe.")
