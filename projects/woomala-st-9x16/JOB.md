# JOB — Woomala St renders → 9:16

- **Client:** TBC (12-16 Woomala Street development, architect renders)
- **Brief:** 14 landscape renders → 9:16 vertical. Use AI outpaint. Original render must stay untouched (no distortion).
- **Method:** Higgsfield Nano Banana Pro (`nano_banana_2`, 4k, 9:16, render as image ref, prompt names every element + what continues above/below). Then the original pixels are pasted back 1:1 over the AI frame (`composite.py`) with a 10px seam feather.
- **Status:** DELIVERED 2026-10-06

## Log
- 2026-10-06: free side-crops made (`crop-9x16/`). Hunter rejected them; wants AI expansion instead.
- 2026-10-06: test #04 boardroom, ideogram mode with a long prompt, **50 cr**. FAIL: ideogram drew the prompt as text/UI in the new areas. Paste-back worked. Output was only 736px wide.

- 2026-10-06: Higgsfield CLI updated 0.2.1 → 1.1.26, logged in (marketing@ account, Ultra, 830 cr), skills synced.
- 2026-10-06: test #04 boardroom on Nano Banana Pro 4k, **4 cr**. PASS: clean ceiling + oak floor, paste-back has no visible seam.
- 2026-10-06: batch of 12 (#02-03, #05-14) launched, ~48 cr. #01 is a real drone photo, so it stays a plain crop (no AI).

## Cost tally
| Item | Credits |
|---|---|
| Test #04 ideogram | 50 |
| Test #04 Nano Banana Pro (Higgsfield) | 4 |
| Batch 12 × NBP 4k (Higgsfield) | 48 |
| Re-roll 7 × NBP 4k padded | 28 |
| Re-roll #01 bottom-anchored | 4 |
| Re-roll #03 padded (seam fix) | 4 |
| **Total** | **50 Magnific + 88 Higgsfield** |

## Batch result (2026-10-06)
- PASS (original pasted back 1:1, seams clean): #03 #04 #06 #07 #12 #13 #14 → `deliver/`. #01 is a plain crop with the caption re-set.
- FAIL, model reframed/zoomed the render so paste-back can't line up: #02 #05 #08 #09 #10 #11. Fix: pad the original onto a 9:16 grey canvas myself, then NBP fills only the grey bands (~24 cr for 6). Hunter: "keep trying" + #01 crop rejected ("very wrong").
- 2026-10-06: re-roll on grey-padded 9:16 canvases (original placed by me, NBP fills only the bands): #01 #02 #05 #08 #09 #10 #11, 28 cr. All aligned full width. #10 needed a 60px seam blend. #01 seam broke on rooftops → re-rolled with the photo bottom-anchored (sky-only fill), 4 cr, 90px sky blend.
- 2026-10-06: ALL 14 delivered in `deliver/` (1080×1920). Contact sheet: `contact-sheet-final.jpg`.

**Lesson:** NBP with a raw landscape ref + 9:16 reframes/zooms ~half the time. Pre-padding the ref onto a 9:16 grey canvas locks position (7/7). For real photos, anchor the photo to a frame edge so the AI only fills sky.
- 2026-10-06: #03 bottom seam showed a paving scale/tone line → re-rolled on padded canvas, 4 cr, clean. Heavy intermediates (nbp/, nbp2/, clean/, padded/, final/) git-ignored; deliver/ is the source of truth.
