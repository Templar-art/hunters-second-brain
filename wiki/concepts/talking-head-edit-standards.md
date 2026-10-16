---
type: concept
tags: [video-editing, motion-graphics, remotion, client-feedback, standing-rules]
status: active
updated: 2026-10-16
---
# Talking-head edit standards (client feedback)

> Context: built for Hunter's personal side work (fitness coach edits, e.g. Tyson's intro reel). Separate from 10x Visuals.

Standing rules for short-form talking-head / explainer edits — including the AI/Remotion pipeline in `projects/remotion-pipeline/`. Every new edit gets checked against this list before it goes to the client.

## Client feedback — 16 Oct 2026
> "I think the cuts need to be more on point so it's flowing, could have some light music on, sound effect and even some image overlay if needed. AI is solid but I would personally be going over each video as well. I'll send through our last one."

### What that means in practice
1. **Tighter cuts / flow.** Cut out dead air, breaths, false starts and pauses between phrases (e.g. the gaps at ~5.7s and ~15.5s in IMG_9573). Cut on the beat of the speech so it never sags. Use punch-ins (zoom in/out) to hide jump cuts.
2. **Light music bed.** Always put a low music bed under the voice, ducked well below the dialogue. Pick it from [[music-taxonomy]].
3. **Sound effects.** Every graphic entrance, wipe, pop and click gets an SFX (whoosh, pop, click, riser). Use the [[sfx-library]] (Ocular Sounds).
4. **Image overlays where they help.** B-roll or photo overlays (gym, food, the client's own content) when the speech names something visual, not just text cards.
5. **Human pass on every video.** AI output is a first draft, never the delivery. Hunter watches every edit end to end before it goes out.
6. **Reference first.** Before starting the next job, look at the client's last delivered video (they are sending it) and match its pace and feel.

## Applies to
- Tyson fitness intro (IMG_9573 + IMG_9577) — Remotion explainer edit, 16 Oct 2026. First cut had no music, no SFX, no dead-air trimming. Fix these in v2.

See also: [[sfx-library]] · [[music-taxonomy]] · [[typography]]

## Hunter's notes — 16 Oct 2026 (v2 of the Tyson edit)
- **Captions sit at chest height**, around the middle of the frame (y ≈ 1180 of 1920), not down at the bottom. Keep them subtle: smaller text with a soft shadow, not big and heavy.
- **Graphics need time.** Slow, gentle easing in and out (iris wipes ~0.9s in / 0.8s out, soft springs, staggered card entrances). Hold each scene long enough to read. No fast pop-and-vanish.
- Keep name tags and CTA cards in the top third so they never clash with the captions.
- **No branded end card.** End on the speaker's last line or CTA ("I'll see you in the next one" / the follow CTA) with the music fading out. An end card adds nothing for coach and fitness reels (Hunter, 16 Oct 2026).
- **No light leaks.** The orange flare looked off-brand. The lime/charcoal palette was liked (Hunter, 16 Oct 2026).
- **Scripts first.** Push for value-first openers. The edit can't fix a generic script (see [[hormozi-style-motion-playbook]]).
- **No dark gradient bars behind titles.** The top-of-frame gradient read as a black bar. Use text-shadow instead (Hunter, 16 Oct 2026).
- **Pop-ups must linger.** Exits ~0.6s with ease, not 0.25s. Hold them long enough to read (Hunter, 16 Oct 2026).
- **Export quality — no generation loss.** Render once at high quality and never re-encode the video afterwards: Remotion `--jpeg-quality=100 --crf=14 --x264-preset=slow`, then loudness on the audio only (`-c:v copy`). Keep grain subtle (~6% opacity), since heavy grain eats bitrate and Instagram re-compresses it to mush. Cap punch-ins around 1.08× on 1080p sources. v7 had dropped to ~4.8 Mbps through a "phone-friendly" crf 21 re-encode plus Remotion's default JPEG-80 frames (Hunter flagged it, 16 Oct 2026).
