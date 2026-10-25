---
type: concept
tags: [ai, people, lifestyle, listings, framework, higgsfield]
status: piloted
updated: 2026-10-26
---

# AI lifestyle people (listings)

How 10x puts **AI-generated people** into listing photos and films so they read as real lifestyle shots: a couple in the kitchen, a family on the lawn, someone reading by the window. No real talent is cast. Every person is invented and stays consistent from listing to listing. **Pilot done (Hunter confirmed 2026-10-26).** The results (cast, what held, real costs) haven't been written back here yet, and there is no `projects/ai-cast/` folder in the vault.

It slots into [[job-framework-v2]] as two new shot classes, run by the `10x-ai` skill like any other job.

## Principles
1. **The property is never touched.** People are added and the room is not regenerated. On a real photo, only the pixels of the person and their contact shadow come from AI; every other pixel is the original photo. This is the same rule as [[staging-rules]] and the "never full-frame a real photo" lesson in [[higgsfield-pipelines]].
2. **Invented people only.** No real person's likeness: no celebrities, no agents' faces without consent, no faces copied from reference photos. Cast members are generated from text.
3. **A recurring house cast.** A small set of locked characters is reused across listings. Consistency is what makes them read as "talent" instead of random AI faces, and reusing them saves the cost of a face lock every job.
4. **Candid, not posed.** The people are mid-moment, side-on or three-quarter, often slightly soft. They are part of the room, never the subject. Real lifestyle photography rarely shows a face square to camera.
5. **The buyer persona picks the cast.** A $3M Sunshine Coast family home gets a family. A city apartment gets a young professional or couple. Decide it at intake, not per photo.
6. **Disclosure is the agency's call.** AI people don't misrepresent the property, but check each agency's policy on AI imagery before delivery. Note it in JOB.md.

## The house cast (built once, reused)
Folder: `projects/ai-cast/<id>/`. Each character has:
- `face.png`: a face lock, neutral expression, mid-grey seamless backdrop, black tank (the [[higgsfield-pipelines]] / `banana-pro-director-2.0` mode 0 default).
- `sheet.png`: a 6-panel character sheet (front, three-quarter, profile, full body) for angle consistency.
- `bible.md`: age, look, hair, skin, build, wardrobe palette per season, the listing types they fit, and the exact descriptive paragraph that goes into every prompt.

Starting cast (draft, Hunter to confirm):

| ID | Who | For |
|---|---|---|
| `c1-couple` | couple, early 30s (two characters, locked together) | apartments, townhouses, first homes |
| `c2-family` | parents late 30s + two kids (6 and 9) | family homes, lawns, pools |
| `c3-pro` | woman, early 40s, professional | executive homes, home offices, coastal luxury |
| `c4-downsizer` | couple, early 60s | downsizer / acreage / luxury single level |

Kids are generated characters too, never real children's photos. Keep them back-of-frame or in motion.

## Shot classes (add to [[shot-class-routes]] after the pilot)

| Class | When | Route |
|---|---|---|
| **P5 People into a real photo** | real listing photo, staged or furnished | Place → composite back onto the raw (below). **Pilot required.** |
| **C6 People in a render / CG / AI film** | renders, Blender, or AI-generated scenes with no ground truth | Generate the person directly in the scene with the cast reference (Sunburst / Nano Banana Pro), then Seedance 2.5 omni_reference for motion. **Pilot required.** |

## P5 pipeline: people into a real photo
1. **Pick the photo and the moment.** Choose the spot (island bench, sofa, deck), the action (pouring coffee, reading, walking in with groceries) and the cast member. Not every photo gets people: 2–4 per listing, the hero lifestyle rooms only.
2. **Scale and light notes (free).** Note what the person stands next to (bench height ~900 mm, door frame ~2,040 mm) and where the light comes from (which window). Both go into the prompt in words, per [[feedback-name-every-element-render-prompts]] in auto-memory.
3. **Place (paid, ~3 HF).** Nano Banana Pro or GPT Image 2.5 edit, given the photo plus the cast `face.png` and `sheet.png`. The prompt describes only the person: position, action, wardrobe, how the window light falls on them, the contact shadow. Everything else is "unchanged".
4. **Composite back onto the raw (local, free).** Segment the person and their shadow from the AI output (an ML matte, the same SegFormer/rembg tooling as [[plate-vfx]]). Feather the edge, then paste only that region onto the original photo, so the room is pixel-identical outside the person. Match grain and sharpness to the raw. This is the [[staging-rules]] "composite raw window views" trick, inverted.
5. **QC** against the realism checklist below. Re-roll from the raw, never from the last AI output.
6. **Optional motion (paid, ~35 HF at 720p).** Seedance 2.5 omni_reference from the finished still, with one small action (steam from a cup, a page turning, a hair move) and a locked camera or a slow gimbal drift. Then the Topaz chain if needed (below).

## Blender-directed lifestyle films (C6 at full scale)
The cinematic version is a short film rather than single photos: someone on a bench looking out at the water, a couple on the balcony at dusk, the car rolling up the drive, hands on a coffee cup at the island. Blender directs it and AI paints it. Blender fixes the camera move, the composition, the person's pose and position, and the car's path; the AI only makes it photoreal. It reuses what's already built:
- [[blender-blockout-pipeline]]: the kit (`scene.json` → headless build), MPFB2 posed humans, Camera Shakify, material-ID maps (people = purple), and the Sunburst → video route.
- [[lambo-huracan]]: the CG car rig (a clean world-aligned rig, bicycle-model steering, drive IN), tracked real plates, and the 2026-10-22 finish chain.

**The film is the real property; AI people are a few directed moments (Hunter, 2026-10-22).** Most of the film is 10x's real footage of the house. The AI cast appears only in 2–4 hand-picked hero moments that Hunter directs: the bench looking at the water, the balcony, the car arriving. It's never a whole AI film. Each moment is planned like a shot on set (who, where, what action, which camera move), then built with the recipe below and cut between the real shots, graded to match.

**Per-shot recipe**
1. **Set.** Choose the source:
   - the kit for render and plan jobs;
   - a low-poly scan of the real house (Object Capture, as on 18 Maryland);
   - a real plate when 10x shot the property.
2. **Block the shot (free).** Place an MPFB2 person with the pose and action named in the shot list: sitting on the bench facing the water, leaning on the balcony rail, walking in. Then set the camera move (one continuous crane or gimbal move, no zoom) and the car path if there is one. Render a guide frame, plus a material-ID map for any shot with clutter.
3. **Photoreal still (~3 HF).** GPT Image 2.5 Sunburst from the guide frame plus the cast `face.png`. The prompt reads the guide in prose and dresses the MPFB figure as the cast member. Use the filmic "unretouched ARRI footage" wording that fixed the plasticky Lambo stills.
4. **Motion.** Route by what moves:
   - Empty architecture or a slow move → Seedance 2.5 omni_reference.
   - Faces in frame → Kling 3.0 Pro (12.5 HF) or Veo 3.1 Fast (32 HF). They held faces in the beach face test where Seedance morphed at ~2 s.
   - Car → CG car tracked into a real plate when the plate exists. Otherwise use a start frame plus an end frame (empty drive → parked car), so the AI only fills the drive.
5. **Finish.** Topaz Video for 4K 50 fps, then Hyperion HDR if it's for an HDR delivery.

**Close-ups don't need Blender.** Hands on a rail, a coffee cup, a back-of-head shot looking out at the view: generate them straight from the cast still with a small action and a slow slider move. Blender earns its keep on the wides and the moves, where AI drifts.

**Typical lifestyle film (8–10 shots):** establishing drone (real or kit) → car arrival → front door → interior walk-through → island moment (cast) → bench or lawn looking at the water (cast, close plus wide) → balcony at golden or blue hour (cast) → detail close-ups → closing wide. The sky comes from [[sky-library]].

## Realism checklist (QC, and the prompt wording)
- **Hands:** simple grips (mug, book, rail), no interlaced fingers, no hands floating near faces. Hands are the first thing that gives AI away.
- **Skin:** natural texture and pores, uneven tone, no airbrushing. Say "unretouched" and "natural skin". Glam only for agent portraits ([[feedback-ai-face-swap-glam]] in auto-memory applies to replaced faces, not lifestyle cast).
- **Scale:** heads at a believable height against the bench or door. Check it with a ruler line on the image.
- **Light:** key light from the real window side, shadow direction matching the room's existing shadows, a contact shadow under feet and objects.
- **Focus:** the person can sit slightly soft if the photo's focus plane is on the room.
- **Wardrobe:** plain, current, no logos or text, colours from the listing's palette (ZED rooms get neutrals, see [[zed-style]]).
- **Gaze:** never at camera. Looking at the task, out a window, or at each other.
- **Count:** state the exact number of people. Models add extras.
- **Same person:** compare the face against `face.png` side by side before delivery.

## Video and finish
- People video comes from the approved still (Seedance 2.5 omni_reference), never generated from scratch, so the face holds. Write the motion small; big actions morph faces.
- Camera moves follow the car-detail lesson: one continuous crane or gimbal move, constant speed, eased, no zoom, no shake (see [[lambo-huracan]] and auto-memory `feedback-cg-car-clips`).
- Finish chain, proven on the Lambo side intake 2026-10-22:
  1. Topaz Video at 2160p with frame interpolation (`apo-8`, 50 fps): ~28 HF per 5 s.
  2. Then Topaz Hyperion 2.5 for SDR→HDR: 13 HF at 720p, 56 HF at 4K.
  - Hyperion is HDR only, **not** an upscaler, and it compresses hard (~9.5 Mbps at 4K).
  - Judge it on an HDR screen; ffmpeg frame grabs look washed out. Details in auto-memory `reference-higgsfield-topaz-video`.

## Costs (estimates, confirm with `gen_runner.py estimate`)

| Item | Cost |
|---|---|
| Cast member: face lock + sheet, a few re-rolls | ~10–15 HF once |
| P5 still (place + 1–2 re-rolls) | ~3–9 HF |
| Motion, 5 s at 720p | 35 HF |
| 4K 50 fps HDR finish per 5 s clip | ~84 HF |

A typical listing (3 stills with people + 1 motion clip at 720p) runs about **45–60 HF** once the cast exists.

## Pilot plan (Gate A when Hunter says go)
1. Build `c1-couple`: two face locks + sheets, ~25 HF.
2. P5 on two real photos from a past job, one kitchen and one living room, ~15 HF.
3. One Seedance motion clip from the better still, 35 HF.
4. Write the results (what held, what failed, the real costs) back here and into [[shot-class-routes]], then decide on the rest of the cast.

**Pilot total: ~75 HF (estimate).** ✅ Done per Hunter 2026-10-26. The cast list, pilot job and agency-rules questions are closed; their answers aren't filed here yet.

## Related
[[job-framework-v2]] · [[shot-class-routes]] · [[staging-rules]] · [[higgsfield-pipelines]] · [[zed-style]] · [[plate-vfx]] · [[lambo-huracan]]
