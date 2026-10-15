---
type: concept
tags: [virtual-staging, style, zed]
updated: 2026-10-12
---

# ZED Style — "Option 01" (canonical staging library)

**This is now the canonical, locked spec.** Zed ran a formal research/asset pass (Perplexity deep research → `raw/zed/option-01-full-staging-library.md` + `raw/zed/option-01-full-staging-asset-library.html`) and named it **Option 01**. It supersedes both prior eras below. Unlike the two earlier changes, this one isn't a fresh vibe swap — it's largely a formalisation of the "sand & walnut" boards from 2026-09-15 (same ivory/oatmeal/walnut/olive/brass direction), now with hex codes, per-room reference images, exclusions and a colour-hierarchy ratio. Read the raw file for the full per-room prompt blocks and reference-image filenames before writing a ZED prompt.

## Identity
Warm organic contemporary, with restrained Australian coastal and Mediterranean-resort influences. Quiet, premium, architectural — not flashy. Low-profile sculptural furniture, matte/honed materials, sparse deliberate styling, soft natural daylight.

## Palette (colour hierarchy: 70% / 20% / 7% / 3%)
| Use | Direction | Hex |
|---|---|---|
| Main walls/upholstery (70% incl. stone) | Warm ivory | `#E9E2D6` |
| Secondary linen/curtains | Oatmeal | `#D8D0C2` |
| Timber (20%) | Dark smoked walnut | `#4A3326` |
| Stone | Honed travertine / warm limestone | `#C9B79B` |
| Accent (7%) | Muted eucalyptus olive | `#6B7257` |
| Metal (3%) | Subdued aged brass | `#9A7445` |
| Dark detail | Soft charcoal | `#4D4A43` |

## Exclusions — never introduce
Hamptons styling, blue-and-white coastal, farmhouse furniture, whitewashed timber, generic beige-on-beige with no timber contrast, excess indoor rattan/cane, high-gloss gold or chrome, black marble, orange timber, bright green cushions/plants, heavy decorative clutter, artificial orange golden-hour light, distorted furniture/floating objects/incorrect shadows.

## Resolved contradictions (previously flagged, now settled by the Option 01 library)
- **Dining tables ARE timber** — dark-oak/walnut oval pedestal table, default six oatmeal bouclé armchairs. This resolves the 2026-09-11 "stone only, never timber" rule in favour of timber; that rule is now marked superseded in auto-memory (`feedback-zed-no-timber-dining-table`), not deleted.
- **Bedroom DOES get large wall art** — one oversized tonal abstract (taupe/putty/warm grey/limestone/olive/charcoal) in a thin oak frame, centred over the headboard, aligned to room perspective. This is a ZED-specific override of the general no-wall-art-default rule in [[staging-rules]] — the general rule still applies to other clients.

## Room-by-room piece-list (see the raw library for exact prompt-block wording and reference filenames)
- **Living** — low warm-ivory/oatmeal modular sofa, rounded arms, tailored deep seats; 1–2 compact ivory-bouclé occasional chairs; oversized low dark-smoked-walnut coffee table; large ivory woven-wool rug; walnut media console only if appropriate; 2–4 muted-olive cushions; one aged-brass lamp accent max; one large tonal artwork; one ceramic vessel with olive branches.
- **Dining** — long oval dark-walnut/matt-dark-oak pedestal table; six compact oatmeal-bouclé dining armchairs (default; 4 or 8 only if room size demands); large sculptural linen/paper pendant centred over the table; ceramic vessel with olive branches; one large warm-neutral artwork.
- **Kitchen** — 2–3 counter stools sized to the actual island (dark-walnut frame, oatmeal bouclé curved back, restrained aged-brass foot rail); one ceramic vessel with olive branches, one small stone bowl, one timber board. Fixed cabinetry/benchtop/splashback/appliances/tapware/windows/floor stay untouched in strict staging.
- **Bedroom** — low upholstered king bed, warm oatmeal/ivory linen, wide straight or gently softened two-panel headboard; crisp layered off-white bedding; 2 muted-olive lumbar cushions; one oatmeal throw; 2 compact dark-walnut bedsides with matte ceramic lamps; large ivory wool rug beneath the bed; slim walnut bench at the foot only if circulation permits; one oversized warm-neutral abstract centred over the headboard.
- **Office/study** — sculptural deep-walnut desk, oval/bullnose top, substantial rounded legs; one compact oatmeal-upholstered desk chair; low walnut credenza or shelving only if room supports it; aged-brass dome lamp; ivory textured rug; one tonal artwork; olive branches + minimal books.
- **Entry/hallway** — narrow dark-walnut console, oval/bullnose top, rounded legs; one aged-brass dome lamp; large tonal artwork or mirror where wall permits; long ivory runner; compact ivory-bouclé bench only if width permits; stoneware vessel with olive branches.
- **Outdoor lounge** — aged-teak sofa; two matching teak lounge chairs; thick warm-ivory cushions; natural rope/woven side details; max 2 muted-olive cushions; low teak or limestone coffee table; natural outdoor woven rug where suitable; large matte stoneware planters with olive trees/subtropical greenery.
- **Outdoor dining** — long aged-teak table (rounded-rectangle top, thick cylindrical legs, or classic straight rectangular alternative); 6–8 teak-and-rope dining chairs per actual space; sand/warm-ivory cushions; one ceramic vessel with olive branches; very restrained table styling. **Never invent a pool, outdoor kitchen, pergola, deck, view or landscaped garden that doesn't exist** unless the job is explicitly an architectural-rerender/concept visualisation.

## Global styling kit (apply after the main furniture is right)
One oversized tonal abstract in a thin oak frame (taupe/putty/warm grey/limestone/olive/charcoal palette) · one textured stoneware vessel with olive branches · max 2 neutral hardcover books · one small honed-stone bowl · full-height warm-white linen sheers where physically possible · ivory wool/woven rugs, minimal visible pattern · 2–4 muted-olive cushions max · one oatmeal throw max · one aged-brass dome lamp as an accent, not in every room · matte ceramic bedside lamps · large outdoor stoneware planters with olive trees/mature subtropical greenery.

## Lighting direction
Follow the real window/door/opening direction in the source photo. Soft natural daylight, controlled highlights, open shadows. Whites/ivory should read warm-neutral, not yellow. Walnut deep brown, not orange. Greenery desaturated olive/eucalyptus, not bright green. Final grade happens in Lightroom/ACR, not heavy AI relighting — consistent with `feedback-staging-brightness-default`.

## Project modes (new concept from this library — not used before on ZED jobs)
- **STRICT_VIRTUAL_STAGING** — preserve walls, openings, fixed joinery, flooring, ceiling, exterior view and camera angle; add loose furniture/styling only. This is the mode every ZED job has run in so far.
- **RENOVATION_VISUALISATION** — walls/openings/finishes/joinery can change; must stay recognisable and be labelled conceptual.
- **ARCHITECTURAL_RERENDER** — new camera angle, changed wall layout or idealised room; generate a new scene informed by the original, never presented as literal listing photography.
Never combine "preserve the exact camera angle and architecture" with "change the walls/windows/openings/camera angle" in one prompt — pick the mode that matches what's actually being asked.

## Rules that still ride with it
- Plants rotate between rooms — olive branches/trees are the house greenery; vary vessel and scale rather than species.
- Secondary bedrooms styled a tier below the primary (still applies within Option 01).
- Fixtures preserved everywhere in STRICT_VIRTUAL_STAGING mode: floors, windows and the view, cabinetry, stone, appliances, curtains, tapware, built-ins.
- Placement locks (footprint + axis vs a named fixed feature + direction cue) apply to every hero piece — see [[staging-rules]].
- Round dining table fallback for end-chair risk is superseded for ZED specifically — Option 01's oval pedestal table is itself end-chair-proof (rounded ends, no flat end to seat someone at); the general round-table fallback still applies to other clients.

## Proposed modern-luxury alternatives (2026-10-09)

**✅ 2026-10-12: Zed chose Option 04 Riviera Resort for the furnished-home job.** That makes it an approved style for that job. It does not replace Option 01 as his default; the next job still needs the choice confirmed. Riviera's room kit and anchor images are in `projects/zed-style-guide/rooms/04-*` and its prompts are in `prompts/option-04-riviera-resort/`. Known model quirks for Riviera: oval or rectangular tables pick up end chairs, so round tables are the proven fix; and terracotta pots go orange, so call them matte sand stoneware.

Example directions drafted to show Zed, deliverable at [zed-modern-luxury-style-guide.html](../../projects/zed-style-guide/zed-modern-luxury-style-guide.html) (artifact: https://claude.ai/artifact/G4GcAynouMDafi4zVLJLEU). **Option 01 above stays canonical**; none of these is used on a job until Zed picks one and it gets its own full room library.
- **02 Gallery Stone** — chalk/plaster/honed travertine, minimal smoked oak, bronze; curved chalk-bouclé sofa, travertine block coffee table, round travertine pedestal dining. New builds, apartments.
- **03 Smoked Oak Suite** — hotel-suite: mushroom/taupe, espresso oak, cognac leather, smoked glass, antique bronze; channel-stitched king. Prestige listings. Exposure risk: dark palette pulls the frame moody, so prompts pin true exposure.
- **04 Riviera Resort** — limewash/sand linen/travertine/natural oak, muted clay accent instead of olive; oak trestle oval table with cord chairs. Coastal, pool houses.
Each has palette hexes + ratio, per-room kit, exclusions and one Sunburst-style prose prompt with pass-confidence score.

**Visual boards (2026-10-09):** one 10-room board per option on Magnific GPT 2.5 Sunburst (2k medium, 180cr each, 720cr total), stitched into one master sheet: [zed-master-style-guide-web.jpg](../../projects/zed-style-guide/zed-master-style-guide-web.jpg). Learned: Sunburst holds a 5×2 captioned grid + swatch row in one text-to-image pass with readable labels, but it adds footer taglines nobody asked for and can drop a letter in spaced caps. Concept boards only, not listing staging. **v2 (2026-10-12):** rebuilt as 40 separate Nano Banana Pro rooms (one living-room anchor per option, other 9 rooms referencing it; 3,000cr) and assembled in code: much better consistency and no text errors. Remaining failure: "three along each long side" still got end chairs on 4 of 8 dining tables, so it confirms `feedback-no-end-chairs-positive`: use round tables when ends must stay empty. Price check: `gpt-2-mini` + `variant: sunburst` is the real Sunburst; plain `gpt-2` prices at 100cr and is a different model.

Full standing rules: [[staging-rules]]. Pipeline routing and models: [[higgsfield-pipelines]]. Raw source: `raw/zed/option-01-full-staging-library.md` and `raw/zed/option-01-full-staging-asset-library.html`.

## Used by
[[akmal]] · [[zed-full-house]]

---

## Piece-list (superseded 2026-09-15, same session — "sand & walnut" board era)

Warm sand/cream/greige base, dark walnut contrast, olive-green only accent, aged stone/ceramic, antique brass — cream linen sectionals, boucle on timber legs, walnut block coffee tables, sheer linen curtains, olive branches in stone urns, plaster-tone abstract art. This was correct in direction but informal; **Option 01 above is the same style, now formalised with hex codes and per-room kits** — no rooms were actually staged to this exact intermediate spec, so nothing needs re-running from it specifically.

## Piece-list (superseded 2026-09-10 — taupe / olive / boucle era)

Warm taupe / olive / stone neutrals; black allowed (chair legs, side tables); fluted light-oak joinery and walnut bedsides; emerald-green channel-tufted velvet modular sofa in the living room; taupe boucle beds, benches and armchairs; brass mushroom-dome lamps; textured neutral rugs. Kitchen: stone benchtops, fluted cream/taupe fronts. Outdoor: rope/cord chairs, warm-grey cushions.

The whole `zed-full-house` job so far (green sofa living/dining frames, taupe boucle rumpus, deck dining set, master bedroom) was staged to **this** spec and now needs review against Option 01 — see the note on [[zed-full-house]].

## Piece-list (superseded pre-2026-09-10 — white / cream era)

White / cream modern luxury. **No black, no timber furniture.**

**Dining** — white stone/concrete-top table (round or rectangular) on a matte-white pedestal or block base; 4 cream upholstered dining chairs; one low matte-cream ceramic bowl. Approved 2026-08-24, replacing an earlier marble-and-gold version.

**Living** — cream bouclé L-sectional; white marble + brushed-gold rectangular coffee table; cream shag rug wider than the sofa's front legs; one ivory accent chair; gold-stem floor lamp; fiddle-leaf fig in a white ceramic pot.

**Bedroom** — white-gloss bed with a cream bouclé headboard, layered white and cream linen, no more than three accent cushions, folded cream throw; white-gloss bedsides styled differently left and right; gold-stem lamps; kentia palm in white ceramic; cream shag rug clear of the window and door.

**Outdoor / patio** — rectangular white concrete table with 4 cream chairs on the long sides only. Indoor velvet and marble pieces never go outside.
