# Jarvis — Phase 1 Design (Brain + Ops Copilot)

**Date:** 2026-07-10
**Status:** Draft — awaiting Hunter's approval
**Owner:** Hunter / Claude

## Vision (full stack, later phases)

Jarvis is Hunter's personal assistant built on Claude Code. Full ambition, in build order:

1. **Brain + ops copilot** ← this spec
2. **Job orchestrator** — one command runs a whole 10x job (intake → staging → stills → video → delivery) using existing skills
3. **Voice layer** — wake word + STT/TTS on the Mac, riding on top of 1–2

Each later phase gets its own spec. Nothing below designs for them beyond not blocking them.

## Phase 1 scope

A morning brief that arrives as a push notification on weekdays, built from the 10x CRM. Nothing else.

- **Sources:** 10x CRM MCP only (tasks + reminders). Vault, calendar, and email are explicitly out of scope for phase 1.
- **Channel:** push notification (Claude Code notifications to Hunter's devices). No email, iMessage, or bots.
- **Cadence:** weekdays ~7:00 AM, one run per day. No midday or evening runs.

## Architecture

Three pieces:

### 1. Identity + prompt

- `wiki/concepts/jarvis.md` — durable wiki page: what Jarvis is, phase roadmap, links to this spec and the prompt. Indexed in `wiki/index.md`.
- `projects/jarvis/PROMPT.md` — the actual instruction file the scheduled agent runs. Defines the brief format:
  - Pull all open tasks and reminders from the 10x CRM MCP.
  - Rank: overdue first, then due today, then upcoming (next 3 days).
  - Compose a brief of at most 10 lines: one line per task ("[OVERDUE] Client — task"), closing with a single one-line read on the shape of the day.
  - Tone: terse, factual, no filler.

### 2. Scheduled routine

A Claude Code scheduled agent (routine):

- **Cron:** weekdays 7:00 AM Australia/Brisbane.
- **Run:** fresh session executes `projects/jarvis/PROMPT.md` → reads CRM → composes brief → sends push notification.
- **Notification format:** title `Jarvis — {weekday} {date}`, body = the brief.

### 3. Failure handling

- CRM unreachable or unauthorized → still push: `Jarvis: CRM unreachable — re-auth needed.` Never fail silently; a missing brief must itself be a signal.
- Zero open tasks → push `Jarvis: slate clear today.` (confirms the loop ran).

## Dependencies / blockers

- **10x-crm MCP re-auth** — currently unauthorized. Hunter must re-authorize via claude.ai connector settings (or `/mcp` in an interactive session) before the routine can read tasks. Hard blocker for phase 1 going live.

## Out of scope (later phases)

- Vault/calendar/email as brief sources
- Two-way chat with Jarvis
- Afternoon/evening runs, event-driven nudges
- Voice, job orchestration

## Success criteria

- Weekday mornings, a push notification arrives unprompted with an accurate, ranked view of what's on Hunter's plate.
- CRM outage produces an explicit "unreachable" push, not silence.

---
_Vault: [[jarvis]]_
