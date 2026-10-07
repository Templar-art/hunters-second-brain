---
type: concept
tags: [virtual-staging, workflow, rules]
updated: 2026-10-07
---

# Virtual Staging Rules

Standing rules for AI staging of listing photos, distilled from job feedback (canonical versions in auto-memory `feedback-*` files). Pipeline routing → [[higgsfield-pipelines]].

- **Preserve fixtures** — never change taps, windows, vanities, or any fixed element; only movable furniture, décor, declutter.
- **One-shot staging** — must land in one pass (volume work); pick self-enforcing geometry (e.g. round dining table when end-chairs are the risk).
- **No end chairs, every dining table, by default** — never rely on saying "no end chairs" (negation is unenforced on Nano Banana). Default to a round or oval/pedestal table shape with no flat end to seat someone at, and when chairs are still needed spell out the count and placement explicitly ("N chairs evenly spaced around it, none at the ends"). Apply this on every dining prompt without being asked. See [[feedback-no-end-chairs-positive]].
- **Phrase positively** — "open/empty ends + exact count"; negation alone fails on Nano Banana.
- **Default model:** none confirmed — ask (see below). Nano Banana Pro was the assumed default until 2026-09-15.
- **Two bedsides always** — a table + lamp on both sides of every bed, master or secondary; the secondary tier-down applies to bedding and styling, never to dropping a bedside. See [[feedback-two-bedsides-always]].
- **TV front only** — wall-mount the TV with only its screen visible, no cables or rear panel. See [[feedback-tv-never-show-back]].
- **Restrained light, balanced exposure** — "soft natural window light, gentle directional shadows, subtle warmth, no dramatic light beams or haze", and "natural true-to-life exposure, neither dark/moody nor blown-out". Streaming-rays wording blows out and mesh-shadows; golden/editorial reads moody, bright/airy overshoots. See [[feedback-sun-ray-restraint]], [[feedback-staging-brightness-default]].
- **Explain + score every prompt** — each prompt handed over carries a plain-English "what this changes" summary and a pass-confidence score. See [[feedback-prompt-explain-and-score]].
- **No default model** — Nano Banana Pro was assumed, not confirmed; zed-full-house actually ran on GPT Image 2.5 Sunburst. Ask which model before writing the prompt. Sunburst: standalone full-text restyles work, reference transfer is unreliable. See [[feedback-gpt-image-sunburst]].
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
- **Every pass runs from the raw** — redos go back to the original photo, never on top of a previous AI output (quality degrades). Consequence for redo prompts: they must be complete standalone descriptions restating every change, including the ones that already landed. Carry-over wording ("keep the credenza as it is, that part is correct") silently preserves the *original* furniture when the input is the raw.
- **Curtains by default, frame-locked** — every stage/restyle prompt checks each visible window and glass door for existing curtains; any bare one gets full-height sheers added without being asked. Anchor each panel to its own frame explicitly ("width matching only its own frame's width... no fabric spanning between separate frames or extending onto the plain wall") — an un-anchored curtain instruction bled a single sheer across an entire wall on the first attempt. See [[feedback-curtains-default-and-anchor]].
- **Lock the camera framing** — type an explicit framing lock into every prompt ("keeps the exact camera position, focal length, framing and perspective of the original — identical composition and crop"). GPT Image 2.5 Sunburst silently re-crops and zooms otherwise, and a re-framed shot can't sit beside the rest of the set. See [[feedback-lock-camera-framing]].
- **Square to the room** — furniture aligned straight against its wall, rug edges running parallel to the walls and along the floor's grout lines or floorboard direction, art hung "centred and level". Without it, rugs render visibly twisted and the furniture on them reads wrong. The models have no depth map — naming a line that actually exists in the frame is the only real anchor, and furniture against a wall beats anything floating mid-room. See [[feedback-square-to-the-room-geometry]].
- **Mirrors must reflect the staging** — mirrored wardrobes, bathroom mirrors and angled glass render the *empty* room unless the reflection is described explicitly ("the bed, bedside table and rug visible in the reflection, correctly reversed and in true perspective"). An unreflected bed discredits the whole set at a glance. See [[feedback-mirrors-must-reflect-staging]].
- **Exact inventory, or it invents** — list the room's contents up front ("the room contains exactly these pieces and nothing more: ..."). Without it, Sunburst adds consoles nobody asked for and layers a second rug.
- **Name what a piece would displace** — placing furniture on a wall already occupied by a fixture makes the model delete the fixture. A display cabinet vanished when a sofa was assigned to its wall; reposition the furniture, or state the fixture stays and nothing sits in front of it.
- **Prompts in prose, not checklists** — deliverable prompts read as flowing description, never bold region headings or token legends, and never cite an internal style-guide sheet as a reference image. See [[feedback-prompt-prose-not-checklist]].
- **Orient devices to the seat** — a laptop or screen must face the chair it serves, not the camera; the model defaults to screen-to-camera. Say "screen turned to face the chair, camera sees the plain lid back with no logo". Built-in shelves are fixtures: name them "built-in" and lock timber, size and position. First tried on Nano Banana 2.1 (Jessica Wallace office, 7 Oct) — held framing and fixtures in one pass.
- **Matching angles need a reference** — every room angle after the first must pass the approved frame as `@reference`; standalone prompts only for the first frame of a room.
- **Token the images** — multi-image staging/transfer prompts use `@original` / `@reference` tokens plus a legend, so images can be swapped without reading the prompt body.
- **Outdoor = outdoor furniture** — patios get weatherproof pieces in the client palette (never indoor furniture), and fences are pinned with "nothing new built".
- **Reference-transfer SOP** (Freepik) and **Magnific upscale recipe** — auto-memory `reference-staging-transfer-sop`, `reference-magnific-upscale-recipe`, `reference-freepik-staging-workflow`.

## Craft
Prompting patterns behind these rules: [[ai-prompting]]. Tool selection: [[ai-image-tools]]. Shooting the source photos: [[interior-photography]].
