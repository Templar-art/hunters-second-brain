---
type: project
tags: [ecommerce, product-research, gethookd, meta-ads, tradies]
status: research
updated: 2026-10-02
---

# Product research via GetHookd (tradie / problem-solving products)

Hunter is looking for a new product to sell, separate from 10x client work and from [[one-percent-standard-store]]. The brief: source from proven US Meta ad winners, sell into **Australia**, with a **$500–2k test budget per product**. It must be a problem-solving product (column 2 of the "3 types of products" guide) or an essential (column 3), and **not something Bunnings already sells cheaply**. Construction and tradies are the preferred audience, because a mate of Hunter's does well selling to tradies, mostly through Google Ads.

## GetHookd setup
- GetHookd is a Meta (Facebook and Instagram) ad-intelligence platform: about 5–6M running ads across 400k+ brands. It does **not** see Google ads, so tradie demand on Google search has to be checked elsewhere (Keyword Planner).
- The MCP server `gethookd` was added at **user scope** on 2026-10-02 (`claude mcp add --transport http`, URL `https://app.gethookd.ai/api/mcp/v1`, key in `~/.claude.json`, never in the vault).
- The account is on the **Starter plan**, with 60 credits at setup. Searches bill per row at about **0.01 credits per row**, so a 10-row search costs about 0.1. Brand Spy (needed for `get_creative_breakdown`) costs about 8× a normal call. `get_brand` and the profile tools are free.
- The profile survey is part-done: seller type C (no product yet), niches recorded, market left open. Hunter researches US data to sell into AU, so pass `geo: "US"` by hand. The two closing questions, what he can produce and whether to create a product in GetHookd (5 credits), are still unanswered.

## First pass (2026-10-02, ~1.3 credits spent)
Filters: US, performance tiers optimized+winning (4–5 stars), brands with 100–400 active ads, one ad per brand.

- **Niche sweep** (Home/Garden, Tech, Health/Wellness, problem/solution angle): 68 brands. About 80% were health-claim products (gut, tinnitus, menopause, pain devices), which are TGA-risky in AU, or services. Physical keepers: Muravai shower head, Tumbler knife sharpener, Wyze Window Cam, AIRLOCK RV purifier, Manta Sleep (night-shift sleep mask), Magic Mat.
- **The keyword "construction" is useless.** It matches "premium construction" apparel and articles. Tradie products only surface under product words: tools, storage, socks, measuring, truck.

Web research on six candidates, against four tests (retail ≥ 3× landed cost, not at Bunnings, 10-second demo, small and light):

| Product | Score | Why it fails |
|---|---|---|
| Cyber Power Tools MeasurePro (tape + laser + level) | 4/10 | Generic white label already sold by AU DTC stores (Ozerty A$96, lasertapemeasure.com.au A$69) and on eBay from A$16. Accuracy complaints. Check laser import class |
| ToolBox Widget organisers | 3/10 | Brand already sells in AU (.com.au), 6 US patents plus an AU trademark, and a Bunnings Trojan holder at A$17.98 |
| Camel City Mill merino work socks | 4/10 | Kmart and Big W sell merino work 6-packs at about A$11.50 a pair; a 3× markup prices above them |
| EZARC step drill set | 4/10 | Bunnings Craftright A$14.98 and Ryobi A$34.99. The angle only works against Milwaukee at A$157 |
| Muravai filtered shower head | 4/10 | WaterMark and WELS are mandatory (fines up to A$109k per breach), and Bunnings has filtered heads from A$34 |
| Tumbler rolling knife sharpener | 3/10 | AU is saturated: Kimbo, KitchSharp, Bunnings-listed Baccarat, Horl |

**Lesson: by the time a US Meta winner is obvious, it's usually already in AU, either at Bunnings or Kmart or through an AU DTC clone.** For each US winner, the screen has to ask "is anyone selling this in AU yet?", not just "is it winning?".

**Leads still open:**
- EZARC's longest-running ad is not the drill set. It's **Japanese-tooth pruning blades for reciprocating saws**, running 442 days in US and GB: a consumable, small, tradie- and garden-friendly.
- Cyber Power Tools' longest-running ad is a stud finder ("drilled into a live wire once"), running 99 days.

Both still need the AU check.

## Second pass (2026-10-02, ~2.5 credits spent, 56.2 left)
A GetHookd sweep of 43 tradie product keywords, using the same filters, then nine web-research agents scoring candidates on a 100-point scorecard. The scorecard weights: AU gap 25, margin 20 (≥3× landed **and** gross profit ≥ A$30 to fund a Meta CPA of A$25–40), US proof 15, demo 10, shipping 10, compliance/IP 10, repeat/AOV 10.

| Product | Score | Verdict | Key fact |
|---|---|---|---|
| Wire break / short finder (SolderStick, generic EM415PRO), 6–42V DC | 70 | MAYBE | Landed ~A$18. No Bunnings equivalent (Power Probe A$579 at Supercheap). eBay AU A$19 clones, and the model number printed on the unit lets buyers find them |
| Chain offset extension (Bolthero), for ratchets, not drills | 67 | MAYBE | Landed ~A$21, GP ~A$36 at A$69. Not at Bunnings or Total Tools. eBay AU clones from A$19.95 |
| Japanese-tooth recip pruning blades (EZARC) | 62 | MAYBE | 8+ US sellers. GP ~A$25 on a 5-pack fails the A$30 bar. Milwaukee 5-pack A$55.95 at Total Tools |
| Spanner-to-socket adapter (Olsa "stubby clip") | 59 | MAYBE | GP ~A$19. Mechanics' niche |
| Rugged job-site smartwatch (Njord) | 59 | SKIP | 7+ AU sellers already, including Hard Hat Foreman A$199.95 |
| Bluetooth hearing-protection earbuds | 54 | SKIP | Bunnings Citeco AS/NZS 1270 Class 5 at A$60.77 |
| Stylish safety glasses | 54 | SKIP | SafeStyle (founded by a Perth plumber) at Total Tools. Needs AS/NZS 1337.1 |
| Drill-tap combo bits (FixionTools) | 54 | SKIP | A$9–12 on eBay and Amazon AU |
| Portable drill guide (SpeTool) | 52 | SKIP | The brand itself sells on Amazon AU at A$405 |
| Stud finder (Cyber Power Tools) | 46 | SKIP | 20 SKUs at Bunnings. Useless on brick walls |
| Socket rails (Olsa) | 41 | SKIP | Kincrome at Bunnings ~A$18 |

**Nothing scored TEST.** Across 17 products, the pattern held: a US Meta winner is almost always a Chinese white label that is already on eBay or Amazon AU, so the AU price ceiling is set by the A$20 clone. The best scores went to products where **big-box stores don't stock them and the only competition is marketplace junk**. That gap can only be held with a branded bundle that a buyer can't search their way around.

Gotchas: a GetHookd landing-page URL often 404s (find the live page by search). The `rubric.txt` handed to research agents has to live in the session scratchpad, not `$TMPDIR`.

## Third pass (2026-10-03, ~1.5 credits, 54.7 left)
A GetHookd sweep of 36 Australian lifestyle keywords (4WD, caravan, camping, ute, garage, garden, pool, BBQ, fishing), then 9 products scored on the same 100-point card. Six of the research agents hit the Claude session limit partway through and were resumed. The pool thermometer report is thinner as a result.

| Product | Score | Verdict | Key fact |
|---|---|---|---|
| Drill-chuck fence wire twister | 63 | SKIP | Only twists pre-formed 9-gauge chain-link ties; no AU supply of those ties. GP ~A$23 |
| Flatpack grill / stove / pit (Bigfoot) | 59 | SKIP | Kmart folding pit A$49, Bunnings A$65, Winnerwell AU. Fire-ban season |
| Stick-on caravan door catch | 53 | SKIP | Camec catch (A$12.95) already fitted on most AU vans. 6+ on Amazon AU |
| Auto-stop tyre inflator (LockNLube) | 52 | SKIP | LockNLube has its own .com.au. Tracker 4x4 and iCheck A$229–249. Ozito preset A$60 |
| Trailer "GPS" tracker (Add-On Design) | 45 | SKIP | It's a Bluetooth Find My tag; Kmart sells them at A$12. A real 4G tracker is a separate idea |
| Magnetic UHF mic mount | 44 | SKIP | Uniden, GME and Oricom sell their own at A$40 (Supercheap, Repco, BCF) |
| Collapsible fire pit (Chiasson) | 44 | SKIP | 20kg; ARB flat pack A$349 |
| Camping rope tensioners (Hydrava) | 42 | SKIP | Hydrava is itself Australian. Bunnings Grunt 2-pack A$14.87 |
| Wireless pool thermometer | 42 | SKIP | Inkbird AU store A$30–46 caps the price |

**After 26 products across three passes, none scored TEST.** The method is the problem. A US brand running 100–400 ads with 4–5 star performance is, almost by definition, selling a generic white label, and by then that item is already on Amazon or eBay AU, at Bunnings or Kmart, or with an AU distributor. In AU lifestyle categories, specialist incumbents (ARB, GME, Camec, Inkbird) own the shelf as well. Next: flip the method (AU demand first, or GetHookd with `geo: AU` to see what's winning *here*), or build a differentiated bundle around the best "maybe" (the 12V fault-finding kit).

## Fourth pass: AU-running ads (2026-10-03, ~1.6 credits, 53.1 left)
**Hunter's steer: stay in his niches (tradie/construction, home/interiors, fitness/wellness, camera/video gear). No more 4WD/caravan drift.**

Searched with `geo: AU`. Only 6 brands matched 100–400 active ads, so the minimum was lowered to 20. AU winners run far longer (380–750 days), so AU demand is already proven. The scorecard was adjusted accordingly (`rubric_au.txt`): "AU gap" now asks whether the competition is one overseas dropshipper (beatable with local stock and better video) or many sellers plus big-box.

| Product | Score | Verdict | Key fact |
|---|---|---|---|
| SuperGrip magnetic phone/tablet desk arm (Cyber Vintage) | 69 | MAYBE | No premium AU seller; the advertiser ships from Dongguan/US (~14 days). GP ~A$52 at A$89. Cheap A$32 arms on Amazon AU |
| Concealed hinge jig (Fivalo) | 66 | MAYBE | Fivalo is an overseas dropshipper (9-day delivery). Kreg at Bunnings A$63 caps the price; GP ~A$30 at A$59. Bundle needed |
| GlowRight multi-light sensor system | 64 | MAYBE | 10.7k reviews, ships in 10–12 days. Single bars are A$15–17 at Kmart and Bunnings; only the "one sensor, whole room" system is a gap. Lithium + RCM |
| Pilates bar kit (Stretched Fusion) | 64 | MAYBE→SKIP | The advertiser really sells a video subscription. The bar is A$10–70 everywhere |
| Lumbar/seat cushion (Nordic Comforts) | 56 | SKIP | Kmart and Big W A$20–47. TGA bans the "back pain" hook |
| Countersink bit set (Fivalo) | 52 | SKIP | Ryobi A$9.98 at Bunnings |

**Overall top 5 after 32 products:** 12V wire fault finder 70 (auto, outside the core niches), SuperGrip arm 69, Bolthero offset extension 67, hinge jig 66, GlowRight system 64. None is a clean TEST yet. The next validation step is a physical sample plus a filmed demo, not more desk research.

## Fifth pass: back on brief (2026-10-03, ~1.3 credits, 51.8 left)
**Locked brief (updated 2026-10-03):** NO camera/video or fitness — Hunter doesn't think there's a market; tradie/DIY + home/interiors only. Every MAYBE+ gets a traffic check (visits + source mix via SimilarWeb-type estimators). Original brief: US data, brands running 100–400 active ads, 4–5 star ads, problem-solving (col 2) or essentials (col 3), only in camera/video, fitness/wellness, home/interiors, tradie/construction, nothing Bunnings sells. Every product gets a "problem it fixes" line. Swept 31 camera, fitness and home keywords.

| Product | Score | Problem it fixes | Why not |
|---|---|---|---|
| Horizum Tap-To-Snap magnetic pop-up tripod | 59 | Phone tripods are fiddly; clamps slip, legs wobble | Ulanzi MT85 at A$30 on Amazon AU, Kmart magnetic A$39 |
| Cotton Carrier camera chest harness | 55 | Neck-strap pain, swinging camera | Brand already sold by AU camera stores; A$35 generics |
| Neck phone holder (Moonighty) | 54 | Arm fatigue holding a phone; hands-free POV filming | Kmart A$6 |
| DrainWig shower hair catcher | 52 | Hair clogging the shower drain | Already in AU (Grays); Bunnings/Kmart A$12–20 |
| Octobuddy suction phone mount | 49 | Nowhere to put the phone when filming in a bathroom or gym | Kmart A$6 |
| GLASSGUARD mould gel | 39 | Black mould in shower silicone | Already an Australian brand shipping from Sydney; chemical DG |
| Chiclify anti-snap bands | 39 | Cheap bands snap mid-rep | Kmart/Rebel; the advertiser is a churned dropshipper |

40 products scored so far. Pattern: low-ticket problem-solvers (<A$30 retail) always lose to Kmart's A$6–20 copy. The only workable shape is a **higher-ticket product (A$60–120) or a bundle**, where the US premium version hasn't landed in AU and Kmart's version is visibly worse.

## Sixth pass: home/interiors + price filter (2026-10-03, ~2.2 credits, 49.6 left)
The `price_point: mid,premium` filter only covers a small share of ads (mostly recent), so it can't be used as a primary filter. A home/interiors sweep of 25 keywords followed.

| Product | Score | Problem it fixes | Why not |
|---|---|---|---|
| Frame For TV snap-on frame | 60 | A wall TV looks like a TV, not art | **Fits Samsung The Frame only**, despite the "any TV" ad. Deco TV Frames AU (Sydney) A$599–949; Samsung bezel A$149 at Harvey Norman. GP ~A$186 at A$299, but a tiny audience and a 1.5m box |
| Invisible under-desk wireless charger | 41 | Cable and pad clutter on the desk | IKEA SJÖMÄRKE A$55; Deskup AU |
| LED anti-fog mirror cabinet (Wellfor) | 37 | Foggy mirror, bad light, cluttered vanity | Bunnings Attica, Temple & Webster; bulky glass; electrician needed |

Total scored: 43.

## Seventh pass: fitness + camera accessories (2026-10-03, ~2.3 credits, 47.3 left)
Camera accessory searches only returned big brands (Neewer, Amaran, SIRUI, SANDMARC), with nothing to white-label. An Ekko lifting-straps ad (4–5 stars) surfaced as a reference for [[one-percent-standard-store]].

| Product | Score | Problem it fixes | Why |
|---|---|---|---|
| Cordless (ropeless) battle ropes, Ekoh/BattleFlex white label | 66 | Battle-rope cardio without a 15m rope, anchor or garage | MAYBE: not at Kmart/Big W/Rebel (rope only); AU has only eBay/Stacks junk at A$42–51. GP ~A$28 at A$69, just under the bar. Air freight on 1.8kg hurts; sea freight would fix it |
| Sauna blanket (Hydragun HeatPod) | 49 | Sauna heat at home without a sauna | Hydragun ships free to AU; Mihigh A$259 |
| Adjustable kettlebell (Freak Athlete) | 35 | One bell replaces a rack | FA AU store, Bells of Steel AU A$280; 33kg freight |
| Mini 1-person sauna (Peak) | 37 | Real sauna in a corner, no electrician | 120V only, 140kg crate; Jarli AU A$1,709 |

Total scored: 47.
