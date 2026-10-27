---
type: source
tags: [kollosche, brand, video, captions, guidelines]
updated: 2026-10-26
---

# Kollosche — Video and Caption Guidelines (2024) + asset pack

Kollosche's own brand rules for every video made for their social channels. The 12-page InDesign PDF is dated Sep–Nov 2024. It came with the asset pack Hunter downloaded on 2026-10-26, which is filed at `raw/kollosche/`. Client page: [[kollosche]].

- PDF: [Video and Caption Guidelines 2024](../../raw/kollosche/guidelines/Video%20and%20Caption%20Guidelines%202024%20(2)%20(2).pdf). This is the newer copy, with per-page dates and the Nov 2024 Auction and Agent Focus pages. The older `Video and Caption Guidelines.pdf` beside it has the same rules.
- Design contact for logo approvals: design@kollosche.com.au

## Content types
- **VPA (Vendor Paid Advertising):** property listing videos.
- **PAS (Paid Agent Strategy):** agent-led content and series (e.g. "The Conversation").
- **Corporate / Podcast:** brand content.
- **Agent Focus:** agent-specific promos. This is the only type allowed to open on a team logo.
- **Auction campaigns:** these open on an AUCTION overlay instead of the K.

## Universal rules
- **The "K" opens every vertical video.** It is there from frame 1 with no fade-in, centred, for 2–4 s. A fade-out is preferred, and a hard cut is fine if the edit needs it. **The K never appears at the end.** Use only the approved overlay (`overlays/` and `brand-logos/K-icon-1080-x-1920.png`).
- **4K landscape (YouTube):** the full KOLLOSCHE wordmark replaces the K, with the same rules (frame 1, centred, 2–4 s, never at the end). YouTube adds its own watermark, so there is no logo on the outro either.
- **16:9 logo placement (measured 2026-10-27):** in `Kollosche-3840-x-2160.png` the wordmark has **no ™**, is 700×133 px (≈18% of frame width) and is dead centre (centre 1920, 1080). The 4K example matches. In Final Cut, put the full-frame PNG on the timeline at scale 100% and position 0, 0. Spatial Conform *Fit* scales it to a 1080p timeline, so don't resize it by hand.
- **16:9 address super (measured from the 4K example, 2026-10-27):** cap height 47 px on 3840×2160 (≈2.2% of frame height), which is ≈65 px font size. Tracking ≈8% (≈80/1000 em). Line pitch 78 px (≈1.2 em, i.e. default leading). The block is centred on the frame. Line 1 ("56B WOODROFFE AVENUE") is ≈29% of frame width.
- **Font:** Söhne Breit **Kräftig** (Klim Type Foundry). It is used for all supers: **40 pt on 9:16** and **75 pt on 4K**. The agent and address supers use the same font and size.
- **Intro order:** K → agent mention → address (VPA), or K → agent → subject/series title (PAS). The agent and address can swap order. Each super appears on a frame switch or fades in. The agent super runs 2–3 s and the address or title 3–4 s, then fades out or hard-cuts.
- Supers are **ALL CAPS**, centred, and white. Two-line addresses go street on line 1 and suburb on line 2 (e.g. "18 TANJA COURT / TALLAI").

## Outro (agent details)
- Fade from the original colour to the **blue overlay**. The overlay and the agent details **fade in together**.
- **No logo or K on the outro.**
- The agent details are centred: NAME on one line and the phone number below it. Put **2 line breaks** between agents when there are several.
- The 9:16 text zone is y ≈ 535.8–885.7 px. The outro length is up to the editor.
- Blue overlay = `#0B152C` at 50% opacity (sampled from `Blue_overlay_*.png`).

**Outro generator (2026-10-27):** `projects/kollosche-outro/make_outro.py "NAME|0400 000 000" …` renders the outro for any agents as 16:9 + 9:16 ProRes 4444 alpha plus PNG. The layout is measured from the Taylor × Thibault cards: 16:9 is cap 110 px on 8000 wide (≈75 pt at 4K), line pitch 1.03 em, and one agent block step = 3 line pitches (two blank lines). The copyright line is copied from the card, and the reel card has none. The cards are **kerned with zero tracking**: Pillow here has no kerning, so the script uses HarfBuzz from `~/.venvs/typeset`. `--check` rebuilds the reference card (0.2 % of pixels differ). ⚠️ Taylor Kleinberg's number is 0446 466 177 on the end-card files but 0447 466 177 in the guidelines PDF and a live video.

## Agent Focus (agent promos only, never VPA)
- Open on the **approved team logo**, already on screen with no fade-in, for 2–4 s. Then the series or subject super for 2–3 s. Outro on the approved Kollosche logo with the blue overlay. Don't repeat the agent details at the end.

## Auction campaigns
- **No K or Kollosche logo at the open.** The AUCTION overlay (`overlays/auction.png`) is there from frame 1 with no fade.
- Team details go on **one line only** (e.g. "TAYLOR KLEINBERG TEAM") as live text. **No team logo.** The team and address supers are the same size.
- The outro is the same as a normal VPA outro.

## Subtitles (reels)
- Söhne Breit Kräftig, **40 pt, 30 tracking**, centred, white `#FFFFFF`.
- **Max 17 characters (2–3 words), one line only, never break a word.**
- Remove full stops and commas. Keep question marks.
- **No drop shadows, outlines, other fonts or embellishments.**
- Position: zone centred, at 0 and 360. Keep clear of the native app UI (likes, share).

## ⚠️ Four caption specs in the pack disagree
| Source | Weight / size | Tracking | Box | Other |
|---|---|---|---|---|
| Guidelines PDF (Sep 2024) | Kräftig 40 | 30 | none | 17 chars, one line, no punctuation |
| `examples/02. Captions_Kraftig_45pt.mp4` | Kräftig 45 | — | none | 1–3 lowercase words, lower-middle of frame |
| `guidelines/Premier subtitles-caption settings.png` | **Leicht** 48 | 30 | **navy box, 85%, 30 pad** | position 0, 1152; keeps the comma |
| `guidelines/SOP _ Kollosche style subtitles for reels.pdf` (Final Cut, made 20 Oct 2026) | Kräftig 67 (FCP scale) | 0 | none | fade in word by word, Y offset 282.31 |

The PDF and the example video agree on Kräftig with no box, and the example (45 pt) is the most recent real Kollosche output in the pack. Default to that. The Premiere screenshot's box style contradicts the "no embellishments" rule, so check with Kollosche before using it. The FCP SOP was a headless-Chrome export, most likely 10x-made, and FCP point sizes don't map 1:1 to Premiere's.

## Asset pack inventory (`raw/kollosche/`)
| Folder | Contents |
|---|---|
| `guidelines/` | 2× guidelines PDF, the Final Cut caption SOP, the Premiere caption settings screenshot, `Disclaimer 2026.docx` (© Kollosche Sales Pty Ltd 2026 copyright line, the small print on 4K outros) |
| `brand-logos/` | K icon + KOLLOSCHE wordmark overlays (1080×1920, 3840×2160, transparent PNG); `wordmark/Kollosche-wordmark-{navy,black,white}.png` (2411 px, transparent, extracted 2026-10-27 from the Hayley Kidson lockup, the largest clean copy in the pack). ⚠️ No vector of the plain wordmark came in the pack. The `svg_Kollosche …` files were actually **Kara Christensen team logos** with misleading names, and they were moved to her folder |
| `overlays/` | Blue overlay 9:16 + 4K (50% navy), AUCTION overlay 9:16 |
| `templates-psd/` | `Agent-Outro`, `Agent-Property-Intro` (K + AUCTION + address + team), `Agent-Title` (name + title lower-third), `Monthly-wrap-INTRO` (KOLLOSCHE + month), `Blue_overlay_4K`, `Kollosche_YouTube-video_overlays_GROUPED` (4K K + address). Local only, not in git |
| `fonts/sohne-breit/` | Söhne Breit: Extraleicht, Leicht, Buch, Kräftig, Halbfett, Dreiviertelfett, Extrafett (licensed, local only; installed to `~/Library/Fonts` 2026-10-26) |
| `examples/` | `01. Intro_and_Outro` (9:16, 28 s), `02. Captions_Kraftig_45pt` (9:16, 63 s, Infinity 33 agent piece), `03. 4K Landscape example` (3840×2160, 24 s, 55B Woodroffe Ave Main Beach) |
| `end-cards/` | Taylor Kleinberg × Thibault Parolini end cards (9:16 + 16:9) |
| `team-logos/<Agent>/` | 32 agent/team logo sets (below) |
| `_duplicates/` | byte-identical re-downloads (local only) |

### Team logo naming
Each agent has `_TeamLogo.eps` (master) plus `_Kollosche Black_01/02`, `_Kollosche Blue_01/02` and `_White_01/02` in EPS + SVG. **01 = stacked, 02 = single line.** Kollosche Blue `#011A3B`, Kollosche Black `#282829`.

Teams: Andrew Ramsey, Brad Coyne, Bright Ward, Danny Stanley, Debora Sutton, Duncan Longmore, Duncan McInnes, Eddie Wardale, Eoghan Murphy, Gareth Denning, Harry Kakavas, Hayley Kidson, Jamie Harrison, John & Nicole Mayer, Jonathon Patton, Josh Finch, Kara Christensen, Ledgerwood, MK, Marco De Vincentiis, Markovitch Team, Nicky & Jason Cunningham, Paul Harrison, Rob Lamb, Sam & Julia, Stuart Rooke, Taylor Kleinberg, Team Grbcic (plus the Grbcic Duo podcast logo and "powered by Kollosche Commercial"), Tony Velissariou, Troy Dowker, William Sarti.
