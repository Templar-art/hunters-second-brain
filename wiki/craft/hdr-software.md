---
type: reference
tags: [hdr, software, editing, exposure, real-estate]
updated: 2026-07-19
---

# HDR Software

## What HDR merge does
Combines a bracket (e.g. -2 / 0 / +2 EV) into one high-range file. Pulls shadow and highlight detail from separate frames into a single image that holds both bright windows and dark corners.

## The tools and their character
- **Lightroom / ACR HDR Merge** — creates a floating-point 32-bit `.DNG` you then edit like any normal raw. Natural, non-destructive, full slider range. The safe default. Best starting point.
- **Aurora HDR / Photomatix** — dedicated tone-mappers. Powerful, fast presets, but easy to overcook into the crunchy look. Use with restraint if at all.
- **Photoshop Merge to HDR Pro** — capable but dated; the LR/ACR path is cleaner for most jobs.

## The key distinction
- **HDR MERGE (good)** — extend dynamic range into one editable file, then edit it normally. Looks like a photo.
- **Aggressive TONE-MAPPING (bad for property)** — local contrast cranked, halos, over-saturation, muddy midtones, glowing window frames. The "HDR look." Reads as amateur to agents and buyers.

## When to use which
- **HDR merge** = fast, decent, high volume. Good for standard real-estate turnaround where speed and consistency matter. See [[real-estate-vs-architectural]].
- **Manual luminosity blending / flambient** = the premium, natural, controllable route for high-end architectural and hero shots. See [[exposure-blending]].
- Honest positioning: HDR merge is the **quick path**; flambient is the **quality path**.

## Avoiding the "HDR look"
- Turn down / off any tone-mapping, "HDR" or "structure" sliders.
- Keep Clarity, Texture, Dehaze low. Keep Saturation/Vibrance natural.
- Keep contrast realistic — no flattened, milky midtones.
- Natural whites, clean neutral WB.
- No halos around window frames, roof lines, or backlit edges.

## Ghosting / deghosting
- Bracket on a tripod so frames align. See [[metering-and-dynamic-range]].
- Enable Deghost (Low → High) for moving foliage, water, ceiling fans, cars.
- Higher deghost = fewer ghosts but can reintroduce blown highlights; use the lowest level that clears the motion.

## After the merge
A merged DNG is a starting point, not a finished frame. It still needs a normal edit: [[perspective-correction]], WB, tone, crop, then [[color-grading]] and set consistency across the whole shoot. See [[photo-editing-pipeline]].

## Related
[[architectural-photography]] · [[exposure-blending]] · [[metering-and-dynamic-range]] · [[photo-editing-pipeline]] · [[real-estate-vs-architectural]] · [[strobe-lighting]] · [[color-grading]]
