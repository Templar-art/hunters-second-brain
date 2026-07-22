# Bespoke International Realty — Full Site Scrape

**Source:** https://bespokeinternationalrealty.com/ (WordPress + Elementor)
**Scraped:** 2026-07-22
**Total:** 222 asset files + 25 HTML pages · 27 MB

---

## Folder map

| Folder | What's in it |
|---|---|
| `brand/logos/` | 3 brand logos (SVG) — main lockup, header, footer |
| `brand/icons/` | 16 UI/spec icons (SVG) — bed/car/shower, menu, arrows |
| `originals/` | 32 full-size photos (no resize suffix) — the clean source images |
| `assets/wp-content/uploads/…` | EVERYTHING, mirrored in the site's real folder structure (all 187 jpgs incl. resize variants, all svgs, 2 videos) |
| `assets/wp-content/…/*.css .js` | 6 stylesheets + 8 scripts (theme + Elementor + plugins) |
| `raw/html/` | All 25 page HTMLs (home, about, services, contact, 8 projects, 11 listings) |
| `raw/` | Sitemaps, media JSON, URL lists used to build the scrape |

---

## Logos (`brand/logos/`)

- **`BESPOKE_FullLogoLockup_Green.svg`** — primary full logo lockup (green)
- **`Top-Logo.svg`** — header logo
- **`Footer-logo.svg`** — footer logo

## Icons (`brand/icons/`)

Property spec: `Bed / Car / Shower` + white variants (`WhiteBed / WhiteCar / WhiteShower`).
Nav/UI: `Menu`, `Menu-close`, `Next`, `Prev`, plus Bespoke-branded menu open/close (green + white).

---

## Brand system (extracted from CSS/HTML)

**Colours**
| Hex | Role |
|---|---|
| `#eceae8` | Off-white / page background (dominant, 534 hits) |
| `#0a2b24` | Deep bottle green — primary brand colour |
| `#1f2f2b` | Dark green-grey — secondary |
| `#ffffff` | White |

*(Remaining hex values are default WordPress/Gutenberg swatches — ignore.)*

**Type:** Montserrat (Google Fonts, full weight range 100–900 + italics).

---

## Media

- **Videos (2):** `Bespoke-Home-Header.mp4` (3 MB, homepage hero) · `BESPOKE_LoadScreen.mp4` (134 KB, load animation)
- **Photos:** 32 originals → 187 total incl. WordPress-generated resize variants (`-300x200`, `-768x…`, `-1024x…`, `-1536x…`, `-150x150`)

Key photo sets: Aalto, Coastal Collection, De Luxe, Blue Mirage Fiji, Rockpool, Shellhaven, Sovereign, Uniq (project heroes); Garfield Terrace CG renders; agent portraits (Jason & Barbara Ward); Versace shoot; about/services/contact headers.

---

## Contact / social (from site)

- **Email:** info@bespokerealestate.com.au
- **Phone:** 0422 228 229 · 0424 731 063 · 1300 111 111
- **Instagram:** [@bespoke.international](https://www.instagram.com/bespoke.international)
- **Facebook:** [bespokeinternationalrealty](https://www.facebook.com/bespokeinternationalrealty)
- **LinkedIn:** [bespoke-international-realty](https://www.linkedin.com/company/bespoke-international-realty)
- **Built by:** Desire Studio (desirestudio.com.au)

---

## Pages scraped (25)

Home · About · Services · Contact · Current projects
Projects: Aalto Surfers Paradise · Coastal Collection · De Luxe · Radisson Blu Mirage Resort Fiji · Rockpool Rainbow Bay · Shellhaven · The Sovereign Collection · Uniq Residences
Listings: 71/3 King Arthurs Court Sovereign Island · Aalto Full Floor / Penthouse / Sub-Penthouse · De Luxe Penthouse / Sub-Penthouse · Coming Soon 1 & 2 · Buy/Lease/Sold status pages

---

## Notes

- Full media library confirmed complete via WP REST (`/wp-json/wp/v2/media`, 62 library items → all resize variants pulled). Nothing left on the server unreferenced.
- A few outbound links point to separate project microsites (rockpoolrainbowbay.com.au, uniqbundall.com.au, thesovereigncollection.com.au) — those are external sites, not assets of this one, so not downloaded. Say the word and I'll scrape those too.
- Assets are the client/site's own copyrighted material — pulled here for reference/dev use.
