# Log

Append-only record of wiki operations. Entry format: `## [YYYY-MM-DD] ingest|query|lint|migrate | Title`

## [2026-07-10] migrate | Genesis — vault restructured to LLM-wiki pattern
Converted the vault to the Karpathy LLM-wiki structure (spec: `docs/superpowers/specs/2026-07-10-llm-wiki-restructure-design.md`). `memory/` retired and translated into `wiki/` (5 people, 5 clients, 6 projects/concepts pages); CLC pack PDFs + capability statement moved to `raw/clc/`; CLC pack markdown, audit, field research, and swipe file became `wiki/sources/` pages; CONTEXT.md → [[music-taxonomy]]; root notes → wiki/projects/; working artifacts (scroll demo, CVA breakdown, dashboard, TASKS) → top-level `projects/`; CLAUDE.md rewritten as the schema.
