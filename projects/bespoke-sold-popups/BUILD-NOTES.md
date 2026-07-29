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

## Aspect
Both 9:16 (1080×1920) and 16:9 (1920×1080) come out of the same markup — type is sized in `em`
off `#stage`'s font-size (100px at 9:16, 74px at 16:9), positions are in `%`. Toggle with the
aspect button or `A`; `?ar=169` loads straight into 16:9.

The frame is `position:fixed` and centred with `translate(-50%,-50%) scale()`, so it is always
fully on screen. (Earlier it was scaled but still laid out at 1080×1920, so the page overflowed
and pushed the frame off the bottom.)

## Rendering to video
```
node tools/render-sequence.mjs 169 ~/Desktop/popups-169 none     # transparent, ProRes 4444 + webm
node tools/render-sequence.mjs 916 ~/Desktop/popups-916 plate    # over the test still, H.264
```
One headless Chrome driven over DevTools Protocol, 25fps, ~80ms a frame — the whole run is under a
minute. Outputs a PNG sequence plus `-alpha.mov` (ProRes 4444, `yuva444p12le`) and `-alpha.webm`
(VP9 alpha) when `bg=none`, or an `.mp4` otherwise.

Alpha masters live on the Desktop (`Bespoke-SOLD-popups/`), not in the repo — 60–90MB each,
gitignored. The small webms are in `preview/`.

Three things had to line up for this to work, all of them non-obvious:
1. **`--default-background-color=00000000` does nothing** in Chrome 150 (and `--headless=old` is gone).
   Transparency comes from CDP `Emulation.setDefaultBackgroundColorOverride` with `a: 0`.
2. **`Page.captureScreenshot` never returns if the page has paused animations.** `renderFrame` used to
   freeze by pausing; it now sets `currentTime`, calls `commitStyles()`, then `cancel()`s — the frame is
   baked into inline styles and no animation is left running. `reset()` restores each element's authored
   `style` attribute (which carries `--d`/`--o`) from a WeakMap.
3. **`--window-size` is not the capture size** — it leaves ~87px of browser chrome out, giving 1920×993.
   `Emulation.setDeviceMetricsOverride` fixes it (and is harmless once #2 is sorted).

`tools/render-frames.sh` is the fallback: one Chrome launch per frame, 6 in parallel, ~6 min. It cannot
do alpha (see #1) so it's plate/black/green only.

The static server is `tools/serve.mjs`, not `python3 -m http.server` — the Python one dies on this Mac
with `'idna' codec can't encode character '\x83'` because `http.server` calls `socket.getfqdn()` on
bind and the machine's hostname isn't ASCII-clean.

## Controls
Play all · scene 1/2/3 · background cycle (black → Bespoke green → checker → chroma `#00b140` → `assets/plate.jpg` → none) · speed 1× / 0.5× / 0.25×.
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
