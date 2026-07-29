# Bespoke — SOLD pop-ups (9:16)

Three animated pop-ups for a Bespoke Estate Agents SOLD reel, built to match the pop-up
treatment in Belinda Blucher's "SOLD in 7 Days" reel
(https://www.instagram.com/reel/DVwW3IQkuA_/), re-typeset in Bespoke's own faces.

## Files
- `popups.html` — **the build.** Reference-matched: no panels, white type straight on the footage, numbers count up.
- `popups-cards.html` — first pass (glass cards, lower third, hairlines). Kept as an alternative look.
- `assets/` — Zodiak Light + Light Italic, Poppins Medium/SemiBold/Bold, Bespoke lockup + mark, `plate.jpg` (test still).
- `reference/` — frames pulled from the reference reel: contact sheet, title card, stat stack.
- Server: `bespoke-popups` in `.claude/launch.json` → http://localhost:8773/popups.html

## What the reference reel actually does
Pulled the reel with `yt-dlp` and stepped it at 2fps (`reference/reference-contact-sheet.jpg`):

- **No cards, no panels, no hairlines.** Plain white type sitting directly on the footage with a soft drop shadow.
- **Centred**, not lower-third. Title block sits ~top third; the stat stack sits centre.
- **Title card (0–3s):** script "Sold" (~300px) / "IN" small caps / "7 DAYS" heavy sans, tight stack, slight overlap.
- **Stat stack (4–13s):** numbers **count up** — 3→9→17→24→29→30+ enquiries, 62→4,038→6,099→9,282→10,000+ views.
  Each block is a big bold number with a small bold caps label under it. Blocks **accumulate** down the frame
  (enquiries → social views → PREMIUM MARKETING → PROVEN IN THE RESULT) and all clear together.
- `+` sits to the right of the number, ~45% size, raised.
- **Closer:** "WANT RESULTS LIKE THIS?" bold caps centred, then agent name + contact + agency logo.

The count-up is the signature move. That's the bit worth stealing.

## How this build maps onto it
| # | Content | Motion |
|---|---------|--------|
| 1 | `Sold` / `for` / `$1,125,000` | Sold + for pop in, price counts $0 → $1,125,000 over 1.7s |
| 2 | Bespoke lockup + "Beyond Luxury Real Estate" | lockup pops in, tagline follows at 0.62s |
| 3 | 63 Enquiries → 4 Offers → 26 Days on market → "Premium marketing, proven" | blocks accumulate ~1s apart, each number counting up |

Every element: in = rise 30px + scale 0.965→1 + blur 9px→0, 740ms on `cubic-bezier(.16,1,.3,1)`.
Out = fall 18px + blur, 460ms. Beats at 1×: 3.6s / 2.8s / 5.2s, 200ms gap.

**Brand deviation, deliberate:** numbers and labels are **Poppins Bold**, not Zodiak. Zodiak Light 300 vanishes
over busy footage at reel scale, and the reference look depends on heavy sans weight. Zodiak Light *Italic* carries
the word "Sold" — the on-brand stand-in for the reference's brush script (Bespoke has no script face).

## Controls
Play all · scene 1/2/3 · background cycle (black → Bespoke green → checker → chroma `#00b140` → `assets/plate.jpg`) · speed 1× / 0.5× / 0.25×.
Keys: `1` `2` `3` · `R`/space replay · `B` background · **`C` hides the control bar before you record**.

## Getting it into the edit
1. `C` to hide controls, `B` to chroma green (or black for a Screen/Add comp).
2. Screen-record the pane, key the green, drop over the footage.
3. Or rebuild in FCP off the spec below.

### FCP / Resolve spec (1080×1920)
- Fonts: **Poppins Bold** numbers + labels · **Zodiak Light Italic** for "Sold" · Poppins Medium for the tracked-caps line.
- Colour: pure white `#FFFFFF`. Shadow: `0 6px 34px rgba(0,0,0,.42)` + `0 1px 3px rgba(0,0,0,.30)`.
- Scene 1: "Sold" 280px (line-height .86) · "for" 58px / 0.34em tracking · price 138px. Block top at y≈330.
- Scene 2: lockup 660px wide, top y≈640 · tagline 36px / 0.36em, 70px below.
- Scene 3: numbers 112px · labels 54px / 0.02em, 16px under the number · 86px between blocks · kicker 54px, 96px gap.
- Count-up easing: ease-out cubic. Enquiries 1.5s, offers 0.9s, days 1.1s, price 1.7s.

## Editing the copy
Numbers live in `data-count` (`data-prefix="$"` for the price, `data-dur` for roll length); labels are plain text.
Nothing else to touch.

## Notes
- `impeccable` design hook flagged Zodiak and the utility colours (`#000`, `#00b140`, checker greys) in the cards
  version. Left as-is: Zodiak is Bespoke's brand heading face and those colours are recording backdrops
  (chroma key / transparency checker), not design surfaces.
- Brand tokens claimed the Zodiak font files were missing — they are in `projects/bespoke-scrape/brand/zodiak/`.
  **⚠️ supersedes** that line in `BRAND-TOKENS.md`.
