"""Run: python3 -m unittest discover -s tests -v   (from the auto-sound-design folder)"""

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402

import sounddesign  # noqa: E402
from asd import analysis, fcpxml, library, media, mix, placement  # noqa: E402

DTD = HERE / "fixtures" / "FCPXMLv1_10.dtd"
HAVE_FFMPEG = shutil.which("ffmpeg") and shutil.which("ffprobe")


def cfg():
    return sounddesign.load_config()


def fake_video(fps=Fraction(25), seconds=60, tc="", path="/tmp/My Video (final).mov"):
    frames = int(seconds * fps)
    return media.VideoInfo(path=Path(path), duration=float(seconds), fps=fps, frame_count=frames, width=1920,
                           height=1080, has_audio=True, audio_rate=48000, audio_channels=2, timecode=tc,
                           start_tc=media.parse_timecode(tc, fps), codec="prores")


def fake_sound(path, category, duration, peak=0.5, onset=0.0, loop=False):
    return {"path": path, "name": Path(path).name, "relative": Path(path).name, "duration": duration,
            "sample_rate": 48000, "channels": 2, "categories": [category], "category": category,
            "category_source": "filename", "is_loop": loop, "tags": [category],
            "analysis": {"peak_s": peak, "onset_s": onset, "attack_s": onset, "peak_db": -3.0, "rms_db": -18.0}}


def fake_library():
    sounds = []
    for i in range(4):
        sounds.append(fake_sound(f"/sfx/whoosh_{i}.wav", "whoosh", 1.2, peak=0.7))
        sounds.append(fake_sound(f"/sfx/impact_{i}.wav", "impact", 3.0, peak=0.02))
    sounds.append(fake_sound("/sfx/riser_0.wav", "riser", 5.0, peak=4.9))
    sounds.append(fake_sound("/sfx/shimmer_0.wav", "shimmer", 2.0, peak=0.1))
    sounds.append(fake_sound("/sfx/amb_0.wav", "ambience", 30.0, peak=3.0))
    sounds.append(fake_sound("/sfx/amb_loop.wav", "whoosh", 1.0, loop=True))
    return {"sounds": sounds, "root": "/sfx"}


def busy_music(seconds=60, rises=(15.0, 40.0)):
    """Onsets on every 0.5 s and a couple of energy rises: plenty of bait for over-placement."""
    beats = list(np.arange(0.5, seconds, 0.5))
    return analysis.MusicAnalysis(available=True, source="test", onsets=[(b, 0.9) for b in beats],
                                  energy_rises=[(r, 10.0) for r in rises], beats=beats, beats_reliable=True,
                                  rms_db=np.full(int(seconds / (analysis.HOP / analysis.SR)), -18.0))


def cuts_every(seconds=60, step=1.5):
    return [analysis.Cut(t, int(t * 25), 0.9) for t in np.arange(step, seconds - 0.5, step)]


class Timing(unittest.TestCase):
    def test_rational_strings(self):
        self.assertEqual(fcpxml.t(Fraction(0)), "0s")
        self.assertEqual(fcpxml.t(Fraction(5)), "5s")
        self.assertEqual(fcpxml.t(Fraction(1001, 30000)), "1001/30000s")

    def test_ntsc_frames_stay_exact(self):
        fd = Fraction(1001, 30000)
        # 10 minutes of 29.97 frames: exact rational, no float drift.
        self.assertEqual(17982 * fd, Fraction(17982 * 1001, 30000))
        snapped = placement.snap(600.0, fd)
        self.assertEqual((snapped / fd).denominator, 1)
        self.assertLessEqual(abs(float(snapped) - 600.0), float(fd) / 2)

    def test_snap_modes(self):
        fd = Fraction(1, 24)
        self.assertEqual(placement.snap(1.02, fd), Fraction(1))
        self.assertEqual(placement.snap(1.03, fd, "floor"), Fraction(1))
        self.assertEqual(placement.snap(1.03, fd), Fraction(25, 24))

    def test_timecode(self):
        self.assertEqual(media.parse_timecode("01:00:00:00", Fraction(25)), Fraction(3600))
        self.assertEqual(media.parse_timecode("00:00:01:12", Fraction(24)), Fraction(3, 2))
        # 29.97 DF: 00:01:00;02 is frame 1800 (frames 0 and 1 of minute 1 are skipped).
        self.assertEqual(media.parse_timecode("00:01:00;02", Fraction(30000, 1001)), 1800 * Fraction(1001, 30000))
        self.assertEqual(media.parse_timecode("", Fraction(25)), 0)


class Placement(unittest.TestCase):
    def run_place(self, seed=10, seconds=60, **over):
        c = cfg()
        c["seed"] = seed
        for key, value in over.items():
            section, name = key.split("__")
            c[section][name] = value
        video = fake_video(seconds=seconds)
        chosen, skipped, missing = placement.place(cuts_every(seconds), busy_music(seconds), video, fake_library(), c)
        return chosen, skipped, missing, video, c

    def test_effects_inside_video(self):
        chosen, _, _, video, _ = self.run_place()
        self.assertTrue(chosen)
        end = Fraction(video.frame_count) * video.frame_duration
        for p in chosen:
            self.assertGreaterEqual(p.offset, 0, p.id)
            self.assertLessEqual(p.end(), end, p.id)
            self.assertGreater(p.duration, 0)
            self.assertEqual((p.offset / video.frame_duration).denominator, 1, "offset not on a frame")
            self.assertEqual((p.duration / video.frame_duration).denominator, 1, "duration not whole frames")

    def test_overlap_and_lanes(self):
        chosen, _, _, _, c = self.run_place()
        one_shots = [p for p in chosen if p.category in placement.ONE_SHOT]
        # Peak concurrency: check at every clip start (concurrency only rises at a start).
        for p in one_shots:
            sounding = [q for q in one_shots if q.offset <= p.offset < q.end()]
            self.assertLessEqual(len(sounding), c["limits"]["max_overlap"])
        beds = [p for p in chosen if p.category in placement.BEDS]
        for a in beds:
            for b in beds:
                if a is not b:
                    self.assertFalse(a.offset < b.end() and b.offset < a.end(), "two beds overlap")
        for a in chosen:
            for b in chosen:
                if a is not b and a.lane == b.lane:
                    self.assertFalse(a.offset < b.end() and b.offset < a.end(), f"{a.id}/{b.id} share a lane and overlap")
            self.assertLess(a.lane, 0)

    def test_sparse_and_spaced(self):
        chosen, skipped, _, _, c = self.run_place()
        cuts = cuts_every(60)
        whooshes = [p for p in chosen if p.category == "whoosh"]
        self.assertLess(len(whooshes), len(cuts) * 0.5, "a whoosh on most cuts")
        self.assertLessEqual(len(whooshes), int(len(cuts) * c["limits"]["max_whoosh_share_of_cuts"]))
        hits = sorted((p for p in chosen if p.category in placement.ONE_SHOT and p.category != "riser"), key=lambda p: p.event_time)
        for a, b in zip(hits, hits[1:]):
            self.assertGreaterEqual(b.event_time - a.event_time, c["limits"]["min_spacing_s"] - 1e-6)
        self.assertTrue(skipped, "nothing was turned down: rules aren't biting")

    def test_reproducible(self):
        a = [p.to_json() for p in self.run_place(seed=3)[0]]
        b = [p.to_json() for p in self.run_place(seed=3)[0]]
        self.assertEqual(a, b)

    def test_every_effect_is_explained(self):
        for p in self.run_place()[0]:
            self.assertTrue(p.heuristic)
            self.assertTrue(p.reason)
            self.assertGreaterEqual(p.confidence, 0)
            self.assertLessEqual(p.confidence, 1)

    def test_peak_ceiling_per_category(self):
        chosen, _, _, _, c = self.run_place()
        for p in chosen:
            peak_after = -3.0 + p.gain_db  # fake sounds peak at -3 dBFS
            self.assertLessEqual(peak_after, c["levels"]["peak_ceiling_dbfs"][p.category] + 1e-6, p.id)

    def test_loops_not_used_as_one_shots(self):
        for p in self.run_place()[0]:
            self.assertNotEqual(p.source, "/sfx/amb_loop.wav")

    def test_missing_category_reported(self):
        lib = fake_library()
        lib["sounds"] = [s for s in lib["sounds"] if s["category"] != "impact"]
        video = fake_video()
        _, skipped, missing = placement.place(cuts_every(), busy_music(), video, lib, cfg())
        self.assertIn("impact", missing)
        self.assertTrue(any("no 'impact'" in s["why"] for s in skipped))

    def test_no_audio_still_places_on_cuts_only_when_allowed(self):
        music = analysis.MusicAnalysis(available=False)
        video = fake_video()
        chosen, _, _ = placement.place(cuts_every(), music, video, fake_library(), cfg())
        self.assertFalse([p for p in chosen if p.category == "whoosh"], "whoosh_requires_sync should block unsynced cuts")


class Library(unittest.TestCase):
    def test_categorise(self):
        self.assertEqual(library.categorise(library.tokens("Big Whoosh Into Hit 02"))[:2], ["whoosh", "impact"])
        self.assertEqual(library.categorise(library.tokens("SubDrop"))[0], "impact")  # camelCase splits to "sub drop"
        self.assertEqual(library.categorise(library.tokens("whiteNoise")), [])

    @unittest.skipUnless(HAVE_FFMPEG, "needs ffmpeg")
    def test_manifest_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "My SFX"
            (root / "Ambience").mkdir(parents=True)
            silent = np.zeros((4800, 2), dtype=np.float32)
            silent[100] = 0.5
            for rel in ("Ambience/take one.wav", "odd name.wav", "boom thing.wav", "cat item.wav", "nothing.wav"):
                media.write_wav(root / rel, silent)
            (root / "odd name.wav.tags").write_text("shimmer, glass")
            (root / "catalog.csv").write_text("path,category,description\ncat item.wav,Risers,big tension riser\n")
            man = library.build_manifest(root)
            by = {s["relative"]: s for s in man["sounds"]}
            self.assertEqual(by["Ambience/take one.wav"]["category_source"], "folder")
            self.assertEqual(by["odd name.wav"]["category"], "shimmer")
            self.assertEqual(by["odd name.wav"]["category_source"], "sidecar tags")
            self.assertEqual(by["boom thing.wav"]["category"], "impact")
            self.assertEqual(by["cat item.wav"]["category"], "riser")
            self.assertEqual(by["nothing.wav"]["categories"], [])
            self.assertIn("low drone", man["missing_categories"])
            self.assertAlmostEqual(by["nothing.wav"]["duration"], 0.1, places=2)

    def test_missing_folder(self):
        with self.assertRaises(media.MediaError):
            library.build_manifest("/nonexistent/sfx folder")


class Missing(unittest.TestCase):
    def test_missing_video(self):
        with self.assertRaises(media.MediaError):
            media.video_info("/nonexistent/video file.mov")

    @unittest.skipUnless(HAVE_FFMPEG, "needs ffmpeg")
    def test_cli_friendly_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = sounddesign.main(["process", "/nonexistent/clip.mov", "--sfx", tmp, "--out", tmp])
            self.assertEqual(code, 2)
            code = sounddesign.main(["process", "/nonexistent/clip.mov", "--sfx", "/nonexistent/sfx", "--out", tmp])
            self.assertEqual(code, 2)

    def test_missing_config(self):
        with self.assertRaises(media.MediaError):
            sounddesign.load_config("/nonexistent/settings.json")


class FinalCutXML(unittest.TestCase):
    def build(self, tc=""):
        video = fake_video(fps=Fraction(30000, 1001), seconds=30, tc=tc)
        lib = fake_library()
        chosen, _, _ = placement.place(cuts_every(30), busy_music(30, rises=(12.0,)), video, lib, cfg())
        sources = {s["path"]: s for s in lib["sounds"]}
        seq = Fraction(video.frame_count) * video.frame_duration
        return video, chosen, fcpxml.build(video, chosen, sources, seq, "Test & <Project>", "Auto Sound Design")

    def test_validates_against_dtd(self):
        _, chosen, xml = self.build()
        self.assertTrue(chosen)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.fcpxml"
            path.write_text(xml)
            ok, msg = fcpxml.validate(path, DTD)
            self.assertTrue(ok, msg)

    def test_paths_and_names_escaped(self):
        _, _, xml = self.build()
        self.assertIn("file:///tmp/My%20Video%20%28final%29.mov", xml)
        self.assertIn("Test &amp; &lt;Project&gt;", xml)
        self.assertIn('frameDuration="1001/30000s"', xml)
        self.assertIn('audioRole="effects"', xml)

    def test_connected_offsets_include_timecode_start(self):
        video, chosen, xml = self.build(tc="01:00:00;00")
        first = chosen[0]
        expected = fcpxml.t(video.start_tc + first.offset)
        self.assertIn(f'offset="{expected}"', xml)
        self.assertIn(f'start="{fcpxml.t(video.start_tc)}"', xml)
        self.assertIn('tcFormat="DF"', xml)


class Mixing(unittest.TestCase):
    def test_balance_never_exceeds_ceiling_when_source_is_quiet(self):
        c = cfg()
        c["mix"]["max_bus_trim_db"] = 12.0  # enough room for the check to fix it on its own

        class P:
            def __init__(self, i, gain):
                self.id, self.gain_db, self.notes, self.offset = f"fx{i}", gain, [], Fraction(0)

        rate = mix.RATE
        loud = np.full((rate, 2), 0.6, dtype=np.float32)
        placements = [P(1, 0.0), P(2, 0.0)]
        clips = [(0, loud), (rate // 2, loud)]
        source = np.full((2 * rate, 2), 0.1, dtype=np.float32)
        bus, gain, report = mix.balance(placements, clips, 2.0, source, c)
        self.assertLessEqual(report["mix_peak_dbfs"], c["mix"]["ceiling_dbfs"] + 0.01)
        self.assertEqual(gain, 0.0)
        self.assertTrue(report["effects_turned_down_db"])
        self.assertTrue(all(-c["mix"]["max_bus_trim_db"] <= v < 0 for v in report["effects_turned_down_db"].values()))

    def test_hot_source_is_reported_not_changed(self):
        c = cfg()
        source = np.full((48000, 2), 0.99, dtype=np.float32)
        before = source.copy()
        _, gain, report = mix.balance([], [], 1.0, source, c)
        self.assertTrue(np.array_equal(source, before))
        self.assertLess(gain, 0)
        self.assertIn("warning", report)


@unittest.skipUnless(HAVE_FFMPEG, "needs ffmpeg")
class EndToEnd(unittest.TestCase):
    """Real media through the whole pipeline (synthetic clip, known cuts)."""

    @classmethod
    def setUpClass(cls):
        import fixtures
        cls.fixtures = fixtures
        cls.tmp = tempfile.TemporaryDirectory()
        base = Path(cls.tmp.name) / "Folder With Spaces"
        base.mkdir()
        cls.video = fixtures.video(base / "Test House (v2).mp4")
        cls.sfx = fixtures.sfx_library(base / "My SFX Library")
        cls.out = base / "out"
        code = sounddesign.main(["process", str(cls.video), "--sfx", str(cls.sfx), "--out", str(cls.out)])
        assert code == 0
        cls.run_dir = next(cls.out.glob("Test House (v2)_*"))
        cls.edl = json.loads((cls.run_dir / "edit_decisions.json").read_text())

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_cuts_found_within_a_frame(self):
        found = [c["time"] for c in self.edl["analysis"]["cuts"]]
        self.assertEqual(len(found), len(self.fixtures.CUTS), found)
        for truth, got in zip(self.fixtures.CUTS, found):
            self.assertLessEqual(abs(truth - got), 1 / self.fixtures.FPS + 1e-6)

    def test_energy_rise_found(self):
        rises = [r["time"] for r in self.edl["analysis"]["energy_rises"]]
        self.assertTrue(any(abs(r - self.fixtures.ENERGY_JUMP) < 0.25 for r in rises), rises)
        impacts = [e for e in self.edl["effects"] if e["category"] == "impact"]
        self.assertTrue(any(abs(e["event_time"] - self.fixtures.ENERGY_JUMP) < 0.25 for e in impacts))

    def test_outputs(self):
        outs = self.edl["outputs"]
        for key in ("preview", "sfx_only_wav", "fcpxml"):
            self.assertTrue(Path(outs[key]).is_file(), key)
        wav = media.audio_info(outs["sfx_only_wav"])
        self.assertEqual(wav["sample_rate"], 48000)
        self.assertAlmostEqual(wav["duration"], self.fixtures.DURATION, delta=0.05)
        ok, msg = fcpxml.validate(outs["fcpxml"], DTD)
        self.assertTrue(ok, msg)
        self.assertIn("NOT yet confirmed", self.edl["fcpxml_status"])

    def test_preview_picture_untouched(self):
        src = media.probe(self.video)["streams"][0]
        prev = next(s for s in media.probe(self.edl["outputs"]["preview"])["streams"] if s["codec_type"] == "video")
        self.assertEqual(prev["codec_name"], src["codec_name"])
        self.assertEqual(prev.get("nb_frames"), src.get("nb_frames"))

    def test_source_files_unchanged(self):
        # Re-hash after the run: originals must be byte-identical to a fresh fixture build.
        import hashlib
        before = hashlib.sha1(self.video.read_bytes()).hexdigest()
        sounddesign.main(["process", str(self.video), "--sfx", str(self.sfx), "--out", str(self.out), "--test-seconds", "5", "--no-xml"])
        self.assertEqual(hashlib.sha1(self.video.read_bytes()).hexdigest(), before)

    def test_sfx_wav_matches_decisions(self):
        """Energy in the SFX-only WAV sits where the decision file says effects are."""
        bus = media.decode_audio(self.edl["outputs"]["sfx_only_wav"], rate=48000, channels=1)[:, 0]
        mask = np.zeros(len(bus), dtype=bool)
        for e in self.edl["effects"]:
            a = int(e["offset_s"] * 48000)
            mask[a: a + int(e["duration_s"] * 48000) + 480] = True
        self.assertLess(np.abs(bus[~mask]).max() if (~mask).any() else 0, 1e-3)
        self.assertGreater(np.abs(bus[mask]).max(), 1e-3)

    def test_short_test_mode(self):
        code = sounddesign.main(["process", str(self.video), "--sfx", str(self.sfx), "--out", str(self.out), "--test-seconds", "8"])
        self.assertEqual(code, 0)
        run = sorted(self.out.glob("Test House (v2)_test8s_*"))[-1]
        edl = json.loads((run / "edit_decisions.json").read_text())
        for e in edl["effects"]:
            self.assertLessEqual(e["end_s"], 8.0 + 1e-6)
        dur = float(media.probe(edl["outputs"]["preview"])["format"]["duration"])
        self.assertAlmostEqual(dur, 8.0, delta=0.1)


if __name__ == "__main__":
    unittest.main()
