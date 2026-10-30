---
client: {client-slug}
address: {street address}
opened: {YYYY-MM-DD}
status: intake        # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 30, aud: 0 }   # derived from ## Ledger
---

# Job — {address}

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | {shot name} | full-frame / masked / video | todo | |

## Log

- {YYYY-MM-DD} intake: {N} shots triaged

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- Higgsfield batches: gen_runner.py run appends here. Magnific/MCP or web spends: gen_runner.py log JOB.md <amount> <hf|cr|aud> <note> -->
- 2026-10-30 | 2 hf | 14_newangle nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | A_kitchen_to_balcony nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | B_balcony_looking_back nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | C_glass_looking_in nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | W08_kitchen nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | W09_living nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | W10_bedroom nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | W11_dining nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | W03_amenity_dining nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | W04_rooftop_dining nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | W05_gym nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | W02_pool nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | W01_pool_daybed nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | W06_tower nano_banana_2_1 (gen-runner)
- 2026-10-30 | 2 hf | W07_entry nano_banana_2_1 (gen-runner)

---
_Vault: [[jarvis]]_
