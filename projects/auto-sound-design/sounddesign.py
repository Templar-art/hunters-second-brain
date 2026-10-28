#!/usr/bin/env python3
"""Auto Sound Design: a first-pass SFX layer for a finished cut, for refining in Final Cut Pro.

  python3 sounddesign.py check
  python3 sounddesign.py manifest --sfx "/path/to/SFX Library" [--search "whoosh soft"]
  python3 sounddesign.py process "/path/to/My Video.mp4" --sfx "/path/to/SFX Library" [--music track.wav]
                                 [--test-seconds 20] [--seed 10] [--config my.json] [--out output]
"""

import argparse
import copy
import datetime as dt
import hashlib
import json
import shutil
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from asd import analysis, fcpxml, library, media, mix, placement, scenes  # noqa: E402

DTD = HERE / "tests" / "fixtures" / "FCPXMLv1_10.dtd"


def deep_merge(base, extra):
    out = copy.deepcopy(base)
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def load_config(path=None, seed=None):
    cfg = json.loads((HERE / "config.default.json").read_text())
    for extra in (HERE / "asd.local.json", Path(path) if path else None):
        if extra and extra.is_file():
            cfg = deep_merge(cfg, json.loads(extra.read_text()))
        elif extra and path and extra == Path(path):
            raise media.MediaError(f"Config file not found: {extra}")
    if seed is not None:
        cfg["seed"] = seed
    return cfg


def manifest_cache(root):
    digest = hashlib.sha1(str(Path(root).expanduser().resolve()).encode()).hexdigest()[:10]
    return HERE / "output" / ".cache" / f"sfx-manifest-{digest}.json"


def cmd_check(_args):
    ok = True
    print(f"Python {sys.version.split()[0]}  ({sys.executable})")
    for tool in ("ffmpeg", "ffprobe"):
        where = shutil.which(tool)
        print(f"{tool:8} {'OK  ' + where if where else 'MISSING - install with: brew install ffmpeg'}")
        ok &= bool(where)
    try:
        import numpy
        print(f"numpy    OK  {numpy.__version__}")
    except ImportError:
        print("numpy    MISSING - run ./setup.sh (it asks before installing anything)")
        ok = False
    try:
        import lxml  # noqa: F401
        print("lxml     OK  (FCPXML validation)")
    except ImportError:
        print(f"lxml     not installed; {'xmllint will validate' if shutil.which('xmllint') else 'XML validation unavailable'}")
    fcp_dtds = sorted(Path("/Applications").glob("Final Cut Pro*.app/Contents/Frameworks/Interchange.framework/Versions/A/Resources/FCPXMLv1_*.dtd"))
    if fcp_dtds:
        print(f"FCP DTDs found: {', '.join(p.name for p in fcp_dtds)}")
    return 0 if ok else 1


def cmd_manifest(args):
    cache = manifest_cache(args.sfx)
    print(f"Indexing {args.sfx} ...")
    man = library.build_manifest(args.sfx, cache_path=cache, skip_underscore=not args.include_underscore)
    print(f"{man['count']} sounds. Manifest: {cache}")
    for cat in library.CATEGORIES:
        print(f"  {cat:10} {man['category_counts'][cat]}")
    print(f"  uncategorised {man['uncategorised']}")
    if man["missing_categories"]:
        print(f"Missing: {', '.join(man['missing_categories'])}. Add files with those words in the name, or a sidecar .tags file.")
    print(man["note"])
    if args.search:
        hits = library.search(man, args.search)
        print(f"\n{len(hits)} match '{args.search}':")
        for s in hits[:40]:
            print(f"  {s['duration']:6.2f}s  {s['category'] or '-':10}  {s['relative']}")
    if args.export:
        library.save_manifest(man, args.export)
        print(f"Wrote {args.export}")
    return 0


def cmd_process(args):
    media.require_tools()
    cfg = load_config(args.config, args.seed)
    folders = cfg.get("sfx_folder")
    args.sfx = args.sfx or ([folders] if isinstance(folders, str) else folders)
    if not args.sfx:
        raise media.MediaError('No sound-effects folder. Pass --sfx "/path/to/folder" or set "sfx_folder" in asd.local.json')
    video_path = Path(args.video).expanduser()
    video, flags = media.video_info(video_path)
    music_path = Path(args.music).expanduser() if args.music else None
    if music_path and not music_path.is_file():
        raise media.MediaError(f"Music file not found: {music_path}")
    limit = args.test_seconds
    fd = video.frame_duration
    full = Fraction(video.frame_count) * fd
    # A test section starts on a keyframe so the picture can be stream-copied, untouched.
    start = Fraction(0)
    if args.start:
        if args.start >= float(full):
            raise media.MediaError(f"--start {args.start}s is past the end of the video ({float(full):.2f}s)")
        before = [k for k in media.keyframes(video.path) if k <= args.start + 1e-6]
        start = placement.snap(before[-1] if before else 0.0, fd)
    remaining = full - start
    seq_dur = min(remaining, placement.snap(limit, fd, "floor")) if limit else remaining
    seconds = float(seq_dur)
    start_s = float(start)
    partial = start > 0 or seq_dur < full
    if partial:
        cfg["_analysis_limit"] = seconds
        if start + seq_dur < full:
            cfg["rules"]["outro_shimmer"] = False  # the section's last cut isn't the film's ending
        if start > 0:
            cfg["rules"]["intro_bed"] = None  # nor is its first second the film's opening

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    tag = f"_test_{start_s:.1f}-{start_s + seconds:.1f}s" if partial else ""
    out_dir = Path(args.out).expanduser() / f"{video_path.stem}{tag}_{stamp}"
    out_dir.mkdir(parents=True, exist_ok=False)
    print(f"Video: {video.path.name}  {video.width}x{video.height}  {float(video.fps):.3f} fps ({video.fps})  "
          f"{video.duration:.2f}s  {video.frame_count} frames  tc {video.timecode or 'none'}")
    if flags["variable_frame_rate"]:
        print("  ! variable frame rate source: timing uses the nominal rate; check sync in FCP.")
    if partial:
        print(f"  Test section: {start_s:.3f}s to {start_s + seconds:.3f}s ({seconds:.2f}s)"
              + (f"; start moved back to the keyframe at {start_s:.3f}s" if args.start and abs(start_s - args.start) > 1e-3 else ""))

    print("Indexing sound effects ...")
    parts = [library.build_manifest(folder, cache_path=manifest_cache(folder), log=lambda m: print(m),
                                    skip_underscore=cfg["library"]["skip_underscore_folders"]) for folder in args.sfx]
    man = library.merge_manifests(parts)
    print(f"  {man['count']} sounds; " + ", ".join(f"{c} {n}" for c, n in man["category_counts"].items()))
    if man["count"] == 0:
        raise media.MediaError(f"No audio files found in {args.sfx}")

    print("Finding cuts ...")
    cuts = [c for c in analysis.detect_cuts(video, cfg["analysis"], limit=seconds, start=start_s) if c.time < seconds]
    motion = analysis.cut_motion(video.path, cuts, video.fps, start=start_s)
    for c in cuts:
        c.motion = motion.get(round(c.time, 4), 0.0)
    print(f"  {len(cuts)} cuts ({sum(1 for c in cuts if c.motion >= cfg['rules'].get('motion_whoosh_min', 0.5))} with motion blur)")
    print("Analysing music ...")
    if music_path:
        music = analysis.analyse_music(music_path, cfg["analysis"], limit=seconds, start=start_s,
                                       label=f"separate music file: {music_path.name}")
    elif video.has_audio:
        music = analysis.analyse_music(video.path, cfg["analysis"], limit=seconds, start=start_s, label="video's own audio track")
    else:
        music = analysis.MusicAnalysis(available=False, source="no audio")
    print(f"  {music.source}: {len(music.onsets)} onsets, {len(music.energy_rises)} energy rises, "
          f"tempo {music.tempo_bpm} BPM (confidence {music.tempo_confidence}, beats {'used' if music.beats_reliable else 'NOT used - unreliable'})")

    scene_map = None
    if args.scenes:
        scene_map = scenes.load(args.scenes).shifted(start_s, seconds)
        print(f"Scene map: {len(scene_map.segments)} segments, {len(scene_map.accents)} accents ({scene_map.source})")
    existing = analysis.existing_sfx(video.path, cuts, cfg["analysis"], start=start_s, limit=seconds) if video.has_audio else []
    if existing:
        print(f"  Effects already in the edit (heuristic): " + ", ".join(f"{e['kind']} {e['time']:.2f}s" for e in existing))
    placements, skipped, missing = placement.place(cuts, music, video, man, cfg, scenes=scene_map, existing=existing)
    for part in parts:  # keep newly measured peak times (sound dicts are shared with the merged view)
        library.save_manifest(part, manifest_cache(part["root"]))
    print(f"Placed {len(placements)} effects ({len(skipped)} candidates skipped)")

    print("Rendering effects bus ...")
    clips = mix.render_clips(placements)
    source = media.decode_audio(video.path, rate=mix.RATE, channels=2, start=start_s, duration=seconds) if video.has_audio else None
    bus, preview_gain, mix_report = mix.balance(placements, clips, seconds, source, cfg)
    sfx_wav = out_dir / f"{video_path.stem}_sfx_only.wav"
    media.write_wav(sfx_wav, bus)
    if source is not None:
        n = min(len(source), len(bus))
        preview_audio = (source[:n] + bus[:n]) * 10 ** (preview_gain / 20)
    else:
        preview_audio = bus * 10 ** (preview_gain / 20)
    preview_wav = out_dir / ".preview_mix.wav"
    master_report = None
    if cfg.get("master", {}).get("enabled"):
        # Mastering replaces the blunt overall turn-down: build the mix at full level, then level it.
        raw = (source[:n] + bus[:n]) if source is not None else bus
        media.write_wav(out_dir / ".premaster.wav", raw)
        master_report = mix.master(out_dir / ".premaster.wav", preview_wav, cfg)
        (out_dir / ".premaster.wav").unlink()
        mix_report["preview_output_gain_db"] = "replaced by mastering"
        mix_report.pop("warning", None)
        mix_report["master"] = master_report
        print(f"  Mastered preview: {master_report['input_lufs']:.1f} -> {master_report['output_lufs']} LUFS, "
              f"LRA {master_report['input_lra']:.1f} -> {master_report['output_lra']} LU, true peak {master_report['output_true_peak_dbfs']} dBFS")
    else:
        media.write_wav(preview_wav, preview_audio)
    ext = video_path.suffix.lower() if video_path.suffix.lower() in (".mov", ".mp4", ".m4v") else ".mov"
    preview = out_dir / f"{video_path.stem}{tag}_SOUND-MIX{ext}"
    media.mux_preview(video.path, preview_wav, preview, duration=seconds, start=start_s)
    preview_wav.unlink()

    xml_status = "skipped (--no-xml)"
    xml_path = None
    if not args.no_xml:
        sources = {s["path"]: s for s in man["sounds"]}
        # Copies of the effects used travel with the run folder, so the XML can be relinked on another machine.
        used_dir = out_dir / "sfx_used"
        used_dir.mkdir()
        copies = {}
        for p in placements:
            if p.source not in copies:
                name = f"{len(copies) + 1:02d}_{Path(p.source).name}"
                shutil.copy2(p.source, used_dir / name)
                copies[p.source] = str(used_dir / name)
        project_name = f"{video_path.stem}{tag} - SFX pass {stamp}"
        xml = fcpxml.build(video, placements, sources, seq_dur, project_name, cfg["fcpxml"]["event_name"],
                           write_fades=cfg["fcpxml"]["write_fades"], window_start=start,
                           media_path=lambda path: copies.get(path, path))
        xml_path = out_dir / f"{video_path.stem}_sfx.fcpxml"
        xml_path.write_text(xml, encoding="utf-8")
        ok, msg = fcpxml.validate(xml_path, DTD)
        xml_status = ("DTD-valid; " if ok else "DTD INVALID; ") + msg + ". NOT yet confirmed by a Final Cut import."

    tags_by_path = {snd["path"]: snd["tags"] for snd in man["sounds"]}
    unverified = sorted({p.source_name for p in placements if "unverified" in tags_by_path.get(p.source, [])})
    if unverified:
        print(f"  ! LICENCE UNVERIFIED (preview only, do not deliver): {', '.join(unverified)}")
    edl = {
        "tool": "auto-sound-design",
        "version": 1,
        "created": dt.datetime.now().isoformat(timespec="seconds"),
        "video": {"path": str(video.path), "fps": str(video.fps), "frame_duration": f"{fd.numerator}/{fd.denominator}s",
                  "duration_s": video.duration, "frames": video.frame_count, "width": video.width, "height": video.height,
                  "timecode": video.timecode, "has_audio": video.has_audio, **flags},
        "processed_seconds": seconds,
        "window": {"start_s": start_s, "end_s": round(start_s + seconds, 6),
                   "note": "effect times are relative to the start of this section; video_time_s is the time in the full video"},
        "test_seconds": limit,
        "music_source": music.source,
        "scene_map": ({"file": str(Path(args.scenes).resolve()), "source": scene_map.source,
                       "note": "scene labels come from a visual review recorded in this file, not from the tool's own analysis"}
                      if scene_map else None),
        "sfx_library": [p["root"] for p in parts],
        "seed": cfg["seed"],
        "honesty": ("Placements are heuristic: they come from cut scores, music loudness and onsets. The tool does not "
                    "know what any shot shows (drone, room reveal, sun flare, twilight). SFX categories come from file "
                    "and folder names, not from listening. No dialogue detection, so nothing is ducked."),
        "analysis": {"cuts": [{"time": round(c.time, 4), "frame": c.frame, "score": round(c.score, 3),
                              "motion": round(c.motion, 3)} for c in cuts],
                     "energy_rises": [{"time": round(a, 3), "rise_db": round(b, 2)} for a, b in music.energy_rises],
                     "tempo_bpm": music.tempo_bpm, "tempo_confidence": music.tempo_confidence,
                     "beats_used": music.beats_reliable, "onset_count": len(music.onsets),
                     "existing_sfx_in_edit": existing},
        "effects": [{**p.to_json(), "video_time_s": round(start_s + p.event_time, 4)} for p in placements],
        "skipped_candidates": skipped,
        "missing_categories": sorted(set(missing) | set(man["missing_categories"])),
        "mix": mix_report,
        "licence_unverified": unverified,
        "outputs": {"preview": str(preview), "sfx_only_wav": str(sfx_wav), "fcpxml": str(xml_path) if xml_path else None},
        "fcpxml_status": xml_status,
        "config": {k: v for k, v in cfg.items() if not k.startswith("_")},
    }
    (out_dir / "edit_decisions.json").write_text(json.dumps(edl, indent=2))
    (out_dir / "REPORT.md").write_text(report(edl))
    print(f"\nDone -> {out_dir}")
    print(f"  preview:  {preview.name}\n  sfx only: {sfx_wav.name}\n  decisions: edit_decisions.json, REPORT.md")
    print(f"  FCPXML:   {xml_status}")
    if mix_report.get("warning"):
        print(f"  ! {mix_report['warning']}")
    if edl["missing_categories"]:
        print(f"  ! Missing SFX categories: {', '.join(edl['missing_categories'])} (nothing downloaded or generated)")
    return 0


def cmd_synth(args):
    from asd import synth
    for path in synth.make_assets(args.out):
        print(f"  {path}")
    print("Synthetic stand-ins (tagged 'synthetic'); recorded ambience will sound more natural.")
    return 0


def cmd_relink(args):
    """Point a run folder's FCPXML at where its files live now (e.g. after copying it to the Mac)."""
    import re
    from urllib.parse import unquote
    run = Path(args.run_dir).expanduser().resolve()
    xmls = sorted(p for p in run.glob("*.fcpxml") if not p.stem.endswith("_relinked"))
    if not xmls:
        raise media.MediaError(f"No .fcpxml in {run}")
    video = Path(args.video).expanduser().resolve()
    if not video.is_file():
        raise media.MediaError(f"Video not found: {video}")
    used = run / "sfx_used"
    text = xmls[0].read_text(encoding="utf-8")
    missing = []

    def swap(match):
        old = unquote(match.group(1))
        name = Path(old).name
        if (used / name).is_file():
            return f'src="{fcpxml.file_url(used / name)}"'
        if Path(old).parent.name == "sfx_used":
            missing.append(name)
            return match.group(0)
        return f'src="{fcpxml.file_url(video)}"'

    out = re.sub(r'src="file://([^"]+)"', swap, text)
    if missing:
        raise media.MediaError(f"sfx_used is missing: {', '.join(missing)}")
    target = xmls[0].with_name(xmls[0].stem + "_relinked.fcpxml")
    target.write_text(out, encoding="utf-8")
    ok, msg = fcpxml.validate(target, DTD)
    print(f"Wrote {target}\n  {('DTD-valid; ' if ok else 'DTD INVALID; ') + msg}")
    return 0 if ok else 1


def report(edl):
    lines = [f"# Sound-design pass: {Path(edl['video']['path']).name}", "",
             f"Created {edl['created']} · seed {edl['seed']} · {edl['processed_seconds']:.2f}s processed"
             + (f" (test section {edl['window']['start_s']:.2f}s to {edl['window']['end_s']:.2f}s of the full video;"
                " times below are within the section)" if edl["window"]["start_s"] or edl["test_seconds"] else ""), "",
             f"> {edl['honesty']}", "", "## Effects", "",
             "| # | time | category | file | level | confidence | why |", "|---|---|---|---|---|---|---|"]
    for e in edl["effects"]:
        lines.append(f"| {e['id']} | {e['event_time']:.2f}s | {e['category']} | {e['source_name']} | {e['gain_db']:+.1f} dB | "
                     f"{e['confidence']} | {e['reason']} |")
    if not edl["effects"]:
        lines.append("| - | - | - | none placed | - | - | see skipped list |")
    a = edl["analysis"]
    lines += ["", "## What the analysis saw", "",
              f"- Cuts: {len(a['cuts'])} (hard cuts only; dissolves and slow fades are mostly missed)",
              f"- Music: {edl['music_source']}; {a['onset_count']} onsets, {len(a['energy_rises'])} energy rises",
              f"- Tempo: {a['tempo_bpm']} BPM, confidence {a['tempo_confidence']}; beat grid {'used' if a['beats_used'] else 'not used (unreliable)'}",
              f"- Skipped candidates: {len(edl['skipped_candidates'])} (reasons in edit_decisions.json)", "",
              "## Mix", ""]
    for k, v in edl["mix"].items():
        lines.append(f"- {k}: {v}")
    if edl.get("licence_unverified"):
        lines += ["", "## ⚠️ Licence unverified: preview only", "",
                  "These sounds' licences could not be verified. Don't deliver this mix to a client until they're "
                  "swapped for owned sounds: " + ", ".join(edl["licence_unverified"])]
    lines += ["", "## Final Cut", "", f"- {edl['fcpxml_status']}"]
    if edl["missing_categories"]:
        lines += ["", "## Missing sound categories", "",
                  f"No usable sounds for: {', '.join(edl['missing_categories'])}. Nothing was downloaded or generated. "
                  "Add files with the category word in the name (e.g. `soft_shimmer_01.wav`) or a `name.wav.tags` sidecar."]
    lines += ["", "## Review", "", "- Watch the preview; mute any effect you don't like in FCP (each is its own clip, role *Effects*).",
              "- Re-run with `--seed N` for different file picks, or edit `asd.local.json` to change density and levels."]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Automatic first-pass sound design for real-estate videos.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="check Python, FFmpeg, FFprobe, numpy")
    m = sub.add_parser("manifest", help="index a sound-effects folder")
    m.add_argument("--sfx", required=True)
    m.add_argument("--search")
    m.add_argument("--export", help="also write the manifest JSON here")
    m.add_argument("--include-underscore", action="store_true", help="also index folders starting with _")
    p = sub.add_parser("process", help="make a sound-design pass for one video")
    p.add_argument("video")
    p.add_argument("--sfx", action="append", help="folder of sound effects (repeatable; default: sfx_folder in asd.local.json)")
    p.add_argument("--scenes", help="scene-map JSON (what each stretch shows) for scene ambience + accents")
    p.add_argument("--music", help="optional separate music file (analysis only; it is not added to the mix)")
    p.add_argument("--out", default=str(HERE / "output"))
    p.add_argument("--config")
    p.add_argument("--seed", type=int)
    p.add_argument("--test-seconds", type=float, help="only process N seconds (quick check)")
    p.add_argument("--start", type=float, help="start the test section here (moved back to the nearest keyframe)")
    p.add_argument("--no-xml", action="store_true")
    y = sub.add_parser("synth", help="make the free synthetic ambience + shimmer kit")
    y.add_argument("--out", default=str(HERE / "sfx" / "generated"))
    r = sub.add_parser("relink", help="re-point a run folder's FCPXML at this machine's paths")
    r.add_argument("run_dir")
    r.add_argument("--video", required=True, help="where the source video is on this machine")
    args = parser.parse_args(argv)
    try:
        return {"check": cmd_check, "manifest": cmd_manifest, "process": cmd_process, "relink": cmd_relink, "synth": cmd_synth}[args.command](args)
    except media.MediaError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
