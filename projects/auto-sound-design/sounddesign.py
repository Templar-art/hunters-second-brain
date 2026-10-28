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

from asd import analysis, fcpxml, library, media, mix, placement  # noqa: E402

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
    args.sfx = args.sfx or cfg.get("sfx_folder")
    if not args.sfx:
        raise media.MediaError('No sound-effects folder. Pass --sfx "/path/to/folder" or set "sfx_folder" in asd.local.json')
    video_path = Path(args.video).expanduser()
    video, flags = media.video_info(video_path)
    music_path = Path(args.music).expanduser() if args.music else None
    if music_path and not music_path.is_file():
        raise media.MediaError(f"Music file not found: {music_path}")
    limit = args.test_seconds
    if limit:
        cfg["_analysis_limit"] = limit
        if limit < video.duration:
            cfg["rules"]["outro_shimmer"] = False  # the test excerpt's last cut isn't the film's ending
    fd = video.frame_duration
    full = Fraction(video.frame_count) * fd
    seq_dur = min(full, placement.snap(limit, fd, "floor")) if limit else full
    seconds = float(seq_dur)

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    tag = f"_test{int(limit)}s" if limit else ""
    out_dir = Path(args.out).expanduser() / f"{video_path.stem}{tag}_{stamp}"
    out_dir.mkdir(parents=True, exist_ok=False)
    print(f"Video: {video.path.name}  {video.width}x{video.height}  {float(video.fps):.3f} fps ({video.fps})  "
          f"{video.duration:.2f}s  {video.frame_count} frames  tc {video.timecode or 'none'}")
    if flags["variable_frame_rate"]:
        print("  ! variable frame rate source: timing uses the nominal rate; check sync in FCP.")
    if limit:
        print(f"  Short test: first {seconds:.2f}s only")

    print("Indexing sound effects ...")
    man = library.build_manifest(args.sfx, cache_path=manifest_cache(args.sfx), log=lambda m: print(m),
                                 skip_underscore=cfg["library"]["skip_underscore_folders"])
    print(f"  {man['count']} sounds; " + ", ".join(f"{c} {n}" for c, n in man["category_counts"].items()))
    if man["count"] == 0:
        raise media.MediaError(f"No audio files found in {args.sfx}")

    print("Finding cuts ...")
    cuts = [c for c in analysis.detect_cuts(video, cfg["analysis"], limit=limit) if c.time < seconds]
    print(f"  {len(cuts)} cuts")
    print("Analysing music ...")
    if music_path:
        music = analysis.analyse_music(music_path, cfg["analysis"], limit=limit, label=f"separate music file: {music_path.name}")
    elif video.has_audio:
        music = analysis.analyse_music(video.path, cfg["analysis"], limit=limit, label="video's own audio track")
    else:
        music = analysis.MusicAnalysis(available=False, source="no audio")
    print(f"  {music.source}: {len(music.onsets)} onsets, {len(music.energy_rises)} energy rises, "
          f"tempo {music.tempo_bpm} BPM (confidence {music.tempo_confidence}, beats {'used' if music.beats_reliable else 'NOT used - unreliable'})")

    placements, skipped, missing = placement.place(cuts, music, video, man, cfg)
    library.save_manifest(man, manifest_cache(args.sfx))  # keep newly measured peak times
    print(f"Placed {len(placements)} effects ({len(skipped)} candidates skipped)")

    print("Rendering effects bus ...")
    clips = mix.render_clips(placements)
    source = media.decode_audio(video.path, rate=mix.RATE, channels=2, duration=seconds) if video.has_audio else None
    bus, preview_gain, mix_report = mix.balance(placements, clips, seconds, source, cfg)
    sfx_wav = out_dir / f"{video_path.stem}_sfx_only.wav"
    media.write_wav(sfx_wav, bus)
    if source is not None:
        n = min(len(source), len(bus))
        preview_audio = (source[:n] + bus[:n]) * 10 ** (preview_gain / 20)
    else:
        preview_audio = bus * 10 ** (preview_gain / 20)
    preview_wav = out_dir / ".preview_mix.wav"
    media.write_wav(preview_wav, preview_audio)
    ext = video_path.suffix.lower() if video_path.suffix.lower() in (".mov", ".mp4", ".m4v") else ".mov"
    preview = out_dir / f"{video_path.stem}_sfx_preview{ext}"
    media.mux_preview(video.path, preview_wav, preview, duration=seconds)
    preview_wav.unlink()

    xml_status = "skipped (--no-xml)"
    xml_path = None
    if not args.no_xml:
        sources = {s["path"]: s for s in man["sounds"]}
        project_name = f"{video_path.stem} - SFX pass {stamp}"
        xml = fcpxml.build(video, placements, sources, seq_dur, project_name, cfg["fcpxml"]["event_name"],
                           write_fades=cfg["fcpxml"]["write_fades"])
        xml_path = out_dir / f"{video_path.stem}_sfx.fcpxml"
        xml_path.write_text(xml, encoding="utf-8")
        ok, msg = fcpxml.validate(xml_path, DTD)
        xml_status = ("DTD-valid; " if ok else "DTD INVALID; ") + msg + ". NOT yet confirmed by a Final Cut import."

    edl = {
        "tool": "auto-sound-design",
        "version": 1,
        "created": dt.datetime.now().isoformat(timespec="seconds"),
        "video": {"path": str(video.path), "fps": str(video.fps), "frame_duration": f"{fd.numerator}/{fd.denominator}s",
                  "duration_s": video.duration, "frames": video.frame_count, "width": video.width, "height": video.height,
                  "timecode": video.timecode, "has_audio": video.has_audio, **flags},
        "processed_seconds": seconds,
        "test_seconds": limit,
        "music_source": music.source,
        "sfx_library": man["root"],
        "seed": cfg["seed"],
        "honesty": ("Placements are heuristic: they come from cut scores, music loudness and onsets. The tool does not "
                    "know what any shot shows (drone, room reveal, sun flare, twilight). SFX categories come from file "
                    "and folder names, not from listening. No dialogue detection, so nothing is ducked."),
        "analysis": {"cuts": [{"time": round(c.time, 4), "frame": c.frame, "score": round(c.score, 3)} for c in cuts],
                     "energy_rises": [{"time": round(a, 3), "rise_db": round(b, 2)} for a, b in music.energy_rises],
                     "tempo_bpm": music.tempo_bpm, "tempo_confidence": music.tempo_confidence,
                     "beats_used": music.beats_reliable, "onset_count": len(music.onsets)},
        "effects": [p.to_json() for p in placements],
        "skipped_candidates": skipped,
        "missing_categories": sorted(set(missing) | set(man["missing_categories"])),
        "mix": mix_report,
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


def report(edl):
    lines = [f"# Sound-design pass: {Path(edl['video']['path']).name}", "",
             f"Created {edl['created']} · seed {edl['seed']} · {edl['processed_seconds']:.2f}s processed"
             + (f" (short test of {edl['test_seconds']}s)" if edl["test_seconds"] else ""), "",
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
    p.add_argument("--sfx", help="folder of sound effects you own (default: sfx_folder in asd.local.json)")
    p.add_argument("--music", help="optional separate music file (analysis only; it is not added to the mix)")
    p.add_argument("--out", default=str(HERE / "output"))
    p.add_argument("--config")
    p.add_argument("--seed", type=int)
    p.add_argument("--test-seconds", type=float, help="only process the first N seconds (quick check)")
    p.add_argument("--no-xml", action="store_true")
    args = parser.parse_args(argv)
    try:
        return {"check": cmd_check, "manifest": cmd_manifest, "process": cmd_process}[args.command](args)
    except media.MediaError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
