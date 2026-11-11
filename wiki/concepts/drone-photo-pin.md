---
type: concept
tags: [tool, drone, kollosche, pin, outline, cadastre]
status: built-untested-on-live-job
updated: 2026-11-09
---

# Drone photo pinning

`projects/drone-pin/drone_pin.py` places the Kollosche K pin and the lot outline on DJI drone stills automatically. It works out where the property sits in each photo from the drone's own position data and the surveyed lot boundaries (Queensland or NSW), then Hunter approves or nudges each photo in a browser page before it renders. Everything runs locally except the address lookup, and it spends no credits. It was built 2026-10-27 for the Kollosche townhouse stills; the video version is [[plate-vfx]] / the `kollosche-drone-graphics` scripts.

## How it works
1. **Address → lot.** QLD Spatial's public cadastre (`LandParcelPropertyFramework` MapServer) turns the address into a lot/plan and its surveyed boundary polygon. The outline is the real legal boundary, not a trace.
   - **NSW (added 2026-11-06, for Tweed-side jobs such as [[real-specialists]]).** If QLD finds nothing or times out, or the address ends in "NSW", the tool tries NSW Spatial Services. That's a two-step lookup:
     - **Address point:** `NSW_Geocoded_Addressing_Theme/FeatureServer/1`, exact match first, then a LIKE match that keeps the house number whole. Street types are expanded, so Ave → AVENUE.
     - **Lot:** the polygon under that point, from `NSW_Land_Parcel_Property_Theme/FeatureServer/8` on portal.spatial.nsw.gov.au.
   - The `maps.six` public cadastre is only a fallback, because it stalled for minutes on 2026-11-06 while the portal answered in 0.2 s.
   - Tested: 5 Riviera Ave Tweed Heads West → 93//DP29193 (649 m²), and 138 Kennedy Dr → 10//DP33087.
2. **Photo → camera.** DJI writes GPS, height above takeoff, heading and gimbal tilt into each photo's XMP, and EXIF holds the 35 mm focal length. **Lightroom exports keep all of it** (checked on Mavic 4 Pro and Air 3S exports), including the crop (`crs:Crop*`, `CropAngle`), so the original frame is rebuilt and projected through the crop.
3. **Review page.** Run `drone_pin.py review <job>`. Every photo opens with the auto placement already on it.
   - The **first pin drag marks the house**: that pixel becomes the pin target for every photo, because the lot's deepest interior point isn't always the roof (on Somerset Dr it was the pool).
   - Later drags correct that photo's camera.
   - ⌥-drag re-marks the house, and ⇧-drag moves one outline corner by hand.
   - "Apply correction" carries a compass offset fitted from the approved photos to the rest of the flight.
4. **Render.** Run `drone_pin.py render <job>`. It writes the full-resolution JPG (EXIF and colour profile kept) and a transparent PNG overlay for each approved photo. The outline carries a very subtle drop shadow (Hunter, 2026-10-27): black at 60%, offset half a line width down, blurred 0.6× the line width; the pin has none. The pin uses the same proportions as the video pin, and the line shortens when needed so the K stays in frame.

## Next time (run order)
1. Open `Drone Pin.app`, or for a Claude session use `preview_start drone-pin-review` after pointing `.claude/launch.json` at the job.
2. Pick the photo folder and confirm the address.
3. In review, for each photo: drag the pin onto the house on a close or top-down shot (this sets the house for every photo). Use Draw outline or drag corners to fix the lot, Lasso or Behind brush to hide the line behind buildings, and Razor for pieces that shouldn't show. Zoom in for accuracy.
4. Export: name with "Name all" and "Number them", pick the folder, export Print and Web. Kollosche prints are pinned.
5. Up next: **Coastal** drone stills (client and pin style to be confirmed; Hunter, 2026-10-27). Check whether they use their own badge, Kollosche's look, or ZED's blackout before starting. **Answered 2026-10-28:** Coastal's own listing drones use a white "C°" mark on a thin white stem with a thin white lot outline, no label and no fill (see [[katrina-walsh]]). Coastal is a separate agency from Coastline Prestige.

## Mac app (2026-10-27)
To use it without Claude, double-click **`~/Desktop/Drone Pin.app`**. It's built from `projects/drone-pin/app.applescript` with `osacompile -o ~/Desktop/"Drone Pin.app" projects/drone-pin/app.applescript`.
1. Pick the folder of drone stills.
2. The first time for a folder, confirm the address. It's pre-filled from a folder named like `Client | 5 Street, Suburb`.
3. It reads the GPS, finds the lot, and opens the review page in the browser on port 8770.
4. Edit and Export from there.

Jobs live in `projects/drone-pin/jobs/<folder>`. Reopening the same folder resumes the job. Only one job is served at a time; opening another stops the last one. The backend is `app.sh`.

## Style (matched to Kollosche's own listing stills, 2026-10-27)
- **Pin:** a Kollosche Blue (#011A3B) square badge with a white border and a white K. **Proportions match Kollosche's own `Kollosche Map Pin.png`** (Drive: `Clients/Kollosche/3026 The Boulevard/`; Hunter's boss flagged the line thickness, 2026-10-27): border is 5% of the badge, the K is 54% of the badge width, and the pin line is 5.5% of the badge width. Our earlier line was half that thickness. That asset's navy is `#0B162C`, darker than the brand-pack `#011A3B`; we keep the brand navy. It sits directly on a thin white line, with no gap. Drag the badge to set the line length per photo. This replaced the bare-K video pin for stills.
- **Outline:** thin white, 0.22% of photo width, with a very subtle drop shadow.
- **Location pins** (dot, line, label and auto distance) are built for other clients. **Kollosche doesn't use location pins**, only the logo pin and the outline.

## Hand editing (Hunter's request, 2026-10-27)
- **Outline:** drag a corner, drag the line or the inside to move it all, double-click the line to add a corner, and ⌥-click a corner to delete it. Hand edits stick, and re-solving the camera won't overwrite them.
- **Outline thickness:** a Small–Large slider for each photo (0.5–3× of 0.33% of the width), plus an "All" button that applies it to every photo.
- **Import…** (added 2026-11-09) opens the macOS file picker, which takes several files at once. The photos you pick can come from any folder. They join the current job: GPS is read, a pin and outline are proposed, and a preview is made. Each one keeps its own source path (`src` in marks.json), so print copies and finished renders read the right original. A name already in the job is skipped. If a job opens empty, the page says to use Import.
- **Export…** opens a panel. Tick photos, name each one ("Name all" + "Number them" gives `Base 01`, `Base 02` …), and pick a folder (Choose… opens the macOS folder picker). Writes `Print/` **with the pin and outline** by default (full size, JPEG q100, 300 dpi). **⚠️ Supersedes the same-day note that Kollosche prints are clean:** Kollosche does pin the prints (Hunter, 2026-10-27, later that day). Untick the box to get the clean original instead. It also writes and `Web/` (2048 px, q85, no EXIF so the drone GPS is dropped, ~0.7 MB). It remembers the folder and names for each job in the browser.
- **Gotcha (Finder thumbnail):** copying the source EXIF also carried Lightroom's embedded thumbnail of the clean photo, so Finder and Quick Look showed full-size prints "without the pin" even though the pixels had it. The EXIF is now re-serialised without the thumbnail.
- **Fit view** button (or 0) zooms back out. Edits are kept.
- **Gotcha:** the Claude app's preview pane silently cancels `window.confirm()`/`prompt()`, which is why Reset photo did nothing. The page now uses in-page dialogs. The server also wasn't saving `/solve` results, so tip corrections and resets vanished on reload; that's fixed too.
- **Draw outline (D):** click points around anything to make your own outline. Click the first point, double-click or press ⏎ to close it; ⌫ undoes a point and Esc cancels. It replaces the photo's outline (marked as a hand edit) and switches the mode to show the outline.
- **Lasso (A):** the quickest way to hide the outline behind a building. Click its corners (or hold and drag freehand) and close the shape; ⇧ while closing erases that area instead.
- **Razor (R):** click the outline to cut it. ⇧-click a piece of line to remove it (shown red dashed) or bring it back. Removed pieces are stored as `gaps` (edge start indices) in marks.json and skipped by the final render.
- **Brush slider:** the Behind brush and the Eraser each keep their own size; `[` and `]` work too.
- **ZED blackout (2026-10-27):** ZED's drone stills darken everything except the house. Set the **Blackout** slider (0 = off, default 70% once you use it; All copies it to every photo) and use **Bright lasso (G)** to lasso what stays bright. Add more shapes to add bright area, ⇧ while closing cuts back to dark, and ⌥-click a shape to delete it. The edge is softened (0.15% of width). With no lasso, the outline itself is the bright area. A "lift" (sweeping the outline upward) was tried and dropped because it lit the trees behind the house, which looked weird; the code still supports `lift` but the UI hides it.
- **Zoom:** scroll or pinch zooms at the pointer (up to 12×). Hold space and drag, or right-drag, to pan. 0 fits the photo. Previews are 3200 px, so a zoomed view stays sharp.
- **Eraser (X):** rubs out the behind mask so the outline comes back.
- **Behind brush (B):** paint over buildings or trees that stand in front of the outline, and the line and its shadow are hidden there. The mask is stored per photo in `masks/`. Use it on the close-up and straight-on shots; the far wides don't need it.
- **Drones-6 lesson (Esther Pl):** at 45 m up, the drone's height and heading were off enough that the camera maths couldn't place the outline (the rear corners landed in front of the building). Close oblique shots will often need the outline placed by hand, and that's what the editing is for.

## Photos with no drone GPS (2026-11-11)
Exports made without "All Metadata" (for example the Nassau "to be pinned" JPGs) carry no DJI position data. They used to load as "no GPS", and the review page then refused to draw or edit them, which Hunter reported as "Amir won't let me pin or outline". They now work **by hand**. The pin starts mid-frame, and dragging the tip just moves it, with no camera solve. Draw the lot with **Draw outline (D)**. A location pin added on such a photo stays on that photo only, with no distance. Nothing gets auto-placed and "set house for every photo" doesn't apply.

## Client fit
- The top-down outline shot is worth making for most agencies, but **Kollosche doesn't use top-downs** (see [[kollosche]]).

## Client style profiles (2026-10-28)
Each client's look is a file in `projects/drone-pin/clients/<slug>.json`, so a new client or a style change means editing JSON rather than code. The app reads the client and address from the SSD's `Client | Address` folder name (e.g. `Zed | 86 Ormeu Street`). A branch suffix is fine (`Belle Property Hope Island` → Belle). The review page has **Client** and **Agent** pickers; an agent entry in the profile can override any style key, e.g. a team logo instead of the K. Kollosche's agent list comes from its 32 team-logo folders. Re-rendering the delivered Esther set with the profile system was pixel-identical to the delivery.

Pin heads available:
- `badge`: a square (Kollosche).
- `ring`: a circle with a white ring (Belle, YPA, Jessica Wallace).
- `disc`: a solid circle with a tinted mark (Place).
- `mark`: the logo PNG on its own, optionally over a soft circle. ZED's ringed Z works this way, as does Bespoke's B icon.
- `none`.

Other style keys:
- A dot at the end of the line (Remax, Bespoke).
- Outline colour (YPA is yellow).
- Label options: no dot, sentence case, and a regular font (ZED, Coastline).
- `place_color`: label text in a colour, drawn flat with no shadow. REAL Specialists use dark #1E1E1E text on the sky. The default is white with the line's shadow.
- `place_dist: false`: drops the distance line under every label.
- `mark_anchor: "left"`: hangs the logo by its left edge over the pin line (REAL Specialists). The default centres it.
- `elbow` (2026-11-11, Amir apartments and towers): drag the pin head sideways in Edit and the line drops, then turns 90° to the tip, so it points at the exact floor. Within half a badge of the tip it snaps back straight. Per photo this is stored as `pin_dx`.
- `outline_dash` (WHITEFOX land): a dotted outline. `outline_fill`, or the per-photo **Fill** slider, washes white inside the outline (Amir's apartment floor band).
- `notes` + `note_default` + `note_font` (Amir): a disclaimer under the outline. Pick it per photo in the **Note** box ("" = none; stored as `disclaimer`, because `note` was already taken by the camera summary). Amir's centred "Boundaries and dimensions are approximate only…" used to be the default under every outline. **⚠️ Now off by default** (Hunter, 2026-11-11: "please remove it"), so pick it per photo only if wanted; "OUTLINES INDICATIVE ONLY" sits small and bottom-left. Fill and Note only show for clients with notes.
- `watermark` (WHITEFOX): a logo burned into the corner of **every** exported photo, set by diameter, opacity and its centre offset from the right and bottom edges.
- `surround: "mono"`: **ZED's real look**. The neighbourhood goes black and white, while the lot, any Bright-lasso shapes and the far landscape (fading out above the lot) stay in colour. It isn't a darkening. The earlier "blacks out" description was a misreading, now corrected from the Sam Drones files.

Research sweep (finished pinned sets on the Clients Drive and SSD):
- **ZED:** `Zed Real Estate/*/Print/*Map Pin*`, plus `SSD/Zed | 86 Ormeu Street/AI PHOTOS/Sam Drones-0*`. How far the black and white reaches varies by job.
- **Belle:** `Belle Property Hope Island/5 Jackson Street`.
- **Bespoke:** `3009 The Boulevard`, `45 Devoy St`.
- **YPA:** `41 Sears Road`, `57 Girtin Ct`.
- **Place:** `Place Cleveland/13 Pyrite Street`.
- **Remax:** `Stuart Legg/32 Southern Skies`.
- **Coastline Prestige:** `10x Drive Pulls/REA/…/71-73 Lydford Close`.
- **Jessica Wallace:** `88 Third Ave` (The Agency, but she may now be with Harcourts).

Only **Kollosche** is confirmed. Every other profile is marked unconfirmed and explains itself in the review page. Logo files are in `projects/drone-pin/logos/`: ZED, Belle and Bespoke. **Still needed:** the YPA, Place, RE/MAX, Coastline and agency logos as white PNGs. **REAL Specialists** (Connor Hewitt, 2026-11-06): orange logo on a white line plus dark suburb labels, no outline; see [[real-specialists]]. **Amir Prestige** and **WHITEFOX** profiles were built 2026-11-11 from audits of their whole current listing books; see [[amir-prestige]] and [[whitefox]]. Both are unconfirmed. The WHITEFOX ring logo and watermark were redrawn from their photos, so ask for vector files. **Coastal** (34 Albany Ave) has no finished graphics yet, and it may be Coastline Prestige; this needs confirming.

## Auto-align attempts (2026-10-28): none beat a hand drag
Tested on Esther against Hunter's hand fixes. On a photo 11,000 px wide, the uncorrected drift was 100–400 px.
- **Matching against QLD aerial imagery:** 0–10 matches. The imagery is 3 or more years old, and the Esther lot has been redeveloped since, which is exactly Hunter's renovation concern.
- **Sea horizon for pitch and roll:** this locked onto the skyline and gave 2–3° where the right answer was 0.5–1°.
- **Matching photos against each other:** only 7–13 matches, because the views face different directions.
- **Neighbouring lot boundaries (cadastre, 765 parcels) chamfer-matched to image edges:** worse on 5 of 6 photos. Fences don't sit on boundary lines closely enough, and roofs, trees and shadows swamp the edge signal.

Conclusion: one drag per photo plus "Apply to flight" stays the method. Revisit only with a better edge signal, for example a segmentation model trained on kerbs and roads.

## Lessons from the build (Somerset Dr test set, 7 photos)
- **⚠️ Don't trust `GimbalYawDegree`.** On these DJI files it sat 39–55° off true north. `FlightYawDegree` (the aircraft heading) put the lot on the house on every photo, top-downs included, so the tool uses it.
- **Accuracy with no drags:** the outline matched the fence lines on the top-down and the close obliques, and the pin landed on the roof ridge at 360 m. The 400 m near-horizon wide was about 1° off, and one drag fixed it.
- **Ground height can't be fitted from one photo**, because a single far shot can't separate tilt from terrain height (an early version solved -20 m and wrecked the close shots). The flight fix only solves ground height when the approved photos are at clearly different ranges; otherwise it corrects the compass alone.
- **Amir Prestige** (2026-11-09, unconfirmed): white "ap." monogram on a thin line, white caps location labels, B&W surround on top-downs. See [[amir-prestige]].
- **REAL Specialists pin = icon only** (Hunter, 2026-11-09): the orange square mark (`logos/real-specialists-icon-orange.png`), centred on the line with a gap above it (`mark_gap` 0.3 of the icon size), with no wordmark.
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
- **QLD cadastre outages.** On 2026-10-29 QLD Spatial returned 502 for over 15 minutes, so `init` can't run. Fallback used on 4-6 Buckingham Way, Elanora (Kollosche): find the roof by eye in full-resolution crops, write `marks.json` by hand with `mode: pin` and an empty `lot`, and call `export()` directly. The result is pins only, with no outline until QLD is back.
- **Edited exports with no metadata** (42 Salerno St, Isle of Capri, 2026-11-06). Lightroom exported the edited stills without XMP, so `init` saw no drone position. Fix: match each edit to its HDR DNG with SIFT, which gives the crop rect. Then copy the edited JPG into `jobs/<job>/src/`, take FocalLengthIn35mm from the raw `_D.DNG` (the HDR merge DNGs drop the `drone-dji` flight tags), and append the raw's `drone-dji:*` attributes plus `crs:Crop*` as a trailer comment, which `meta()` reads by regex. Run `init` on `src/`. Also, the cadastre registers Isle of Capri addresses under **Surfers Paradise**, so a lookup with "Isle of Capri" finds nothing.
- **Queensland and NSW only.** Other states would need their own cadastre service.
- Townhouses and strata lots may resolve to the whole scheme parcel. Check the outline, and use a ⇧-drag on the corners or pin-only.
- Lens distortion is ignored, which is fine for DJI JPGs and Lightroom-corrected DNGs.

Related: [[kollosche]], [[kollosche-video-guidelines]], [[plate-vfx]].
