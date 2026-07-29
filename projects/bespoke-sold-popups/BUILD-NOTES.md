# Bespoke — SOLD pop-ups (9:16)

Three animated lower-third pop-ups for a Bespoke Estate Agents SOLD reel, built off the
structure of Belinda Blucher's "SOLD in 7 Days" reel
(https://www.instagram.com/reel/DVwW3IQkuA_/) but re-cut in Bespoke's brand system.

⚠️ **Reference not seen.** The Instagram video would not decode in the automated browser
(login-walled reel, media never loaded), so the motion here is a Bespoke-brand interpretation
of the three beats Hunter specified, not a frame-match of that reel. Send 3 screen grabs
(one per pop-up) and the timing gets matched exactly.

## Files
- `popups.html` — the animated build. 1080×1920 stage, scaled to fit the window.
- `assets/` — Zodiak Light/Regular (woff2), Poppins Regular/Medium/SemiBold, Bespoke lockup + mark SVGs.
- Local server: `bespoke-popups` in `.claude/launch.json` → http://localhost:8773/popups.html

## Scenes
| # | Content | Motion |
|---|---------|--------|
| 1 | `SOLD` / `$1,125,000` | card rises + un-blurs, hairline wipes L→R, price rises per character (45ms stagger) |
| 2 | Bespoke lockup + "Beyond Luxury Real Estate" | lockup revealed by L→R clip wipe, hairline draws from centre, tagline fades up |
| 3 | 63 Enquiries / 4 Offers / 26 Days on market | rows rise + un-blur, staggered 170ms, hairline divider between each |

Out on every scene: fall 26px + blur 10px + fade, 520ms.

## Controls
Play all · scene 1/2/3 · background cycle (black → Bespoke green → checker → chroma `#00b140` → `assets/plate.jpg` if you drop a still in) · speed 1× / 0.5× / 0.25×.
Keys: `1` `2` `3` scenes · `R` or space replay · `B` background · **`C` hides the control bar** before you record.

## Getting it into the edit
1. `C` to hide controls, background → chroma green (or black if you'd rather comp on Screen/Add).
2. Screen-record the pane at full size, or for real alpha render frames:
   `` chromium --headless --screenshot `` per frame, or just re-time it in FCP off the spec below.
3. Drop over the footage, key the green (Keyer) or use a Screen blend on the black version.

### FCP / Resolve rebuild spec
- Fonts: Zodiak **Light 300** for numbers (never 700+ on Zodiak), Poppins **Medium 500** for caps labels.
- Colours: panel `#132a24` @ 58% + 26px blur behind; text `#F0EDE8`; hairlines `#F0EDE8` @ 34%.
- Type: eyebrow 30px / 0.38em tracking · price 122px · stat numbers 104px · labels 26px / 0.26em.
- Card: 888px wide, 72px padding, 8px radius, 1px border `#F0EDE8` @ 20%, shadow 0 32 90 black 42%.
- Position: 96px side margins, card bottom 300px off frame bottom (clear of IG UI).
- Ease everything on `cubic-bezier(.16,1,.3,1)` (≈ FCP "Ease Out" with a long tail). In 780–900ms, out 520ms.
- Beat lengths at 1×: scene 1 3.0s, scene 2 2.6s, scene 3 3.8s, 180ms gap between.

## Editing the copy
All three scenes are plain HTML in `popups.html` — price, stat numbers and labels are literal text
in `#s1` / `#s3`. Numbers auto-split into per-character spans, so nothing else needs touching.

## Notes
- `impeccable` design hook flags Zodiak and the utility colours (`#000`, `#00b140`, checker greys)
  as outside `DESIGN.md`. Left as-is: Zodiak is Bespoke's brand heading face and those colours are
  the recording backdrops (chroma key / transparency checker), not design surfaces.
- Brand tokens said Zodiak font files were missing — they are in
  `projects/bespoke-scrape/brand/zodiak/`. **⚠️ supersedes** that line in `BRAND-TOKENS.md`.
