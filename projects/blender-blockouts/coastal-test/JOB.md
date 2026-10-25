---
client: internal-rnd
address: Coastal house (invented Gold Coast beach house, test build)
opened: 2026-10-26
status: review        # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 8.25, aud: 0 }   # derived from ## Ledger
---

# Job — Coastal house drone reveal (guide frame for AI)

First build after the Blender MCP add-on update and asset-library switch-on. An invented two-storey beach house built entirely by the kit (`house` generator, beach `site`/`landscape`), no imported geometry. Spec: [coastal.scene.json](coastal.scene.json). 1,405 objects, built in about 4 s (9 s with renders).

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | C1 street drone reveal (8 s, 192 f, 24 mm) | guide + ID → Sunburst stills → video | stills PASS 3/3 | Starts low on the street, rises over the roof and ends on the pool, dunes and ocean. Guides + ID at frames 1 / 97 / 192 in `build/` (local) |

## Log

- 2026-10-26 build: v1 → v3. Added front-fence and entry planting plus verge trees; trimmed the trees that blocked the facade; pushed the end frame higher and toward the sea so the pool clears the balcony.
- 2026-10-26 kit fixes found on this build: (1) `copy_obj` copied the template's hidden flag, so every kit tree came out invisible (beach rebuild included); (2) ID rule order sent "footpath" to timber red; (3) `island_tree` trunks matched the kitchen-island rule and came out stone orange. All fixed in `blender-kit/kit/`.
- 2026-10-26 generate: 3 × GPT Image 2.5 Sunburst (high, 2K, 16:9), guide + ID map as Image 1 / Image 2, quoted 8.25 HF and spent 8.25 HF. QC: **all 3 PASS first time.** Layout, framing, house, pool, boardwalk and people positions all held; the palms and trees came out real (the "placeholder" wording worked). Small drift: the sandy side verge became a gravel path and the front pad became concrete, both acceptable. The house reads the same across all 3 (timber garage door, 3 dark-framed upper windows), so the stills work as start and end frames. Comparison: `stills/guide-vs-still.jpg`.
- Next: video. Start frame f001 → end frame f192 (first/last-frame), quote before running.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
- 2026-10-26 | 2.75 hf | c1_f001 gpt_image_2_5 (gen-runner)
- 2026-10-26 | 2.75 hf | c1_f097 gpt_image_2_5 (gen-runner)
- 2026-10-26 | 2.75 hf | c1_f192 gpt_image_2_5 (gen-runner)

---
_Vault: [[jarvis]]_
