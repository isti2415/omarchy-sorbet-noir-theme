#!/usr/bin/env python3
"""Regenerate the Sorbet Noir backgrounds at any resolution.

    python3 tools/generate-backgrounds.py [WIDTH] [HEIGHT] [OUTDIR]

Requires ImageMagick (`magick`) on PATH. No Python dependencies.
"""
import math, random, subprocess, os, sys

W = int(sys.argv[1]) if len(sys.argv) > 1 else 2560
H = int(sys.argv[2]) if len(sys.argv) > 2 else 1440
OUT = sys.argv[3] if len(sys.argv) > 3 else "backgrounds"
os.makedirs(OUT, exist_ok=True)

MINT=(0xa8,0xf0,0xdc); SKY=(0xa2,0xc4,0xff); LILAC=(0xdc,0xaa,0xff)
ROSE=(0xff,0x9a,0xa9); PEACH=(0xff,0xbd,0x94); BUTTER=(0xff,0xea,0xa0); AQUA=(0x9c,0xe8,0xde)

def lerp(a,b,t): return tuple(a[i]+(b[i]-a[i])*t for i in range(3))
def ramp(stops,t):
    t=min(max(t,0.0),1.0); n=len(stops)-1; i=min(int(t*n), n-1)
    return lerp(stops[i],stops[i+1], t*n-i)
def save(name, buf):
    p=os.path.join(OUT, name+".ppm")
    open(p,"wb").write(b"P6\n%d %d\n255\n"%(W,H)+bytes(buf))
    subprocess.run(["magick",p,"-depth","8",os.path.join(OUT,name+".png")],check=True)
    os.remove(p); print("wrote", name)

# 1. Pure black — truest AMOLED, every pixel off.
subprocess.run(["magick","-size",f"{W}x{H}","xc:#000000",
                os.path.join(OUT,"1-pure-black.png")],check=True)
print("wrote 1-pure-black")

# 2. Mint bloom — two whisper-soft corner glows that decay to true black.
buf=bytearray(W*H*3)
glows=[(0.10*W, 0.94*H, 0.46*W, MINT,  0.34),
       (0.93*W, 0.06*H, 0.38*W, LILAC, 0.22)]
for y in range(H):
    row=y*W*3
    for x in range(W):
        r=g=b=0.0
        for gx,gy,gr,col,peak in glows:
            d2=((x-gx)**2+(y-gy)**2)/(gr*gr)
            if d2>6: continue
            f=math.exp(-d2*2.6)*peak
            f*=f
            r+=col[0]*f; g+=col[1]*f; b+=col[2]*f
        i=row+x*3
        buf[i]=min(255,int(r)); buf[i+1]=min(255,int(g)); buf[i+2]=min(255,int(b))
save("2-mint-bloom", buf)

# 3. Aurora ribbon — the full pastel spectrum sweeping across pure black.
buf=bytearray(W*H*3)
stops=[MINT,AQUA,SKY,LILAC,ROSE,PEACH]
cy=[0.0]*W; sig=[0.0]*W; env=[0.0]*W
for x in range(W):
    u=x/W
    cy[x]=H*0.52 + H*0.104*math.sin(u*2*math.pi*0.9+0.6) + H*0.043*math.sin(u*2*math.pi*2.3+2.1)
    sig[x]=H*0.047 + H*0.028*math.sin(u*2*math.pi*1.4+0.9)
    env[x]=math.sin(min(max(u,0),1)*math.pi)**0.75
for y in range(H):
    row=y*W*3
    for x in range(W):
        dy=(y-cy[x])/sig[x]
        f=math.exp(-dy*dy)*env[x] + math.exp(-(dy*dy)*0.12)*env[x]*0.12
        if f<0.004: continue
        c=ramp(stops, x/W)
        i=row+x*3
        buf[i]=min(255,int(c[0]*f)); buf[i+1]=min(255,int(c[1]*f)); buf[i+2]=min(255,int(c[2]*f))
save("3-aurora-ribbon", buf)

# 4. Drift — sparse pastel stars on true black.
random.seed(11)
buf=bytearray(W*H*3)
pal=[MINT,AQUA,SKY,LILAC,ROSE,PEACH,BUTTER]
scale=(W*H)/(2560*1440)
parts=[]
for _ in range(int(320*scale)):
    parts.append((random.uniform(0,W), random.uniform(0,H),
                  random.uniform(1.6,4.2), random.choice(pal), random.uniform(0.55,1.0)))
for _ in range(int(34*scale)):
    parts.append((random.uniform(0,W), random.uniform(0,H),
                  random.uniform(6,13), random.choice(pal), random.uniform(0.7,1.0)))
for px,py,pr,col,amp in parts:
    R=pr*3.4
    for y in range(max(0,int(py-R)), min(H,int(py+R))):
        row=y*W*3
        for x in range(max(0,int(px-R)), min(W,int(px+R))):
            d2=((x-px)**2+(y-py)**2)/(pr*pr)
            if d2>11: continue
            f=math.exp(-d2*0.85)*amp
            i=row+x*3
            buf[i]=min(255,buf[i]+int(col[0]*f))
            buf[i+1]=min(255,buf[i+1]+int(col[1]*f))
            buf[i+2]=min(255,buf[i+2]+int(col[2]*f))
save("4-drift", buf)
