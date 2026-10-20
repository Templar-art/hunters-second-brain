"""Camera-track the drone plate in Blender's Clip Editor and save a solved scene.

Run with the GUI (clip ops need a Clip Editor area):
  Blender --factory-startup --python scripts/01_track.py
Writes track.blend + track_report.json next to the job folder, then quits.
"""
import bpy, json, os

JOB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIRST = os.path.join(JOB, "frames", "f_0001.png")
N = 45  # frame 46 is a hard cut to the next shot
report = {}


def run():
    try:
        scene = bpy.context.scene
        scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
        scene.render.fps, scene.render.fps_base = 24000, 1001
        scene.frame_start, scene.frame_end = 1, N

        clip = bpy.data.movieclips.load(FIRST)
        clip.frame_start = 1
        tr = clip.tracking
        s = tr.settings
        s.default_pattern_size = 21
        s.default_search_size = 81
        s.default_motion_model = 'Affine'
        s.default_correlation_min = 0.8
        s.use_default_normalization = True
        cam = tr.camera
        cam.sensor_width = 36.0
        cam.focal_length = 24.0  # DJI Hasselblad 24mm-equiv; fixed, not refined (short push = weak parallax)

        win = bpy.context.window_manager.windows[0]
        area = max(win.screen.areas, key=lambda a: a.width * a.height)
        area.type = 'CLIP_EDITOR'
        sp = area.spaces.active
        sp.clip = clip
        region = next(r for r in area.regions if r.type == 'WINDOW')

        with bpy.context.temp_override(window=win, area=area, region=region, space_data=sp, edit_movieclip=clip):
            scene.frame_set(1)
            bpy.ops.clip.detect_features(placement='FRAME', margin=40, threshold=0.05, min_distance=70)
            report["detected"] = len(tr.tracks)
            bpy.ops.clip.select_all(action='SELECT')
            bpy.ops.clip.track_markers(backwards=False, sequence=True)
            # keep only tracks that survive (nearly) the whole shot
            for t in tr.tracks:  # drop markers on the cut frame
                if t.markers.find_frame(46):
                    t.markers.delete_frame(46)
            bpy.ops.clip.clean_tracks(frames=40, error=0.0, action='DELETE_TRACK')
            report["after_length_clean"] = len(tr.tracks)

            obj = tr.objects.active
            obj.keyframe_a, obj.keyframe_b = 1, 45
            s.use_keyframe_selection = False
            s.refine_intrinsics_focal_length = False
            bpy.ops.clip.solve_camera()
            report["err_pass1"] = tr.reconstruction.average_error

            # drop bad tracks (surf, cars) then re-solve
            bad = [t for t in tr.tracks if t.has_bundle and t.average_error > 1.0]
            for t in tr.tracks:
                t.select = t in bad
            if bad:
                bpy.ops.clip.delete_track()
            report["after_error_clean"] = len(tr.tracks)
            bpy.ops.clip.solve_camera()
            report["err_final"] = tr.reconstruction.average_error
            report["solved"] = tr.reconstruction.is_valid

            bpy.ops.clip.setup_tracking_scene()

        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(JOB, "track.blend"))
    except Exception as e:  # noqa
        import traceback
        report["error"] = traceback.format_exc()
    with open(os.path.join(JOB, "track_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    bpy.ops.wm.quit_blender()
    return None


bpy.app.timers.register(run, first_interval=2.0)
