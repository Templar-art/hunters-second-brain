---
type: project
tags: [ecommerce, brand-identity, packaging, store-prototype, white-label]
status: provisional
updated: 2026-11-11
---

# VELLAN body device store (brand + packaging + store prototype)

A white-label body-contour device brand, **VELLAN** ("The Body Contour System"), in the same family as Hunter's own stores [[one-percent-standard-store]] and [[bebita-lifestyle-store]]. Built 3 Nov 2026: brand marks, a tuck-end box dieline, a supplier pack and a multi-page static store prototype (`store.html`). **Provisional:** it is not yet on Shopify, the supplier's box size is unconfirmed, and no product, pricing or supplier facts are recorded in the folder. Project folder: [projects/body-device-store](../../projects/body-device-store/).

## Brand
Palette: Bone `#EEE8E0` (background), Sand `#DCCFBF`, Clay `#9C5B43` (accent), Espresso `#221C18` (ink), Stone `#7A6E64`. Type: Cormorant (serif, 400/500) with Jost (sans, 400/500), as variable fonts in `fonts/`. Marks are in `brand/`: a clay logo mark, wordmarks and stacked logos in bone and espresso, and a favicon.

## Reusable technique
- **Outline every glyph for print.** `brand.py` uses fontTools to instance the variable fonts and convert all text into SVG paths, so the printer's files need no fonts. `make_logo.py` and `make_box.py` build on it.
- **Parametric dieline.** `make_box.py` draws a straight tuck-end carton in mm (W/D/H plus bleed, tuck and glue flaps). It outputs three files, **cutter lines only**, **dieline with art** and **print art only**, each as SVG, PDF and PNG, which is the set a packaging supplier asks for. It is currently set to 230×80×170 mm: change W/D/H to the supplier's confirmed internal size and re-run.
- `VELLAN_supplier_pack.zip` bundles the brand and box files to send to the supplier.
