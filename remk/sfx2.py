import numpy as np, json, sys
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
key=sys.argv[1]; J=json.load(open(f'tl_{key}.json'))
SR=48000; N=int(SR*J['total']); L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(5)
bp=lambda x,lo,hi: sosfilt(butter(2,[lo,hi],'band',fs=SR,output='sos'),x)
lp=lambda x,f: sosfilt(butter(2,f,'low',fs=SR,output='sos'),x)
hp=lambda x,f: sosfilt(butter(2,f,'high',fs=SR,output='sos'),x)
def put(x,at,g=1.0,pan=0.0):
    n0=int(at*SR); 
    if n0<0: x=x[-n0:]; n0=0
    n1=min(N,n0+len(x)); 
    if n1>n0: L[n0:n1]+=x[:n1-n0]*g*(1-pan*.6); R[n0:n1]+=x[:n1-n0]*g*(1+pan*.6)
def whoosh(d=0.45):
    n=int(d*SR); x=rng.standard_normal(n); out=np.zeros(n)
    for k in range(20):
        a=k*n//20; b=(k+1)*n//20; fc=400+5000*k/20; out[a:b]=bp(x,fc*.6,min(20000,fc*1.4))[a:b]
    return out*np.sin(np.pi*np.linspace(0,1,n))**1.5*0.5
def boom(d=1.3,f0=48):
    n=int(d*SR); t=np.arange(n)/SR; f=f0+60*np.exp(-t*18); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*3.2)*0.9+lp(rng.standard_normal(n),900)*np.exp(-t*14)*0.25
def pop(f=900):
    n=int(0.12*SR); t=np.arange(n)/SR; fr=f*(1+0.6*np.exp(-t*60)); return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*38)*0.45
def ding():
    n=int(0.9*SR); t=np.arange(n)/SR; return (np.sin(2*np.pi*1568*t)*.35+np.sin(2*np.pi*2349*t)*.2)*np.exp(-t*5)
def shimmer(d=2.2):
    n=int(d*SR); t=np.arange(n)/SR; x=sum(np.sin(2*np.pi*f*t+rng.random()*6)*np.exp(-t*2.2) for f in [1568,2093,2637,3136,3951]); return x*0.06*np.minimum(1,t*20)
put(boom(1.2,50),0.05,0.6)
for b in J['beats']:
    put(whoosh(0.4),b['a']-0.3,0.45,0.3)
    if b['type']=='chips':
        n=len(b['items']); span=max(0.6,(b['until']-b['a'])-0.2)
        for j in range(n): put(pop(700+(j%6)*90),b['a']+j*span/n,0.5,((-1)**j)*0.4)
    if b['type']=='flow':
        for j in range(len(b['items'])): put(pop(1000+j*120),b['a']+0.25+j*0.32,0.55)
    if b['type']=='checks':
        for j in range(len(b['items'])): put(ding(),b['a']+0.4+j*0.5,0.5)
for (fn,ss,d) in J['bg'][1:]: pass
put(whoosh(0.6),J['end']-0.45,0.6); put(boom(1.6,45),J['end']+0.1,0.8); put(shimmer(),J['end']+0.6,1.0)
m=np.stack([L,R],1); m/=max(1e-6,np.max(np.abs(m)))*1.1
wavfile.write(f'sfx_{key}.wav',SR,(m*32767).astype(np.int16)); print('sfx',key)
