# IG listing post templates

5 square (1080x1080) listing post templates, one HTML file each. Boutique, hero-photo-first, agent's own logo — no 10x branding.

- `coming-soon.html`
- `just-listed.html`
- `just-sold.html`
- `sold-off-market.html`
- `open-home-times.html`

Shared look lives in `styles.css` — one skeleton across all 5: full-bleed hero photo, soft navy gradient scrim at the bottom, kicker + address headline, agent logo bottom-right. Headline font is Bodoni Moda, body/kicker is Nunito Sans (closest free stand-ins for BW Vivant / Circular Std — swap the `@import` and `font-family` values in `styles.css` if the real font files ever get bought/installed).

## Per-listing swap (no code knowledge needed)

Open the relevant `.html` file in a text editor and change three things:

1. **Hero photo** — in the `<div class="hero hero--placeholder">` line, delete `hero--placeholder` and add a background image instead:
   ```html
   <div class="hero" style="background-image: url('path/to/photo.jpg')">
   ```
2. **Address / copy** — edit the text inside `.headline`, `.subtext` (and the two `.slot` lines on the open home template).
3. **Agent logo** — replace `assets/logo-placeholder.svg` with the agent's white logo file (icon or long-form, transparent background) and update the `src` in `.logo-slot img`.

Then open the file in a browser at 1080x1080 and export/screenshot as a PNG (or use `serve.mjs`, see below), ready to post.

## Preview / export

```bash
node serve.mjs        # serves this folder on http://localhost:8774
```
Then open `http://localhost:8774/<template>.html`, or render straight to PNG headlessly:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --force-device-scale-factor=1 --window-size=1080,1080 \
  --screenshot="preview/coming-soon.png" "http://localhost:8774/coming-soon.html"
```

`preview/` has one rendered example of each template with placeholder copy.

## Note on Canva

Originally scoped as Canva Brand Templates, but Canva's MCP connector can't do a native 1:1 square design, can't reposition elements precisely, and can't tag Autofill fields — all of that needs the Canva web editor by hand. Built as plain HTML/CSS instead: same swap-and-post workflow, full control over the layout.
