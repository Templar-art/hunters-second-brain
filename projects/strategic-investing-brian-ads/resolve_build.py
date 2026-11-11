# Run inside Resolve (MCP run_script_unsafe): exec(open(this).read()); build(names)
# W = A wide, M = A punch-in (zoom 1.5, tilt -150), C = B close. A clips get the A->B match LUT.
# Audio: A-cam lav on every segment, Voice Isolation 40, Dialogue Leveler, 4-frame centre crossfades.
import json
ROOT = "/Users/10xhunter/Documents/Hunters Second Brain/projects/strategic-investing-brian-ads/"
EDL = json.load(open(ROOT + "edl.json")); ANG = json.load(open(ROOT + "angles.json"))
BOFF = round(63.52 * 25)

def build(names):
    p = resolve.GetProjectManager().GetCurrentProject(); mp = p.GetMediaPool()
    cl = {c.GetName(): c for c in mp.GetRootFolder().GetClipList()}
    A, B = cl["C8202.MP4"], cl["C9731.MP4"]
    log = []
    for name in names:
        segs, ang = EDL[name], ANG[name]
        tl = mp.CreateEmptyTimeline("Brian " + name); p.SetCurrentTimeline(tl)
        st = tl.GetStartFrame(); rec = 0; infos = []
        for (f0, f1, _), a in zip(segs, ang):
            d = f1 - f0; src = B if a == "C" else A; s = f0 - BOFF if a == "C" else f0
            infos.append({"mediaPoolItem": src, "startFrame": s, "endFrame": s + d, "mediaType": 1, "trackIndex": 1, "recordFrame": st + rec})
            infos.append({"mediaPoolItem": A, "startFrame": f0, "endFrame": f0 + d, "mediaType": 2, "trackIndex": 1, "recordFrame": st + rec})
            rec += d
        mp.AppendToTimeline(infos)
        v = tl.GetItemListInTrack("video", 1); au = tl.GetItemListInTrack("audio", 1)
        for it, a in zip(v, ang):
            if a != "C":
                it.GetNodeGraph().SetLUT(1, "Sony/10x_A_to_Bcam_match.cube")
            if a == "M":
                it.SetProperty("ZoomX", 1.5); it.SetProperty("ZoomY", 1.5); it.SetProperty("Tilt", -150)
        for it in au:
            it.SetProperty("AudioVoiceIsolationEnabled", True); it.SetProperty("AudioVoiceIsolationAmount", 40)
            it.SetProperty("AudioDialogueLevelerEnabled", True)
        tr = sum(bool(it.AddTransition({"type": "Cross Fade 0 dB", "category": "audio", "position": "start", "alignment": "center", "duration": 4})) for it in au[1:])
        gaps = sum(1 for x, y in zip(v, v[1:]) if y.GetStart() != x.GetEnd())
        log.append((name, len(v), gaps, tr, tl.GetEndFrame() - st == rec))
    return log
