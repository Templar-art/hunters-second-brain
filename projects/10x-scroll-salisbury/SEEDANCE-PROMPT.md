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

---

# v2 — "BUILT BEFORE YOUR EYES" (approved concept, generation on hold 14 Jul)

The upgrade Hunter wants: the scroll IS the build — slab to finished home, longer runtime.
Run in Higgsfield web app (plan credits) or via API when approved
(quotes 14 Jul: 2.0 Mini 15s 720p = 2,100 cr · 1.5 Pro 12s 1080p = 1,320 cr · 2.0 Pro 8s 1080p = 5,600 cr).

Attach: `120 Kennedys Lane-17.jpg` as image reference (the finished house — the film must END on it).

**Seedance prompt — 15s**

```
Scene & Mood: A family home builds itself before the viewer's eyes — from bare earth to a finished brick residence glowing at dusk — one continuous time-lapse take, calm and inevitable, like watching months compress into seconds.

Frame Map: Fixed composition matching @image1 — the build occupies the full frame edge to edge, gabled two-storey wing rising in the left third, entry porch at center, chimney wing in the right third, hedges and gravel drive arriving across the lower edge late in the take. Sky holds the upper fifth throughout.

Subject Lock — @image1: The finished house in @image1 is the destination — identical architecture, brickwork pattern, roofline, window placement, landscaping, and dusk light must be reached by the final second. No people, no vehicles, no machinery in frame; the build assembles cleanly, materials rising and settling into place.

Cross-Frame Rules: Single continuous take, locked camera position with a very slow push-in. The footprint never shifts, walls rise plumb, the roofline arrives straight. Daylight wheels overhead as the build progresses and lands at dusk for the finish.

Movement: 0–3s — bare graded earth and a fresh concrete slab under bright midday light, timber wall frames rising plumb along the footprint. 3–6s — the skeleton completes, roof trusses sweeping into place left wing first, then center, then right. 6–9s — brickwork climbs the walls course by course in the herringbone-accented pattern, window frames setting into their openings. 9–12s — dark roof tiles roll across the trusses, glass glazes the windows catching the lowering sun, the arched dormer takes shape at center. 12–15s — the light falls to dusk, hedges and gravel drive settle into the foreground, warm interior light ignites in the entry and windows, and the frame resolves exactly into @image1. Thin clouds crawl throughout; the sun's angle wheels gently from midday to dusk.

Last Frame: Exactly the finished home of @image1 — dusk sky, warm windows lit, entry glowing at center, hedges full. No on-screen text, no captions, no signage typography, no rendered text in the frame.

World Plate: Northern Rivers acreage; the day compresses from clear midday through golden hour to dusk across the runtime, clear sky throughout, mature flanking trees constant at the frame edges.

Sound Bed: Diegetic only — soft wind bed, distant timber knocks and settling materials low in the mix, evening crickets fading in over the final three seconds, no music, no dialogue.

Capture Realism: The build sits inside real depth — light atmosphere suspended between camera, structure, and the treeline behind, background rendered softer and lower-contrast than the rising brickwork. Low-contrast curve — shadows lifted gently, highlights rolled off softly never clipping, nothing crushed to black. All specular highlights removed from glass, brick, and tiles, every surface matte and diffuse. Slightly desaturated grade, warmth preserved, the dusk finish matching @image1's palette.

Camera Capture: wide-latitude cinema capture, vintage 35mm 2x anamorphic character at a wide aperture — oval bokeh, soft edge falloff — light diffusion bloom on the lit windows in the final seconds, locked position with extremely slow continuous push-in only, color-negative film rendition with fine grain, light atmospheric haze, 24fps 180° shutter, 15 seconds. No humans, environment is the subject.
```

After render: `ffmpeg -i build.mp4 -vf "fps=24" -q:v 3 "frames/f_%04d.jpg"` → set FRAME_COUNT
to the frame count (15s ≈ 360) → captions in index.html can gain per-stage lines
(SLAB. / FRAME. / BRICK. / ROOF. / HOME.) keyed to scroll ranges.
