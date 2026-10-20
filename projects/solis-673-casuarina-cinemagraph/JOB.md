---
client: salt-pm
address: Solis, 673 Casuarina Way
opened: 2026-10-20
status: review            # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 160, aud: 0 }   # derived from ## Ledger
---

# Job — Solis, 673 Casuarina Way (pool cinemagraph)

Source: `Posting for 10xRealestate/To Post/Solis 673 Casuarina Way | SALTPM/Photos/Solis 673 Casuarina Way _ Salt PM-16.JPG` (9504×6336), cropped 9:16 at x=3270, w=3564 → `hero/solis16_916.jpg` (1080×1920).

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | Pool cinemagraph, 10s 9:16 | video (Seedance 2.5 i2v, 1080p, no audio) | review | locked camera; only pool water + wall spout move; composite still back over non-water if drift |

## Log

- 2026-10-20 intake: 1 shot; Hunter approved Seedance 2.5 1080p 10s 9:16 (160 hf est.)
- 2026-10-20 v1 generated (Seedance 2.5, 1080p, 10s, 9:16). QC: frame locked, only water + spout move, woman holds still. gen_runner NO_MOTION flag is a false positive for cinemagraphs (whole-frame metric). Awaiting Hunter review.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- Higgsfield batches: gen_runner.py run appends here. Magnific/MCP or web spends: gen_runner.py log JOB.md <amount> <hf|cr|aud> <note> -->
- 2026-10-20 | 160 hf | pool_cinemagraph seedance_2_5 (gen-runner)

---
_Vault: [[jarvis]]_
