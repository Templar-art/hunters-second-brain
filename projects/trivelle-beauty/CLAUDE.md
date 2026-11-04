# CLAUDE.md — Trivelle Beauty

Read this before any Trivelle work. It replaces the original build chat (2026-11-04). The wiki summary is [[trivelle-beauty]] at `wiki/projects/trivelle-beauty.md`.

## What it is
Hunter's own Shopify dropshipping store, **trivellebeauty.com**, separate from 10x Visuals client work. The store runs on Hunter's other laptop, under a custom Gmail owner account; Claude can't reach the Shopify admin from here.

- **Product:** Trivelle 4-in-1 Sculpt & Glow, a cordless handheld device with four modes: Warm (gentle heat), Glow (red light), Lift (EMS micro-pulses) and Smooth (vacuum massage). It comes with an **80 g microcurrent gel**.
- **Price:** **A$219** for the kit, **A$389** for the Gift 2-Pack ("Save $49 vs buying two"). No fake compare-at or "was" prices. Never write "under $1 a session"; "about a dollar a session" is fine.
- **Supplier:** ships blind (no supplier branding) direct to customers, with tracking, and replaces defective units. Landed cost is about A$45. Processing is within 24 h on weekdays, then 1–3 days to the warehouse, then 7–15 days in transit.
  - Store wording: **"Ships within 1–4 business days, then 7–15 business days delivery."**
  - **Open questions for the supplier:** does the gel fit in the stock box (one tracking number or two)? How do returns work: an AU return address, or refund and the customer keeps it?
- **Packaging:** the supplier's plain stock box. The custom box is shelved: the draft in `packaging/` and `scripts/box_dieline.py` is too bland, and the run would cost about A$900–1,000 for 500.
- **Brand:**
  - Logo: italic serif "trivelle" with a red glowing dot, in `brand/logo-on-light.png` and `logo-on-dark.png`.
  - Colours: green #1D2A26 (29,42,38), sage (225,232,229), lime #C4CE26 (196,206,38).
  - Fonts: Anton (headlines) and Montserrat (body), in `fonts/`.

## Where everything lives
- **Google Drive** (`My Drive/Trivelle/`) is synced at `~/Library/CloudStorage/GoogleDrive-hunter@10xvisuals.com.au/My Drive/Trivelle/`. Hunter works from Drive, so **copy every new deliverable or doc there**.
  - `0 TONIGHT - START HERE.md` (same file as `TONIGHT.md` here): ordered launch steps.
  - `LAUNCH-CHECKLIST.md`, `STORE-COPY.md`, `MESSAGES.md`, `ADS-IDEAS.md`, `INSTAGRAM-SETUP.md`.
  - `Trivelle-Launch-Pack.zip` (graphics, stills, A–D ads), `Trivelle-Facebook-Posts.zip`, `profile-picture.jpg`, `cover-photo.jpg`.
  - `New ads/`: E–I ads, plus the `15s/` and `reels/` folders.
- **Local copies:** `~/Desktop/Trivelle-Launch-Pack` and `~/Downloads/Trivelle-Facebook-Posts`.
- **Repo** (`projects/trivelle-beauty/`):
  - `device-v2/graphics/`: 01-kit-hero, 02-four-rituals, 03-how-to-use, 04-gel, 05-where-to-use, 06-comparison, 07-in-the-box (plain white box, which matches what ships), 08-guarantee, profile and cover images. Built by `scripts/graphics_v3.py`.
  - `device-v2/stills/`: product and lifestyle stills.
  - `device-v2/broll/`: Kling device-on-skin clips.
  - `device-v2/vo/`: voiceovers.
  - `device-v2/ads/`: every ad (mp4s are gitignored, so Drive is the backup).
  - Never use `videos/ads/`: those show the old 3-in-1 device.

## Ads inventory (`device-v2/ads/`)
| Ad | What | Lengths |
|---|---|---|
| A salon | AI UGC presenter hook + B-roll, salon-cost angle | 62 s, 30 s, 15 s, 10 s hook |
| B lived-a-little | body-confidence angle (some rejection risk on Meta) | 46 s, 30 s, 15 s |
| C drawer | "devices end up in the drawer" angle | 52 s, 30 s, 15 s |
| D seated explainer | presenter explains the 4 modes | 34 s, 30 s, 15 s |
| E animated | flat illustrated, mode labels | 25 s, 15 s, reel |
| F review-reply | D with a "YOU ASKED" comment bubble | 34 s, 30 s, 15 s |
| G animated 3D | original 3D animated-film character; the "motion" version is fully animated (Kling) | 27 s, 15 s, reel |
| H girls' night | 3D, two friends; ends on a voiced "Okay… send me the link!" payoff | 23 s, reel |
| I podcast | realistic podcast host (Seedance) + 2 device cutaways | 19 s, reel |

Builders in `scripts/`:
- `build_ads_v2.py` (A–D, F) holds the shared helpers: words, chunks, caption_track, build, norm, end_card. Other scripts load them with `exec(src[:src.index("B = lambda")])`.
- Scripts that take arguments are run as `python3 <script> <asr_dir> <work_dir>`.
- Captions come from `whisper-cli -m ~/.cache/whisper/ggml-large-v3.bin -ml 1 -sow -oj`.
- One builder per ad: `build_anim_ad.py` (E), `build_anim3d_motion_ad.py` (G), `build_friends_ad.py` (H), `build_podcast_ad.py` (I).
- `make_short_cuts.py` makes the 15 s cuts and the reels.
- This machine's ffmpeg has no drawtext, so render text with PIL and overlay it.

## Launch plan
- **Meta:**
  - Meta Business portfolio "Trivelle", ad account "Trivelle Ads" (AUD, Brisbane).
  - One Sales campaign with **one ad set**: Australia, women 35–65, **$20/day**, Advantage+.
  - **4 ads, one per format:** D seated 30 s, A salon 30 s, G fully animated 3D, H girls' night. Tick the "AI-generated" label on every ad. Ad copy is in LAUNCH-CHECKLIST section 6.
  - Don't touch it for 3 days. From day 3, turn off any ad that has spent about $40 with no add-to-carts.
  - **Day 5:** Hunter sends a screenshot, then round 2 runs with the backups (I podcast, F, E, B) and new formats.
  - Keep testing new formats all the time; Hunter sees the ads as the main risk.
- **Shopify:** install the Facebook & Instagram app and the TikTok pixel, then a test order to check the Purchase event, then refund it. Turn on Afterpay. Markets: Australia only.
- **Instagram:** being set up as a Business account linked to the Page. Post the 9 posts in `INSTAGRAM-SETUP.md` before the ads go live, and run the ads under the IG identity.

## Hard rules
- **Credits:**
  - Magnific is gated: any Magnific tool (even an upload or trash) needs Hunter's latest message to start with yes/go/approved.
  - Always `simulate_cost` first and quote the exact number.
  - Known costs:
    - nano-banana 2k still: 65.
    - Kling `kling-25`, 5 s, 720p: 140.
    - Seedance `bytedance-seedance-pro-2.5`, 15 s, 720p: 6,600.
    - ElevenLabs v4 short line: about 6–8.
  - Hunter mentioned **Wan** as a cheaper option for animated clips; price it against Kling and Seedance next time.
- **Compliance** (Meta and ACCC):
  - Cosmetic wording only (looks / feels).
  - No medical claims, no fat or cellulite claims, no stats.
  - No fake doctors or experts, no fake named reviewers or commenters.
  - No before/after body imagery. Hunter also rejected mood before/after tags: "doesn't make sense".
  - AI label on every ad and post.
  - Only show packaging the customer actually gets.
- **Characters:** original only, never Disney or any other existing IP.
- **Editing:**
  - No shot under about 3.5 s and no cuts that feel rushed.
  - Never two B-roll clips of the same body part back to back.
  - Animated zooms use a sub-pixel affine transform, never integer crops (those jitter).
  - Every spoken line needs audio; Kling clips are silent, so add VO.
- **Freepik/Magnific library:** after downloading, Hunter wants everything trashed (done 2026-11-04, 137 items). Never empty the trash; Hunter does that.
- Never enter payment details or credentials; Hunter does Shopify, Meta billing and logins himself.
- Commit and push freely.

## Known issues
- The AI presenters in A–D mispronounce "Trivelle" ("Trevolz"). The captions are correct. Re-roll once sales justify it.
- The kit hero graphic shows a green TRIVELLE box as styling; customers get the plain box (the in-the-box image is correct).
