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
4. **Render.** Run `drone_pin.py render <job>`. It writes the full-resolution JPG (EXIF and colour profile kept) and a transparent PNG overlay for each approved photo. The outline carries a very subtle drop shadow (Hunter, 2026-10-27): black at 60%, offset half a line width down, blurred 0.6× the line width; the pin has none. The pin uses the same proportions as the video pin, and the line shortens when needed so the K stays in frame.

## Style (matched to Kollosche's own listing stills, 2026-10-27)
- **Pin:** a Kollosche Blue (#011A3B) square badge with a thin white border and a white K. It sits directly on a thin white line, with no gap. Drag the badge to set the line length per photo. This replaced the bare-K video pin for stills.
- **Outline:** thin white, 0.22% of photo width, with a very subtle drop shadow.
- **Location pins** (dot, line, label and auto distance) are built for other clients. **Kollosche doesn't use location pins**, only the logo pin and the outline.

## Hand editing (Hunter's request, 2026-10-27)
- **Outline:** drag a corner, drag the line or the inside to move it all, double-click the line to add a corner, and ⌥-click a corner to delete it. Hand edits stick, and re-solving the camera won't overwrite them.
- **Outline thickness:** a Small–Large slider for each photo (0.5–3× of 0.33% of the width), plus an "All" button that applies it to every photo.
- **Export…** opens a panel. Tick photos, name each one ("Name all" + "Number them" gives `Base 01`, `Base 02` …), and pick a folder (Choose… opens the macOS folder picker). Writes `Print/`, which is the **clean original photo with no pin or outline** (Hunter, 2026-10-27, for Kollosche: print copies carry no graphics). A tick-box adds the graphics to print too, at full size, JPEG q100 and 300 dpi. It also writes and `Web/` (2048 px, q85, no EXIF so the drone GPS is dropped, ~0.7 MB). It remembers the folder and names for each job in the browser.
- **Gotcha (Finder thumbnail):** copying the source EXIF also carried Lightroom's embedded thumbnail of the clean photo, so Finder and Quick Look showed full-size prints "without the pin" even though the pixels had it. The EXIF is now re-serialised without the thumbnail.
- **Fit view** button (or 0) zooms back out. Edits are kept.
- **Gotcha:** the Claude app's preview pane silently cancels `window.confirm()`/`prompt()`, which is why Reset photo did nothing. The page now uses in-page dialogs. The server also wasn't saving `/solve` results, so tip corrections and resets vanished on reload; that's fixed too.
- **Draw outline (D):** click points around anything to make your own outline. Click the first point, double-click or press ⏎ to close it; ⌫ undoes a point and Esc cancels. It replaces the photo's outline (marked as a hand edit) and switches the mode to show the outline.
- **Lasso (A):** the quickest way to hide the outline behind a building. Click its corners (or hold and drag freehand) and close the shape; ⇧ while closing erases that area instead.
- **Razor (R):** click the outline to cut it. ⇧-click a piece of line to remove it (shown red dashed) or bring it back. Removed pieces are stored as `gaps` (edge start indices) in marks.json and skipped by the final render.
- **Brush slider:** the Behind brush and the Eraser each keep their own size; `[` and `]` work too.
- **Zoom:** scroll or pinch zooms at the pointer (up to 12×). Hold space and drag, or right-drag, to pan. 0 fits the photo. Previews are 3200 px, so a zoomed view stays sharp.
- **Eraser (X):** rubs out the behind mask so the outline comes back.
- **Behind brush (B):** paint over buildings or trees that stand in front of the outline, and the line and its shadow are hidden there. The mask is stored per photo in `masks/`. Use it on the close-up and straight-on shots; the far wides don't need it.
- **Drones-6 lesson (Esther Pl):** at 45 m up, the drone's height and heading were off enough that the camera maths couldn't place the outline (the rear corners landed in front of the building). Close oblique shots will often need the outline placed by hand, and that's what the editing is for.

## Lessons from the build (Somerset Dr test set, 7 photos)
- **⚠️ Don't trust `GimbalYawDegree`.** On these DJI files it sat 39–55° off true north. `FlightYawDegree` (the aircraft heading) put the lot on the house on every photo, top-downs included, so the tool uses it.
- **Accuracy with no drags:** the outline matched the fence lines on the top-down and the close obliques, and the pin landed on the roof ridge at 360 m. The 400 m near-horizon wide was about 1° off, and one drag fixed it.
- **Ground height can't be fitted from one photo**, because a single far shot can't separate tilt from terrain height (an early version solved -20 m and wrecked the close shots). The flight fix only solves ground height when the approved photos are at clearly different ranges; otherwise it corrects the compass alone.
- **Exports without metadata won't place.** If Lightroom strips location info, use the originals off the drone.

## Usage
```
PY=~/.venvs/typeset/bin/python   # needs OpenCV, SciPy, Pillow, HarfBuzz
$PY -I projects/drone-pin/drone_pin.py init   <job_dir> <photos_dir> --address "47 Somerset Drive Mudgeeraba"
$PY -I projects/drone-pin/drone_pin.py review <job_dir>
$PY -I projects/drone-pin/drone_pin.py render <job_dir>     # --all also renders unapproved photos
```
Mode per photo: `pin`, `outline`, `both` or `none`. By default, straight-down shots (pitch ≤ -70°) get the outline and angled shots get the pin.

## Limits
- Queensland addresses only (QLD cadastre). NSW would need its own service.
- Townhouses and strata lots may resolve to the whole scheme parcel. Check the outline, and use a ⇧-drag on the corners or pin-only.
- Lens distortion is ignored, which is fine for DJI JPGs and Lightroom-corrected DNGs.

Related: [[kollosche]], [[kollosche-video-guidelines]], [[plate-vfx]].
