import json, subprocess, sys
key=sys.argv[1]; J=json.load(open(f'tl_{key}.json')); T=J['total']
inp=[]; fl=[]; i=0
zz=[(1.0,1.12),(1.12,1.02),(1.0,1.1),(1.04,1.14)]
for k,(fn,ss,d,sp) in enumerate(J['bg']):
    if fn:
        src=d*sp
        inp+=['-ss',str(ss),'-t',f'{src+0.15:.3f}','-i',fn]; nf=max(1,int(round(d*30))); z0,z1=zz[k%4]
        fl.append(f"[{i}:v]setpts=PTS/{sp},fps=30,scale=1620:2880:flags=lanczos,setsar=1,zoompan=z='{z0}+({z1}-{z0})*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,unsharp=5:5:0.5,eq=contrast=1.04:saturation=1.06,trim=duration={d:.3f},setpts=PTS-STARTPTS[v{k}]"); i+=1
    else:
        fl.append(f"color=c=0x131615:s=1080x1920:r=30:d={d:.3f},setsar=1[v{k}]")
n=len(J['bg']); fl.append(''.join(f'[v{k}]' for k in range(n))+f"concat=n={n}:v=1:a=0[bg]")
ov,vo,mu,sx=i,i+1,i+2,i+3
inp+=['-framerate','30','-i',f'ov_{key}/%04d.png','-i',f'vo_{key}.wav','-i',f'music_m_{key}.wav','-i',f'sfx_{key}.wav']
fl+=[f"[bg][{ov}:v]overlay=format=auto,format=yuv420p[vout]",
     f"[{vo}:a]highpass=f=80,acompressor=threshold=0.1:ratio=3:attack=5:release=120,volume=1.15,asplit=2[vo1][vo2]",
     f"[{mu}:a]volume=0.6[mus]", f"[mus][vo2]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=300[mduck]",
     f"[{sx}:a]volume=0.55[sfx]", f"[vo1][mduck][sfx]amix=inputs=3:normalize=0,alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=9[aout]"]
name={'busy':'OneTap_Ocupado_no_es_rentable','batt':'OneTap_Recarga_tu_negocio'}[key.split('_')[0]]
out=f"{name}_{key.split('_')[1].upper()}.mp4"
subprocess.run(['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(fl),'-map','[vout]','-map','[aout]','-t',str(T),'-c:v','libx264','-preset','medium','-crf','18','-profile:v','high','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',out],check=True); print('done',out)
