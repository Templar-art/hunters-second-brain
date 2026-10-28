"""Heuristic placement. Turns cuts + music events into a sparse list of effects.

Every placement is labelled heuristic: the rules see cut scores and loudness, not content.
"Impact on an energy rise" is a guess that a big musical moment wants weight under it."""

import random
from dataclasses import dataclass, asdict, field
from fractions import Fraction

from .library import sound_shape

ONE_SHOT = {"whoosh", "riser", "impact", "shimmer"}
BEDS = {"low drone", "ambience"}

# Which point of the effect lands on the event time.
ALIGN = {"whoosh": "peak", "riser": "peak", "impact": "attack", "shimmer": "onset", "low drone": "start", "ambience": "start"}


@dataclass
class Candidate:
    time: float
    category: str
    score: float
    reason: str
    group: str = ""  # riser+impact pairs share a group so spacing treats them as one moment


@dataclass
class Placement:
    id: str
    category: str
    event_time: float  # the cut/beat the effect is aimed at
    offset: Fraction  # where the effect file starts on the timeline (frame-snapped)
    duration: Fraction  # how much of the file is used (frame-snapped)
    source: str
    source_name: str
    gain_db: float
    fade_in: float
    fade_out: float
    confidence: float
    reason: str
    heuristic: bool = True
    align: str = "peak"
    lane: int = -1
    snap_error_ms: float = 0.0
    notes: list = field(default_factory=list)

    def end(self):
        return self.offset + self.duration

    def to_json(self):
        data = asdict(self)
        data["offset_s"] = round(float(self.offset), 6)
        data["offset_rational"] = f"{self.offset.numerator}/{self.offset.denominator}s"
        data["duration_s"] = round(float(self.duration), 6)
        data["duration_rational"] = f"{self.duration.numerator}/{self.duration.denominator}s"
        data["end_s"] = round(float(self.end()), 6)
        del data["offset"], data["duration"]
        return data


def snap(seconds, frame_duration, mode="nearest"):
    """Seconds -> exact Fraction on a frame boundary."""
    frames = Fraction(seconds) / frame_duration
    if mode == "floor":
        n = frames.numerator // frames.denominator
    else:
        n = round(frames)
    return n * frame_duration


def _near(times, t, tol):
    best = None
    for item in times:
        x = item[0] if isinstance(item, tuple) else item
        if abs(x - t) <= tol and (best is None or abs(x - t) < abs(best[0] - t)):
            best = (x, item)
    return best


def candidates(cuts, music, duration, cfg):
    rules = cfg["rules"]
    out = []
    onset_tol = rules["sync_tolerance_s"]
    beat_points = music.beats if music.beats_reliable else []

    # 1. Big musical energy rises -> impact (+ a riser leading in, when the rise is large).
    for t, rise_db in music.energy_rises:
        cut = _near([(c.time, c) for c in cuts], t, rules["snap_to_cut_s"])
        when = cut[0] if cut else t
        strength = min(1.0, rise_db / rules["energy_full_db"])
        group = f"rise@{when:.2f}"
        where = f"cut at {when:.2f}s (score {cut[1][1].score:.2f})" if cut else f"music onset {when:.2f}s"
        out.append(Candidate(when, "impact", 0.6 + 0.4 * strength,
                             f"music energy rises {rise_db:.1f} dB; impact on {where}", group))
        if rise_db >= rules["riser_min_rise_db"]:
            out.append(Candidate(when, "riser", 0.45 + 0.45 * strength,
                                 f"riser peaking into the {rise_db:.1f} dB energy rise at {when:.2f}s", group))

    # 2. Cuts that land on a strong onset or beat -> whoosh peaking on the cut.
    for c in cuts:
        onset = _near(music.onsets, c.time, onset_tol)
        beat = _near(beat_points, c.time, onset_tol)
        sync = 0.0
        why = []
        if onset:
            sync = max(sync, onset[1][1])
            why.append(f"music onset {abs(onset[0] - c.time) * 1000:.0f} ms away")
        if beat:
            sync = max(sync, 0.6)
            why.append("on the beat grid")
        if not why and rules["whoosh_requires_sync"]:
            continue
        # Capped below an impact's floor so a musical hit outranks a whoosh on the same cut.
        score = 0.4 * c.score + 0.4 * sync
        out.append(Candidate(c.time, "whoosh", score,
                             f"hard cut (scene score {c.score:.2f})" + (f", {', '.join(why)}" if why else ", no music sync")))

    # 3. Intro bed: low ambience under the opening, until the first big moment.
    bed = rules.get("intro_bed")
    if bed:
        first = min([t for t, _ in music.energy_rises] + [duration])
        length = min(rules["intro_bed_max_s"], first, duration)
        if length >= 3:
            out.append(Candidate(0.0, bed, 0.5, f"opening bed under the first {length:.1f}s (generic intro texture, not scene-aware)", "intro"))

    # 4. Outro: shimmer on the last cut in the final stretch (often an end card; not verified).
    if rules.get("outro_shimmer") and cuts:
        last = cuts[-1]
        if last.time >= duration * (1 - rules["outro_window"]):
            out.append(Candidate(last.time, "shimmer", 0.45,
                                 f"last cut at {last.time:.2f}s is in the final {int(rules['outro_window'] * 100)}%; shimmer as a closing accent (assumes an end card, not checked)", "outro"))
    return out


def _fits(sound, category, cfg):
    lo, hi = cfg["durations"][category]
    if not (lo <= sound["duration"] <= hi):
        return False
    if category in ONE_SHOT and sound.get("is_loop"):
        return False
    return True


def choose_sound(category, library, cfg, rng, recent):
    pool = [s for s in library["sounds"] if category in s["categories"] and _fits(s, category, cfg)]
    if not pool:
        return None
    fresh = [s for s in pool if s["path"] not in recent] or pool
    return fresh[rng.randrange(len(fresh))]


def place(cuts, music, video, library, cfg, log=print):
    """Greedy, score-ordered selection under spacing/density/overlap limits. Deterministic for a seed."""
    rules = cfg["rules"]
    limits = cfg["limits"]
    fd = video.frame_duration
    duration = Fraction(video.frame_count) * fd
    limit_s = cfg.get("_analysis_limit")
    if limit_s:
        duration = min(duration, snap(limit_s, fd, "floor"))
    rng = random.Random(cfg["seed"])
    available = {c for s in library["sounds"] for c in s["categories"]}

    cands = candidates(cuts, music, float(duration), cfg)
    cands.sort(key=lambda c: (-c.score, c.time, c.category))
    minutes = max(float(duration) / 60, 0.5)
    per_cat_cap = {cat: max(1, int(round(n * minutes))) for cat, n in limits["per_minute"].items()}
    total_cap = max(1, int(round(limits["total_per_minute"] * minutes)))
    whoosh_cap = max(1, int(len(cuts) * limits["max_whoosh_share_of_cuts"])) if cuts else 0

    chosen, skipped = [], []
    used_count = {}
    recent = {}
    group_times = {}

    def reject(c, why):
        skipped.append({"time": round(c.time, 3), "category": c.category, "score": round(c.score, 3), "why": why})

    for c in cands:
        cat = c.category
        if c.score < rules["min_score"]:
            reject(c, f"score {c.score:.2f} under min_score {rules['min_score']}")
            continue
        if cat not in available:
            reject(c, f"no '{cat}' sounds in the library")
            continue
        if used_count.get(cat, 0) >= per_cat_cap.get(cat, 99):
            reject(c, f"{cat} cap reached ({per_cat_cap.get(cat)} for this length)")
            continue
        if cat == "whoosh" and used_count.get(cat, 0) >= whoosh_cap:
            reject(c, f"whoosh share cap ({whoosh_cap} of {len(cuts)} cuts)")
            continue
        if cat in ONE_SHOT and sum(1 for p in chosen if p.category in ONE_SHOT) >= total_cap:
            reject(c, f"total density cap reached ({total_cap})")
            continue
        if cat in ONE_SHOT:
            clash = next((p for p in chosen if p.category in ONE_SHOT and abs(p.event_time - c.time) < limits["min_spacing_s"]
                          and not (c.group and group_times.get(c.group) == p.id)), None)
            if clash:
                reject(c, f"within {limits['min_spacing_s']}s of {clash.category} at {clash.event_time:.2f}s")
                continue
        if cat == "riser" and c.group and not any(p.id == group_times.get(c.group) for p in chosen):
            reject(c, "riser only plays into an impact that was kept")
            continue

        sound = choose_sound(cat, library, cfg, rng, recent.get(cat, set()))
        if sound is None:
            reject(c, f"no '{cat}' sound fits duration limits {cfg['durations'][cat]}")
            continue
        try:
            shape = sound_shape(sound)
        except Exception as exc:  # unreadable file: skip, keep going
            reject(c, f"could not read {sound['name']}: {exc}")
            continue

        align = ALIGN[cat]
        anchor = {"peak": shape["peak_s"], "onset": shape["onset_s"], "attack": shape["attack_s"], "start": 0.0}[align]
        start_s = c.time - anchor
        file_len = sound["duration"]
        notes = []
        if cat in BEDS:
            use_len = min(file_len, rules["intro_bed_max_s"] if c.group == "intro" else cfg["durations"][cat][1])
        else:
            use_len = file_len
        if start_s < 0:
            if cat in BEDS:
                start_s = 0.0
            else:
                reject(c, f"{sound['name']} would start {-start_s:.2f}s before the video")
                continue
        offset = snap(start_s, fd)
        snap_err = (float(offset) - start_s) * 1000
        length = snap(use_len, fd, "floor")
        if offset + length > duration:
            length = duration - offset
            notes.append("trimmed at the end of the video")
            if length < snap(min(1.0, use_len), fd, "floor"):
                reject(c, f"{sound['name']} would mostly run past the end")
                continue
        if length <= 0:
            reject(c, "zero length after frame snapping")
            continue

        # Overlap limit: count effects already sounding at any point in this one's span.
        def overlapping(kind):
            return [p for p in chosen if (p.category in kind) and p.offset < offset + length and offset < p.end()]
        if cat in ONE_SHOT and len(overlapping(ONE_SHOT)) >= limits["max_overlap"]:
            reject(c, f"already {limits['max_overlap']} one-shots sounding there")
            continue
        if cat in BEDS and len(overlapping(BEDS)) >= limits["max_beds"]:
            reject(c, "another bed already covers that span")
            continue

        level_ref = music.level_at(c.time)
        rel = cfg["levels"]["relative_db"][cat]
        gain = level_ref + rel - shape["rms_db"] - (1 - c.score) * cfg["levels"]["confidence_scale_db"]
        # RMS under-reads transient hits, so also cap the effect's own peak per category.
        gain = min(gain, cfg["levels"]["peak_ceiling_dbfs"][cat] - shape["peak_db"])
        gain = max(cfg["levels"]["min_gain_db"], min(cfg["levels"]["max_gain_db"], gain))
        fades = cfg["fades"][cat]
        fade_out = fades[1]
        if "trimmed at the end of the video" in notes or (cat in BEDS and use_len < file_len):
            fade_out = max(fade_out, cfg["fades"]["trim_fade_out"])
        confidence = round(min(1.0, c.score) * (0.8 if cat in BEDS or c.group == "outro" else 1.0), 2)

        pid = f"fx{len(chosen) + 1:02d}"
        chosen.append(Placement(
            id=pid, category=cat, event_time=round(c.time, 4), offset=offset, duration=length,
            source=sound["path"], source_name=sound.get("relative", sound["name"]), gain_db=round(gain, 2),
            fade_in=fades[0], fade_out=min(fade_out, float(length) / 2), confidence=confidence,
            reason=c.reason + f"; '{sound.get('relative', sound['name'])}' picked from {cat} by {sound['category_source'] or 'tags'} (seed {cfg['seed']})",
            align=align, snap_error_ms=round(snap_err, 2), notes=notes,
        ))
        used_count[cat] = used_count.get(cat, 0) + 1
        recent.setdefault(cat, set()).add(sound["path"])
        if len(recent[cat]) > 3:
            recent[cat] = set(list(recent[cat])[-3:])
        if c.group:
            group_times.setdefault(c.group, pid)

    chosen.sort(key=lambda p: (p.offset, p.category))
    _assign_lanes(chosen)
    for n, p in enumerate(chosen, 1):
        p.id = f"fx{n:02d}"
    missing = sorted({s["category"] for s in skipped if s["why"].startswith("no '")})
    return chosen, skipped, missing


def _assign_lanes(placements):
    """Lanes below the picture (-1, -2, ...) so overlapping clips never share a lane."""
    lanes = []  # end time per lane
    for p in placements:
        for i, end in enumerate(lanes):
            if end <= p.offset:
                lanes[i] = p.end()
                p.lane = -(i + 1)
                break
        else:
            lanes.append(p.end())
            p.lane = -len(lanes)
