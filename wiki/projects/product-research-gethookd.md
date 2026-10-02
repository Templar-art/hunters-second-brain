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
