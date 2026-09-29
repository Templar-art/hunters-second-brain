---
type: project
tags: [shopify, ecommerce, white-label]
status: setup
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

## Open
- Shop location has no street address (needed for shipping rates).
- Product, unit cost, brand, weight and dimensions not yet given.
- AU compliance depends on product category (TGA, RCM, ACCC mandatory safety standards).
