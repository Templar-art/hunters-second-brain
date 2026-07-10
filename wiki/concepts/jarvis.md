---
type: concept
tags: [jarvis, automation, ops]
status: active
updated: 2026-07-10
---

# Jarvis

Hunter's personal assistant built on Claude Code. Built in phases; each phase gets its own spec.

## Roadmap

1. **Brain + ops copilot** — live. Weekday 8:30 AM morning brief: ranked open to-dos from the 10x CRM, delivered as a push notification. Spec: [phase 1 design](../../docs/superpowers/specs/2026-07-10-jarvis-phase1-design.md). Prompt: [PROMPT.md](../../projects/jarvis/PROMPT.md).
2. **Job state tracking** — live. Every job folder gets `JOB.md` (from [JOB-template.md](../../projects/jarvis/JOB-template.md)): status, shots table, cost tally, append-only log; updated on every state change. Enforced by vault CLAUDE.md rule + cross-project auto-memory. Spec: [phase 2 design](../../docs/superpowers/specs/2026-07-10-jarvis-phase2-job-tracking-design.md). Query/resume/brief-integration deferred — cheap once tracking exists.
3. **Voice layer** — live (tested 10 Jul). Push-to-talk: hold right-option → speak → spoken (Daniel en_GB) + on-screen answer. Components in [projects/jarvis/voice/](../../projects/jarvis/voice/): `jarvis.lua` (Hammerspoon hotkey + overlay), `jarvis-ask.sh` (ffmpeg → whisper-cli base.en → `claude -p` with [VOICE-PROMPT.md](../../projects/jarvis/voice/VOICE-PROMPT.md) → TTS), Cmd+Alt+J mute. TTS = macOS `say` Jamie (Premium) — Hunter's pick, instant (`.use-say` flag present). Kokoro local neural installed as alternative (`bm_george` etc., ~5 s load latency); delete `projects/jarvis/voice/.use-say` to switch back. Ask + capture only: reads vault/CRM, may create todos, hard-banned from paid ops/writes. Spec: [phase 3 design](../../docs/superpowers/specs/2026-07-10-jarvis-phase3-voice-design.md). Note: headless CRM connector access still unverified — voice may answer task questions with "CRM not reachable"; wire local MCP config if so.

## Phase 1 mechanics

- Scheduled task `jarvis-morning-brief` in the Claude desktop app (local, not cloud — file: `~/.claude/scheduled-tasks/jarvis-morning-brief/SKILL.md`), cron `30 8 * * 1-5` local time (Hunter opens the laptop ~8:30; if closed at fire time it runs on next launch). Local task, not cloud.
- Reads the 10x CRM MCP (`list_personal_todos` — the only read tool the CRM exposes: title, priority, optional due date).
- Brief: max 10 lines, overdue → due today → next 3 days → by priority; one closing line on the shape of the day.
- Failure is loud: CRM unreachable pushes "re-auth needed"; empty slate pushes "slate clear". A missing brief is itself the alarm.

## Related

- [[higgsfield-pipelines]] — generation work Jarvis will orchestrate in phase 2.
