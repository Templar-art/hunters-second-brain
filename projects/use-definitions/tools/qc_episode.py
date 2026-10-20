"""Automatic video QC for one episode render, reading its declared qcAllow windows from episode.js.

    python3 tools/qc_episode.py <episode-name> <version-label>     # e.g. bus-network v3

Runs gen-runner's edit-mode QC (FREEZE + LOOK@t continuity dips outside the allow windows) and
writes the contact sheet to episodes/<name>/build/<name>-<label>-qc.jpg.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNNER = os.path.join(os.path.dirname(ROOT), "gen-runner", "gen_runner.py")

ep, label = sys.argv[1], sys.argv[2]
d = os.path.join(ROOT, "episodes", ep)
src = open(os.path.join(d, "episode.js")).read()
m = re.search(r"qcAllow:\s*(\[.*?\]\s*\])\s*,", src, re.S)           # whole list, even across lines
if not m:
    raise SystemExit(f"{ep}: no qcAllow in episode.js — declare the deliberate transitions first")
wins = re.findall(r"\[\s*([\d.]+)\s*,\s*([\d.]+)\s*\]", m.group(1))
allow = ",".join(f"{a}-{b}" for a, b in wins)
print(f"{ep} {label}: {len(wins)} allow windows")
sys.exit(subprocess.call(["python3", RUNNER, "qc", os.path.join(d, f"{ep}-{label}.mp4"), "--edit", "--allow", allow,
                          "--sheet", os.path.join(d, "build", f"{ep}-{label}-qc.jpg")]))
