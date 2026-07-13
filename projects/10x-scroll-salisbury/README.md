# Salisbury Building Projects — Scroll-the-Build Demo

Scroll-scrub page in Salisbury's brand voice (near-black, heavy condensed caps like
their wordmark, one amber accent pulled from the twilight windows). Scrolling scrubs
a push-in on 120 Kennedys Lane frame-by-frame, forward and back.

**Run it:** `python3 -m http.server 8765` in this folder → http://localhost:8765
(a server is needed — `file://` blocks the frame fetches).

## The pipeline (this is the repeatable part)

1. **Source still** → pick the hero frame (here: `120 Kennedys Lane-17.jpg`, front facade,
   from `10x Library/_drive_intake/Salisbury Building Projects/kennedys_photos/`).
2. **Motion** — two options:
   - **Stand-in (free, what's in here now):** ffmpeg Ken Burns push-in on the still —
     ```
     ffmpeg -y -loop 1 -i SRC.jpg -vf "scale=6912:-2,zoompan=z='1+0.20*on/240':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=240:s=1728x1152:fps=24" -t 10 -pix_fmt yuv420p standin.mp4
     ```
   - **Real cinematic (Seedance, credits):** run the prompt in SEEDANCE-PROMPT.md in
     Higgsfield with the same still attached as @image1 — true parallax, warming windows,
     moving foliage. 10s.
3. **Frames** — `ffmpeg -i VIDEO.mp4 -vf "fps=12" -q:v 3 "frames/f_%04d.jpg"` → 120 frames.
   If the count changes, update `FRAME_COUNT` in index.html.
4. **Page** — index.html scrubs the frames on scroll (canvas + ImageBitmap + lerp; direct
   snap fallback for embedded/throttled contexts). Rebrand per client: the CSS vars at the
   top (`--ink/--bone/--amber`) + the two font families + header/captions.

## Swapping in the Seedance render
Replace `standin.mp4` with the Seedance output, rerun step 3, done — same frame names.

## Usage
Demo asset for selling scroll-driven builds to Salisbury (and the template for any client).
Photo is 10x's own delivery to Salisbury; clear it with Murph before the page goes public.

## LIVE: Seedance 2.0 render (14 Jul 2026)
`seedance_render.mp4` (5s, 1080p, 3,500 credits) now drives the page — 121 frames at 24fps.
The ffmpeg stand-in is kept at `_standin_backup.mp4`. Concept: **"the house comes alive"** —
push-in + dusk deepening + windows igniting room by room. All three changes are monotonic,
so the scrub reads perfectly in both directions.

## Replicating per niche (the product)
Same recipe, one variable — what "comes alive" means for the client:
- **Builder** (this demo): lights ignite room by room as you approach — the handover moment.
- **Developer:** slow aerial rise from street to masterplan view, stage lighting coming on.
- **RE agency:** twilight glamour push toward the pool/entry, water lights blooming.
- **Architect:** light study — sun sweeping across the facade, shadows walking the brick.
Prompt template: SEEDANCE-PROMPT.md structure; swap Scene & Mood + Movement's "ignition"
layer. One 5s 1080p Seedance 2.0 Pro clip per site (3,500 cr) or run it in the Higgsfield
web app on the plan. Then: frames at fps=24 → index.html (FRAME_COUNT + brand vars).

## v2 LIVE: "Built before your eyes" (14 Jul 2026)
The scroll now plays the FULL BUILD — 20s, 323 frames, four chained Seedance 2.0 Pro clips:
slab → timber frame → brickwork → roof/glass/gardens/dusk → the original lights-on push-in
as the finale. Chaining trick: 3 construction-stage stills generated with Nano Banana Pro
from the real finished photo (exact geometry held), then each clip keyframed start→end on
consecutive stills so the joins are seamless. Stage captions (FRAME. / BRICK. / ROOF. / HOME.)
fade per scroll band. Cost: 3 stills ~300 cr + 3 clips 10,500 cr (+3,500 for v1's dusk clip).
Full film also saved as `build_full.mp4` (usable as a reel/timelapse asset on socials).
