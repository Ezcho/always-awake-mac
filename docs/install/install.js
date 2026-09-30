/* Explicit guide language only. All other requested locales use English. */
(() => {
  'use strict';
  const lang = new URLSearchParams(location.search).get('lang');
  if (location.pathname === '/install/' && lang && /^ko(?:-|$)/i.test(lang)) {
    location.replace('/install/ko/' + location.hash);
  }
})();
