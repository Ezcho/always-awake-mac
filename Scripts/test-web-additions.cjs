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
  const classes=new Set(),handlers={},windowHandlers={},images=[],timers=new Map();
  let now=0, nextTimer=0;
  const media={matches:true,addEventListener:(k,f)=>handlers.media=f};
  const fine={matches:true,addEventListener:(k,f)=>handlers.fine=f};
  const host={dataset:{gaze:'center'},querySelector:()=>({getBoundingClientRect:()=>({left:0,top:0,width:620,height:635})}),classList:{toggle:(k,on)=>on?classes.add(k):classes.delete(k)}};
  const doc={hidden:false,querySelector:()=>host,addEventListener:(k,f)=>handlers[k]=f,documentElement:{addEventListener:(k,f)=>handlers[k]=f}};
  vm.runInNewContext(fs.readFileSync('docs/motion.js','utf8'),{
    document:doc,window:{addEventListener:(k,f)=>windowHandlers[k]=f},matchMedia:q=>q.includes('reduced')?media:fine,
    Image:class{constructor(){images.push(this);}},performance:{now:()=>now},
    setTimeout:(f,delay)=>{timers.set(++nextTimer,{f,at:now+delay});return nextTimer;},clearTimeout:id=>timers.delete(id)
  });
  const move=(x,y,type='mouse')=>handlers.pointermove({clientX:x,clientY:y,pointerType:type});
  const tick=ms=>{now+=ms;for(const [id,t] of timers)if(t.at<=now){timers.delete(id);t.f();}};
  assert.equal(images[0].src,undefined);assert(!classes.has('motion-ready'));
  media.matches=false;handlers.media();assert.equal(images[0].src,'/assets/pika-motion.png');images[0].onload();assert(classes.has('motion-ready'));
  const directions=['e','se','s','sw','w','nw','n','ne'];
  directions.forEach((direction,i)=>{tick(125);move(290+200*Math.cos(i*Math.PI/4),305+200*Math.sin(i*Math.PI/4));assert.equal(host.dataset.gaze,direction);});
  tick(125);move(290,305);assert.equal(host.dataset.gaze,'center');
  // Input bursts coalesce to the latest pointer and never create an idle loop.
  tick(125);move(600,305);assert.equal(host.dataset.gaze,'e');move(0,305);move(290,600);
  assert.equal(timers.size,1);tick(124);assert.equal(host.dataset.gaze,'e');tick(1);assert.equal(host.dataset.gaze,'s');assert.equal(timers.size,0);
  tick(125);move(0,305,'touch');assert.equal(host.dataset.gaze,'s');
  handlers.pointerleave();assert.equal(host.dataset.gaze,'center');
  move(0,305);move(600,305);doc.hidden=true;handlers.visibilitychange();assert(classes.has('motion-paused'));assert.equal(timers.size,0);assert.equal(host.dataset.gaze,'center');
  doc.hidden=false;handlers.visibilitychange();tick(125);move(0,305);windowHandlers.blur();assert.equal(host.dataset.gaze,'center');
  media.matches=true;handlers.media();move(600,305);assert.equal(host.dataset.gaze,'center');assert(classes.has('motion-paused'));
  media.matches=false;handlers.media();fine.matches=false;handlers.fine();move(600,305);assert.equal(host.dataset.gaze,'center');
  images[0].onerror();assert(!classes.has('motion-ready'));
  const css=fs.readFileSync('docs/style.css','utf8');assert(css.includes('pika-type 9s steps(1,end) infinite'));assert(!css.includes('background-position'));
  const page=fs.readFileSync('docs/ko/index.html','utf8');
  assert.equal((page.match(/class="gaze-frame /g)||[]).length,8);
  assert(page.includes('class="motion-body" href="#pika-sheet"'));
  assert(!page.includes('motion-sprite'));
  console.log('PASS motion: eight directions, 8 Hz limit, burst coalescing, no idle timer, fixed body, touch/hidden/reduced-motion/reset/error handling');

})().catch(e=>{console.error(e);process.exit(1)});
