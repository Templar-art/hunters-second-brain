"""Grade assistant planning + the Resolve bridge against a fake Resolve (no real Resolve here)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "grade"))
sys.path.insert(0, str(HERE.parent))

import resolve_bridge  # noqa: E402

ASSIST = {"shots": [
    {"shot": 0, "start": 0.0, "end": 1.0, "skip": "black or fade"},
    {"shot": 1, "start": 1.0, "end": 2.5, "scene": "interior", "resolve_gain": [1.06, 1.0, 0.94], "note": "noticeably more saturated than the film: try Sat 45-48"},
    {"shot": 2, "start": 2.5, "end": 4.0, "scene": "aerial", "resolve_gain": [1, 1, 1], "note": ""},
]}


class Plan(unittest.TestCase):
    def test_frames_inclusive_and_contiguous(self):
        p = resolve_bridge.plan(ASSIST, 24)
        self.assertEqual([(s["startFrame"], s["endFrame"]) for s in p], [(0, 23), (24, 59), (60, 95)])

    def test_cdl_and_flags(self):
        p = resolve_bridge.plan(ASSIST, 24)
        self.assertTrue(p[0]["skip_grade"])
        self.assertEqual(p[1]["cdl"]["Slope"], "1.0600 1.0000 0.9400")
        self.assertEqual(p[1]["cdl"]["Saturation"], "0.920")
        self.assertEqual(p[1]["cdl"]["NodeIndex"], "1")
        self.assertTrue(p[2]["aerial"])


class FakeGraph:
    def __init__(self, log):
        self.log = log

    def ApplyGradeFromDRX(self, path, mode):
        self.log.append(("drx", Path(path).name, mode))
        return True

    def SetLUT(self, node, path):
        self.log.append(("lut", node, Path(path).name))
        return True


class FakeItem:
    def __init__(self, log, info):
        self.log, self.info = log, info

    def GetNodeGraph(self):
        return FakeGraph(self.log)

    def SetCDL(self, cdl):
        self.log.append(("cdl", self.info["startFrame"], cdl["Slope"]))
        return True

    def AddMarker(self, *a):
        self.log.append(("marker", self.info["startFrame"]))
        return True


class FakeResolve:
    def __init__(self):
        self.log = []

    def GetProjectManager(self):
        return self

    def LoadProject(self, name):
        return None

    def CreateProject(self, name):
        self.log.append(("project", name))
        return self

    def SetSetting(self, k, v):
        return True

    def GetMediaPool(self):
        return self

    def ImportMedia(self, paths):
        return ["clip"]

    def CreateEmptyTimeline(self, name):
        return "tl"

    def SetCurrentTimeline(self, tl):
        return True

    def AppendToTimeline(self, infos):
        self.log.append(("append", len(infos)))
        return [FakeItem(self.log, i) for i in infos]


class Bridge(unittest.TestCase):
    def test_calls_in_order_against_fake_resolve(self):
        fake = FakeResolve()
        resolve_bridge._load_resolve = lambda: fake
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "grade-assist.json"
            a.write_text(json.dumps(ASSIST))
            code = resolve_bridge.main(["/tmp/master.mov", "--assist", str(a), "--fps", "24",
                                        "--powergrade", "house.drx", "--drone-lut", "dji.cube"])
            self.assertEqual(code, 0)
            self.assertTrue((Path(tmp) / "resolve-bridge-report.json").is_file())
        kinds = [x[0] for x in fake.log]
        self.assertEqual(kinds[:2], ["project", "append"])
        self.assertEqual(sum(1 for x in fake.log if x[0] == "drx"), 3)       # house look on every shot
        self.assertEqual(sum(1 for x in fake.log if x[0] == "cdl"), 2)       # not on the black shot
        self.assertIn(("lut", 1, "dji.cube"), fake.log)                      # aerial only
        self.assertEqual(sum(1 for x in fake.log if x[0] == "lut"), 1)


if __name__ == "__main__":
    unittest.main()
