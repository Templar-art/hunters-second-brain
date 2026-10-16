"""Align ASR token timestamps (sherpa-onnx zipformer) to the cleaned transcript.
usage: align_words.py tokens.json out.json  -> [{text,start,end}] in edit-timeline seconds"""
import json, sys, difflib, re
SCRIPT = ("Hey guys, if you're seeing this, you do not follow me yet. So let me tell you a little bit about myself. "
          "My name is Tyson. I'm a fitness and nutrition coach on the Gold Coast. I've been training for about 9 years now. "
          "I also work full time at a hotel. On my page, I'll be sharing things that took me 9 years to learn, "
          "so you can skip all the mistakes I made along the way and you'll get there faster. "
          "So now you know who I am, hit follow and I'll see you in the next one.")
END = float(sys.argv[3]) if len(sys.argv) > 3 else None
toks = json.load(open(sys.argv[1]))
asr = []
for tok, t in toks:
    if tok.startswith(' ') or not asr:
        asr.append([tok.strip(), t])
    else:
        asr[-1][0] += tok
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower().replace('9', 'nine'))
words = SCRIPT.split()
sm = difflib.SequenceMatcher(None, [norm(w) for w in words], [norm(w) for w, _ in asr], autojunk=False)
start = [None] * len(words)
for a, b, n in sm.get_matching_blocks():
    for k in range(n):
        start[a + k] = asr[b + k][1]
# fill gaps (ASR misses / mishears) by interpolation
known = [i for i, s in enumerate(start) if s is not None]
for i in range(len(words)):
    if start[i] is None:
        prev = max([k for k in known if k < i], default=None)
        nxt = min([k for k in known if k > i], default=None)
        if prev is not None and nxt is not None:
            start[i] = start[prev] + (start[nxt] - start[prev]) * (i - prev) / (nxt - prev)
        elif prev is not None:
            start[i] = start[prev] + 0.28 * (i - prev)
        else:
            start[i] = 0
out = []
for i, w in enumerate(words):
    nxt = start[i + 1] if i + 1 < len(words) else start[i] + 0.4
    out.append({'text': w, 'start': round(start[i], 3), 'end': round(min(nxt, start[i] + 0.7), 3)})
json.dump(out, open(sys.argv[2], 'w'), indent=0)
print(sum(s is not None for s in start), 'of', len(words), 'words;', len(known), 'matched by ASR')
