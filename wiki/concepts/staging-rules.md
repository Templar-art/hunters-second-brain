---
type: concept
tags: [virtual-staging, workflow, rules]
updated: 2026-09-15
---

# Virtual Staging Rules

Standing rules for AI staging of listing photos, distilled from job feedback (canonical versions in auto-memory `feedback-*` files). Pipeline routing → [[higgsfield-pipelines]].

- **Preserve fixtures** — never change taps, windows, vanities, or any fixed element; only movable furniture, décor, declutter.
- **One-shot staging** — must land in one pass (volume work); pick self-enforcing geometry (e.g. round dining table when end-chairs are the risk).
- **Phrase positively** — "open/empty ends + exact count"; negation alone fails on Nano Banana.
- **Default model:** Nano Banana Pro for full-frame staging.
- **Vary plants** — never the same plant across rooms in one listing (fig/kentia/rubber/olive/monstera rotation, white pots).
- **Vary bed styling** — no two beds dressed identically; vary ≥2 of cushions/throw/coverlet/pillow stack.
- **Room hierarchy** — secondary bedrooms one step below primary (bed-width headboard, single bedside, ≤3 cushions).
- **Fridge isolation** — kitchen staging: isolate the fridge in its own pass, name the door, freeze island size.
- **Ask the room type** — never infer master/guest/secondary from a photo; ask Hunter before labelling or setting the styling tier.
- **Ask if the property is low-end** — if it is, stage every room to feel as large as possible (corner placement, minimum footprint, open floor).
- **No wall art by default** — don't add paintings or framed art above beds; Nano Banana defaults to it, so phrase the bare wall positively and expect to mask residuals.
- **One bedside lamp** — Nano Banana Pro spawns a second floating lamp; enforce the count with geometry and a positive number, never negation.
- **No detail vignettes in wide frames** — desks, laptops and small props read as "past the couch" in a wide; save them for the close-up.
- **Lock placement with three anchors** — every major piece (bed, sofa, dining table) gets: same footprint as the piece it replaces, axis tied to a named fixed feature ("back parallel to the left-hand window wall"), and a directional cue ("chaise extending toward the camera", "not rotated or squared to the camera"). A bare wall label alone has failed twice; don't skip it because the layout looks obvious.
- **Curtains by default, frame-locked** — every stage/restyle prompt checks each visible window and glass door for existing curtains; any bare one gets full-height sheers added without being asked. Anchor each panel to its own frame explicitly ("width matching only its own frame's width... no fabric spanning between separate frames or extending onto the plain wall") — an un-anchored curtain instruction bled a single sheer across an entire wall on the first attempt. See [[feedback-curtains-default-and-anchor]].
- **Matching angles need a reference** — every room angle after the first must pass the approved frame as `@reference`; standalone prompts only for the first frame of a room.
- **Token the images** — multi-image staging/transfer prompts use `@original` / `@reference` tokens plus a legend, so images can be swapped without reading the prompt body.
- **Outdoor = outdoor furniture** — patios get weatherproof pieces in the client palette (never indoor furniture), and fences are pinned with "nothing new built".
- **Reference-transfer SOP** (Freepik) and **Magnific upscale recipe** — auto-memory `reference-staging-transfer-sop`, `reference-magnific-upscale-recipe`, `reference-freepik-staging-workflow`.

## Craft
Prompting patterns behind these rules: [[ai-prompting]]. Tool selection: [[ai-image-tools]]. Shooting the source photos: [[interior-photography]].
