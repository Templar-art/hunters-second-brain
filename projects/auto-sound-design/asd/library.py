"""Sound-effect manifest. Categories come from words in filenames, folder names, sidecar
tag files and catalog CSVs. That is text matching, not listening: a file called
"soft_whoosh.wav" is assumed to be a whoosh. The manifest records where each tag came from."""

import csv
import json
import re
from pathlib import Path

import numpy as np

from . import media

AUDIO_EXT = {".wav", ".aif", ".aiff", ".mp3", ".m4a", ".flac", ".caf", ".ogg"}

CATEGORIES = ["whoosh", "riser", "impact", "low drone", "shimmer", "ambience"]

# Word -> category. Matched against whole tokens, so "hit" doesn't fire on "white".
KEYWORDS = {
    "whoosh": ["whoosh", "woosh", "swoosh", "swish", "swipe", "whip", "passby", "pass", "flyby", "transition", "zip"],
    "riser": ["riser", "rise", "rising", "uplifter", "build", "buildup", "swell", "tension", "upsweep", "reverse"],
    "impact": ["impact", "hit", "boom", "slam", "thud", "punch", "braam", "stomp", "drop", "subdrop", "kick", "hits"],
    "low drone": ["drone", "rumble", "sub", "low", "pad", "dark"],
    "shimmer": ["shimmer", "sparkle", "chime", "chimes", "glitter", "twinkle", "magic", "glint", "shine", "bell", "bells", "glisten"],
    "ambience": ["ambience", "ambiance", "ambient", "atmos", "atmosphere", "roomtone", "room", "birds", "rain", "forest", "city", "wind", "waves", "nature", "rainforest", "cityscape", "cityscapes"],
}
TOKEN_TO_CATEGORY = {word: cat for cat, words in KEYWORDS.items() for word in words}

CATALOG_NAMES = {"catalog.csv", "tags.csv"}


def tokens(text):
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)  # camelCase -> camel Case
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if t]


def categorise(words):
    """Score each category by keyword hits. Returns categories, best first."""
    scores = {}
    for word in words:
        cat = TOKEN_TO_CATEGORY.get(word)
        if cat:
            scores[cat] = scores.get(cat, 0) + 1
    return sorted(scores, key=lambda c: (-scores[c], CATEGORIES.index(c)))


def _load_catalogs(root):
    """path -> extra words, from any catalog.csv / tags.csv under the library root.
    Accepts any column whose name contains 'path' or 'file'; every other column is text."""
    extra = {}
    for catalog in root.rglob("*.csv"):
        if catalog.name.lower() not in CATALOG_NAMES:
            continue
        try:
            with catalog.open(newline="", encoding="utf-8-sig") as handle:
                for row in csv.DictReader(handle):
                    key = next((k for k in row if k and ("path" in k.lower() or "file" in k.lower())), None)
                    if not key or not row[key]:
                        continue
                    target = Path(row[key])
                    if not target.is_absolute():
                        target = (catalog.parent / target)
                    words = " ".join(str(v) for k, v in row.items() if k != key and v)
                    extra[str(target.resolve())] = (words, str(catalog))
        except (OSError, csv.Error, UnicodeDecodeError):
            continue
    return extra


def _sidecar(path):
    """'boom.wav.tags' or 'boom.tags' (comma/space separated), or 'boom.json' {"tags": [...], "category": "..."}."""
    for candidate in (path.with_name(path.name + ".tags"), path.with_suffix(".tags")):
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8", errors="replace"), None, str(candidate)
    candidate = path.with_suffix(".json")
    if candidate.is_file():
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
            return " ".join(data.get("tags", [])), data.get("category"), str(candidate)
        except (ValueError, AttributeError):
            pass
    return "", None, None


def build_manifest(root, cache_path=None, log=print, skip_underscore=True):
    """Index every audio file under root. Folders starting with '_' (e.g. _docs, _Archives,
    _magnific rejects) are skipped by default: in Hunter's libraries that prefix means "not for use"."""
    root = Path(root).expanduser()
    if not root.is_dir():
        raise media.MediaError(f"Sound-effects folder not found: {root}")
    cache = {}
    if cache_path and Path(cache_path).is_file():
        try:
            cache = {e["path"]: e for e in json.loads(Path(cache_path).read_text())["sounds"]}
        except (ValueError, KeyError):
            cache = {}
    catalogs = _load_catalogs(root)
    files = sorted(p for p in root.rglob("*") if p.suffix.lower() in AUDIO_EXT and p.is_file() and not p.name.startswith("._")
                   and not (skip_underscore and any(part.startswith("_") for part in p.relative_to(root).parts[:-1])))
    sounds = []
    for n, path in enumerate(files):
        resolved = str(path.resolve())
        stat = path.stat()
        cached = cache.get(resolved)
        if cached and cached.get("mtime") == stat.st_mtime and cached.get("size") == stat.st_size:
            info = {k: cached[k] for k in ("duration", "sample_rate", "channels")}
            analysis = cached.get("analysis")
        else:
            try:
                info = media.audio_info(path)
                info.pop("codec", None)
            except media.MediaError as exc:
                log(f"  skip (unreadable): {path.name}: {exc}")
                continue
            analysis = None
        if n and n % 200 == 0:
            log(f"  indexed {n}/{len(files)}")

        rel = path.relative_to(root)
        sources = {}
        file_words = tokens(path.stem)
        folder_words = [w for part in rel.parts[:-1] for w in tokens(part)]
        side_text, side_cat, side_file = _sidecar(path)
        side_words = tokens(side_text)
        cat_text, cat_file = catalogs.get(resolved, ("", None))
        catalog_words = tokens(cat_text)

        if side_cat and side_cat in CATEGORIES:
            categories, category_source = [side_cat], "sidecar category"
        else:
            # Most specific evidence first: sidecar, then catalog, then filename, then folders.
            categories, category_source = [], None
            for label, words in (("sidecar tags", side_words), ("catalog", catalog_words), ("filename", file_words), ("folder", folder_words)):
                found = categorise(words)
                if found:
                    categories, category_source = found, label
                    break
        if side_file:
            sources["sidecar"] = side_file
        if cat_file:
            sources["catalog"] = cat_file
        all_words = sorted(set(file_words + folder_words + side_words + catalog_words))
        sounds.append({
            "path": resolved,
            "name": path.name,
            "relative": str(rel),
            "duration": round(info["duration"], 4),
            "sample_rate": info["sample_rate"],
            "channels": info["channels"],
            "categories": categories,
            "category": categories[0] if categories else None,
            "category_source": category_source,
            "is_loop": "loop" in all_words or "loops" in all_words,
            "tags": all_words,
            "tag_sources": sources,
            "mtime": stat.st_mtime,
            "size": stat.st_size,
            "analysis": analysis,
        })
    counts = {cat: sum(1 for s in sounds if cat in s["categories"]) for cat in CATEGORIES}
    manifest = {
        "root": str(root.resolve()),
        "skipped_underscore_folders": skip_underscore,
        "count": len(sounds),
        "category_counts": counts,
        "missing_categories": [c for c, n in counts.items() if n == 0],
        "uncategorised": sum(1 for s in sounds if not s["categories"]),
        "note": "Categories are guessed from words in names, folders, sidecars and catalogs, not from listening to the audio.",
        "sounds": sounds,
    }
    if cache_path:
        save_manifest(manifest, cache_path)
    return manifest


def save_manifest(manifest, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(manifest, indent=1))


def search(manifest, query):
    words = tokens(query)
    hits = [s for s in manifest["sounds"] if all(any(w in t for t in s["tags"]) or w in s.get("categories", []) for w in words)]
    return hits


def sound_shape(sound):
    """Peak and onset times + active loudness, measured from the file itself (cached in the manifest).
    Used to line a whoosh's loudest moment up with a cut."""
    if sound.get("analysis") and "attack_s" in sound["analysis"]:
        return sound["analysis"]
    rate = 48000
    audio = media.decode_audio(sound["path"], rate=rate, channels=1)[:, 0]
    if len(audio) == 0:
        raise media.MediaError(f"Empty audio: {sound['path']}")
    hop = rate // 100  # 10 ms
    n = max(1, len(audio) // hop)
    env = np.sqrt(np.mean(audio[: n * hop].reshape(n, hop) ** 2, axis=1)) if len(audio) >= hop else np.array([np.sqrt(np.mean(audio ** 2))])
    env_db = 20 * np.log10(env + 1e-9)
    peak_i = int(np.argmax(env))
    above = np.nonzero(env_db >= env_db[peak_i] - 24)[0]
    onset_i = int(above[0]) if len(above) else 0
    # Attack: the sharpest 30 ms jump among the loud part. For a "whoosh into hit" that's the hit,
    # not the start of the whoosh; for a plain boom it's the transient.
    jump = np.full(len(env_db), -np.inf)
    jump[3:] = env_db[3:] - env_db[:-3]
    jump[env_db < env_db[peak_i] - 12] = -np.inf
    jump[peak_i + 1:] = -np.inf  # the attack comes before (or at) the loudest moment
    attack_i = max(0, int(np.argmax(jump)) - 1) if np.isfinite(jump).any() else onset_i
    active = env_db >= env_db[peak_i] - 30
    active_rms = 10 * np.log10(np.mean(env[active] ** 2) + 1e-12) if active.any() else float(env_db.max())
    sound["analysis"] = {
        "peak_s": round(peak_i * hop / rate + hop / rate / 2, 4),
        "onset_s": round(onset_i * hop / rate, 4),
        "attack_s": round(attack_i * hop / rate, 4),
        "peak_db": round(float(20 * np.log10(np.abs(audio).max() + 1e-9)), 2),
        "rms_db": round(float(active_rms), 2),
    }
    return sound["analysis"]
