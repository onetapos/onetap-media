import numpy as np, json, sys
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
lang=sys.argv[1]; TL=json.load(open(f'tl_{lang}.json'))['tl']
SR=48000; dur=TL['total']; N=int(SR*dur); t=np.arange(N)/SR
rng=np.random.default_rng(7)
bpm=96; beat=60/bpm
def lp(x,fc,o=2): return sosfilt(butter(o,fc,'low',fs=SR,output='sos'),x)
def hp(x,fc,o=2): return sosfilt(butter(o,fc,'high',fs=SR,output='sos'),x)
def env(n,a,r):
    e=np.ones(n); A=min(n,int(a*SR)); R=min(n,int(r*SR)); e[:A]=np.linspace(0,1,A); e[-R:]*=np.linspace(1,0,R); return e
mid=lambda m: 440*2**((m-69)/12)
chords=[[57,60,64,67],[53,57,60,64],[48,52,55,59],[55,59,62,65]]  # Am7 Fmaj7 Cmaj7 G7
bass=[45,41,36,43]
L=np.zeros(N); Rr=np.zeros(N)
bar=4*beat; seglen=2*bar
# pads
k=0; s=0.0
while s<dur:
    ch=chords[k%4]; n0=int(s*SR); n1=min(N,int((s+seglen+0.3)*SR)); n=n1-n0; tt=np.arange(n)/SR
    pad=np.zeros(n)
    for m in ch:
        f=mid(m)
        for det in (-0.12,0.0,0.12):
            ph=rng.random()*6.28
            pad+= (2*((tt*f*2**(det/12)+ph/6.28)%1)-1)*0.05
    pad=lp(pad,1400)*env(n,0.6,0.6)
    L[n0:n1]+=pad*1.0; Rr[n0:n1]+=np.roll(pad,240)
    # bass
    fb=mid(bass[k%4]); bb=np.sin(2*np.pi*fb*tt)*0.22+np.sin(2*np.pi*fb*2*tt)*0.05
    bb*=env(n,0.05,0.4); L[n0:n1]+=bb; Rr[n0:n1]+=bb
    s+=seglen; k+=1
# drums: kick on 1&3 (all beats in lift), hats on 8ths
def kick():
    n=int(0.35*SR); tt=np.arange(n)/SR; f=50+90*np.exp(-tt*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*9)*0.9
def hat():
    n=int(0.05*SR); return hp(rng.standard_normal(n),7000)*np.exp(-np.arange(n)/SR*90)*0.12
def snap():
    n=int(0.18*SR); return (hp(rng.standard_normal(n),1800)*np.exp(-np.arange(n)/SR*28))*0.22
K=kick(); Hh=hat(); Sn=snap()
def add(x,at,g=1.0,pan=0.0):
    n0=int(at*SR); n1=min(N,n0+len(x)); 
    if n0>=N: return
    L[n0:n1]+=x[:n1-n0]*g*(1-pan); Rr[n0:n1]+=x[:n1-n0]*g*(1+pan)
b=0
while b*beat<dur:
    at=b*beat; sec = 'kit' if at<TL['kitEnd'] else 'hero' if at<TL['heroEnd'] else 'night' if at<TL['nightEnd'] else 'ui' if at<TL['uiEnd'] else 'morn' if at<TL['mornEnd'] else 'end'
    if sec in ('kit','ui','morn'):
        add(K,at,1.0)
        if b%2==1: add(Sn,at,1.0)
        add(Hh,at,1.0,0.3); add(Hh,at+beat/2,0.7,-0.3)
    elif sec=='hero':
        if b%4==0: add(K,at,0.6)
        add(Hh,at+beat/2,0.4,0.2)
    elif sec=='night':
        if b%4==0: add(K,at,0.5)
    elif sec=='end' and at < TL['mornEnd']+beat*0.5:
        add(K,at,1.0)
    b+=1
# riser into UI and impact at hero->kit
def riser(a,b_):
    n0=int(a*SR); n1=int(b_*SR); n=n1-n0; x=hp(rng.standard_normal(n),3000)*np.linspace(0,1,n)**2*0.12; L[n0:n1]+=x; Rr[n0:n1]+=x
riser(TL['nightEnd']-1.2,TL['nightEnd']); riser(TL['kitEnd']-0.6,TL['kitEnd'])
for at in (0.0,TL['kitEnd'],TL['nightEnd'],TL['mornEnd']):
    add(K*1.2,at,1.0)
# master: gentle level shape, night darker via lowpass segment
mix=np.stack([L,Rr],1)
ns=int(TL['heroEnd']*SR); ne=int(TL['nightEnd']*SR)
for c in range(2): mix[ns:ne,c]=lp(mix[ns:ne,c],700)
fade=np.ones(N); fo=int(1.6*SR); fade[-fo:]=np.linspace(1,0,fo); fi=int(0.02*SR); fade[:fi]=np.linspace(0,1,fi)
mix*=fade[:,None]
mix/=np.max(np.abs(mix))*1.12
wavfile.write(f'music_{lang}.wav',SR,(mix*32767).astype(np.int16))
print('ok',dur)
