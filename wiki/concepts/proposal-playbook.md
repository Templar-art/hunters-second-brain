---
type: concept
tags: [proposal, pricing, positioning, pitch, retainer]
updated: 2026-07-17
---

# Proposal Playbook

Evergreen recipe for pitching a content retainer, distilled from the three-iteration Anthony/Hattie Boydle proposal (July 2026). Worked example: [projects/anthony-proposal/](../../projects/anthony-proposal/) — `proposal-anthony.html` (source) and `Hattie Boydle - Content Partnership Proposal.pdf` (delivered). Client trail: [[anthony]].

## 1. Style the doc to the recipient's world, not 10x branding

When pitching a **personal brand**, the proposal should look like it already belongs in their feed — 10x branding on the doc reads as "our template", theirs reads as "we get you". The Hattie doc took three passes to learn this: v1 shipped generic, v2 rebuilt in her dark athletic-luxury world (near-black, champagne-bronze, condensed caps, an outlined "2X" champion motif from her actual title), v3 settled on a warm editorial system. The lesson survived all three: pull motifs from the recipient's identity (titles, handle, niche aesthetic) into the design itself. Keep 10x presence to a footer line (name + email).

## 2. Delivery pipeline: self-contained HTML → Chrome print-to-PDF

Fonts embedded as **data-URI `@font-face`** so the single HTML file renders identically anywhere, plus an `@media print` block (`print-color-adjust: exact`, `break-inside: avoid` on cards/tables, tightened padding), then Chrome headless print-to-PDF. Shared mechanics — logo embedding, exact Chrome invocation — already documented in auto-memory `reference-cost-breakdown-deliverable.md`; use that, don't rebuild.

## 3. Incumbent-comparison table, quality-over-quantity framing

A "current setup vs this partnership" table converts the prospect's existing frustration into the pitch. Rows that worked: monthly cost, deliverables (moving target → fixed in writing), scope, posting, point of contact (account manager → direct line to the person filming). **Never out-promise on volume when a tool can out-promise you** — OpusClip quotes 32 clips/episode; the proposal offered 16 framed as "cut for the hook, not the timestamp… 16 that are actually worth posting". Curated count beats inflated count, and it's a commitment you can actually keep.

## 4. Pricing structure

- **Undercut the incumbent visibly** — $1,500 vs their current $2,000, and *say the saving out loud* ("$500 a month back in your pocket for more output").
- **Shortfall-carry-over guarantee** — if a month falls short on our end, the shortfall carries over at no cost. Turns "fixed deliverables in writing" from a claim into a mechanism, and directly answers the over-promise/under-deliver wound the incumbent left.
- **90-day term, no lock-in beyond it, no setup fee** — low-risk entry for a burned prospect.

## 5. Structure that landed

Hero (their name + one-line promise) → pain section naming their exact frustration → deliverables ledger with big numbers → "how a month runs" week-by-week table → incumbent comparison → investment block → 3-bullet getting-started. Every number is written as a commitment, not a pitch.

## Craft
Wider business craft this recipe sits inside: [[business-craft]] · [[pricing-and-packaging]] · [[lead-gen-and-sales]] · [[client-onboarding]].
