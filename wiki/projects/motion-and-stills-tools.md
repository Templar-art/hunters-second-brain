---
type: project
tags: [motion, tooling, internal]
updated: 2026-10-19
---

# Motion + stills tooling (small builds)

Small, reusable scripts built during jobs that never got their own pages. Each one is code-driven (Python + HTML/canvas), so it can be re-run instead of rebuilt.

- **10x logo sting** ([projects/10x-logo-sting](../../projects/10x-logo-sting/)) — renders the 10X symbol and the full "10X VISUALS" wordmark to transparent RGBA frames, with geometry pulled straight from the brand SVGs. The X chevrons converge, the "10" glides in, "VISUALS" closes its tracking, and the glow blooms once. Frames are stored **premultiplied** because straight-alpha glows blow out to white blobs in compositors. See [[brand-system]].
- **HIA awards title card** ([projects/hia-awards-title](../../projects/hia-awards-title/)) — animated title for the 2026 HIA Gold Coast & Northern Rivers Housing Awards, in three modes: green field, "punch" (type cut out as alpha holes so footage plays inside the letters in FCP), and alpha-only for comping.
- **Motion SFX test** ([projects/motion-sfx](../../projects/motion-sfx/)) — canvas motion-graphics scenes plus synthesised whooshes/booms (numpy) rendered to mp4, 9 Oct. Synth SFX were judged poor, so real libraries were used afterwards (Magnific SFX, Ocular Sounds — see [[use-definitions-series]]). A better-designed synth option, [[sound-lab]], was added 19 Oct 2026 and hasn't been tested in an edit yet.
- **White border** ([projects/white-border](../../projects/white-border/)) — puts a white mat around stills for IG grids. The margin is computed off the long edge so it looks even, and the canvas locks to one aspect so mixed portrait/landscape carousels read as one grid. First used for [[salt-pm]] Kingscliff (24 Aug).
