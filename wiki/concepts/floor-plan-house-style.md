---
type: concept
tags: [floor-plans, deliverables, brand, qa]
status: active
updated: 2026-10-28
---

# Floor-plan house style (as delivered)

This is an audit of the floor plans 10x has delivered to real-estate clients, all drawn by the outsourced supplier from CubiCasa scans. Eleven plans were checked across eight clients, from September 2025 to October 2026. Contact sheet: [floorplans-by-client.jpg](../../projects/floorplan-app/refs/floorplans-by-client.jpg). The plans live on the Clients Drive under `<Client>/<Address>/Floor Plan/`, each delivered as a JPG and a PDF. Related: [[drone-photo-pin]] for per-client styling; the planned in-house app is in [audit-01-robina](../../projects/floorplan-app/audit-01-robina.md).

## Two template generations

| | Gen A (Sep 2025 – Feb 2026) | Gen B (Oct 2026) |
|---|---|---|
| Clients | RE/MAX Regency, The Agency (Jessica), Belle, Place, Ray White TMG | Coastline Prestige ×2, ZED, Harcourts Property Hub (Jessica) |
| Address | **Bold**, suburb in caps (Ray White: title case) | Regular weight, suburb in caps |
| Dimensions | `4.3 x 4.7` (no units) | `4.3m x 3.4m` (units) |
| Area strip | ALL CAPS `INTERNAL │ EXTERNAL │ TOTAL │ LAND SIZE` | Title case `Internal │ External │ Total │ Land area` |
| Site plan | Flat vector with a "│ Site Legend" line (RE/MAX, Ray White), or the house drawn inside the lot (Place, Belle, 88 Third) | Illustrated aerial cut-out with numbered markers and a vertical "Legend" list |
| North | Thin line arrow | Filled circle arrow |
| Walls | Heavy black | Mid-grey (Coastline, ZED, Parkwood) |

Common to both: A4 landscape, address top left, bed/bath/car counts plus north top right, framed plan area, area strip under the frame, client logo bottom left, the disclaimer, and the 10X VISUALS logo bottom right.

**The house style changed between February and October 2026.** No one has decided which generation is the 10x standard. That decision has to be made before the in-house app gets a template.

## Per-client blocks (what actually varies)

- **YPA QLD:** a completely different layout. There is no frame, a **yellow footer band**, `HOUSE SIZE` or the full area set, and a site plan with a hatched "Residence" footprint. **There is no 10x logo and no YPA logo.** The address sits bottom left. Fractional bathrooms are allowed (2.5).
- **RE/MAX Regency, Ray White TMG, Place, Coastline, ZED:** the agency logo only.
- **Belle Property:** the agency logo plus the agent's name and phone number (Logan Rullis).
- **Jessica Wallace:** the agency logo plus her name and phone. Her agency has changed from The Agency to Harcourts Property Hub, and she is co-listed with Talei Kelly.
- **Legend marker colour** follows the client: navy for Coastline and Harcourts, black for ZED.

## Errors found in delivered plans

These went out to clients.

1. **Jessica Wallace's phone number differs between plans:** `0422 962 688` on 88 Third Ave (Feb) and `0422 692 688` on Parkwood (Oct). One of them is wrong.
2. **Parkwood land area reads `1.061m²`.** That is a European thousands separator, so it reads as 1 m². It should be `1,061m²`.
3. **Ormeau (ZED):** "Siting" should be "Sitting". There is also a generic "Room" label, and no External figure.
4. **Lydford Close (Coastline):** "Addtional parking" should be "Additional parking". The study size `2.6 x 2.4m` is missing a unit on the first figure. The capitalisation is mixed: "Pdr" and "ENS" on one plan.
5. **Parkwood:** uses `4.5m X 3.2m` with a capital X alongside lowercase x elsewhere.
6. **Labels are inconsistent across all plans:**
   - Master: Bed 1, Master Bed and Master Bedroom.
   - Laundry: L'dry and Laundry.
   - Ensuite: Ens, Ens. and ENS.
   - Walk-in robe: WIR and W.I.C.

## Implications for the in-house app

- The template needs **client profiles**, the same way the drone-pin tool has them: logo, agent lines, marker colour, and the YPA layout as its own template.
- A label dictionary and a dimension format should be **locked rules**, not left to the drafter. Most of the errors above are the kind a deterministic check would catch: units, separators, spelling against a dictionary, and phone numbers against a stored client record.
- Agent phone numbers should come from a single stored record, never retyped.
