import numpy as np, wave
SR=48000; DUR=15; out=np.zeros(SR*DUR)
rs=np.random.default_rng(1)
def add(t,sig,g=1.0):
    i=int(t*SR); n=min(len(sig),len(out)-i); out[i:i+n]+=sig[:n]*g
def env(n,a=0.005,d=0.3):
    t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-t/d)
def whoosh(dur=0.6):
    n=int(dur*SR); x=rs.standard_normal(n); t=np.linspace(0,1,n)
    # sweeping one-pole lowpass
    y=np.zeros(n); a=0.02+0.3*np.sin(np.pi*t)**2; p=0
    for k in range(n): p+=a[k]*(x[k]-p); y[k]=p
    return y*np.sin(np.pi*t)**2*3
def boom(f=55,d=0.6):
    n=int(d*2*SR); t=np.arange(n)/SR
    return np.sin(2*np.pi*(f+80*np.exp(-t*20))*t)*env(n,0.002,d)
def pop(f):
    n=int(0.12*SR); t=np.arange(n)/SR
    return np.sin(2*np.pi*f*(1+2*np.exp(-t*60))*t)*env(n,0.001,0.03)
def tick(): n=int(0.03*SR); return rs.standard_normal(n)*env(n,0.0005,0.004)
def chime(f): n=int(1.5*SR); t=np.arange(n)/SR; return (np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*f*2.01*t))*env(n,0.003,0.5)
# scene 1 title
add(0.0,whoosh(0.5),0.5); add(0.1,boom(50,0.7),0.9); add(0.15,chime(880),0.15)
# scene 2 grid pops (match stagger seed-free approx)
add(2.6,whoosh(0.5),0.4)
for i in range(48): add(3+i*0.03+0.05,pop(500+(i%8)*90),0.18)
# scene 3 ring
add(5.6,whoosh(0.6),0.5); add(6.0,boom(70,0.5),0.6)
for i in range(12): add(6+i*0.05,tick(),0.3)
# scene 4 bars
add(8.6,whoosh(0.5),0.4)
for i in range(9): add(9+i*0.08,pop(220+i*40),0.3)
for k in range(12): add(9.6+k*0.2,tick(),0.15)
# outro slam
add(11.5,whoosh(0.6),0.6); add(12.05,boom(42,1.0),1.0); add(12.05,chime(660),0.2)
out=np.tanh(out*1.2); out/=np.abs(out).max()*1.1
s=(out*32767).astype(np.int16)
w=wave.open('sfx.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(s.tobytes()); w.close()
