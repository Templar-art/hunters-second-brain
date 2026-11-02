---
type: client
tags: [kollosche, real-estate, gold-coast, video, brand]
status: active
updated: 2026-11-02
---

# Kollosche

Prestige Gold Coast real-estate agency (Kollosche Pty Ltd / Kollosche Sales Pty Ltd). It runs agent "teams" under one brand, and also a commercial arm (Kollosche Commercial). Its listings are at the high end; the pack's examples are in Main Beach and Tallai. Brand: navy `#011A3B`, charcoal `#282829`, white, set in Söhne Breit. Logo approvals go to design@kollosche.com.au.

## Instagram handles (verified in-app by Hunter, 2026-10-26)
- Agency: **@kollosche_** (verified badge). ⚠️ Not @kollosche.com.au, which is only the email domain and was wrongly used in a draft caption.
- Taylor Kleinberg: **@taylorkleinberg_kollosche**
- Thibault Parolini: **@thibaultparolini_kollosche**
- Other agents usually follow the `firstnamelastname_kollosche` pattern, but verify each one in the app before tagging.

## Posted work
- **13 Mayra Court, Mermaid Waters** (Taylor Kleinberg + Thibault Parolini listing): main video captioned for @10xrealestate_ on 2026-10-26. The house has a script name sign on the facade (reads "Saraya", unconfirmed).

## The video rulebook
Kollosche has strict, written rules for every video on its channels. The full spec is at [[kollosche-video-guidelines]]. The short version:
- **The K opens every 9:16 video** (the full wordmark on 4K landscape). It is there from frame 1, centred, for 2–4 s, and **never at the end**.
- Supers in **Söhne Breit Kräftig, ALL CAPS, white, centred**: 40 pt on 9:16, 75 pt on 4K.
- **Outro:** fade to the 50% navy overlay with the agent name and number fading in together. **No logo on the outro.**
- **Auctions** open on the AUCTION overlay instead of the K, with the team name on one line and no team logo.
- **Team logos** appear only on Agent Focus promos, never on listing (VPA) videos.
- **Captions:** one line, 2–3 words (≤17 characters), no full stops or commas, no shadow or outline. The specs in the pack conflict, so read the ⚠️ table on the source page before captioning.

## Assets
The full pack is in `raw/kollosche/`. It holds the guidelines, overlays, PSD templates, Söhne Breit fonts, three example edits and logo sets for 32 agent teams. The inventory is on [[kollosche-video-guidelines]]. The EPS/PSD/font masters are kept local and are not in git.

**Font:** all 7 Söhne Breit weights were installed to `~/Library/Fonts` on 2026-10-26 (from `raw/kollosche/fonts/sohne-breit/`). Restart Premiere or Final Cut if either was open at the time.

## Work for and around Kollosche
- **Townhouse drone graphics** (2026-10-27, outline, pin and Eddie Wardale outro delivered, $0). The top-down `Main` gets a tracked white lot outline. The wide `View` gets the K pin locked to the townhouse roof. The plate-vfx solver failed on the blurred spin-in top-down, so it was tracked with chained homographies instead (SIFT, ≤0.2 px once settled). [JOB.md](../../projects/kollosche-drone-graphics/JOB.md)
- **K location pin** (2026-10-27): the K from the wordmark over a thin white line down to the house, matching a reference Hunter sent. [projects/kollosche-pin/](../../projects/kollosche-pin/make_pin.py) renders 1080×1920 transparent PNGs and 5 s ProRes 4444 alpha movies (the line draws up over 0.5 s, then the K fades in), in long and short lengths. ⚠️ A mid-video K bends the "K only at the open" rule, so confirm with Kollosche before using it on their channels.
  - **Boxed badge version (2026-10-28), the correct one:** Hunter wants the pin head to be "the one in the box that we do for the photos", meaning the navy square K badge used on the drone stills. Both `kollosche-drone-graphics/scripts/render_pin.py … badge` (the tracked View clip) and `kollosche-pin/make_pin.py . out badge` (the generic 9:16 overlay) now draw it with drone-pin's own `badge()` and `clients/kollosche.json`, so it is pixel-identical to the photos. The outputs carry a `_badge`/`-badge` suffix.
  - **Navy-K version (2026-10-28, ⚠️ wrong logo per Hunter, kept for history):** `make_pin.py . out navy` takes the K from the official navy wordmark (`raw/kollosche/brand-logos/wordmark/Kollosche-wordmark-navy.png`, #011A3B), which is the only blue Kollosche logo on file; nothing was recoloured. The line stays white. The outputs are `kollosche-pin-{long,short}-navy.{png,mov}`. The navy K reads well against sky but gets lost over dark trees or buildings, so place it with sky behind it.
- [[extra-salt-kollosche-birds]]: CG gulls comped into a Pottsville drone wide from the Kollosche reel (Oct 2026). That plate became the [[plate-vfx]] benchmark.
- 18 Maryland: the house and site were rebuilt in Blender from the Kollosche floor plan (`raw/18-maryland/floorplan-kollosche*.png`).
- `~/Downloads/Kollosche BTS REEL FINAL.mp4` (1 Sep 2026) is a BTS reel. It was left in Downloads and is not part of the brand pack.
- Custom transition SFX: `~/Desktop/Ocular Sounds/kollosche_transition_SFX.wav` ([[sfx-custom]]).

- **Competitor reference:** Desire Media shot "The Pilot" (17 Pilot Ct, Mermaid Waters) for Kollosche. It's broken down in [[desire-the-pilot-reference]] and is Hunter's target style for sound design. The 5 Esther Pl edit is the [[auto-sound-design]] test case.

- **4-6 Buckingham Way, Elanora — FCP overlay pack** (2026-11-02, Taylor Kleinberg listing, $0, in review). Hunter's finished 63 s 1080p edit got the KOLLOSCHE wordmark + address super opener, a white tracked lot outline on the top-down, one K badge pin on the view wide, and Taylor's outro, plus an SFX pass ([[auto-sound-design]]: beds + whooshes synced to the graphics, the Kollosche transition sound on the opener and outro). ⚠️ v1 also had a second pin on the final pull-out and plate-vfx gulls. Hunter cut both ("end pin is unnecessary", "birds are shit"). Hunter asked for **overlays he lays in FCP**, not a finished comp, so the output is 4 full-length ProRes 4444 alpha files (all start at 00:00, frame-matched to `Main.mp4`) plus a preview MP4. They're in `Edits/Kollosche Overlays/` beside the original on SSD1. Lessons:
  - Hunter's drone moves are often **speed-ramped whips**. The plate-vfx solve fails across the whip, so split the shot: graphics on the sharp section before or after it (KLT/SIFT homography), and birds on the settled tail.
  - **Lot outlines come from Hunter's delivered pinned stills**, never by eye. v1's eyeballed block was wrong. The real lot (QLD cadastre 130RP206900, 4,799 m², ~40 × 120 m) is the strip on his `Drone Graphics/Web-02`, which is SIFT-registered onto the video top-down. Cadastre lookup: QLD `LandParcelPropertyFramework` MapServer, layer 0 (address → lotplan), layer 4 (parcel polygon).
  - One K pin per video is enough.
  - On a wide over hinterland the solve stalls at ~1.2 px (hillside parallax).
  - A white address super can wash out over white eaves, and Kollosche bans shadows, so place it over darker footage.
  - [JOB.md](../../projects/kollosche-buckingham-way/JOB.md)

## Agents seen in the pack
Taylor Kleinberg (**0447 466 177**, confirmed from his agent profile 2026-11-02) and Thibault Parolini (end cards), Duncan Longmore, Michael Kollosche and Marco De Vincentiis (4K example outro), Gareth Denning, and Hayley Kidson ("The Conversation" PAS series). There are 32 team logo sets in all. The list is on the source page.

- **Buckingham Way fixes (2026-11-02):** wordmark → address is a **hard cut, no transition, and they're separate layers** (Hunter). The outro carries both listing agents: Taylor Kleinberg + Thibault Parolini (0401 023 142).
- **4-6 Buckingham Way reel** (2026-11-02, $0, in review): same overlay-pack approach at 9:16 — K icon opener, one K pin tracked on the coast wide (⚠️ outline under it cut: "for the pin didnt need the outline" — pin shots get the pin alone), sky gulls, Taylor outro, SFX. In `Edits/Kollosche Overlays - Reel/` on SSD1. See [projects/kollosche-buckingham-way](../../projects/kollosche-buckingham-way/JOB.md).

- **Reels (Day to Night townhouse, opened 2026-10-27):** a flythrough and a cinematic reel, 9:16. The kit (K opener + Eddie Wardale outro) is in [projects/kollosche-reels](../../projects/kollosche-reels/JOB.md).

- **Drone stills pin/outline:** [[drone-photo-pin]] (built 2026-10-27, for the townhouse stills).
- **Drone stills deliverable (2026-10-27):** both the web and print versions get the K badge pin and the lot outline. ⚠️ Corrected the same day; an earlier note said prints are clean, which was wrong. See [[drone-photo-pin]].
- **No top-down drone stills (2026-10-27):** Kollosche doesn't like straight-down shots, so Hunter dropped the Esther Pl top-down (Drones-4) from the delivery. Keep shooting them because other agencies use them, but leave them out of Kollosche deliveries.
