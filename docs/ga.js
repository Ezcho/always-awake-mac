/* Shared GA4 loader for every localized page. Measurement IDs are public. */
(async () => {
  'use strict';
  if (location.hostname !== 'no-sleep-pika.online' || location.protocol !== 'https:' ||
      navigator.globalPrivacyControl === true || window.pikaLanguageRedirect) return;
  try {
    const response = await fetch('/analytics.json');
    if (!response.ok) return;
    const { measurementId } = await response.json();
    if (!/^G-[A-Z0-9]+$/.test(measurementId || '')) return;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', measurementId, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      page_location: location.origin + location.pathname
    });
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + measurementId;
    document.head.appendChild(script);
    document.addEventListener('click', event => {
      const anchor = event.target.closest?.('a[href]');
      if (!anchor) return;
      const url = new URL(anchor.href, location.origin);
      if (url.hostname !== 'github.com' ||
          !url.pathname.startsWith('/Ezcho/always-awake-mac/releases/download/') ||
          !/\.(pkg|dmg|zip)$/i.test(url.pathname)) return;
      window.gtag('event', 'pika_download_click', {
        file_name: url.pathname.split('/').pop(),
        link_url: url.origin + url.pathname,
        language: document.documentElement.lang,
        transport_type: 'beacon'
      });
    });
  } catch (_) {
    // Analytics failures must never affect downloads or page interactions.
  }
})();
