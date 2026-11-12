# @10xconstruction_ profile pack

This pack matches @10xrealestate_: a short two-line bio, a white avatar with the colour 10X, and darkened photo highlights with the 10X in the centre.

## Avatar
Use `highlights/avatar.png`. It replaces the current black disc.

## Name field
10x Visuals · Construction (keep it, it's already parallel to "10x Visuals · Real Estate")

## Category
The label is hidden, to match the real-estate account (applied 2026-11-12).

## Bio
```
Construction film and photography
By @10xvisuals_
```

## Link
Remove the `?fbclid=` link. The real-estate account has no link, so either drop it to match or use plain `10xvisuals.com.au`.

## Highlights (in this order)
| Title | Cover | Source frame |
|---|---|---|
| Commercial | highlights/commercial.png | Maroochy RSL (Ashley Cooper) |
| Hospitality | highlights/hospitality.png | Prince Hotel cocktail bar (Ashley Cooper) |
| Education | highlights/education.png | Rivermount College (Ashley Cooper) |
| Residential | highlights/residential.png | West End kitchen (Livit) |
| Films | highlights/films.png | Grandview Hotel (SHAPE) |

Rebuild with `~/.venvs/typeset/bin/python highlights/build_highlights.py`.

## Grid
New posts use the same carousel/cover system as real estate (`../10xrealestate-ig/build_carousels.py carousels.json .`): a large white Poppins project name and a small 10X top left. The queued decks in SCHEDULE.md are already in that style. Once they're posted, the talking-head tiles drop below the fold.

## Status (2026-11-12)
- Applied: avatar, bio, category label hidden.
- Pending: the website link must be cleaned to `10xvisuals.com.au` in the mobile app. The 14 story frames in `highlights/stories/` need posting through Business Suite, and then the 5 highlights get built from the web profile's New button.
