# O'Neill Group — preloader handoff

Intro load screen: charcoal panel, the O'Neill mark draws itself in as an outline,
briefly holds, then fills solid cream. Runs once per browser session.

## Files, in order of where they go

1. **`1-head-script.html`** → paste inside `<head>`, **before** the stylesheet `<link>`.
2. **`2-body-markup.html`** → paste as the very first thing inside `<body>`, above the header/nav.
3. **`3-styles.css`** → merge into the site's main CSS file.
4. **`4-script.js`** → merge into the site's main JS file; `initPreloader()` just needs
   to run on `DOMContentLoaded` (or wherever the site's existing init sequence lives).

## Behaviour

- Shows once per browser session (`sessionStorage`), instant-skip on repeat page loads.
- Respects `prefers-reduced-motion` — skipped entirely for anyone with that OS setting on.
- Self-releases after ~4s even if something stalls — never traps a visitor.
- `~/projects/oneill-group-site/preloader/oneill-preloader.mp4` is a recorded reference
  clip of the animation, if it's easier to just watch it play than read the code.

## Known dependency

The two `stroke-dasharray` values in `3-styles.css` (234 and 3313) are the exact
traced lengths of the two `<path>`s in the mark SVG. If the mark is ever re-exported
from Illustrator/Figma with different path data, these need re-measuring — in any
browser devtools console, on the live page:

```js
[...document.querySelectorAll('.preloader__mark path')].map(p => p.getTotalLength())
```

Getting this wrong doesn't error, it just makes the draw stop short or the outline
sit fully-drawn for a while before the timeline says it's done — the "dead hold"
bug that got fixed during design.

## Brand colours in use

- Charcoal `#2d2d2d` — panel background
- Cream `#d9d2c7` — mark stroke + fill
- Sage `#758670` — loaded as `--og-sage` but not used by the preloader itself;
  available if a future element on this screen needs it.
