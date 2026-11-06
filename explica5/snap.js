const {chromium}=require('playwright'); const fs=require('fs');
(async()=>{const key=process.argv[2]; const J=fs.readFileSync(`${__dirname}/tl_${key}.json`,'utf8');
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/v5.html?d='+encodeURIComponent(encodeURIComponent(J)));await p.waitForTimeout(700);
await p.addStyleTag({content:'body{background:#7a7468 !important}'});
fs.mkdirSync(`${__dirname}/sn`,{recursive:true});
for(const t of process.argv.slice(3).map(Number)){ await p.evaluate(t=>seek(t),t); await p.screenshot({path:`${__dirname}/sn/${key}_${t}.png`}); }
await b.close();})();
