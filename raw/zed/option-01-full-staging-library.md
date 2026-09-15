# Option 01 — Full AI Staging Library

> **Client option:** Option 01  
> **Style:** Warm organic contemporary with restrained Australian coastal and Mediterranean-resort influences.  
> **Use:** This file is Claude's persistent reference guide for this client option. When the user says `Option 01 + [room type]`, Claude must read the corresponding room kit below, retrieve the named image files from `02_FURNITURE_REFERENCES/option-01/`, and use those images as visual references.

---

## Folder location

```text
AI_STAGING/
└── [CLIENT NAME]/
    ├── [CLIENT NAME]_OPTION_01_FULL_STAGING_LIBRARY.md
    ├── 00_CLIENT_MOCKUPS/
    │   └── option-01-client-board.jpg
    ├── 01_STYLE_REFERENCES/
    │   └── option-01-style-overview.jpg
    ├── 02_FURNITURE_REFERENCES/
    │   └── option-01/
    │       ├── option-01-living-sofa-oat-boucle.jpg
    │       ├── option-01-living-sofa-curved-modular.jpg
    │       ├── option-01-living-occasional-chair-chalk-boucle.jpg
    │       ├── option-01-living-occasional-chair-cream-boucle.jpg
    │       ├── option-01-living-occasional-chair-boucle-timber.jpg
    │       ├── option-01-living-coffee-table-dark-walnut.jpg
    │       ├── option-01-living-coffee-table-organic-walnut.jpg
    │       ├── option-01-living-media-console-walnut.jpg
    │       ├── option-01-aged-brass-dome-lamp.jpg
    │       ├── option-01-dining-table-dark-oak.jpg
    │       ├── option-01-dining-table-dark-oak-pedestal.jpg
    │       ├── option-01-dining-chair-cloud-boucle.jpg
    │       ├── option-01-kitchen-counter-stool-chai-boucle.jpg
    │       ├── option-01-kitchen-counter-stool-timber-oatmeal.jpg
    │       ├── option-01-bedroom-bed-oatmeal-upholstered.jpg
    │       ├── option-01-bedroom-bench-walnut-oatmeal.jpg
    │       ├── option-01-bedroom-bedside-dark-walnut.jpg
    │       ├── option-01-office-desk-walnut.jpg
    │       ├── option-01-office-desk-oval-timber.jpg
    │       ├── option-01-entry-console-walnut.jpg
    │       ├── option-01-entry-console-styling.jpg
    │       ├── option-01-outdoor-sofa-aged-teak-sesame.jpg
    │       ├── option-01-outdoor-lounge-aged-teak-sesame.jpg
    │       ├── option-01-outdoor-lounge-woven-teak.jpg
    │       ├── option-01-outdoor-dining-table-aged-teak.jpg
    │       ├── option-01-outdoor-dining-table-teak-rectangular.jpg
    │       ├── option-01-outdoor-dining-chair-teak-rope.jpg
    │       └── option-01-outdoor-dining-chair-rope-back.jpg
    ├── 03_MATERIAL_REFERENCES/
    ├── 04_LAYOUT_SKETCHES/
    └── 05_GENERATED_OUTPUTS/
```

---

# Claude operating instructions

When a user says:

```text
[CLIENT NAME] — Option 01 — [ROOM] — [MODE]
```

Claude must:

1. Read this file first.
2. Read the room kit matching `[ROOM]`.
3. Retrieve the client Option 01 style board.
4. Retrieve only the listed furniture references for that room.
5. Analyse the new source property photograph before creating a prompt.
6. Choose the correct mode.
7. Write the generation prompt using the room recipe, colour hierarchy and exclusions.
8. Explain exactly which references it selected.
9. Create a QA checklist for the output.
10. Do not mix Option 01 furniture with a different client option.

## Project modes

| Mode | Use when | Rule |
|---|---|---|
| `STRICT_VIRTUAL_STAGING` | A listing image must remain truthful | Preserve walls, openings, fixed joinery, flooring, ceiling, exterior view and camera angle. Add loose furniture and styling only. |
| `RENOVATION_VISUALISATION` | Walls, openings, finishes or joinery can change | Keep the home recognisable and label it conceptual. |
| `ARCHITECTURAL_RERENDER` | The user wants a new camera angle, changed wall layout or idealised room | Generate a new scene informed by the original property. Do not present as literal listing photography. |

## Hard rule

Never write a prompt that says both:

```text
Preserve the exact original camera angle and architecture.
```

and:

```text
Change the walls, windows, openings or camera angle.
```

If structure or viewpoint must change, use `RENOVATION_VISUALISATION` or `ARCHITECTURAL_RERENDER`.

---

# Option 01 style identity

## Design direction

- Warm organic contemporary
- Restrained Australian coastal
- Mediterranean-resort material warmth
- Quiet, premium, architectural rather than flashy
- Low-profile sculptural furniture
- Matte / honed materials
- Sparse, deliberate styling
- Soft natural daylight

## Palette

| Use | Direction | Hex guide |
|---|---|---|
| Main walls and upholstery | Warm ivory | `#E9E2D6` |
| Secondary linen and curtains | Oatmeal | `#D8D0C2` |
| Timber | Dark smoked walnut | `#4A3326` |
| Stone | Honed travertine / warm limestone | `#C9B79B` |
| Accent | Muted eucalyptus olive | `#6B7257` |
| Metal | Subdued aged brass | `#9A7445` |
| Dark detail | Soft charcoal | `#4D4A43` |

## Colour hierarchy

- 70% warm ivory, oatmeal and stone
- 20% dark walnut / natural timber
- 7% muted olive / eucalyptus
- 3% aged brass / soft charcoal

## Required materials

- Warm ivory linen
- Oatmeal bouclé
- Dark smoked walnut
- Matt dark oak
- Honed travertine or limestone
- Muted eucalyptus olive
- Aged brass
- Ivory woven wool
- Textured ceramic stoneware

## Exclusions

Never introduce:

- Hamptons styling
- Blue-and-white coastal styling
- Farmhouse furniture
- Whitewashed timber
- Generic beige-on-beige with no timber contrast
- Excess indoor rattan or cane
- High-gloss gold or chrome
- Black marble
- Orange timber
- Bright green cushions or plants
- Heavy decorative clutter
- Artificial orange golden-hour light
- Distorted furniture, floating objects or incorrect shadows

---

# Global styling kit

These elements are prompt-controlled and should be used **after** the main furniture is correct:

- One oversized tonal abstract artwork in thin oak frame
- Palette for artwork: taupe, putty, warm grey, limestone, muted olive and charcoal
- One textured stoneware vessel with olive branches
- Two neutral hardcover books maximum
- One small honed-stone bowl
- Full-height warm-white linen sheers where physically possible
- Ivory wool or woven rugs with minimal visible pattern
- Two to four muted-olive cushions maximum
- One oatmeal throw maximum
- One aged-brass dome lamp as an accent, not in every room
- Matte ceramic bedside lamps
- Large outdoor stoneware planters with olive trees or mature subtropical greenery

## Lighting direction

- Follow the real window / door / opening direction in the source property photo.
- Use soft natural daylight with controlled highlights and open shadows.
- White walls and ivory furniture should feel warm-neutral, not yellow.
- Walnut should be deep brown, not orange.
- Greenery should be desaturated olive/eucalyptus, not bright green.
- Final campaign grade happens in Lightroom / ACR, not through heavy AI relighting.

---

# Living room kit

## Retrieve these images

```text
option-01-living-sofa-oat-boucle.jpg
option-01-living-occasional-chair-chalk-boucle.jpg
option-01-living-coffee-table-dark-walnut.jpg
```

## Optional images

```text
option-01-living-sofa-curved-modular.jpg
option-01-living-occasional-chair-cream-boucle.jpg
option-01-living-occasional-chair-boucle-timber.jpg
option-01-living-coffee-table-organic-walnut.jpg
option-01-living-media-console-walnut.jpg
option-01-aged-brass-dome-lamp.jpg
```

## Furniture recipe

- Low warm-ivory / oatmeal modular sofa
- Soft rounded arms and deep but tailored cushions
- One or two compact sculptural ivory-bouclé chairs
- Oversized low dark-smoked-walnut coffee table
- Large ivory woven-wool rug
- Low walnut media console only if appropriate
- Two to four muted-olive cushions
- One aged-brass side lamp or side table maximum
- One large tonal artwork
- One ceramic vessel with olive branches

## Placement rules

- Leave a clear circulation path around the seating zone.
- Coffee table should sit approximately 35–45 cm from sofa seating.
- Do not block doors, windows, fireplaces or views.
- Chairs must sit naturally on the rug/floor with correct contact shadows.

## Prompt block

```text
Furnish with a low warm-ivory linen modular sofa with softly rounded arms, one or two compact sculptural ivory-boucle occasional chairs, an oversized low dark-smoked-walnut coffee table, a large ivory woven-wool rug, muted eucalyptus-olive cushions, one restrained aged-brass accent and tonal abstract art. Keep the scene calm, low-profile, architectural and minimally styled.
```

---

# Dining room kit

## Retrieve these images

```text
option-01-dining-table-dark-oak.jpg
option-01-dining-chair-cloud-boucle.jpg
```

## Optional images

```text
option-01-dining-table-dark-oak-pedestal.jpg
```

## Furniture recipe

- Long oval dark-walnut / matt-dark-oak pedestal table
- Six compact oatmeal-bouclé dining armchairs
- Large sculptural linen / paper pendant centred above table
- Oversized ivory rug only where room scale supports it
- Ceramic vessel with olive branches
- One large warm-neutral artwork

## Placement rules

- Default to six chairs unless the source room demands four or eight.
- Maintain believable chair clearance from walls.
- Keep chair legs aligned on floor/rug perspective.
- Ensure pendant is centred over the table, not necessarily centred in the entire room.

## Prompt block

```text
Use a substantial dark-smoked-walnut oval pedestal dining table with six compact oatmeal-boucle dining armchairs, a sculptural linen pendant centred above the table and minimal ceramic styling with olive branches. Maintain realistic chair spacing, clear circulation, realistic floor contact and restrained warm-neutral styling.
```

---

# Kitchen kit

## Retrieve these images

```text
option-01-kitchen-counter-stool-chai-boucle.jpg
```

## Optional images

```text
option-01-kitchen-counter-stool-timber-oatmeal.jpg
```

## Furniture recipe

- Two or three counter-height stools, based on true island size
- Dark-walnut frame
- Oatmeal textured / bouclé upholstered seat and curved back
- Restrained aged-brass foot rail
- One ceramic vessel with olive branches
- One small stone bowl
- One timber board

## Strict staging rule

Do not alter fixed kitchen cabinetry, benchtops, splashback, appliances, tapware, window frames or floor in `STRICT_VIRTUAL_STAGING` mode.

## Prompt block

```text
Add only two or three counter-height stools with dark-walnut frames, curved oatmeal textured upholstery and subtle aged-brass foot rails. Add minimal styling: one ceramic vessel with olive branches, one small stone bowl and one timber board. Preserve all fixed cabinetry, benchtops, appliances, windows, lighting direction and camera geometry unless the job is a renovation visualisation.
```

---

# Bedroom kit

## Retrieve these images

```text
option-01-bedroom-bed-oatmeal-upholstered.jpg
option-01-bedroom-bench-walnut-oatmeal.jpg
option-01-bedroom-bedside-dark-walnut.jpg
```

## Furniture recipe

- Low upholstered king bed in warm oatmeal / ivory linen
- Wide straight or gently softened two-panel headboard
- Crisp layered off-white bedding
- Two muted-olive lumbar cushions
- One oatmeal textured throw
- Two compact dark-walnut bedside tables
- Two matte ceramic lamps
- Large ivory wool rug beneath bed
- Slim walnut bench at foot of bed only when circulation permits
- One oversized warm-neutral abstract artwork

## Placement rules

- Bed must remain at believable scale for room width.
- Bench must not block door swings or walking routes.
- Rug should extend at least beyond both sides of the bed and partially at foot where possible.
- Artwork should be correctly centred over headboard and aligned with room perspective.

## Prompt block

```text
Create a refined bedroom with a low upholstered king bed in warm oatmeal linen, a wide straight two-panel headboard, crisp layered ivory bedding, two muted eucalyptus-olive lumbar cushions, dark-smoked-walnut bedside tables, simple ceramic lamps, a large ivory wool rug and one oversized warm-neutral abstract artwork. Add a slim walnut bench at the foot only if there is clear circulation around it.
```

---

# Office / study kit

## Retrieve these images

```text
option-01-office-desk-walnut.jpg
```

## Optional images

```text
option-01-office-desk-oval-timber.jpg
option-01-living-media-console-walnut.jpg
option-01-aged-brass-dome-lamp.jpg
```

## Furniture recipe

- Sculptural deep-walnut desk with oval / bullnose top and substantial rounded legs
- One compact oatmeal upholstered desk chair
- Low walnut credenza or full-height shelving only where room supports it
- Aged-brass dome lamp
- Ivory textured rug
- One tonal artwork
- Olive branches and minimal books

## Prompt block

```text
Create a calm executive study using a sculptural deep-walnut desk with a rounded or oval top and substantial legs, one compact oatmeal-upholstered desk chair, a low walnut credenza, an aged-brass dome lamp, a warm-neutral abstract artwork and minimal olive-branch styling. Keep work surfaces mostly clear and retain realistic circulation around the desk.
```

---

# Entry / hallway kit

## Retrieve these images

```text
option-01-entry-console-walnut.jpg
option-01-aged-brass-dome-lamp.jpg
```

## Optional images

```text
option-01-entry-console-styling.jpg
option-01-living-occasional-chair-chalk-boucle.jpg
```

## Furniture recipe

- Narrow dark-walnut console with oval/bullnose top and rounded legs
- One aged-brass dome lamp
- Large tonal artwork or mirror only where wall permits
- Long ivory runner
- Compact ivory-bouclé bench only if width permits
- Stoneware vessel with olive branches

## Prompt block

```text
Style the entry with a narrow dark-walnut console with softly rounded pedestal legs, one subdued aged-brass dome lamp, a textured stoneware vessel with olive branches, one large tonal artwork and an ivory woven runner. Add a compact ivory-boucle bench only where it does not restrict hallway clearance.
```

---

# Outdoor lounge kit

## Retrieve these images

```text
option-01-outdoor-sofa-aged-teak-sesame.jpg
option-01-outdoor-lounge-aged-teak-sesame.jpg
```

## Optional images

```text
option-01-outdoor-lounge-woven-teak.jpg
```

## Furniture recipe

- Aged-teak outdoor sofa
- Two matching teak lounge chairs
- Thick warm-ivory outdoor cushions
- Natural rope / woven side details
- Maximum two muted olive cushions
- Low teak or limestone coffee table
- Natural outdoor woven rug where suitable
- Large matte stoneware planters with olives or mature subtropical planting

## Prompt block

```text
Create a premium outdoor lounge with an aged-teak sofa, two matching teak-and-woven lounge chairs, thick warm-ivory weatherproof cushions, a low teak or limestone coffee table, maximum two muted eucalyptus-olive cushions and large matte stoneware planters. Use natural outdoor shadows and weather-appropriate matte materials.
```

---

# Outdoor dining kit

## Retrieve these images

```text
option-01-outdoor-dining-table-aged-teak.jpg
option-01-outdoor-dining-chair-teak-rope.jpg
```

## Optional images

```text
option-01-outdoor-dining-table-teak-rectangular.jpg
option-01-outdoor-dining-chair-rope-back.jpg
```

## Furniture recipe

- Long aged-teak dining table with rounded rectangle top and thick cylindrical legs
- Alternative: classic straight rectangular teak table with four legs
- Six or eight teak-and-rope dining chairs, based on actual space
- Sand / warm-ivory outdoor cushions
- One ceramic vessel with olive branches
- Very restrained outdoor table styling

## Strict staging rule

Never add a pool, outdoor kitchen, pergola, deck, view, landscaped garden or structural outdoor feature that does not exist unless the output is clearly an `ARCHITECTURAL_RERENDER` / conceptual visualisation.

## Prompt block

```text
Create an alfresco dining setting with a long aged-teak table with a broad rounded-rectangle top and substantial cylindrical legs, paired with six or eight matching natural-teak dining chairs with sand-coloured rope weave and warm-ivory cushions. Use restrained ceramic styling with olive branches, physically believable outdoor shadows and matte weather-resistant materials.
```

---

# Universal generation prompt

Use this as the base prompt after Claude reads the relevant room kit:

```text
Use the uploaded source property image as the structural reference. Use the uploaded Option 01 client board as the approved style reference. Use the uploaded product images only for individual furniture silhouettes, construction and materials.

Style: warm organic contemporary with restrained Australian coastal and Mediterranean-resort influences. Warm ivory linen, oatmeal bouclé, dark smoked walnut, honed travertine, warm limestone, muted eucalyptus olive and subtle aged brass. Low-profile sculptural furniture, minimal styling, soft natural daylight, open shadows, controlled highlights, low saturation and premium Australian architectural photography.

Do not use Hamptons, blue coastal, whitewashed timber, farmhouse details, black marble, glossy gold, bright green, orange timber, decorative clutter or artificial golden-hour light.

Prioritise physically plausible furniture scale, clear circulation, correct verticals, real floor contact shadows and one consistent natural window-light direction. Final campaign colour will be completed in Lightroom.
```

---

# Property job template

Copy this to create a new property job note:

```markdown
# [PROPERTY ADDRESS] — Option 01 AI Staging

- Client: [CLIENT NAME]
- Selected option: Option 01
- Room: [living / dining / kitchen / bedroom / office / entry / outdoor lounge / outdoor dining]
- Mode: [STRICT_VIRTUAL_STAGING / RENOVATION_VISUALISATION / ARCHITECTURAL_RERENDER]
- Source property image: [[file-name.jpg]]
- Client style board: [[option-01-client-board.jpg]]
- New camera angle required: [yes/no]
- Wall/opening changes required: [yes/no]
- Fixed features that must remain: [list]
- Client notes: [text]

## References Claude must retrieve

- Primary furniture: [[file-name.jpg]]
- Secondary furniture: [[file-name.jpg]]
- Optional layout sketch: [[file-name.jpg]]

## Claude output required

1. Mode classification
2. Selected-reference list
3. Furniture and layout plan
4. Main generation prompt
5. Architecture correction prompt
6. Furniture correction prompt
7. Lighting/colour preview prompt
8. Lightroom finish notes
9. QA checklist

## Generation log

- Generator:
- Prompt version:
- Image version selected:
- What worked:
- What failed:
- Photoshop corrections:
- Final output:
```

---

# Quick command examples

```text
[CLIENT NAME] — Option 01 — Bedroom — STRICT_VIRTUAL_STAGING.
Use the Option 01 bedroom kit and preserve the existing bed position, window frames, carpet, ceiling and camera angle.
```

```text
[CLIENT NAME] — Option 01 — Outdoor dining — ARCHITECTURAL_RERENDER.
Use the Option 01 outdoor dining kit. Create a new angle from the pool-side corner toward the alfresco zone. Retain recognisable property materials but design the new scene as a client concept visualisation.
```

```text
[CLIENT NAME] — Option 01 — Living room — RENOVATION_VISUALISATION.
Use the living kit. Remove the nominated internal wall, create a larger opening to the dining room, maintain a believable structure, and use the sofa/chair/coffee-table references from this library.
```

---

# Final QA checklist

Before delivery, Claude must check:

- [ ] Correct client and correct option selected
- [ ] Correct room kit and only relevant reference images selected
- [ ] Project mode is correctly classified
- [ ] No contradiction between preserve/change instructions
- [ ] Room scale and camera viewpoint are physically plausible
- [ ] Verticals are straight
- [ ] Windows, doors, floors and ceilings are correct for the selected mode
- [ ] Furniture does not block access or circulation
- [ ] Furniture legs and rugs contact the floor correctly
- [ ] Shadows follow a single believable light direction
- [ ] Timber is deep neutral brown, not orange
- [ ] Whites are warm-neutral, not yellow
- [ ] Greenery is muted olive, not neon green
- [ ] Styling is minimal and consistent with Option 01
- [ ] No duplicated furniture, broken geometry, warped chair legs or melted objects
- [ ] Architecture changes are labelled conceptual when required
- [ ] Final image receives Lightroom/Photoshop finishing before campaign delivery
