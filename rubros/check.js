const {chromium}=require('playwright'); const fs=require('fs');
(async()=>{const key=process.argv[2]; const [vert,lang]=key.split('_'); const J=JSON.parse(fs.readFileSync(`${__dirname}/tl_${key}.json`));
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+`/v2.html?vert=${vert}&lang=${lang}&tl=`+encodeURIComponent(JSON.stringify(J.tl))+'&segs='+encodeURIComponent(JSON.stringify(J.segs)));await p.waitForTimeout(600);
for(const t of process.argv.slice(3).map(Number)){await p.evaluate(t=>seek(t),t);await p.screenshot({path:`${__dirname}/chk_${key}_${t}.png`,omitBackground:true});}
await b.close();})();
