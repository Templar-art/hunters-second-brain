import subprocess,re,concurrent.futures as cf
BASE=" One continuous shot, no cuts, no zoom. The architecture, furniture, people and car stay solid and consistent throughout; nothing morphs, appears or disappears. Bright clear Gold Coast morning sun, true-to-life colour, real cinematic footage, editorial luxury property film."
S={
"01_surf":"Cinematic drone footage. The drone glides very slowly forward low over the rolling surf toward the beachfront homes, rising gently as waves roll in and break into white foam beneath it, the couple walking along the wet sand in the distance, palms and dune grass moving softly in the sea breeze.",
"02_pool":"Smooth gimbal footage. The camera glides slowly sideways along the infinity pool toward the house, the pool water gently rippling and sparkling, the woman at the pool edge turning her head toward the ocean, the couple on the balcony relaxed in conversation, the umbrella fabric stirring in the breeze.",
"03_living":"Slow interior gimbal footage. The camera drifts gently forward through the open-plan living room toward the floor-to-ceiling glass and the ocean view, the woman behind the kitchen island lifting a glass and looking out to the sea, palms swaying outside, soft daylight across the timber floor.",
"04_top":"Top-down drone footage looking straight down. The drone rises slowly and smoothly straight up from above the roof, revealing more of the pool, deck, garden, beach and the surf line as it climbs, the pool water glinting, palm fronds moving, waves rolling onto the sand.",
"05_walk":"Slow walking gimbal footage. The camera steps gently forward through the open sliding glass door from the deck into the ground-floor lounge, passing the sofa and armchairs toward the floating timber staircase, subtle natural handheld walk motion, sheer daylight filling the room.",
"06_track":"Gimbal tracking footage at chest height. The camera tracks smoothly alongside the couple as they walk barefoot along the wet sand, matching their pace, the woman laughing softly and brushing her hair back, the man smiling, their clothes and hair moving in the sea breeze, small waves washing over the sand beside them.",
"07_car":"Low cinematic tracking footage. The pearl-white supercar rolls slowly forward along the street in front of the house, wheels turning, reflections sliding across its glossy paintwork, the camera tracking alongside at the same pace, palms swaying gently behind.",
}
def run(k):
    cmd=["higgsfield","generate","create","seedance_2_5","--mode","omni_reference","--start-image",f"hero/{k}_sunburst.png","--duration","8","--resolution","1080p","--aspect_ratio","16:9","--generate_audio","false","--prompt",S[k]+BASE,"--wait"]
    for a in range(3):
        r=subprocess.run(cmd,capture_output=True,text=True); t=r.stdout+r.stderr; u=re.findall(r"https://\S+\.mp4\S*|https://\S+",t)
        if u: subprocess.run(["curl","-s","-o",f"video/{k}.mp4",u[-1]]); return (k,"ok")
        if not any(s in t for s in ("no response","520","PUT media","timeout")): return (k,t[-200:])
    return (k,"failed")
with cf.ThreadPoolExecutor(4) as ex:
    for r in ex.map(run,list(S)): print(r,flush=True)
