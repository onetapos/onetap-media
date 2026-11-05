const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const [vert,lang,...ts]=process.argv.slice(2);
await p.goto('file://'+__dirname+`/v2.html?vert=${vert}&lang=${lang}`);await p.waitForTimeout(600);
await p.addStyleTag({content:'body{background:#556 !important}'});
for(const t of ts){await p.evaluate(t=>seek(+t),t);await p.screenshot({path:`${__dirname}/sn_${vert}_${lang}_${t}.png`});}
await b.close();})();
