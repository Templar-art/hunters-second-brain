"""Strategic Investing / Brian ads: build A/B cam cuts from one continuous two-camera take.

Selections = (A-cam window start, end, phrase). The phrase is snapped onto the FCP
transcript words inside the window (last best match), padded, edge-snapped to quiet.
Audio always A-cam (lav). Camera alternates every take change so jump cuts are hidden.
Outputs: one FCPXML with 10 projects + per-script picks report.
"""
import json, re, difflib, wave, sys
import numpy as np
from pathlib import Path

S = Path(sys.argv[1])  # scratch dir with fcpwl.json + a.wav
OUT = Path(__file__).parent
FPS = 25
B_OFF = 63.52  # A time = B time + B_OFF (audio xcorr, 63.527 s, stable over clip)
A_TC = ((12*3600 + 6*60 + 57)*FPS + 3)   # 12:06:57:03
B_TC = ((16*3600 + 7*60 + 31)*FPS + 5)   # 16:07:31:05
A_SRC = "file:///Volumes/Kristian%20T7/Brian%20Ads/A7siii%201/C8202.MP4"
B_SRC = "file:///Volumes/Kristian%20T7/Brian%20Ads/A7siii%202/C9731.MP4"
A_DUR, B_DUR = 1224.0, 1170.24

SCRIPTS = {
 "01 Another rate rise": [
  (154.0, 156.8, "The RBA just raised the cash rate again"),
  (173.6, 176.4, "So when did you last review your property plan"),
  (187.4, 188.5, "higher repayments"),
  (194.0, 195.5, "Less breathing room"),
  (199.0, 201.6, "And the same strategy you put together years ago"),
  (224.3, 227.0, "You can't control the next rate decision"),
  (231.3, 234.0, "But you can review your debt"),
  (233.4, 236.1, "Your cash flow"),
  (243.5, 246.2, "And what your property can realistically support"),
  (533.5, 535.7, "I'm Brian from Strategic Investing"),  # S1 take said "Investor in Queensland"; borrowed S3 ID line
  (257.4, 260.2, "before you make your next property move"),
  (270.8, 273.3, "get in touch and let's discuss your options"),
 ],
 "02 Rent doesn't tell the whole story": [
  (301.6, 303.7, "The rent lands in your account"),
  (305.1, 306.6, "Then the mortgage comes out"),
  (308.7, 310.3, "How much is actually left"),
  (352.9, 355.1, "With the latest rate rise"),
  (374.0, 377.3, "The purchase price and the rental income"),
  (377.6, 378.6, "Isn't enough"),
  (380.1, 381.4, "To judge an investment"),
  (408.6, 412.9, "Insurance maintenance and vacancies"),
  (417.0, 419.3, "The numbers need to work after those costs"),
  (422.5, 423.5, "Not before"),
  (461.5, 463.1, "At strategic investing"),
  (465.0, 466.4, "We help property investors"),
  (467.0, 468.7, "Look at their property"),
  (469.3, 470.4, "and equity"),
  (479.1, 480.7, "In context their goals"),
  (481.8, 485.7, "Get in touch before your next move"),
 ],
 "03 A mortgage isn't a strategy": [
  (493.6, 494.8, "You've got a mortgage"),
  (497.5, 499.8, "That doesn't mean you've got a property strategy"),
  (503.3, 505.0, "A loan tells you what you owe"),
  (509.3, 512.1, "A strategy as you what are you trying to achieve"),
  (514.1, 515.3, "What can you afford"),
  (517.5, 519.8, "And what happens if things don't go as planned"),
  (523.5, 526.4, "Buying another property isn't automatically the answer"),
  (528.6, 530.6, "Neither is leaving everything untouched"),
  (533.5, 535.7, "I'm Brian from Strategic Investing"),
  (556.4, 559.3, "We help homeowners and investors"),
  (563.8, 566.3, "explore their property and"),
  (566.9, 567.9, "equity options"),
  (569.3, 570.5, "Let's talk about yours"),
 ],
 "04 Property value doesn't pay the bills": [
  (601.7, 604.8, "A higher property value isn't going to help you pay off your mortgage"),
  (609.9, 612.9, "That's the difference between having equity and cash flow"),
  (616.1, 618.3, "Before you borrow against your home"),
  (626.1, 628.0, "You need to understand what"),
  (628.9, 632.2, "the extra repayments would mean for you"),
  (634.1, 637.1, "And your everyday life"),
  (649.1, 650.9, "Not just what you can buy with the money"),
  (653.4, 655.4, "Equity could create options"),
  (664.3, 668.7, "But accessing it means taking on more debt"),
  (670.4, 672.2, "That's strategic investing"),
  (673.5, 675.2, "We help you explore those options"),
  (676.0, 677.2, "Get in touch"),
 ],
 "05 Equity isn't free money": [
  (694.4, 695.9, "Just use your equity"),
  (699.1, 700.9, "That's easy advice to give"),
  (707.2, 708.8, "when it's not your home on the line"),
  (713.9, 715.4, "Equity isn't free money"),
  (718.7, 721.2, "Accessing it through a loan means more debt"),
  (722.4, 724.0, "More repayments"),
  (724.8, 726.2, "And more responsibility"),
  (728.2, 729.9, "The question isn't just"),
  (731.6, 733.1, "How much can I access"),
  (752.4, 753.6, "What would I use it for"),
  (756.3, 757.9, "And can I afford the risk"),
  (760.3, 762.4, "I'm Brian from Strategic investing"),
  (764.5, 765.8, "before you use your equity"),
  (767.3, 768.8, "Let's discuss your options"),
 ],
 "06 Waiting for a rate cut": [
  (783.9, 785.4, "Waiting for a rate cut"),
  (787.3, 788.7, "Isn't property strategy"),
  (792.0, 794.6, "A rate cut might ease the repayments"),
  (801.3, 805.0, "It won't tell you whether your next property"),
  (810.6, 812.6, "actually stacks up"),
  (814.7, 817.1, "Before you borrow more"),
  (817.7, 819.0, "Look at the repayments"),
  (820.4, 821.9, "The ongoing costs"),
  (832.2, 834.7, "And what happens if rates stay higher than you hoped"),
  (837.9, 839.5, "Equity can give you options"),
  (845.4, 847.7, "Using it means taking on more debt"),
  (853.2, 855.3, "I'm Brian from Strategic Investing"),
  (856.6, 859.4, "Before your next move get in touch"),
  (860.2, 861.9, "And let's discuss your options"),
 ],
 "07 Only works when everything goes right": [
  (868.5, 873.6, "If your investment only works When everything goes right"),
  (875.0, 876.6, "What happens when nothing goes right"),
  (879.9, 881.3, "The tenant leaves"),
  (882.3, 884.0, "A repair comes up"),
  (889.2, 891.5, "Or interest rates stay higher than expected"),
  (893.6, 895.3, "Before you add another property"),
  (901.4, 908.6, "Look at whether Your cash flow Can handle those things happening together"),
  (923.3, 924.5, "The next purchase"),
  (925.5, 928.7, "Shouldn't depend on a perfect run"),
  # S7 own CTA ("At SI we help investors... with risk in view") = 1 s fragments, unreliable -> borrowed ID line
  (533.5, 535.7, "I'm Brian from Strategic Investing"),
  (944.2, 945.2, "Get in touch"),
 ],
 "08 Don't collect properties": [
  (973.0, 975.3, "A second property isn't a trophy"),
  (976.9, 978.8, "It's another financial commitment"),
  (982.0, 983.3, "Before you buy"),
  (986.6, 988.8, "Ask what it actually means for you"),
  (993.0, 995.3, "is it building long term wealth"),
  (998.9, 1000.4, "to support future income"),
  (1007.5, 1009.4, "Does it fit a particular timeline"),
  # dropped: "Then ask whether the repayments, costs and risks fit your life" - no clean take
  (1026.5, 1027.7, "Using equity"),
  (1042.3, 1043.4, "Because it's available"),
  (1044.5, 1045.5, "Isn't the same"),
  (1046.3, 1047.5, "As using it"),
  (1048.2, 1049.0, "With purpose"),
  (1053.3, 1055.3, "I'm Brian from Strategic Investing"),
  (1061.2, 1063.5, "Let's discuss the plan before the purchase"),
 ],
 "09 Can borrow vs should borrow": [
  (1070.5, 1072.4, "The biggest loan you can get"),
  (1074.4, 1076.9, "Isn't necessarily the right one"),
  (1080.7, 1082.0, "A borrowing limit"),
  (1083.1, 1088.6, "Doesn't tell you how much breathing room you want"),
  (1093.0, 1094.3, "What else you're planning"),
  (1097.5, 1099.6, "Oh how comfortable you are with risk"),
  (1102.9, 1104.6, "Before you use your property"),
  (1106.2, 1107.8, "To take on more debt"),
  (1112.7, 1114.8, "Decide what you're willing to commit to"),
  # dropped: "Not just what might get approved" - only stuttered takes
  (1131.4, 1133.1, "That's strategic investing"),
  (1134.3, 1135.6, "We help homeowners"),
  (1136.3, 1137.5, "And investors"),
  (1138.3, 1139.4, "Explore their options"),
  (1140.4, 1141.4, "Get in touch"),
 ],
 "10 The missing exit plan": [
  (1152.5, 1154.3, "You thought about buying the next property"),
  (1161.5, 1164.0, "you thought about how you eventually gonna get out"),
  (1173.5, 1177.6, "Holding cuffs don't stop"),
  (1177.4, 1179.7, "Just because your plans change"),
  (1181.8, 1183.3, "And selling takes time"),
  (1184.1, 1185.2, "And costs money"),
  (1187.7, 1190.4, "Before you use equity to invest"),
  (1192.0, 1193.6, "Think beyond the purchase"),
  (1196.0, 1197.5, "How long could you hold it"),
  (1200.0, 1201.5, "And what would make you sell"),
  (1204.1, 1206.1, "What happens if you need the money sooner"),
  (1211.3, 1213.7, "I'm Brian from Strategic investing"),
  (1216.4, 1219.3, "And let's discuss your options before you commit"),
 ],
}

W = json.load(open(S / "fcpwl.json"))
wv = wave.open(str(S / "a.wav")); AUD = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(float)
norm = lambda t: re.sub(r"[^a-z']", "", t.lower())

def energy(t):
    x = AUD[int(t*16000):int(t*16000)+320]
    return np.sqrt((x**2).mean()) if len(x) else 0

def quiet_snap(t, lo, hi):
    """move t to quietest 20 ms point within [t+lo, t+hi]"""
    cands = np.arange(t+lo, t+hi, 0.01)
    return float(min(cands, key=energy))

QUIET_DB = 36.0
def db(t0, t1):
    x = AUD[int(t0*16000):int(t1*16000)]
    return 20*np.log10(np.sqrt((x**2).mean())+1e-9) if len(x) else 0
def tail(t, d, limit):
    """walk from t in direction d until a 150 ms window is quiet; stop at limit; add 60 ms air"""
    while (t < limit if d > 0 else t > limit):
        w = (t, t+0.15) if d > 0 else (t-0.15, t)
        if db(*w) < QUIET_DB: break
        t += 0.01*d
    t += 0.06*d
    return min(t, limit) if d > 0 else max(t, limit)

def pick(s, e, phrase):
    ws = [w for w in W if w[0] >= s-0.2 and w[1] <= e+0.3]
    target = [norm(x) for x in phrase.split()]
    n = len(target); best = None
    for i in range(len(ws)):
        for L in (n-1, n, n+1):
            if L < 1 or i+L > len(ws): continue
            cand = [norm(w[2]) for w in ws[i:i+L]]
            r = difflib.SequenceMatcher(None, cand, target).ratio()
            if best is None or r >= best[0] - 1e-9: best = (r, i, L)
    if not best or best[0] < 0.5:
        return s, e, f"NO MATCH ({phrase})", 0
    r, i, L = best
    seg = ws[i:i+L]
    a0, a1 = seg[0][0], seg[-1][1]
    gi0, gi1 = W.index(seg[0]), W.index(seg[-1])
    prev_end = W[gi0-1][1] if gi0 else 0
    next_start = W[gi1+1][0] if gi1+1 < len(W) else a1 + 1
    # FCP word ends run early: extend until 150 ms of quiet (or the next word), then breathe
    a1 = tail(a1, +1, a1 + 0.6)  # energy decides; FCP next-word times are unreliable
    a0 = tail(a0, -1, max(prev_end + 0.04, a0 - 0.5))
    return a0, a1, " ".join(w[2] for w in seg), r

fr = lambda t: int(round(t*FPS))
def rt(frames): return f"{frames}/25s" if frames % 25 else f"{frames//25}s"

report, projects, EDL = [], [], {}
for name, sel in SCRIPTS.items():
    segs = []
    for s, e, ph in sel:
        a0, a1, said, r = pick(s, e, ph)
        f0, f1 = fr(a0), fr(a1)
        if segs and segs[-1][0] < f0 < segs[-1][1]: f0 = segs[-1][1]  # no overlap with previous
        segs.append([f0, f1, said, r])
    # camera: alternate on every take change; first line (hook) on A wide, then B
    cams, cur = [], "A"
    for i, sg in enumerate(segs):
        contiguous = i and 0 <= sg[0] - segs[i-1][1] <= 2
        if i and not contiguous: cur = "B" if cur == "A" else "A"
        cams.append(cur)
    EDL[name] = [[f0, f1, c] for (f0, f1, _, _), c in zip(segs, cams)]
    report.append(f"\n## {name}")
    off, spine = 0, []
    for (f0, f1, said, r), cam in zip(segs, cams):
        d = f1 - f0
        report.append(f"- {cam}  {f0/FPS:7.2f}-{f1/FPS:7.2f}  ({d/FPS:4.1f}s, match {r:.2f})  {said}")
        conn = ""
        if cam == "B":
            bstart = B_TC + f0 - fr(B_OFF)
            conn = (f'\n            <asset-clip ref="rB" lane="1" offset="{rt(A_TC+f0)}" start="{rt(bstart)}" '
                    f'duration="{rt(d)}" audioRole="dialogue" name="B cam"><adjust-volume amount="-96dB"/></asset-clip>')
        spine.append(f'          <asset-clip ref="rA" offset="{rt(off)}" start="{rt(A_TC+f0)}" duration="{rt(d)}" '
                     f'name="{cam} | {said[:40].replace(chr(34),"")}" tcFormat="NDF">{conn}\n          </asset-clip>')
        off += d
    report.append(f"  total {off/FPS:.1f}s")
    projects.append(f'''    <project name="Brian {name} AB">
      <sequence format="r1" duration="{rt(off)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">
        <spine>
{chr(10).join(spine)}
        </spine>
      </sequence>
    </project>''')

xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.10">
  <resources>
    <format id="r1" name="FFVideoFormat2160x3840p25" frameDuration="1/25s" width="2160" height="3840"/>
    <format id="r2" name="FFVideoFormat3840x2160p25" frameDuration="1/25s" width="3840" height="2160"/>
    <asset id="rA" name="C8202 A cam" start="{rt(A_TC)}" duration="{rt(fr(A_DUR))}" hasVideo="1" hasAudio="1" format="r2" audioSources="1" audioChannels="2" audioRate="48000">
      <media-rep kind="original-media" src="{A_SRC}"/>
    </asset>
    <asset id="rB" name="C9731 B cam" start="{rt(B_TC)}" duration="{rt(fr(B_DUR))}" hasVideo="1" hasAudio="1" format="r2" audioSources="1" audioChannels="2" audioRate="48000">
      <media-rep kind="original-media" src="{B_SRC}"/>
    </asset>
  </resources>
  <library>
    <event name="Brian Ads AB cuts">
{chr(10).join(projects)}
    </event>
  </library>
</fcpxml>
'''
(OUT / "Brian_AB_cuts.fcpxml").write_text(xml)
(OUT / "picks.md").write_text("# Picks (A-cam seconds; A = wide, B = close)\n" + "\n".join(report) + "\n")
json.dump(EDL, open(OUT/"edl.json", "w"), indent=0)
print("\n".join(report))
