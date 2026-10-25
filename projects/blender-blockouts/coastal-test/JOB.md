---
client: internal-rnd
address: Coastal house (invented Gold Coast beach house, test build)
opened: 2026-10-26
status: review        # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 0, aud: 0 }   # derived from ## Ledger — never edit by hand
---

# Job — Coastal house drone reveal (guide frame for AI)

First build after the Blender MCP add-on update and asset-library switch-on. An invented two-storey beach house built entirely by the kit (`house` generator, beach `site`/`landscape`), no imported geometry. Spec: [coastal.scene.json](coastal.scene.json). 1,405 objects, built in about 4 s (9 s with renders).

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | C1 street drone reveal (8 s, 192 f, 24 mm) | guide + ID → Sunburst stills → video | guides done | Starts low on the street, rises over the roof and ends on the pool, dunes and ocean. Guides + ID at frames 1 / 97 / 192 in `build/` (local) |

## Log

- 2026-10-26 build: v1 → v3. Added front-fence and entry planting plus verge trees; trimmed the trees that blocked the facade; pushed the end frame higher and toward the sea so the pool clears the balcony.
- 2026-10-26 kit fixes found on this build: (1) `copy_obj` copied the template's hidden flag, so every kit tree came out invisible (beach rebuild included); (2) ID rule order sent "footpath" to timber red; (3) `island_tree` trunks matched the kitchen-island rule and came out stone orange. All fixed in `blender-kit/kit/`.
- Next: on Hunter's go, Sunburst stills from the 3 guides (~2.75 HF each, ~8.25 HF), then a first/last-frame video.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->

---
_Vault: [[jarvis]]_
