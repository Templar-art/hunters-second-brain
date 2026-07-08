# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Note: this "repository" is an **Obsidian vault / knowledge workspace**, not a software project — there is nothing to build, lint, or test. See *How this repo works* below. This file also serves as the `productivity` plugin's working memory; the sections immediately below follow that format.

# Memory

## Me
Hunter, Videographer & founder at 10x Visuals (10xvisuals.com.au). Full creative agency — branding, video, photo, design. Email: hunter@10xvisuals.com.au.

## People
| Who | Role |
|-----|------|
| **Lachlan** | Editor |
| **Damon** | COO |
| **Tyson** | CEO |
| **Kris** | Videographer |
| **Hunter** | Videographer (me) |
→ Full profiles: memory/people/

## Terms
| Term | Meaning |
|------|---------|
| **Higgsfield** | AI image/video gen platform, run via `higgsfield` CLI |
| **Seedream** | Higgsfield image model (`seedream_v4_5`) — composition-locked render enhance, 1cr |
| **Nano Banana Pro** | Higgsfield image model (`nano_banana_2`) — creative staging, 4cr |
| **Topaz** | Upscale model (`topaz_image`) — optional, ask before using |
| **job_set_type** | Higgsfield's model ID string passed to `generate create` |
→ Full glossary: memory/glossary.md

## Projects
| Name | What |
|------|------|
| **CVA** | Architectural render gen — DELIVERED June 2026 (19 stills + ~40 clips, client happy). Repeat client; cost basis in auto-memory `project-cva-render-job.md`. |
| **Belle Property — Lot 48** | Insert proposed house into empty lot photos. House already rendered photoreal; remaining step is angle-matched composite into lot photos (T7/T8 + Seedream). SketchUp not needed. Awaiting "run it". |
| **CLC IG Repositioning** | Coast Life Constructions Instagram overhaul — audit 6 Jul 2026. 3 shifts: name every project, 40/25/20/15 pillar mix, editorial captions. → memory/projects/coast-life-constructions.md |
| **10x IG Repositioning** | Own @10xvisuals.co overhaul — audit 7 Jul 2026. Credit-loop growth (JUNE benchmark), one design system, named-work highlights, 52-tile arsenal ready. → memory/projects/10x-instagram-repositioning.md |
| **Bespoke Estate Agents** | Jason Ward, GC prestige agent — full brand system + Jun–Dec 2026 social strategy filed 8 Jul. Green #132a24, Zodiak/Poppins, 2 posts/wk. Kit: `General Folder/Bespoke Brand Kit`. → memory/projects/bespoke-estate-agents.md |
→ Details live in **auto-memory** (`~/.claude/…/memory/` → `project-lot48-belle-property.md`, `ai-realestate-workflow.md`) and in `memory/projects/` for vault-local project notes (currently: CLC, Bespoke).

## Preferences
- Tools: Gmail, Google Calendar
- Brand: colour #61a8d8, Poppins/Montserrat — full guidelines in memory/

---

# How this repo works (for Claude)

This is **not a software project** — it's an **Obsidian vault** that doubles as a Claude Code workspace ("Hunter's Second Brain"). There is no build, lint, or test step. "Editing code" here means editing Markdown notes. Respect Obsidian conventions: `[[wikilinks]]` for cross-note references, daily notes named `YYYY-MM-DD.md`, and `.base` (Bases plugin database views) / `.canvas` files as structured Obsidian documents — don't hand-author their internals unless asked.

## Two memory systems — don't confuse them
1. **Vault memory (committed to this repo):** the sections above in this file + the `memory/` tree (`people/`, `projects/`, `context/company.md`, `glossary.md`). This is Hunter's working knowledge and travels with the vault. Governed by the `productivity:memory-management` skill. Keep `CLAUDE.md` as the slim index; push detail down into `memory/`.
2. **Auto-memory (outside the repo):** `~/.claude/projects/.../memory/` with its own `MEMORY.md` index. Holds the full AI-workflow KB, brand guidelines, and feedback. Loaded automatically each session via system reminders. The `Projects` table above points to it ("full AI workflow KB in ~/.claude memory").

When asked to "remember" something, decide which tier it belongs to. Repo-specific facts → vault `memory/`. Cross-project preferences/feedback → auto-memory.

## The real work: Higgsfield AI generation
The substantive tasks are AI image/video generation for real-estate clients (see `Projects`). Two layers:
- **Vendored skills** in `.agents/skills/` (`higgsfield-generate`, `higgsfield-soul-id`, `higgsfield-product-photoshoot`, `higgsfield-marketplace-cards`), pinned by `skills-lock.json` (each entry carries a `computedHash` for integrity, sourced from the `higgsfield-ai/skills` GitHub repo). Treat these as read-only vendored content — update via the sync tooling, not by hand-editing.
- **Runtime:** everything runs through the `higgsfield` CLI. Bootstrap, auth, model discovery, and prompt patterns live in the skills — read the relevant `SKILL.md` before generating. Key rule from the skills: discover models/workflows with an unfiltered `higgsfield model list` / `higgsfield workflow list` rather than trusting search or `--help`.
- **Two pipelines — route before generating** (full detail in auto-memory `ai-realestate-workflow.md` → *Sky Replacement — Bulletproof SOP*): **full-frame generative** (Higgsfield generate / Freepik Magnific reimagine / Seedream) for interiors, staging, renders, tight exteriors; **masked inpaint** (Freepik Magnific Retouch / Higgsfield `/image-editing`) for any targeted edit on a detail-heavy exterior — sky, declutter, object removal. ❌ Never run full-frame on a drone wide — it regenerates the ground and wrecks fine detail.

## Magnific MCP server (connected — credit-metered)
A second generation/upscaling platform is wired in as the `magnific` MCP server (HTTP, `https://mcp.magnific.com/mcp`, local config; OAuth). Tools are `mcp__magnific__*`: 46 image models, video, 3D, audio, plus creations/folders/library/spaces. Overlaps Higgsfield/Topaz for upscaling and full-frame generative work — another option in the same pipeline. Full detail + price list in auto-memory `reference-magnific.md`.
- **Every generation costs credits through the MCP** — verified across all 46 image models, none are free. Hunter's account shows `isUnlimitedMode: true`, but that "unlimited" applies only in Magnific's **web app**; the API/MCP path bills credits regardless. Don't quote the API `credits.available` field to Hunter — it doesn't match his dashboard (trust the ~8k shared-add-on figure he sees).
- **Always run `images_simulate_cost` first** (read-only, exact, never charges) and quote the cost, then wait for explicit go-ahead before any `images_*` / `video_*` / `models3d_*` / `audio_*` op. This extends the standing ask-before-upscaling rule to all paid Magnific actions.

## 10x CRM MCP server (connected — source of truth for tasks)
Hunter's own CRM is wired in as the `10x-crm` MCP server (HTTP, `https://crm.10xvisuals.com.au/api/mcp`, local config; OAuth — server may surface under a UUID name in tool lists). Currently exposes two tools: **list personal to-dos** and **create a personal to-do** (title, optional description / ISO due date / low-medium-high priority). **The CRM is the source of truth for Hunter's task list** — check it before answering "what's on my plate", write new tasks/reminders there, and don't duplicate CRM items into `TASKS.md` (which stays a local scratch view at most). More tools (contacts, jobs, deals) may appear as the CRM endpoint grows.

## Productivity-plugin artifacts (generated — don't hand-edit)
- `TASKS.md` — task tracker with `## In Progress / To Do / Done`. Managed by `productivity:task-management`. Superseded by the CRM for real tasks — see *10x CRM MCP server* above.
- `dashboard.html` — a ~3000-line generated dashboard. Regenerated by `productivity:start` / `productivity:update`; don't edit by hand.
- `Welcome.md` — leftover Obsidian starter note; safe to ignore.

## Other files
- `CONTEXT.md` — a domain taxonomy (currently the music-reference library for scoring edits) produced via the grilling skills. Uses **locked terminology with `_Avoid_` lists** — when editing, keep terms consistent with what's already locked there.
- `.github/workflows/claude.yml` — runs the Claude Code GitHub Action on new issue comments and PRs (needs `ANTHROPIC_API_KEY` secret).
- `.gitignore` excludes machine-specific Obsidian state (`workspace.json`, `graph.json`, `.obsidian/cache`, `.trash/`). Don't re-add these to tracking.

## Git
Default branch is `main`. **Commit and push freely without asking** — git operations are free, so autonomous commit/push is fine (and keeps the vault backed up to GitHub). The line is **money, not git**: any action that spends credits or money (Magnific generations, Higgsfield credits, any paid op) ALWAYS needs Hunter's explicit go-ahead first — never spend autonomously. Obsidian writes to `.obsidian/` constantly — expect (and ignore) churn there.
