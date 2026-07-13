# Design

Visual system for 10x Visuals own-brand social graphics (the "Premium Kit" system, Hunter-approved 7–9 Jul 2026). Not a web app — rendered via PIL in `~/Desktop/General Folder/10x Premium Kit/`.

## Theme

Cinematic film-title cards over 10x's own footage frames. The photograph is the design; type is quiet, tracked, white. No tiles, no bands, no boxes, no body copy on the grid.

## Color

- White type only on imagery: `#ffffff`
- Shadow ink: `#050c14` (soft wide drop shadow, blur ~9px @1x, alpha ~150)
- Navy `#102f41` — dim tint for highlight covers (16% blend, brightness ×0.62) and the legibility scrim hue; never a flat tile colour on the grid
- Brand blue `#61a8d8` + kicker blue `#8ec6e8` — reserved for ads/utility surfaces, not grid cards
- Scrim: "whisper gradient" — black bottom gradient, quadratic falloff; peak alpha adapts to frame brightness (~165 base → up to 235 on bright interiors)

## Typography

- **Poppins Light** — titles, all-caps, wide tracking (~9–16px @1x), auto-shrink to fit width
- **Poppins SemiBold** — kickers, all-caps, small (~19–21px @1x), wide tracking
- Kicker grammar is a named brand system: "A 10X VISUALS FILM" / "CRAFT · NO 01" / "10X VISUALS · PHOTOGRAPHY" / "VIRTUAL STAGING" / "THE PROCESS"
- Titles end with a full stop: "THE BOWSPRIT." (film-title voice)
- **No dashes anywhere in copy** — middots `·` and slashes `/` only
- Montserrat = body font for non-grid collateral only

## Formats

| Format | Size | Layout |
|---|---|---|
| Project card | 1080×1350 | kicker + title lower-left, gradient 0.42 span |
| Craft card | 1080×1350 | series kicker + title centred, placed in sky/negative space |
| Recap card | 1080×1350 | huge month word centred ("JULY."), "THE MONTH THROUGH OUR LENS" |
| Hero | 1080×1350 | pure photo, zero type (The Local Project pattern) |
| Story frame | 1080×1920 | same grammar; safe zones top 170px / bottom 280px |
| Highlight cover | 1080×1080 | photo dimmed ×0.62 + 16% navy, white 10X mark centred at 34% height (per boss: white mark, NOT engraved-material) |

## Logos

Real files only, never text wordmarks — see auto-memory `reference-brand-assets`. White 10X mark baked at `10x Premium Kit/_assets/10x_mark_white.png`. Only white logos exist; dark export pending from designer.

## Imagery rules

- Source: `10x Library/_Selected` (55 curated keepers) + project folders; picked from eyeballed contact sheets, never filenames
- No third-party branding/map pins/sold signs/watermarks in frames
- Never re-post already-published media — check the live feed first
- One property per highlight cover; vary properties across a posting run (no 3 near-identical sunsets in one pack)
