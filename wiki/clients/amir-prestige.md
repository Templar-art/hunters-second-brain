---
type: client
tags: [client, real-estate, agency, drone, pin, gold-coast, prestige]
status: prospect
updated: 2026-11-09
---

# Amir Prestige

**Who:** Amir Prestige Group is a prestige agency on the Gold Coast and in Northern NSW, run by principal **Amir Mian**. Head office is 2268 Gold Coast Highway, Mermaid Beach. Other offices are at Paradise Point (opened 2016), Bundall and Byron Bay. Domain lists roughly 180–200 sales a year. Their own material claims the Gold Coast beachfront record ($28 m, 41-45 Hedges Ave, Mermaid Beach); we haven't verified that. They publish a print magazine, *Residence* (on Issuu). Website: [amirprestige.com.au](https://www.amirprestige.com.au/), which runs on Reapit/Agentpoint WordPress. Instagram: `@amirprestigegroup`.

**Why we care:** Hunter asked for their guidelines on 2026-11-09 so we're ready to shoot for them. Which agent or listing comes first is still unconfirmed.

## Brand (gathered from their site, 2026-11-09; no official guideline PDF found)
- **Wordmark:** "amir prestige" in lowercase, in a high-contrast serif with a hand-cut swash through "am" and "ti". It comes in black and white only. Copies are in `raw/amir-prestige/` as 1000 px PNGs.
- **Monogram:** **"ap."**, the same serif with a diamond full stop. On their favicon it is white in a **deep teal circle, #24506A**. That teal is the only brand colour seen. The rest of the site is black, white and light greys (#F0F0F0, #1E1E1E).
- **Font:** the site sets **Garet** (Type Forward) for headings and body. It isn't installed here, so labels use Söhne Breit as a stand-in.
- **Tone:** prestige restraint, monochrome, photo-first.
- **Not yet in hand:** vector logos or a brand pack. Ask the agent for them before any print work, because the monogram we have was cut from a 512 px favicon.

## Drone style (from their own listing, 44 Via Roma, Isle of Capri, Nov 2026)
References are saved in `raw/amir-prestige/`.
- **Wide pin:** the **white "ap." monogram** sits on the sky, small (about 3% of frame height), with no circle or badge. Below it is a small gap, then a **thin white line** down to the house. There is no dot and **no lot outline**.
- **Location pins:** **white BOLD UPPERCASE** wide sans labels (SURFERS PARADISE, ROMA PARK, school and shopping names), placed to the right of the top of a thin white line. There is no dot and no distance.
- **Close top-down oblique:** no pin and no outline. The **neighbourhood goes black & white** and the lot and house stay in colour, the same treatment as [[zed]].

Profile: `projects/drone-pin/clients/amir-prestige.json`, **unconfirmed**. The mono surround is in the profile but `blackout` defaults to 0, so set the slider per photo on the top-downs only. A test render on a 21 Albany still matched their look. See [[drone-photo-pin]].

## Listing videos (from their YouTube channel, 2026-11-09)
All their listing films sit on one YouTube channel, [Amir Prestige](https://www.youtube.com/channel/UCKRDrsPL0UD32sasmnXmJxQ). Titles follow `Address, Suburb | Gold Coast Real Estate | Amir Prestige`, with "Northern Rivers Real Estate" for NSW listings. The 21 latest run **37–120 s**, mostly 60–90 s, in 16:9. The film for 44 Via Roma, Isle of Capri (Nov 2026, 60 s) was broken down frame by frame. Frames are in `raw/amir-prestige/video-refs/`.
- **Structure:**
  - Cold open on a styled interior, with the address super over a model walking through the shot.
  - A ~1 s burst of rapid cuts, about 3 frames each, landing on a bass drop at 2.3 s.
  - The tour runs on gimbal moves with plenty of tight texture details: travertine, tiles, linen, ceramics, pool water.
  - A short **agent cameo**: the agent in the kitchen around 10 s, possibly a line to camera.
  - A **framed montage** at 15 s and again at 52 s: the shots sit inset in a **light grey mat (about #E0E0E0)**, cutting about every 4 frames, with white flash frames between sections.
  - A second rapid burst at 43 s, then drones: a city wide, a top-down, and the **"ap." pin on a wide drone**, which is the same look as their stills.
  - It ends back on the opening kitchen shot with the agent names, then the end card.
- **Type:**
  - **Address super:** centred, one line, white, a geometric sans in Montserrat style. The street is Regular caps and the suburb is **Bold caps**, e.g. `44 VIA ROMA, ISLE OF CAPRI`. No box and no logo.
  - **Agent names:** white **serif in title case** (Playfair or Garet Display in feel), each name over the agent's mobile in small sans, placed left and right over the hero shot, e.g. Omar Amir-Mian 0428 553 883 and Sean Weill 0432 749 677.
  - **End card:** solid **black** with the small white **"amir prestige" wordmark** centred. That's all: no URL and no phone number.
- **Grade:** warm, slightly desaturated and filmic, with lifted creamy whites. Interiors lean beige and terracotta; exteriors run punchy blue sky against white render.
- **Audio:** music only, with **no voice-over**. The track is a **lo-fi hip-hop beat (~132 BPM)** with vocal chops, at -19 LUFS and -1 dBTP. The rapid bursts are cut to the drops, and the rest is cut loosely: only 20 % of cuts land within a frame of a sound. There are no added whooshes or SFX beds.

To match them: Montserrat Regular/Bold for the address, a serif for the agent names, a black wordmark end card, grey-mat framed montages and rapid-fire cut bursts on the drops, a warm filmic grade, a lo-fi beat, no VO, and the ap. pin on one wide drone. An overlay pack like [[real-specialists]]' (`projects/real-specialists-overlays/`) would cover the address super, agent names and end card.

Sources: [YouTube channel](https://www.youtube.com/channel/UCKRDrsPL0UD32sasmnXmJxQ), [44 Via Roma film](https://www.youtube.com/watch?v=RgFwW6Hm8Pk), [amirprestige.com.au](https://www.amirprestige.com.au/), [Domain agency page](https://www.domain.com.au/real-estate-agencies/amirprestigegroup-33541), [RateMyAgent Paradise Point](https://www.ratemyagent.com.au/real-estate-agency/amir-prestige-paradise-point-as181/sales/overview), [Ocean Road Magazine](https://www.oceanroadmagazine.com.au/at-amir-prestige-we-dont-follow-records-we-set-them/).
