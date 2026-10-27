---
client: kollosche
address: 5 Esther (Villas on Esther townhouses, street TBC)
opened: 2026-10-27
status: intake        # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 0, aud: 0 }   # derived from ## Ledger — never edit by hand
---

# Job — Kollosche day-to-night clips, Villas on Esther

Source: `~/Downloads/Kollosche Day to Night/1–4.mp4`. All are 3840×2160 H.264 bt709 at 23.976 fps, between 1.46 and 3.46 s long. Target look: [[house-twilight]]. For the interiors, use the relight-from-fittings method learned on [[extra-salt-pottsville-dusk]]. Prompts: [prompts.md](prompts.md).

This is a different property from the Pottsville reel. Clip 1 was checked frame-by-frame against the Pottsville source, and they are not the same shot.

## Shots

| # | Shot | Len | Pipeline | Status | Notes |
|---|------|-----|----------|--------|-------|
| 1 | Living/dining dolly → corner balcony doors | 3.46 s | video (Seedance 2.5, still-as-reference) | done | Hunter: worked |
| 2 | Covered balcony, interior visible through slider | 1.96 s | video (Seedance 2.5) | todo | pad to 4 s |
| 3 | Close through glass: sofa cushions → balcony chairs, palms | 2.00 s | video (Seedance 2.5) | todo | pad to 4 s; no sky and no visible fitting, so it's the weakest |
| 4 | Street front, "VILLAS ON ESTHER" sign wall, push-in | 1.46 s | video (Seedance 2.5) | todo | pad to 4 s; signage lettering at risk |

## Log

- 2026-10-27 intake: 4 clips triaged. Prompts written. Nothing has been spent yet. Waiting on Hunter's go-ahead and a decision on resolution.
- 2026-10-27 Hunter is running it himself: night still per first frame, then that still as the video reference. Credits are on his own account, so no ledger lines from us. Clip 2 still approved ("this one is great"). Clip 4 still: Hunter liked the look but wants it darker. Two problems: the sign misspells the name as "ONTSTHER", and the 5 glows gold. The source frame shows flat black standoff letters with no visible halo LED, so they stay unlit and a darker re-roll was given. Plan: comp the source sign wall back in during post.
- 2026-10-27 Clip 4 darker still approved ("looks great"), using the master prompt with the sign unlit. Built 4K padded 4.2 s copies of all 4 clips in `~/Downloads/Kollosche Day to Night/padded-4s/` for the video step. Trim back to the source lengths afterwards: 3.46 / 1.96 / 2.00 / 1.46 s.
- 2026-10-27 Clip 1 video worked (Hunter). The interior target is the clip 2 look, and the deep-blue-hour "moody/amber" still failed with an orange cast and added lanterns. Clip 3 changed frame because it was under 4 s, so it's being re-run on the 4.3 s padded copy. New standing rule: clips must be at least 4 s.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- Higgsfield batches: gen_runner.py run appends here. Magnific/MCP or web spends: gen_runner.py log JOB.md <amount> <hf|cr|aud> <note> -->

---
_Vault: [[jarvis]] · Client: [[kollosche]]_
