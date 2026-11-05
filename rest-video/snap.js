const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const lang=process.argv[2]||'es'; const ts=process.argv.slice(3).map(Number);
await p.goto('file://'+__dirname+'/v.html?lang='+lang);await p.waitForTimeout(800);
await p.addStyleTag({content:'body{background:#556 !important}'});
for(const t of ts){await p.evaluate(t=>seek(t),t);await p.screenshot({path:`${__dirname}/snap_${lang}_${t}.png`});}
await b.close();})();
