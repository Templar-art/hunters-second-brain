---
client: tbc
address: "Vista" (render set, 12 renders)
opened: 2026-10-20
status: intake         # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 35, aud: 0 }   # derived from ## Ledger
---

# Job — Vista renders → cinemagraphs

Source: 12 developer renders pasted by Hunter (2000×1368) → `inputs/1–12.jpg`. Brief: camera locked, only real ambient motion (curtains, trees, fans, sun streaks drifting). Recipe from [[solis-pool-cinemagraph]]: Seedance 2.5 i2v, hard camera lock + still-list. Picks cropped centre 16:9 → `hero/*_169.jpg` (1920×1080).

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 8 | Bedroom: 2 fans, curtain, trees, sun band | video (Seedance 2.5 720p 5s, start=end frame) + local loop/upscale | review | `video/08_bedroom_v1_loop15_1080.mp4` |
| 11 | Hallway: sheer curtain, sun beams creep, skylight leaves | video | todo | |
| 5 | Powder: tree in window, wall sun patch dapple | video | todo | |
| 6 | Kitchen: floor sun stripes creep, garden | video | todo | |
| 4 | Living: palms outside, ceiling sun patches | video | todo | |
| 1 | Exterior: palm fronds + their shadows on garage/drive | video | todo | |
| 2,3,7,9,10,12 | gate, office, laundry, towel nook, gym, ensuite | — | reserve | weaker motion or mirror/signage risk |

## Log

- 2026-10-20 intake: 12 renders, 6 picked, 16:9 silent. Hunter asked for cheaper: switched 1080p 10s (160 hf) → 720p 5s with end-image = start-image for a seamless loop (35 hf). Batch est 210 hf (was 960).
- 2026-10-20 bedroom pilot (Hunter go, 35 hf): frame locked, both fans spin, curtain sways, furniture holds. gen_runner NO_MOTION = whole-frame false positive again (fan/curtain region diff ~0.9 vs wardrobe 0.05). Looped 3× with 0.4s crossfades → 15s, lanczos 1920×1080 + light unsharp (0 credits). Awaiting Hunter review.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
- 2026-10-20 | 35 hf | 08_bedroom seedance_2_5 (gen-runner)
