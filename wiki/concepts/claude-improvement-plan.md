---
type: concept
tags: [claude, efficiency, infrastructure, plan]
status: proposed
updated: 2026-10-20
---

# Claude Improvement Plan

Research pass of 19 October 2026 on how to make the whole setup run better: Claude Code itself, the vault, and the job workflow. It has two sources. One is a Claude Code best-practices sweep of the official docs and changelog (v2.1.303, 18 October). The other is a read-only audit of this vault and the auto-memory folder. What has already been applied is logged on [[claude-code-setup]]; everything else below is proposed and not done.

## Already done (19 Oct)

- Global MCP servers moved to vault scope.
- These plugins are off in the vault (via `.claude/settings.json`): ui-ux-pro-max, scroll-world, frontend-design, superpowers, code-review, commit-commands, hookify, security-guidance.
- 15 skills parked in `~/.claude/skills-parked/`: 13 animation/web-dev skills plus `caveman-help` and `caveman-review`. `caveman`, `caveman-compress` and `ultracave` stay, because CLAUDE.md runs ultra.
- Baseline before any of this: about 80k tokens loaded before the first message.

## Priority 1: stop the repo bloat — ✅ ignore rules done 2026-10-20 (history rewrite not done)

The biggest real problem the audit found.

- `.git` is **6.6 GB**. 187 tracked media files (mp4/mov/wav/blend) account for about 2.2 GB. History still holds the cliff-mansion `.blend` and its `.blend1` (~500 MB each) and `beach-house-v1.blend` (247 MB).
- About 360 MB of untracked mp4s sit in `projects/blender-blockouts/beach/video/`. Because CLAUDE.md says "commit freely", they will go in on the next commit.
- `.gitignore` only has per-folder media rules. **Fix:** add global `*.mp4 *.mov *.wav *.blend *.blend1 *.zip` rules. Keep finals on Drive or the SSD; the wiki should point at them, not store them.
- An optional, bigger fix is to rewrite history with `git filter-repo` to drop the old binaries. That is destructive and every clone must re-clone, so Hunter decides.

## Priority 2: hard money gate in config, not just in prose — ✅ done 2026-10-20

**As built** (supersedes the plan bullets below): `.claude/hooks/magnific-gate.py`, wired in `.claude/settings.json`. Live test showed a hook `ask` is **silently auto-approved under bypass-permissions mode**, so a plain ask rule would have protected nothing in Hunter's usual mode. The gate therefore asks in normal modes and **denies** in bypass mode unless Hunter's latest typed message starts with yes/go/approved (valid 20 min, recorded by a UserPromptSubmit hook Claude cannot trigger). Read-only and `simulate_*` tools always pass. Verified live: `guides_list` passed, `tags_create` was blocked before reaching Magnific.

At the moment the "ask before any paid op" rule lives only in CLAUDE.md, and nothing enforces it mechanically. The fix is a permission rule in the vault's `.claude/settings.json`:

- `allow` the free tools: `mcp__magnific__simulate_cost` and the list/show/status tools.
- `ask` on `mcp__magnific__*` so every paid call prompts, whatever the session's mode.
- The docs say `ask` beats a hook's allow. **Unverified:** whether it still prompts under bypass-permissions mode. Test it with a free tool before trusting it.
- Optional: a PreToolUse hook that appends every Magnific call to a cost log. That would make the JOB.md tallies (Priority 3) automatic.

## Priority 3: job tracking drift

- `projects/cva-woomala-enhance/JOB.md` still has the blank template header (`{client-slug}`, cost 0). Its log body ends at **4,035cr**, but [[cva-woomala-render-enhance]] and log.md still say 3,210cr, so the moody pass (825cr) never reached the wiki.
- `projects/zed-4-alex-keith-st/JOB.md` shows `intake` and cost 0, while the wiki says `generating`.
- `zed-full-house` and `bespoke-sold-popups` have sat at `review` since July.
- **Root-cause fix:** a small script that sums the `Ncr` entries in a JOB.md log and rewrites the header, run from `/harvest`.

## Priority 4: rules living in two systems

- `feedback-staging-default-model.md` still says "default to Nano Banana Pro", while [[staging-rules]] says to ask. Rewrite the body, not just the contradiction note.
- The 16 October ZED override in `feedback-curtains-default-and-anchor.md` ("add nothing to the house") is missing from [[staging-rules]], which was last updated 7 October.
- `feedback-zed-no-timber-dining-table.md` is superseded. Retire it, and fold its history into [[zed-style]].
- `ai-realestate-workflow.md` (25 KB, last changed 18 June) is still cited as "the full KB", but it is four months older than the wiki pipeline pages. Either refresh it or demote it to history and make [[higgsfield-pipelines]] the KB.

## Priority 5: Claude Code habits and settings

- **Model per task.** Sonnet for routine wiki and admin work, Opus for staging prompts and hard calls, Haiku for mechanical chores. Set subagents to a cheap model with `CLAUDE_CODE_SUBAGENT_MODEL`.
- **Effort.** Leave the default at medium and raise it only for tricky prompt work.
- **Session hygiene.** `/clear` between unrelated jobs, one session per job, `/compact <focus>` on long ones. Add a "when compacting, preserve job state + cost" line to CLAUDE.md.
- **Side-effect skills.** Set `disable-model-invocation: true` on `zip-job-folder`, `ssd-drive-upload` and `harvest`, so they only run when Hunter asks.
- **Skill descriptions.** Put trigger phrases first. The longest (banana-pro-director, cinema-worldbuilder, impeccable) are about 1k characters each.
- **`/usage`** shows spend broken down by skill, subagent and MCP server. Check it monthly.
- **Remote Control** lets Hunter drive a local session from his phone on a shoot day.

## Priority 6: housekeeping

- `wiki/log.md` is 163 KB (~40k tokens), and its first entries are out of date order. Split it into `log-2026-H1.md` plus a current file. Write one line per impeccable pass.
- `projects/10x-prestige-world` has a delivered JOB.md and 17 generations, but no wiki page (a harvest leak).
- Stray files: `projects/10x-site-for-lach.zip`, `fb-ads-handoff.md`, `salt-pm-brand-voice-handoff.md`.
- Staging boards are rebuilt per job (zed-style-guide, zed-86, zed-4). One shared board-builder script would replace the copies.
- Make the audit checks a `lint-vault` script: folders vs wiki, memory vs wiki, JOB.md header vs log total, index orphans.

## Related

[[claude-code-setup]] · [[staging-rules]] · [[higgsfield-pipelines]] · [[jarvis]]
