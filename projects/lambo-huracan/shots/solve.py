"""Camera-solve a ground-level plate with Blender's tracker (libmv), for dropping the CG car in.

Clip ops need a Clip Editor, so this runs with the GUI and quits itself:
  Blender --factory-startup --python solve.py -- <shot dir> [focal_mm 24] [fps 50]
Reads <shot>/frames/f_0001.png.., writes <shot>/track.blend + <shot>/solve.json (camera per frame,
refined focal, bundles). Sony a7S III sensor 35.6 mm wide. Ground-level moves have real parallax, so the
focal length is refined (unlike the drone benchmark).
"""
import json
import os
import sys

import bpy

a = sys.argv[sys.argv.index("--") + 1:]
SHOT = os.path.abspath(a[0]); FOCAL = float(a[1]) if len(a) > 1 else 24.0; FPS = int(a[2]) if len(a) > 2 else 50
N = len([f for f in os.listdir(os.path.join(SHOT, "frames")) if f.endswith(".png")])
rep = {"frames": N}


def run():
    try:
        sc = bpy.context.scene
        sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
        sc.render.fps = FPS; sc.frame_start, sc.frame_end = 1, N
        clip = bpy.data.movieclips.load(os.path.join(SHOT, "trk" if os.path.isdir(os.path.join(SHOT, "trk")) else "frames", "f_0001.png")); clip.frame_start = 1
        tr = clip.tracking; s = tr.settings
        s.default_pattern_size = 25; s.default_search_size = 101
        s.default_motion_model = "Affine"; s.default_correlation_min = 0.75; s.use_default_normalization = True
        tr.camera.sensor_width = 35.6; tr.camera.focal_length = FOCAL
        win = bpy.context.window_manager.windows[0]
        area = max(win.screen.areas, key=lambda x: x.width * x.height); area.type = "CLIP_EDITOR"
        sp = area.spaces.active; sp.clip = clip
        region = next(r for r in area.regions if r.type == "WINDOW")
        with bpy.context.temp_override(window=win, area=area, region=region, space_data=sp, edit_movieclip=clip):
            # seed features at the start, middle and end so tracks cover the whole push
            for f in (1, N // 2, N):
                sc.frame_set(f)
                bpy.ops.clip.select_all(action="DESELECT")
                bpy.ops.clip.detect_features(placement="FRAME", margin=30, threshold=0.008, min_distance=45)
                bpy.ops.clip.track_markers(backwards=False, sequence=True)
                bpy.ops.clip.track_markers(backwards=True, sequence=True)
            rep["detected"] = len(tr.tracks)
            bpy.ops.clip.clean_tracks(frames=max(25, N // 6), error=0.0, action="DELETE_TRACK")
            rep["after_length_clean"] = len(tr.tracks)
            obj = tr.objects.active
            s.use_keyframe_selection = True
            s.refine_intrinsics_focal_length = True
            bpy.ops.clip.solve_camera()
            rep["err_pass1"] = tr.reconstruction.average_error
            s.use_keyframe_selection = False     # keep the keyframes pass 1 found
            for lim in (3.0, 2.0, 1.4, 1.0):     # drop tracks on moving things (leaves, people), re-solve
                bad = [t for t in tr.tracks if t.has_bundle and t.average_error > lim]
                if not bad or len(tr.tracks) - len(bad) < 50:
                    continue
                for t in tr.tracks:
                    t.select = t in bad
                bpy.ops.clip.delete_track()
                try:
                    bpy.ops.clip.solve_camera()
                except RuntimeError as e:
                    rep.setdefault("resolve_fail", []).append(lim); break
                rep.setdefault("passes", []).append([lim, len(tr.tracks), tr.reconstruction.average_error])
            rep["err_final"] = tr.reconstruction.average_error
            rep["solved"] = tr.reconstruction.is_valid
            rep["focal_mm"] = tr.camera.focal_length
            rep["tracks"] = len(tr.tracks)
            rep["keyframes"] = [obj.keyframe_a, obj.keyframe_b]
            bpy.ops.clip.setup_tracking_scene()
        # dump camera path + bundles (in the solver's arbitrary frame; scene.py sets ground/scale)
        cams = []
        for c in tr.reconstruction.cameras:
            cams.append({"frame": c.frame, "matrix": [list(r) for r in c.matrix]})
        rep["solved_frames"] = len(cams)
        bundles = [{"name": t.name, "co": list(t.bundle), "err": t.average_error,
                    "px": [list(m.co) for m in t.markers if m.frame == 1 and not m.mute]}
                   for t in tr.tracks if t.has_bundle]
        json.dump({"cameras": cams, "bundles": bundles, "focal_mm": tr.camera.focal_length, "sensor_mm": 35.6,
                   "w": 1920, "h": 1080, "fps": FPS}, open(os.path.join(SHOT, "solve.json"), "w"))
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(SHOT, "track.blend"))
    except Exception:
        import traceback
        rep["error"] = traceback.format_exc()
    json.dump(rep, open(os.path.join(SHOT, "solve_report.json"), "w"), indent=2)
    print("SOLVE_REPORT", json.dumps(rep))
    bpy.ops.wm.quit_blender()


bpy.app.timers.register(run, first_interval=2.0)
