---
type: project
tags: [10x-visuals, instagram, design-system, content-engine]
status: active
updated: 2026-07-14
---

# 10x Social Engine — System, Audit + SOPs

The unified graphics + content system for @10xvisuals.co. Strategy lives in [[10x-ig-repositioning]]; this page is the operating system: what exists, the gap audit (14 Jul 2026), and the SOPs that keep content flowing. Design spec codified in repo-root `PRODUCT.md` + `DESIGN.md` (impeccable).

## The engine (one system, no drift)

`~/Desktop/General Folder/10x Premium Kit/` — everything renders through the shared module `_engine/tenx.py` (fonts, tracked type, shadow, cover crop, **adaptive whisper gradient** that deepens on bright frames, dim, white mark). Builders are thin scripts on top:

| Builder | Output | Formats |
|---|---|---|
| `build_10x_feed.py` | `~/Desktop/10x FEED - READY TO POST/` | project card, craft card, recap, pure hero, carousel closer + caption.txt each |
| `build_10x_stories.py` | `stories/` | 9:16 story cards + craft openers (IG safe zones) |
| `build_10x_premium.py` | `highlight_covers/`, `samples/` | highlight covers (white mark on dimmed photo, per boss) |
| `build_10x_reels.py` | `reels/` | **NEW** — transparent title-card overlay PNGs for Final Cut + burned 9:16 reel covers (title inside the 4:5 grid-crop band); framegrabs pulled from the reel files by % position |
| `build_10x_ads.py` | `ads/` | **NEW** — premium ad cards (photo + film title + ONE conversion line + small mark), 4:5 + 9:16 each. Replaces the 52-tile look for paid |
| `build_grid_preview.py` | `GRID_PREVIEW.jpg` | 3-col profile-order rhythm check before posting |

**The 52-tile editorial arsenal is retired for everything.** Grid was already ruled out ([[10x-ig-repositioning]] v2); ads now have the premium format above. Keep the files but nothing new ships from `build_all.py`.

## Gap audit (14 Jul 2026)

Ranked by Hunter's priorities (volume/cadence, reels, ads first):

| # | Gap | Status after this pass |
|---|---|---|
| 1 | **Volume/cadence** — 10 feed posts ≈ 5 weeks, then dry; no refill loop | SOP below: the engine turns every delivered job into feed + story + reel assets in one run. Bottleneck is library ingestion, not design |
| 2 | **Tue reel slot had no system** | ✅ Built: FCP overlay + cover per reel; 3 reels ready (Criterion, Hour Glass, Bell Street). Cutting stays in FCP |
| 3 | **Ads/lead gen had only the rejected tiles** | ✅ Built: 3 premium ad cards × 2 placements (listings / builders / staging). Captions per [[../concepts/brand-system]] ad formula |
| 4 | **Nothing posted yet** — bubbles, stories, feed all sitting on Desktop | On Hunter: post per pack READMEs. Everything is blocked behind this |
| 5 | **3 pins** (showreel / meet 10x / how-a-shoot-works) not built | Needs footage decisions — next session with Hunter |
| 6 | **Bio not updated** | 30-second manual change; text in [[10x-ig-repositioning]] |
| 7 | **Credit loop not systemised** | SOP below — deliverable line goes in JOB.md template |
| 8 | **Monthly recap reel** (AC Media pattern) | Recap card exists; reel = monthly FCP cut, overlay from `build_10x_reels.py` |
| 9 | **Before/after staging format** | Not built — no before-frames in the library yet. Add befores to job folders (SOP) and it's one builder away |

## SOPs

### Monthly content flow (the volume fix)
1. After each job delivers: drop 3–5 best frames into `10x Library/<project>/` + best verticals into `_Selected` candidates; reel export into the project folder. (Add to JOB.md checklist.)
2. Contact-sheet the new frames, pick, add entries to `build_10x_feed.py` / `build_10x_stories.py` / `build_10x_reels.py`, rerun.
3. `build_grid_preview.py` → check rhythm (no two title-cards adjacent, heroes breathe between).
4. Post: Thu + Sun feed, Tue reel, stories → matching highlight bubble same day.
5. Month end: recap card (+ recap reel when running).

### Credit loop (the growth channel)
Every delivery email + JOB.md gets the line: *"When posting, please credit @10xvisuals.co in the caption (Filmed and edited by @10xvisuals.co)."* Collab-post wherever the client agrees. Track "how did you hear" against it.

### Before posting ANY asset
- Verify handles against live profiles; fill `[@handle]` blanks.
- Check the client's live feed — never re-post already-published media ([[../concepts/brand-system]] rules; the Chambers miss).
- No third-party branding/pins/watermarks in frames (client's own branding in their doco film is fine).

## Rules baked into the engine
No dashes (middot/slash only) · white Poppins tracked type only · adaptive scrim, never tiles/bands · titles are film titles ("THE BOWSPRIT.") · heroes stay zero-type · one property per cover, varied properties per pack · organic captions no hashtags/CTA, ads get exactly one conversion line.
