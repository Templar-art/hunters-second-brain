# @10xrealestate_ posting schedule (draft, 2026-10-26)

One post every 3 days at 7pm AEST. Alternates Kollosche and Salt PM, and alternates reel and carousel.
Carousels are 4:5 exports in `carousels/`. Videos come from `~/Documents/Posting for 10xRealestate/To Post/`.
Caption rule: mention the client and agents, no collab invites, no "picture yourself" hooks.

| # | Date | Listing | Format | Client |
|---|------|---------|--------|--------|
| 1 | Tue 28 Oct | 13 Mayra Ct, Mermaid Waters | Reel (main video) | Kollosche |
| 2 | Fri 31 Oct | 59 Cylinders Dr | Carousel | Salt PM |
| 3 | Mon 3 Nov | 10 Australis Ct | Reel | Kollosche |
| 4 | Thu 6 Nov | Solis, 673 Casuarina Way | Carousel | Salt PM |
| 5 | Sun 9 Nov | 59 Cylinders Dr | Reel | Salt PM |
| 6 | Wed 12 Nov | 2/7A Elanora Ave | Carousel | Salt PM |
| 7 | Sat 15 Nov | Solis, 673 Casuarina Way | Reel | Salt PM |
| 8 | Tue 18 Nov | 10 Australis Ct | Carousel (8, no drones) | Kollosche |
| 9 | Fri 21 Nov | 2/7A Elanora Ave | Reel | Salt PM |

Skipped: 2/9B Elanora Ave. It's the same complex and finishes as 2/7A, so it would read as a repeat. Hold it for later.
The videos themselves haven't been QC'd. Picks were made from the photos.

## Carousel design (v2, 2026-10-26)
Built by `build_carousels.py` from `carousels.json`, at 4:5 1080x1350 with no drone shots. Slide 1 is a full-bleed hero with the address, a navy rule and the suburb. After that, full-bleed photos alternate with stacked pairs on navy #102f41, and some slides carry a small room label. The deck closes on a navy end card with the 10X mark, "PHOTOGRAPHY · FILM" and the handle. Every slide has the mark top-left and the page index top-right, and every photo gets one subtle grade. To edit a deck, change the slide list in carousels.json and rerun the script.
