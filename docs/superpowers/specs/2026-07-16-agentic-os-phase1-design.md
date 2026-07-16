# Agentic OS (AIOS) — Phase 1 Design

**Date:** 2026-07-16 · **Status:** approved by Hunter · **Scope:** Level 1 (loops) + Level 3 (dashboard)

## Vision (the 4 levels)

Hunter's AIOS follows a four-level model:

| Level | Purpose | Status |
|-------|---------|--------|
| L1 Skill + Loop Engineering | keeps behavior | **build tonight** — skills exist, loops don't |
| L2 Memory + State | keeps state | already exists (this vault: wiki schema, auto-memory, JOB.md) |
| L3 Interface / UI | keeps access | **build tonight** — live local dashboard with action buttons |
| L4 Distribution | keeps it for others | later (repo already on GitHub) |

## L1 — Loop Engine

One **action registry** (`projects/aios-dashboard/actions/*.md` prompt files) consumed by two triggers:

1. **Clock** — macOS launchd LaunchAgents (durable, survives reboots, no Claude window needed) run `claude -p "$(cat <action>.md)"` headless in the vault directory:
   - `com.10x.aios.morning-brief` — weekdays 6:27am. Pulls CRM tasks (skips with a note until 10x-crm MCP is re-authed), scans `projects/*/JOB.md` for in-flight jobs and credit tallies, scans wiki client pages for waiting-on/follow-ups, adds a vault-health one-liner. Writes the brief into the daily note `YYYY-MM-DD.md` at vault root, refreshes dashboard data, commits + pushes.
   - `com.10x.aios.nightly-lint` — daily 9:57pm. Wiki lint per CLAUDE.md (contradictions, orphans, stale pages), appends `wiki/log.md`, refreshes dashboard data, commits + pushes.
2. **Click** — dashboard buttons fire the same action files on demand.

**Hard rule:** loop sessions never spend credits. Action prompts state the money gate explicitly and headless runs get no paid-MCP tools.

## L3 — Dashboard

`projects/aios-dashboard/` — zero-dependency Node server (`server.mjs`, port 8770):

- **Static UI** `index.html` — dark 10x theme (#61a8d8 accent, Poppins/Montserrat), terminal-industrial aesthetic per Hunter's reference screenshot.
- **GET /api/data** — live vault scan (`lib/scan.mjs`): active jobs parsed from JOB.md frontmatter (status, credits, aud), follow-ups from wiki pages, pages updated this week, recent log entries, today's daily-note presence.
- **POST /api/run** `{action}` — spawns `claude -p` headless with the action's prompt file, streams stdout back chunked into a terminal panel on the page. One run at a time; kill button aborts.
- **`actions/actions.json`** — button registry: id, label, prompt file, description. Adding a button = one JSON entry + one prompt file, no code.
- Button row v1: Morning Brief · Plan Today · Vault Lint · Job Status · Weekly Review · Pull CRM (disabled until re-auth).
- Stat cards: active jobs, credits spent (month), pages updated (week), follow-ups waiting.
- Registered in `.claude/launch.json` as `aios` (port 8770).

## Error handling

- CRM MCP unauthorized → brief includes "CRM skipped — re-auth needed" line, never fails the loop.
- Concurrent button presses → server returns 409, UI shows "run in progress".
- launchd job failure → stdout/stderr logged to `projects/aios-dashboard/logs/`.

## Out of scope (roadmap)

- L4 GitHub template/distribution; cloud scheduled agents; push notifications; social-metrics pull; CRM write-back.
