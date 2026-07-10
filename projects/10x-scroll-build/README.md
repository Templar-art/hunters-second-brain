# 10x Scroll-Driven Film — demo

A self-contained scroll-scrub page: as you scroll, a real render plays frame-by-frame
(forward and back). Open `index.html` in any browser. No build step, no server needed
for the effect itself (though a local server avoids browser file:// image caching quirks).

Used as a 10x Visuals sales/portfolio piece to sell scroll-driven experiences.

## Frames (not in git)

The `frames/` folder holds the extracted render frames and is **git-ignored** — the source
render belongs to CVA Architects, and the frames are large. Regenerate them from the render
video with ffmpeg (free, local, no credits):

```bash
cd "10x Scroll Build"
mkdir -p frames
ffmpeg -i "/path/to/CVA Render Video.mp4" -vf "fps=4,scale=1728:-2" -q:v 3 "frames/f_%04d.jpg"
```

This produces ~164 frames named `f_0001.jpg …`. If the frame count changes, update
`FRAME_COUNT` at the top of the `<script>` in `index.html`.

## Swapping in a different render

1. Extract frames from the new video with the command above.
2. Set `FRAME_COUNT` in `index.html` to the number of frames produced.
3. Adjust the caption copy / `range()` fade windows in `render()` if the story changes.

## Credit / usage

Render: **CVA Architects**. Scroll experience: **10x Visuals**. Fine for one-to-one sales
demos. Before posting publicly, genericise or get CVA's OK on reusing their render.
