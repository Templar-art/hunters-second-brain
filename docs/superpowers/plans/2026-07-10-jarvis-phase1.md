# Jarvis Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A scheduled Jarvis routine that pushes a ranked morning brief of open CRM to-dos to Hunter's devices, weekdays 7:00 AM Brisbane.

**Architecture:** Three artifacts — a durable wiki page (`wiki/concepts/jarvis.md`), the agent prompt (`projects/jarvis/PROMPT.md`), and a scheduled cloud routine (created via the `schedule` skill) whose prompt is a self-contained copy of PROMPT.md. The routine reads the 10x CRM MCP (`list_personal_todos`) and ends by sending a push notification. Failures push explicitly — a missing brief must itself be a signal.

**Tech Stack:** Claude Code scheduled cloud agents (routines), 10x CRM MCP connector, push notifications. No application code.

**Spec:** `docs/superpowers/specs/2026-07-10-jarvis-phase1-design.md`

**Known constraint discovered post-spec:** the CRM MCP exposes only `list_personal_todos` (title, priority, optional due date) and `create_personal_todo`. The brief ranks by due date then priority; there is no richer "client job" data yet.

---

### Task 1: Jarvis prompt file

**Files:**
- Create: `projects/jarvis/PROMPT.md`

- [ ] **Step 1: Write the prompt file** with exactly this content:

```markdown
# Jarvis — Morning Brief

You are Jarvis, Hunter's ops copilot. Produce the weekday morning brief. You have no memory of prior runs; this file is your full instruction set.

## Steps

1. Call the 10x CRM tool `list_personal_todos` (limit 20).
2. Rank the results:
   1. Overdue (due date before today) — prefix line with `OVERDUE:`
   2. Due today — prefix with `TODAY:`
   3. Due within the next 3 days — prefix with the weekday, e.g. `FRI:`
   4. No due date — order by priority (high, medium, low), no prefix.
3. Compose the brief:
   - At most 10 lines, one task per line: `PREFIX Title (priority)` — omit `(medium)` since it is the default.
   - If more than 10 open tasks, show the top 9 and a final line `+N more`.
   - Close with ONE line reading the shape of the day (e.g. "Heavy render day" / "Light — good day to chase the funnel"). Terse, factual, no filler.
4. Send a push notification: title `Jarvis — {Weekday} {D Mon}` (e.g. `Jarvis — Thu 10 Jul`), body = the brief.

## Failure rules — never fail silently

- CRM tool unavailable or errors → push notification: title `Jarvis — CRM down`, body `CRM unreachable — re-auth the 10x-crm connector.`
- Zero open tasks → push notification: title `Jarvis — {Weekday} {D Mon}`, body `Slate clear today.`

Do nothing else: no task creation, no file edits, no other tools.
```

- [ ] **Step 2: Commit**

```bash
git add projects/jarvis/PROMPT.md
git commit -m "feat: Jarvis phase 1 morning-brief prompt"
```

### Task 2: Wiki page + index + log

**Files:**
- Create: `wiki/concepts/jarvis.md`
- Modify: `wiki/index.md` (concepts section — add one line)
- Modify: `wiki/log.md` (append entry)

- [ ] **Step 1: Write `wiki/concepts/jarvis.md`** with exactly this content:

```markdown
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

- Scheduled cloud routine, cron weekdays 7:00 AM Australia/Brisbane.
- Reads the 10x CRM MCP (`list_personal_todos` — the only read tool the CRM exposes: title, priority, optional due date).
- Brief: max 10 lines, overdue → due today → next 3 days → by priority; one closing line on the shape of the day.
- Failure is loud: CRM unreachable pushes "re-auth needed"; empty slate pushes "slate clear". A missing brief is itself the alarm.

## Related

- [[higgsfield-pipelines]] — generation work Jarvis will orchestrate in phase 2.
```

- [ ] **Step 2: Add to `wiki/index.md`** under the concepts section, one line matching the file's existing format:

```markdown
- [[jarvis]] — Hunter's phased personal assistant; phase 1 = weekday 7am CRM morning brief via push
```

- [ ] **Step 3: Append to `wiki/log.md`**:

```markdown
## [2026-07-10] ingest | Jarvis phase 1 — spec, prompt, wiki page, scheduled routine
```

- [ ] **Step 4: Commit**

```bash
git add wiki/concepts/jarvis.md wiki/index.md wiki/log.md
git commit -m "feat: Jarvis concept page + index/log entries"
```

### Task 3: Scheduled routine

**Files:** none (cloud-side routine)

- [ ] **Step 1: Invoke the `schedule` skill** to create a scheduled cloud agent:
  - Name: `jarvis-morning-brief`
  - Cron: `0 7 * * 1-5`, timezone Australia/Brisbane
  - Prompt: the full body of `projects/jarvis/PROMPT.md` (copy verbatim — the routine has no repo access guarantees, so the prompt must be self-contained).
  - Follow the skill's instructions; if cloud routines cannot reach the 10x CRM connector or cannot push, fall back to the local `mcp__scheduled-tasks__create_scheduled_task` (same prompt, same cron, note the "runs while app open" limitation to Hunter).

- [ ] **Step 2: Record the routine** — append the routine name/ID and mechanism (cloud vs local fallback) to `wiki/concepts/jarvis.md` under "Phase 1 mechanics", bump `updated`, commit:

```bash
git add wiki/concepts/jarvis.md
git commit -m "docs: record Jarvis routine id + mechanism"
```

### Task 4: Verification run

- [ ] **Step 1: Trigger the routine once manually** (schedule skill's run-now, or local task manual start). Free — no paid ops involved.
- [ ] **Step 2: Confirm with Hunter** that the push notification arrived and the brief matches the 7 open CRM todos (all medium, no due dates → priority order, so brief = 7 plain lines + shape-of-day line).
- [ ] **Step 3: Fix and re-run if wrong** — edit the routine prompt via the schedule skill, trigger again.
- [ ] **Step 4: Push all commits**

```bash
git push
```
