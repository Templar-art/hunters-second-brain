# 10x Visuals Social Redesign — Editorial System

Date: 2026-06-18
Status: Approved (Hunter), ready to build

## Problem
The first social set (44 posts, `Marketing and Social Media/build_all.py`) read as templated and cheap. Hunter's confirmed faults:
1. Thin white **edge frame** — tacky.
2. Bottom **tick-mark / crosshair "datum" texture** — filler clutter.
3. **Generic blue gradient** on every tile — SaaS-default, not a visual agency.
4. **Dead space** on text tiles, headline floating.
5. Faded giant **X watermark** — cliché.
6. **Photo tiles too dark** — scrim crushed the photography.

## Direction (chosen from 3 mockups)
**Editorial, photo-first.** Rejected: bold flat-type, split-block, flat colour fields ("tacky").
Every tile carries a graphic — no flat colour tiles at all.

## The system — one skeleton, two photo treatments
Shared skeleton on every tile:
- **Logo:** real white wordmark PNG (`10xVisuals_White Logo Blue X.png`), top-left, ~230px wide, soft drop shadow. Never a text wordmark.
- **Bottom band:** kicker + headline, bottom-anchored. Optional body (≤2 lines) + footer (url + action).
- **Kicker:** Montserrat 700, uppercase, letter-spaced, light-blue `#8ec6e8` (chosen for legibility over photo).
- **Headline:** Poppins 700, white, bottom-anchored so 2 vs 3 lines never shift the layout.

Two treatments:
- **`photo`** (photo posts): full-bleed shoot frame + gradient scrim (transparent → navy `#102f41` ~0.95 at base). Default.
  - **`photoband`** fallback: denser solid-ish band for bright/busy frames where the gradient won't hold the label.
- **`duotone`** (text posts — tips/FAQ/process/hooks/angles/templates): shoot frame tinted deep navy (navy base + photo at reduced opacity + navy→blue tint overlay) behind the same band. Photographic, never flat.

## Removed
Edge frame, datum tick/crosshair texture, X watermark, sky/blue gradient fields, flat navy tiles, fake text wordmarks.

## Palette
Navy `#102f41` / deeper `#0d2734`, blue `#61a8d8`, kicker light-blue `#8ec6e8`, white. No dashes in copy — middots `·` and slashes `/` only.

## Assets
Photos: `~/Desktop/Edited Photos/` (5 drone DJI, ~10 ground DSC, 1 render). Logo: `~/Desktop/10x Final Cut stuff/`.
Render: cairosvg + PIL via `~/.claude-tools/Skill_Seekers/.venv/bin/python`.

## Scope
- Rewrite `build_all.py` to a single `tile()` builder with the three treatments; convert all existing post copy; assign a photo to every post; add extra posts ("go ham").
- Regenerate `posts/` + `GRID_MOCKUP.png`.
- Local renders only — no credits, no paid ops.

## Out of scope
Flat-colour treatments (revisit later — "ditch the coloured stuff for now"), light/white-background tiles (blocked on a dark-logo export).

---
_Vault: [[10x-social-engine]]_
