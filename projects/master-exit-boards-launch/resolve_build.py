# MASTR Exit Boards launch ad (LinkedIn), one continuous take C8203 (27 min, coach feeding lines).
# Her takes picked by lav loudness (talent 45-55 dB vs coach 25-35 dB), every pick re-transcribed alone.
# Single camera: W = wide, P = punch-in. Angle changes on each script beat; Smooth Cut on joins inside a beat.
# Run inside Resolve MCP: exec(open(this).read()); build()
SRC = "/Volumes/Kristian T7/Master Launch 11:11/C8203.MP4"
SEG = [  # (in s, out s, angle, line)
 (220.15, 225.95, "W", "Most business owners spend years building something, but very few actually build it to sell."),
 (302.25, 305.45, "P", "When the time comes, they find out the business still depends on them."),
 (318.45, 320.75, "P", "The value isn't where they thought it was"),
 (323.85, 326.85, "P", "and the exit they planned isn't really an option."),
 (345.04, 347.89, "W", "Philip De Bella and I are launching the MASTR Exit Boards."),
 (364.26, 367.85, "W", "It's a small group of business owners working together on one goal:"),
 (372.86, 376.70, "W", "building a business ready to exit on your terms."),
 (408.44, 410.00, "P", "Every board meets regularly."),
 (411.79, 412.85, "P", "We work through the numbers,"),
 (413.64, 414.45, "P", "the systems"),
 (415.17, 415.90, "P", "and the team,"),
 (417.55, 419.34, "P", "so that the business can run without you"),
 (421.77, 424.04, "P", "and is worth more when you're ready to move on."),
 (542.40, 548.20, "W", "It's for owners who have built something real and want to make sure that all that hard work pays off."),
 (1548.10, 1561.80, "P", "The exit boards kick off early next year, but we want to meet you now. That's why Philip De Bella and myself are hosting the first Exit Board Breakfast on the 15th of December, and we'd love to see you there, so we can learn more about you, your business and your journey."),
]
ANG = {"W": (1.0, 0, 0), "P": (1.35, 0, -260), "C": (1.75, 0, -520)}
ROT = ["W", "P", "C"]  # every join changes angle (Hunter: Smooth Cuts jumped); 3-way so it never ping-pongs A-B
FPS = 25

def build(name="Master Exit Boards launch"):
    pm = resolve.GetProjectManager()
    if pm.GetCurrentProject().GetName() != "Master Exit Boards":
        if not pm.LoadProject("Master Exit Boards"):
            p = pm.CreateProject("Master Exit Boards")
            p.SetSetting("timelineResolutionWidth", "2160"); p.SetSetting("timelineResolutionHeight", "3840"); p.SetSetting("timelineFrameRate", "25")
    p = pm.GetCurrentProject(); mp = p.GetMediaPool()
    cl = {c.GetName(): c for c in mp.GetRootFolder().GetClipList()}
    if "C8203.MP4" not in cl: mp.ImportMedia([SRC]); cl = {c.GetName(): c for c in mp.GetRootFolder().GetClipList()}
    for i in range(p.GetTimelineCount(), 0, -1):
        t = p.GetTimelineByIndex(i)
        if t.GetName() == name: mp.DeleteTimelines([t])
    tl = mp.CreateEmptyTimeline(name); p.SetCurrentTimeline(tl); st = tl.GetStartFrame(); I = cl["C8203.MP4"]
    rec = 0; info = []
    for a, b, ang, _ in SEG:
        f0, f1 = round(a * FPS), round(b * FPS)
        for m in (1, 2): info.append({"mediaPoolItem": I, "startFrame": f0, "endFrame": f1, "mediaType": m, "trackIndex": 1, "recordFrame": st + rec})
        rec += f1 - f0
    mp.AppendToTimeline(info)
    V = tl.GetItemListInTrack("video", 1); A = tl.GetItemListInTrack("audio", 1)
    for k, it in enumerate(V):
        z, px, ty = ANG[ROT[k % 3]]
        it.GetNodeGraph().SetLUT(1, "Sony/10x_Bespoke_look.cube")  # S-Log3 -> 10x look (chosen vs LC-709 / Phntm Arri)
        if z != 1.0: it.SetProperty("ZoomX", z); it.SetProperty("ZoomY", z); it.SetProperty("Pan", px); it.SetProperty("Tilt", ty)
    for it in A:
        it.SetProperty("AudioVoiceIsolationEnabled", True); it.SetProperty("AudioVoiceIsolationAmount", 55); it.SetProperty("AudioDialogueLevelerEnabled", True)
    xf = sum(bool(it.AddTransition({"type": "Cross Fade 0 dB", "category": "audio", "position": "start", "alignment": "center", "duration": 4})) for it in A[1:])
    sm = []  # Smooth Cuts removed 2026-11-11: they visibly jumped
    return {"v": len(V), "a": len(A), "xf": xf, "smooth": sm, "sec": rec / FPS}
