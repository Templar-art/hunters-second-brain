# 10x Visuals homepage, Prestige rebuild

Static rebuild of the `10xvisuals.com.au` homepage against Prestige Design System v1.0, amended for WCAG AA. One self-contained `index.html` plus `assets/`. Works over `file://` and HTTP.

- **Spec + build outcome:** [2026-07-30-10x-homepage-prestige-rebuild-design.md](../../docs/superpowers/specs/2026-07-30-10x-homepage-prestige-rebuild-design.md)
- **Design system of record:** [DESIGN.md](../../DESIGN.md), the Prestige layer section
- **Wiki:** [[10x-website]]

## Run it

```bash
python3 -m http.server 8791 --directory "projects/10x-site"
```

Then open `http://localhost:8791`. Opening `index.html` directly also works; assets are all relative.

## Before this goes live

1. Set `FORM_ENDPOINT` at the top of the script block to a real POST endpoint. While it is `null` the form opens a `mailto:` compose to hello@10xvisuals.com.au, so enquiries still arrive but nothing is captured server-side.
2. Replace the founders photograph. The current frame is a studio-seamless team shot, greyscaled and cropped as a holding treatment.
3. Decide on the client strip. It is currently a typeset Prata roster of sixteen clients. Logos return only with a matched monochrome set on transparent grounds.
4. **Stonehaven has no project page.** It is the hero and the opening case study, but `10xvisuals.com.au` has no `/stonehaven` route, so that entry is deliberately not a link and carries no "View project" CTA. Build the page, then make it one.

## Assets

Every image ships as **WebP plus a JPEG fallback, at three or four widths**, wired up through `<picture>` with `srcset` and `sizes`. Measured cold-cache transfer: **0.98MB at 1440px, 0.34MB at 390px**, down from 4.34MB when a single full-size JPEG was served to everyone. The hero is preloaded with a responsive `imagesrcset`.

**The full-size masters are not in this folder.** They were removed because an unreferenced 4.34MB would ship with a static deploy. The masters live in `~/Downloads` (the 47 Somerset Drive prints) and on the live WordPress uploads. To regenerate the variant set from a master, per image:

```bash
# widths 800 / 1400 / 1800 / native, WebP from each JPEG
sips -Z 1400 -s format jpeg -s formatOptions 68 master.jpg --out name-1400.jpg
cwebp -quiet -q 72 -m 5 name-1400.jpg -o name-1400.webp
```

`assets/manifest.json` records the widths generated for each image; keep it in step with the `srcset` values in `index.html`.

To re-fetch the client logo files that were removed:

```bash
B=https://10xvisuals.com.au/wp-content/uploads; mkdir -p projects/10x-site/assets/logos; for f in The-Agency-REA Shape-Construction Ray-White-Rea Salisbury-Building-Projects-Logo PRD-Rea Mastr-Logo Kollosche Gold-Coast-BMW-Logo Ashley-Cooper-Construction-Logo; do curl -sfL "$B/2026/03/10x-Visuals-Web-Logos_$f.jpg" -o "projects/10x-site/assets/logos/$f.jpg"; done
```

## Work order

Six entries: Stonehaven (full bleed), Davenport and Bespoke (two up), Elysium (full bleed), then SOL and Broncos Leagues Club (two up). SOL sits below Elysium by request; it used to be the hero.

The hero is Stonehaven at 47 Somerset Drive, marketed by Whitefox, shot at dusk. It replaced the SOL drone frame because that shot's lower third is a bright white roof, so the headline sat on the subject with almost no contrast. Stonehaven's foreground lawn and paving are genuinely dark, which is what the DS scrim expects.

## Scope

Homepage only. The other five pages (`/branding`, `/content-creation`, `/lead-generation`, `/systems-processes`, `/contact-us`) are untouched and will visibly clash with this one until they get the same treatment.
