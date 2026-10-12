# Writes one Sunburst staging prompt per shot (ZED Option 04 Riviera Resort) + an index with summary and pass score.
LOCK = "The photograph keeps the exact camera position, focal length, framing and perspective of the original, identical composition and crop, with every wall, ceiling, cornice, window, shutter, door, floor surface, ceiling fan, air-conditioning unit, light fitting and power point exactly where it is."
LIGHT = "Soft natural daylight from the existing windows, gentle directional shadows, true-to-life exposure that is neither moody nor blown out, real contact shadows under every piece, and every piece square to the walls."
FIX = "All existing taps, tapware, fixtures, windows, doors, vanities, cabinetry and tiles unchanged."
R = "in a Mediterranean-resort style of sand linen, natural oak, honed travertine, woven paper cord and muted clay"
S = {}
def add(id, room, route, body, summary, score):
    S[id] = (room, route, body, summary, score)

add("DSC05720","Master bedroom","full-frame",
f"This photograph shows the master bedroom restyled {R}. All of the owners' furniture and belongings are gone: the timber bed, bedsides, chest of drawers, the large timber dressing table in the right foreground, bags and every loose item, leaving the charcoal carpet clear. The room contains exactly these pieces and nothing more: one low natural-oak king bed with a sand linen padded headboard standing on the same footprint as the original bed, its headboard flat against the back wall directly below the air-conditioning unit and its foot pointing toward the camera; one rounded natural-oak bedside on each side of the bed, each holding exactly one clay-glazed ceramic lamp; and a large natural jute rug under the lower two thirds of the bed with its edges parallel to the walls. The bed is dressed in washed white linen with two white pillows, two sand cushions and one muted clay throw folded across the foot. The mirrored wardrobe doors on the right reflect this same restyled room, correctly reversed. {LOCK} {LIGHT} {FIX}",
"Strips the owners' bedroom and puts in a Riviera oak king, two matching bedsides and lamps, and a jute rug. The mirrored robe shows the new room.",55)

add("DSC05735","Master bedroom (to robe and ensuite)","full-frame",
f"This photograph shows the master bedroom looking toward the walk-in robe and ensuite, restyled {R}. The foreground right shows the foot corner of a low natural-oak king bed dressed in washed white linen with a muted clay throw, replacing the original bed. The timber drawers at the far left and the bedside at the far right become a rounded natural-oak bedside holding one clay-glazed lamp on the right and nothing on the left. Inside the walk-in robe the clothing is reduced to a calm, sparse row of neutral garments on the rail, with the floor and shelves clear of bags, boxes and shoes except two neat pairs. The ensuite is tidy with nothing on the floor. {LOCK} {LIGHT} {FIX}",
"Swaps the bed edge and bedside for the Riviera pieces and thins the walk-in robe down to a few neutral clothes.",60)

add("DSC05740","Secondary bedroom (was nursery)","full-frame",
f"This photograph shows a secondary bedroom restyled {R}, a simpler tier than the master. Every nursery item is gone: the cot, change table, rocking chair, globe, toys, oil heater, humidifier, side table and lamp, the moon mirror and wording on the left wall, the star decals and the wall-mounted camera arm. The room contains exactly these pieces and nothing more: one queen natural-oak bed with a slatted oak headboard against the right-hand wall below the air-conditioning unit, its foot pointing toward the mirrored wardrobe; one small rounded oak bedside on each side of the bed, each holding exactly one ceramic lamp; bedding of white linen with one sand throw and two white pillows. No rug, bare charcoal carpet. The mirrored wardrobe doors reflect this same restyled room, correctly reversed. {LOCK} {LIGHT} {FIX}",
"Turns the nursery into a calm guest bedroom: oak queen, two bedsides and lamps, no rug. The mirror shows the new room.",55)

add("DSC05750","Secondary bedroom (was kid's room)","full-frame",
f"This photograph shows a secondary bedroom restyled {R}. Every child's item is gone: the house bed and canopy net, the white dresser in the foreground, the small table, lamp, armchair, soft toys and the framed pictures on the left wall. The pink painted feature wall with its dragonfly artwork stays exactly as it is. The room contains exactly these pieces and nothing more: one queen natural-oak bed with a sand linen headboard against the pink feature wall, its foot pointing toward the left wall; one small rounded oak bedside on each side of the bed, each holding exactly one ceramic lamp; bedding of white linen with one muted clay throw and two white pillows. No rug, bare charcoal carpet. {LOCK} {LIGHT} {FIX}",
"Clears the kid's room and stages a guest bedroom. The pink feature wall stays, because walls are fixtures.",55)

add("DSC05765","Main bathroom","full-frame",
f"This photograph shows the main bathroom, decluttered and lightly styled {R}. The bath toys, loofahs, the toy holder and the small items on the vanity are gone. The towel rail on the right holds exactly two sand linen towels folded over it, the vanity holds exactly one matte clay jug and one small stoneware soap bottle, and the bath edge holds one rolled white towel. {LOCK} {LIGHT} {FIX}",
"Declutter only: toys out, two sand towels, a clay jug and a soap bottle in.",75)

add("DSC05770","Upstairs landing","full-frame",
f"This photograph shows the upstairs landing, decluttered. The black baby gate at the top of the stairs is gone and the timber stair balustrade is fully visible. Through the open door the bedroom shows a low natural-oak bed in washed white linen and a rounded oak bedside with a clay lamp in place of the original furniture. Walls are clean with no hooks or marks. {LOCK} {LIGHT} {FIX}",
"Removes the baby gate and updates the bedroom glimpse through the door.",70)

add("DSC05775","Stairwell","full-frame",
f"This photograph shows the stairwell, decluttered: the small dark object at the bottom right of the stair rail is gone, and the walls are clean. The pendant light, louvre window, stairs, carpet and balustrade are unchanged. {LOCK} {LIGHT} {FIX}",
"Barely anything to change; mostly a clean-up.",80)

add("DSC05780","Ensuite","full-frame",
f"This photograph shows the ensuite, decluttered and lightly styled {R}. Every bottle, toothbrush, cosmetic, tray and the hand towel are gone from the vanity and the mirror ledge. The vanity holds exactly one matte clay jug and one small stoneware soap bottle. The large mirror reflects this tidy vanity and the shuttered window, correctly reversed. Through the doorway on the right the master bedroom shows a low natural-oak king bed in washed white linen with a muted clay throw, and the timber chests of drawers there are gone. {LOCK} {LIGHT} {FIX}",
"Clears the heavily cluttered vanity and updates the bedroom view through the door.",60)

add("DSC05785","Secondary bedroom","full-frame",
f"This photograph shows a secondary bedroom restyled {R}. The clothes airer, the folded quilt and towel, the drying rack and the existing bed are all gone. The room contains exactly these pieces and nothing more: one queen natural-oak bed with a slatted oak headboard against the back wall to the left of the window, its foot pointing toward the camera; one small rounded oak bedside on each side of the bed, each holding exactly one ceramic lamp; white linen bedding with one sand throw and two white pillows. No rug, bare charcoal carpet. {LOCK} {LIGHT} {FIX}",
"Replaces the bed and clutter with an oak queen, two bedsides and lamps.",60)

add("DSC05790","Second bathroom","full-frame",
f"This photograph shows the second bathroom, decluttered and lightly styled {R}. The hanging brown towel, the bin, the toilet brush and the bottles in the shower and on the vanity are gone. The black towel rail holds exactly two sand linen towels folded over it, and the vanity holds exactly one small stoneware soap bottle and one matte clay vase with a single olive sprig. The large mirror reflects the tidy room, correctly reversed. {LOCK} {LIGHT} {FIX}",
"Declutter, plus two sand towels and two small vanity pieces.",70)

add("DSC05810","Dining and family (wide)","full-frame",
f"This photograph shows the open-plan dining and family room restyled {R}. Everything belonging to the owners is gone: the long timber dining table and black chairs, the sunflowers, the glass breakfast table and grey chairs, the exercise bike, the children's table and play mat, all toys, all framed photographs, and every appliance on the white bench, leaving the glossy white tiles clear. The room contains exactly these pieces and nothing more: in the left foreground, on the same footprint as the original dining table, one large round natural-oak pedestal dining table with exactly six natural-oak chairs with woven paper-cord seats spaced evenly all the way around it and one clay bowl of lemons at its centre; in the far right corner by the kitchen bench, on the footprint of the glass table, one smaller round natural-oak pedestal table with exactly four matching chairs spaced evenly around it; under the far shuttered windows, two natural-oak armchairs with sand cushions angled toward each other beside one small round travertine side table. The two framed photographs become two sun-washed abstracts in sand, clay and sage in thin oak frames, hung level in the same positions. The wall-mounted TV stays, screen side only. The white bench holds exactly one clay jug. {LOCK} {LIGHT} {FIX}",
"The hardest wide shot. Clears a busy family room and stages two round oak tables (dining and breakfast), a reading corner and two artworks. Round tables avoid the end-chair problem.",45)

add("DSC05825","Kitchen (from meals)","full-frame",
f"This photograph shows the kitchen, decluttered and lightly styled {R}. The blue cabinetry, timber cupboards, benchtops, splashback, microwave, fridge and the door are all unchanged. The two bins, the glass table and grey chair in the foreground, the small timber stool, the robot vacuum and its dock, the fridge magnets and papers, the wall clock on the column, the framed photographs, the wall TV on the column and every item on the benches are gone. The bench by the window holds exactly one oak board, one clay jug and one bowl of lemons. In the background living room, the leather sofa and timber coffee tables become a sand linen sofa and a round travertine coffee table, and the baby gate is gone. {LOCK} {LIGHT} {FIX}",
"Kitchen declutter: bins, magnets, foreground table and appliances out, three small Riviera pieces in, and the living room glimpse updated.",50)

add("DSC05830","Meals area","full-frame",
f"This photograph shows the meals area beside the kitchen restyled {R}. The exercise bike, play mat, toys, the glass table and grey chairs, the bin, the framed photographs and every appliance and item on the white bench are gone, leaving the glossy white tiles clear. The room contains exactly these pieces and nothing more: on the footprint of the glass table, one round natural-oak pedestal table with exactly four natural-oak chairs with woven paper-cord seats spaced evenly around it and one clay bowl of lemons at its centre; and under the shuttered window on the left, one natural-oak armchair with a sand cushion beside a small round travertine side table. The two framed photographs become two sun-washed abstracts in sand, clay and sage in thin oak frames, hung level in the same positions. The wall-mounted TV stays, screen side only. The white bench holds exactly one clay jug. {LOCK} {LIGHT} {FIX}",
"Meals area: round oak table with 4 chairs, a reading chair, art swapped. Matches DSC05810.",55)

add("DSC05845","Kitchen peninsula","full-frame",
f"This photograph shows the kitchen peninsula, decluttered and lightly styled {R}. The dish rack, toaster, coffee machine, blender, cups, bottles, cloths and every loose item on the benches and open shelves are gone. The bench holds exactly one oak board leaning against the splashback and one bowl of lemons. In the background the meals area shows a round natural-oak table with four woven paper-cord chairs, the exercise bike and toys are gone, and the framed photographs become sun-washed abstracts in thin oak frames. The dark cabinetry, sink, tapware, dishwasher and timber cupboards are unchanged. {LOCK} {LIGHT} {FIX}",
"Clears the benches and matches the background to the staged meals area.",60)

add("DSC05860","Rumpus (window wall)","full-frame",
f"This photograph shows the upstairs rumpus room facing the shuttered windows, restyled {R}. The leather sofa, soft toys, blanket, the computer desk and monitors, the speakers, the baby gate, the books, the storage tubs and the floor mats are all gone, leaving the charcoal carpet clear. The room contains exactly these pieces and nothing more: in the foreground, on the same footprint as the leather sofa, the back of one deep sand linen slipcovered sofa facing the windows with two muted clay cushions; in front of it a round travertine drum coffee table holding one clay bowl; and a large natural jute rug under both with its edges parallel to the window wall. {LOCK} {LIGHT} {FIX}",
"Clears the rumpus and sets a sand sofa, coffee table and rug facing the view.",55)

add("DSC05865","Rumpus (wide from stairs)","full-frame",
f"This photograph shows the large upstairs rumpus room restyled {R}. Everything belonging to the owners is gone: the toys and toy table in the foreground, the floor mats, the baby gates, the leather sectional, the timber coffee boxes and TV unit, the computer desks, chairs, monitors and printer, the wall-mounted shelving and clutter on the right, the wall clock and every framed photograph, leaving the charcoal carpet clear. The room contains exactly these pieces and nothing more: along the far window wall, on the same footprint as the leather sectional, one large sand linen modular L-shaped sofa with its chaise returning toward the camera; one round travertine drum coffee table in front of it; two natural-oak armchairs with woven cord seats facing the sofa; a large natural jute rug under the seating with edges parallel to the walls; against the left wall, on the footprint of the timber sideboard, one long low natural-oak sideboard holding one slim TV, screen facing the sofa; in the right corner by the windows, on the footprint of the computer desk, one natural-oak writing desk with one oak chair and one ceramic lamp; the timber bookcase on the far left becomes a natural-oak open shelf holding a few neutral books and one clay vase. One sun-washed abstract in sand, clay and sage in a thin oak frame hangs level on the back wall. {LOCK} {LIGHT} {FIX}",
"The biggest job: a fully occupied rumpus becomes a Riviera lounge with an L sofa, coffee table, armchairs, sideboard and TV, a desk corner and a shelf.",40)

add("DSC05880","Rumpus (TV side)","full-frame",
f"This photograph shows the upstairs rumpus room from the TV side, restyled {R}. The leather sectional, the timber coffee boxes, the timber TV cabinet and the drawers on the far left, the soundbar, the soft toys and baskets, the baby gate, the computer desk and monitors, the speakers, the wall clock and every framed photograph are gone, leaving the charcoal carpet clear. The room contains exactly these pieces and nothing more: on the same footprint as the leather sectional, one large sand linen modular L-shaped sofa running along the back wall with its chaise returning toward the camera on the right; one round travertine drum coffee table in front of it; one natural-oak armchair with a woven cord seat; a large natural jute rug under the seating with edges parallel to the walls; on the left, on the footprint of the timber TV cabinet, one long low natural-oak sideboard holding one slim TV, screen facing the sofa; and in the right corner by the windows, one natural-oak writing desk with one oak chair. One sun-washed abstract in sand, clay and sage in a thin oak frame hangs level on the back wall. {LOCK} {LIGHT} {FIX}",
"The same rumpus from another angle; it must match DSC05865 and DSC05885.",45)

add("DSC05885","Rumpus (long view)","full-frame",
f"This photograph shows the long upstairs rumpus room restyled {R}. The leather sectional, the timber coffee boxes, the long timber sideboard in the left foreground, the TV and bracket on the left wall, the toy shelves, toys, floor mats and pink toy car on the right, the baby gate, the computer area, the speakers and every framed photograph are gone, leaving the charcoal carpet clear. The room contains exactly these pieces and nothing more: on the same footprint as the leather sectional, one large sand linen modular L-shaped sofa along the back window wall with its chaise returning toward the camera on the right; one round travertine drum coffee table in front of it; two natural-oak armchairs with woven cord seats facing the sofa; a large natural jute rug under the seating; in the left foreground, on the footprint of the timber sideboard, one long low natural-oak sideboard holding one clay vase with olive branches; and in the right-hand window corner, one natural-oak armchair with a sand cushion beside a small round travertine side table. One sun-washed abstract in sand, clay and sage hangs level on the back wall between the windows. {LOCK} {LIGHT} {FIX}",
"The rumpus long view: L sofa, coffee table, armchairs, sideboard and a reading corner where the toys were.",45)

add("DSC05915","Downstairs hall to rumpus","full-frame",
f"This photograph shows the downstairs hall looking into the rumpus room, restyled {R}. The black baby gate between the columns, the tall timber cabinet on the right edge, the framed photographs, and in the rumpus the leather sectional, timber coffee boxes, soft toys, baskets and computer area are gone. Through the opening the rumpus shows one large sand linen modular L-shaped sofa along the back window wall with a round travertine coffee table, two natural-oak armchairs and a natural jute rug, and a long low natural-oak sideboard where the timber sideboard stood. One sun-washed abstract hangs on the left column wall where the photograph was. {LOCK} {LIGHT} {FIX}",
"Removes the gate and cabinet and matches the rumpus glimpse.",50)

add("DSC05920","Stairs and hall","full-frame",
f"This photograph shows the stairs and hallway, decluttered. Both black baby gates are gone, and the dark framed picture on the far right edge is gone, leaving a clean white wall. The stairs, carpet, handrail, doors and tiles are unchanged. {LOCK} {LIGHT} {FIX}",
"Removes the two baby gates and a frame.",70)

add("DSC05925","Entry into meals","full-frame",
f"This photograph shows the front entry looking into the meals area, restyled {R}. The front door, screen door, sidelight, column and tiles are unchanged. The wall clock on the column, the robot vacuum and its dock, the exercise bike, the children's table and play mat, the toys, the glass table and grey chairs and the sunflowers are gone, leaving the glossy white tiles clear. In the meals area, one round natural-oak pedestal table with four natural-oak chairs with woven paper-cord seats stands on the footprint of the glass table, and one natural-oak armchair with a sand cushion sits under the shuttered window. The timber surface in the right foreground becomes the edge of a natural-oak dining table. The wall TV stays, screen side only. {LOCK} {LIGHT} {FIX}",
"Clears the entry view and matches the staged meals area.",55)

add("DSC05930","Back yard","full-frame",
f"This photograph shows the back lawn, styled {R} with weatherproof pieces only and nothing new built. The lawn, rock retaining wall, shed, pool fence, palms and garden are unchanged. On the flat lawn in the middle ground stand exactly two aged-teak sun loungers with sand weatherproof cushions, side by side and parallel to the rock wall, with one small round stone side table between them. {LOCK} {LIGHT} {FIX}",
"Adds two teak loungers to the lawn. Low value; candidate to skip.",60)

add("DSC05945","Gazebo exterior","masked",
"MASKED (T10): mask the person filming on the gazebo deck plus a 10px margin and their shadow. Fill prompt: the empty dark timber gazebo deck continuing naturally, the cream rendered wall and the screen door behind, soft natural daylight.",
"Removes the person (you, filming) from the gazebo deck. Masked edit, so nothing else changes.",80)

add("DSC05955","Gazebo (to pool)","full-frame",
f"This photograph shows the thatched gazebo, decluttered and styled {R} with weatherproof pieces only and nothing new built. The lawn mower, the glass table, the black crates and storage boxes, and every loose item on the built-in timber benches are gone. The stainless barbecue stays, closed and clean. The room contains exactly these pieces and nothing more: in the centre of the timber deck under the roof apex, one round aged-teak pedestal dining table with exactly six teak chairs with sand rope seats spaced evenly all the way around it, and one clay bowl of lemons at its centre. The built-in benches hold exactly one large clay vessel with olive branches. {LOCK} {LIGHT} {FIX}",
"Clears the gazebo and sets a round teak table with six chairs under the roof.",55)

add("DSC05960","Gazebo (to house)","full-frame",
f"This photograph shows the thatched gazebo looking toward the house, decluttered and styled {R} with weatherproof pieces only and nothing new built. The glass table with the covered barbecue and toolbox, the lawn mower, the hose reel, the crates and every loose item are gone, leaving the timber deck clear. On the deck stands exactly one round aged-teak pedestal dining table with six teak chairs with sand rope seats spaced evenly around it, partly in frame on the right, and one clay bowl of lemons at its centre. {LOCK} {LIGHT} {FIX}",
"Clears the gazebo and matches the teak table from DSC05955.",50)

add("DSC05990","Pool deck","full-frame",
f"This photograph shows the pool deck, styled {R} with weatherproof pieces only and nothing new built. The pool, coping, fences, wall planters, gazebo and safety sign are unchanged. The white bench is gone. On the timber deck along the left of the pool stand exactly two aged-teak sun loungers with sand weatherproof cushions, parallel to the pool edge, with one small round stone side table between them holding one rolled white towel. Inside the gazebo, one round teak table with rope chairs replaces the clutter. {LOCK} {LIGHT} {FIX}",
"Swaps the white bench for two teak loungers and tidies the gazebo glimpse.",55)

add("DSC05995","Pool (from corner)","full-frame",
f"This photograph shows the pool from the deck corner, styled {R} with weatherproof pieces only and nothing new built. The inflatable dolphin, the pool cleaner and hose, the folded umbrella and its base, the hose reel and the white bench are gone, leaving the water and timber deck clear. On the deck along the far wall stand exactly two aged-teak sun loungers with sand weatherproof cushions, parallel to the pool edge, with one small round stone side table between them. {LOCK} {LIGHT} {FIX}",
"Removes the pool toys and cleaner and adds two teak loungers.",55)

add("DSC06010","Rear deck (to house)","full-frame",
f"This photograph shows the rear composite deck and the back of the house, styled {R} with weatherproof pieces only and nothing new built. The children's ride-on car is gone. On the open deck stand exactly these pieces and nothing more: one aged-teak outdoor sofa with sand weatherproof cushions and two muted clay cushions, its back parallel to the right-hand balustrade; two matching teak lounge chairs facing it; one low round stone coffee table between them; and two large matte sand-coloured stoneware planters with olive trees beside the house columns. {LOCK} {LIGHT} {FIX}",
"Adds an outdoor lounge to the empty deck and removes the toy car.",60)

add("DSC06025","Covered deck","full-frame",
f"This photograph shows the covered rear deck, styled {R} with weatherproof pieces only and nothing new built. The children's ride-on car and the pots by the retaining wall are gone. On the deck in the open foreground to the left of the column stands exactly one round aged-teak pedestal dining table with six teak chairs with sand rope seats spaced evenly all the way around it and one clay bowl of lemons at its centre, and one large matte sand-coloured stoneware planter with an olive tree beside the column. {LOCK} {LIGHT} {FIX}",
"Adds a round teak dining setting to the deck and removes the toy car.",60)

add("DSC06050","View","skip",
"SKIP: a view from the deck over the balustrade. There's nothing to furnish; deliver as shot.",
"No staging; use as shot.",100)

import os
os.makedirs('prompts',exist_ok=True)
idx=["# 4 Alex Keith St: staging prompts (ZED Option 04 Riviera, GPT Image 2.5 Sunburst 2k medium, 180cr each)",""]
for k,(room,route,body,summ,sc) in S.items():
    open(f'prompts/{k}.txt','w').write(body+'\n')
    idx+= [f"## {k}: {room}  ·  {route}  ·  pass confidence {sc}%","",f"**What this changes:** {summ}","",body,""]
open('prompts/INDEX.md','w').write('\n'.join(idx))
full=[k for k,v in S.items() if v[1]=='full-frame']
print(len(S), 'full-frame', len(full), 'masked', sum(v[1]=='masked' for v in S.values()), 'skip', sum(v[1]=='skip' for v in S.values()))
