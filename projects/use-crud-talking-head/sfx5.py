# SFX bed for v3, timed to v3.html. 48k mono WAV → build/sfx5.wav
import numpy as np, wave
SR = 48000; DUR = 23.6; out = np.zeros(int(SR * DUR)); rs = np.random.default_rng(5)
def add(t, s, gain=1.0):
    i = int(t * SR); n = min(len(s), len(out) - i); out[i:i + n] += s[:n] * gain
def env(n, a=.003, d=.2): t = np.arange(n) / SR; return np.minimum(t / a, 1) * np.exp(-t / d)
def lp(x, a):
    y = np.empty_like(x); p = 0.0
    for k in range(len(x)): p += a[k] * (x[k] - p); y[k] = p
    return y
def whoosh(d=.45, bright=.25):
    n = int(d * SR); u = np.linspace(0, 1, n)
    return lp(rs.standard_normal(n), .01 + bright * np.sin(np.pi * u) ** 2) * np.sin(np.pi * u) ** 2 * 3
def tick(): n = int(.022 * SR); return lp(rs.standard_normal(n), np.full(n, .55)) * env(n, .0004, .0035)
def pop(f, d=.07): n = int(d * 2 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * f * (1 + 1.5 * np.exp(-t * 70)) * t) * env(n, .001, d / 3)
def thud(f=55, d=.4): n = int(d * 2 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (f + 90 * np.exp(-t * 25)) * t) * env(n, .002, d / 2)
def glass(n_tri=24, t0=0, span=.4):                                  # mosaic: cluster of tiny pops
    for i in range(n_tri): add(t0 + rs.random() * span, pop(1800 + rs.random() * 1600, .025), .05)
def typing(t0, chars, cps):
    for i in range(chars): add(t0 + i / cps, tick(), .28)
def shards(t0, n=6):
    add(t0, whoosh(.35, .35), .3)
    for i in range(n): add(t0 + .05 + i * .03, pop(900 + rs.random() * 600, .04), .06)
# title
typing(.1, 11, 22); add(.12, whoosh(.4), .35); add(.25, thud(60, .35), .45); shards(.25, 7); shards(.4, 3)
add(2.0, whoosh(.35), .3)                                           # title exits
add(2.35, whoosh(.3, .4), .3); typing(2.75, 13, 30); shards(2.45, 2) # lower third
for t in (2.22, 3.18, 3.60, 4.36): add(t, pop(1300, .03), .05)      # caption chunks
# mosaic → def card
add(4.55, whoosh(.6, .3), .55); glass(30, 4.62, .4); glass(30, 5.02, .4); add(5.1, thud(50, .4), .4)
typing(5.42, 26, 30); shards(5.1, 8)
add(6.2, whoosh(.45), .45)                                          # shrink to navy inset
typing(6.45, 15, 30)
for i, t in enumerate((6.40, 6.60, 7.12, 7.68)): add(t, pop(600 + i * 90, .06), .22); add(t, whoosh(.18, .4), .12)
add(7.95, whoosh(.35), .35); add(8.0, thud(70, .25), .25)           # punch-in cut
for t in (8.04, 9.04, 9.72): add(t, pop(1300, .03), .05)
add(9.88, thud(48, .5), .6); add(9.85, whoosh(.3, .4), .3); add(10.04, pop(1000, .06), .2)
add(10.35, whoosh(.55), .45)                                        # panel rises
for t in (10.46, 11.08, 12.30, 13.42, 14.30): add(t, pop(1300, .03), .05)
add(10.76, pop(700, .07), .18); add(10.9, pop(780, .07), .18); add(11.3, pop(520, .07), .15); typing(11.5, 8, 28)
add(13.84, thud(80, .25), .3); add(13.84, pop(1100, .05), .15); typing(14.0, 10, 28)
add(14.85, whoosh(.6), .5)                                          # panel takes over
add(15.15, pop(600, .08), .2); typing(15.3, 12, 30)
for i, t in enumerate((15.38, 16.62, 17.58, 18.38)): add(t - .05, whoosh(.25, .35), .25); add(t, pop(500 + i * 120, .07), .25)
add(15.5, pop(900, .05), .15); add(17.9, pop(1100, .05), .15); add(18.45, whoosh(.3, .5), .15); add(18.9, whoosh(.3), .2)
# whips + expand
add(6.0, whoosh(.3, .5), .45); add(7.8, whoosh(.4, .3), .4)
# terminal card
add(13.3, whoosh(.3, .4), .25); typing(13.6, 40, 34)
# whip to 200 OK
add(19.05, whoosh(.35, .5), .5); add(19.15, whoosh(.3, .4), .3); add(19.5, thud(70, .2), .25)
for i in range(10): add(19.3 + i * .035, tick(), .4)
add(19.65, pop(1500, .05), .2); typing(19.55, 30, 60)
# shatter → mosaic → end card
add(19.95, thud(45, .5), .5); glass(60, 19.95, .35)
add(19.95, whoosh(.6, .3), .5); glass(30, 20.0, .4); glass(30, 20.4, .4); add(20.45, thud(45, .8), .55)
typing(20.85, 28, 30); typing(21.5, 18, 30); shards(20.4, 8)
out = np.tanh(out * 1.1); out *= .5 / max(np.abs(out).max(), 1e-6)
w = wave.open('build/sfx5.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
