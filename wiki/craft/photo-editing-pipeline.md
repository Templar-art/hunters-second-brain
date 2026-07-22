---
type: reference
tags: [post-production, photo-editing, lightroom, photoshop, real-estate]
updated: 2026-07-19
---

# Photo Editing Pipeline

Real-estate / architectural stills. Lightroom for baseline + volume, Photoshop for blending and clean-up.

## 1. Cull
- Import, flag/reject fast. One hero per angle. Kill blinks, soft frames, dupe brackets you won't use.
- Keep bracket sets grouped for flambient/blend shots.

## 2. RAW baseline (Lightroom)
- White balance: neutral. Match to a known-white surface. Avoid orange interiors from tungsten — correct toward neutral.
- Exposure: set for the room, not the window (windows get pulled later).
- Lens corrections: enable profile, remove CA.
- [[perspective-correction]]: Transform → verticals straight. Keep some ceiling/foreground; don't over-crop.
- Highlights down, shadows up modestly. Don't crush or clip.

## 3. Local adjustments
- Masks: brighten ceilings, recover window frames, tame hotspots, lift dark corners.
- Selective WB fixes for mixed lighting (warm lamps vs cool daylight).

## 4. Blend in Photoshop ([[exposure-blending]])
- Flambient: ambient/base exposure + flash frames + window (darker) exposure.
- Manual luminosity masks or layer masks. Brush windows in from the darker bracket.
- Fix flash reflections and colour casts per frame. Believable, not HDR halos.

## 5. Clean-up
- Remove: bins, cords, remotes, stray reflections (tripod, photographer in mirrors/glass), sensor dust.
- Clone/heal/content-aware. Straighten art, tidy staging.
- Sky replacement when flat/blown — realistic, matched to scene light and direction. Don't oversaturate.

## 6. Colour consistency across the set
- Pick the look on one hero image. Sync/paste settings to the set.
- Uniform WB, exposure, and tone room-to-room. A gallery should read as one shoot — [[brand-system]] one look.

## 7. Sharpen + export
- Output sharpening for screen. Resize per deliverable (MLS/web vs print).
- sRGB for web, correct dimensions, consistent naming.

## Do / Don't
- Verticals straight. Natural whites. Clean, colour-neutral windows. Believable skies.
- Don't over-HDR, don't crush blacks, don't leave orange interiors, don't halo edges.

## Volume workflow
- Edit hero → sync to set → spot-fix outliers. Presets for recurring clients (e.g. [[coast-life-constructions]]).
- Batch export with saved presets.

## Handoff (offshore editor — jang-studio)
- Consistent written brief: WB target, vertical correction, window pulls, sky policy, delete-object list, export specs.
- Supply a graded reference frame. Review round, then lock.

## Downstream: virtual staging
- AI virtual staging is a separate path on empty rooms — see [[staging-rules]]. Don't blend into the base edit; version it.

## Related
[[color-grading]] · [[exposure-blending]] · [[perspective-correction]] · [[post-production]]
