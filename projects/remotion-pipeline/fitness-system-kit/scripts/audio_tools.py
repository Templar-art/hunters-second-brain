import argparse,json,math,re,subprocess
from pathlib import Path

def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=300)
    if r.returncode:raise RuntimeError(r.stderr[-6000:])
    return r

def measure(source,target='I=-16:TP=-1.5:LRA=11'):
    r=run(['ffmpeg','-hide_banner','-nostats','-i',str(source),'-vn','-af',f'loudnorm={target}:print_format=json','-f','null','-'])
    matches=re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr,re.S)
    if not matches:raise RuntimeError('No loudness measurement')
    return json.loads(matches[-1])

def mix(voice,music,output,music_db=-22):
    if Path(output).exists():raise FileExistsError('Refusing overwrite')
    if not math.isfinite(music_db) or music_db>0:raise ValueError('Invalid gain')
    graph=f'[0:a]asplit=2[v][sc];[1:a]volume={music_db}dB[m];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=300[d];[v][d]amix=inputs=2:duration=first:normalize=0[out]'
    run(['ffmpeg','-hide_banner','-nostdin','-n','-i',str(voice),'-stream_loop','-1','-i',str(music),'-filter_complex',graph,'-map','[out]','-c:a','pcm_s24le',str(output)])

def master(source,output,integrated,peak,lra):
    if Path(output).exists():raise FileExistsError('Refusing overwrite')
    if not all(math.isfinite(x) for x in [integrated,peak,lra]) or not -70<=integrated<=-5 or not -9<=peak<=0 or not 1<=lra<=50:raise ValueError('Invalid mastering settings')
    target=f'I={integrated}:TP={peak}:LRA={lra}';m=measure(source,target)
    if any(not math.isfinite(float(m[k])) for k in ['input_i','input_tp','input_lra','input_thresh','target_offset']):raise ValueError('Nonfinite measurement; inspect silence/input')
    filt=f'loudnorm={target}:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true:print_format=json'
    run(['ffmpeg','-hide_banner','-nostdin','-n','-i',str(source),'-vn','-af',filt,'-ar','48000','-c:a','pcm_s24le',str(output)])
    return measure(output)

def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='action',required=True)
    a=s.add_parser('analyse');a.add_argument('input');a.add_argument('report')
    m=s.add_parser('mix');m.add_argument('voice');m.add_argument('music');m.add_argument('output');m.add_argument('--music-db',type=float,default=-22)
    q=s.add_parser('master');q.add_argument('input');q.add_argument('output');q.add_argument('report');q.add_argument('--integrated',type=float,required=True);q.add_argument('--true-peak',type=float,required=True);q.add_argument('--lra',type=float,required=True)
    a=p.parse_args()
    if a.action=='mix':mix(a.voice,a.music,a.output,a.music_db);return
    if Path(a.report).exists():raise FileExistsError('Refusing report overwrite')
    result=measure(a.input) if a.action=='analyse' else master(a.input,a.output,a.integrated,a.true_peak,a.lra)
    result['note']='input_* values describe the analysed file; output_* fields are filter test results, not original-file measurements.'
    with open(a.report,'x') as f:json.dump(result,f,indent=2)
if __name__=='__main__':main()
