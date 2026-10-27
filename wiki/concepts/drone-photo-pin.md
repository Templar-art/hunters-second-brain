---
type: concept
tags: [tool, drone, kollosche, pin, outline, cadastre]
status: built-untested-on-live-job
updated: 2026-10-27
---

# Drone photo pinning

`projects/drone-pin/drone_pin.py` places the Kollosche K pin and the lot outline on DJI drone stills automatically. It works out where the property sits in each photo from the drone's own position data and Queensland's surveyed lot boundaries, then Hunter approves or nudges each photo in a browser page before it renders. Everything runs locally except the address lookup, and it spends no credits. It was built 2026-10-27 for the Kollosche townhouse stills; the video version is [[plate-vfx]] / the `kollosche-drone-graphics` scripts.

## How it works
1. **Address → lot.** QLD Spatial's public cadastre (`LandParcelPropertyFramework` MapServer) turns the address into a lot/plan and its surveyed boundary polygon. The outline is the real legal boundary, not a trace.
2. **Photo → camera.** DJI writes GPS, height above takeoff, heading and gimbal tilt into each photo's XMP, and EXIF holds the 35 mm focal length. **Lightroom exports keep all of it** (checked on Mavic 4 Pro and Air 3S exports), including the crop (`crs:Crop*`, `CropAngle`), so the original frame is rebuilt and projected through the crop.
3. **Review page.** Run `drone_pin.py review <job>`. Every photo opens with the auto placement already on it.
   - The **first pin drag marks the house**: that pixel becomes the pin target for every photo, because the lot's deepest interior point isn't always the roof (on Somerset Dr it was the pool).
   - Later drags correct that photo's camera.
   - ⌥-drag re-marks the house, and ⇧-drag moves one outline corner by hand.
   - "Apply correction" carries a compass offset fitted from the approved photos to the rest of the flight.
4. **Render.** Run `drone_pin.py render <job>`. It writes the full-resolution JPG (EXIF and colour profile kept) and a transparent PNG overlay for each approved photo. The pin uses the same proportions as the video pin, and the line shortens when needed so the K stays in frame.

## Lessons from the build (Somerset Dr test set, 7 photos)
- **⚠️ Don't trust `GimbalYawDegree`.** On these DJI files it sat 39–55° off true north. `FlightYawDegree` (the aircraft heading) put the lot on the house on every photo, top-downs included, so the tool uses it.
- **Accuracy with no drags:** the outline matched the fence lines on the top-down and the close obliques, and the pin landed on the roof ridge at 360 m. The 400 m near-horizon wide was about 1° off, and one drag fixed it.
- **Ground height can't be fitted from one photo**, because a single far shot can't separate tilt from terrain height (an early version solved -20 m and wrecked the close shots). The flight fix only solves ground height when the approved photos are at clearly different ranges; otherwise it corrects the compass alone.
- **Exports without metadata won't place.** If Lightroom strips location info, use the originals off the drone.

## Usage
```
python3 -I projects/drone-pin/drone_pin.py init   <job_dir> <photos_dir> --address "47 Somerset Drive Mudgeeraba"
python3 -I projects/drone-pin/drone_pin.py review <job_dir>
python3 -I projects/drone-pin/drone_pin.py render <job_dir>     # --all also renders unapproved photos
```
Mode per photo: `pin`, `outline`, `both` or `none`. By default, straight-down shots (pitch ≤ -70°) get the outline and angled shots get the pin.

## Limits
- Queensland addresses only (QLD cadastre). NSW would need its own service.
- Townhouses and strata lots may resolve to the whole scheme parcel. Check the outline, and use a ⇧-drag on the corners or pin-only.
- Lens distortion is ignored, which is fine for DJI JPGs and Lightroom-corrected DNGs.

Related: [[kollosche]], [[kollosche-video-guidelines]], [[plate-vfx]].
