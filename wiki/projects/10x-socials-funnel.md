---
type: project
tags: [10x-visuals, instagram, tiktok, strategy, branding]
status: active
updated: 2026-07-14
---

# 10x Socials Funnel — vertical accounts → master curation

Sibling initiative to [[10x-ig-repositioning]] (which is scoped to @10xvisuals.co alone). This one splits volume by vertical and uses the master account as a curated best-of, not a firehose.

## The architecture
- **Master** — `@10xvisuals.co` (existing, unchanged). Only the best work lands here — the funnel destination.
- **Real estate** — new account, all RE content (full volume, no curation bar).
- **Construction** — new account, all construction content (full volume, no curation bar).
- Bio links: master's bio points out to both verticals; each vertical's bio points back to master ("Best of it all → @10xvisuals.co").

## Handles (checked live, 13 Jul 2026)
| Vertical | Instagram | TikTok |
|---|---|---|
| Real estate | `10x.realestate` (free) | `10x.realestate` (free) |
| Construction | `10x.construction` (free) | `10xconstruction` — **note: no dot.** `10x.construction` is squatted on TikTok by a dead unrelated account (2 followers) |

Platforms: IG + TikTok only at launch (Hunter's call). Facebook auto-links via IG cross-post — no dedicated FB content plan. YouTube deferred until IG/TikTok cadence is proven.

## Colour system — ⚠️ reversed 13 Jul 2026, same day
First call (13 Jul, AM): per-vertical recolour (navy RE / orange construction), an explicit override of the brand guideline's "never recolour the X" rule — see git history / earlier revision of this page.
**Overturned same day (PM):** Hunter's boss directed plain white profile photos across all three accounts, no per-account colour coding. This actually restores the original brand guideline (never recolour the X) rather than breaking it — the override didn't survive contact with the boss. Colour differentiation between accounts is dropped entirely; all three (master + both verticals) use the same plain-white 10X mark as profile photo.

The orange/navy SVG/PNG pairs are left in `assets/` for the record but **not used** — superseded by the all-white version below.

**Bug found while building the white version:** the "canonical" all-white icon at `~/Desktop/General Folder/10xVisuals_10X Symbol White.svg` is NOT actually all-white — only one of the X's two diagonal strokes was whitened; the other is still the blue gradient (confirmed by diffing it against the Blue X source — one line differs, the rest of the X-stroke fills are untouched). `reference-brand-assets` auto-memory previously took this file's filename at face value; corrected there too. Built a true all-white replacement instead.

**Assets produced:**
- [10X Symbol All-White.svg](../../projects/10x-socials-funnel/assets/10xVisuals_10X%20Symbol%20All-White.svg) / [.png](../../projects/10x-socials-funnel/assets/10xVisuals_10X%20Symbol%20All-White.png) — **the profile photo, used identically on all three accounts**
- Rendered on brand navy `#102f41` background — the white mark is invisible on white/transparent per the existing asset note in `reference-brand-assets`; dark bg is the correct usage, matches how the white master logo is already used.
- Superseded (not used): Orange X / Navy X variants, still in the same folder.

## Bios + highlight structure (drafted, approved as-is 13 Jul 2026)

**@10x.realestate**
> Real estate content by 10x Visuals
> Listings shot to sell, not just look nice
> Best of it all → @10xvisuals.co

Highlights: Listings · Drone · Before/After · Process · Client Love

**@10x.construction** (IG) / **@10xconstruction** (TikTok)
> Construction content by 10x Visuals
> Builds documented, first cut to handover
> Best of it all → @10xvisuals.co

Highlights: Builds · Progress · Drone · Process · Client Love

## Launch packs — BUILT (14 Jul 2026, for launch "tomorrow")
Everything an account needs on day one, on the Desktop, rendered through the [[10x-social-engine]] (tenx):
- **`~/Desktop/10x REALESTATE - LAUNCH/`** — 5 highlight covers (Listings/Drone/Before·After/Process/Client Love, white mark on dimmed photo) + 6 launch feed posts with captions (Bowsprit twilight, 88 Third, Dungogie, Ocean Shores, staging, aerial) + README + TALKING-HEADS.md.
- **`~/Desktop/10x CONSTRUCTION - LAUNCH/`** — 5 covers (Builds/Progress/Drone/Process/Client Love) + 6 posts (Broncos, Hour Glass + Bell Street from reel framegrabs, toolbox BTS, Criterion mid-fitout, Ladds Ridge aerial) + README + TALKING-HEADS.md.
- Builder: `10x Premium Kit/build_vertical_launch.py` (re-runnable).
- **Caption policy split:** verticals carry 3 niche hashtags per post (growth accounts); master stays hashtag-free organic. `[@handle]` blanks to verify before posting.
- **Cadence decided:** launch week = 1 post/day per vertical, then 4–5/wk (Tue + Fri talking heads); master unchanged. Backfill = yes — vertical accounts are full-volume by design.

## Talking-head system — BUILT (14 Jul 2026)
`projects/10x-socials-funnel/TALKING-HEADS.md` (copied into both launch folders): shooting format (batch 6 per sitting, 30–45s, hook in 2s, burned captions, vertical), script format (HOOK/MEAT/ENDER + caption), **12 scripts ready** — 6 RE (twilight window, virtual staging, film v slideshow, drone altitude, first-photo psychology, shoot-day walkthrough) + 6 construction (document-or-lose-it, post-the-build, toolbox talks, drone progress sets, fitout window, progress-film cost) — plus the weekly cadence table for both accounts.

## Status / what's left
- **Account creation itself is Hunter's to do** — needs login/email/password, which is outside what Claude will do. Handles, bios, profile photo, covers, first 6 posts and 6 scripts per account are all staged; creating + filling the accounts is now a one-morning job.
- Master bio copy update (add the two outbound links) still pending.
- Website/10xvisuals.com.au funnel explicitly out of scope for this initiative (Hunter's call, 13 Jul) — socials only.
