"""FFprobe/FFmpeg wrappers. Every call passes arguments as a list (no shell), so paths with
spaces, apostrophes or brackets are safe."""

import json
import shutil
import subprocess
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np


class MediaError(RuntimeError):
    pass


def require_tools():
    missing = [tool for tool in ("ffmpeg", "ffprobe") if shutil.which(tool) is None]
    if missing:
        raise MediaError(
            f"Missing {', '.join(missing)}. On a Mac: install Homebrew (https://brew.sh), "
            "then run: brew install ffmpeg"
        )


def _run(cmd, binary=False):
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", "replace").strip().splitlines()[-5:]
        raise MediaError(f"{Path(cmd[0]).name} failed: " + " | ".join(err))
    return proc.stdout if binary else proc.stdout.decode("utf-8", "replace")


def probe(path):
    path = Path(path)
    if not path.is_file():
        raise MediaError(f"File not found: {path}")
    out = _run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)])
    return json.loads(out)


def parse_rate(text):
    """'30000/1001' -> Fraction(30000, 1001). Returns None for 0/0 or missing."""
    if not text or text in ("0/0", "0"):
        return None
    rate = Fraction(text)
    return rate if rate > 0 else None


def parse_timecode(tc, fps):
    """'01:00:00:00' (or ';' for drop frame) -> seconds as Fraction, at the clip's frame rate.
    Drop-frame is converted with the standard 29.97/59.94 frame-dropping rule."""
    if not tc:
        return Fraction(0)
    drop = ";" in tc
    hh, mm, ss, ff = (int(x) for x in tc.replace(";", ":").split(":"))
    nominal = round(float(fps))
    frames = ((hh * 60 + mm) * 60 + ss) * nominal + ff
    if drop and nominal in (30, 60):
        dropped = 2 if nominal == 30 else 4
        total_minutes = hh * 60 + mm
        frames -= dropped * (total_minutes - total_minutes // 10)
    return frames / Fraction(fps)


@dataclass
class VideoInfo:
    path: Path
    duration: float
    fps: Fraction
    frame_count: int
    width: int
    height: int
    has_audio: bool
    audio_rate: int
    audio_channels: int
    timecode: str
    start_tc: Fraction  # media start in seconds (from the timecode tag; 0 for most exports)
    codec: str

    @property
    def frame_duration(self):
        return 1 / self.fps


def video_info(path):
    data = probe(path)
    video = next((s for s in data["streams"] if s.get("codec_type") == "video"), None)
    if video is None:
        raise MediaError(f"No video stream in {path}")
    audio = next((s for s in data["streams"] if s.get("codec_type") == "audio"), None)
    fps = parse_rate(video.get("r_frame_rate")) or parse_rate(video.get("avg_frame_rate"))
    if fps is None:
        raise MediaError(f"Could not read a frame rate from {path}")
    avg = parse_rate(video.get("avg_frame_rate"))
    if avg and abs(float(avg) - float(fps)) > 0.01:
        # Variable frame rate (phone footage). Timing is still rational, but warn upstream.
        pass
    duration = float(video.get("duration") or data["format"].get("duration") or 0)
    if duration <= 0:
        raise MediaError(f"Could not read a duration from {path}")
    frame_count = int(video["nb_frames"]) if str(video.get("nb_frames", "")).isdigit() else int(duration * fps)
    tags = {**data["format"].get("tags", {}), **video.get("tags", {})}
    tc = tags.get("timecode", "")
    if not tc:
        tc_stream = next((s for s in data["streams"] if s.get("tags", {}).get("timecode")), None)
        tc = tc_stream["tags"]["timecode"] if tc_stream else ""
    return VideoInfo(
        path=Path(path).resolve(),
        duration=duration,
        fps=fps,
        frame_count=frame_count,
        width=int(video.get("width", 1920)),
        height=int(video.get("height", 1080)),
        has_audio=audio is not None,
        audio_rate=int(audio.get("sample_rate", 48000)) if audio else 48000,
        audio_channels=int(audio.get("channels", 2)) if audio else 0,
        timecode=tc,
        start_tc=parse_timecode(tc, fps),
        codec=video.get("codec_name", ""),
    ), {"variable_frame_rate": bool(avg and abs(float(avg) - float(fps)) > 0.01)}


def audio_info(path):
    data = probe(path)
    audio = next((s for s in data["streams"] if s.get("codec_type") == "audio"), None)
    if audio is None:
        raise MediaError(f"No audio stream in {path}")
    duration = float(audio.get("duration") or data["format"].get("duration") or 0)
    return {
        "duration": duration,
        "sample_rate": int(audio.get("sample_rate", 0)),
        "channels": int(audio.get("channels", 0)),
        "codec": audio.get("codec_name", ""),
    }


def decode_audio(path, rate=48000, channels=2, start=None, duration=None):
    """Decode any audio/video file's first audio stream to float32, shape (samples, channels)."""
    cmd = ["ffmpeg", "-v", "error", "-nostdin"]
    if start is not None:
        cmd += ["-ss", f"{start:.6f}"]
    cmd += ["-i", str(path)]
    if duration is not None:
        cmd += ["-t", f"{duration:.6f}"]
    cmd += ["-map", "0:a:0", "-vn", "-ac", str(channels), "-ar", str(rate), "-f", "f32le", "-"]
    raw = _run(cmd, binary=True)
    return np.frombuffer(raw, dtype="<f4").reshape(-1, channels).copy()


def scene_scores(path, duration=None, width=256, start=None):
    """Per-frame scene-change score (0..1) from FFmpeg's select filter, on a downscaled copy.
    Times are relative to `start` when one is given."""
    cmd = ["ffmpeg", "-v", "error", "-nostdin"]
    if start:
        cmd += ["-ss", f"{start:.6f}"]
    cmd += ["-i", str(path)]
    if duration is not None:
        cmd += ["-t", f"{duration:.6f}"]
    cmd += [
        "-map", "0:v:0", "-an",
        "-vf", f"scale={width}:-2,select='gte(scene,0)',metadata=print:key=lavfi.scene_score:file=-",
        "-f", "null", "-",
    ]
    out = _run(cmd)
    times, scores = [], []
    current = None
    for line in out.splitlines():
        if line.startswith("frame:"):
            for part in line.split():
                if part.startswith("pts_time:"):
                    current = float(part.split(":", 1)[1])
        elif line.startswith("lavfi.scene_score=") and current is not None:
            times.append(current)
            scores.append(float(line.split("=", 1)[1]))
            current = None
    return np.array(times), np.array(scores)


def write_wav(path, samples, rate=48000):
    """Write float32 (samples, channels) to 24-bit PCM WAV via FFmpeg."""
    samples = np.ascontiguousarray(samples, dtype="<f4")
    channels = samples.shape[1]
    cmd = [
        "ffmpeg", "-v", "error", "-nostdin", "-y",
        "-f", "f32le", "-ar", str(rate), "-ac", str(channels), "-i", "-",
        "-c:a", "pcm_s24le", str(path),
    ]
    proc = subprocess.run(cmd, input=samples.tobytes(), capture_output=True)
    if proc.returncode != 0:
        raise MediaError("ffmpeg WAV write failed: " + proc.stderr.decode("utf-8", "replace")[-400:])


def keyframes(path):
    """Keyframe times (seconds) of the first video stream."""
    out = _run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-skip_frame", "nokey",
                "-show_entries", "frame=pts_time", "-of", "csv=p=0", str(path)])
    return [float(x.strip(",")) for x in out.split() if x.strip(",")]


def mux_preview(video_path, audio_wav, out_path, duration=None, start=None):
    """Copy the picture untouched and lay the preview mix underneath as AAC.
    `start` must be a keyframe so the stream copy begins exactly there."""
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-y"]
    if start:
        cmd += ["-ss", f"{start:.6f}"]
    cmd += ["-i", str(video_path), "-i", str(audio_wav)]
    if duration is not None:
        cmd += ["-t", f"{duration:.6f}"]
    cmd += ["-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", str(out_path)]
    _run(cmd)
