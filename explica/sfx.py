import numpy as np, json, sys
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
key=sys.argv[1]; J=json.load(open(f'tl_{key}.json'))
SR=48000; N=int(SR*J['total']); L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(5)
bp=lambda x,lo,hi: sosfilt(butter(2,[lo,hi],'band',fs=SR,output='sos'),x)
lp=lambda x,f: sosfilt(butter(2,f,'low',fs=SR,output='sos'),x)
hp=lambda x,f: sosfilt(butter(2,f,'high',fs=SR,output='sos'),x)
def put(x,at,g=1.0,pan=0.0):
    n0=int(at*SR)
    if n0<0: x=x[-n0:]; n0=0
    n1=min(N,n0+len(x))
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
def tick():
    n=int(0.05*SR); t=np.arange(n)/SR; return hp(rng.standard_normal(n),3000)*np.exp(-t*120)*0.5
def ding():
    n=int(0.9*SR); t=np.arange(n)/SR; return (np.sin(2*np.pi*1568*t)*.35+np.sin(2*np.pi*2349*t)*.2)*np.exp(-t*5)
def shimmer(d=2.2):
    n=int(d*SR); t=np.arange(n)/SR; x=sum(np.sin(2*np.pi*f*t+rng.random()*6)*np.exp(-t*2.2) for f in [1568,2093,2637,3136,3951]); return x*0.06*np.minimum(1,t*20)
def charge(d=1.4):
    n=int(d*SR); t=np.arange(n)/SR; f=220*2**(t/d*2.2); x=np.sin(2*np.pi*np.cumsum(f)/SR)*0.18+np.sin(2*np.pi*np.cumsum(f*1.5)/SR)*0.08
    return x*np.minimum(1,t*6)*np.minimum(1,(d-t)*10)
def lowbeep():
    n=int(0.16*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*330*t)*np.exp(-t*14)*0.35
def scanner(d=1.0):
    n=int(d*SR); t=np.arange(n)/SR; return bp(rng.standard_normal(n),1800,4200)*0.08*np.sin(np.pi*t/d)
def shutter():
    n=int(0.18*SR); t=np.arange(n)/SR; x=hp(rng.standard_normal(n),2500)*(np.exp(-t*90)+0.6*np.exp(-np.maximum(0,t-0.07)*90)*(t>0.07)); return x*0.5
put(boom(1.2,50),0.05,0.55)
for b in J['beats']:
    if b['type']=='big':
        put(whoosh(0.4),b['a']-0.3,0.4,0.3)
        if 'at' in b:
            for x in b['at'][1:]: put(tick(),x,0.35)
    if b['type']=='flash':
        put(boom(1.4,46),b['a'],0.7); put(shimmer(),b['a']+0.05,1.0)
    if b['type']=='batt':
        put(charge(b['charge'][1]-b['charge'][0]),b['charge'][0],0.9)
        k=b['k']; lowt=[x[0] for x in k if x[1]<=12]
        if lowt:
            t0=lowt[0];
            for i in range(4): put(lowbeep(),t0+0.45*i,0.6)
    if b['type']=='ui':
        put(whoosh(0.6),b['a']-0.35,0.6); put(boom(1.0,60),b['a'],0.35)
        for i,s in enumerate(b['steps']):
            if i>0: put(whoosh(0.4),s['t']-0.3,0.45,(-1)**i*0.4)
            if s['scr']=='import': put(scanner(1.0),s['t']+0.2,1.0); [put(ding(),s['t']+1.25+j*0.3,0.35) for j in range(3)]
            if s['scr']=='invoice': put(shutter(),s['t']+0.05,0.8); [put(ding(),s['t']+1.6+j*0.3,0.35) for j in range(3)]
            if s['scr']=='margin': [put(pop(900+j*120),s['t']+0.35+j*0.3,0.45) for j in range(4)]
            if s['scr']=='brief': [put(pop(1000+j*150),s['t']+0.35+j*0.32,0.5) for j in range(3)]
            if s['scr']=='chat': [put(pop(1200),s['t']+0.35+j*0.32,0.45) for j in range(2)]
put(whoosh(0.6),J['end']-0.45,0.6); put(boom(1.6,45),J['end']+0.1,0.8); put(shimmer(),J['end']+0.6,1.0)
m=np.stack([L,R],1); m/=max(1e-6,np.max(np.abs(m)))*1.1
wavfile.write(f'sfx_{key}.wav',SR,(m*32767).astype(np.int16)); print('sfx',key)
