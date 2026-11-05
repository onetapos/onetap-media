const {chromium}=require('playwright'); const fs=require('fs');
(async()=>{const key=process.argv[2]; const [vert,lang]=key.split('_'); const J=JSON.parse(fs.readFileSync(`${__dirname}/tl_${key}.json`));
const dir=`${__dirname}/ov_${key}`; const A=+(process.argv[3]||0), B=process.argv[4]?+process.argv[4]:null; if(!process.argv[3]){fs.rmSync(dir,{recursive:true,force:true}); fs.mkdirSync(dir);}
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+`/v2.html?vert=${vert}&lang=${lang}&tl=`+encodeURIComponent(JSON.stringify(J.tl))+'&segs='+encodeURIComponent(JSON.stringify(J.segs)));await p.waitForTimeout(800);
const n=Math.ceil(J.tl.total*30);
for(let i=A;i<(B??n);i++){ await p.evaluate(t=>seek(t),i/30); await p.screenshot({path:`${dir}/${String(i).padStart(4,'0')}.png`,omitBackground:true}); }
await b.close(); console.log('frames',n);})();
