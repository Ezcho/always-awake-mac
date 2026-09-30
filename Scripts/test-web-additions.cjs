const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

async function visitors({host='no-sleep-pika.online', service='pika-test.goatcounter.com', count='1,234', privacy=false, failure=false}={}) {
  const requests=[], pixels=[];
  const holder={dataset:{}};
  const node={textContent:'—',closest:()=>holder};
  const ctx={location:{hostname:host,protocol:'https:',pathname:'/ko/',search:'?private=not-sent'},document:{getElementById:()=>node,documentElement:{lang:'ko'},prerendering:false},navigator:{globalPrivacyControl:privacy},AbortController,Intl,Date,setTimeout,clearTimeout,Image:class{set src(value){pixels.push(value);}},fetch:async url=>{requests.push(url);if(failure)throw Error('offline');return {ok:true,json:async()=>url==='/analytics.json'?{goatcounter:service}:{count}};}};
  await vm.runInNewContext(fs.readFileSync('docs/visitors.js','utf8'),ctx);
  return {node,requests,pixels,holder};
}
(async()=>{
  let r=await visitors();assert.equal(r.node.textContent,'1,234');assert.equal(r.pixels.length,1);assert(!r.pixels[0].includes('private'));assert(r.requests[1].endsWith('/counter/TOTAL.json'));
  r=await visitors({host:'127.0.0.1'});assert.equal(r.requests.length,0);
  r=await visitors({service:null});assert.equal(r.pixels.length,0);assert.equal(r.node.textContent,'—');
  r=await visitors({service:'pika.goatcounter.com.evil.invalid'});assert.equal(r.requests.length,1);assert.equal(r.pixels.length,0);
  r=await visitors({privacy:true});assert.equal(r.pixels.length,0);
  r=await visitors({failure:true});assert.equal(r.node.textContent,'—');
  r=await visitors({count:'<script>bad</script>'});assert.equal(r.node.textContent,'—');
  console.log('PASS visits: real total rendering, no localhost counting, no unconfigured host, privacy signal, errors, injection, query omission');
  const classes=new Set(),handlers={},images=[];
  const media={matches:true,addEventListener:(k,f)=>handlers.media=f};
  const host={classList:{toggle:(k,on)=>on?classes.add(k):classes.delete(k),remove:k=>classes.delete(k)}};
  const doc={hidden:false,querySelector:()=>host,addEventListener:(k,f)=>handlers[k]=f};
  vm.runInNewContext(fs.readFileSync('docs/motion.js','utf8'),{document:doc,matchMedia:()=>media,Image:class{constructor(){images.push(this);}}});
  assert.equal(images[0].src,undefined);assert(!classes.has('motion-ready'));
  media.matches=false;handlers.media();assert.equal(images[0].src,'/assets/pika-motion.png');images[0].onload();assert(classes.has('motion-ready'));
  doc.hidden=true;handlers.visibilitychange();assert(classes.has('motion-paused'));
  media.matches=true;handlers.media();assert(!classes.has('motion-ready'));
  images[0].onerror();assert(!classes.has('motion-ready'));
  assert(fs.readFileSync('docs/style.css','utf8').includes('pika-work 9s steps(1,end) infinite'));
  console.log('PASS motion: nine-second loop, one sprite, Reduced Motion, hidden tab pause, static error fallback');
})().catch(e=>{console.error(e);process.exit(1)});
