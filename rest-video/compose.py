import json, subprocess, sys
lang=sys.argv[1]; DEBUG=len(sys.argv)>2; J=json.load(open(f'tl_{lang}.json')); T=J['tl']
H="/mnt/user-data/uploads/Downloads/OneTap anuncios/higgs/"
K=H+"hf_20261105_010246_ebb961b1-e45e-43d5-b1a2-430915b986e9.mp4"
R=H+"hf_20261105_010227_ae33ab28-206a-4c67-b16f-9bce09822d72.mp4"
Nn=H+"hf_20261105_011531_0b6a8633-d402-46f6-a55a-77b7ede2a2d7.mp4"
M=H+"hf_20261105_010838_391f1c9b-6902-4690-b8c3-811358fdf92b.mp4"
segs=[(K,0.3,T['kitEnd'],0.55),(R,2.4,T['heroEnd']-T['kitEnd'],0.4),(Nn,4.4,T['nightEnd']-T['heroEnd'],0.35),(None,0,T['uiEnd']-T['nightEnd'],0),(M,3.0,T['mornEnd']-T['uiEnd'],0.3),(None,0,T['total']-T['mornEnd'],0)]
inp=[]; fl=[]; vlab=[]; alab=[]; i=0
for k,(f,ss,d,vol) in enumerate(segs):
    if f:
        inp+=['-ss',str(ss),'-t',f'{d:.3f}','-i',f]
        fl.append(f"[{i}:v]fps=30,scale=1080:1920,setsar=1,eq=contrast=1.04:saturation=1.06,trim=duration={d:.3f},setpts=PTS-STARTPTS[v{k}]")
        fl.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration={d:.3f},asetpts=PTS-STARTPTS,volume={vol},afade=t=in:d=0.05,afade=t=out:st={max(0,d-0.08):.3f}:d=0.08[a{k}]")
        i+=1
    else:
        fl.append(f"color=c=0x131615:s=1080x1920:r=30:d={d:.3f},setsar=1[v{k}]")
        fl.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d:.3f}[a{k}]")
    vlab.append(f'[v{k}]'); alab.append(f'[a{k}]')
n=len(segs)
fl.append(''.join(f'[v{k}][a{k}]' for k in range(n))+f"concat=n={n}:v=1:a=1[bg][amb]")
ov=i; vo=i+1; mu=i+2
inp+=['-framerate','30','-i',f'ov_{lang}/%04d.png','-i',f'vo_{lang}.wav','-i',f'music_{lang}.wav']
fl.append(f"[bg][{ov}:v]overlay=format=auto,format=yuv420p[vout]") if not DEBUG else fl.append('[bg]null[vout]')
fl.append(f"[{vo}:a]asplit=2[vo1][vo2]")
fl.append(f"[{mu}:a]volume=0.55[mus]")
fl.append(f"[mus][vo2]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[mduck]")
fl.append(f"[vo1][mduck][amb]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[aout]")
cmd=['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(fl),'-map','[vout]','-map','[aout]','-t',str(T['total']),'-c:v','libx264','-preset',('ultrafast' if DEBUG else 'medium'),'-crf','18','-profile:v','high','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',(f'dbg_{lang}.mp4' if DEBUG else f'OneTap_Restaurantes_Cine_{lang.upper()}.mp4')]
subprocess.run(cmd,check=True); print('done',lang)
