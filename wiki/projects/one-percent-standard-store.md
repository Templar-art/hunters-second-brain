---
type: project
tags: [shopify, ecommerce, white-label]
status: draft-product
updated: 2026-09-29
---

# One Percent Standard (Shopify store)

Hunter's own white-label e-commerce store, separate from 10x client work. 100 units of stock landed with Hunter on 2026-09-29, so this is **self-fulfilled white label, not dropshipping**: Hunter packs and posts (Australia Post MyPost Business via Starshipit/Shippit) until volume justifies a 3PL.

## Setup
- Store: One Percent Standard, `2gasmy-p1.myshopify.com` (alias `onepercentstandard.myshopify.com`), AUD, trial plan. Dev Dashboard org is also named One Percent Standard.
- Claude access: a Dev Dashboard app named **Claude** (version `claude-2`) with product, inventory, order, fulfilment, shipping and location scopes. `claude-1` shipped with no scopes; scopes live in the version, so adding them means releasing a new version and re-approving the install.
- Credentials: `SHOPIFY_STORE`, `SHOPIFY_CLIENT_ID`, `SHOPIFY_CLIENT_SECRET` in `~/.zshrc` (created 2026-09-29, mode 600). Never in the vault.
- Dev Dashboard apps don't issue a permanent `shpat_` token; [shopify.sh](../../projects/shopify-store/shopify.sh) swaps the client ID/secret for a short-lived token (client-credentials grant) and caches it 20h. Admin GraphQL API `2026-07`.
- Shopify Dev MCP (`@shopify/dev-mcp`) added at user scope for docs and schema lookups.

## Product
**Cuffed D-Ring Lifting Straps** (SKU `OPS-STRAP-DR-01`), one size, sold as a pair. Created 2026-09-29 as a **draft** at A$39.95, 100 in stock at the Upper Coomera location, cost US$5.60 (≈A$8.50 at an assumed 0.66). Copy source: [product.json](../../projects/shopify-store/product.json).
- Margin at $39.95: about $19.50 (49%) if shipping is free, about $29.40 if $9.95 shipping is charged; breakeven on the 100 units is about 45 sales. Not GST-registered (under $75k), so the variant is set non-taxable.
- Compliance: low risk, no known AU mandatory standard for lifting straps; Consumer Law accuracy only. Trademark search for the brand name still to do.

## Open
- Weight is a 250g placeholder: weigh one packed unit.
- Strap material and length unconfirmed, so the copy avoids them.
- No photos yet; the product can't go live without them.
- Shipping rates, Store details address, and a competitor price check.

## Lessons (API)
- The app needs `write_locations` to edit a location; `read_locations` only reads it.
- Admin API `2026-07`: `inventorySetQuantities` no longer takes `ignoreCompareQuantity`; `inventoryAdjustQuantities` requires `changeFromQuantity` on each change and an `@idempotent(key:)` directive. `totalInventory` lags a few seconds after an adjustment.
