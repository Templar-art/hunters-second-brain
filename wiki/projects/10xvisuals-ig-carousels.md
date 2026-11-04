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

Photos pulled via Chrome from Frame.io (10x Clients project) into `Documents/10x Drive Pulls/<client>/`.

## Cut / skipped
- Buckingham Way (Elanora) and 506/388 Marine Parade: built, then cut by Hunter as not editorial enough.
- 25 Bunderoo Circuit (Belle): standard project home, skipped. 84 Southaven, 13 Mayra Ct, 53 Tenth St: video only.
- SHAPE: clubs/venues, not listings; undecided.

## What it taught us
- Hunter wants these batches fully automated: look up suburbs yourself, judge editorial quality yourself, don't ask.
- Suburb lookup that works when web search is blank: reverse-geocode a drone photo's GPS (`mdls -name kMDItemLatitude`) via OpenStreetMap Nominatim. Harold St → Stafford this way.
- Frame.io duplicates filenames with `(1)` suffixes on re-download; filter by mtime when sorting.
- Mermaid Beach for Seagull Ave is unverified.
