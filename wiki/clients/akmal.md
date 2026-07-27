---
type: client
tags: [virtual-staging, real-estate]
status: delivered
updated: 2026-07-27
---

# Akmal — 1007/180 Marine Parade

Virtual staging job, delivered 14 Jul 2026. Full [[zed-style]] restyle of an apartment: open-plan living/dining/kitchen from four angles, master bedroom, ensuite, study nook. Existing dark furniture (black leather living set, black round dining set) was **replaced**, not added to an empty room.

Job file: `projects/akmal/JOB.md`. Cost: 14 credits (~$0.56).

## What it taught us

- **Filename scrambles cost credits.** Three dining prompts were run on frame `-3`, which was actually the master bedroom. ~7 credits wasted before the mapping was caught. The JOB.md now carries a locked true-file mapping block at the top — worth copying on any job where the source filenames don't describe the room. Related: never infer the room from the photo, ask ([[staging-rules]]).
- **Seedream's composition lock is trustworthy.** The proof was accidental: fed the wrong room, it faithfully kept that room's shell instead of drifting toward the prompt.
- **Division of labour settled here** — Hunter runs the generations himself on Seedream; Claude supplies prompts and does the Magnific upscale finish on keepers. That split has held on later jobs.
- Consistency came from anchor-frame transfer: approve the widest frame first, then transfer it into the rest ([[staging-rules]]).

## Links
[[zed-style]] · [[staging-rules]] · [[higgsfield-pipelines]]
