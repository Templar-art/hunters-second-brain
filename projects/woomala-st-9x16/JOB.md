# JOB — Woomala St renders → 9:16

- **Client:** TBC (12-16 Woomala Street development, architect renders)
- **Brief:** 14 landscape renders → 9:16 vertical. Use AI outpaint. Original render must stay untouched (no distortion).
- **Method:** Magnific `images_expand` 9:16, then the original pixels are pasted back 1:1 over the AI frame (`composite.py`) with a 10px seam feather.
- **Status:** test phase

## Log
- 2026-10-06: free side-crops made (`crop-9x16/`). Hunter rejected them; wants AI expansion instead.
- 2026-10-06: test #04 boardroom, ideogram mode with a long prompt, **50 cr**. FAIL: ideogram drew the prompt as text/UI in the new areas. Paste-back worked. Output was only 736px wide.

## Cost tally
| Item | Credits |
|---|---|
| Test #04 ideogram | 50 |
| **Total** | **50** |
