/* Real aggregate counts only. No local incrementing, invented baseline, or API secrets. */
(async () => {
  'use strict';
  if (location.hostname !== 'no-sleep-pika.online' || location.protocol !== 'https:') return;
  const node = document.getElementById('visitor-count');
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch('/analytics.json', { signal: controller.signal });
    if (!response.ok) return;
    const { goatcounter } = await response.json();
    if (typeof goatcounter !== 'string' || !/^[a-z0-9][a-z0-9-]{1,60}\.goatcounter\.com$/.test(goatcounter)) return;
    const base = `https://${goatcounter}`;
    // Count public page paths only. No query strings, referrers, or browser fingerprint is sent by this code.
    // Use the documented tracking pixel; no remote JavaScript executes on this page.
    if (!navigator.webdriver && !document.prerendering && navigator.globalPrivacyControl !== true) {
      const pixel = new Image(1, 1);
      pixel.referrerPolicy = 'no-referrer';
      pixel.src = `${base}/count?p=${encodeURIComponent(location.pathname)}&t=no-sleep-pika&r=&rnd=${Date.now()}`;
    }
    if (!node) return;
    const countResponse = await fetch(`${base}/counter/TOTAL.json`, {
      signal: controller.signal, credentials: 'omit', referrerPolicy: 'no-referrer'
    });
    if (!countResponse.ok) return;
    const result = await countResponse.json();
    const raw = String(result.count ?? '');
    if (!/^[0-9][0-9,.\s\u00a0\u202f]*$/.test(raw)) return;
    const total = Number(raw.replace(/[,\s\u00a0\u202f]/g, ''));
    if (!Number.isSafeInteger(total) || total < 0) return;
    node.textContent = new Intl.NumberFormat(document.documentElement.lang).format(total);
    const holder = node.closest('.visitor-counter');
    holder.dataset.connected = 'true';
    holder.title = node.dataset?.label || 'Total visits';
  } catch (_) {
    // Unconfigured/blocked/offline shows an em dash, never a fabricated zero.
  } finally { clearTimeout(timeout); }
})();
