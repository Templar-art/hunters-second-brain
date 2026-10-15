# JOB: Committed Coaching (Jackson Farrier): "Don't work with me if…" Reel

- **Client:** Jackson Farrier, Committed Coaching (@jacksonfarrier, committedcoaching.scos-app.com). Online coach for male business owners.
- **Brief (Hunter, 10 Oct 2026):** turn 7 raw iPhone takes into one video. A pilot for the "talking-head motion graphics for coaches" offer.
- **Status:** v4 built 10 Oct 2026: v3 picture plus a Lyria 3 music bed (80cr, approved) and Ocular Sounds SFX (the new sfx-lib). -16.1 LUFS. Boss PASS on the v3 picture.
- **Cost:** 80 credits (Lyria 3 music, 10 Oct 2026). The rest was a local render.

## Build
- Template copied from `projects/use-definitions` and rebranded: black #0A0A0A, red #E02020, Inter, cracked COMMITTED wordmark logo.
- The 7 takes were trimmed to their last word and joined (31.4s), with jump cuts every take and alternate takes punched in.
- Beats: hook on a chest panel → 30-day shred rebound graph ✗ → dusty PDF ✗ → fibbed check-in ✗ → BUT business vs body KPIs → show up / follow plan / tell truth ticks → free video in bio CTA → black end card.
- Output: `episodes/not-your-guy/not-your-guy-v1.mp4` (34.8s, -15.6 LUFS).

## Premium cut (10 Oct 2026)
- Hunter: the pop-ups felt tacky for a coach and the reel "needs to feel premium". Built `episodes/not-your-guy-premium/not-your-guy-premium-v1.mp4` (33.7s, 50fps, -16.0 LUFS).
- System:
  - Inter for the voice, plus Instrument Serif italic for one key word per line.
  - Hand-set phrase captions, not word-by-word karaoke.
  - A scale widget on the whiteboard beside his head.
  - Three "verdict" lines with a red rule.
  - A black "But" type card.
  - The three steps as plain type.
  - One white CTA pill.
  - A 2s end card.
  - Soft Ocular SFX (soft, sub, ding kits). Same Lyria music bed at 0.18, faded for the shorter end.
- Rule learned: nothing sits on the COMMITTED shirt print, and type lives below it. The automated text check can't see printed text in the footage; the boss review caught it.
- Boss review: a fresh premium-brief reviewer, PASS on round 4 (4/4/5/4/4). Face and text checks clear (only the end dip to black).

## Premium v3: multi-reviewer polish (11 Oct 2026)
- Jackson liked the premium cut, and Hunter wants it perfected with more B-roll. Jackson films his own B-roll; Hunter picked that over stock at ~600cr per clip. `SHOTLIST.md` asks for 2 clips: D, one heavy rep on "to treat your body", and H, the hero shot of his forearm spotting a client on "I'll handle the rest". They drop in with `tools/broll.py`. Empty slots fall back to him on camera.
- The engine now supports B-roll: an `EP.broll` slot loads one frame per output frame.
- Reviewers, run in parallel and merged:
  - a premium creative director: 6 rounds, final PASS at 4/4/4/4/4
  - an Instagram retention strategist: hook 3→4, pacing 3→4
  - a typographer for pixel QA: 2 rounds
  - a numeric audio and loop-seam check
- Changes made:
  - the stock stand-in was dropped, since a stranger presented as his coaching misleads
  - B-roll cut from 8 slots to 2, keeping his on-camera finger count during the list
  - a PDF widget ("Opened: 0 times") that grows open on "forget"
  - the "FOR BUSINESS OWNERS" kicker and the hook subline both set from frame 0
  - no end card: it ends on the CTA and loops back into the hook
  - a punch-in on "check-ins"
  - curly apostrophes, optical centring, better contrast
- Output: `not-your-guy-premium-v3.mp4`, 31.76s, 50fps, −15.9 LUFS, −1.9 dBTP. Face and text checks fully clear. 0 credits.
- Open items for Hunter and Jackson:
  - the real title of the free video, to add a value line to the CTA
  - set the Instagram cover at about 2.0–2.5s
  - consider a "comment FIT" keyword DM in the caption
  - the scale and PDF numbers are illustrative

## Reel 2: "Brett and the guessing game" (15 Oct 2026)
- **Footage:** Jackson's OneDrive. 5 takes plus a brief image, and his whole B-roll library (54 files, 6.7 GB) in `footage/`, which is git-ignored. Downloaded through OneDrive's anonymous share API with Hunter's OK.
- **Clone format:** Jackson plays both Brett and the coach. `tools/clone.py` composites two locked-off takes into one frame:
  - feathered seam on the closet-door edge
  - per-take colour fit, plus per-frame exposure matching against the iPhone's auto-exposure ramps
  - 50fps JPG frames straight from the originals
  - the speaking take's audio
- **Missing lines:** two scripted lines were never filmed. They're carried as wall type: the hook plus an "IN HIS WORDS" quote card, and an "Open the app. Do it." beat.
- **B-roll:** the deadlift, the desk from behind, portions being weighed, and portions in containers, all chosen with no faces that could read as a third character.
- **Reviews:** the premium creative director (3 rounds, PASS), the retention strategist and the typographer. Their fixes:
  - exposure match
  - 4:5-safe hook in serif quotes
  - dead air out
  - centred 1.07 punch-ins
  - "CLIENT · RE-ENACTED" disclosure
  - captioned CTA
  - near-black end card
- **Output:** `episodes/brett-guessing-game/brett-guessing-game-v1.mp4`, 37.7s, 50fps, −16.0 LUFS. Face and text checks clear. 0 credits.
- **Delivered** to Hunter's personal Google Drive (`gdrive-personal:Committed Coaching/`, an rclone drive.file remote set up 15 Oct 2026).
- **Open items:**
  - confirm Brett is a real client who's OK being named and quoted
  - a real result for a proof line
  - consider a stronger CTA than "Follow for more"
