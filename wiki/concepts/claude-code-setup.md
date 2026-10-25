---
type: concept
tags: [claude, infrastructure, security, tooling]
status: audited
updated: 2026-10-26
---

# Claude Code Setup

The standing map of Hunter's Claude Code install — what is configured, where it lives, and what the safety posture is. First full audit 2026-08-10. Machine-level tooling detail lives in auto-memory `reference-claude-tooling.md`; this page is the vault-side record and the security findings.

## Layout

| Thing | Where | Notes |
|-------|-------|-------|
| Global settings | `~/.claude/settings.json` | statusline, theme, enabled plugins, extra marketplaces |
| Project settings | `.claude/settings.json` (vault, committed) | disables ui-ux-pro-max, scroll-world, frontend-design plugins here (2026-10-19) |
| Magnific money gate | `.claude/hooks/magnific-gate.py` | One PreToolUse hook (2026-10-20, v3). Approval = Hunter's latest typed message in the session transcript starts with yes/go/approved and is under 20 min old; harness-injected blocks, tool results and isMeta rows are skipped. **No state file**, so nothing to forge. Paid Magnific tools: ask in default/acceptEdits/plan, denied in bypass/auto/unknown mode unless approved. Exact allowlist of 67 read-only + simulate_* tools; any new tool is gated. Bash/Write/Edit/MultiEdit/NotebookEdit touching `.claude/hooks`, `.claude/settings*.json` or session transcripts also need approval, so the gate can't be quietly switched off. Fails closed. 20-case test with fake transcripts passed. Threat model is a careless agent, not a hostile one; no HMAC. Approval is a 20-min window, not single-use, on purpose (batch jobs) |
| Project local settings | `.claude/settings.local.json` (vault) | one PostToolUse hook only |
| Skills | `~/.claude/skills/` | 35 as of 10 Aug; only `caveman-compress`, `impeccable`, `webapp-testing` ship executable code, and none of it auto-runs |
| MCP servers | `~/.claude.json` | **none global** since 2026-10-19; all six (`magnific`, `10x-crm`, `skill-seekers`, `shopify-dev`, `gethookd`, `blender`) scoped to this vault. Kept in `~/.claude.json`, not `.mcp.json`, because the GetHookd entry carries a bearer token. `blender` still runs as `uvx blender-mcp`; upstream renamed it to `mcp-for-blender`, but the old name keeps working. Its socket (localhost:9876) has no authentication, and `BLENDER_MCP_SAFE_MODE=1` is available but not set ([[claude-blender-guides-2026-10]]) |
| Parked skills | `~/.claude/skills-parked/` | 13 animation/web-dev skills moved out of global 2026-10-19; README there says how to revive |
| Scheduled agents | `~/Library/LaunchAgents/com.10x.aios.*` | see [[agentic-os]] |

Plugins were pruned 2026-07-27 — the dev-tooling packs and both output styles were injecting ~6–7k tokens of skill descriptions into every request in a vault that is not a software project. They stay registered but disabled; flip to `true` to revive.

## Efficiency pass — 2026-10-19

Measured baseline before the first message: ~80k tokens (system tools 28k, MCP tools 23k, system prompt 11k, skills 10k, memory 5k). Pass: global MCP servers moved to vault scope (all are used here, so in-vault savings are nil, but other folders no longer load them), web/UI plugins disabled for the vault, 13 animation/web skills parked. Same day, second pass: superpowers + code-review + commit-commands + hookify + security-guidance also off for the vault; caveman-help and caveman-review parked. Next steps live on [[claude-improvement-plan]]. Configs backed up to `~/.claude/backups/efficiency-2026-10-19/`. Habits that matter more than config: `/clear` between unrelated jobs, a fresh session per job rather than one long thread, and subagents for broad searches.

## Git media rule

Since 2026-10-20 `.gitignore` blocks `*.mp4 *.mov *.m4v *.mxf *.wav *.aif *.aiff *.mp3 *.blend *.zip` vault-wide (`.git` had reached 6.6 GB). Files already tracked stay tracked. To force a small one in, use `git add -f`. History has not been rewritten.

## Permissions posture

There is **no permission allowlist** in either settings file, so every tool call prompts. That is the safe default and worth keeping deliberately: the vault's real risk is not typing speed, it is an unattended agent spending credits or pushing to a client repo. The money gate ([[higgsfield-pipelines]], Magnific) depends on that friction.

The only hook is the `impeccable` UI checker on `Edit|Write|MultiEdit`, running a local `hook.mjs`. Benign, 5s timeout.

## Vault repo

`Templar-art/hunters-second-brain`, **private**. Secret scan over tracked files is clean, and `.gitignore` correctly excludes the things that would hurt if it ever went public — invoice bank details (`projects/elevra-invoices/invoices/`), client render frames, Obsidian machine state.

⚠️ **Obsidian has zero community plugins** — no Git plugin, no Sync. Backup is entirely "Claude committed this session." Nothing saves between sessions. An Obsidian Git plugin on a timer would close that gap; until then, a session that ends without a commit loses work.

## Audit findings — 2026-08-10

**🔴 The AIOS dashboard was reachable from the LAN.** `server.mjs` called `server.listen(PORT)` with no host, which binds `0.0.0.0`. Any device on the network could reach `/api/data` (a full vault scan — client names, jobs, credits) and `POST /api/run`, which spawns headless `claude -p` with `Read,Write,Edit` and `git push` and **no authentication**. It had been that way since the dashboard went live in July. Fixed: bound to `127.0.0.1`, verified LAN-refused (`cdac0f6`). The lesson generalises — every local agent server in this vault binds loopback, because the dashboard pattern is "unauthenticated button that runs an agent with write access."

**🔴 Every scheduled job had been silently dead.** All four launchd agents failed identically: `/bin/zsh: can't open input file`. Under launchd, `/bin/zsh` has no TCC access to `~/Documents`, so it could `stat` and `cd` into the vault but got `Operation not permitted` the moment it read a file's contents. `node` is already permitted — `server.mjs` has been reading the vault under launchd the whole time — which is why the dashboard worked while every clock-triggered loop did not. Fixed by moving the runners to node (`3c20adf`); see [[agentic-os]].

Diagnostic worth keeping: `[[ -r file ]]` returns true under a TCC denial because `access(2)` is not blocked — only the read is. A permission test that passes is not proof the read will.

## Related

[[agentic-os]] · [[mac-performance]] · [[jarvis]] · [[higgsfield-pipelines]]
