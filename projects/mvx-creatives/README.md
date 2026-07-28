# MVX Meta Creatives

Six assets, three services × two formats. Copy is new; **layout, fonts and colours are unchanged** from the creatives already running.

Regenerate: `python3 build.py`. No credits, no paid APIs — PIL + League Gothic (Google Fonts, vendored) + Poppins (system).

| Service | Square 1080×1080 | Story 1080×1920 | CTA |
|---|---|---|---|
| Aircon | `out/mvx-aircon-1x1.png` | `out/mvx-aircon-9x16.png` | Get your free quote |
| General electrical | `out/mvx-general-1x1.png` | `out/mvx-general-9x16.png` | Get in touch today |
| Hot water | `out/mvx-hotwater-1x1.png` | `out/mvx-hotwater-9x16.png` | Get your free quote |
| **New builds & renos** | `out/mvx-newbuild-1x1.png` | `out/mvx-newbuild-9x16.png` | Request your free quote |

**New builds & renos is the live one.** It's the offer for the current campaign
(see `../mvx-meta-rebuild/BUILD-NEWBUILDS.md`). The other three are symptom-led
and belong to the superseded three-service plan; keep them, don't run them yet.

## Copy rules applied

- **No pricing.** Hunter's call: public numbers invite comparison shopping and date instantly.
- **No same-day or guaranteed-time promises.** "Get in touch today" is an instruction to the reader, not a promise from MVX.
- **No fear or urgency**, per Brand Guidelines §07. Bullets name the symptom the homeowner already has; nothing threatens them.
- One service per creative. Problem-led bullets, not service-list bullets.
- Square carries 5 bullets, story carries the first 4. Order the list accordingly.

## Photos

Real MVX imagery only, chosen off a contact sheet rather than filenames.

- **Aircon** — `79233.jpg`, split-system service. The shot already used in the incumbent creative.
- **General electrical** — `liversaver10.jpg`, real crew in hi-vis at a panel. Per §06 this beats stock, which the guide explicitly rejects.
- **Hot water** — `hotwater-wide.jpg` (square) and `hotwater-tall.jpg` (story), stock supplied by Hunter 28 Jul. A tech at a wall-mounted unit. Each format gets the crop that suits it, via `photo_sq` / `photo_st`.

## Headline sizing

The square headline **fills the left column top to bottom**. Both the green and
white lines wrap, and the block is set at the largest shared size where every
line fits the column and the whole thing fits the available height.

Sizing off the longest single line instead left short headlines ("Electrical
problems at home?") floating in void space, which was the first thing Hunter
picked up. Longer headlines now come out smaller and taller, shorter ones bigger,
and either way the column is full.

## Cropping a wide photo into the story format

The story block is roughly 0.70 aspect and every source photo is 3:2, so a plain
crop keeps only about half the width. When the subject is small in frame that
loses the action: the new-build shot cropped straight onto the tradesman's
shoulder, then onto bare brick, and read as a photo of a wall.

`crop_st` fixes it. It takes a normalised `(x0, y0, x1, y1)` region of the source
and applies it *before* the fit, so you can frame the part that matters. The
new-build story uses `(0.28, 0.30, 0.94, 1.0)` to land on the hand, pliers and
cable. `fx_st` / `fy_st` bias the remaining crop if that's all you need.

## Notes

- The Google review badge matches the incumbent creatives (4.9, five gold stars, "REVIEWS"). Stars use the real glyph from Arial Unicode: Poppins has no star, and my first attempt at drawing them as polygons looked wrong.
- **The story is ONE photo.** A single image sits behind the lower two thirds; the white CTA panel is drawn over it, so the photo shows above the panel and again below the green band. It is not two crops.
- Green stays an accent: the CTA word, the ticks, the rule and the slabs. Never a background fill, per §04.
- To change wording, edit `SERVICES` at the top of `build.py` and re-run. Nothing else needs touching.
- `fx_sq` / `fy_sq` bias the square's crop, but every current photo is 3:2 against a 1.38:1 frame, so there's only ~90px of horizontal play. It won't reposition a subject out from under the headline; the dark scrim is what keeps the type legible. Left at centre.

---
_Vault: [[mvx-electrical]] · campaign spec: [BUILD.md](../mvx-meta-rebuild/BUILD.md)_
