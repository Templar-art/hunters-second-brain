# Subject-aware protected placement

## Actual process
Detect/annotate source faces → map through real shot crop/transforms → add padded face/manual movement zones → measure actual text/card bounds after fonts load → include complete animation path → select a stable anchor over the scene/phrase → validate final render.

## Detector boundary
Optional scripts/detect_faces.py requires MediaPipe, OpenCV and a supplied detector model. It emits observations, not automatically approved safe regions. A missed face is not an empty frame. Multiple people, blur, profile, occlusion and fast motion need caution. The adapter assumes validated CFR; use PTS or approved conform for VFR. No model/dependencies are bundled.

## Coordinate boundary
code/placement.mjs maps a source crop filling the output. Rotation, letterbox, PiP and perspective require actual transform adapters. Do not use source boxes directly after reframing. Manually protect relevant hands, feet, joints, equipment and demonstrations: face detection cannot certify movement visibility.

## Placement policy
Use one stable anchor per appropriate interval; do not jump captions with detector jitter. Account for platform controls separately. Candidate bounds must include stroke, backplate and all animated states; keyframe samples alone may miss overshoot/rotation. Conservative unions may reject otherwise usable layouts; that is an explicit tradeoff.
No feasible placement → reduce secondary information, delay graphic, use approved alternate layout/cutaway, or ask. Never silently sacrifice subject visibility.

## Validation
Debug overlay includes protected zones, candidate envelope and chosen placement; export clean output separately. Sparse checks are provisional. A caller-provided claim of all-frame coverage must be backed by actual final-frame evidence. Geometry clearance is not perceptual certification.
