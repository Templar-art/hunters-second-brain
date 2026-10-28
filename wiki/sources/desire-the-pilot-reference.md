---
type: source
tags: [reference, sound-design, editing, transitions, real-estate, kollosche, competitor]
updated: 2026-10-28
---

# Desire Media: "THE PILOT, 17 Pilot Court, Mermaid Waters (First Look)"

A reference film Hunter supplied on 28 Oct 2026 as the style to learn from for [[auto-sound-design]]. It was shot by Desire Media for **Kollosche** (the agents on the end card are Taylor Kleinberg and Paul Harrison). It runs 110 s at 1280×720, 25 fps. The file was uploaded by phone and is kept locally as `projects/auto-sound-design/input/Desire - The Pilot 17 Pilot Ct (reference).mp4`, git-ignored and not in the repo.

Method: Claude looked at one frame per shot (65 shots) plus 8-frame strips across 16 key cuts. The audio was analysed per cut for whoosh signatures (high-frequency noise rising into the cut), boom signatures (a one-off sub-bass spike) and noise texture per shot. That analysis is signal-level, and its findings are labelled below as measured or as read from frames.

## Structure
- **0–5.5 s, logo-led open:** the Kollosche wordmark stays fixed centre-frame while four shots change underneath it (palms and facade, house, shadow on paving, a curtain-light abstract). The logo is the constant and the shots are the rhythm.
- **5.5–12 s, lifestyle at golden hour:** a woman in a robe at the window, then on the balcony, then a sunset over the water. The address super is small, over the lifestyle shot.
- **12–14.7 s, title card:** "The Pilot / 17" in script on marble, then the same title over palms.
- **14.7 s:** a dusk hero of the facade with all the lights on.
- **Interiors (22–38 s):** kitchen and living, with talent (a woman on the sofa with wine).
- **Lifestyle beats are spread throughout:** pool swim, treadmill and gym, spa, rooftop drinks, golf putting green. Each amenity is shown *in use*, not empty.
- **Close:** a dusk aerial, then the agent end card over a dark aerial.
- **Pace:** 64 cuts in 110 s, so a cut roughly every 1.7 s, faster through the amenities.

## Transitions worth stealing
| Time | Transition | How it reads |
|---|---|---|
| 0–5.5 s | Logo held over changing shots | Brand as the anchor; the cuts feel deliberate |
| 21.0 s | Whip into a dark ceiling spin, out onto pendant lights | Motion blur carries the cut |
| 22.1 s | **Lights switch on** in the dark kitchen | A reveal inside the shot, with a sound on it |
| 39.3 s | Whip pan from the pool to an aerial | Smear frames hide the cut |
| 41.6 s | Fast drone push matched to a ground move | Continuous motion across locations |
| 68.5 s | Blur whip from a timber detail into the next room | Same trick indoors |
| 79.2 s | **Foreground pillar wipe**, dusk aerial to interior | The camera passes an object that wipes the frame |
| 89.4 s | Aerial to a **top-down spiral staircase** | Shape/rotation match |
| 53.3 s | Spa bubbles to talent in the spa | Texture match, on the music drop |

## Sound design (measured)
- **Whooshes are sparse: about 8–13 of 64 cuts (12–20%)**, concentrated on motion (whips, fast moves) and reveals (the lights-on kitchen at 22.1 s had the strongest whoosh signature). Most cuts carry **no** effect; the music does the work.
- **Big low hits: about 2–5 in 110 s.** The clearest are a one-off sub spike at 14.7 s (the dusk hero after the title) and a sub event at 53.3 s (the spa, on the music drop).
- **Ambience:** exterior shots carry slightly more broadband noise texture under the music than interiors (about +1 to +2 dB against −2 to −4 dB, relative to the median shot). That suggests light location ambience outside and clean interiors. This is weak evidence; nobody has listened to it.
- Tempo is about 118 BPM, steady. Cuts mostly land on the grid.

## Mastering (measured 28 Oct)
- **-16.2 LUFS integrated, loudness range 5.4 LU**: a tight, glued mix. The 3 s RMS moves only about 5 dB across the film.
- For comparison, Kollosche Esther Pl (10x) is -15.7 LUFS with LRA 8.0, so it swings about twice as much. Matching the consistency matters more than adding effects.

## What changed in the tool because of it
- `presets/tasteful.json`: whooshes capped at about 22% of cuts, and they now favour **motion blur across the cut** (new `cut_motion` detector), as Desire does. On Desire itself the detector picked out the 39.3, 68.5, 79.2 and 89.4 s whips and the 22.1 s reveal.
- A new **existing-effects detector** (`existing_sfx`) finds whooshes and booms already baked into an edit so the tool doesn't double them. On Hunter's Kollosche Esther Pl edit it found 6 likely whooshes (16.7, 24.2, 42.2, 43.2, 57.4, 58.4 s) that the earlier passes had been doubling.

## Creative ideas for 10x edits (not tool features)
- Use talent for lifestyle in every amenity (swim, gym, golf, wine). It's the biggest difference from a plain walkthrough.
- Shoot a **lights-off to lights-on** reveal of the kitchen at dusk. It's cheap and very effective.
- Plan **foreground wipes** (a pillar or doorframe) on gimbal moves to join exterior and interior.
- Hold the **logo static** over the opening montage instead of animating it.
- Use a top-down of any spiral or feature stair as a geometric beat.

Related: [[auto-sound-design]] · [[kollosche]] · [[sfx-sourcing-and-design]] · [[video-edit-pipeline]]
