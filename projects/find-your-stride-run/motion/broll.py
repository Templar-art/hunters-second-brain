"""Overwrite talk frames (where Alex reads off the phone) with graded B-roll. Cut-time windows → source ranges."""
import subprocess, os, shutil, math, glob
FPS=24000/1001; SRC="/Users/10xhunter/Downloads/Run video.mp4"
GRADE="eq=contrast=1.07:saturation=1.18:gamma=0.98,colorbalance=rs=0.03:bs=-0.03:rm=0.02:bm=-0.02,unsharp=5:5:0.4"
PLAN=[(18.96,21.50,16.40,18.88,""),        # selfie runners (unused)
      (21.50,24.10, 3.60, 5.95,",hflip"),  # night bridge, mirrored
      (30.45,32.45, 8.40, 9.55,""),        # ocean pano, slowed
      (32.45,34.94,14.00,16.25,",hflip"),  # trees, mirrored
      (41.16,44.55,12.00,13.78,"")]        # path runner, slow-mo (under the coin)
fr="ep/build/frames"; tmp="ep/build/broll_tmp"; shutil.rmtree(tmp,ignore_errors=True); os.makedirs(tmp)
for k,(a,b,s,e,x) in enumerate(PLAN):
    i0=math.floor(a*FPS)+1; i1=math.ceil(b*FPS)+1; n=i1-i0+1; speed=(e-s)/(n/FPS); d=f"{tmp}/{k}"; os.makedirs(d)
    subprocess.run(["ffmpeg","-v","error","-ss",str(s),"-to",str(e),"-i",SRC,"-map","0:v:0","-vf",
      f"setpts=PTS/{speed:.4f},fps=24000/1001,scale=1080:1920,{GRADE}{x}","-frames:v",str(n),"-q:v","2",f"{d}/b%04d.jpg"],check=True)
    got=sorted(glob.glob(f"{d}/b*.jpg"))
    for j in range(n): shutil.copy(got[min(j,len(got)-1)], f"{fr}/f{i0+j:04d}.jpg")
    print(k,a,b,n,len(got),f"speed {speed:.2f}")
