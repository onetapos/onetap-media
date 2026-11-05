const {chromium}=require('playwright'); const fs=require('fs');
(async()=>{const key=process.argv[2]; const J=fs.readFileSync(`${__dirname}/tl_${key}.json`,'utf8'); const T=JSON.parse(J);
const dir=`${__dirname}/ov_${key}`; const ts=process.argv.slice(3).map(Number);
if(!ts.length){ fs.rmSync(dir,{recursive:true,force:true}); fs.mkdirSync(dir); }
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/v4.html?d='+encodeURIComponent(encodeURIComponent(J)));await p.waitForTimeout(700);
if(ts.length){ await p.addStyleTag({content:'body{background:#556 !important}'}); for(const t of ts){ await p.evaluate(t=>seek(t),t); await p.screenshot({path:`${__dirname}/sn_${key}_${t}.png`}); } await b.close(); return; }
const n=Math.ceil(T.total*30);
for(let i=0;i<n;i++){ await p.evaluate(t=>seek(t),i/30); await p.screenshot({path:`${dir}/${String(i).padStart(4,'0')}.png`,omitBackground:true}); }
await b.close(); console.log('frames',n);})();
