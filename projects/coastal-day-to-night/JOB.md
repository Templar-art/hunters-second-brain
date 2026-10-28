---
client: coastal
address: TBC (balcony and bedroom, jacaranda outlook)
opened: 2026-10-28
status: review        # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 30, aud: 0 }   # derived from ## Ledger
---

# Job — Coastal balcony day-to-night

Source: `~/Downloads/Kollosche Ester Place/Coastal Day to Night/Day.mp4`. It is 3840×2160 at 23.976 fps and **3.09 s long, which is under the 4 s minimum** ([[house-twilight]]), so it needs a longer export of about 4.5 s. The look reference is `Main.mp4` in the same folder. It is the same shot already at dusk, 1280×720 and 3.17 s. The frame I pulled from it, `Reference-dusk-frame.jpg`, is Image 1 for the still pass.

**Target look (from the reference):** early dusk with a soft pastel sky, peach and lavender light catching the clouds, and a warm glow at the horizon. The foliage stays green and readable, and the jacarandas stay vivid purple. Inside, the bedside lamps and the ceiling fan light glow warm amber. The balcony is lit evenly with no sun patches, and the dark timber ceiling stays dark. Nothing is added.

## Shots

| # | Shot | Len | Pipeline | Status | Notes |
|---|------|-----|----------|--------|-------|
| 1 | Balcony slide, bedroom behind the glass | 3.09 s | still (NB 2.1), then video (Omni Edit 4K, with the still as reference) | review | padded to 4.2 s, trimmed back to 3.09 s |

## Log

- 2026-10-28 intake: 1 shot. The reference is the same shot already at dusk. Nothing has been spent.
- 2026-10-28 Hunter said go (~30 HF), pad to 4 s. Still v1 matched the look but took its framing from the reference at 1.5 s, which is mid-move. Re-pulled the reference from frame 0 to get v2, which lines up with Day. Omni Edit 4K: motion edge-match against the source holds at 75–78% across the clip. The lamps and fan light are warm, the sun patches are gone and the jacarandas are still purple. The sky came out as a clean pink-peach gradient with fewer clouds than the reference. Delivered `Coastal Balcony - DUSK 4K` as .mov and .mp4 next to the source, trimmed to 3.09 s. Lesson: when the reference is the same shot, pull it from the frame that matches the source's first frame.
- 2026-10-28 Hunter rejected it: wrong sky, the door is messed up, and the movement isn't the same. Diagnosis:
  - **Door:** in the dusk clip, the white hinged bedroom door with its silver lever has turned into a mirror or glass panel, and the lever has become a black wall sconce.
  - **Right window:** a sheer curtain has been added over the trees.
  - **Root cause:** Night-still-v2 was **not aligned to Day frame 0**. Its framing is shifted toward the reference, and it had already dropped the door. Omni blended the still's geometry into the plate. Lesson: before spending on video, check the still against the day frame with phase correlation.
  - **Sky:** the still has a clear pink gradient. The reference has peach-lit cumulus.
  - **Motion:** optical flow matches Day.mp4 (dx about −0.3, dy about +0.27 px per 0.25 s in both). Main.mp4 is a different take with a different move.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- Higgsfield batches: gen_runner.py run appends here. Magnific/MCP or web spends: gen_runner.py log JOB.md <amount> <hf|cr|aud> <note> -->
- 2026-10-28 | 6 hf | Nano Banana 2.1 4K night still x2 (v1 took the reference's mid-move framing; v2 used reference frame 0)
- 2026-10-28 | 24 hf | Kling 3.0 Omni Edit 4K, padded 4.2 s clip with still v2 as reference

---
_Vault: [[jarvis]] · Same workflow as [[kollosche-day-to-night]]_
