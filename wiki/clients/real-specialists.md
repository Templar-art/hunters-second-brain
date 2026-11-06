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
- **Orange:** about **#FF6634**, sampled from the Allhomes agency tile (R255 G102 B52). This is approximate, so get the real value from a brand pack.
- **Fonts:** unknown.
- **Website:** realspecialists.com.au did not resolve from here on 2026-11-06. Their listings are on Allhomes, Domain and REA.

## Drone pin style (from their own listing stills)
Reference: 5 Riviera Ave, Tweed Heads West (EOI, Nov 2026). The three pinned drones are saved in `raw/real-specialists/`.
- **Pin:** the full orange logo with no badge, box or circle, sitting on the sky above a **thin white vertical line** down to the house. There is no dot at the end.
- **Lot outline:** none in their stills.
- **Location pins:** yes. These are small **dark (near-black) sentence-case labels** for nearby suburbs and landmarks (Bilinga, Kirra, Coolangatta, Currumbin, Tugun), each on a thin white line, with no dot and no distance.
- They are used on high wide obliques along the river and coast.

The profile is `projects/drone-pin/clients/real-specialists.json`. It is **unconfirmed** until Hunter or Connor signs off the look.

**Still needed:**
- The logo as a transparent PNG; only a 120 px thumbnail was online. Ask Connor or the office for the brand pack.
- A dark-label style key in `drone_pin.py`, because labels currently render white.
- Confirmation of whether Connor wants their stock look or something of his own. Prestige agents often brand themselves; his JW-era IG handle suggests a personal brand.

## Gotchas
- **NSW lots.** The Drone Pin tool's cadastre lookup is QLD only (see [[drone-photo-pin]]). Tweed-side listings (Tweed Heads, Kingscliff, Murwillumbah) need the NSW Spatial cadastre added, or a hand-placed pin with no outline.

Sources: [Allhomes agency page](https://www.allhomes.com.au/agency/real-specialists-496872/), [Connor Hewitt on Allhomes](https://www.allhomes.com.au/agent/connor-hewitt-1602534/), [RateMyAgent](https://www.ratemyagent.com.au/real-estate-agency/real-specialists-am265/sales), [Connor Hewitt on RateMyAgent (JW. Prestige)](https://www.ratemyagent.com.au/real-estate-agent/connor-hewitt-eb505/sales), [McGrath profile](https://www.mcgrath.com.au/agents/connor-hewitt-a1VRE0000019fkv2AA).

Related: [[drone-photo-pin]], [[kollosche]], [[jessica-wallace]].
