import json, sys
# Original-audio versions: visuals are timed to Luz's original soundtrack.
R="/mnt/user-data/uploads/Downloads/OneTap anuncios/higgs/robot/"
r1=R+"hf_20261031_175609_91e84310-9083-449e-a1b5-d1e1b7f23c36.mp4"; r2=R+"hf_20261031_175617_2cba802e-4cf0-48c2-ab19-81b4e1938252.mp4"
r3=R+"hf_20261031_182527_fb2a69bd-bffd-43dc-bb4d-ff41f1d2c9c7.mp4"; r4=R+"hf_20261031_182534_8f77422b-1571-46c9-8fc2-9d7ed48ee138.mp4"
r5=R+"hf_20261031_182540_370214df-8ea5-4601-937c-2d1b3f1cb765.mp4"; r6=R+"hf_20261031_182547_3201952a-5fb4-4776-8747-c5aa3581d93c.mp4"
G=lambda s: f'<span class="gold">{s}</span>'
key=sys.argv[1]
def big(a,b,w,at=None,**kw):
    d=dict(type='big',a=a,b=b,w=w)
    if at: d['at']=at
    d.update(kw); return d
H=lambda a,b: f'{a}<br><span class="g2">{b}</span>'
if key=='obusy_en':
    total=44.0; endT=35.9
    beats=[big(0.15,2.0,['Busy','<span class="neq">≠</span>',G('profitable.')],at=[0.15,0.55,0.95],cls='huge',top=330),
           big(2.0,2.85,['Is','it','working','for',G('you?')],step=0.1),
           big(2.95,4.95,['Here\'s','what','makes',G('OneTap'),G('different.')],step=0.13),
           dict(type='flash',a=2.95),
           dict(type='ui',a=4.95,b=33.6,nonum=True,steps=[
             dict(t=5.0,scr='import',h=H('Easy setup.','Start with one file.')),
             dict(t=7.0,scr='hours',h=H('Documents ready?','Get started in hours.')),
             dict(t=10.0,scr='support',h=H('Set it up yourself.','Support when you need it.')),
             dict(t=14.5,scr='connected',h=H('Your business.','Connected.')),
             dict(t=21.7,scr='invoice',h=H('Feed it your invoices.','Let the data flow.')),
             dict(t=25.7,scr='margin',h=H('Spot waste.','Protect your margins.')),
             dict(t=29.6,scr='brief',h=H('Know what needs attention.','Your AI morning briefing.'))]),
           big(33.7,endT,['Less',G('admin.'),'More',G('business.')],at=[33.75,33.95,34.6,34.8])]
    bg=[(r1,0.0,2.95,1.0),(r5,5.4,2.0,1.0),(None,0,28.65,1),(r2,11.0,2.3,1.0)]
    endl='Save time.<br>Reduce costs.'
elif key=='obatt_en':
    total=81.933; endT=71.3
    beats=[big(0.1,3.95,['Big',G('dream.'),'Full',G('battery.')],at=[0.2,0.45,1.9,2.15]),
           big(4.05,10.45,['Then','comes','the',G('paperwork.')],step=0.15),
           big(10.55,19.95,['Sell.','Count.','Check.',G('Repeat.')],at=[10.6,12.4,14.2,16.0]),
           big(20.05,25.45,['Missed',G('sales.'),'Costly',G('mistakes.')],at=[20.1,20.35,21.9,22.15]),
           big(25.55,30.45,['Running','on',G('empty.')],step=0.18),
           big(30.55,33.65,['Meet',G('OneTap.')],step=0.2),
           dict(type='flash',a=31.6),
           big(33.75,37.65,['Your','AI-powered',G('business'),G('system.')],step=0.15),
           big(37.75,39.5,['Here\'s','what','makes','it',G('different.')],step=0.12),
           dict(type='ui',a=39.55,b=56.75,nonum=True,steps=[
             dict(t=39.6,scr='import',h=H('One file.','Your business, connected.')),
             dict(t=43.6,scr='invoice',h=H('Feed OneTap.','Your documents do the work.')),
             dict(t=49.6,scr='brief',h=H('Know your next move.','Your morning briefing.')),
             dict(t=52.6,scr='chat',h=H('AI that helps you act.','You stay in control.'))]),
           big(56.85,62.45,['More','time','for','your',G('customers.')],step=0.14),
           big(62.55,67.45,['Know','your',G('costs.'),'Understand','your',G('margins.')],at=[62.6,62.75,62.9,64.3,64.45,64.6]),
           big(67.55,endT,['And','finally...','enjoy','that',G('coffee.')],at=[67.6,67.8,69.0,69.2,69.4])]
    beats.append(dict(type='batt',win=[[0.0,39.55],[56.75,endT]],charge=[30.7,33.0],
        k=[[0.0,100],[4.0,100],[10.4,84],[10.6,80],[19.9,36],[20.1,32],[25.4,14],[25.6,11],[28.5,2],[30.7,2],[33.0,100]]))
    bg=[(r3,0.2,4.0,1.0),(r3,4.2,6.5,1.0),(r1,0.5,9.5,1.0),(r4,0.5,5.5,1.0),(r4,8.5,5.0,1.0),(r5,4.4,3.2,1.0),(r2,3.0,4.0,1.0),(r5,7.7,1.85,1.0),
        (None,0,17.2,1),(r6,0.0,5.75,1.0),(r2,9.6,5.0,1.0),(r6,7.0,3.8,1.0)]
    endl='Save time. Save money.<br><span style="font-size:40px;font-weight:600;color:#cfcfcb">Put your energy back into your business.</span>'
else: raise SystemExit('unknown key')
s=0.0
for x in bg: s+=x[2]
assert abs(s-endT)<0.06,(s,endT)
bg.append((None,0,round(total-endT,3),1))
json.dump(dict(total=total,end=endT,beats=beats,segs=[],bg=bg,endl=endl,lang='en'),open(f'tl_{key}.json','w'),ensure_ascii=False)
print(key,'ok',total)
