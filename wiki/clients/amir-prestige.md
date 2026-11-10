---
type: client
tags: [client, real-estate, agency, drone, pin, gold-coast, prestige]
status: prospect
updated: 2026-11-10
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

### Pin system across their whole book (checked 2026-11-10)
On 2026-11-10 we went through all 18 residential listings on their site (about 450 gallery photos). References are in `raw/amir-prestige/pin-refs/`.
- **The "ap." pin is house style.** Almost every listing with a wide drone has it: the white "ap." in the sky, a gap, then a hairline straight down to the property. It is used in blue-sky, dusk and night shots, over canals, golf courses, cities and acreage. It appears once per wide, and the same frame is often reused with a second crop. The size varies with the shot. It is about 3% of frame height on city wides, but it can be **much bigger** (roughly 8–10%) on a single-subject shot. The Coombabah example has a large ap. over the river.
- **Location labels are inconsistent.** They depend on who shot the listing.
  - The Surfers and Isle of Capri style is **BOLD UPPERCASE** sans, with the hairline starting at the label's left end.
  - Coombabah uses **light sentence-case** sans ("The Pines Golf Course", "Paradise Point"), with the label centred over a short line that ends in a **small dot**.
  - Eureka uses regular uppercase with a short line ("BANGALOW", "BYRON BAY").
  - So there's no locked type spec for labels. Default to the Via Roma uppercase style.
- **Apartments and towers:** the ap. line runs down, then elbows sideways (a right-angle leader) to the exact floor. One version adds a **translucent white-filled outline of the unit's floor band**, with "OUTLINES INDICATIVE ONLY" in small caps bottom-left. A tower at dusk instead lit the floor glowing gold, with an elbow leader to it.
- **Lot outlines do get used,** contradicting the Via Roma-only read above. They are a **plain white stroke (~3 px at 1400 px), with no fill, no ap., no dimensions**.
  - On top-down obliques the outline sits over the **B&W surround** with the lot in colour, plus centred bottom text: "Boundaries and dimensions are approximate only / Interested parties should conduct their own independent enquiries."
  - On acreage it is used in full colour with no mono surround and no text.
- **Multi-lot land:** each lot gets its own **semi-transparent colour fill** (rust, green, ochre, burgundy), a white border, and a centred white **address in uppercase**. A grey-box disclaimer sits top-left: "**DISCLAIMER:** BOUNDARIES INDICATIVE ONLY".
- **Never seen:** a dot or pin head on the ap. pin, a distance or km label, coloured or teal lines, or a circle or badge behind the ap.

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
  - **⚠️ Not universal (checked 2026-11-10).** In three more films the agent names are the last frame, with no black card. Those films are 48/53 Darrambal St (Surfers Paradise), 1/37 Broadwater St (Runaway Bay) and 7 Martinique Way (Clear Island Waters). Each one ends on a **scenic drone**: a Surfers skyline from the water, a boat wake over sandbanks, or a canal sunset. The names sit **over that drone**, in the same white serif with sans mobiles, either left and right or stacked in the centre, held about 3 s with a fade-in. So the common ending is **agent names over the closing drone**, and the black wordmark card is optional.
- **Grade:** warm, slightly desaturated and filmic, with lifted creamy whites. Interiors lean beige and terracotta; exteriors run punchy blue sky against white render.
- **Audio:** music only, with **no voice-over**. The track is a **lo-fi hip-hop beat (~132 BPM)** with vocal chops, at -19 LUFS and -1 dBTP. The rapid bursts are cut to the drops, and the rest is cut loosely: only 20 % of cuts land within a frame of a sound. There are no added whooshes or SFX beds.

To match them: Montserrat Regular/Bold for the address, a serif for the agent names, a black wordmark end card, grey-mat framed montages and rapid-fire cut bursts on the drops, a warm filmic grade, a lo-fi beat, no VO, and the ap. pin on one wide drone. 
## Overlay pack (built 2026-11-09)
The generator is `projects/amir-prestige-overlays/make_overlays.py`. It renders ProRes 4444 alpha MOVs for FCP at 25 fps, in 16:9 4K and 9:16 1080x1920, plus a PNG of each:
- **00 logo opener:** the white wordmark centred with a soft shadow and no box. It eases in over 3 s and hard-cuts out. The Via Roma film opens on the address with no logo, so this opener is our addition at Hunter's ask.
- **00b logo on black** (2026-11-10): the same wordmark on solid black, opaque. It fades up from black and back over 3.5 s. The 1000 px source is upscaled about 15 % at 4K, so ask for a vector logo.
- **01 address:** `STREET, **SUBURB**` in Montserrat Regular/Bold caps, on one line, 3 s.
- **01n property name** (e.g. "Bella Vista"): the first version used a large italic with a swash, and Hunter called it **tacky** (2026-11-09). It is now restrained, with `--name-style lower` as the default, Hunter's pick: **bella vista** in Playfair SemiBold lowercase like their wordmark, and the suburb clear and bold in Montserrat SemiBold tracked caps, with no rule. Option A was BELLA VISTA in Playfair Regular caps with wide tracking, a short hairline, and the suburb in small tracked Montserrat caps. The tracking settles slightly as it fades in, and it holds 4 s. The `lower` style (lowercase, like their wordmark) and the `roman` style are alternatives.
- **02 agents:** Playfair names over Montserrat mobiles, left and right (stacked for 9:16), 3 s.
- **03 end card:** black with the small white wordmark, 3 s, opaque.
- **04 grey mat:** their framed-montage border, #D6D6D6 with a clear window, 5 s.

Run: `~/.venvs/typeset/bin/python -I make_overlays.py <out> --address "STREET|SUBURB" --name "Bella Vista" --name-sub "SUBURB" --agent "Name|mobile" --preview frame.jpg`. The sample in `out/` uses the Via Roma address and agents as placeholders.

**First job: 8 Nassau Ave, Terranora NSW 2486, "Bella Vista"** (2026-11-09). The pack is on T7 at `8 Nassau Avenue Terranora/Amir Overlays/`. The agent isn't known yet, so the 02 card now reads "Placeholder / 0000 000 000" (re-rendered 2026-11-10); re-run with `--agent` when we have it. Note that the T7 shoot folder is named `| Coastline`. Fonts are OFL: Montserrat and Playfair Display stand in for Garet and their serif.

Sources: [YouTube channel](https://www.youtube.com/channel/UCKRDrsPL0UD32sasmnXmJxQ), [44 Via Roma film](https://www.youtube.com/watch?v=RgFwW6Hm8Pk), [amirprestige.com.au](https://www.amirprestige.com.au/), [Domain agency page](https://www.domain.com.au/real-estate-agencies/amirprestigegroup-33541), [RateMyAgent Paradise Point](https://www.ratemyagent.com.au/real-estate-agency/amir-prestige-paradise-point-as181/sales/overview), [Ocean Road Magazine](https://www.oceanroadmagazine.com.au/at-amir-prestige-we-dont-follow-records-we-set-them/).
