# Sky drift composite: v1 Seedance water + still sky slowly zooming from top-right. 0 credits.
import cv2, numpy as np, subprocess
W,H=1080,1920
im=cv2.imread("hero/solis16_916.jpg"); s=W/540
poly=np.array([(178,0),(540,0),(540,286),(485,318),(470,330),(330,438),(178,438),(178,384),(212,384),(212,378)],float)*s
geo=np.zeros((H,W),np.uint8); cv2.fillPoly(geo,[poly.astype(np.int32)],255)
hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV); b,g,r=[im[...,i].astype(int) for i in range(3)]
sky=((b>r+15)&(b>=g))|((hsv[...,2]>185)&(hsv[...,1]<45))
m=(sky&(geo>0)).astype(np.uint8)*255
m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
m[770:874,358:430]=255   # sky pocket under the eave
m=cv2.erode(m,np.ones((3,3),np.uint8)); m=cv2.GaussianBlur(m,(7,7),0)
cv2.imwrite("work/sky_mask.png",m)
still=im.astype(np.float32); mf=(m.astype(np.float32)/255)[...,None]
dec=subprocess.Popen(["ffmpeg","-v","error","-i","video/pool_cinemagraph_v1.mp4","-f","rawvideo","-pix_fmt","bgr24","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","24","-i","-","-c:v","libx264","-crf","14","-preset","slow","-pix_fmt","yuv420p","-movflags","+faststart","video/pool_cinemagraph_v2_sky.mp4"],stdin=subprocess.PIPE)
N=241; i=0; ax,ay=W-1,0
while (buf:=dec.stdout.read(W*H*3)) and len(buf)==W*H*3:
    f=np.frombuffer(buf,np.uint8).reshape(H,W,3).astype(np.float32)
    k=1+0.16*i/(N-1)
    sk=cv2.warpAffine(still,np.float32([[k,0,ax-k*ax],[0,k,ay-k*ay]]),(W,H),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REFLECT)
    enc.stdin.write(np.clip(f*(1-mf)+sk*mf,0,255).astype(np.uint8).tobytes()); i+=1
enc.stdin.close(); enc.wait(); print("frames",i)
