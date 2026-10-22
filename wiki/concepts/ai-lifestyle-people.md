---
type: concept
tags: [ai, people, lifestyle, listings, framework, higgsfield]
status: draft — not piloted
updated: 2026-10-22
---

# AI lifestyle people (listings)

How 10x puts **AI-generated people** into listing photos and films so they read as real lifestyle shots: a couple in the kitchen, a family on the lawn, someone reading by the window. No real talent is cast. Every person is invented and stays consistent from listing to listing. This is a draft framework; nothing is piloted yet (see **Pilot plan**).

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

**Pilot total: ~75 HF.** Open questions for Hunter: confirm the cast list, which past job to pilot on, and whether agents have rules on AI people.

## Related
[[job-framework-v2]] · [[shot-class-routes]] · [[staging-rules]] · [[higgsfield-pipelines]] · [[zed-style]] · [[plate-vfx]] · [[lambo-huracan]]
