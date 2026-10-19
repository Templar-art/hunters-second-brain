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

READ_ONLY = re.compile(
    r"^mcp__magnific__("
    r"simulate_.*|account_.*|guides_.*|feed_view_options|project_report"
    r"|.*_list|.*_list_.*|.*_show|.*_get|.*_search|.*_status|.*_state|.*_wait"
    r"|.*_models_settings|audio_timing_get|spaces_get_nodes|scene3d_search_library_objects"
    r"|projects_share_candidates|video_metadata|creations_tags"
    r")$"
)


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


def gate(data):
    tool = data.get("tool_name", "")
    if READ_ONLY.match(tool):
        return
    short = tool.removeprefix("mcp__magnific__")
    if data.get("permission_mode") != "bypassPermissions":
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

if "--record-prompt" in sys.argv:
    record_prompt(data)
else:
    gate(data)
