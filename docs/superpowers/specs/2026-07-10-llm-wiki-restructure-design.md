# LLM Wiki Restructure — Design

**Date:** 2026-07-10
**Status:** Approved by Hunter
**Pattern:** Karpathy LLM Wiki (raw sources / wiki / schema, index.md + log.md)

## Goal

Convert Hunter's Second Brain vault from an ad-hoc `memory/` tree + root notes into a three-layer LLM-maintained wiki: immutable **raw sources**, an LLM-owned **wiki** of interlinked markdown pages, and CLAUDE.md rewritten as the **schema** that tells Claude how to maintain it.

## Target structure

```
Hunters Second Brain/
├── CLAUDE.md          # SCHEMA: wiki conventions + ingest/query/lint workflows.
│                      # Operational sections KEPT: Higgsfield routing, Magnific
│                      # cost gate, 10x CRM, git rules, two-memory-systems note.
├── wiki/
│   ├── index.md       # catalog of every page, by category, one-liner each
│   ├── log.md         # append-only: ## [YYYY-MM-DD] ingest|query|lint | Title
│   ├── overview.md    # synthesis: 10x Visuals at a glance
│   ├── people/        # lachlan, damon, tyson, kris, hunter
│   ├── clients/       # coast-life-constructions, bespoke-estate-agents,
│   │                  # belle-property, cva, jang
│   ├── projects/      # 10x-ig-repositioning, clc-ig-repositioning,
│   │                  # music-library, board-committee-headshots,
│   │                  # 10x-scroll-build, board-committee-bts-edit-plan
│   ├── concepts/      # higgsfield-pipelines, staging-rules, brand-system,
│   │                  # ig-caption-voice, music-taxonomy (from CONTEXT.md),
│   │                  # glossary terms promoted to pages
│   └── sources/       # one summary page per ingested raw source
├── raw/
│   ├── assets/        # Obsidian attachment target
│   └── clc/           # CLC capability statement, pack PDFs, field research,
│                      # swipe file, audit PDF
├── projects/          # working deliverables (NOT knowledge)
│   ├── 10x-scroll-build/   # demo index.html + frames (moved from root)
│   ├── cva/                # cva_breakdown.html/pdf
│   └── dashboard.html, TASKS.md
└── (root)             # Welcome.md and empty 2026-06-15.md deleted
```

## Decisions

1. **Full conversion** — `memory/` retired; content translated (not just moved) into wiki pages with YAML frontmatter (`type`, `tags`, `updated`) and `[[wikilinks]]`.
2. **CLAUDE.md two halves** — wiki schema (structure, conventions, ingest/query/lint) + operational rules (Higgsfield, money gate, CRM, git). Memory tables at top replaced by a pointer to `wiki/index.md` + `wiki/overview.md`.
3. **CLC pack markdown files** become `wiki/sources/` pages; their PDFs and reference material go to `raw/clc/`.
4. **CONTEXT.md** → `wiki/concepts/music-taxonomy.md`, locked terminology and `_Avoid_` lists preserved verbatim.
5. **log.md genesis entry** documents this migration; all future ops append.
6. **Auto-memory (~/.claude) untouched** — boundary stated in schema: vault wiki = business knowledge; auto-memory = Claude working preferences/feedback.
7. **git mv** wherever possible; single commit; push (autonomous git is standing policy).
8. Working artifacts (`10x Scroll Build/`, `cva_breakdown.*`, `dashboard.html`, `TASKS.md`) move under top-level `projects/` — referenced from wiki pages but outside the wiki.

## Out of scope

- No qmd/search tooling yet (index.md sufficient at this scale).
- No changes to `.agents/` vendored skills, skills-lock.json, `.github/`, `.obsidian/`.
- No Dataview/Marp setup.
