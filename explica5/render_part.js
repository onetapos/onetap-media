const {chromium}=require('playwright'); const fs=require('fs');
(async()=>{const key=process.argv[2]; const A=+process.argv[3], B=+process.argv[4]; const css=process.argv[5]||'';
const J=fs.readFileSync(`${__dirname}/tl_${key}.json`,'utf8'); const dir=`${__dirname}/ov_${key}`;
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/v5.html?d='+encodeURIComponent(encodeURIComponent(J)));await p.waitForTimeout(700);
if(css) await p.addStyleTag({content:css});
for(let i=A;i<B;i++){ await p.evaluate(t=>seek(t),i/30); await p.screenshot({path:`${dir}/${String(i).padStart(4,'0')}.png`,omitBackground:true}); }
await b.close(); console.log('ok',A,B);})();
