"""Broadcast-style compose: audio processed on its own (no gaps), crossfades between shots.
usage: compose2.py KEY TLDIR SRC_AUDIO OUT"""
import json, subprocess, sys, os
key, D, SRC, OUT = sys.argv[1:5]
J = json.load(open(f'{D}/tl_{key}.json')); T = J['total']; F = 0.32
zz = [(1.0, 1.08), (1.08, 1.02), (1.0, 1.07), (1.03, 1.1)]
segs = []
for s in J['bg']:
    s = list(s)
    while len(s) < 4: s.append(1.0)
    if len(s) < 5: s.append(False)
    segs.append(s)
# 1) audio alone, continuous, loudness-normalised
aud = f'{D}/aud_{key}.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-vn', '-af', f'aresample=48000,apad,atrim=0:{T},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000', '-ac', '2', aud], check=True)
# 2) background with crossfades
inp = []; fl = []; i = 0; starts = []; t = 0.0
for k, s in enumerate(segs):
    fn, ss, d, sp = s[0], s[1], s[2], s[3]; blur = bool(s[4]) if len(s) > 4 else False
    starts.append(t); t += d
    dd = d + (F if k < len(segs) - 1 else 0)
    if fn:
        inp += ['-ss', str(ss), '-t', f'{dd * sp + 0.2:.3f}', '-i', fn]; nf = max(1, int(round(dd * 30))); z0, z1 = zz[k % 4]
        fl.append(f"[{i}:v]setpts=PTS/{sp},fps=30,scale=2160:3840:flags=bicubic,setsar=1,zoompan=z='{z0}+({z1}-{z0})*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,"
                  + ("boxblur=22:2," if blur else "") + f"eq=contrast=1.04:saturation=1.06,unsharp=5:5:0.4,trim=duration={dd:.3f},setpts=PTS-STARTPTS,format=yuv420p,settb=1/30[v{k}]"); i += 1
    else:
        fl.append(f"color=c=0x131615:s=1080x1920:r=30:d={dd:.3f},setsar=1,format=yuv420p,settb=1/30[v{k}]")
prev = 'v0'
for k in range(1, len(segs)):
    off = starts[k]
    fl.append(f"[{prev}][v{k}]xfade=transition=fade:duration={F}:offset={off:.3f}[x{k}]"); prev = f'x{k}'
bgf = f'{D}/bg2_{key}.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fl), '-map', f'[{prev}]', '-t', str(T), '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', '30', bgf], check=True)
# 3) overlay graphics + mux audio (no audio filters here)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', bgf, '-framerate', '30', '-i', f'{D}/ov_{key}/%04d.png', '-i', aud,
                '-filter_complex', '[0:v][1:v]overlay=format=auto:eof_action=pass,format=yuv420p[vout]', '-map', '[vout]', '-map', '2:a',
                '-t', str(T), '-r', '30', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', OUT], check=True)
print('done', OUT)
