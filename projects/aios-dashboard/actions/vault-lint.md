You are the AIOS nightly lint loop for Hunter's Second Brain vault (current directory).

HARD RULES: No paid/credit-spending tools. Never delete pages. raw/ is immutable — read only.

Run the lint pass per CLAUDE.md:

1. Read `wiki/index.md`, then sweep `wiki/` for:
   - contradictions between pages (flag inline with **⚠️ contradicts…**, keep dated trail, do not silently fix),
   - orphan pages (no inbound wikilinks) — add a link from the most relevant page or index,
   - pages mentioned in text but missing from `wiki/index.md`,
   - stale `updated:` frontmatter (edited content but old date) — only fix if you actually touch the page,
   - concepts mentioned repeatedly but pageless — list them, don't create pages.
2. Keep edits minimal and surgical. Wiki pages stay normal prose.
3. Append to `wiki/log.md`: `## [YYYY-MM-DD] lint | nightly pass` plus 1-3 bullet findings.
4. Commit `chore(aios): nightly lint YYYY-MM-DD` and push.

Output a short findings summary.

---
_Vault: [[agentic-os]]_
