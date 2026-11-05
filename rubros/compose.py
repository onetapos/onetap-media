import json, subprocess, sys, glob
key=sys.argv[1]; vert=key.split('_')[0]; J=json.load(open(f'tl_{key}.json')); T=J['tl']
R="/mnt/user-data/uploads/Downloads/OneTap anuncios/higgs/rubros/"
f=lambda k: glob.glob(R+f"hf_20261105_{k}_*.mp4")[0]
CL={'clin':dict(chaos='021739',cuts=[0.5,2.0,4.6,6.6],hero=('021757',3.0),night=('021816',3.0),morn=('021834',4.0)),
    'manu':dict(chaos='021851',cuts=[0.4,2.4,4.4,8.4],hero=('021910',2.0),night=('021927',3.0),morn=('021939',2.0))}[vert]
kd=T['kitEnd']/4; K=f(CL['chaos'])
zz=[(1.10,1.0),(1.0,1.08),(1.08,1.0),(1.0,1.1)]
segs=[(K,CL['cuts'][i],kd,0.7 if i==0 else 0.55,*zz[i]) for i in range(4)]
segs+=[(f(CL['hero'][0]),CL['hero'][1],T['heroEnd']-T['kitEnd'],0.4,1.0,1.10),
       (f(CL['night'][0]),CL['night'][1],T['nightEnd']-T['heroEnd'],0.3,1.0,1.12),
       (None,0,T['uiEnd']-T['nightEnd'],0,1,1),
       (f(CL['morn'][0]),CL['morn'][1],T['mornEnd']-T['uiEnd'],0.3,1.12,1.0),
       (None,0,T['total']-T['mornEnd'],0,1,1)]
inp=[]; fl=[]; i=0
for k,(fn,ss,d,vol,z0,z1) in enumerate(segs):
    if fn:
        inp+=['-ss',str(ss),'-t',f'{d+0.1:.3f}','-i',fn]; nf=max(1,int(round(d*30)))
        fl.append(f"[{i}:v]fps=30,scale=1620:2880:flags=bicubic,setsar=1,zoompan=z='{z0}+({z1}-{z0})*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,eq=contrast=1.05:saturation=1.08,trim=duration={d:.3f},setpts=PTS-STARTPTS[v{k}]")
        fl.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration={d:.3f},asetpts=PTS-STARTPTS,volume={vol},afade=t=in:d=0.03,afade=t=out:st={max(0,d-0.06):.3f}:d=0.06[a{k}]"); i+=1
    else:
        fl.append(f"color=c=0x131615:s=1080x1920:r=30:d={d:.3f},setsar=1[v{k}]"); fl.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d:.3f}[a{k}]")
n=len(segs); fl.append(''.join(f'[v{k}][a{k}]' for k in range(n))+f"concat=n={n}:v=1:a=1[bg][amb]")
ov,vo,mu,sx=i,i+1,i+2,i+3
inp+=['-framerate','30','-i',f'ov_{key}/%04d.png','-i',f'vo_{key}.wav','-i',f'music_{key}.wav','-i',f'sfx_{key}.wav']
fl+= [f"[bg][{ov}:v]overlay=format=auto,format=yuv420p[vout]",
      f"[{vo}:a]highpass=f=80,acompressor=threshold=0.1:ratio=3:attack=5:release=120,volume=1.15,asplit=2[vo1][vo2]",
      f"[{mu}:a]volume=0.6[mus]", f"[mus][vo2]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=300[mduck]",
      f"[{sx}:a]volume=0.55[sfx]", f"[vo1][mduck][amb][sfx]amix=inputs=4:normalize=0,alimiter=limit=0.95,loudnorm=I=-13.5:TP=-1.5:LRA=9[aout]"]
names={'clin':'Clinicas','manu':'Manufactura'}
out=f"OneTap_{names[vert]}_Cine_{key.split('_')[1].upper()}.mp4"
subprocess.run(['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(fl),'-map','[vout]','-map','[aout]','-t',str(T['total']),'-c:v','libx264','-preset','medium','-crf','17','-profile:v','high','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',out],check=True); print('done',out)
