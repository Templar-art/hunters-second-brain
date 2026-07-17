---
name: harvest
description: Use when a project in projects/ is finished or a deliverable has shipped and its lessons should be distilled into the wiki — trigger on "harvest", "/harvest <project>", "that job's done, write it up", or when closing out a job/JOB.md.
---

# Harvest — distill a finished project into the wiki

## Overview

Wiki pages are earned, not drafted from thin air: when a project ships, harvest what was *learned* (not what was done — git history already records that) into durable wiki knowledge. One harvest may touch several pages; that's the point.

## Inputs

`/harvest <project-folder-or-name>` — e.g. `/harvest anthony-proposal`. If no argument, list `projects/` folders modified recently and ask which one.

## Workflow

1. **Read the project**: the project folder in `projects/` (JOB.md first if present), plus any wiki pages that already reference it (grep `wiki/` for the project name).
2. **Extract learnings, not events.** Ask of the material: what would change how the *next* job is done? Candidates:
   - a reusable technique or recipe → `wiki/concepts/` page (new or updated)
   - a fact about a client/contact → update their `wiki/clients/` or `wiki/people/` page
   - pricing/positioning insight → `wiki/overview.md` if it shifts the 10x picture
   - a proven prompt/pipeline setting → the relevant concept page (e.g. staging-rules, higgsfield-pipelines)
3. **Write/update wiki pages** following vault conventions: kebab-case, YAML frontmatter (`type`, `tags`, `updated` bumped), `[[wikilinks]]` between pages, relative markdown links back to the project deliverables in `projects/`. If a new claim contradicts an existing one, flag inline (**⚠️ supersedes…**) — keep the dated trail.
4. **Cross-link both ways**: the project's JOB.md (or a short HARVESTED.md note in the folder) links to the wiki pages created; each wiki page links back to the project folder. If no JOB.md exists, note the gap (backfill from `projects/jarvis/JOB-template.md` only if the job is still active) — HARVESTED.md is the cross-link fallback.
5. **Update `wiki/index.md`** — add/adjust one-liners for every page touched.
6. **Append to `wiki/log.md`**: `## [YYYY-MM-DD] harvest | <project> → <pages touched>`.
7. **Commit** with message `harvest(<project>): <one-line summary>`.

## Rules

- Distill: a harvest that copies the project file into wiki/ has failed. Wiki pages are shorter than their sources and written as evergreen reference.
- Skip harvests with nothing durable — say so, log `harvest | <project> → nothing durable`, and stop. Not every job teaches something.
- Outcome-dependent claims (deal not closed, result unverified) get marked **provisional** with a date; harvest the technique now, the verdict at close.
- Never modify `raw/` or delete anything in `projects/`.
- Routing new knowledge: business-facing knowledge (clients, pricing, positioning, techniques as concepts) → wiki; cross-project build recipes/templates → auto-memory. If auto-memory already holds the lesson (check MEMORY.md index), point the wiki page at it rather than duplicating.

## Common mistakes

| Mistake | Fix |
|---|---|
| Writing a project diary ("we did X then Y") | Write only what changes future behaviour |
| One giant harvest page | Route each learning to the entity/concept page it belongs on |
| Appending more diary to a live-maintained client page | Harvest's job there is to *compress* the chronology into evergreen form + cross-link, not add events |
| Forgetting index.md / log.md | Steps 5-6 are mandatory, every time |
