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
  const tick=ms=>{
    const until=now+ms;
    while(true){
      const next=[...timers].filter(([,t])=>t.at<=until).sort((a,b)=>a[1].at-b[1].at)[0];
      if(!next)break;
      now=next[1].at;timers.delete(next[0]);next[1].f();
    }
    now=until;
  };
  const directions=['e','ese','se','sse','s','ssw','sw','wsw','w','wnw','nw','nnw','n','nne','ne','ene'];
  const point=i=>move(290+200*Math.cos(i*Math.PI/8),305+200*Math.sin(i*Math.PI/8));
  assert.equal(images[0].src,undefined);assert.equal(images[1].src,undefined);
  media.matches=false;handlers.media();images[0].onload();images[1].onload();assert(classes.has('motion-ready'));assert(classes.has('motion-lean-ready'));
  directions.forEach((direction,i)=>{tick(90);point(i);assert.equal(host.dataset.gaze,direction);assert(classes.has('motion-looking'));});
  // ENE -> ESE crosses E in two frames, along the short arc across zero degrees.
  tick(90);point(1);assert.equal(host.dataset.gaze,'e');tick(84);assert.equal(host.dataset.gaze,'ese');
  handlers.pointerleave();tick(100);point(0);point(12);point(4);
  assert.equal(timers.size,2);tick(82);assert.equal(host.dataset.gaze,'e');tick(2);assert.equal(host.dataset.gaze,'ese');
  tick(84);assert.equal(host.dataset.gaze,'se');tick(84);assert.equal(host.dataset.gaze,'sse');tick(84);assert.equal(host.dataset.gaze,'s');
  // Stop, soften the last pose, then return to typing. No polling remains.
  assert(classes.has('motion-looking'));tick(14);assert(classes.has('motion-returning'));assert(classes.has('motion-looking'));
  tick(84);assert(!classes.has('motion-looking'));assert(!classes.has('motion-returning'));assert.equal(host.dataset.gaze,'center');assert.equal(timers.size,0);
  point(0);tick(300);point(0);tick(300);assert(classes.has('motion-looking'));assert(!classes.has('motion-returning'));
  tick(50);assert(classes.has('motion-returning'));point(0);assert(!classes.has('motion-returning'));assert(classes.has('motion-looking'));
  // Touch never starts attention. Background/blur cancel every pending callback.
  handlers.pointerleave();tick(100);move(0,305,'touch');assert.equal(timers.size,0);assert(!classes.has('motion-looking'));
  point(0);point(4);doc.hidden=true;handlers.visibilitychange();assert(classes.has('motion-paused'));assert.equal(timers.size,0);assert.equal(host.dataset.gaze,'center');
  doc.hidden=false;handlers.visibilitychange();tick(100);point(0);windowHandlers.blur();assert.equal(timers.size,0);
  media.matches=true;handlers.media();point(4);assert(!classes.has('motion-looking'));assert(classes.has('motion-paused'));
  media.matches=false;handlers.media();fine.matches=false;handlers.fine();point(4);assert.equal(timers.size,0);
  images[1].onerror();assert(!classes.has('motion-lean-ready'));assert(classes.has('motion-ready'));
  images[0].onerror();assert(!classes.has('motion-ready'));
  const css=fs.readFileSync('docs/style.css','utf8');assert(css.includes('.motion-looking .motion-hand{animation:none;opacity:0}'));
  const page=fs.readFileSync('docs/ko/index.html','utf8');
  assert.equal((page.match(/class="gaze-frame /g)||[]).length,16);
  assert.equal((page.match(/<filter id="pika-lean-/g)||[]).length,16);
  assert.equal((page.match(/<filter id="pika-soft-/g)||[]).length,16);
  console.log('PASS motion: 16 directions, intermediate short-arc turns, 12 Hz limit, typing pause, soft idle return, no idle polling, touch/background/reduced motion/asset failure');

})().catch(e=>{console.error(e);process.exit(1)});
