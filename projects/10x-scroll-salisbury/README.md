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

## v3 engine: cross-blend + camera-fly rig (14 Jul 2026)
Two upgrades, both free/local (no new credits):
- **Sub-frame cross-blend** — the canvas now draws `floor(f)` solid + `ceil(f)` at the
  fractional weight every rAF, so the scrub interpolates continuously instead of stepping
  to the nearest frame. This is the "60fps / time-interpolation" smoothness in software —
  and it's safer than ffmpeg `minterpolate` on this footage, because optical-flow interp
  warps on build-morph content (bricks/trusses appearing aren't real motion). Frames
  re-extracted at 15fps/1280px (303 frames) — density × blend reads buttery.
- **Camera rig** — scroll-driven `scale`+`translate` keyframes on the canvas (GPU transform):
  dive onto the slab (1.30) → pull back as it tops out (1.05) → dive into the brick (1.32) →
  rise for the shell (1.07) → punch toward the glowing entry (1.36) → settle on reveal (1.03).
  In-and-out rhythm layered over the footage. Scale floor 1.03 = no edge gaps.

### Ceiling / next step (PAID — needs Hunter go-ahead)
The camera fly is a 2D digital move on flat footage — reads as movement, but it's not true
3D parallax. Real drone-swoop / orbit / crane "flying" only comes from regenerating the
Seedance clips WITH camera motion (Seedance 2.0 supports fpvDrone, craneUp/Down, orbitLeft/
Right, superDollyIn/Out, 360Orbit). Cost to redo the 4 build clips with camera moves:
~3,500 cr each on 2.0 Pro (~14,000 total) or ~700 cr each on 2.0 Mini 720p (~2,800 total).
Recommend Mini first as a look-test before committing Pro credits.

## Camera-move look-test (14 Jul 2026, Seedance 2.0 Mini 720p, 4×700=2,800 cr)
Tested 4 signature moves on the finished house (camtests/): orbit / super-dolly-in / crane-up / fpv-drone.
Verdict: ORBIT best (faithful + real 3D parallax) · DOLLY-IN strong (lands inside on the staircase) ·
CRANE-UP good reveal · FPV drifted (hallucinated a wide street + tree) → drop.
Next: commit winner(s) to Seedance 2.0 Pro 1080p for the final page. Concept options —
(A) single hero move on the finished house (simplest, instantly replicable per niche), or
(B) regenerate the 4 build stages on Pro WITH camera moves (richest, geometry-continuity risk).

## v4 LIVE — cinematic fly-story (14 Jul 2026, FINAL)
Replaced the build-timelapse with a genuine 3D camera journey the user asked for:
**reveal → orbit → step inside**, 15.2s, 304 frames. Three Seedance 2.0 Pro 1080p clips
(~10,500 cr) chained seamlessly by keyframing each clip's START on the previous clip's
END frame (extracted via ffmpeg `-sseof`):
1. **Reveal** — pullOut from the glowing entry to the full dusk facade framed by trees.
2. **Orbit** — orbitLeft around the house, real foreground-tree parallax.
3. **Step inside** — superDollyIn straight through the front door, landing in the timber
   staircase foyer. The payoff: the scroll literally walks the buyer into the home.
Engine: 2D camera rig retired (footage now carries the motion); cross-blend interpolation
kept for scrub smoothness. Captions: The reveal. / Every angle. / Step inside.
Full film saved as `fly_full.mp4` (usable as a hero reel). Prior build clips + Mini camera
tests kept in flystory/ + camtests/ (all git-ignored).
Per-niche recipe unchanged: same 3-move chain, swap the property photo + the interior payoff.

## v5 LIVE — full aerial build + fly (14 Jul 2026, FINAL)
The complete story the user asked for: **aerial dirt → slab (builders) → frame → finished
house → reveal → orbit → step inside.** 30.4s, 365 frames, 6 Seedance 2.0 Pro 1080p clips
chained by end→start keyframes:
1. Aerial descent onto the graded lot; concrete slab pours into the pegged footprint, two
   distant hi-vis workers (craneDown). Start still = Nano Banana aerial-dirt render.
2. Descent continues; timber frame rises from the slab (craneDown).
3. Frame → brick → roof → dusk finished house. END-KEYFRAMED to the real finished photo,
   which RE-ANCHORS fidelity after build-morph drift and joins seamlessly into...
4–6. the earlier fly clips (reveal pull-out / orbit / dolly-in through the door), reused
   because clip 3 ends exactly where clip 4 starts (the real photo) — saved ~7,000 cr.
Captions: The site / Framed / Built / The reveal / Every angle / Step inside.
Cost this pass: 2 aerial-dirt stills ~150 cr + 3 Pro clips 10,500 cr (orbit/reveal/inside reused).
Engine unchanged (cross-blend interpolation, 2D rig off). Full film: fly_full.mp4.
Per-niche recipe: swap the property photo + interior payoff; the 6-beat chain is the template.

---
_Vault: [[10x-scroll-build]]_
