import json, subprocess, sys
K="/mnt/user-data/uploads/Downloads/OneTap anuncios/higgs/kevin/"
H="/mnt/user-data/uploads/Downloads/OneTap anuncios/higgs/"
CFG={
 'es': dict(f=K+"hf_20261105_014325_2ff9399b-4b5f-4469-bab1-e2cdf5f9154e.mp3",
  ph=[(3.67,4.85),(5.27,7.85),(0.0,3.22),(8.30,10.26),(10.77,12.35),(12.60,17.00),(17.43,20.44),(20.81,22.46),(22.81,24.76)],
  tx=['¿Cuánto te deja este plato?','Si no lo sabes al centavo, no eres el único.','Restaurante lleno no siempre es restaurante rentable.','Y el cierre a mano te roba la noche.','Sube tu carta a OneTap.','Calcula el costo real de cada plato y lo actualiza con cada factura del proveedor.','Y cada mañana te da tres acciones para cuidar tu margen.','Primer mes gratis, sin tarjeta.','onetaphq.com']),
 'en': dict(f=K+"hf_20261105_014332_25cadce6-0326-4e15-b05c-df2b33e717e6.mp3",
  ph=[(3.79,5.22),(5.94,8.10),(0.0,2.94),(8.63,10.82),(11.33,12.69),(13.08,17.69),(18.15,21.32),(21.86,23.96),(24.35,26.04)],
  tx=['What does this plate really make you?','If you don\'t know it to the cent, you\'re not alone.','A full restaurant isn\'t always a profitable one.','And closing out by hand steals your nights.','Upload your menu to OneTap.','It calculates the real cost of every dish, and updates it with every supplier invoice.','And every morning, it gives you three actions to protect your margin.','First month free. No card required.','onetaphq.com']),
}
# gap AFTER phrase i
ORDER=[2,0,1,3,4,5,6,7,8]
GAP=[0.55,0.45,1.15,0.45,0.25,0.75,0.5,0.35,0]
LEAD=0.12
for lang,c in CFG.items():
    t=LEAD; parts=[]; segs=[]; starts=[]
    for i,oi in enumerate(ORDER):
        a,b=c['ph'][oi]
        a2=max(0,a-0.05); b2=b+0.12; d=b2-a2
        parts.append((a2,b2,t)); segs.append([round(t+0.05,3),round(t+d-0.1,3),c['tx'][oi]]); starts.append(t+0.05)
        t+=d+GAP[i]
    total=t+0.9
    # build audio with adelay
    fl=[]; inputs=[]
    for k,(a2,b2,at) in enumerate(parts):
        fl.append(f"[0:a]atrim={a2}:{b2},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b2-a2-0.03}:d=0.03,adelay={int(at*1000)}|{int(at*1000)}[p{k}]")
    fl.append(''.join(f'[p{k}]' for k in range(len(parts)))+f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{total}[out]")
    subprocess.run(['ffmpeg','-v','error','-y','-i',c['f'],'-filter_complex',';'.join(fl),'-map','[out]','-ar','48000','-ac','2',f'vo_{lang}.wav'],check=True)
    S=starts; cut=lambda i: round(S[i]-0.15,3)
    tl=dict(k1=round(S[0],3),p1=round(S[1],3),p1e=round(segs[1][1],3),p2=round(S[2],3),kitEnd=cut(1),heroEnd=cut(3),nightEnd=cut(4),uiEnd=cut(6),mornEnd=cut(7),total=round(total,3))
    json.dump(dict(tl=tl,segs=segs),open(f'tl_{lang}.json','w'),ensure_ascii=False)
    print(lang,tl)
