---
type: client
tags: [client, real-estate, agency, drone, pin, southern-gold-coast, tweed]
status: active
updated: 2026-11-06
---

# REAL Specialists

**Who:** a southern Gold Coast and Tweed agency. The head office is at 4/6-8 Amber Road, **Tweed Heads South NSW 2486**, and the agency works both sides of the border (Coolangatta, Kirra, Bilinga, Tugun, Currumbin, Tweed Heads, Kingscliff, Murwillumbah). There are about 30 agents. Wayne Bisgrove is listed at "REALSPECIALISTS Head Office". The agency rates 4.8 on RateMyAgent from roughly 109 reviews. A separate commercial arm, REAL Specialists Commercial, exists. Don't confuse the agency with **RE/MAX Real Estate Specialists** (Burleigh), which is a different business with its own profile, `remax.json`.

**Why we care:** **Connor Hewitt** has moved here (Hunter, 2026-11-06). Allhomes now lists him on the REAL Specialists team. He was previously at JW. Prestige Agents in Mermaid Beach, and McGrath also lists him as a Palm Beach/Currumbin sales agent. His Instagram is `@connorprestigeagents`, a handle from the JW era. His Allhomes profile shows no live listings yet.

## Brand
- **Logo:** an orange stacked-bar "R" icon, then **REAL** in heavy caps over a lighter **SPECIALISTS**. On their portal tiles it is white on solid orange. In drone stills the logo is orange directly on the sky.
- **Orange:** **#E45E39**, taken from the transparent logo on their own site. (The #FF6634 sampled from the Allhomes tile was a JPEG approximation.)
- **Web font:** Lato (site body and headings).
- **Website:** [realspecialists.com](https://www.realspecialists.com/). It is .com, not .com.au, and has the tagline "Reinventing Real Estate". The logo files are `/assets/img/RS-logo-blue.png` (which is actually the orange version) and `RS-logo-white.png`, both 491 px PNGs. Copies are in `raw/real-specialists/`.

## Drone pin style (from their own listing stills)
Reference: 5 Riviera Ave, Tweed Heads West (EOI, Nov 2026). The three pinned drones are saved in `raw/real-specialists/`.
- **Pin:** the full orange logo with no badge, box or circle, sitting on the sky above a **thin white vertical line** down to the house. There is no dot at the end.
- **Lot outline:** none in their stills.
- **Location pins:** yes. These are small **dark (near-black) sentence-case labels** for nearby suburbs and landmarks (Bilinga, Kirra, Coolangatta, Currumbin, Tugun), each on a thin white line, with no dot and no distance.
- They are used on high wide obliques along the river and coast.

The profile is `projects/drone-pin/clients/real-specialists.json`. It is **unconfirmed** until Hunter or Connor signs off the look.

**Still needed:**
- ~~Logo PNG~~ **done 2026-11-06:** traced their 491 px PNG into a vector (`projects/drone-pin/logos/real-specialists.svg`, potrace) and rendered a 3000 px orange PNG for print. Their line hangs from the logo's **left edge**, so a new `mark_anchor: "left"` style key was added to `drone_pin.py` and `review.html`. A test render matched their stills. An official vector from the brand pack would still be better.
- ~~Dark labels~~ **done 2026-11-06:** `place_color: "#1E1E1E"` and `place_dist: false` are set in the profile. A test render gave flat dark labels with no distance line on white lines, as in their stills. Place labels on the sky: dark text over rooftops is hard to read.
- Confirmation of whether Connor wants their stock look or something of his own. Prestige agents often brand themselves; his JW-era IG handle suggests a personal brand.

## Gotchas
- **NSW lots:** ~~QLD only~~ **done 2026-11-06.** The Drone Pin tool now falls back to NSW Spatial Services, so Tweed-side addresses resolve to the real lot outline (see [[drone-photo-pin]]).

Sources: [Allhomes agency page](https://www.allhomes.com.au/agency/real-specialists-496872/), [Connor Hewitt on Allhomes](https://www.allhomes.com.au/agent/connor-hewitt-1602534/), [RateMyAgent](https://www.ratemyagent.com.au/real-estate-agency/real-specialists-am265/sales), [Connor Hewitt on RateMyAgent (JW. Prestige)](https://www.ratemyagent.com.au/real-estate-agent/connor-hewitt-eb505/sales), [McGrath profile](https://www.mcgrath.com.au/agents/connor-hewitt-a1VRE0000019fkv2AA).

Related: [[drone-photo-pin]], [[kollosche]], [[jessica-wallace]].
