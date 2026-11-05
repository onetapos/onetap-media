const P = new URLSearchParams(location.search);
const LANG = P.get('lang') || 'es', VERT = P.get('vert') || 'clin';
const TL = Object.assign({k1:0.2,kitEnd:3.2,p1:3.4,p1e:5.0,p2:5.6,heroEnd:9,nightEnd:12,uiEnd:20,mornEnd:24,total:30}, P.get('tl')?JSON.parse(P.get('tl')):{});
const T = DATA[VERT][LANG];
const segs = P.get('segs') ? JSON.parse(P.get('segs')) : [];
const $ = id => document.getElementById(id);
const words = (el, arr) => { el.innerHTML = arr.map(w => `<span class="w">${w}</span>`).join(' '); return [...el.querySelectorAll('.w')]; };
if (T.hookSize) document.querySelector('#hook').style.setProperty('--hs', T.hookSize);
const hookW = words($('hook'), T.hook); if (T.hookSize) hookW.forEach(w=>w.style.fontSize=T.hookSize+'px');
const big1W = words($('big1'), T.big1); const big2W = words($('big2'), T.big2);
$('tags').innerHTML = T.tags.map((t,i)=>`<div class="tag abs" id="tg${i}" style="left:${t[2]}px;top:${t[3]}px"><span class="dot"></span>${t[0]}<b>${t[1]}</b></div>`).join('');
$('costCard').innerHTML = `<div class="row"><span class="lbl">${T.cost[0]}</span><span>${T.cost[1]}</span></div><div class="row"><span class="lbl">${T.cost[2]}</span><span>${T.cost[3]}</span></div><div class="row m"><span>${T.cost[4]}</span><span class="gold">${T.cost[5]}</span></div><div class="illus" style="margin-top:12px">${T.illus}</div>`;
if (T.costTop) $('costCard').style.top = T.costTop+'px';
$('uiTitle').innerHTML = `<span class="k">${T.uiK}</span>${T.uiT}`;
const bar = `<div class="appbar"><div class="logo"></div><span>OneTap</span></div>`;
T.screens.forEach((s,i)=>{ const e=$('s'+(i+1)); if (s.dark) e.classList.add('dark'); e.innerHTML = bar + `<h4>${s.h}</h4><div class="sub">${s.s}</div>` + s.html; });
const fcPos = [[60,560],[610,390],[40,1160],[620,1420]];
T.fc.forEach((f,i)=>{ const e=$('fc'+(i+1)); e.innerHTML=`<small>${f[0]}</small>${f[1]}`; e.style.left=fcPos[i][0]+'px'; e.style.top=fcPos[i][1]+'px'; });
$('uiIllus').textContent = T.illus;
$('brief').innerHTML = `<div class="hd"><div class="logo"></div><div><b>${T.brief.t}</b><span>${T.brief.s}</span></div></div>` + T.brief.a.map((a,i)=>`<div class="a" id="ba${i}"><i>${i+1}</i><span>${a}</span></div>`).join('') + `<div class="illus">${T.illus}</div>`;
if (T.briefTop) $('brief').style.top=T.briefTop+'px';
$('endCta').innerHTML = `<div class="l1">${T.end.l1}</div><div class="btn">${T.end.btn}</div><div style="margin-top:28px;font-size:34px;color:#9A9B98">${T.end.sub}</div>`;
let ph=''; for (let i=0;i<40;i++){ ph+=`<div class="pt" id="pt${i}"></div>`; } $('pts').innerHTML=ph;
const chunks = [];
segs.forEach(([a,b,txt]) => { const ws = txt.split(' '); const total = ws.reduce((s,w)=>s+w.length+1,0); let t=a; const per=(b-a)/total;
  const wt = ws.map(w => { const s=t; t += (w.length+1)*per; return [w,s,t]; });
  for (let i=0;i<wt.length;i+=4){ const g = wt.slice(i,i+4); if (i+4 < wt.length && wt.length-(i+4) === 1) { g.push(wt[i+4]); i++; } chunks.push(g); } });
const scrItems = [1,2,3,4].map(i=>[...$('s'+i).querySelectorAll('.ai')]);
const counters = [...document.querySelectorAll('[data-to]')];
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)); const lin=(t,a,b)=>clamp((t-a)/(b-a));
const eo=x=>1-Math.pow(1-x,3); const back=x=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);};
function fadeWin(t,a,b,fi=.35,fo=.35){ return Math.min(eo(lin(t,a,a+fi)), 1-lin(t,b-fo,b)); }
function wordsIn(ws,t,a,step,out){ ws.forEach((w,i)=>{ const s=a+i*step; const k=back(lin(t,s,s+.35)); const o=out?1-lin(t,out-.3,out):1; w.style.opacity=clamp(lin(t,s,s+.2))*o; w.style.transform=`translateY(${(1-k)*60}px) scale(${.85+.15*k})`; }); }
window.seek = function(t){
  const ui = t>=TL.nightEnd && t<TL.uiEnd, end = t>=TL.mornEnd;
  $('botShade').style.opacity = (ui||end)?0:1;
  $('hookShade').style.opacity = Math.min(1, fadeWin(t,0,TL.kitEnd,.01,.2) + fadeWin(t,TL.kitEnd,TL.heroEnd,.2,.4) + fadeWin(t,TL.heroEnd,TL.nightEnd,.2,.3)*0.9);
  wordsIn(hookW,t,TL.p1,Math.min(0.2,(TL.p1e-TL.p1)/hookW.length),TL.heroEnd-0.2);
  T.tags.forEach((g,i)=>{ const e=$('tg'+i); const s=TL.p2+0.15+i*0.4; const k=back(lin(t,s,s+.4)); e.style.opacity=clamp(lin(t,s,s+.2))*(1-lin(t,TL.heroEnd-.4,TL.heroEnd)); e.style.transform=`scale(${.6+.4*k}) translateY(${Math.sin((t-s)*1.6)*6}px)`; });
  { const s=TL.p2+1.9; const k=back(lin(t,s,s+.5)); const e=$('costCard'); e.style.opacity=clamp(lin(t,s,s+.25))*(1-lin(t,TL.heroEnd-.4,TL.heroEnd)); e.style.transform=`translateY(${(1-k)*80}px)`; }
  wordsIn(big1W,t,TL.k1,0.12,TL.kitEnd);
  wordsIn(big2W,t,TL.heroEnd+0.2,0.13,TL.nightEnd);
  const u0=TL.nightEnd, ud=TL.uiEnd-TL.nightEnd;
  $('ui').style.opacity = ui ? lin(t,u0,u0+.25) : 0;
  if (ui) { const lt=t-u0;
    $('uiTitle').style.opacity = eo(lin(lt,.1,.5)); $('uiTitle').style.transform=`translateY(${(1-eo(lin(lt,.1,.6)))*40}px)`;
    const ry=-16+10*Math.sin(lt*0.45), rx=6-3*Math.cos(lt*0.5), ent=eo(lin(lt,0,.7));
    $('phone').style.transform = `translateY(${(1-ent)*500+Math.sin(lt*1.1)*10}px) rotateY(${ry}deg) rotateX(${rx}deg) scale(${.96+.04*ent})`;
    const q=ud/4;
    ['s1','s2','s3','s4'].forEach((id,i)=>{ const a=i*q, b=(i+1)*q; const e=$(id); const o = i==3 ? eo(lin(lt,a,a+.3)) : (i==0? 1-lin(lt,b-.15,b+.15) : Math.min(eo(lin(lt,a-.15,a+.15)),1-lin(lt,b-.15,b+.15))); e.style.opacity=o; e.style.clipPath = i==0?'none':`circle(${eo(lin(lt,a-.15,a+.35))*150}% at 80% 10%)`; });
    scrItems.forEach((items,k)=>{ const a=k*q+0.2, step=Math.min(0.28,(q-0.7)/Math.max(1,items.length)); items.forEach((e,j)=>{ const s=a+j*step; e.style.opacity=eo(lin(lt,s,s+.22)); e.style.transform=`translateY(${(1-back(lin(lt,s,s+.4)))*36}px)`; }); });
    counters.forEach(e=>{ const k=+e.closest('.scr').id.slice(1)-1; const s=k*q+0.3; const v=+e.dataset.to*eo(lin(lt,s,s+1.0)); const d=+(e.dataset.dec||0); e.textContent=(e.dataset.pre||'')+v.toFixed(d)+(e.dataset.suf||''); });
    [1,2,3,4].forEach(i=>{ const a=(i-1)*q+.25, b=i*q; const e=$('fc'+i); e.style.opacity=Math.min(eo(lin(lt,a,a+.3)),1-lin(lt,b-.1,b+.15)); e.style.transform=`translateY(${Math.sin(lt*1.4+i)*10}px) scale(${.8+.2*back(lin(lt,a,a+.4))})`; });
    $('uiIllus').style.opacity = 0.9; }
  { const a=TL.uiEnd+0.15, b=TL.mornEnd; const e=$('brief'); e.style.opacity=fadeWin(t,a,b,.3,.25); e.style.transform=`translateY(${(1-back(lin(t,a,a+.45)))*120}px)`;
    [0,1,2].forEach(i=>{ const s=a+.3+i*.3; $('ba'+i).style.opacity=eo(lin(t,s,s+.3)); $('ba'+i).style.transform=`translateX(${(1-eo(lin(t,s,s+.4)))*60}px)`; }); }
  $('end').style.opacity = end ? eo(lin(t,TL.mornEnd,TL.mornEnd+.3)) : 0;
  if (end) { const lt=t-TL.mornEnd;
    $('lgRing').setAttribute('stroke-dashoffset', 352*(1-eo(lin(lt,.15,.9))));
    $('lgDot').style.transform=`scale(${back(lin(lt,.8,1.1))})`; $('lgDot').style.transformOrigin='182px 48px';
    $('endLogo').style.transform=`scale(${.9+.1*eo(lin(lt,0,.6))})`;
    $('endWord').style.opacity=eo(lin(lt,.6,.9)); $('endTag').style.opacity=eo(lin(lt,.8,1.1));
    $('endCta').style.opacity=eo(lin(lt,1.0,1.4)); $('endCta').style.transform=`translateY(${(1-eo(lin(lt,1.0,1.5)))*40}px)`;
    for (let i=0;i<40;i++){ const e=$('pt'+i); const ang=i*2.4, r=60+((i*37)%180), s=.7+(i%7)*.05; const k=lin(lt,s,s+1.4); e.style.opacity=(k>0&&k<1)?(1-k):0; e.style.left=(540+Math.cos(ang)*(r+k*260))+'px'; e.style.top=(725+Math.sin(ang)*(r+k*260))+'px'; } }
  const bigOn = (t<TL.p2-0.1) || (t>=TL.heroEnd && t<TL.nightEnd);
  const sub=$('subs'); const ch = bigOn ? null : chunks.find(g => t>=g[0][1]-0.05 && t<g[g.length-1][2]+0.25);
  if (ch && !end) { sub.style.top = ui ? '1650px' : (t>=TL.kitEnd && t<TL.heroEnd ? '1700px' : '1500px'); sub.innerHTML = ch.map(([w,a,b])=>`<span class="w${t>=a&&t<b+0.05?' on':''}">${w}</span>`).join(''); } else sub.innerHTML='';
};
window.seek(0);
