"""Heuristic placement. Turns cuts + music events into a sparse list of effects.

Every placement is labelled heuristic: the rules see cut scores and loudness, not content.
"Impact on an energy rise" is a guess that a big musical moment wants weight under it."""

import random

import numpy as np
from dataclasses import dataclass, asdict, field
from fractions import Fraction

from .library import sound_shape

ONE_SHOT = {"whoosh", "riser", "impact", "shimmer", "click", "pop"}
BEDS = {"low drone", "ambience"}

# Which point of the effect lands on the event time.
ALIGN = {"click": "attack", "pop": "attack", "whoosh": "peak", "riser": "peak", "impact": "attack", "shimmer": "onset", "low drone": "start", "ambience": "start"}


@dataclass
class Candidate:
    time: float
    category: str
    score: float
    reason: str
    group: str = ""  # riser+impact pairs share a group so spacing treats them as one moment
    level_offset_db: float = 0.0  # per-accent trim from the scene map
    file: str = ""  # scene-map accent pinned to a library file (substring of its path)


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
    source_in: Fraction = Fraction(0)  # where in the effect file playback starts (beds vary this)

    def end(self):
        return self.offset + self.duration

    def to_json(self):
        data = asdict(self)
        data["offset_s"] = round(float(self.offset), 6)
        data["offset_rational"] = f"{self.offset.numerator}/{self.offset.denominator}s"
        data["duration_s"] = round(float(self.duration), 6)
        data["duration_rational"] = f"{self.duration.numerator}/{self.duration.denominator}s"
        data["end_s"] = round(float(self.end()), 6)
        data["source_in_s"] = round(float(self.source_in), 6)
        del data["offset"], data["duration"], data["source_in"]
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


def candidates(cuts, music, duration, cfg, scenes=None):
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
        moving = c.motion >= rules.get("motion_whoosh_min", 0.5)
        if moving:
            why.append(f"motion blur {c.motion:.2f} across the cut (whip/fast move)")
        if not why and rules["whoosh_requires_sync"]:
            continue
        if rules["whoosh_requires_sync"] and not (onset or beat) and not moving:
            continue
        change = scenes.zone_change(c.time) if scenes else None
        if scenes and rules.get("whoosh_on_scene_changes_only"):
            # Back the flow, not every cut: only where the film moves somewhere new, or the camera moves.
            if not change and not moving:
                continue
        if change:
            why.append(f"scene change {change[0]} -> {change[1]}")
        # Capped below an impact's floor so a musical hit outranks a whoosh on the same cut;
        # motion lifts it, since a whoosh sells movement more than it sells a static cut.
        score = min(0.85, 0.4 * c.score + 0.4 * sync + rules.get("motion_weight", 0.35) * c.motion)
        if change:
            score = min(0.85, score + rules.get("scene_change_weight", 0.2))
        if rules.get("impact_on_synced_cuts") and sync >= rules.get("impact_sync_min", 0.7):
            # Dense mode: a cut that lands hard on a music hit can take a small impact instead of a whoosh.
            out.append(Candidate(c.time, "impact", 0.35 + 0.3 * sync,
                                 f"hard cut (scene score {c.score:.2f}) on a strong music hit ({', '.join(why)})"))
        out.append(Candidate(c.time, "whoosh", score,
                             f"hard cut (scene score {c.score:.2f})" + (f", {', '.join(why)}" if why else ", no music sync")))

    # 3. Intro bed: low ambience under the opening, until the first big moment.
    bed = None if scenes else rules.get("intro_bed")  # a scene map supplies proper beds instead
    if bed:
        first = min([t for t, _ in music.energy_rises] + [duration])
        length = min(rules["intro_bed_max_s"], first, duration)
        if length >= 3:
            out.append(Candidate(0.0, bed, 0.5, f"opening bed under the first {length:.1f}s (generic intro texture, not scene-aware)", "intro"))

    # Scene-map accents (placed from a visual review, not from the signal).
    if scenes:
        for a in scenes.accents:
            out.append(Candidate(float(a["time"]), a["category"], 0.9,
                                 f"scene map: {a.get('why', a['category'])} ({scenes.source})", f"accent@{a['time']}",
                                 float(a.get("level_db", 0.0)), a.get("file", "")))

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
    # Preset word blocklist, e.g. earthy edits never want "hit" or "throttle" whooshes
    name = sound.get("relative", sound.get("name", "")).lower()
    if any(w in name for w in cfg.get("avoid_words", [])):
        return False
    return True


def sound_options(category, library, cfg, rng, recent):
    """Files to try for one placement: never-used ones (seeded shuffle) first, then the rest
    least-recently-used first, so a small library rotates instead of hammering one file."""
    pool = [s for s in library["sounds"] if category in s["categories"] and _fits(s, category, cfg)]
    unused = [s for s in pool if s["path"] not in recent]
    rng.shuffle(unused)
    used = sorted((s for s in pool if s["path"] in recent), key=lambda s: recent.index(s["path"]))
    return unused + used


def _fit_sound(c, sound, cat, cfg, chosen, duration, fd, extra_overlap=0):
    """Place one file against one candidate. Returns (fit tuple, None) or (None, reason)."""
    rules, limits = cfg["rules"], cfg["limits"]
    try:
        shape = sound_shape(sound)
    except Exception as exc:  # unreadable file: try the next one
        return None, f"could not read {sound['name']}: {exc}"
    align = ALIGN[cat]
    anchor = {"peak": shape["peak_s"], "onset": shape["onset_s"], "attack": shape["attack_s"], "start": 0.0}[align]
    # A whoosh feels on time when its peak arrives a hair *before* the cut and pulls you through it.
    lead = rules.get("whoosh_peak_lead_s", 0.0) if cat == "whoosh" else 0.0
    start_s = c.time - anchor - lead
    file_len = sound["duration"]
    notes = []
    if cat in BEDS:
        use_len = min(file_len, rules["intro_bed_max_s"] if c.group == "intro" else cfg["durations"][cat][1])
    else:
        use_len = file_len
        tail = rules.get("max_tail_s", {}).get(cat)
        if tail and anchor + tail < file_len:
            use_len = anchor + tail
            notes.append(f"tail trimmed to {tail}s after the {align}")
    if start_s < 0:
        if cat in BEDS:
            start_s = 0.0
        else:
            return None, f"{sound['name']} would start {-start_s:.2f}s before the video"
    offset = snap(start_s, fd)
    snap_err = (float(offset) - start_s) * 1000
    length = snap(use_len, fd, "floor")
    if offset + length > duration:
        length = duration - offset
        notes.append("trimmed at the end of the video")
        if length < snap(min(1.0, use_len), fd, "floor"):
            return None, f"{sound['name']} would mostly run past the end"
    if length <= 0:
        return None, "zero length after frame snapping"

    def overlapping(kind):
        return [p for p in chosen if (p.category in kind) and p.offset < offset + length and offset < p.end()]
    if cat in ONE_SHOT and len(overlapping(ONE_SHOT)) >= limits["max_overlap"] + extra_overlap:
        return None, f"already {limits['max_overlap'] + extra_overlap} one-shots sounding there"
    if cat in BEDS and len(overlapping(BEDS)) >= limits["max_beds"]:
        return None, "another bed already covers that span"
    return (sound, shape, align, offset, length, snap_err, notes, use_len, file_len), None


def place(cuts, music, video, library, cfg, log=print, scenes=None, existing=None):
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

    cands = candidates(cuts, music, float(duration), cfg, scenes)
    cands.sort(key=lambda c: (-c.score, c.time, c.category))
    minutes = max(float(duration) / 60, 0.5)
    # 0 per minute switches a category off; otherwise at least one is allowed
    per_cat_cap = {cat: max(1, int(round(n * minutes))) if n else 0 for cat, n in limits["per_minute"].items()}
    total_cap = max(1, int(round(limits["total_per_minute"] * minutes)))
    whoosh_cap = max(1, int(len(cuts) * limits["max_whoosh_share_of_cuts"])) if cuts else 0
    if limits.get("count_existing_whooshes") and existing:
        # The edit's own whooshes use up the budget too: the film as a whole should stay sparse.
        whoosh_cap = max(0, whoosh_cap - sum(1 for e in existing if e["kind"] == "whoosh"))

    chosen, skipped = [], []
    used_count = {}
    recent = {}
    group_times = {}

    def reject(c, why):
        skipped.append({"time": round(c.time, 3), "category": c.category, "score": round(c.score, 3), "why": why})

    for c in cands:
        cat = c.category
        # Scene-map accents are deliberate "flavour" on something visible (a flash, a pin, a title):
        # they layer on top, so density caps and spacing don't apply; presenter/existing rules still do.
        accent = c.group.startswith("accent@")
        if c.score < rules["min_score"]:
            reject(c, f"score {c.score:.2f} under min_score {rules['min_score']}")
            continue
        if cat not in available:
            reject(c, f"no '{cat}' sounds in the library")
            continue
        near = next((e for e in (existing or []) if abs(e["time"] - c.time) <= rules.get("existing_clearance_s", 0.6)), None)
        if near and rules.get("respect_existing_sfx", True) and cat in ONE_SHOT:
            reject(c, f"the edit already has a {near['kind']} here ({near['evidence']})")
            continue
        if scenes and scenes.quiet_at(c.time):
            reject(c, "presenter on screen (scene map): kept clear")
            continue
        if not accent and used_count.get(cat, 0) >= per_cat_cap.get(cat, 99):
            reject(c, f"{cat} cap reached ({per_cat_cap.get(cat)} for this length)")
            continue
        if not accent and cat == "whoosh" and used_count.get(cat, 0) >= whoosh_cap:
            reject(c, f"whoosh share cap ({whoosh_cap} new of {len(cuts)} cuts, after the edit's own)")
            continue
        if not accent and cat in ONE_SHOT and sum(1 for p in chosen if p.category in ONE_SHOT) >= total_cap:
            reject(c, f"total density cap reached ({total_cap})")
            continue
        if cat in ONE_SHOT and not accent:
            clash = next((p for p in chosen if p.category in ONE_SHOT and abs(p.event_time - c.time) < limits["min_spacing_s"]
                          and not (c.group and group_times.get(c.group) == p.id)), None)
            if clash:
                reject(c, f"within {limits['min_spacing_s']}s of {clash.category} at {clash.event_time:.2f}s")
                continue
        if cat == "riser" and c.group and not any(p.id == group_times.get(c.group) for p in chosen):
            reject(c, "riser only plays into an impact that was kept")
            continue

        options = sound_options(cat, library, cfg, rng, recent.get(cat, []))
        if c.file:  # an approved pick stays put however the rest of the pass shuffles
            options = [s for s in library["sounds"] if c.file in s.get("relative", s["name"])]
        if not options:
            reject(c, f"no '{cat}' sound fits duration limits {cfg['durations'][cat]}")
            continue
        fit, why_not = None, ""
        for sound in options:  # least-recently-used first; fall through to the next file if one won't fit
            fit, why_not = _fit_sound(c, sound, cat, cfg, chosen, duration, fd, extra_overlap=2 if accent else 0)
            if fit:
                break
        if not fit:
            reject(c, why_not)
            continue
        sound, shape, align, offset, length, snap_err, notes, use_len, file_len = fit
        if scenes and any(seg.quiet and float(offset) < seg.end - 0.3 and seg.start + 0.3 < float(offset + length)
                          for seg in scenes.segments):
            reject(c, f"{sound['name']} would play over the presenter (scene map)")
            continue

        level_ref = music.level_at(c.time)
        if accent and len(music.rms_db):
            # An end card or a hush in the music shouldn't make an accent vanish.
            level_ref = max(level_ref, float(np.median(music.rms_db)) - 6)
        rel = cfg["levels"]["relative_db"][cat]
        gain = level_ref + rel - shape["rms_db"] - (1 - c.score) * cfg["levels"]["confidence_scale_db"] + c.level_offset_db
        # RMS under-reads transient hits, so also cap the effect's own peak per category.
        gain = min(gain, cfg["levels"]["peak_ceiling_dbfs"][cat] - shape["peak_db"])
        gain = max(cfg["levels"]["min_gain_db"], min(cfg["levels"]["max_gain_db"], gain))
        fades = cfg["fades"][cat]
        fade_out = fades[1]
        if use_len < file_len or "trimmed at the end of the video" in notes:
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
        history = recent.setdefault(cat, [])
        if sound["path"] in history:
            history.remove(sound["path"])
        history.append(sound["path"])
        if c.group:
            group_times.setdefault(c.group, pid)

    if scenes:
        chosen += scene_beds(scenes, music, library, cfg, duration, fd, skipped)
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


def scene_beds(scenes, music, library, cfg, duration, fd, skipped):
    """One ambience bed per scene stretch, matched by tag, crossfaded at the joins.
    Each bed starts at a different point in its file so repeats don't line up."""
    sc = cfg.get("scenes", {})
    xfade = sc.get("crossfade_s", 0.6)
    beds = []

    def lay(seg, n, tag, offset_db, layer):
        pool = [s for s in library["sounds"] if "ambience" in s["categories"] and tag in s["tags"]]
        if not pool:
            skipped.append({"time": round(seg.start, 3), "category": "ambience", "score": 1.0,
                            "why": f"no ambience tagged '{tag}' for the {seg.label} scene"})
            return
        recorded = [s for s in pool if "synthetic" not in s["tags"]]
        if sc.get("prefer_recorded") and recorded:
            pool = recorded  # a real recording always beats the synthetic stand-in
        sound = pool[(n + len(beds)) % len(pool)]
        shape = sound_shape(sound)
        start = max(0.0, seg.start - xfade / 2)
        end = min(float(duration), seg.end + xfade / 2)
        offset = snap(start, fd)
        length = snap(end - float(offset), fd, "floor")
        if length <= 0:
            return
        spare = max(0.0, sound["duration"] - float(length) - 1.0)
        source_in = snap((n * 7.37) % spare, fd) if spare > 0 else Fraction(0)
        if float(length) > sound["duration"] - float(source_in):
            length = snap(sound["duration"] - float(source_in), fd, "floor")
        rel = sc.get("relative_db", {}).get(tag, -16) + offset_db
        gain = music.level_at((seg.start + seg.end) / 2, window=max(1.0, (seg.end - seg.start) / 2)) + rel - shape["rms_db"]
        # Recordings arrive at wildly different levels (a crickets file can sit 20 dB under a birds
        # file), so beds may be boosted well past the one-shot limit; the peak cap still applies.
        gain = min(gain, sc.get("peak_ceiling_dbfs", -12) - shape["peak_db"])
        gain = max(cfg["levels"]["min_gain_db"], min(sc.get("max_gain_db", 24.0), gain))
        beds.append(Placement(
            id="bed", category="ambience", event_time=round(seg.start, 4), offset=offset, duration=length,
            source=sound["path"], source_name=sound.get("relative", sound["name"]), gain_db=round(gain, 2),
            fade_in=xfade, fade_out=xfade, confidence=0.7,
            reason=f"{seg.label} scene{' (layer)' if layer else ''} {seg.start:.1f}-{seg.end:.1f}s -> '{tag}' ambience (scene map: {scenes.source})",
            align="start", source_in=source_in,
            notes=["synthetic ambience" if "synthetic" in sound["tags"] else "library ambience"],
        ))
    for n, seg in enumerate(scenes.merged()):
        if not seg.tag or seg.tag in sc.get("skip_tags", []):
            continue
        lay(seg, n, seg.tag, seg.offset_db, False)
        for tag, extra_db in seg.layers:
            lay(seg, n, tag, seg.offset_db + extra_db, True)
    return beds
