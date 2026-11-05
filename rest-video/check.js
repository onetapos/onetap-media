const {chromium}=require('playwright'); const fs=require('fs');
(async()=>{const lang=process.argv[2]; const J=JSON.parse(fs.readFileSync(`${__dirname}/tl_${lang}.json`));
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/v.html?lang='+lang+'&tl='+encodeURIComponent(JSON.stringify(J.tl))+'&segs='+encodeURIComponent(JSON.stringify(J.segs)));await p.waitForTimeout(600);
for(const t of process.argv.slice(3).map(Number)){await p.evaluate(t=>seek(t),t);await p.screenshot({path:`${__dirname}/chk_${t}.png`,omitBackground:true});}
await b.close();})();
