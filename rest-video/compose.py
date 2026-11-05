import json, subprocess, sys
lang=sys.argv[1]; J=json.load(open(f'tl_{lang}.json')); T=J['tl']
H="/mnt/user-data/uploads/Downloads/OneTap anuncios/higgs/"
K=H+"hf_20261105_010246_ebb961b1-e45e-43d5-b1a2-430915b986e9.mp4"
R=H+"hf_20261105_010227_ae33ab28-206a-4c67-b16f-9bce09822d72.mp4"
Nn=H+"hf_20261105_011531_0b6a8633-d402-46f6-a55a-77b7ede2a2d7.mp4"
M=H+"hf_20261105_010838_391f1c9b-6902-4690-b8c3-811358fdf92b.mp4"
kd=T['kitEnd']/4
# (file, start, dur, ambience vol, zoom from, zoom to)
segs=[(K,0.6,kd,0.75,1.10,1.0),(K,4.0,kd,0.6,1.0,1.08),(K,6.0,kd,0.6,1.08,1.0),(K,7.3,kd,0.6,1.0,1.1),
      (R,2.4,T['heroEnd']-T['kitEnd'],0.35,1.0,1.10),
      (Nn,4.2,T['nightEnd']-T['heroEnd'],0.3,1.0,1.12),
      (None,0,T['uiEnd']-T['nightEnd'],0,1,1),
      (M,3.0,T['mornEnd']-T['uiEnd'],0.3,1.12,1.0),
      (None,0,T['total']-T['mornEnd'],0,1,1)]
inp=[]; fl=[]; i=0
for k,(f,ss,d,vol,z0,z1) in enumerate(segs):
    if f:
        inp+=['-ss',str(ss),'-t',f'{d+0.1:.3f}','-i',f]
        nf=max(1,int(round(d*30)))
        z=f"{z0}+({z1}-{z0})*on/{nf}"
        fl.append(f"[{i}:v]fps=30,scale=1620:2880:flags=bicubic,setsar=1,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,eq=contrast=1.05:saturation=1.08,trim=duration={d:.3f},setpts=PTS-STARTPTS[v{k}]")
        fl.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration={d:.3f},asetpts=PTS-STARTPTS,volume={vol},afade=t=in:d=0.03,afade=t=out:st={max(0,d-0.06):.3f}:d=0.06[a{k}]")
        i+=1
    else:
        fl.append(f"color=c=0x131615:s=1080x1920:r=30:d={d:.3f},setsar=1[v{k}]")
        fl.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d:.3f}[a{k}]")
n=len(segs)
fl.append(''.join(f'[v{k}][a{k}]' for k in range(n))+f"concat=n={n}:v=1:a=1[bg][amb]")
ov=i; vo=i+1; mu=i+2; sx=i+3
inp+=['-framerate','30','-i',f'ov_{lang}/%04d.png','-i',f'vo_{lang}.wav','-i',f'music_{lang}.wav','-i',f'sfx_{lang}.wav']
fl.append(f"[bg][{ov}:v]overlay=format=auto,format=yuv420p[vout]")
fl.append(f"[{vo}:a]highpass=f=80,acompressor=threshold=0.1:ratio=3:attack=5:release=120,volume=1.15,asplit=2[vo1][vo2]")
fl.append(f"[{mu}:a]volume=0.6[mus]")
fl.append(f"[mus][vo2]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=300[mduck]")
fl.append(f"[{sx}:a]volume=0.55[sfx]")
fl.append(f"[vo1][mduck][amb][sfx]amix=inputs=4:normalize=0,alimiter=limit=0.95,loudnorm=I=-13.5:TP=-1.5:LRA=9[aout]")
cmd=['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(fl),'-map','[vout]','-map','[aout]','-t',str(T['total']),'-c:v','libx264','-preset','medium','-crf','17','-profile:v','high','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',f'OneTap_Restaurantes_Cine_v2_{lang.upper()}.mp4']
subprocess.run(cmd,check=True); print('done',lang)
