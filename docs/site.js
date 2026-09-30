/* Language stays local to this browser. No geo-IP lookup or translation service. */
(() => {
  'use strict';
  const locales = ['en', 'ko', 'zh-CN', 'zh-TW', 'ja', 'hi', 'id', 'es', 'fr', 'de', 'pt-BR', 'ru', 'ar', 'vi', 'th'];
  const key = 'pika-language';
  const current = document.documentElement.lang;
  const pathFor = locale => locale === 'en' ? '/' : `/${locale}/`;
  function readChoice() { try { return localStorage.getItem(key); } catch (_) { return null; } }
  function saveChoice(locale) { try { localStorage.setItem(key, locale); } catch (_) { /* Private browsing can deny storage. */ } }
  function resolveLocale(tag) {
    const normalized = String(tag || '').toLowerCase().replace(/_/g, '-');
    const exact = locales.find(locale => locale.toLowerCase() === normalized);
    if (exact) return exact;
    if (normalized.startsWith('zh')) return /(?:tw|hk|mo|hant)/.test(normalized) ? 'zh-TW' : 'zh-CN';
    if (normalized === 'pt' || normalized.startsWith('pt-')) return 'pt-BR';
    return locales.find(locale => locale === normalized.split('-')[0]) || null;
  }
  // Only the language-neutral entry URL negotiates language. Shared locale URLs
  // always keep their own language, even if this device saved another choice.
  if (location.pathname === '/' || location.pathname === '/index.html') {
    const saved = readChoice();
    const preferred = locales.includes(saved) ? saved : (navigator.languages || [navigator.language]).map(resolveLocale).find(Boolean) || 'en';
    if (preferred !== 'en') {
      window.pikaLanguageRedirect = true;
      location.replace(pathFor(preferred) + location.search + location.hash);
      return;
    }
  }
  const selector = document.getElementById('language');
  if (selector) {
    selector.value = current;
    selector.addEventListener('change', () => {
      const locale = selector.value;
      if (!locales.includes(locale)) return;
      saveChoice(locale);
      location.assign(pathFor(locale) + location.search + location.hash);
    });
  }
  const guide = document.getElementById('mcp-guide');
  document.querySelectorAll('[data-open-mcp]').forEach(button => {
    button.addEventListener('click', () => guide.showModal());
  });
  document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', async () => {
      const target = document.getElementById(button.dataset.copy);
      const status = button.closest('.terminal-body').querySelector('[role="status"]');
      if (!target) return;
      try {
        if (!navigator.clipboard) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(target.textContent.trim());
        const previous = button.innerHTML;
        button.textContent = button.dataset.copied;
        status.textContent = button.dataset.copied;
        window.setTimeout(() => { button.innerHTML = previous; status.textContent = ''; }, 1800);
      } catch (_) {
        const range = document.createRange();
        range.selectNodeContents(target);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        status.textContent = button.dataset.failed;
        button.textContent = button.dataset.failed;
      }
    });
  });
})();
