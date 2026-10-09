# Synth SFX bed for the Empire CRUD cut, timed to graphics.html beats. 48k mono WAV.
import numpy as np, wave
SR = 48000; DUR = 22.5; out = np.zeros(int(SR * DUR)); rs = np.random.default_rng(3)
def add(t, s, gain=1.0):
    i = int(t * SR); n = min(len(s), len(out) - i); out[i:i + n] += s[:n] * gain
def env(n, a=.003, d=.2): t = np.arange(n) / SR; return np.minimum(t / a, 1) * np.exp(-t / d)
def lp(x, a):
    y = np.empty_like(x); p = 0.0
    for k in range(len(x)): p += a[k] * (x[k] - p); y[k] = p
    return y
def whoosh(d=.45):
    n = int(d * SR); u = np.linspace(0, 1, n)
    return lp(rs.standard_normal(n), .01 + .25 * np.sin(np.pi * u) ** 2) * np.sin(np.pi * u) ** 2 * 3
def tick(): n = int(.025 * SR); return lp(rs.standard_normal(n), np.full(n, .5)) * env(n, .0004, .004)
def blip(f, d=.08): n = int(d * 2 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * f * t) * env(n, .001, d / 3)
def thud(f=60, d=.4): n = int(d * 2 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (f + 90 * np.exp(-t * 25)) * t) * env(n, .002, d / 2)
def chime(f): n = int(1.2 * SR); t = np.arange(n) / SR; return (np.sin(2*np.pi*f*t) + .3*np.sin(2*np.pi*f*2.0*t)) * env(n, .003, .35)
def typing(t0, chars, cps):
    for i in range(chars): add(t0 + i / cps, tick(), .35)
# hook card
add(.05, blip(1200), .15); typing(.1, 9, 28); add(.3, whoosh(.3), .15)
add(2.8, thud(90, .2), .25)                      # strike
add(4.1, blip(880), .2)                           # built well
add(4.85, whoosh(.55), .55); add(5.3, thud(50, .5), .45)   # wipe to graphics
typing(5.42, 18, 28)
for i in range(4): add(5.42 + i * .1, blip(500 + i * 120), .2)
for at in (6.40, 6.60, 7.12, 7.68): add(at, whoosh(.18), .25)
for at in (8.0, 10.45, 15.0): add(at - .2, whoosh(.4), .4)
typing(8.04, 17, 28); add(8.62, thud(70, .3), .3); add(9.72, thud(70, .3), .3); typing(10.0, 4, 14)
typing(10.76, 16, 28); add(11.5, blip(700), .15); add(12.3, whoosh(.2), .2); typing(13.84, 10, 22); add(14.3, thud(60, .35), .4)
typing(15.02, 27, 28)
for i, at in enumerate((15.38, 16.62, 17.58, 18.38)): add(at, whoosh(.18), .2); add(at + .7, blip(880 + i * 110, .12), .25)
typing(19.0, 25, 28)
add(19.6, whoosh(.5), .5); add(20.0, thud(45, .8), .7); add(20.0, chime(587), .12); add(20.5, chime(880), .1)
for i in range(13): add(20.5 + i * .04, blip(1400 + i * 40, .03), .06)
out = np.tanh(out * 1.1); out *= .5 / max(np.abs(out).max(), 1e-6)
w = wave.open('build/sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
