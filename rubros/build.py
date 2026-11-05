import json, subprocess, sys
R="/mnt/user-data/uploads/Downloads/OneTap anuncios/higgs/rubros/"
def f(k): import glob; return glob.glob(R+f"hf_20261105_{k}_*")[0]
CFG={
 'clin_es': dict(vo='022013', ph=[(0,2.79),(3.36,4.98),(5.49,8.82),(9.47,11.94),(12.58,16.05),(16.46,19.75),(20.42,22.33),(22.72,24.63),(24.96,27.09)],
   tx=['Agenda llena no siempre es agenda ordenada.','¿Cuántas citas se te pierden al mes?','Si llevas la agenda en papel o en WhatsApp, no eres el único.','Y confirmar cita por cita te roba la tarde.','Con OneTap, tu agenda va por profesional y sin cruces.','Y envía recordatorios por WhatsApp, sin costo por mensaje.','Cada mañana sabes cómo viene tu día.','Primer mes gratis, sin tarjeta.','onetaphq.com']),
 'clin_en': dict(vo='022027', ph=[(0,2.64),(3.27,5.04),(5.67,8.93),(9.60,12.21),(12.81,16.74),(17.18,19.90),(20.50,22.42),(23.07,25.20),(25.68,27.56)],
   tx=['A full schedule isn\'t always an organized one.','How many appointments slip away every month?','If your calendar lives on paper or in WhatsApp, you\'re not alone.','And confirming one by one steals your afternoon.','With OneTap, your schedule runs by professional, with zero overlaps.','And it sends WhatsApp reminders at no cost per message.','Every morning, you know how your day looks.','First month free. No card required.','onetaphq.com']),
 'manu_es': dict(vo='022041', ph=[(0,3.43),(4.28,6.32),(6.90,9.71),(10.22,12.05),(12.76,17.81),(18.43,20.68),(21.16,23.47),(24.12,26.11),(26.56,28.60)],
   tx=['Producción a tope no siempre es producción rentable.','¿Cuánto material se te va sin que lo sepas?','Si cuentas tu inventario en papel, no eres el único.','Y el conteo a mano te roba la noche.','Con OneTap, cada producción usa su lista de materiales y descuenta los insumos del inventario.','Con lotes y trazabilidad en cada bodega.','Y cada mañana sabes qué pedir antes de que falte.','Primer mes gratis, sin tarjeta.','onetaphq.com']),
 'manu_en': dict(vo='022051', ph=[(0,3.36),(4.10,6.18),(6.85,9.86),(10.47,12.37),(12.96,18.60),(19.04,21.37),(21.73,24.41),(24.96,26.98),(27.28,29.23)],
   tx=['A busy production floor isn\'t always a profitable one.','How much material slips away without you knowing?','If you still count inventory on paper, you\'re not alone.','And counting by hand steals your nights.','With OneTap, every production run uses its bill of materials and deducts raw materials from stock.','With lots and traceability across warehouses.','And every morning, you know what to reorder before you run out.','First month free. No card required.','onetaphq.com']),
}
GAP=[0.5,0.45,1.15,0.45,0.25,0.75,0.5,0.35,0]; LEAD=0.12
key=sys.argv[1]; c=CFG[key]
t=LEAD; parts=[]; segs=[]; S=[]
for i,(a,b) in enumerate(c['ph']):
    a2=max(0,a-0.05); b2=b+0.12; d=b2-a2
    parts.append((a2,b2,t)); segs.append([round(t+0.05,3),round(t+d-0.1,3),c['tx'][i]]); S.append(t+0.05); t+=d+GAP[i]
total=t+0.9
fl=[f"[0:a]atrim={a2}:{b2},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b2-a2-0.03}:d=0.03,adelay={int(at*1000)}|{int(at*1000)}[p{k}]" for k,(a2,b2,at) in enumerate(parts)]
fl.append(''.join(f'[p{k}]' for k in range(len(parts)))+f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{total}[out]")
subprocess.run(['ffmpeg','-v','error','-y','-i',f(c['vo']),'-filter_complex',';'.join(fl),'-map','[out]','-ar','48000','-ac','2',f'vo_{key}.wav'],check=True)
cut=lambda i: round(S[i]-0.15,3)
tl=dict(k1=round(S[0],3),p1=round(S[1],3),p1e=round(segs[1][1],3),p2=round(S[2],3),kitEnd=cut(1),heroEnd=cut(3),nightEnd=cut(4),uiEnd=cut(6),mornEnd=cut(7),total=round(total,3))
json.dump(dict(tl=tl,segs=segs),open(f'tl_{key}.json','w'),ensure_ascii=False)
kc=json.load(open('kcuts.json')) if __import__('os').path.exists('kcuts.json') else {}
kc[key]=[round(i*tl['kitEnd']/4,3) for i in range(4)]; json.dump(kc,open('kcuts.json','w'))
print(key,tl)
