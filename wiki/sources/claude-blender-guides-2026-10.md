---
type: source
tags: [blender, mcp, archviz, research, add-ons]
updated: 2026-10-26
---

# Claude + Blender guides (October 2026 research pair)

Two research write-ups prepared for 10x on 23 October 2026, ingested 26 October. Frozen originals:
- [Claude + Blender MCP: Automation and Photoreal Render Guide](../../raw/blender/claude-blender-mcp-render-guide-2026-10-23.md): setup, capabilities, limits, a best-practice workflow, a realism checklist, AI refinement and a critique loop.
- [Claude and Blender: Recommended Plugins and Add-ons](../../raw/blender/claude-blender-plugins-addons-2026-10-23.md): the companion. It shortlists add-ons and corrects several claims in the render guide.

Both are documentation research, not hands-on tests. Where the two disagree, **the add-ons doc wins**: it was written as the correction pass.

## Takeaways for 10x

### The bridge
- There are two different Blender MCPs, and you should never connect both at once:
  - **Official Blender Lab MCP server** (blender.org, 26 tools). Good for grounded Python API and manual lookups and for auditing files. Needs Blender 4.2+ and Claude Desktop.
  - **Community MCP for Blender** (ahujasid, MIT). This is the one 10x runs. It adds asset search and import (Poly Haven, Sketchfab, Poly Pizza), `generate_3d` (Rodin, Hunyuan3D, Tripo) and `look`. A third option, blender-ai-mcp, is verification-first and runs in Docker.
- The community package is now called **`mcp-for-blender`**. The old `blender-mcp` command, which 10x's config still uses, keeps working. Its add-on runs a socket on `localhost:9876` with **no authentication and no encryption**, so it must stay on localhost.
- `BLENDER_MCP_SAFE_MODE=1` validates scripts before they run. It is not a security boundary: saving, import and export still work.
- `generate_3d` and the premium asset services cost money on their own. They are not free with the bridge.
- Limits: one MCP client per Blender session. Long Cycles renders time the tool call out, so render previews small and run finals headless. Claude's spatial judgement is weaker than its coding (floating objects, intersections, wrong scale). AI-generated meshes are messy, so use them for background props only. Low-res screenshots hide noise and texture stretching.

### Working rules (largely already 10x practice)
Use metres with scale applied, one task per prompt with a visual check after each, and numbers instead of adjectives. Name everything (`WALL_N`, `LGT_Key`, `MAT_Oak`) and use collections. Save versioned files before each big step, and lock the camera early. The add-ons doc corrects the "lowest point at z = 0" floor check: each object's **intended support points must meet its intended support surface**. Wall art, pendants, stacked objects and upper floors each need a different test.

### Add-on shortlist (verdicts reconciled in [[blender-blockout-pipeline]])
| Add-on | Use | Cost | Note |
|---|---|---|---|
| **fSpy + importer** | match a Blender camera to a still property photo | free | New to 10x. Still photos only, not moving-camera tracking. Validate it against one known dimension. |
| Blendkit (BlenderKit) | furniture, materials | free tier / Full plan | no Claude interface; import by hand, then let Claude arrange |
| Poly Haven Asset Browser | HDRIs, materials, models | paid add-on, free assets | redundant: the MCP's own Poly Haven import covers it |
| Photographer 5 | physical exposure, white balance, lens shift, IES, render queue | paid (Gumroad) | Blender 3.2.2+; never drive one parameter from both Photographer and native controls |
| Geo-Scatter | lawns, gardens, exterior scatter | paid; Biome-Reader free | 5.6.4 targets Blender 5.2 LTS; never install both Geo-Scatter and Biome-Reader together |
| Archipack | parametric walls, windows, roofs, stairs | old edition free, **2.x paid** | outputs plain mesh |
| Node Wrangler | material node setup and repair | bundled | auto texture hookup relies on filenames, so check the connections |

**Acceptance test before trusting Claude with any add-on:** read-only inspection first (Blender version, add-on version, registered operators). Then run one reversible test in a temporary collection and read the values back. Never invent operator names, and never take "no error" as proof that it worked. Keep a version manifest (Blender, add-on, engine, OS, tested actions, known failures).

### Photoreal checklist (for shots where Blender is the final pixel, not just a guide frame)
- **Geometry:** bevel every hard edge (2–5 mm, harden normals). Add imperfections: skirting, power points, switches, cornices, uneven cushions. Use real sizes: door 2.04 m, bench 0.9 m, seat 0.45 m.
- **Light:** HDRI first. Add a sun only if the HDRI's own direction calls for one, and never a hard sun on an overcast HDRI. Use Blackbody temperatures: daylight 5500–6500 K, downlights 2700–3000 K. Use IES profiles. Let the shadows go dark. Light portals can help interiors but slow each sample, so benchmark them, and they do nothing outdoors.
- **Materials:** keep albedo between about 0.03 and 0.9. Roughness variation matters more than colour. Glass gets real thickness and an IOR of 1.45–1.52. Break up tiling.
- **Camera:** 16–24 mm at 1.2–1.6 m height, two-point perspective (shift Y, not pitch). Light lens distortion, chromatic aberration, vignette and grain in the compositor.
- **Render:** AgX, saved as EXR. Diffuse and glossy bounces 4–8, transmission 12. Treat any sample count as a test setting: compare crops at final size before choosing the budget.

### AI finishing
Render to EXR with passes, then grade. Upscale at low creativity, make local masked fixes only, then do the final grade. The add-ons doc **retracts** the guide's universal creativity numbers: use each tool's own controls, then compare geometry, openings, finishes and text against the raw render. Unbuilt property is labelled "artist's impression". This agrees with [[staging-rules]] (never regenerate the whole architecture).

### Critique loop
Each round: render a preview through `CAM_Main`, score it against a fixed rubric, apply the top 1–3 fixes **one at a time**, re-render from the same camera, compare side by side, save `vNN` and log the change. Run 4–8 rounds. Rubric axes, each scored 1–10: scale and proportion, geometry detail, lighting realism, exposure and contrast, material realism, composition and verticals, styling, noise and artefacts. For every axis under 8, name the cause and the exact Blender fix. Verification passes: clay override, wireframe and X-ray, and a dimension report of every furniture item.

### Proposed, not built
A **"10x Archviz QA" skill** holding scene rules (protected objects, approved cameras and materials), editing rules (inspect first, one subsystem at a time, checkpoints, never silently swap assets), verification rules and finishing rules. Start it as a short checklist and grow it from real production failures.

## Where it landed
- [[blender-blockout-pipeline]]: add-on verdicts reconciled (contradictions flagged), plus the fSpy, safe-mode, realism and critique-loop notes.
- [[claude-code-setup]]: Blender MCP package rename and safe-mode note.
