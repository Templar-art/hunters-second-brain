---
client: kollosche
address: 4-6 Buckingham Way, Elanora
opened: 2026-11-02
status: review            # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 0, aud: 0 }   # derived from ## Ledger — never edit by hand
---

# Job — 4-6 Buckingham Way, Elanora (Kollosche, Taylor Kleinberg)

Source: `/Volumes/10X SSD1/4-6 Buckingham Way Elanorra /Edits/Main.mp4` (Hunter's finished edit, 63.5 s, 1920×1080 23.976, AAC). Never modified; deliverables are written beside it.
Brief: "everything done to it" = Kollosche K badge pin + white tracked lot outline, CG gulls, start/end cards. 16:9. No sky, dusk or grade.

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 0 | Opener 0–6 s | KOLLOSCHE 4K wordmark frames 0–71 (fade out 62–71) → address super "4-6 BUCKINGHAM WAY / ELANORA" 72–143, Söhne Breit Kräftig cap 47 px@4K, 8% tracking | review | ⚠️ address sits over a white eave at ~4.5 s, "BUCKINGHAM" washes slightly; Hunter can retime in FCP |
| 1 | Top-down pull-up 31.2–34.2 s (src 748–819) | chained SIFT homographies (plate-vfx solve FAILED: speed-ramp whip), white outline draws on f38–51 | review | 0.16–0.24 px/frame. Lot traced by eye from the frame (front at kerb, N fence past side drive, tennis court, S hedge), not from a plan |
| 2 | View wide 34.2–36.2 s (820–867) | plate-vfx PASS 0.477 px; K badge pin via KLT roof track; 4 gulls standard | review | birds plate-untouched PASS |
| 3 | Final pull-out 57.7–63.5 s (1383–1521) | pin f1–36 (KLT, fades out into the whip at f29–36); gulls on settled wide f71–139 | review | wide solve 1.27 px (fails 0.5 gate: hillside parallax) — accepted for airborne birds only; plate-untouched PASS |
| 4 | Outro 61.0 s → end (1463–1521) | make_outro.py TAYLOR KLEINBERG / 0447 466 177, 15-frame fade in | review | birds of shot 3 run under the 50% navy overlay |

## Log

- 2026-11-02 intake: 35-shot edit, 6 drone shots. Contact sheet at `contact/sheet.jpg`. Scope from Hunter: pin + outline, birds, cards, 16:9. Agent: Taylor Kleinberg 0447 466 177.
- 2026-11-02 Hunter: "just make the overlay and i can do it on fcp" → deliverable switched from finished comp to full-length alpha overlays.
- 2026-11-02 built: `scripts/graphics.py` (outline + pins), plate-vfx birds (view, pullout_wide), `scripts/assemble.py` → 5 ProRes 4444 alpha overlays, 1522 frames / 63.48 s each, all start at 00:00 over Main.mp4, + preview MP4. Copied to `/Volumes/10X SSD1/4-6 Buckingham Way Elanorra /Edits/Kollosche Overlays/` (original Main.mp4 untouched), revealed in Finder. Sent for review. $0, all local.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- no spend: all local -->

---
_Vault: [[jarvis]]_
