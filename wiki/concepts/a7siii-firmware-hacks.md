---
type: concept
tags: [gear, sony, a7siii, firmware, research]
status: research-only
updated: 2026-11-12
---

# Sony a7S III firmware hacks (community feature-unlock scene)

Research snapshot of the unofficial a7S III (ILCE-7SM3) feature-unlock scene as of **Nov 2026**. **Nothing here has been run on Hunter's camera. Verdict: leave the working body stock.** This page exists so the topic isn't re-dug in three months.

## Why this suddenly exists
A firmware-decryption key for Sony's CXD90057 camera platform was reportedly published ~Sept 2026. That let people unpack the official firmware images offline and map how each hidden menu is *gated* — i.e. which FX3/cinema features physically exist in the a7S III's code but are switched off by a product-class flag. The Doom-on-a7S-III story that kicked this off is a side-effect of the same code-execution route, not the point.

## The features in play
- **Shutter angle** — express exposure as a shutter *angle* (e.g. 180°) instead of a shutter *speed* (1/50). See the explainer below. This is the FX3/cinema way of working.
- **Variable Shutter** — fine, continuous shutter-speed trim to cancel flicker from LEDs / monitors (match 100 Hz, 120 Hz, etc.). The one genuinely useful item for interiors.
- **BIG6** — the six-box FX3-style home/control dashboard: frame rate, ISO, shutter, iris, look profile, white balance in one view. A UI, not a secret capability.
- **Cine EI / base ISO selection / full Cinema Line menu** — the FX3 log-shooting workflow.
- **Open Gate** — full-sensor 3:2 readout.

## Status — straight
| Feature | a7S III | Reality (Nov 2026) |
|---|---|---|
| Shutter angle (display) | fw 5.01 | Reported working by **one owner** ("Rambo", 22 Oct). Reversible. Dial/touch *adjustment* may still be gated. |
| Variable Shutter | fw not stated | **Screenshots only, one user** (CoupleMother1623, 3 Nov). No installer, not reproduced. |
| BIG6 | same | Same single demo. |
| Cine EI / base ISO / Cinema menu | — | **Blocked** — tied to the FX3 product class. |
| Open Gate | — | **Blocked** — no open-gate readout mode in the firmware. |
| Doom | — | Runs via the same root payload; method unpublished. |

Nothing above is independently verified by a second tester.

## Two methods — they are not the same risk
1. **Shutter angle (the tame one):** a *settings* write via the open-source `Sony-PMCA-RE` tool in USB service mode. Back up settings, change one property, cold reboot (battery out 10 s). Firmware is left untouched. Persists, and is undone by writing the old value back.
   - Properties (a7S III 5.01, from firmware analysis): shutter **mode** `0x02cf15a5` (`00` speed / `01` angle), **angle** `0x02cf15a7` (`10` = 180°).
2. **Variable Shutter / BIG6 / Doom (the dangerous one):** a payload (`libJit.so`) pushed through a hidden USB update channel ("Jiritsu") that works even in Mass Storage mode. It loads **as root** in the main app process and patches menus in RAM. A reboot wipes it — **unless** you write the camera's persistent Backup settings memory, which survives and has **no stated undo**.

## The brick (why this matters)
An **A7 IV** (not a7S III), Reddit user Mr_BananaPants: camera fell into a **boot loop after an 8K attempt**, traced to a path-traversal bug used to pull decrypted firmware. **No recovery reported anywhere.** The first A7 IV hacker explicitly warned about bricking.

## Warranty
- Sony US excludes "rooting or other modifications to control the behavior of the product."
- Sony EU excludes unauthorised adaptations / "upgrading beyond specifications described in the manual." EU 2-year statutory rights against the *seller* survive; US warranty is void.

## Verdict for 10x
**Don't touch the working a7S III.** The only safe-ish unlock (shutter angle) is still single-source; the genuinely useful one (variable shutter) is the un-reproduced, persistent-write, no-undo path from the same family that bricked an A7 IV. A dead body mid-shoot costs the job. If curiosity wins later: **spare body only, shutter-angle only, never near a booking.** Related: [[mac-performance]] (gear discipline mindset).

## Sources
- SonyAlphaRumors — [Variable Shutter & BIG6](https://www.sonyalpharumors.com/the-hacking-continues-variable-shutter-and-big6-added-on-the-sony-a7s-iii/), [shutter angle on a7S III](https://www.sonyalpharumors.com/new-shutter-angle-hack-works-on-the-sony-a7siii-too/), [it runs Doom](https://www.sonyalpharumors.com/yes-it-runs-doom-someone-turned-the-sony-a7s-iii-into-a-gaming-machine/)
- [4Filmmakers — what works, what it risks](https://www.4filmmakers.co/news/sony-a7s-iii-a7-iv-shutter-angle-hack/)
- [PhotographyTalk — read the risks first](https://www.photographytalk.com/sony-a7s-iii-hack-variable-shutter-big6/)
- GitHub (method/analysis, no Sony material): [leogenot/sony-a7iv-feature-research](https://github.com/leogenot/sony-a7iv-feature-research), [domalhambra/plateworks-shutterlock](https://github.com/domalhambra/plateworks-shutterlock)
- Original Reddit posts (fetch-blocked, via secondary coverage): r/A7siii threads by Rambo (shutter angle) and CoupleMother1623 (variable shutter / BIG6 / Doom)
