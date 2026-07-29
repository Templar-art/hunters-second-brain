---
client: bespoke-estate-agents
address: n/a — social template (SOLD reel pop-ups)
opened: 2026-07-29
status: review        # intake → generating → review → delivered
cost: { credits: 0, aud: 0 }
---

# Job — Bespoke SOLD reel pop-ups (9:16)

Reference: Belinda Blucher "SOLD in 7 Days" reel — https://www.instagram.com/reel/DVwW3IQkuA_/
Brief: same three pop-up beats, Bespoke brand. No paid generation involved (HTML/CSS build).

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | Scene 1 — SOLD $1,125,000 | HTML/CSS overlay | built | per-char rise, hairline wipe |
| 2 | Scene 2 — Bespoke lockup | HTML/CSS overlay | built | L→R clip reveal + tagline |
| 3 | Scene 3 — 63 Enquiries / 4 Offers / 26 Days | HTML/CSS overlay | built | 170ms row stagger |

## Log

- 2026-07-29 intake: 3 pop-up scenes specified by Hunter.
- 2026-07-29 build: `popups.html` + Zodiak/Poppins/logo assets; `bespoke-popups` server on :8773;
  all 3 scenes verified in browser. Reference reel could not be decoded in the automated browser
  (IG login wall), so motion is a brand interpretation — awaiting 3 frame grabs from Hunter to frame-match.
- 2026-07-29 reference: pulled the reel with `yt-dlp`, stepped at 2fps. Real treatment = no panels,
  centred white bold sans, **numbers count up**, blocks accumulate. First pass (glass cards, lower third)
  was wrong; parked as `popups-cards.html`.
- 2026-07-29 rebuild: `popups.html` reference-matched — Zodiak Light Italic "Sold", Poppins Bold numbers
  with count-up, accumulating stat stack. All 3 scenes verified over a real Bespoke plate.
- 2026-07-29 16:9: same markup now renders both aspects (em-based type off the frame). Fixed the
  frame falling off screen (scaled but still laid out at 1080x1920 → page overflowed).
- 2026-07-29 delivered preview: `preview/popups-16x9.mp4` (1920x1080, 10s) + 6 stills.
  Render tooling in `tools/`. CDP renderer hangs on captureScreenshot with paused animations; use the shell script.
- 2026-07-30 alpha: transparent renders working — CDP background override (the Chrome flag is dead),
  frozen frames now baked with commitStyles instead of paused (paused animations wedge captureScreenshot),
  device-metrics override for exact frame size. ProRes 4444 + VP9 alpha, both aspects, ~50s a run.
  Masters on Desktop `Bespoke-SOLD-popups/`; webms in `preview/`. Static server swapped to `tools/serve.mjs`
  (python http.server dies on this Mac's hostname).
- 2026-07-29 cost: 0 credits. Nothing paid touched.

---
_Vault: [[jarvis]] · [[bespoke-estate-agents]]_
