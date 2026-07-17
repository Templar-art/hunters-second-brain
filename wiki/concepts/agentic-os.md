---
type: concept
tags: [aios, automation, infrastructure]
status: phase-1-live
updated: 2026-07-16
---

# Agentic OS (AIOS)

Hunter's agentic operating system layered on this vault. Four levels; phase 1 (L1 + L3) went live 2026-07-16. Spec: [phase-1 design](../../docs/superpowers/specs/2026-07-16-agentic-os-phase1-design.md).

## The four levels

1. **Skill + Loop Engineering** (keeps behavior) — skills already live in `.agents/skills/` and Claude plugins; the *loop engine* is new (below).
2. **Memory + State** (keeps state) — this vault: the wiki schema, auto-memory, JOB.md job tracking. Pre-existing.
3. **Interface / UI** (keeps access) — the AIOS dashboard (below).
4. **Distribution** (keeps it for others) — roadmap. Repo already on GitHub (Templar-art/hunters-second-brain).

## Loop engine (L1)

One action registry, two triggers — the clock and a click. Actions are prompt files in `projects/aios-dashboard/actions/`; both launchd and the dashboard run them the same way: `claude -p` headless in the vault, edits allowed, git allowed, **paid MCP tools disallowed** (the money gate is enforced in the spawn flags, not just prose).

Scheduled loops (macOS launchd, survive reboots, no Claude window needed):

| Loop | Schedule | Action |
|------|----------|--------|
| `com.10x.aios.morning-brief` | weekdays 6:27am | writes `## Morning Brief` into the daily note `YYYY-MM-DD.md`: jobs + stalled flags, follow-ups, vault health; commits + pushes |
| `com.10x.aios.nightly-lint` | daily 9:57pm | CLAUDE.md lint pass over the wiki; appends `log.md`; commits + pushes |

Controls: `launchctl bootout gui/$UID/com.10x.aios.morning-brief` pauses a loop; `launchctl bootstrap gui/$UID ~/Library/LaunchAgents/<plist>` resumes it. Logs land in `projects/aios-dashboard/logs/`.

## Dashboard (L3)

`node projects/aios-dashboard/server.mjs` → http://localhost:8770 (also in `.claude/launch.json` as `aios`). Live vault scan (jobs, credits, follow-ups, wiki health, daily note) plus buttons that fire any registry action with output streaming into an on-page console. Adding a button = one entry in `actions/actions.json` + one prompt file.

Current actions: Morning Brief, Plan Today, Vault Lint, Job Status (read-only audit), Weekly Review, Pull CRM (disabled until the 10x-crm MCP is re-authed).

## Relationship to [[jarvis]]

Jarvis phase 1 (weekday 7am CRM brief via push) overlaps the morning-brief loop. AIOS is the engine; Jarvis becomes an action in this registry once the CRM MCP is re-authed — one brief, not two.

## Roadmap

- 10x CRM: **blocked externally** (2026-07-16) — full connection needs Vercel-side authorization the boss hasn't granted; Pull CRM action stays disabled until then. When unblocked: enable the action and fold CRM tasks into the morning brief.
- L4: publish a scrubbed template repo of the OS.
- Social-metrics pull, push notifications on loop failures.
