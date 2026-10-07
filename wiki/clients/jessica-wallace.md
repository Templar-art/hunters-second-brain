---
type: client
tags: [client, real-estate, staging, harcourts]
status: active
updated: 2026-10-07
---

# Jessica Wallace — Harcourts Property Hub

**Client:** Jessica Wallace, Harcourts Property Hub. Sales agent; 10x does her virtual staging.
**Prior work:** the Jessica Wallace IG post set — logo/headline placement varies deliberately per post (auto-memory `feedback-varied-post-placement`).

## Coastal Luxury staging job — 17 Sep 2026

First staging job for this client. Nine raw, unstaged interiors of a dated but well-kept single-level home (white gloss tile throughout, honey hardwood in the main living, cream shaker kitchen with a gold-flecked granite benchtop and aqua glass splashback). Jessica had already paid someone else to stage them and the results were poor — 10x is the redo.

**Style:** her own "Coastal Luxury" concept sheet — warm white dune / linen natural / sand stone / coast soft blue / sage olive / oak natural; linen modular sofas, oak-framed linen occasional chairs, jute rugs, framed coastal art, real greenery, minimal styling. The sheet is a mood board for Claude to translate into words — **never cite it as a reference image in a prompt**, Jessica's look has to be described.

**Client-specific override:** ❌ **no curtains, on any shot.** Contradicts the standing curtains-by-default rule in [[staging-rules]] — logged as an exception on `feedback-curtains-default-and-anchor`.

**Room map** (confirmed with Hunter, never inferred): 1, 3, 8 secondary bedrooms · 2 dining · 4 + 6 open-plan kitchen-living, two angles of one room · 5 second living · 7 main living · 9 master.

**Model:** GPT Image 2.5 "Sunburst", not Nano Banana Pro. Every pass run from the raw.

### What this job taught us
Five rules came out of it, all now on [[staging-rules]] with canonical versions in auto-memory:
- **Framing lock** — Sunburst silently re-crops and zooms (`feedback-lock-camera-framing`).
- **Geometry lock** — rugs rendered twisted; tie rug edges to grout lines / floorboard direction (`feedback-square-to-the-room-geometry`).
- **Mirror reflections** — the mirrored robe reflected an empty room next to a made bed (`feedback-mirrors-must-reflect-staging`).
- **Exact inventory** — without "the room contains exactly these pieces and nothing more", it invented a console and layered a second rug.
- **Prose, not checklists** — Hunter rejected the bold-region-heading prompt format twice (`feedback-prompt-prose-not-checklist`).

Also confirmed: **a piece assigned to an occupied wall makes the model delete the fixture.** A sofa placed "on the wall between the two windows" deleted the timber display cabinet standing there. (Jessica later asked for that cabinet removed anyway, with a TV on the right wall — but the failure mode is general.)

**Flatness fix:** the first three came back flat — the raws are HDR-flattened agent photos, everything sat in one beige tonal band, and "soft diffused daylight" asked for flatness. Fixed with three lifts: a rug in every room including secondary bedrooms (the gloss tile needs the warmth — overrides the usual no-rug-in-secondaries rule), one deeper tone per room to break the beige, and directional light with a soft cast shadow.

**Open limitation:** these models have no depth map — they paint furniture onto a flat image rather than solving the floor plane. Wide real-estate lenses make it worse. Prompt anchors help but don't fully solve it; Hunter finished the set with manual Photoshop transforms and a raw-over-staged composite for a distorted wall. Worth watching for a depth-aware staging tool if this becomes regular work.

**Expectation to set with clients like this:** the mood board is a new build with ocean views; the house is not. Fixtures are locked, so staging delivers *nicely furnished dated home*, not the sheet. Say it before delivery, not after.

## Office staging — 7 Oct 2026

Single extra room: a small office with a white-painted louvre window, frosted glass door, two **built-in** floating oak shelves, polished concrete floor, and an existing oak L-desk with a tan leather chair. Jessica did not like how it was already staged, but Hunter liked the desk — it needed *more*, not replacing.

**Model:** Nano Banana 2.1 (`nano_banana_2_1`, 2 credits at 2k) — first run of it in the vault. Held the exact framing, kept every fixture, square rug, one lamp. Better first-pass fidelity than expected.

**What the job taught us (client rules, apply to all her rooms):**
- ❌ **No standing plants, none in corners.** Dried stems in a vase on a surface are fine. Overrides greenery-by-default in her Coastal Luxury style.
- **Replace the existing staging, keep what Hunter says is good.** Built-in shelves are fixtures — lock them by name ("built-in", same timber/size/position); restyle only the props on them.
- Run 1 (olive tree, armchair + side table, laptop screen toward camera) was rejected: the armchair and plant were too much, and the laptop must face the chair, so the camera sees the plain lid back with no logo.
- Run 2 (desk + leather chair kept, jute rug, open laptop facing the chair, sage lamp, shelf props in the palette) was the keeper. Remaining nits: rug oversized and cropped by the frame edge, books overlapping the laptop corner.
- Chair/laptop orientation: name the person's seat and turn the screen to it — models default to screen-to-camera otherwise.

Related: [[staging-rules]], [[higgsfield-pipelines]].
