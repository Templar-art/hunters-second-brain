"""Scene maps: what each stretch of the video shows, written by a person (or by Claude after
looking at frames) as JSON. The tool itself still has no vision; a scene map is the
hand-off point where human/visual judgement enters, and every placement it drives says so.

Format (times in seconds of the full video):
{
  "source": "Claude visual review of one frame per shot, 28 Oct 2026",
  "segments": [{"start": 0.0, "end": 2.6, "label": "exterior"}, ...],
  "accents":  [{"time": 24.3, "category": "shimmer", "why": "sun flare"}]
}
Labels: exterior, pool, aerial, interior, bathroom, balcony, dusk, presenter, endcard.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

# label -> (ambience tag to look for, extra level offset dB, keep one-shots out?)
LABELS = {
    # Day exteriors want birds; dusk/night want crickets (Hunter, 28 Oct: "that's obvious").
    "exterior": ("outdoor", 0.0, False),
    "night": ("dusk", 0.0, False),
    "night_interior": ("dusk", -6.0, False),  # night outside, heard faintly through the glass
    "balcony": ("outdoor", -3.0, False),
    "pool": ("poolside", 0.0, False),  # unique tag: Ocular catalogs say "pool" for jungle water
    "aerial": ("aerial", 0.0, False),
    "dusk": ("dusk", 0.0, False),
    "interior": ("interior", 0.0, False),
    "bathroom": ("interior", -2.0, False),
    "presenter": (None, 0.0, True),  # someone on camera, probably talking: keep it clear
    "endcard": (None, 0.0, False),
}


@dataclass
class Segment:
    start: float
    end: float
    label: str

    @property
    def tag(self):
        return LABELS.get(self.label, (None, 0, False))[0]

    @property
    def quiet(self):
        return LABELS.get(self.label, (None, 0, False))[2]

    @property
    def offset_db(self):
        return LABELS.get(self.label, (None, 0, False))[1]


@dataclass
class SceneMap:
    source: str
    segments: list
    accents: list
    fixes: list = field(default_factory=list)  # music fixes, in full-video seconds

    def shifted(self, start, length):
        """The part of the map inside a test section, re-timed to the section's start."""
        segs = [Segment(max(s.start, start) - start, min(s.end, start + length) - start, s.label)
                for s in self.segments if s.end > start and s.start < start + length]
        acc = [{**a, "time": a["time"] - start} for a in self.accents if start <= a["time"] < start + length]
        return SceneMap(self.source, segs, acc, self.fixes)

    def label_at(self, t):
        return next((s.label for s in self.segments if s.start <= t < s.end), None)

    def zone_change(self, t, eps=0.15):
        """('outside', 'inside') style pair if the cut at t moves between zones, else None.
        Zones: outside (exterior/balcony/dusk), inside (interior/bathroom), aerial."""
        zone = {"exterior": "outside", "balcony": "outside", "pool": "outside", "dusk": "outside", "night": "outside",
                "night_interior": "inside", "interior": "inside",
                "bathroom": "inside", "aerial": "aerial", "presenter": "presenter", "endcard": "endcard"}
        a, b = zone.get(self.label_at(t - eps)), zone.get(self.label_at(t + eps))
        return (a, b) if a and b and a != b else None

    def quiet_at(self, t):
        return any(s.quiet and s.start <= t < s.end for s in self.segments)

    def merged(self):
        """Neighbouring segments that share an ambience tag become one bed."""
        out = []
        for s in self.segments:
            if out and out[-1].tag == s.tag and abs(out[-1].end - s.start) < 1e-3 and out[-1].offset_db == s.offset_db:
                out[-1] = Segment(out[-1].start, s.end, out[-1].label)
            else:
                out.append(Segment(s.start, s.end, s.label))
        return out


def load(path):
    data = json.loads(Path(path).read_text())
    segs = [Segment(float(s["start"]), float(s["end"]), s["label"]) for s in data["segments"]]
    unknown = sorted({s.label for s in segs} - set(LABELS))
    if unknown:
        raise ValueError(f"Unknown scene labels {unknown}; use one of {sorted(LABELS)}")
    return SceneMap(data.get("source", "unspecified"), segs, data.get("accents", []), data.get("music_fixes", []))
