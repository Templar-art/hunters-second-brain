# CLAUDE.md — Wiki Schema + Operating Rules

This repo is **Hunter's Second Brain**: an Obsidian vault structured as an **LLM-maintained wiki** (Karpathy pattern). It is not a software project — nothing to build, lint, or test. Claude maintains the wiki; Hunter curates sources, directs analysis, and asks questions.

**Response style — ALWAYS:** caveman ultra (`~/.claude/skills/caveman`, level `ultra`). Every conversation in this vault, every response. Terse fragments, abbreviate prose (DB/config/req), arrows for causality. Wiki PAGES + code + commits stay normal prose. Off only if Hunter say "stop caveman".

**Who:** Hunter, videographer at 10x Visuals (founded by Tyson, CEO) (10xvisuals.com.au), hunter@10xvisuals.com.au. Start any session's orientation at `wiki/overview.md` and `wiki/index.md`.

---

# Part 1 — The Wiki Schema

## Layers
```
raw/        IMMUTABLE source material (PDFs, clippings, data). Read, never modify.
            raw/assets/ is the Obsidian attachment target. One subfolder per client/topic (raw/clc/…).
wiki/       LLM-owned knowledge. Claude writes and maintains ALL of it; Hunter reads.
            index.md   catalog of every page (category → link + one-liner). Update on every ingest.
            log.md     append-only ops record: ## [YYYY-MM-DD] ingest|query|lint|migrate | Title
            overview.md the synthesis — current state of 10x, updated when the picture shifts.
            people/ clients/ projects/ concepts/ sources/
projects/   Working deliverables (demos, generated HTML/PDF, TASKS.md, dashboard.html) —
            referenced FROM wiki pages, not part of the knowledge layer.
docs/       Specs and process docs (superpowers).
```

## Page conventions
- Kebab-case filenames; one entity/concept per page.
- YAML frontmatter: `type` (person|client|contact|project|concept|source|overview), `tags`, `status` where useful, `updated` (ISO date — bump on every edit).
- `[[wikilinks]]` liberally between pages; Obsidian resolves by filename. Link raw files and deliverables with relative markdown links.
- Contradictions: when a new source contradicts an existing claim, flag it inline (**⚠️ supersedes/contradicts…**) rather than silently overwriting; keep the dated trail.
- `wiki/sources/clc-*.md` are the **living, editable** versions of the CLC pack; the PDFs in `raw/clc/` are the frozen originals.

## Operations
- **Ingest** (new source dropped in `raw/` or pasted): read it → discuss takeaways → write/update a `sources/` page → update every affected entity/concept page → update `index.md` → append to `log.md`. A single ingest may touch many pages; that's the point.
- **Query**: read `index.md` first, drill into pages, answer with citations. If the answer is a durable artifact (comparison, analysis, connection), file it back into the wiki as a page and index it.
- **Harvest** (a job or deliverable finishes; `/harvest`): every folder under `projects/` needs a wiki page or a paragraph on an existing one — client, what shipped, cost, and what it taught us — then index + log. **A `projects/` folder with no wiki page is a leak**, and the JOB.md is not a substitute: nobody reads it from `index.md`. Same for a `feedback-*` written to auto-memory during a job — the standing-rule page it belongs to (e.g. [[staging-rules]]) gets updated in the same breath, or the rule only exists in one system.
- **Lint** (on request or periodically): hunt contradictions, stale claims, orphan pages, missing cross-references, concepts mentioned but pageless. Also diff `projects/*/` and the auto-memory dir against the wiki — that gap is where knowledge actually goes missing. Log the pass.
- **"Remember this"**: repo/business facts → wiki pages here. Cross-project Claude preferences/feedback → auto-memory (`~/.claude/projects/.../memory/`, its own MEMORY.md index, loaded via system reminders). Two systems — don't confuse them. Auto-memory holds the full AI-workflow KB, brand guidelines, and feedback files the wiki pages point to.

## Obsidian conventions
Daily notes `YYYY-MM-DD.md`; `.base`/`.canvas` are plugin documents — don't hand-author internals unless asked. `.gitignore` excludes machine-specific Obsidian state; don't re-add.

---

# Part 2 — Operating Rules (the actual work)

## Higgsfield / AI generation
The substantive tasks are AI image/video generation for real-estate clients. Routing, models, and hard rules: `wiki/concepts/higgsfield-pipelines.md` + `wiki/concepts/staging-rules.md`; full KB in auto-memory `ai-realestate-workflow.md`.
- **Vendored skills** in `.agents/skills/` (pinned by `skills-lock.json`) are read-only vendored content — update via sync tooling, never hand-edit. Read the relevant `SKILL.md` before generating; discover models with unfiltered `higgsfield model list` / `workflow list`.
- **Route before generating:** full-frame generative for interiors/staging/renders/tight exteriors; masked inpaint for targeted edits on detail-heavy exteriors. ❌ Never full-frame a drone wide.
- **Job tracking (Jarvis):** every 10x job gets a `JOB.md` in its job folder — copy `projects/jarvis/JOB-template.md` at intake, update on EVERY state change (generation, approval, redo, delivery, every credit spent). Cost tally always current. Spec: `docs/superpowers/specs/2026-07-10-jarvis-phase2-job-tracking-design.md`.

## Magnific MCP (credit-metered)
`magnific` MCP server (46 image models, video, 3D, audio). **Every MCP generation costs credits** — "unlimited" is web-app only. Enforced by `.claude/hooks/magnific-gate.py` (paid tools blocked in bypass mode until Hunter's message starts with yes/go/approved; never write its state file). Always `images_simulate_cost` first (free, exact), quote the cost, and wait for explicit go-ahead before ANY paid op. Don't quote the API `credits.available` to Hunter (trust his ~8k dashboard figure). Full detail: auto-memory `reference-magnific.md`.

## 10x CRM MCP (source of truth for tasks)
`10x-crm` MCP server (may surface under a UUID). Check it before answering "what's on my plate"; write new tasks/reminders there. `projects/TASKS.md` is a local scratch view at most.

## Git
Default branch `main`. **Commit and push freely without asking** — git is free and keeps the vault backed up. The line is **money, not git**: anything that spends credits (Magnific, Higgsfield, any paid op) ALWAYS needs Hunter's explicit go-ahead. Expect and ignore `.obsidian/` churn.

## Misc
- `.github/workflows/claude.yml` runs Claude Code on issue comments/PRs (needs `ANTHROPIC_API_KEY`).
- `projects/dashboard.html` + `projects/TASKS.md` are productivity-plugin artifacts — regenerated, don't hand-edit.
- Brand quick facts: colour #61a8d8, Poppins/Montserrat → `wiki/concepts/brand-system.md`.
