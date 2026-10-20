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
| 1 | Pool cinemagraph, 10s 9:16 | video (Seedance 2.5 i2v) + local sky composite | review | v2 = v1 water + still sky slow-zoomed 16% from top-right under a sky mask (work/build_v2.py), 0 credits |

## Log

- 2026-10-20 intake: 1 shot; Hunter approved Seedance 2.5 1080p 10s 9:16 (160 hf est.)
- 2026-10-20 v1 generated (Seedance 2.5, 1080p, 10s, 9:16). QC: frame locked, only water + spout move, woman holds still. gen_runner NO_MOTION flag is a false positive for cinemagraphs (whole-frame metric). Awaiting Hunter review.
- 2026-10-20 Hunter: sky should move too → v2_sky built locally (0 credits): sky masked from the still (geo polygon + colour key, eave pocket forced), zoomed 1.00→1.16 anchored top-right so no house/tree pixels get dragged in. Composited over v1. AI re-roll with clouds held in reserve (160 hf).

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- Higgsfield batches: gen_runner.py run appends here. Magnific/MCP or web spends: gen_runner.py log JOB.md <amount> <hf|cr|aud> <note> -->
- 2026-10-20 | 160 hf | pool_cinemagraph seedance_2_5 (gen-runner)

---
_Vault: [[jarvis]]_
