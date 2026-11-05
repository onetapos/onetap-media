import json, subprocess, sys
K="/mnt/user-data/uploads/Downloads/OneTap anuncios/higgs/kevin2/"
O="/mnt/user-data/uploads/Downloads/OneTap anuncios/higgs/originales/"
A1=O+"hf_20261031_215612_ed5b326a-7207-4267-ba70-b62a75014dcf.mp4"; A2=O+"hf_20261031_215617_d7ba243c-43eb-49c4-b4ae-621889975d68.mp4"
B1=O+"hf_20261031_225236_439cc882-d69b-46ad-974e-66d5457abe94.mp4"; B2=O+"hf_20261031_225256_d4429bbf-29ca-4430-95fe-d09ab58f1eb5.mp4"
CFG={
 'owner_es': dict(vo='vo_A_es', ph=[(0,1.57),(2.08,7.79),(8.20,9.43),(10.04,15.81),(16.24,17.88),(18.31,20.22),(20.62,22.75)],
   tx=['Soy dueño de negocio.','Pero también soy el comprador, el cajero, el contador, el de inventario, el de marketing, el de soporte...','y el equipo completo.','Con OneTap, ventas, inventario, costos, equipo y finanzas quedan conectados.','No tienes que hacerlo todo solo.','Primer mes gratis, sin tarjeta.','onetaphq.com']),
 'owner_en': dict(vo='vo_A_en', ph=[(0,1.14),(1.74,7.91),(8.31,9.46),(10.01,15.23),(15.83,17.22),(17.71,20.03),(20.37,22.05)],
   tx=['I\'m a business owner.','But I\'m also the buyer, the cashier, the bookkeeper, the stock manager, the marketing team, customer support...','and the entire team.','With OneTap, sales, stock, costs, team and finances are all connected.','You don\'t have to do it all alone.','First month free. No card required.','onetaphq.com']),
 'moved_es': dict(vo='vo_B_es', ph=[(0,1.60),(2.08,2.67),(3.17,4.66),(5.07,7.22),(7.53,8.83),(9.41,11.10),(11.39,13.69),(14.07,16.73),(17.24,19.57),(20.08,24.27)],
   tx=['Los negocios ya cambiaron.','¿Y el tuyo?','¿Sigues haciéndolo todo a mano?','Mientras te pones al día con el papeleo...','tu competencia te alcanza.','Conoce tu nueva forma de operar.','OneTap conecta todo tu negocio.','Le das tus facturas y actualiza inventario y costos.','Menos papeleo. Más tiempo para crecer.','Primer mes gratis, sin tarjeta. onetaphq.com']),
 'moved_en': dict(vo='vo_B_en', ph=[(0,1.29),(1.73,2.14),(2.64,4.06),(4.63,6.22),(6.50,8.34),(8.82,10.34),(10.69,12.50),(12.81,15.76),(16.18,18.36),(18.67,20.83),(21.16,22.99)],
   tx=['Business has moved on.','Have you?','Still doing it all by hand?','While you catch up on paperwork...','your competition catches up with you.','Meet your new way to operate.','OneTap connects your whole business.','Feed it your invoices, and it updates stock and costs.','Less busywork. More time to grow.','First month free. No card required.','onetaphq.com']),
}
key=sys.argv[1]; c=CFG[key]; n=len(c['ph'])
t=0.15; parts=[]; segs=[]; S=[]; E=[]
for i,(a,b) in enumerate(c['ph']):
    a2=max(0,a-0.05); b2=b+0.12; d=b2-a2
    parts.append((a2,b2,t)); segs.append([round(t+0.05,3),round(t+d-0.1,3),c['tx'][i]]); S.append(t+0.05); E.append(t+d-0.1)
    gap=0.32
    if key.startswith('owner') and i in (2,): gap=0.5
    if key.startswith('moved') and i in (4,): gap=0.45
    t+=d+gap
total=t+1.0
fl=[f"[0:a]atrim={a2}:{b2},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b2-a2-0.03}:d=0.03,adelay={int(at*1000)}|{int(at*1000)}[p{k}]" for k,(a2,b2,at) in enumerate(parts)]
fl.append(''.join(f'[p{k}]' for k in range(n))+f"amix=inputs={n}:normalize=0,apad,atrim=0:{total}[out]")
subprocess.run(['ffmpeg','-v','error','-y','-i',K+c['vo']+'.mp3','-filter_complex',';'.join(fl),'-map','[out]','-ar','48000','-ac','2',f'vo_{key}.wav'],check=True)
lang=key.split('_')[1]; L=lambda es,en: es if lang=='es' else en
G=lambda s: f'<span class="gold">{s}</span>'
cut=lambda i: round(S[i]-0.12,3)
if key.startswith('owner'):
    endT=cut(5)
    beats=[dict(type='big',a=S[0]-0.1,b=S[1]-0.1,w=L(['Soy','dueño','de',G('negocio.')],['I\'m','a','business',G('owner.')])),
      dict(type='chips',a=S[1],b=cut(3),items=L(['Comprador','Cajero','Contador','Inventario','Marketing','Soporte','Compras','Planilla','Agenda','Facturas','Cobros','Proveedores','Reclutador','Analista','Bodega','Precios'],
                                              ['Buyer','Cashier','Bookkeeper','Stock manager','Marketing','Support','Purchasing','Payroll','Scheduler','Invoices','Collections','Suppliers','Recruiter','Analyst','Warehouse','Pricing']),until=E[1]),
      dict(type='big',a=S[2]-0.05,b=cut(3),w=L(['Y','el','equipo',G('completo.')],['And','the','entire',G('team.')])),
      dict(type='big',a=S[3]-0.05,b=S[3]+1.6,w=L([G('Con'),G('OneTap...')],[G('With'),G('OneTap...')])),
      dict(type='flow',a=S[3]+1.3,b=cut(4)+0.05,items=L(['Ventas','Inventario','Costos','Equipo','Finanzas'],['Sales','Stock','Costs','Team','Finances']),cap=L('Todo conectado','All connected')),
      dict(type='big',a=S[4]-0.05,b=endT,w=L(['No','tienes','que','hacerlo','todo',G('solo.')],['You','don\'t','have','to','do','it','all',G('alone.')]))]
    subs=[1,3]
    bg=[(A1,0.0,cut(3)),(A2,0.0,endT-cut(3))]
    endl=L('No tienes que hacerlo<br>todo solo.','You don\'t have to<br>do it all alone.')
else:
    endT=cut(9)
    beats=[dict(type='big',a=S[0]-0.1,b=cut(2),w=L(['Los','negocios','ya',G('cambiaron.'),'¿Y','el','tuyo?'],['Business','has','moved',G('on.'),'Have','you?']),split=L(4,4),second=S[1]),
      dict(type='big',a=S[2]-0.05,b=cut(3),w=L(['¿Sigues','haciéndolo','todo','a',G('mano?')],['Still','doing','it','all','by',G('hand?')])),
      dict(type='chips',a=S[3],b=cut(4),items=L(['Facturas','Excel','Papeles','Recibos','Inventario a mano','Notas'],['Invoices','Spreadsheets','Paperwork','Receipts','Manual stock','Notes']),until=E[3],few=True),
      dict(type='big',a=S[4]-0.05,b=cut(5),w=L(['Tu','competencia','te',G('alcanza.')],['Your','competition','catches',G('up.')])),
      dict(type='big',a=S[5]-0.05,b=cut(6),w=L(['Conoce','tu','nueva','forma','de',G('operar.')],['Meet','your','new','way','to',G('operate.')])),
      dict(type='flow',a=S[6],b=cut(7),items=L(['Ventas','Inventario','Costos','Equipo'],['Sales','Stock','Costs','Team']),cap=L('OneTap conecta tu negocio','OneTap connects your business')),
      dict(type='checks',a=S[7],b=cut(8),items=L(['Factura leída','Inventario actualizado','Costos actualizados'],['Invoice read','Stock updated','Costs updated'])),
      dict(type='big',a=S[8]-0.05,b=endT,w=L(['Menos',G('papeleo.'),'Más','tiempo','para',G('crecer.')],['Less',G('busywork.'),'More','time','to',G('grow.')]))]
    subs=[3,6,7]
    b1a=cut(4)  # first part of race until competition line
    bg=[(B1,0.0,b1a),(B1,10.0,cut(5)-b1a),(B2,0.0,endT-cut(5))]
    endl=L('Que no te dejen atrás.<br>Automatiza con OneTap.','Don\'t get left behind.<br>Automate with OneTap.')
json.dump(dict(total=round(total,3),end=endT,beats=beats,segs=[segs[i] for i in subs],bg=bg,endl=endl,lang=lang),open(f'tl_{key}.json','w'),ensure_ascii=False)
print(key,'total',round(total,2),'end',endT,[round(x,2) for x in S])
