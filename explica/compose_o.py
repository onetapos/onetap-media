import json, subprocess, sys
key=sys.argv[1]; D=sys.argv[2] if len(sys.argv)>2 else '.'; SRC=sys.argv[3]; OUT=sys.argv[4]
J=json.load(open(f'{D}/tl_{key}.json')); T=J['total']
inp=[]; fl=[]; i=0
zz=[(1.0,1.12),(1.12,1.02),(1.0,1.1),(1.04,1.14)]
for k,seg in enumerate(J['bg']):
    fn,ss,d,sp=seg[:4]; blur=len(seg)>4
    if fn:
        src=d*sp
        inp+=['-ss',str(ss),'-t',f'{src+0.15:.3f}','-i',fn]; nf=max(1,int(round(d*30))); z0,z1=zz[k%4]
        fl.append(f"[{i}:v]setpts=PTS/{sp},fps=30,scale=3240:5760:flags=bicubic,setsar=1,zoompan=z='{z0}+({z1}-{z0})*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,unsharp=5:5:0.5,eq=contrast=1.04:saturation=1.06,"+("boxblur=22:2," if blur else "")+f"trim=duration={d:.3f},setpts=PTS-STARTPTS[v{k}]"); i+=1
    else:
        fl.append(f"color=c=0x131615:s=1080x1920:r=30:d={d:.3f},setsar=1[v{k}]")
n=len(J['bg']); fl.append(''.join(f'[v{k}]' for k in range(n))+f"concat=n={n}:v=1:a=0[bg]")
bgf=f'{D}/bg_{key}.mp4'
subprocess.run(['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(fl),'-map','[bg]','-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p',bgf],check=True)
inp2=['-i',bgf,'-framerate','30','-i',f'{D}/ov_{key}/%04d.png','-i',SRC]
fl2=["[0:v][1:v]overlay=format=auto:eof_action=pass,format=yuv420p[vout]", f"[2:a]apad,atrim=0:{T},loudnorm=I=-14:TP=-1.5:LRA=11[aout]"]
out=OUT
subprocess.run(['ffmpeg','-v','error','-y']+inp2+['-filter_complex',';'.join(fl2),'-map','[vout]','-map','[aout]','-t',str(T),'-c:v','libx264','-preset','medium','-crf','18','-profile:v','high','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',out],check=True); print('done',out)
