---
type: concept
tags: [jarvis, automation, ops]
status: active
updated: 2026-07-10
---

# Jarvis

Hunter's personal assistant built on Claude Code. Built in phases; each phase gets its own spec.

## Roadmap

1. **Brain + ops copilot** — live. Weekday 7:00 AM Brisbane morning brief: ranked open to-dos from the 10x CRM, delivered as a push notification. Spec: [phase 1 design](../../docs/superpowers/specs/2026-07-10-jarvis-phase1-design.md). Prompt: [PROMPT.md](../../projects/jarvis/PROMPT.md).
2. **Job orchestrator** — one command runs a whole 10x job (intake → staging → stills → video → delivery) on existing skills. Not started.
3. **Voice layer** — wake word + STT/TTS on the Mac. Not started.

## Phase 1 mechanics

- Scheduled task `jarvis-morning-brief` in the Claude desktop app (local, not cloud — file: `~/.claude/scheduled-tasks/jarvis-morning-brief/SKILL.md`), cron `0 7 * * 1-5` local time. **Limitation:** runs while the Claude app is open; if closed at 7am, it fires on next launch.
- Reads the 10x CRM MCP (`list_personal_todos` — the only read tool the CRM exposes: title, priority, optional due date).
- Brief: max 10 lines, overdue → due today → next 3 days → by priority; one closing line on the shape of the day.
- Failure is loud: CRM unreachable pushes "re-auth needed"; empty slate pushes "slate clear". A missing brief is itself the alarm.

## Related

- [[higgsfield-pipelines]] — generation work Jarvis will orchestrate in phase 2.
