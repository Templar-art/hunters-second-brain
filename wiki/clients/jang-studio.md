---
type: contact
tags: [vendor, photo-editing, competitor-intel]
updated: 2026-08-19
---

# Jang Studio (vendor / industry contact)

Vietnam-based offshore architectural photo editor — likely the editor behind NIRA Creative's output; also followed by AC Media (the aspirational benchmark in [[10x-ig-repositioning]]).

- Web: jang.studio · WhatsApp + IG contacts in auto-memory `reference-jang-architectural-editor.md`
- Relevance: potential outsource option for volume photo editing, and a window into what the premium AU real-estate media accounts use.

## Suspected technique — fake flambient via 3D relight
Per Lachlan (2026-08-19): Jang's VIP tier (24-48hr turnaround, vs 8-12hr standard) likely fakes the flambient look instead of shooting real flash brackets:
1. Depth map off single photo (MiDaS/Depth-Anything or Photoshop depth blur export).
2. Project photo as texture onto a displaced 3D mesh (Blender) built from that depth map.
3. Place virtual point lights at flash positions in 3D, render a lighting/specular pass only (not full re-render).
4. Composite that pass back over the real ambient/window exposure — screen/soft-light blend, masked hard to reflective + near-camera surfaces only.

Turnaround gap (VIP vs standard) is the tell — this extra 3D pass is the likely reason. See [[photo-editing-pipeline]] for the real flambient process this is faking. Not confirmed, inferred from output + timing.
