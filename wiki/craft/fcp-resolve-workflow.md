---
type: reference
tags: [davinci-resolve, final-cut-pro, color-grading, workflow, post-production]
status: draft-untested
updated: 2026-10-28
---

# Final Cut → DaVinci Resolve Studio → deliver (10x grading workflow)

Hunter cuts in **Final Cut Pro 12.4** and owns **DaVinci Resolve Studio** (stated 28 Oct 2026). Desire Media grades in Resolve, which is a big part of why their colour has more control ([[desire-the-pilot-reference]]). This page is the house workflow for doing the same: **cut, titles and sound stay in Final Cut; only the grade happens in Resolve.**

⚠️ Written 28 Oct from the general [[color-grading]] method plus Resolve round-trip sources (Blackmagic forum, Ripple Training, Larry Jordan). Those sources cover Resolve 17–20; nothing yet confirms the exact menus in Resolve 21. **Run it once on a throwaway job before using it on a client deadline,** and fix this page where the menus differ.

## Which path?

| Your edit has… | Use |
|---|---|
| Speed ramps, motionVFX titles or effects, mixed retimes (most 10x edits) | **Path A: graded master** |
| Straight cuts, little or no retiming, and you want per-clip grading with handles | **Path B: XML round trip** |

Why: in an XML round trip, Resolve renders individual clips **without** the NLE's effects, and users report **speed ramps and reverse playback getting lost**. FCP titles come into Resolve as grey boxes, because they're a proprietary FCP format. Hunter's edits lean on speed ramps and motionVFX titles, so Path A is the safe default.

## Path A: graded master (recommended)
1. **Finish the edit in FCP** (picture lock), including speed ramps.
2. **Disable** titles, supers, logo bugs, captions and any colour effects or LUTs (select, then V). Keep the camera-LUT conversion off too if the footage is log: Resolve will do it.
3. **Export a picture-only master:** File → Share → Master File, video only, **ProRes 422 HQ** (or 4444), source resolution and frame rate. Speed ramps are baked in.
4. **In Resolve:** new project → import the master → **right-click the clip → Scene Cut Detector** (or Timeline → Detect Scene Cuts in newer versions) to split it at every edit, so each shot gets its own grade. Check the cut list against the FCP timeline; it misses dissolves.
5. **Grade** (node tree below).
6. **Deliver:** a single clip in **ProRes 422 HQ**, same resolution and frame rate, no audio.
7. **Back in FCP:** import the graded master, connect it **above** the original at the start (or replace the storyline), re-enable titles on top, and leave all audio (music, your SFX, the [[auto-sound-design]] clips) untouched in FCP.
8. Export the final from FCP as usual.

Trade-off: you grade a baked master, so there are no handles; if the cut changes, re-export the changed section. For 10x's mostly locked, single-delivery films that's fine.

## Path B: XML round trip (no ramps)
1. FCP: select the project → **File → Export XML** (save as `.fcpxml`, not a `.fcpxmld` bundle, which Resolve may not read).
2. Resolve: **File → Import → Timeline** → the .fcpxml, and let it find the media.
3. Grade per clip.
4. Deliver page → render settings → **Final Cut Pro round-trip preset** (Easy Setup), **individual clips**, with handles (e.g. 24 frames), ProRes 422 HQ. That writes graded clips plus an XML.
5. FCP: **File → Import → XML** → the round-trip XML gives a new project pointing at the graded clips. Titles and effects from the original need re-adding or copying across.
6. **Check every retime and transition** against the original before delivery.

## Resolve project settings (once per project)
- **Colour science: DaVinci YRGB Color Managed.** Input: per clip (below). Timeline: DaVinci Wide Gamut / Intermediate. Output: **Rec.709 Gamma 2.4** for TV-style mastering, or **Rec.709-A** when it will mostly be watched on Macs, iPhones and web (it stops QuickTime and Safari washing it out). Pick one per job and stick with it.
- **Input colour space per source:**
  - Sony **S-Log3 / S-Gamut3.Cine**.
  - DJI drone **D-Log M**: use the input preset if your Resolve lists it; otherwise use DJI's free D-Log M → Rec.709 LUT on the first node instead of colour management for those clips. The drone model decides D-Log vs D-Log M (not yet recorded; see [[fcp-plugin-research]]).
  - Already-Rec.709 material (Path A masters exported after an FCP camera LUT): Rec.709 Gamma 2.4.
- Timeline frame rate and resolution are the same as the FCP project.

## Node tree for 10x (keeps Hunter's brightness)
House rule from 28 Oct: **don't darken 10x footage to chase a reference.** The Desire-match LUT read as "just dark". Balance and consistency first; any look stays subtle.

1. **Balance:** white balance on a neutral surface (white wall, ceiling) and exposure. Check whites on the waveform (bright, not clipped) and use the parade to neutralise.
2. **Contrast:** gentle S in Curves; blacks just off the floor (not crushed); pivot around the midtones.
3. **Whites clean-up (qualifier):** select the brightest neutral areas (walls, ceilings, linen) → pull yellow saturation down a little. This is the "white whites, warm timber" move a global LUT can't do.
4. **Timber and skin (qualifier on orange):** protect or lightly enrich warmth here so the wood stays rich while whites go clean.
5. **Sky/water (qualifier or window, tracked):** blue not cyan, a touch of density. Gives the warm/cool separation Desire has.
6. **Saturation:** Hue vs Sat / Sat vs Sat to calm only the over-saturated yellows and greens; don't drop global saturation hard.
7. **Look (optional, last, low key output):** Film Look Creator or a creative LUT at 20–40%.
- **Shot match:** grade a hero shot per space, then right-click other shots → **Shot Match to This Clip** as a starting point, then trim by eye on the scopes.
- Use **groups** for Sony vs drone, so the source-specific balance lives on a group pre-clip and the look on group post-clip.

## Studio-only tools worth using (verify in your version)
- **Magic Mask:** isolate people or objects for lifestyle shots without hand-drawn windows.
- **Noise reduction (temporal + spatial, UltraNR):** low-light interiors, dusk and twilight, AI clips. Replaces buying Neat Video for most jobs ([[fcp-plugin-research]] listed Neat as buy #4).
- **Film Look Creator:** a controlled film look instead of a stock LUT.
- **Relight:** add a soft light to a flat interior after the fact.
- **Super Scale:** clean upscales of 1080p drone or AI clips.

## Sound stays in FCP
Grade-only round trips keep the mix where it is. The [[auto-sound-design]] FCPXML (SFX as separate clips) imports into FCP. Resolve can also read FCPXML, but the round trip with the SFX XML is **untested**.

## Related
[[color-grading]] · [[video-edit-pipeline]] · [[desire-the-pilot-reference]] · [[fcp-plugin-research]] · [[auto-sound-design]]

Sources: [Blackmagic forum: render individual clips](https://forum.blackmagicdesign.com/viewtopic.php?p=63353) · [Blackmagic forum: Resolve ↔ FCPX round trip](https://forum.blackmagicdesign.com/viewtopic.php?p=420713) · [Ripple Training: round-tripping with FCP X](https://rippletraining.com/?p=11850) · [Larry Jordan: round tripping FCP ↔ Resolve](https://larryjordan.com/articles/round-tripping-projects-between-final-cut-pro-and-davinci-resolve/) · [Blackmagic forum: individual clips audio](https://forum.blackmagicdesign.com/viewtopic.php?p=412556)
