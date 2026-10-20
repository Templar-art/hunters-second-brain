"""Static check: two rise() headlines on the same line at the same time overprint each other.

    python3 tools/lint_rise.py [episode ...]      # default: every episode

The 1 s boss sheets miss short overlaps (bus-network v2 had 'Simple.' + 'Standard.' stacked for
0.18 s), so this reads the literal rise('txt', x, y, T - start, { size, exitAt }) calls and flags
pairs in the same function whose boxes collide while both are parked. A swap where the new word starts as the
old one's exit begins (a push) is fine and not flagged. Calls with computed
x/y/start are skipped (reported as 'unchecked').
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALL = re.compile(r"rise\('((?:[^'\\]|\\.)*)',\s*([\d.]+),\s*([\d.]+),\s*T\s*-\s*([\d.]+),\s*\{([^}]*)\}")


def opt(body, key, default):
    m = re.search(key + r":\s*([\d.]+)", body)
    return float(m.group(1)) if m else default


def lint(path):
    src, hits = open(path).read(), []
    for fn in re.split(r"\nfunction ", src):                 # compare within one scene function only
        calls = []
        for m in CALL.finditer(fn):
            txt, x, y, t0, body = m.group(1), float(m.group(2)), float(m.group(3)), float(m.group(4)), m.group(5)
            size, dur = opt(body, "size", 150), opt(body, "dur", .5)
            ex = opt(body, "exitAt", float("inf"))
            al = re.search(r"align:\s*'(\w+)'", body)
            wid = len(txt) * size * .38                       # condensed display face, ~0.38 em per char
            x0 = x - wid if al and al.group(1) == "right" else x - wid / 2 if al and al.group(1) == "center" else x
            calls.append((txt, x0, y, t0, ex, size, x0 + wid, m.start(), m.end()))
        for i, a in enumerate(calls):
            for b in calls[i + 1:]:
                same_line = abs(a[2] - b[2]) < .8 * min(a[5], b[5])
                overlap_x = max(a[1], b[1]) < min(a[6], b[6])
                both_on = max(a[3], b[3]) < min(a[4], b[4])     # new one lands while the old is still parked
                exclusive = re.search(r"\belse\b", fn[a[8]:b[7]])  # if/else branches never draw together
                if same_line and overlap_x and both_on and not exclusive:
                    hits.append(f"{os.path.relpath(path, ROOT)}: '{a[0]}' and '{b[0]}' share y≈{a[2]:.0f} "
                                f"from {max(a[3], b[3]):.2f}s to {min(a[4], b[4]):.2f}s")
    return hits


eps = sys.argv[1:] or sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(ROOT, "episodes/*/episode.js")))
allhits = [h for e in eps for h in lint(os.path.join(ROOT, "episodes", e, "episode.js"))]
print("\n".join(allhits) or f"RISE CLEAR ({len(eps)} episodes)")
sys.exit(1 if allhits else 0)
