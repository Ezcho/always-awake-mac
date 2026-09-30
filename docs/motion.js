/* One cached sprite sheet, a nine-second CSS timeline, no frame polling. */
(() => {
  'use strict';
  const host = document.querySelector('.pika-motion');
  if (!host) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const sprite = new Image();
  let loaded = false;
  const update = () => {
    if (!reduced.matches && !sprite.src) sprite.src = '/assets/pika-motion.png';
    host.classList.toggle('motion-ready', loaded && !reduced.matches);
    host.classList.toggle('motion-paused', document.hidden);
  };
  sprite.onload = () => { loaded = true; update(); };
  sprite.onerror = () => { loaded = false; host.classList.remove('motion-ready'); };
  reduced.addEventListener('change', update);
  document.addEventListener('visibilitychange', update);
  update();
})();
