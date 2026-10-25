# Architectural Scene Quality Rules (Hunter, pasted 2026-10-26)

GENERAL
- Work in metres and state the coordinate convention.
- Preserve approved architecture and camera settings.
- Save a checkpoint before substantial changes.
- Work in small batches. Validate one asset before duplicating it.
- Do not invent missing dimensions or claim checks were performed
  when the available tools cannot perform them.

ASSET INSPECTION
Before placing an imported asset:
- Inspect dimensions, orientation, origin, hierarchy and scale.
- Identify its actual front direction from geometry.
- Identify the supporting surface and relevant contact points.
- Check whether it is rigged, animated or a fixed-pose mesh.
- Do not blindly apply transforms or alter proportions.

FURNITURE PLACEMENT
- Define the intended facing target.
- Place support points on the actual supporting surface.
- Check meaningful intersections and circulation clearances.
- Do not use object origins or bounding boxes as proof of contact.
- Treat bounding-box overlap as a warning, not proof of collision.

PEOPLE
- Define intended action, facing direction and support surfaces.
- Fit the pose to the seat when the rig permits.
- Check pelvis, thighs, feet, hands and body intersections.
- Do not distort anatomy to fit furniture.
- If the asset cannot fit plausibly, report this and propose a replacement.

VALIDATION
- Show top, front/side and final-camera views where relevant.
- Report measurements separately from visual judgements.
- Mark unresolved checks as UNKNOWN, not PASS.
- Stop for approval after the first furniture/person arrangement.

CAMERA
- Approve start/end framing before animation.
- Specify lens, duration, path and speed behaviour.
- Inspect intermediate frames for clipping and framing changes.
- Produce a cheap preview before final rendering.

AI FINISHING
- Preserve the approved raw Blender render as the baseline.
- Compare architecture, furniture orientation and people
  before and after enhancement.
- Do not use image enhancement to conceal unresolved scene errors.
