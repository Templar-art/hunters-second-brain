---
type: project
tags: [instagram, carousel, 10xvisuals]
status: built, not posted
updated: 2026-11-04
---

# @10xvisuals_ main-page listing carousels

Main-page (@10xvisuals_) versions of the [[10xrealestate-ig]] v5.2 seamless 9-slide decks, for shoots with the editorial look. Same generator (`projects/10xrealestate-ig/build_carousels.py`), separate config: [carousels.json](../../projects/10xvisuals-ig/carousels.json), built with `python3 ../10xrealestate-ig/build_carousels.py carousels.json .` from `projects/10xvisuals-ig/`.

## Decks (2026-11-04)
| Deck | Client | Source |
|---|---|---|
| 5 Esther Place, Surfers Paradise | Kollosche | Frame.io › Kollosche › Photos/Print |
| 2/116 Seagull Avenue, Mermaid Beach | Kollosche | Frame.io Print |
| 13-15 Eagleview Court, Bonogin | Whitefox | Frame.io Print |
| 39 Harold Street, Stafford | Kodiak Projects | Frame.io Photos |
| 37 Southaven Drive, Helensvale | Belle Property | REA Drive pull (layout B) |
| Club Robina, Grand View Hotel, Victoria Point Sharks, CSi Southport, Westside HQ (C), Lions @ Springwood (B) | SHAPE | Frame.io Photos (also on construction page) |
| 59 Cylinders Dr, 10 Australis Ct, 47 Somerset Dr (B); Solis 673 Casuarina Way, 2/7A + 2/9B Elanora Ave Pottsville (C) | various | REA To Post folders |

Photos pulled via Chrome from Frame.io (10x Clients project) into `Documents/10x Drive Pulls/<client>/`.

## Layout variants (2026-11-04, v2)
Hunter asked that decks not all look the same, then rejected the first B/C attempt (grids, staggered columns, room-index list, overlapping collage) as messy: "it needs to show our work, it's for a media page." v2 gets variety from pacing, not collage. `"layout"` per listing:
- **A**: original v5.2 paper deck (bands, tilted prints, film strip, seam split).
- **B "Cinema"**: ink; full-bleed cover; slides 2-3 and 6-7 are one photo panned across the seam; full bleeds; one clean stacked pair; full-bleed hero. Pan slots (p1, p5) need wide, striking frames, never a bathroom.
- **C "Framed"**: paper; one large framed photo per slide with even margins; a framed pan across slides 4-5; one stacked pair; full bleed; framed hero.
Current: A = Esther, Eagleview; B = Harold, Robina, Southaven; C = Seagull, Grand View, Sharks, CSi. Rule saved to auto-memory as feedback-media-page-show-the-work.

## SHAPE on the construction page (2026-11-04)
Six SHAPE venues added to [10xconstruction-ig](../../projects/10xconstruction-ig/carousels.json) from Frame.io › SHAPE › Photos: Club Robina (B), Grand View Hotel Cleveland (C), Westside HQ Corinda (A), Lions @ Springwood (B), Victoria Point Sharks (C), CSi Club Southport (A). Covers avoid shots where the venue's own signage repeats the headline (Lions, CSi).

## Cut / skipped
- Buckingham Way (Elanora) and 506/388 Marine Parade: built, then cut by Hunter as not editorial enough.
- Westside HQ and Lions @ Springwood: added to main page too (Hunter: shows what we do).
- Pan slots: never a bedroom/bathroom across the seam; Solis + Elanora swapped p3/p10 so the pan is the best wide.
- Belle: 25 Bunderoo Circuit (project home) and 5 Jackson St (Drive; cluttered, occupied) skipped; no editorial Belle shoot yet. 84 Southaven, 13 Mayra Ct, 53 Tenth St: video only.


## What it taught us
- Hunter wants these batches fully automated: look up suburbs yourself, judge editorial quality yourself, don't ask.
- Suburb lookup that works when web search is blank: reverse-geocode a drone photo's GPS (`mdls -name kMDItemLatitude`) via OpenStreetMap Nominatim. Harold St → Stafford this way.
- Frame.io duplicates filenames with `(1)` suffixes on re-download; filter by mtime when sorting.
- Mermaid Beach for Seagull Ave is unverified.
