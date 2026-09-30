/* Sixteen registered poses. Intermediate turns run at ≤12 Hz, never idle-poll. */
(() => {
  'use strict';
  const host = document.querySelector('.pika-motion');
  if (!host) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(any-hover: hover) and (any-pointer: fine)');
  const sprite = new Image();
  const leanMap = new Image();
  const directions = ['e', 'ese', 'se', 'sse', 's', 'ssw', 'sw', 'wsw', 'w', 'wnw', 'nw', 'nnw', 'n', 'nne', 'ne', 'ene'];
  const interval = 1000 / 12, idleDelay = 350, angleStep = Math.PI / 8;
  let loaded = false, pending = null, timer = null, idleTimer = null, returnTimer = null;
  let lastPaint = -Infinity, current = -1, target = -1;
  const active = () => loaded && !reduced.matches && finePointer.matches && !document.hidden;
  const clearFrames = () => {
    if (timer !== null) clearTimeout(timer);
    timer = null;
    pending = null;
  };
  const reset = () => {
    clearFrames();
    if (idleTimer !== null) clearTimeout(idleTimer);
    if (returnTimer !== null) clearTimeout(returnTimer);
    idleTimer = returnTimer = null;
    current = target = -1;
    host.dataset.gaze = 'center';
    host.classList.toggle('motion-looking', false);
    host.classList.toggle('motion-returning', false);
  };
  const returnToWork = () => {
    idleTimer = null;
    clearFrames();
    if (current === -1 || !active()) return reset();
    // A half-strength pose bridges the last look and the neutral working pose.
    host.classList.toggle('motion-returning', true);
    returnTimer = setTimeout(reset, interval);
  };
  const paint = () => {
    timer = null;
    if (!active()) return reset();
    lastPaint = performance.now();
    if (pending) {
      const box = host.querySelector('.motion-art').getBoundingClientRect();
      if (!box.width || !box.height) return reset();
      const scale = Math.min(box.width / 620, box.height / 635);
      const x = box.left + (box.width - 620 * scale) / 2 + 290 * scale;
      const y = box.top + (box.height - 635 * scale) / 2 + 305 * scale;
      const dx = pending.x - x, dy = pending.y - y;
      let sector = -1;
      if (Math.hypot(dx, dy) > Math.max(18, 32 * scale)) {
        const angle = Math.atan2(dy, dx);
        sector = (Math.round(angle / angleStep) + 16) % 16;
        if (target !== -1) {
          const delta = Math.atan2(Math.sin(angle - target * angleStep), Math.cos(angle - target * angleStep));
          if (Math.abs(delta) < angleStep / 2 + 0.04) sector = target;
        }
      }
      target = sector;
      pending = null;
    }
    if (current === -1 || target === -1) current = target;
    else {
      // Cross intermediate directions along the shortest arc instead of jumping.
      const delta = (target - current + 24) % 16 - 8;
      current = (current + Math.sign(delta) + 16) % 16;
    }
    const gaze = current === -1 ? 'center' : directions[current];
    if (host.dataset.gaze !== gaze) host.dataset.gaze = gaze;
    if (current !== target) timer = setTimeout(paint, interval);
  };
  const update = () => {
    if (!reduced.matches && !sprite.src) sprite.src = '/assets/pika-motion.png';
    if (!reduced.matches && !leanMap.src) leanMap.src = '/assets/pika-lean-map.svg';
    host.classList.toggle('motion-ready', loaded);
    host.classList.toggle('motion-paused', document.hidden || reduced.matches);
    if (!active()) reset();
  };
  document.addEventListener('pointermove', event => {
    if (event.pointerType !== 'mouse' || !active()) return;
    host.classList.toggle('motion-looking', true);
    host.classList.toggle('motion-returning', false);
    if (returnTimer !== null) clearTimeout(returnTimer);
    returnTimer = null;
    if (idleTimer !== null) clearTimeout(idleTimer);
    idleTimer = setTimeout(returnToWork, idleDelay);
    pending = {x: event.clientX, y: event.clientY};
    if (timer !== null) return;
    const wait = interval - (performance.now() - lastPaint);
    if (wait <= 0) paint();
    else timer = setTimeout(paint, wait);
  }, {passive: true});
  document.documentElement.addEventListener('pointerleave', reset);
  window.addEventListener('blur', reset);
  window.addEventListener('resize', reset, {passive: true});
  window.addEventListener('scroll', reset, {passive: true});
  sprite.onload = () => { loaded = true; update(); };
  sprite.onerror = () => { loaded = false; update(); };
  leanMap.onload = () => host.classList.toggle('motion-lean-ready', true);
  leanMap.onerror = () => host.classList.toggle('motion-lean-ready', false);
  reduced.addEventListener('change', update);
  finePointer.addEventListener('change', update);
  document.addEventListener('visibilitychange', update);
  update();
})();
