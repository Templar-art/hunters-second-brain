# Seedance prompt — Salisbury scroll hero (run in Higgsfield yourself)

Attach in Higgsfield/Seedance in this order:
1. `120 Kennedys Lane-17.jpg` — front facade, dusk, warm entry light (start frame + world plate)

**Seedance prompt — 10s**

```
Scene & Mood: A finished brick family home at dusk, presented like the closing shot of a build film — still, proud, lit from within, the camera drawing slowly toward the front door as the last daylight fades.

Frame Map: The house fills the frame edge to edge exactly as composed in @image1 — gabled two-storey wing in the left third, arched dormer and entry porch at center, chimney wing in the right third, hedges and gravel drive across the lower edge. The glowing entry door sits at center, x=50%, midground. Sky holds the upper fifth as negative space.

Subject Lock — @image1: The house, gardens, hedges, driveway, trees, and sky are locked to @image1 — identical architecture, brickwork pattern, roofline, window placement, landscaping, and dusk light throughout. Warm interior light in the entry, dormer, and left upper windows stays on and steady. No people, no vehicles, no animals enter the frame.

Cross-Frame Rules: Single continuous take. The building never warps, windows never shift, rooflines hold straight. Only the camera's forward travel changes the composition.

Movement: The camera pushes forward slowly and evenly for the full ten seconds, travelling from the street edge toward the entry porch at walking-approach pace, the hedges sliding past the lower frame edges with natural parallax as the door grows from 8% to 16% of frame height. Foliage on the flanking trees drifts gently in a light evening breeze, the entry light flickers once almost imperceptibly like a warm filament, thin clouds crawl at the horizon. Nothing else moves.

Last Frame: The entry porch and glowing front door centered and dominant, dormer above it cresting the top third, both brick wings falling away to the frame edges with soft parallax blur at the extreme corners, sky deepened one stop darker than the opening. No on-screen text, no captions, no signage typography, no rendered text in the frame.

World Plate: Anchored to @image1 — Northern Rivers acreage at dusk, minutes after sunset, clear sky fading from pale blue to deep slate, manicured box hedges, raked gravel drive, mature jacaranda and palms flanking the facade, warm tungsten interior light spilling from the entry and upper windows.

Sound Bed: Diegetic only — evening cricket bed, light breeze through foliage, distant single bird call, faint gravel settle, no music, no dialogue.

Capture Realism: The facade sits inside real depth — light dusk atmosphere suspended in the air between camera, hedges, house, and the treeline behind, the background trees rendered softer, desaturated, and lower-contrast than the brickwork so the house sits within the air rather than pasted on a flat plane. Low-contrast curve — shadows lifted gently holding texture in the eaves and porch, highlights on the lit windows rolled off softly never clipping to white, nothing crushed to black. All specular highlights removed from glass, brick, and roof tiles, every surface reading matte and diffuse. Slightly desaturated grade with the warm window light preserved.

Camera Capture: wide-latitude cinema capture, vintage 35mm 2x anamorphic character at a wide aperture — oval bokeh, soft edge falloff — light diffusion bloom softening the lit windows, extremely slow continuous push-in only, color-negative film rendition with fine grain, palette grade #1c2430, #3a4756, #8a7350, #d99a4e, #efece4, light atmospheric haze, weathered material detail, 24fps 180° shutter, 10 seconds. No humans, environment is the subject.
```

Mode M5 (atmospheric, environment is the subject). After it renders: download →
`ffmpeg -i render.mp4 -vf "fps=12" -q:v 3 "frames/f_%04d.jpg"` → page updates itself.
Generation happens in YOUR Higgsfield session (credits are yours to click) — nothing
has been generated or spent by this prep.
