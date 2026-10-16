import json, subprocess, re, concurrent.futures as cf, os
jobs=json.load(open("hero/jobs.json"))
def run(k,model):
    j=jobs[k]; imgs=[j["guide"],j["id"]]+j["cast"]
    cmd=["higgsfield","generate","create"]+(["seedream_v5_pro","--resolution","2k"] if model=="seedream" else ["gpt_image_2_5","--variant","sunburst","--quality","high","--resolution","2k"])
    cmd+=["--aspect_ratio","16:9","--prompt",j["prompt"],"--wait"]
    for im in imgs: cmd+=["--image",im]
    for attempt in range(2):
        r=subprocess.run(cmd,capture_output=True,text=True)
        urls=re.findall(r"https://\S+",r.stdout+r.stderr)
        if urls:
            out=f"hero/{k}_{model}.png"; subprocess.run(["curl","-s","-o",out,urls[-1]]); return (k,model,"ok")
        if "no response" not in (r.stdout+r.stderr): return (k,model,(r.stdout+r.stderr)[-200:])
    return (k,model,"failed twice")
with cf.ThreadPoolExecutor(6) as ex:
    for res in ex.map(lambda a: run(*a), [(k,m) for k in jobs for m in ("seedream","sunburst")]): print(res, flush=True)
