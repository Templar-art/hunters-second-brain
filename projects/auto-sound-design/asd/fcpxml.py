"""FCPXML exporter: a NEW event + project that references the source video and each effect
file in place (absolute file:// URLs). Nothing is copied and no existing library is touched;
Final Cut adds the event to whichever library is selected when you import.

Schema: FCPXML 1.10, the version Apple publishes in the developer docs (checked Oct 2026).
Final Cut Pro imports older FCPXML versions, so 1.10 is the conservative choice. All times
are exact rationals in seconds (e.g. 1001/30000s) so 23.976/29.97 timing doesn't drift."""

from fractions import Fraction
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import quoteattr

VERSION = "1.10"


def t(value):
    """Fraction seconds -> FCPXML time string."""
    value = Fraction(value)
    if value == 0:
        return "0s"
    if value.denominator == 1:
        return f"{value.numerator}s"
    return f"{value.numerator}/{value.denominator}s"


def file_url(path):
    return "file://" + quote(str(Path(path).resolve()), safe="/")


def format_name(video):
    """FCP's named formats (e.g. FFVideoFormat1080p2398). Only emitted for the common ones;
    otherwise the format is described by frameDuration/width/height alone."""
    rates = {Fraction(24000, 1001): "2398", Fraction(24): "24", Fraction(25): "25",
             Fraction(30000, 1001): "2997", Fraction(30): "30", Fraction(50): "50",
             Fraction(60000, 1001): "5994", Fraction(60): "60"}
    sizes = {(1920, 1080): "1080p", (3840, 2160): "2160p", (1280, 720): "720p"}
    if video.fps in rates and (video.width, video.height) in sizes:
        return f"FFVideoFormat{sizes[(video.width, video.height)]}{rates[video.fps]}"
    return None


def build(video, placements, sources, sequence_duration, project_name, event_name, write_fades=True):
    """sources: {path: {duration, channels, sample_rate}} for every effect file used."""
    fd = video.frame_duration
    start = video.start_tc
    fmt_name = format_name(video)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<!DOCTYPE fcpxml>", f'<fcpxml version="{VERSION}">', "  <resources>"]
    name_attr = f" name={quoteattr(fmt_name)}" if fmt_name else ""
    lines.append(f'    <format id="r1"{name_attr} frameDuration="{t(fd)}" width="{video.width}" height="{video.height}"/>')
    video_dur = Fraction(video.frame_count) * fd
    audio_attrs = (f' hasAudio="1" audioSources="1" audioChannels="{video.audio_channels}" audioRate="{video.audio_rate}"'
                   if video.has_audio else "")
    lines.append(f'    <asset id="r2" name={quoteattr(video.path.stem)} start="{t(start)}" duration="{t(video_dur)}" '
                 f'hasVideo="1" format="r1"{audio_attrs}>')
    lines.append(f'      <media-rep kind="original-media" src={quoteattr(file_url(video.path))}/>')
    lines.append("    </asset>")

    asset_ids = {}
    for p in placements:
        if p.source in asset_ids:
            continue
        rid = f"r{len(asset_ids) + 3}"
        asset_ids[p.source] = rid
        info = sources[p.source]
        dur = (Fraction(info["duration"]) / fd).__floor__() * fd
        lines.append(f'    <asset id="{rid}" name={quoteattr(Path(p.source).stem)} start="0s" duration="{t(dur)}" '
                     f'hasAudio="1" audioSources="1" audioChannels="{info["channels"]}" audioRate="{info["sample_rate"]}">')
        lines.append(f'      <media-rep kind="original-media" src={quoteattr(file_url(p.source))}/>')
        lines.append("    </asset>")
    lines.append("  </resources>")

    lines.append(f"  <event name={quoteattr(event_name)}>")
    lines.append(f"    <project name={quoteattr(project_name)}>")
    tc_format = "DF" if ";" in video.timecode else "NDF"
    lines.append(f'      <sequence format="r1" duration="{t(sequence_duration)}" tcStart="0s" tcFormat="{tc_format}" '
                 f'audioLayout="stereo" audioRate="48k">')
    lines.append("        <spine>")
    lines.append(f'          <asset-clip ref="r2" name={quoteattr(video.path.stem)} offset="0s" start="{t(start)}" '
                 f'duration="{t(sequence_duration)}" tcFormat="{tc_format}">')
    for p in placements:
        # Connected clips are positioned in the parent clip's own time, which begins at its
        # media start (the timecode), so the offset includes `start`.
        lines.append(f'            <asset-clip ref="{asset_ids[p.source]}" lane="{p.lane}" offset="{t(start + p.offset)}" '
                     f'name={quoteattr(f"{p.id} {p.category} - {p.source_name}")} start="0s" duration="{t(p.duration)}" '
                     f'audioRole="effects">')
        lines.append(f'              <note>{_esc(p.reason)} | confidence {p.confidence}</note>')
        fades = ""
        if write_fades:
            parts = []
            if p.fade_in > 0:
                parts.append(f'<fadeIn type="easeIn" duration="{t(_frames(p.fade_in, fd))}"/>')
            if p.fade_out > 0:
                parts.append(f'<fadeOut type="easeOut" duration="{t(_frames(p.fade_out, fd))}"/>')
            if parts:
                fades = f'<param name="amount">{"".join(parts)}</param>'
        lines.append(f'              <adjust-volume amount="{p.gain_db:+.2f}dB">{fades}</adjust-volume>')
        lines.append("            </asset-clip>")
    lines.append("          </asset-clip>")
    lines.append("        </spine>")
    lines.append("      </sequence>")
    lines.append("    </project>")
    lines.append("  </event>")
    lines.append("</fcpxml>")
    return "\n".join(lines) + "\n"


def _frames(seconds, fd):
    """Fade length rounded to whole frames, at least one frame."""
    return max(1, round(Fraction(seconds) / fd)) * fd


def _esc(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def validate(xml_path, dtd_path):
    """DTD validation with lxml if present, else xmllint. Returns (ok, message)."""
    try:
        from lxml import etree
        dtd = etree.DTD(str(dtd_path))
        doc = etree.parse(str(xml_path))
        if dtd.validate(doc):
            return True, f"valid against {Path(dtd_path).name} (lxml)"
        return False, "; ".join(str(e) for e in dtd.error_log.filter_from_errors()[:5])
    except ImportError:
        pass
    import shutil
    import subprocess
    if shutil.which("xmllint"):
        proc = subprocess.run(["xmllint", "--noout", "--dtdvalid", str(dtd_path), str(xml_path)], capture_output=True, text=True)
        return proc.returncode == 0, (f"valid against {Path(dtd_path).name} (xmllint)" if proc.returncode == 0 else proc.stderr.strip()[:600])
    return False, "no validator available (install lxml or xmllint)"
