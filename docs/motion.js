/* Eight registered gaze poses; at most eight updates/second, no idle polling. */
(() => {
  'use strict';
  const host = document.querySelector('.pika-motion');
  if (!host) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(any-hover: hover) and (any-pointer: fine)');
  const sprite = new Image();
  const directions = ['e', 'se', 's', 'sw', 'w', 'nw', 'n', 'ne'];
  const interval = 125;
  let loaded = false, pending = null, timer = null, lastPaint = -Infinity;
  const active = () => loaded && !reduced.matches && finePointer.matches && !document.hidden;
  const reset = () => {
    if (timer !== null) clearTimeout(timer);
    timer = null;
    pending = null;
    host.dataset.gaze = 'center';
  };
  const paint = () => {
    timer = null;
    if (!active() || !pending) return;
    lastPaint = performance.now();
    const box = host.querySelector('.motion-art').getBoundingClientRect();
    if (!box.width || !box.height) return reset();
    // SVG is 620×635, centered inside a square canvas. Aim from between the eyes.
    const scale = Math.min(box.width / 620, box.height / 635);
    const x = box.left + (box.width - 620 * scale) / 2 + 290 * scale;
    const y = box.top + (box.height - 635 * scale) / 2 + 305 * scale;
    const dx = pending.x - x, dy = pending.y - y;
    const radius = Math.max(18, 32 * scale);
    let gaze = 'center';
    if (Math.hypot(dx, dy) > radius) {
      const angle = Math.atan2(dy, dx);
      let sector = (Math.round(angle / (Math.PI / 4)) + 8) % 8;
      // A small deadband prevents flicker while hovering at sector boundaries.
      const previous = directions.indexOf(host.dataset.gaze);
      if (previous !== -1) {
        const delta = Math.atan2(Math.sin(angle - previous * Math.PI / 4), Math.cos(angle - previous * Math.PI / 4));
        if (Math.abs(delta) < Math.PI / 8 + 0.08) sector = previous;
      }
      gaze = directions[sector];
    }
    if (host.dataset.gaze !== gaze) host.dataset.gaze = gaze;
    pending = null;
  };
  const update = () => {
    if (!reduced.matches && !sprite.src) sprite.src = '/assets/pika-motion.png';
    host.classList.toggle('motion-ready', loaded);
    host.classList.toggle('motion-paused', document.hidden || reduced.matches);
    if (!active()) reset();
  };
  document.addEventListener('pointermove', event => {
    if (event.pointerType !== 'mouse' || !active()) return;
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
  reduced.addEventListener('change', update);
  finePointer.addEventListener('change', update);
  document.addEventListener('visibilitychange', update);
  update();
})();
