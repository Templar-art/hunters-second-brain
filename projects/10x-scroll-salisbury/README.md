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
