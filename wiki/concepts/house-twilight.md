---
type: concept
tags: [twilight, exterior, ai-generation, recipe]
status: locked
updated: 2026-10-20
---

# House twilight (the look we like)

Hunter's locked twilight target, set 2026-10-13. Reference frame: [house-twilight-reference.jpg](../../raw/assets/twilight/house-twilight-reference.jpg) (22-number two-storey front elevation, real dusk shoot). Pass it as the reference image on every twilight conversion.

## The look
- **Early dusk, just after sunset** — not deep blue hour, not night.
- **Sky:** clean, clear gradient — soft mid blue overhead fading to pale cream/peach at the horizon. Almost no cloud. No violet, no pink, no drama.
- **Ground stays bright and readable** — grass and gardens keep natural colour, soft even shadowless light. Never moody or crushed.
- **Glow:** warm amber behind every window and shutter; existing garden/path lights on.
- Only light fixtures that actually exist — no invented pool lights, downlights or new fittings.

**⚠️ Supersedes** the ZED aerial #21 recipe ([[zed-full-house]]) as the default — that one (indigo → violet → amber, pink-underlit clouds) is darker and more dramatic than Hunter wants for ground exteriors.

## Prompt skeleton
Image 1 = this reference (match sky, light, grade exactly). Image 2 = photo to convert (framing + every element unchanged, nothing new built). Then: early dusk sky line, named window/fixture glows, "bright and clearly readable in soft, even, shadowless dusk light, natural greens, high-end twilight real estate photography."

Routing per [[higgsfield-pipelines]]: drone wides → masked sky + post, never full-frame.

## Interior video (day → dusk)
Learned 2026-10-20 on the Extra Salt Pottsville reel ([JOB](../../projects/extra-salt-pottsville-dusk/JOB.md)), via Magnific `video_modify` Seedance 2.5:
- Writing "change to early dusk" only dims the daylight, and Hunter said it looked "too much like a filter, not real dusk". A later ffmpeg brighten pass did not fix that.
- What worked: relight from the room's own fittings. Say all daylight is gone, then describe the existing downlights making warm pools on the floor and scallops down the walls, cool blue spill through the glass, faint warm reflections in the glass, and the warm-inside versus cool-outside contrast.
- Interiors can carry a deeper blue sky than ground exteriors and still read well.
- Seedance needs at least 4s of video, so pad short clips with a frozen last frame and trim back afterwards. At 1080p a 4s clip costs 4,320cr, at 720p 2,080cr.
- Magnific Precision with a 3840 target returned a 2560×1440 file, so we upscaled to 4K locally with lanczos.
