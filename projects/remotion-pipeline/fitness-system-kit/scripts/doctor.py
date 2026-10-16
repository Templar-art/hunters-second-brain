import argparse, importlib.util, json, platform, shutil, subprocess, sys
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--project',default='.');p.add_argument('--output',required=True);a=p.parse_args();project=Path(a.project)
    tools={}
    for tool,args in [('node',['--version']),('npm',['--version']),('ffmpeg',['-version']),('ffprobe',['-version']),('nvidia-smi',['--query-gpu=name,memory.total','--format=csv,noheader'])]:
        binary=shutil.which(tool)
        if not binary:tools[tool]={'status':'MISSING'};continue
        try:
            r=subprocess.run([binary,*args],capture_output=True,text=True,timeout=15)
            tools[tool]={'status':'FOUND' if r.returncode==0 else 'ERROR','summary':(r.stdout or r.stderr).splitlines()[:3]}
        except Exception as e:tools[tool]={'status':'ERROR','summary':str(e)}
    packages={m:importlib.util.find_spec(m) is not None for m in ['faster_whisper','mediapipe','cv2','librosa','scenedetect']}
    node={}
    if (project/'package.json').is_file():
        data=json.loads((project/'package.json').read_text());deps={**data.get('dependencies',{}),**data.get('devDependencies',{})};node={k:v for k,v in deps.items() if k=='react' or k=='remotion' or k.startswith('@remotion/')}
    result={'python':sys.version.split()[0],'os':platform.system(),'architecture':platform.machine(),'tools':tools,'pythonModulesPresentNotImported':packages,'projectRemotionDependencies':node,'lockfiles':[x for x in ['package-lock.json','pnpm-lock.yaml','yarn.lock','bun.lock','bun.lockb'] if (project/x).exists()],'inferenceTested':False,'installsPerformed':False}
    target=Path(a.output)
    with target.open('x') as f:json.dump(result,f,indent=2)
if __name__=='__main__':main()
