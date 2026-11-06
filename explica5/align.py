"""Forced alignment of the known narration -> word timings json. usage: align.py WAV16 SCRIPT.json OUT.json"""
import wave, sys, json, re
import numpy as np
from pocketsphinx import Decoder
wav, scr, out = sys.argv[1:4]
w = wave.open(wav, 'rb'); a = np.frombuffer(w.readframes(w.getnframes()), np.int16)
MAP = {'onetap': 'one tap', 'onetap.': 'one tap', 'ai': 'ai', 'ai-powered': 'ai powered', 'pdf': 'p d f', 'onetaphq.com': 'one tap h q dot com', 'setup': 'set up'}
def toks(dw):
    k = re.sub(r"[^a-z0-9'.\-]", '', dw.lower()).strip('.')
    return MAP.get(k, k.replace('-', ' ')).split()
res = []
for s, e, text, *extra in json.load(open(scr)):
    hidden = extra[0] if extra else {}
    disp = text.split()
    al = []
    for i, dw in enumerate(disp):
        al.append((i, toks(dw)))
        for h in hidden.get(str(i), []): al.append((i, [h]))  # spoken-but-not-shown tokens attach to word i
    flat = [(i, t) for i, ts in al for t in ts]
    pad = .12; off = max(0, s - pad)
    d = Decoder(samprate=16000)
    d.set_align_text(' '.join(t for _, t in flat))
    try:
        d.start_utt(); d.process_raw(a[int(off * 16000):int((e + pad) * 16000)].tobytes(), full_utt=True); d.end_utt()
        segs = [x for x in d.seg() if x.word not in ('<s>', '</s>', '<sil>') and not x.word.startswith('[')]
    except Exception as ex:
        print('align fail', ex); segs = []
    times = [None] * len(disp)
    if len(segs) == len(flat):
        for (i, _), x in zip(flat, segs):
            st, en = off + x.start_frame / 100, off + (x.end_frame + 1) / 100
            if times[i] is None: times[i] = [st, en]
            else: times[i][1] = en
        ok = True
    else:
        ok = False; tot = sum(len(x) + 1 for x in disp); t = s
        for i, x in enumerate(disp):
            dd = (e - s) * (len(x) + 1) / tot; times[i] = [t, t + dd]; t += dd
    print(f'{s:6.2f} {"OK " if ok else "EVN"} ' + ' '.join(f'{x}@{tt[0]:.2f}' for x, tt in zip(disp, times)))
    res.append([[x, round(tt[0], 3), round(tt[1], 3)] for x, tt in zip(disp, times)])
json.dump(res, open(out, 'w'), ensure_ascii=False)
