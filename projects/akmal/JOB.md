---
client: akmal
address: 1007/180 Marine Parade
opened: 2026-07-14
status: intake        # intake → generating → review → delivered
cost: { credits: 14, aud: 0.56 }   # ~7cr wasted: dining prompt run on -3 (bedroom) by filename error

# TRUE FILE MAPPING (locked 2026-07-14 after mislabel)
# -2  open-plan living/dining/kitchen wide (hinterland)
# -3  MASTER BEDROOM hero (water/Broadwater view)  <-- NOT dining
# -6  master ensuite/robe angle (city)
# -7  DINING + kitchen, cleanest anchor (hinterland)
# -8  feature wall: desk nook + TV
# -9  living + dining + island (hinterland)  [NBP keeper generated]
# -11 dining + island + living (hinterland)
source: /Users/10xhunter/Desktop/untitled folder 6/
---

# Job — 1007/180 Marine Parade (AKMAL)

Virtual staging, **full ZED restyle** (white/cream modern luxury, no black, no timber furniture). Open-plan living+dining+kitchen shot from 4 angles + master bedroom (main + optional 2nd). Existing dark furniture (black leather living set, black round dining set) to be **replaced**, not filled into an empty room. Consistency held via **anchor-frame transfer**.

## ZED piece-list (LOCKED — every frame must match)

**Dining**
- Round white Carrara-marble table, sculptural white marble pedestal base (table is already round → no end-chair risk)
- 4 cream velvet chairs on slim brushed-gold legs, evenly spaced
- Centrepiece: one low matte-cream ceramic bowl

**Living**
- Cream bouclé L-sectional sofa
- White marble + brushed-gold rectangular coffee table
- Cream shag rug (wider than sofa front legs)
- One ivory/cream accent chair (replaces black recliner)
- Gold-stem floor lamp
- Fiddle-leaf fig in white ceramic pot

**Master bedroom**
- White-gloss bed, cream bouclé headboard, layered white + cream linen, ≤3 accent cushions, folded cream throw
- White-gloss bedsides (vary L vs R styling), gold-stem lamps
- Kentia palm in white ceramic (plant rotated vs living's fiddle-leaf)
- Cream shag rug, not blocking window/door

**Fixtures preserved everywhere:** light oak floors, black-framed floor-to-ceiling windows + view, light timber kitchen cabinetry, stone waterfall island + vertical timber slat end, stainless appliances, curtains, downlights, built-in desk/shelving, ensuite tapware/basins/bath/tiles.

## Shots

| # | Shot | File | Pipeline | Status | Notes |
|---|------|------|----------|--------|-------|
| 1 | Dining anchor | -3 | full-frame NBP 2k | prompt ready | establishes ZED dining pieces |
| 2 | Living anchor | -9 | full-frame NBP 2k | pending | establishes ZED living pieces |
| 3 | Open plan wide | -2 | transfer | pending | both zones; match anchors |
| 4 | Dining + island + living | -11 | transfer | pending | both zones |
| 5 | Master main | -6 | full-frame NBP 2k | pending | own anchor |
| 6 | Master 2nd (optional) | -7 | full-frame / decide | pending | mostly ensuite + foot of bed — low staging value, evaluate |
| 7 | Feature wall (desk/TV) | -8 | — | out? | detail wall, not a room; décor only if briefed |

Tokens (both masters): **@original** = RAW original of the angle (never a prior AI output — restyling a gen compounds its distortion) · **@reference** = the approved hero frame for that room (compact-L living hero / hero bedroom). Run on Seedream. Gens chase the light EFFECT; colour graded uniformly in post.

## LOCKED living master (ZED open-plan) — same block for -2 / -7 / -9 / -11
FIXED LAYOUT = absolute (wall-relative, not camera-relative) so every angle resolves to the same arrangement → couch can't jump walls between shots.

```
Restyle @original to match the furniture, palette, lighting and room setup in @reference, keeping the exact camera angle and room size of @original.
FIXED LAYOUT (identical in every angle): a compact cream bouclé L-shaped sectional sofa with two short equal ends faces the mounted TV and white media console on the feature wall, with the floor-to-ceiling windows to its side; a white-marble and brushed-gold oval coffee table on a large cream shag rug in front of the sofa; a round white Carrara-marble pedestal dining table for four with cream velvet shell-back chairs on brushed-gold legs (four only) in front of the windows between the sofa and the kitchen; the kitchen with its curved timber-slat island along the far wall; a fiddle-leaf fig in a white ceramic pot and a slim brushed-gold floor lamp by the windows.
Replace each existing dark piece with its ZED equivalent from @reference in that layout (black leather sofa/recliner → the compact cream bouclé L-sectional; black dining set → white marble table + four cream velvet chairs; dark gloss media console → low white-gloss console + one neutral cream décor piece; dark/personal wall art → one neutral cream-and-taupe abstract).
Furnish generously so the room feels full and balanced — no large empty floor.
Keep every wall, the mounted TV and media console straight, square and true to @original — no bowing, warping or curving.
Preserve the exact room size, proportions and floor area of @original — do not widen, enlarge or stretch the space.
Bright, airy, well-exposed real-estate photography; warm sunlight streams through the windows casting soft light rays and gentle shadows, the room luminous and evenly bright with open, lifted shadows — sunny and fresh, never dark.
Same focal length and camera position as @original, straight vertical lines, natural perspective without wide-angle distortion.
Keep all existing windows, doors, curtains, kitchen cabinetry, the curved timber-slat island, stone benchtop, sink, tapware, stainless appliances, built-in shelving, mounted TV, flooring and tiles in @original unchanged.
```
Desk/MacBook: leave built-in desk empty in wide frames; add "at the built-in desk, a cream designer chair with an open silver MacBook" ONLY in an angle where the desk has its own clear space (never tucked past the couch).

## LOCKED bedroom master — same block for -3 hero + -6 ensuite angle
FIXED BED = identical spec both angles so the room reads the same. Beds always crisp/wrinkle-free.

```
Restyle @original to match the bed, styling, palette and lighting in @reference so every bedroom angle reads as the same room.
FIXED BED (identical in every angle): a low white-gloss platform bed, dressed in crisp, smoothly made hotel-style linen — taut, freshly pressed and completely wrinkle-free — with plump white euro cushions, cream and oat accent cushions, and a neatly folded cream throw laid straight across the foot; a soft cream rug on the carpet at the foot of the bed.
Where visible in @original: white-gloss bedside tables either side styled differently (a slim brushed-gold stem lamp one side; a low vase and small stack of books the other), and a tall kentia palm in a white ceramic pot in the corner by the window.
Bright, airy, well-exposed real-estate photography; warm sunlight and soft light rays, the room luminous and evenly bright with open, lifted shadows — sunny and fresh, never dark.
Preserve the exact room size, proportions and floor area of @original.
Same focal length and camera position as @original, straight vertical lines, natural perspective without wide-angle distortion.
Keep all existing windows, water view, sliding door, glass ensuite, bath, vanity, walk-in robe, curtains, carpet, walls and fixtures in @original unchanged.
```

## Log

- 2026-07-14 intake: 7 frames triaged; all interior → full-frame, Nano Banana Pro 2k. Scope = full ZED restyle. Consistency = anchor-frame transfer. Anchors: dining -3, living -9, master -6.
- 2026-07-14 gen pass 1 (NBP 2k, 8cr): dining prompt MISTAKENLY run on -3 (bedroom) x2 + living -9 + "master" on -6 (ensuite). Living -9 = KEEPER ✓.
- 2026-07-14 gen pass 2 (Seedream 5.0 Pro 2k, 6cr): dining on -3 (still bedroom, wrong) + master on -6 (ensuite) = ensuite-master usable ✓.
- 2026-07-14 CORRECTION: filename scramble found. -3 = bedroom not dining. 3 dining attempts wasted (~7cr). Seedream composition-lock VERIFIED trustworthy (it faithfully kept the bedroom shell I wrongly fed it). Real dining anchor = -7 (not yet generated). Hero bedroom = -3 (Hunter running on Freepik in tandem).
- KEEPERS so far: living -9 (NBP), ensuite-master -6 (SD5). TODO: dining -7 on Seedream, hero bed -3 (Hunter/Freepik).
- 2026-07-14 KEEPER: master hero -3 done by Hunter on Seedream (Higgsfield) — faithful, on-brief, listing-ready.
- 2026-07-14 workflow decision: Hunter runs all remaining gens himself on Seedream; Claude supplies prompts + does Magnific upscale finish on keepers.
- 2026-07-14 ANCHOR: open-plan anchor = -2 (widest: living+dining+kitchen+TV wall). Approve first, then transfer into -7/-9/-11 to hold the set. Six-frame ZED prompt set written (-7 dining, -2 anchor, -9 living, -11 dining+island, -8 study nook +iMac, -6 ensuite). Swaps: black leather→cream bouclé, black-gloss console→white-gloss, flowers→neutral; boat photos + built-in shelf kept.
