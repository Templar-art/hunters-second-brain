---
type: contact
tags: [agent, coastal, real-estate, gold-coast, music]
status: active
updated: 2026-10-28
---

# Katrina Walsh

**Role:** Sales agent, Lifestyle Properties (QLD) Pty Ltd trading in [[coastal|COASTAL°]] Broadbeach. Not the same agency as [[drone-photo-pin|Coastline Prestige]]: Hunter confirmed on 2026-10-28 that "Coast" means Coastal (coastal.com.au).
**Patch:** luxury and lifestyle property on the Gold Coast and in the hinterland, including Tallebudgera Valley, Tamborine Mountain, Currumbin, Burleigh, Palm Beach, Broadbeach and Isle of Capri. She also sells acreage, waterfront homes and boutique developments.
**Signals from her bio:** more than 20 years in the job and more than $1B sold. Her average sale is above $2M and her average campaign runs 46 days. She sold all 14 remaining residences at The Grand Golf Course on auction day. She describes her approach as "calm, considered" and genuine rather than salesy. She is passionate about wilderness conservation and animal rescue and is "rarely far from her beloved dogs". That last point drives the music direction below.

## Asset inventory (as of 2026-10-28)
Nothing is in the vault or on the Clients Drive yet. There is **no `Coastal` folder** under `gdrive:Clients`, and the Coastline Prestige folder is a different agency. Everything below is public and online. Nothing has been downloaded into the vault.

| Asset | Where |
|---|---|
| Agent profile and bio | https://www.coastal.com.au/katrina-walsh/ (her page exists, but she is not shown on the /team/ grid) |
| Headshot | Online only: `https://cdn.coastal.com.au/wp-content/uploads/2023/08/28121251/KW-Website.jpg`. Hunter doesn't need it, so it isn't downloaded. |
| Her listings | https://www.coastal.com.au/properties-for-sale/?agents=katrinawalsh |
| Instagram | [@katrinawalshrealestate](https://www.instagram.com/katrinawalshrealestate/): 942 posts, about 3.2k followers, bio "Marketing lifestyle and luxury homes on the Gold Coast." @10xvisuals_ and @10xrealestate_ already follow her. |
| LinkedIn | https://www.linkedin.com/in/katrina-walsh-a74b68127/ |
| Agency socials | IG [@coastalpropertyagents](https://www.instagram.com/coastalpropertyagents/), [Facebook](https://www.facebook.com/coastalpropertyagents/), [LinkedIn](https://www.linkedin.com/company/coastalpropertyagents/) |
| Logo | Downloaded 2026-10-28 into `raw/coastal/`: the wordmark in white and black (`coastal-logo-WHITE.png` and `coastal-logo-BLACK.png`, 1011×146), an older 450×58 `coastal-logo.png`, and the C° favicon (`coastal-c-mark-favicon.png`, 512², dark C° on a mint circle). A white transparent C° for drone pins was derived at `projects/drone-pin/logos/coastal-c-white.png`. |
| Third-party profile | [view.com.au](https://view.com.au/agent-profile/katrina-walsh-136600/) (thin data) |
| Past 10x work for her | None on record in the wiki or on Drive. The Coastal drone-pin profile notes the first Coastal job as 34 Albany Ave. |

## Her video formula (studied from IG, 2026-10-28)
The house style comes from her recent listing films: 4 Lita Court (142 s), 6 Stockyard Ct (108 s) and 8 Park Lane (65–110 s).

- **Format:** landscape 16:9, posted as reels. A main film runs about 90–140 s. Cut-downs and updates run 15–35 s (Under Contract, Sold, open-home reminders).
- **"KATRINA WALSH PRESENTS" title card** (Hunter's screenshot, 2026-10-28): her own title card. It is two lines, centred, white, with no box or shadow, laid over live footage (here, Katrina in red with her dogs on the front lawn). "KATRINA WALSH" is large, thin, uppercase geometric sans. "PRESENTS" sits under it, smaller and heavier (medium weight), also uppercase. ⚠️ My first pass from the IG frames wrongly took the COASTAL° wordmark for the "presents" beat. The wordmark is a separate title.
- **COASTAL° wordmark open:** a 4–6 s cold-open montage of drone, detail and nature shots (sunset over the range, a roofline, chickens behind netting, a tree canopy). The white wordmark sits centred over a slow drone sunset or canopy shot from about 5 s to 9 s; on Stockyard it is up by 3 s.
- **Voiceover-led:** she narrates. White, small, sentence-case subtitles sit in the lower centre ("Tallebudgera property", "If seek privacy…"). Captions often say "Turn Up The Volume for your Sneak Preview!". She appears on camera walking the grounds.
- **Music:** low and slow under the VO. The tracks credited on her reels are **Buddha Code – "Moment of Peace"** (8 Park Lane) and **Tony Batts – "To Live Again"** (6 Stockyard Ct, the IG audio version). Most other reels are tagged "Original audio", meaning a VO mix.
- **Outro (the last ~8 s):** a drone sunset over the hinterland with **KATRINA WALSH** in thin white caps and her number under it, centred. The COASTAL° wordmark sits small at the bottom centre. This dissolves to a **charcoal end card**: a dark charcoal-to-near-black vertical gradient. Upper centre: "KATRINA WALSH" in thin uppercase sans, with her number under it at about the same size in regular weight. At the bottom centre is the white COASTAL° wordmark with wide letter-spacing. The card is held to the end. (The red line at the very bottom of Hunter's screenshot is probably the player's progress bar, not part of the design; this needs checking against a clean frame.)
- **Grade:** warm and natural. She leans heavily on golden hour and dusk, with lit windows on the twilight exteriors.

## Rebuilt cards (2026-10-28)
`projects/coastal-katrina/make_cards.py` rebuilds both cards as 4K PNGs from Hunter's screenshots. Both use Helvetica Neue: Light for the name and number, Medium for PRESENTS. They are matched by eye, because her original font file is unknown.
- `out/katrina-walsh-presents-4k.png`: transparent, so it can be laid straight over footage.
- `out/katrina-walsh-end-card-4k.png`: the charcoal gradient end card, using `raw/coastal/coastal-logo-WHITE.png`.
- `animate.py` builds the animated versions as 4K ProRes 4444 with alpha at 25 fps. The MOVs are gitignored; re-run the script to rebuild them.
  - `out/katrina-walsh-end-card-anim-4k.mov` (8 s): the charcoal background fades up over the footage across 0–1 s. The name eases in at 0.6 s, the number at 0.9 s and the wordmark at 1.5 s, each with a fade and a 24 px rise. It holds to the end.
  - `out/coastal-pin-anim-4k.mov` (5 s): the thin white stem draws up from the ground point across 0–0.7 s, then the C° fades in and settles on top across 0.5–1.1 s. The ground point is at frame centre, 72% down; move the clip in the edit to place it. The stills are `out/coastal-pin-4k.png` (full frame) and `out/coastal-pin-tight.png` (cropped).
  - The pin size was matched to Coastal's own pin on the 4 Lita Ct drone still, and overlaid it is near-identical. Coastal's pins carry **no address label**. In her films the place name appears instead as a small white sentence-case caption at the lower centre ("Tallebudgera property").
- To change sizes or positions, edit the numbers in the script and re-run it with `python3 make_cards.py [background.jpg]` (the background only feeds the preview).

## Drone pin style (Coastal listing photos)
From the 4 Lita Court and 6 Stockyard Ct photo sets on coastal.com.au:
- **Pin:** a white **"C°" mark** on top of a **thin white vertical stem**. There is no badge, no dot and no address label.
- **Lot outline:** a thin white boundary polygon with no fill.
- They use it on one to three wide drone frames per set, from both oblique and top-down views.
- This fills in the open `coastal` profile in `projects/drone-pin/clients/coastal.json` (see [[drone-photo-pin]]): pin = mark, fill 0, no label. The white mark is `projects/drone-pin/logos/coastal-c-white.png`.

## Other graphics
- Her open-homes tiles use a line-art **"KW" monogram** in white on light grey, with "Katrina Walsh" / "Open Homes" in a small regular font.
- Her three **pinned IG posts** are brand and trust reels: a January 2026 listings push, a vendor testimonial (Luca by Mosaic), and "$20.25M in sales in recent weeks".
- Highlights: Testimonials · Listings · SOLD · In the News · Coastal · My Spare Time.

## Music shortlist (slow, earthy)
The direction follows from her own picks (meditative ambient, slow piano) and her bio (wilderness, animals, hinterland acreage): soft, organic and acoustic, with room under a VO. Library rows refer to `~/Desktop/_Brand & Tools/10x-Visuals/Business Docs/10x Visuals — Music Reference Library (Cleaned).xlsx` (124 tracks; the finder is `10x Music Finder.html` in the same folder).

| # | Track | In library? | Why |
|---|---|---|---|
| 1 | Novo Amor – *Anchor* | Yes (#97, rated 4) | Hushed falsetto folk with a slow build. Fits misty hinterland mornings. |
| 2 | Gregory Alan Isakov – *The Stable Song* | Yes (#98) | Banjo and dusty folk, the most "earthy" option. Suits acreage and animals. |
| 3 | S. Carey – *In the Dirt* | Yes (#101) | Literal earthiness: piano with natural textures. |
| 4 | Luke Howard – *Dappled Light* | Yes (#82) | Instrumental piano. The safest bed under her voiceover. |
| 5 | Bon Iver – *Holocene* | Yes (#19, rated 5) | A wilderness feel. Good for a sunset-drone open. |
| 6 | Agnes Obel – *Riverside* | Yes (#100) | Water imagery. Suits her waterfront and Isle of Capri listings. |
| 7 | Benjamin Francis Leftwich – *Atlas Hands* | Yes (#66) | Warm fingerpicked acoustic. Lifts a little for the reveal. |
| 8 | Buddha Code – *Moment of Peace* | No (her own pick) | Use it as the tone reference: it shows exactly the calm she chooses. |

**Licensing:** 1–7 are commercial releases, available through Spotify and YouTube. An agency film needs a sync licence, or should use IG's in-app audio, which may be restricted on business accounts. For a clean commercial use, look for close Artlist equivalents (acoustic folk / ambient piano) or the Artlist-sourced rows in the library.

## Related
[[coastal]] · [[drone-photo-pin]] · [[floor-plan-house-style]]
