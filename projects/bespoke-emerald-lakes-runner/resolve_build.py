# exec in Resolve MCP. Runner piece: V1 opener C8194 + C8200 agent lines (Smooth Cut on joins not covered by B-roll),
# V2 B-roll (landscape C39xx zoomed 3.16 to fill 9:16), A1 lav audio with Voice Isolation/Dialogue Leveler + 4f crossfades. Ungraded.
import json
ROOT = "/Users/10xhunter/Documents/Hunters Second Brain/projects/bespoke-emerald-lakes-runner/"
def build(name="Emerald Lakes runner"):
    p = resolve.GetProjectManager().GetCurrentProject(); mp = p.GetMediaPool()
    have = {c.GetName() for c in mp.GetRootFolder().GetClipList()}
    if "C8200.MP4" not in have: mp.ImportMedia(["/Volumes/Kristian T7/Bespoke filming /C8200.MP4"])
    cl = {c.GetName(): c for c in mp.GetRootFolder().GetClipList()}
    for i in range(p.GetTimelineCount(), 0, -1):
        t = p.GetTimelineByIndex(i)
        if t.GetName() == name: mp.DeleteTimelines([t])
    J = json.load(open(ROOT + "edl.json")); E = J["segs"]; O = J["opener"]
    tl = mp.CreateEmptyTimeline(name); p.SetCurrentTimeline(tl); tl.AddTrack("video")
    st = tl.GetStartFrame(); I = cl["C8200.MP4"]; OC = cl[O["clip"]]
    v1 = [{"mediaPoolItem": OC, "startFrame": O["src_in"], "endFrame": O["src_out"], "mediaType": 1, "trackIndex": 1, "recordFrame": st}]
    a1 = [{"mediaPoolItem": OC, "startFrame": O["src_in"], "endFrame": O["src_out"], "mediaType": 2, "trackIndex": 1, "recordFrame": st}]
    v2 = []
    for s in E:
        v1.append({"mediaPoolItem": I, "startFrame": s["src_in"], "endFrame": s["src_out"], "mediaType": 1, "trackIndex": 1, "recordFrame": st + s["rec"]})
        a1.append({"mediaPoolItem": I, "startFrame": s["src_in"], "endFrame": s["src_out"], "mediaType": 2, "trackIndex": 1, "recordFrame": st + s["rec"]})
        for b in s["broll"]:
            v2.append({"mediaPoolItem": cl[b["clip"]], "startFrame": b["src_in"], "endFrame": b["src_in"] + b["rec_out"] - b["rec_in"], "mediaType": 1, "trackIndex": 2, "recordFrame": st + b["rec_in"]})
    mp.AppendToTimeline(v1 + a1 + v2)
    V1 = tl.GetItemListInTrack("video", 1); V2 = tl.GetItemListInTrack("video", 2); A1 = tl.GetItemListInTrack("audio", 1)
    ANG = {"W": (1.0, 0, 0), "P": (1.4, 0, 0), "C": (1.9, 0, 0)}
    for k, it in enumerate(V1):
        it.GetNodeGraph().SetLUT(1, "Sony/10x_Master_look.cube")
        if k:
            z, px, ty = ANG[E[k-1]["angle"]]
            if z != 1.0: it.SetProperty("ZoomX", z); it.SetProperty("ZoomY", z)
    for it in V2:
        if it.GetMediaPoolItem().GetClipProperty("Resolution") == "3840x2160":
            it.SetProperty("ZoomX", 3.16); it.SetProperty("ZoomY", 3.16)
    for it in A1:
        it.SetProperty("AudioVoiceIsolationEnabled", True); it.SetProperty("AudioVoiceIsolationAmount", 55)
        it.SetProperty("AudioDialogueLevelerEnabled", True)
    xf = sum(bool(it.AddTransition({"type": "Cross Fade 0 dB", "category": "audio", "position": "start", "alignment": "center", "duration": 4})) for it in A1[1:])
    covered = [(b.GetStart(), b.GetEnd()) for b in V2]
    sm = []
    for it in V1[2:]:  # interview joins (not opener->C8200, which is a real shot change)
        t = it.GetStart()
        if False:  # Smooth Cuts rejected by Hunter (jarring) - joins are covered by B-roll
            sm.append(bool(it.AddTransition({"type": "Smooth Cut", "category": "simple", "position": "start", "alignment": "center", "duration": 4})))
    return {"v1": len(V1), "v2": len(V2), "xfades": xf, "smooth": sm, "frames": tl.GetEndFrame() - st}
