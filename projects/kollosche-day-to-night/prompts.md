# Kollosche day-to-night prompts (Villas on Esther)

Model: Magnific `video_modify` with Seedance 2.5. `video_modify` takes no reference image, so the [[house-twilight]] look is written out in words. Pad each clip to at least 4 s with a frozen last frame, then trim back to the source length after generating.

---

## Clip 1: living/dining dolly toward the corner balcony doors (3.46 s)

Convert this footage to real early-evening twilight, about twenty minutes after sunset, keeping the exact camera move, framing, lens and timing, and every wall, fitting, object and piece of furniture exactly as it is, with nothing added, removed or rebuilt. All daylight is gone, with no sun patches and no bright daylight on the floor or curtains. The room is now lit only by its own existing fittings: the recessed ceiling downlights are on and lay soft warm pools of light across the pale floor, the timber dining table and the stone kitchen bench, with gentle scallops of light down the walls. The strip lights under the floating shelves on the dark timber wall glow softly, and the small wall light beside the open staircase is on, grazing the timber treads. Beyond the open corner sliding doors, the existing ceiling downlight on the covered balcony softly lights the outdoor lounge and cushions. Through the glass and the sheer curtains the sky is a clear twilight blue fading to a soft pale peach low on the horizon, and the trees outside become cool blue-grey shapes that keep soft detail. Faint warm reflections of the downlights sit in the dark glass of the sliders. The contrast is warm light inside against cool blue outside, while the room stays bright, clean and clearly readable with true white walls and a natural pale floor, like high-end real estate twilight cinematography rather than a colour filter.

**Plain English:** kill the sun, light the room with its own downlights, shelf strips and stair light, add a blue-to-peach sky through the glass, and keep it bright.
**Pass confidence: 80%.** This is the same kind of shot as the Pottsville v2 win (an interior dolly toward glass, relit from fittings). The main risk is Seedance swapping the sheer curtain glow for a dim grey.

---

## Clip 2: covered balcony with the interior seen through the slider (1.96 s)

Convert this footage to real early-evening twilight, about twenty minutes after sunset, keeping the exact camera move, framing, lens and timing, and every object, surface, plant and building exactly as it is, with nothing added, removed or rebuilt. All sunlight is gone. The covered balcony is lit only by its existing ceiling downlight, which throws a soft warm pool across the outdoor sofa, armchairs, cushions, timber coffee table and pale tiles, while the ceiling fan stays as it is. Through the open sliding door the interior glows warmly from its own fittings: the kitchen downlights are on, the glass pendant over the bench glows amber, the wine fridge is softly lit, and warm light falls on the dining table and the artwork. Above the neighbouring houses the sky is a clean, clear early-dusk gradient, soft mid blue overhead fading to pale cream-peach low on the horizon, with the clouds thinned to almost nothing. The neighbouring white houses, palms and gardens sit in soft, even, cool dusk light and stay clearly readable with natural greens, and no lights are added to them. The pool below keeps its shape, its water turning a deep dusk blue with no lights added. The glass balustrade and the timber handrail pick up faint warm reflections. The contrast is warm amber light inside against cool blue outside, bright and readable, like high-end real estate twilight cinematography rather than a colour filter.

**Plain English:** balcony downlight on, kitchen pendant and wine fridge glowing through the door, clear blue-to-peach sky over the neighbours, and nothing invented on the houses next door or in the pool.
**Pass confidence: 70%.** It has a lot of real sky, so dusk will read clearly. The risks are Seedance switching on windows in the neighbours' houses, or adding pool lights.

---

## Clip 3: close-up through the glass, sofa cushions to balcony chairs and palms (2.00 s)

Convert this footage to real early-evening twilight, about twenty minutes after sunset, keeping the exact camera move, focus, framing, lens and timing, and every cushion, chair, door frame and plant exactly as it is, with nothing added or removed. All sunlight is gone. The sofa cushions in the foreground are softly lit from above by the room's warm ceiling downlights out of frame, with gentle falloff into shadow at their lower edges. Beyond the glass, the outdoor armchair and sofa on the balcony catch a soft warm pool from the balcony's ceiling downlight above them, while the palms and garden behind fall into cool blue-grey dusk tones that keep soft detail, no longer sunlit or yellow-green. A faint warm reflection of the interior sits on the sliding glass and the dark aluminium frame. The contrast is warm light inside and on the balcony against cool blue foliage behind, calm and clearly readable, like high-end real estate twilight cinematography rather than a colour filter.

**Plain English:** warm top light on the cushions and balcony chairs, palms go cool blue, and the glass picks up a warm reflection.
**Pass confidence: 55%.** There is no sky and no light fitting in frame, so the dusk can only be inferred from the colour of the foliage. This is the shot most likely to read as a filter. Consider dropping it from the cut, or pilot it at 720p first.

---

## Clip 4: street front with the "VILLAS ON ESTHER" sign wall, push-in (1.46 s)

Convert this footage to early dusk just after sunset, keeping the exact camera move, framing, lens and timing, and the building, fins, battens, planter greenery, sign wall, driveway, lawn, trees, parked vehicles, power pole and lines exactly as they are, with nothing added, removed or rebuilt. The large number 5 and the lettering "VILLAS ON ESTHER" on the stone sign wall, and the three letterbox plates below it, stay perfectly sharp, legible and unchanged. The sky becomes a clean, clear gradient, soft mid blue overhead fading to pale cream and peach at the horizon, with the clouds cleared to almost nothing and no violet, pink or drama. The small existing downlights in the soffit at the top of each white fin are on, washing soft warm light down the fins, and warm amber light glows from the glazing behind the dark timber battens on the upper floors. The existing small wall lights beside the garage doors are on. No new light fittings are added anywhere: no garden uplights, no street lights, no lights in the sign wall. The driveway, lawn, garden beds and footpath stay bright and clearly readable in soft, even, shadowless dusk light with natural greens. High-end twilight real estate cinematography.

**Plain English:** this is the locked house-twilight look on a ground exterior. The fin soffit lights and the glow behind the battens come on, the sky goes clear blue to peach, the ground stays bright, and the signage is locked letter for letter.
**Pass confidence: 60%.** The look itself is easy, but video_modify repaints every pixel, and Kollosche will notice if "VILLAS ON ESTHER" comes back warped. If the lettering breaks, the fix is to mask the sign wall back in from the source, frame by frame. That's a plate composite, not a re-roll.
