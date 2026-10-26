# @10xrealestate_ posting schedule (draft, 2026-10-26)

One post every 3 days at 7pm AEST. Alternates Kollosche and Salt PM, and alternates reel and carousel.
Carousels are 4:5 exports in `carousels/`. Videos come from `~/Documents/Posting for 10xRealestate/To Post/`.
Caption rule: mention the client and agents, no collab invites, no "picture yourself" hooks.

| # | Date | Listing | Format | Client |
|---|------|---------|--------|--------|
| 1 | Tue 28 Oct | 13 Mayra Ct, Mermaid Waters | Reel (main video) | Kollosche |
| 2 | Fri 31 Oct | 59 Cylinders Dr | Carousel | Salt PM |
| 3 | Mon 3 Nov | 10 Australis Ct | Reel | Kollosche |
| 4 | Thu 6 Nov | 673 Casuarina Way (Solis) | Carousel | Salt PM |
| 5 | Sun 9 Nov | 59 Cylinders Dr | Reel | Salt PM |
| 6 | Wed 12 Nov | 2/7A Elanora Ave | Carousel | Salt PM |
| 7 | Sat 15 Nov | 673 Casuarina Way (Solis) | Reel | Salt PM |
| 8 | Tue 18 Nov | 10 Australis Ct | Carousel | Kollosche |
| 9 | Fri 21 Nov | 2/7A Elanora Ave | Reel | Salt PM |

Skipped: 2/9B Elanora Ave. It's the same complex and finishes as 2/7A, so it would read as a repeat. Hold it for later.
The videos themselves haven't been QC'd. Picks were made from the photos.

## Carousel design (v4, 2026-10-26)
Built by `build_carousels.py` from `carousels.json`. Each deck is composed on one long 9-slide canvas and then sliced, so photos run across the swipe seams: slide 1 is the cover, slides 2 and 3 share a panorama, slides 4 and 5 have tall bleeds with a frame cut by the seam, slides 6 and 7 have a frame straddling the seam with an inset detail, slide 8 is full bleed, and slide 9 is a top bleed with an inset. The background is warm paper #f6f4f0 with the original blue #61a8d8 for accents and the X. There's no end card and no navy. Each listing has 10 photos, set in carousels.json, all ground level with no drones.
