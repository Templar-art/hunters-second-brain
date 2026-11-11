# exec inside Resolve MCP. V1 interview (C8197) with punch-ins, V2 B-roll, A1 interview audio.
# W = wide two-shot, MH = punch on her (zoom 1.8, pan -560, tilt 250), MM = punch on him (pan 700, tilt 400).
# All clips: Sony/10x_Bespoke_look.cube (LC-709 TypeA + gentle contrast/warmth/sat + sky roll-off).
# Landscape B-roll (C39xx) zoomed 3.16 to fill 9:16. Audio: Voice Isolation 55, Dialogue Leveler, 4f crossfades.
import json
ROOT = "/Users/10xhunter/Documents/Hunters Second Brain/projects/bespoke-emerald-lakes-interview/"
LUT = "Sony/10x_Bespoke_look.cube"
ANG = {"W": (1.0, 0, 0), "MH": (1.8, -560, 250), "MM": (1.8, 700, 400)}

def build(name="Emerald Lakes interview"):
    p = resolve.GetProjectManager().GetCurrentProject(); mp = p.GetMediaPool()
    cl = {c.GetName(): c for c in mp.GetRootFolder().GetClipList()}
    for i in range(p.GetTimelineCount(), 0, -1):
        t = p.GetTimelineByIndex(i)
        if t.GetName() in ("test", name): mp.DeleteTimelines([t])
    J = json.load(open(ROOT + "edl.json")); E = J["segs"]; O = J["opener"]; OFF = O["src_out"] - O["src_in"]
    tl = mp.CreateEmptyTimeline(name); p.SetCurrentTimeline(tl)
    st = tl.GetStartFrame(); I = cl["C8197.MP4"]; OC = cl[O["clip"]]
    v1 = [] if OFF == 0 else [{"mediaPoolItem": OC, "startFrame": O["src_in"], "endFrame": O["src_out"], "mediaType": 1, "trackIndex": 1, "recordFrame": st}]
    a1 = [] if OFF == 0 else [{"mediaPoolItem": OC, "startFrame": O["src_in"], "endFrame": O["src_out"], "mediaType": 2, "trackIndex": 1, "recordFrame": st}]; v2 = []
    for s in E:
        d = s["src_out"] - s["src_in"]
        v1.append({"mediaPoolItem": I, "startFrame": s["src_in"], "endFrame": s["src_out"], "mediaType": 1, "trackIndex": 1, "recordFrame": st + OFF + s["rec"]})
        a1.append({"mediaPoolItem": I, "startFrame": s["src_in"], "endFrame": s["src_out"], "mediaType": 2, "trackIndex": 1, "recordFrame": st + OFF + s["rec"]})
        for b in s["broll"]:
            v2.append({"mediaPoolItem": cl[b["clip"]], "startFrame": b["src_in"], "endFrame": b["src_in"] + b["rec_out"] - b["rec_in"], "mediaType": 1, "trackIndex": 2, "recordFrame": st + b["rec_in"]})
    tl.AddTrack("video"); mp.AppendToTimeline(v1 + a1 + v2)
    V1 = tl.GetItemListInTrack("video", 1); V2 = tl.GetItemListInTrack("video", 2); A1 = tl.GetItemListInTrack("audio", 1)
    V1i = V1 if OFF == 0 else V1[1:]
    for it, s in zip(V1i, E):
        z, px, ty = ANG[s["angle"]]
        if z != 1.0:
            it.SetProperty("ZoomX", z); it.SetProperty("ZoomY", z); it.SetProperty("Pan", px); it.SetProperty("Tilt", ty)
    for it in V2:
        if it.GetMediaPoolItem().GetClipProperty("Resolution") == "3840x2160":
            it.SetProperty("ZoomX", 3.16); it.SetProperty("ZoomY", 3.16)
    for it in A1:
        it.SetProperty("AudioVoiceIsolationEnabled", True); it.SetProperty("AudioVoiceIsolationAmount", 55)
        it.SetProperty("AudioDialogueLevelerEnabled", True)
    tr = sum(bool(it.AddTransition({"type": "Cross Fade 0 dB", "category": "audio", "position": "start", "alignment": "center", "duration": 4})) for it in A1[1:])
    sm = []
    for k in range(1, len(E)):  # Smooth Cut only where the angle doesn't change (hides um-trim jumps)
        if False:  # Smooth Cuts rejected by Hunter; B-roll covers joins: every interview join gets a Smooth Cut
            sm.append(bool(V1i[k].AddTransition({"type": "Smooth Cut", "category": "simple", "position": "start", "alignment": "center", "duration": 4})))
    gaps = sum(1 for x, y in zip(V1, V1[1:]) if y.GetStart() != x.GetEnd())
    return {"v1": len(V1), "v2": len(V2), "a1": len(A1), "xfades": tr, "smooth": sm, "gaps": gaps, "frames": tl.GetEndFrame() - st}
