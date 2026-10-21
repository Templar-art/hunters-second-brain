---
client: salisbury
address: "Vista" (render set, 12 renders)
opened: 2026-10-21
status: generating        # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 0, aud: 0 }   # derived from ## Ledger — never edit by hand
---

# Job — Vista renders → 1:1 Blender rebuilds

The brief: rebuild each of the 12 Vista developer renders in Blender, room by room, 1:1: same camera, geometry, materials and light. The point is to own the scenes. Any time of day ([[sky-library]] golden/blue hour), real camera moves, no AI. Inputs are the same 12 renders as `vista-render-cinemagraphs/inputs/`.

Method: one headless script per room (`scripts/room_XX.py`, Cycles). Camera matched by vanishing points. Geometry is primitives sized off the render. Materials are CC0 Poly Haven/ambientCG textures. The sun is matched to the shadow directions. Every room is QC'd as a side-by-side against the render. Pilot room first, then batch, as Hunter decides.

## Shots

| # | Room | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 5 | Powder | Blender rebuild | pilot | simplest geometry, one-point perspective |
| 1 | Exterior | Blender rebuild | todo | hardest (palms, stone, plants) |
| 2 | Gate | Blender rebuild | todo | |
| 3 | Office | Blender rebuild | todo | |
| 4 | Living | Blender rebuild | todo | |
| 6 | Kitchen | Blender rebuild | todo | |
| 7 | Laundry | Blender rebuild | todo | |
| 8 | Bedroom | Blender rebuild | todo | |
| 9 | Towel nook | Blender rebuild | todo | |
| 10 | Gym | Blender rebuild | todo | mirror wall |
| 11 | Hallway | Blender rebuild | todo | |
| 12 | Ensuite | Blender rebuild | todo | |

## Log

- 2026-10-21 intake: Hunter wants 1:1 Blender rebuilds, room by room; no AI. Pilot = powder (#5).
- 2026-10-21 powder pilot v11 (0 credits, ~1 min Cycles at 2000×1368, 256 spp). Camera solved from the one-point VP; geometry lines up in the 50% overlay (window, arched niche, counter, pedestal, basin, mirror, taps, towel bar). Materials: flat paint, procedural finger tiles / travertine / crazy pave, brass. Light: sun through the window plus two hidden area fills (the original is lit from behind-left of camera). Brightness was matched region by region against the render. The window view is the original's pixels on a camera-only backplate (still to do: a real garden for other times of day). Lessons: Cycles blocks direct sun through a refractive pane (set the pane shadow-invisible); area lights emit along local −Z (one fill pointed out of the room); the Poly Haven plaster read blotchy, so painted walls are flat colour + faint bump. Known gaps: the sun patch is softer and lacks the original's long diagonal lower lobe; tiles are a simpler stack pattern; products and towel are simplified. → `renders/05_powder_v11.png`, `renders/05_cmp_v11.jpg`, `.blend` alongside. Awaiting Hunter review.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- Higgsfield batches: gen_runner.py run appends here. Magnific/MCP or web spends: gen_runner.py log JOB.md <amount> <hf|cr|aud> <note> -->

---
_Vault: [[jarvis]]_
