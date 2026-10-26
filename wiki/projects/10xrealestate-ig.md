---
type: project
tags: [social, instagram, 10xrealestate, carousels]
status: active
updated: 2026-10-26
---

# @10xrealestate_ page polish + content queue

The work turned the @10xrealestate_ Instagram page into a premium real-estate media portfolio for 10x. Deliverables are in [projects/10xrealestate-ig/](../../projects/10xrealestate-ig/SCHEDULE.md).

## What shipped (2026-10-20 to 26)
- **Bio:** "Property film and photography / By @10xvisuals_". No dot lists and no "picture yourself" copy ([[ig-caption-voice]]).
- **Profile pic and highlights** match @10xvisuals_. The pic is a white circle with a black "10" and the original-blue X. Highlights are dimmed listing photos carrying the white and blue 10X mark. App-only steps are listed in `PHONE-TODO.md`.
- **Captions** for the Salt PM reel (no CTA, since the video sells), Boardwalk Tavern (10xConstruction) and 13 Mayra Ct (Kollosche). There are no collab invites on this page ([[kollosche]] won't accept them).
- **Listing carousels, v5.2.** Five decks are built by `build_carousels.py`: 59 Cylinders Dr (Kingscliff), Solis 673 Casuarina Way, the Elanora Ave townhouses (Pottsville; 2/7A and 2/9B merged because they're identical), 10 Australis Ct (Mermaid Waters) and 47 Somerset Dr (Mudgeeraba, Whitefox).
- **Posting planner:** 12 posts, one every 3 days at 7pm from 28 Oct, alternating reel and carousel. It comes with a grid preview, built by `planner/build_planner.py`.

## Design system
The deck is a seamless 9-slide editorial layout:
1. Cover with the street name layered behind the roofline.
2. Banded photo cuts across slides 2 and 3.
3. Tilted prints cut by the seam.
4. A suburb title and a film strip of details.
5. A frame split on the swipe seam.
6. A full bleed.
7. A closing hero.

It uses warm paper and the original 10x blue #61a8d8. Full rules are in auto-memory `template-10xrealestate-carousel.md`.

## What it taught us
- **Hunter's standing rules:**
  - No navy and no end cards.
  - Close on a hero.
  - Real suburbs, never regions.
  - Drones only when punched-in, never wide views.
  - At most 2 bedrooms per deck.
  - Merge identical shoots.
  - Construction jobs belong on the construction page.
- **Sky-masked headlines look great on a clean roofline**, but they tear on dusk sky behind a treeline. Those covers use front-set type in the open sky.
- **Audit at the 3:4 profile-grid crop.** Full-width headlines lose their edge letters there.
- **References were what moved the design.** v4 read as a template. v5 came after studying five carousel references Hunter sent: layered type, cut photos, tilted frames and film strips.

## Open
- Grandview Hotel: confirm it belongs on the real-estate page or the construction page.
- 13 Mayra Ct has no photos, so it posts as a reel only.
- Reel covers still need setting in the app, and the videos haven't been QC'd.
- Division colour idea: the construction page X goes orange (AI is purple). Not actioned.
