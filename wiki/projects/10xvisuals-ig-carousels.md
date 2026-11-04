---
type: project
tags: [instagram, carousel, 10xvisuals]
status: built, not posted
updated: 2026-11-04
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

Photos pulled via Chrome from Frame.io (10x Clients project) into `Documents/10x Drive Pulls/<client>/`.

## Layout variants (2026-11-04)
Hunter asked that the decks not all look the same. `build_carousels.py` now takes `"layout"` per listing: **A** original paper deck, **B** "Gallery" (ink pages, left-set cover, seamless panorama, 2×2 grid, vertical place name, staggered columns, full-bleed close), **C** "Magazine" (paper cover with name under the photo, overlapping collage, room index page, framed hero). Rotate A/B/C across a feed. Seagull = C, Harold = B.

## SHAPE on the construction page (2026-11-04)
Six SHAPE venues added to [10xconstruction-ig](../../projects/10xconstruction-ig/carousels.json) from Frame.io › SHAPE › Photos: Club Robina (B), Grand View Hotel Cleveland (C), Westside HQ Corinda (A), Lions @ Springwood (B), Victoria Point Sharks (C), CSi Club Southport (A). Covers avoid shots where the venue's own signage repeats the headline (Lions, CSi).

## Cut / skipped
- Buckingham Way (Elanora) and 506/388 Marine Parade: built, then cut by Hunter as not editorial enough.
- Belle: 25 Bunderoo Circuit (project home) and 5 Jackson St (Drive; cluttered, occupied) skipped; no editorial Belle shoot yet. 84 Southaven, 13 Mayra Ct, 53 Tenth St: video only.


## What it taught us
- Hunter wants these batches fully automated: look up suburbs yourself, judge editorial quality yourself, don't ask.
- Suburb lookup that works when web search is blank: reverse-geocode a drone photo's GPS (`mdls -name kMDItemLatitude`) via OpenStreetMap Nominatim. Harold St → Stafford this way.
- Frame.io duplicates filenames with `(1)` suffixes on re-download; filter by mtime when sorting.
- Mermaid Beach for Seagull Ave is unverified.
