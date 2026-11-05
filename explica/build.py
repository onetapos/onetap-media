import json, subprocess, sys
R="/mnt/user-data/uploads/Downloads/OneTap anuncios/higgs/robot/"
K="/mnt/user-data/uploads/Downloads/OneTap anuncios/higgs/kevin3/"
r1=R+"hf_20261031_175609_91e84310-9083-449e-a1b5-d1e1b7f23c36.mp4"; r2=R+"hf_20261031_175617_2cba802e-4cf0-48c2-ab19-81b4e1938252.mp4"
r3=R+"hf_20261031_182527_fb2a69bd-bffd-43dc-bb4d-ff41f1d2c9c7.mp4"; r4=R+"hf_20261031_182534_8f77422b-1571-46c9-8fc2-9d7ed48ee138.mp4"
r5=R+"hf_20261031_182540_370214df-8ea5-4601-937c-2d1b3f1cb765.mp4"; r6=R+"hf_20261031_182547_3201952a-5fb4-4776-8747-c5aa3581d93c.mp4"
O=0.30  # voice lead-in
G=lambda s: f'<span class="gold">{s}</span>'
# voice markers (seconds in the raw Kevin take)
M={
 'busy_en':dict(vo='vo_C_en',hook=0.00,hook2=0.89,q=2.85,q2=4.17,simple=6.18,s1=8.46,s2=14.28,s3=19.87,s4=23.92,less=27.39,more=28.44,end=29.55,dur=33.65),
 'busy_es':dict(vo='vo_C_es',hook=0.18,hook2=0.95,q=2.77,q2=4.06,simple=5.75,s1=8.04,s2=14.67,s3=21.01,s4=25.60,less=29.89,more=31.03,end=32.34,dur=36.75),
 'batt_en':dict(vo='vo_D_en',dream=0.20,dream2=2.15,paper=3.99,sell=6.04,count=6.76,check=7.39,repeat=8.02,missed=9.08,costly=10.11,empty=11.66,recharge=13.57,
                s1=15.65,s2=18.62,s3=21.32,s4=23.94,cust=28.28,fin=30.13,coffee=31.12,end=32.60,dur=36.60),
 'batt_es':dict(vo='vo_D_es',dream=0.05,dream2=2.06,paper=3.55,sell=5.56,count=6.51,check=7.40,repeat=8.43,missed=9.64,costly=10.89,empty=12.34,recharge=14.58,
                s1=16.96,s2=19.91,s3=23.01,s4=25.22,cust=30.58,fin=32.44,coffee=33.42,end=35.21,dur=39.63),
}
key=sys.argv[1]; m={k:(v+O if isinstance(v,float) else v) for k,v in M[key].items()}; lang=key.split('_')[1]; L=lambda es,en: es if lang=='es' else en
total=round(M[key]['dur']+O+0.9,3); endT=round(m['end']-0.1,3)
subprocess.run(['ffmpeg','-v','error','-y','-i',K+M[key]['vo']+'.mp3','-af',f'adelay={int(O*1000)}|{int(O*1000)},apad,atrim=0:{total}','-ar','48000','-ac','2',f'vo_{key}.wav'],check=True)
def big(a,b,w,at=None,**kw):
    d=dict(type='big',a=round(a,3),b=round(b,3),w=w);
    if at: d['at']=[round(x,3) for x in at]
    d.update(kw); return d
beats=[]; flash=[]; bg=[]
if key.startswith('busy'):
    w1=L(['Ocupado','<span class="neq">≠</span>',G('rentable.')],['Busy','<span class="neq">≠</span>',G('profitable.')])
    beats.append(big(m['hook']-0.05,m['q']-0.1,w1,at=[m['hook']-0.05,m['hook2']+0.05,m['hook2']+0.45],cls='huge',top=330))
    wq=L(['Vendes','todo','el','día...','¿Cuánto','te',G('deja?')],['You','sell','all','day...','What','do','you',G('keep?')])
    n1=4; at=[m['q']+i*0.18 for i in range(n1)]+[m['q2']+i*0.16 for i in range(len(wq)-n1)]
    beats.append(big(m['q']-0.05,m['simple']-0.1,wq,at=at))
    beats.append(big(m['simple']-0.05,m['s1']-0.2,L([G('OneTap:'),'así','de','simple.'],[G('OneTap:'),'this','simple.']),step=0.16))
    flash.append(m['simple'])
    steps=[dict(t=m['s1'],scr='import',h=L('Sube tu carta o lista de precios','Upload your menu or price list')),
           dict(t=m['s2'],scr='invoice',h=L('Tómale foto a cada factura','Snap every supplier invoice')),
           dict(t=m['s3'],scr='margin',h=L('Vende y mira tu margen','Sell and see your margins')),
           dict(t=m['s4'],scr='brief',h=L('Cada mañana, 3 acciones','Every morning, 3 actions'))]
    ui=dict(type='ui',a=round(m['s1']-0.2,3),b=round(m['less']-0.1,3),steps=steps)
    beats.append(ui)
    beats.append(big(m['less']-0.05,endT,L(['Menos',G('papeleo.'),'Más',G('negocio.')],['Less',G('paperwork.'),'More',G('business.')]),at=[m['less'],m['less']+0.2,m['more'],m['more']+0.18]))
    bg=[(r1,0.0,m['q2']-0.1,1.0),(r1,10.0,m['simple']-(m['q2']-0.1),1.0),(r5,5.6,ui['a']-m['simple'],1.0),(None,0,ui['b']-ui['a'],1),(r2,11.0,endT-ui['b'],1.0)]
    endl=L('Menos papeleo.<br>Más negocio.','Less paperwork.<br>More business.')
    tlm=dict(kitEnd=ui['a'],heroEnd=ui['a'],nightEnd=ui['a'],uiEnd=ui['b'],mornEnd=endT,total=total)
else:
    beats.append(big(m['dream']-0.05,m['paper']-0.1,L(['Un','gran',G('sueño.'),'Batería',G('llena.')],['A','big',G('dream.'),'Full',G('battery.')]),
        at=[m['dream'],m['dream']+0.2,m['dream']+0.45,m['dream2'],m['dream2']+0.25]))
    beats.append(big(m['paper']-0.05,m['sell']-0.1,L(['Luego','llegó','el',G('papeleo.')],['Then','came','the',G('paperwork.')]),step=0.14))
    beats.append(big(m['sell']-0.05,m['missed']-0.1,L(['Vender.','Contar.','Revisar.',G('Repetir.')],['Sell.','Count.','Check.',G('Repeat.')]),at=[m['sell'],m['count'],m['check'],m['repeat']]))
    wm=L(['Ventas',G('perdidas.'),'Errores','que',G('cuestan.')],['Missed',G('sales.'),'Costly',G('mistakes.')])
    at=[m['missed'],m['missed']+0.2]+[m['costly']+i*0.15 for i in range(len(wm)-2)]
    beats.append(big(m['missed']-0.05,m['empty']-0.1,wm,at=at))
    beats.append(big(m['empty']-0.05,m['recharge']-0.1,L(['Hasta','quedarte','sin',G('batería.')],['Running','on',G('empty.')]),step=0.16))
    beats.append(big(m['recharge']-0.05,m['s1']-0.2,L(['Recarga','tu','negocio','con',G('OneTap.')],['Recharge','your','business','with',G('OneTap.')]),step=0.15))
    flash.append(m['recharge']+1.3)
    steps=[dict(t=m['s1'],scr='import',h=L('Sube un archivo: tu negocio, armado','Upload one file: your business, set up')),
           dict(t=m['s2'],scr='invoice',h=L('Cada factura actualiza inventario y costos','Every invoice updates stock and costs')),
           dict(t=m['s3'],scr='brief',h=L('Cada mañana, qué hacer primero','Every morning, what to do first')),
           dict(t=m['s4'],scr='chat',h=L('Pregúntale a tu asistente','Ask your assistant'))]
    ui=dict(type='ui',a=round(m['s1']-0.2,3),b=round(m['cust']-0.1,3),steps=steps)
    beats.append(ui)
    beats.append(big(m['cust']-0.05,m['fin']-0.1,L(['Más','tiempo','para','tus',G('clientes.')],['More','time','for','your',G('customers.')]),step=0.13))
    wf=L(['Y','por','fin...','disfruta','ese',G('café.')],['And','finally...','enjoy','that',G('coffee.')])
    nf=L(3,2); at=[m['fin']+i*0.18 for i in range(nf)]+[m['coffee']+i*0.18 for i in range(len(wf)-nf)]
    beats.append(big(m['fin']-0.05,endT,wf,at=at))
    rc=m['recharge']
    beats.append(dict(type='batt',win=[[m['dream']-0.1,ui['a']],[ui['b'],endT]],charge=[rc+0.1,rc+1.5],
        k=[[m['dream'],100],[m['paper'],100],[m['paper']+1.4,82],[m['sell'],74],[m['repeat']+0.4,48],[m['missed'],38],[m['costly']+0.8,20],[m['empty'],12],[m['empty']+1.2,3],[rc+0.1,3],[rc+1.5,100]]))
    bg=[(r3,0.2,m['paper'],1.0),(r3,8.2,m['sell']-m['paper'],1.0),(r1,1.0,m['missed']-m['sell'],1.0),(r4,1.6,m['empty']-m['missed'],1.0),(r4,9.0,rc-m['empty'],1.0),
        (r5,5.5,ui['a']-rc,1.0),(None,0,ui['b']-ui['a'],1),(r6,0.3,m['fin']-ui['b'],1.0),(r6,6.2,endT-m['fin'],1.0)]
    endl=L('Ahorra tiempo.<br>Disfruta tu negocio.','Save time.<br>Enjoy your business.')
    tlm=dict(kitEnd=m['missed'],heroEnd=m['empty'],nightEnd=ui['a'],uiEnd=ui['b'],mornEnd=endT,total=total)
for f in flash: beats.append(dict(type='flash',a=round(f,3)))
bg=[(fn,ss,round(d,3),sp) for fn,ss,d,sp in bg]; bg.append((None,0,round(total-endT,3),1))
assert abs(sum(d for _,_,d,_ in bg)-total)<0.05, (sum(d for _,_,d,_ in bg),total)
json.dump(dict(total=total,end=endT,beats=beats,segs=[],bg=bg,endl=endl,lang=lang),open(f'tl_{key}.json','w'),ensure_ascii=False)
json.dump(dict(tl=tlm),open(f'tl_m_{key}.json','w'))
print(key,'total',total,'end',endT,'ui',ui['a'],ui['b'])
