# MVX Meta Creatives

Six assets, three services × two formats. Copy is new; **layout, fonts and colours are unchanged** from the creatives already running.

Regenerate: `python3 build.py`. No credits, no paid APIs — PIL + League Gothic (Google Fonts, vendored) + Poppins (system).

| Service | Square 1080×1080 | Story 1080×1920 | CTA |
|---|---|---|---|
| Aircon | `out/mvx-aircon-1x1.png` | `out/mvx-aircon-9x16.png` | Get your free quote |
| General electrical | `out/mvx-general-1x1.png` | `out/mvx-general-9x16.png` | Get in touch today |
| Hot water | `out/mvx-hotwater-1x1.png` | `out/mvx-hotwater-9x16.png` | Get your free quote |

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
- **Hot water** — ⚠️ `liversaver9.jpg`, **not a hot water photo.** Nothing in MVX's library shows a hot water system. Real crew was chosen over stock because it's on-brand and matches the "we're the electricians" message, but this should be swapped for an actual changeover shot when Matt has one. It's the weakest of the six.

## Notes

- The Google review badge is drawn to match the incumbent creatives (4.9, five stars, "REVIEWS"). Stars are polygons, not glyphs — Poppins has no ★ and renders tofu boxes.
- Green stays an accent: the CTA word, the ticks, the rule and the slabs. Never a background fill, per §04.
- To change wording, edit `SERVICES` at the top of `build.py` and re-run. Nothing else needs touching.

---
_Vault: [[mvx-electrical]] · campaign spec: [BUILD.md](../mvx-meta-rebuild/BUILD.md)_
