---
client: kollosche
address: 5 Esther Place, Surfers Paradise (Villas on Esther, lot 3RP128565)
opened: 2026-10-27
status: delivered           # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 0, aud: 0 }   # derived from - 2026-10-27 stills: 6 drone stills from the SSD (`Done/Drone`) auto-placed with [[drone-photo-pin]] (`stills/`, roof height 10 m). All 6 landed with no drags. Awaiting Hunter's review in the browser.

- 2026-10-27 stills: pin restyled to Kollosche's photo badge (navy square, white K, thin border); thin outline, editable by hand, with a behind brush. Drones-6 outline needs Hunter's hand placement (drone height/heading off). Re-rendered as a draft; final render after Hunter's review.

- 2026-10-27 delivery: Hunter exported Web (pin + outline) and Print (clean) to `Done/Drone Graphics`, and dropped the top-down (Drones-4) because Kollosche doesn't like top-downs.

- 2026-10-27 DELIVERED: Hunter touched up the stills and re-exported all 6 to `Done/Drone Graphics/Print` (full size, 300 dpi, with pin and outline) and `Web` (2048 px, pin and outline), named `5 Esther Place - Surfers Paradise 01–06`. Spend: $0, all local.

## Ledger — never edit by hand
---

# Job — Kollosche townhouse drone graphics

Source clips: `~/Downloads/Kollosche Day to Night/Drones/` (`Main.mp4`, `View.mp4`, both 4K 23.976, 2.0 s).

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | Main (top-down) | local CG overlay, chained SIFT homographies | delivered | White lot outline around the whole townhouse lot (street fence, north boundary, rear timber fence, south wall by the driveway); boundary traced by eye, not from a plan. Draws on from frame 15 once the opening spin and blur settle. Track ≤0.6 px/frame from frame 14. |
| 2 | View (wide to Surfers) | plate-vfx camera solve + KLT roof track | delivered | Kollosche K pin on the townhouse roof (2nd unit), line screen-vertical, K upright. Frame 1 is a cut, so the pin starts on frame 2. Tip KLT track; the camera solve agrees within 3 px median. |
| 3 | Agent outro (Eddie Wardale, 0408 881 678) | `projects/kollosche-outro/make_outro.py` | delivered | Navy overlay + kerned Söhne Breit Kräftig + copyright line, fading in together. Layout measured from Kollosche's Taylor × Thibault card (re-render matches within 0.2 % of pixels). 16:9 + 9:16 ProRes 4444 alpha + PNG in `projects/kollosche-outro/out/`. |

## Log

- 2026-10-27 intake: 2 shots. Hunter asked for the outline (top-down) and a 3D-tracked K pin (wide).
- 2026-10-27 main: plate-vfx track FAILED (blur and spin), so it was re-tracked with chained homographies (`scripts/track_main.py`). Outline rendered.
- 2026-10-27 view: plate-vfx track PASS 0.477 px (free model). Pin rendered (`scripts/render_pin.py`).
- 2026-10-27 review: outputs sent to Hunter. Each shot comes as an mp4 preview, a ProRes 422 HQ comp and a ProRes 4444 alpha overlay in `<shot>/out/`.
- 2026-10-27 delivered: Hunter approved both shots ("looks good").
- 2026-10-27 outro: Hunter asked for the ending. Agent Eddie Wardale, 0408 881 678 (from Hunter). Rendered 16:9 + 9:16.
- 2026-10-27 delivered: Hunter accepted the outro and moved on to the next reels.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- no spend: all local -->

---
_Vault: [[jarvis]]_
