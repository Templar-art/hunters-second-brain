---
type: reference
tags: [post-production, color-grading, davinci-resolve, video]
updated: 2026-10-28
---

# Color Grading

Grading for video (and keeping stills consistent). Balance first, look last, scopes decide.

## Log → Rec.709
- Input transform: colour-managed (Resolve CM / ACES) or a conversion LUT, or manual by eye.
- Convert log to Rec.709 before grading creatively. Set the base, then grade on top.

## Order of operations
1. **Primaries** — balance the shot. WB (temp/tint neutral), lift/gamma/gain, contrast, pivot. Get true whites and clean blacks.
2. **Secondaries** — qualifiers + power windows. Isolate skies, skin, windows, greenery. Track windows on moving shots.
3. **Look** — creative LUT or manual grade last, low opacity, on its own node/layer.

## Scopes are truth
- Waveform: luma/exposure. Whites near top without clipping, blacks off the floor.
- Vectorscope: colour + saturation. Skin sits on the skin-tone line.
- Parade (RGB): channel balance — spot casts, neutralise greys.
- Trust scopes over the monitor.

## Shot matching
- Pick a hero shot per scene/sequence. Match every other shot to it — exposure, WB, contrast, saturation.
- Match cuts side-by-side. No visible jump across an edit.

## The "one grade" premium rule
- One consistent grade across the whole piece — [[brand-system]].
- Unify mixed sources (drone, mirrorless, gimbal, phone b-roll) to a single look. Balance each to neutral, then apply the shared look.

## Property look
- Clean and bright. True whites, neutral WB.
- Interiors slightly warm and inviting. Exteriors punchy but natural — real green grass, blue-not-cyan sky.
- Avoid teal-orange overkill and crushed contrast. Premium reads as clean, not stylised.

## Resolve node/layer order
- Node 1 balance → Node 2 contrast/curves → Nodes 3+ secondaries (windows/sky/skin) → look node last.
- Serial for global, parallel/layer for isolated regions. Keep it readable.

## Export / delivery colour
- Deliver Rec.709, correct levels (video/data range — don't mismatch). Consistent colour across all versions and aspects.
- Loudness (~-14 LUFS) is audio, not colour — set in the mix. Keep the grade identical across 16:9 and 9:16 exports.

## Related
[[video-edit-pipeline]] · [[video-camera-settings]] · [[photo-editing-pipeline]] · [[post-production]]

FCP ↔ Resolve Studio grading round trip: [[fcp-resolve-workflow]].
