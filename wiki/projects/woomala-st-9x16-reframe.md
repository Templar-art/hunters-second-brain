---
type: project
tags: [project, renders, ai-outpaint, nano-banana-pro, 9x16]
status: delivered
updated: 2026-10-06
---

# Woomala St renders → 9:16 (Oct 2026)

14 landscape marketing images for the 12-16 Woomala Street tower (13 architect renders plus one real level-7 drone photo) reframed to 9:16 vertical for Reels and Stories. Client not yet recorded. Job folder: [projects/woomala-st-9x16/](../../projects/woomala-st-9x16/JOB.md), deliverables in `deliver/` (1080×1920).

**Hard brief:** the AI has to add the missing top and bottom, and the original render must not change at all.

## What worked
1. Strip the gallery's navy letterbox bars.
2. **Pad each original onto a 9:16 grey canvas myself**, full width, positioned where I want it.
3. Higgsfield **Nano Banana Pro** (`nano_banana_2`, 4k, 9:16, 4 cr), with the padded canvas as the image ref. The prose prompt names everything in the render and says what fills each grey band (ceiling and downlights, floorboards, sky, street).
4. **Paste the original back 1:1** over the AI frame (`composite.py` auto-aligns, 16–70px seam feather). Every original pixel survives, and the AI only owns the new bands.
5. Real photo (#01): anchor it to the **bottom** edge so the AI only adds sky. A bottom seam through real rooftops can't be blended.

## Realism pass (Hunter: "needs realism passes like sun")
- Run on the finished 9:16 composite, whole frame. **Nano Banana Pro 4k with edit-style wording** ("Edit this image into a real photograph. Keep the exact same composition… change only the realism and light") held the layout on 13/13. Pin window views "crisp, clear, not hazy, not blown out", or NBP washes them out.
- **Seedream 4.5 fails here:** given a scene description, it re-composed the boardroom with a new angle and a different table.
- #11 feedback: the AI-built tower was too short. Prompt the building to run off the top of the frame with no roofline.

## What failed
- **Magnific `images_expand` (Ideogram mode), 50 cr:** it treated the long prompt as text to draw and filled the new bands with fake UI and gibberish. Classic mode is 10 cr but untested.
- **NBP with the raw landscape ref + 9:16:** reframed or zoomed 6 of 13 renders (the street entry became a shot of the upper floors), so paste-back couldn't line up. Pre-padding fixed it 8/8.
- **Free centre crops:** Hunter rejected them. He wants the full render kept and extended, not trimmed.
- **Tone-matching a bad seam** (#03 paving) didn't fix a stone-scale mismatch; a padded re-roll did.

## Cost
149 Higgsfield cr (reframe 88, #11 redo 4, realism tests 5, realism batch 52) + 50 Magnific cr (wasted). Working method: ~4 cr per image to reframe + 4 cr for the realism pass.

## Related
[[higgsfield-pipelines]] · [[cva-architects]] (same render-enhance family) · [[10x-scroll-build]] (Salisbury NBP stills)
