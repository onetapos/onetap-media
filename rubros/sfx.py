import numpy as np, json, sys
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
lang=sys.argv[1]; T=json.load(open(f'tl_{lang}.json'))['tl']
SR=48000; N=int(SR*T['total']); L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(3)
def bp(x,lo,hi): return sosfilt(butter(2,[lo,hi],'band',fs=SR,output='sos'),x)
def lp(x,f): return sosfilt(butter(2,f,'low',fs=SR,output='sos'),x)
def hp(x,f): return sosfilt(butter(2,f,'high',fs=SR,output='sos'),x)
def put(x,at,g=1.0,pan=0.0):
    n0=int(at*SR)
    if n0<0: x=x[-n0:]; n0=0
    n1=min(N,n0+len(x))
    if n1<=n0: return
    L[n0:n1]+=x[:n1-n0]*g*(1-pan*0.6); R[n0:n1]+=x[:n1-n0]*g*(1+pan*0.6)
def whoosh(d=0.45,up=True):
    n=int(d*SR); t=np.arange(n)/SR; x=rng.standard_normal(n)
    out=np.zeros(n); steps=24
    for k in range(steps):
        a=k*n//steps; b=(k+1)*n//steps; fr=k/steps
        fc=(400+5000*fr) if up else (5000-4400*fr)
        out[a:b]=bp(x,max(80,fc*0.6),min(20000,fc*1.4))[a:b]
    e=np.sin(np.pi*np.linspace(0,1,n))**1.5
    return out*e*0.5
def boom(d=1.2,f0=55):
    n=int(d*SR); t=np.arange(n)/SR; f=f0+60*np.exp(-t*18)
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*3.2)*0.9 + lp(rng.standard_normal(n),900)*np.exp(-t*14)*0.25)
def pop(f=900):
    n=int(0.12*SR); t=np.arange(n)/SR; fr=f*(1+0.6*np.exp(-t*60))
    return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*38)*0.45
def click():
    n=int(0.03*SR); return hp(rng.standard_normal(n),2500)*np.exp(-np.arange(n)/SR*220)*0.35
def kaching():
    n=int(1.3*SR); t=np.arange(n)/SR; x=np.zeros(n)
    for f,a,dc in [(2093,0.35,4),(2637,0.3,4.5),(3136,0.22,5),(4186,0.12,6)]:
        x+=np.sin(2*np.pi*f*t)*a*np.exp(-t*dc)
    x[:int(0.06*SR)]+=hp(rng.standard_normal(int(0.06*SR)),3000)*0.5*np.exp(-np.arange(int(0.06*SR))/SR*60)
    d=int(0.09*SR); x[d:]+=x[:-d]*0.55  # second strike
    return x*0.55
def shimmer(d=1.8):
    n=int(d*SR); t=np.arange(n)/SR; x=np.zeros(n)
    for f in [1568,2093,2637,3136,3951]:
        x+=np.sin(2*np.pi*f*t+rng.random()*6)*np.exp(-t*2.2)*(0.5+0.5*np.sin(2*np.pi*(5+rng.random()*3)*t))
    return x*0.06*np.minimum(1,t*20)
def fire(d=1.0):
    n=int(d*SR); x=bp(rng.standard_normal(n),300,4000)*np.exp(-np.linspace(0,3,n))
    return x*0.5*np.minimum(1,np.arange(n)/SR*40)
# kitchen opening
put(boom(1.3,48),0.0,0.9); put(fire(1.1),0.05,0.7)
cuts=json.load(open('kcuts.json'))[lang]
for c in cuts[1:]: put(whoosh(0.32),c-0.2,0.55,0.3)
# into hero
put(whoosh(0.6),T['kitEnd']-0.45,0.8); put(boom(0.9,60),T['kitEnd'],0.55)
# tags + cost card
for i in range(4): put(pop(820+i*90),T['p2']+0.15+i*0.4,0.7,(-1)**i*0.4)
put(kaching(),T['p2']+1.9,0.6)
# into night: downward whoosh
put(whoosh(0.7,False),T['heroEnd']-0.4,0.6)
# into UI
put(whoosh(0.5),T['nightEnd']-0.35,0.7); put(boom(0.8,70),T['nightEnd'],0.45)
q=(T['uiEnd']-T['nightEnd'])/4
for k in range(4):
    a=T['nightEnd']+k*q
    put(click(),a+0.25,0.8); 
    if k>0: put(whoosh(0.28),a-0.12,0.35,0.5)
for i in range(5): put(click(),T['nightEnd']+q+0.15+i*0.18,0.35)
for i in range(3): put(pop(1200),T['nightEnd']+2*q+0.4+i*0.35,0.45)
for i in range(3): put(pop(700),T['nightEnd']+3*q+0.2+i*0.3,0.4)
# morning
put(whoosh(0.5),T['uiEnd']-0.3,0.5); put(pop(1000),T['uiEnd']+0.5,0.55)
for i in range(3): put(pop(1300+i*120),T['uiEnd']+1.0+i*0.45,0.4)
# end sting
put(whoosh(0.6),T['mornEnd']-0.45,0.6); put(boom(1.6,45),T['mornEnd']+0.1,0.8); put(shimmer(2.2),T['mornEnd']+0.6,1.0)
m=np.stack([L,R],1); m/=max(1e-6,np.max(np.abs(m)))*1.1
wavfile.write(f'sfx_{lang}.wav',SR,(m*32767).astype(np.int16)); print('sfx ok')
