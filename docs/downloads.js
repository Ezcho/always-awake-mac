/* Public release-asset totals, not visits or unique people. No tracking cookies. */
(() => {
  'use strict';
  const node = document.getElementById('download-count');
  if (!node) return;
  const api = 'https://api.github.com/repos/Ezcho/always-awake-mac';
  const cacheKey = 'pika-downloads-v1';
  const valid = value => value && Number.isSafeInteger(value.total) && value.total >= 0 &&
    Number.isFinite(Date.parse(value.updatedAt));
  const render = value => {
    if (!valid(value)) return;
    node.textContent = `${new Intl.NumberFormat(document.documentElement.lang).format(value.total)} ${node.dataset.label}`;
    node.dataset.updatedAt = value.updatedAt;
    node.title = `GitHub · ${new Intl.DateTimeFormat(document.documentElement.lang, { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value.updatedAt))}`;
  };
  let cached;
  try { cached = JSON.parse(localStorage.getItem(cacheKey)); } catch (_) { /* Optional cache. */ }
  if (valid(cached)) render(cached);
  if (valid(cached) && Date.now() - Date.parse(cached.updatedAt) >= 0 &&
      Date.now() - Date.parse(cached.updatedAt) < 3600000) return;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);
  async function pages(endpoint) {
    const all = [];
    for (let page = 1; page <= 100; page++) {
      const response = await fetch(`${api}/${endpoint}?per_page=100&page=${page}`, {
        signal: controller.signal, headers: { Accept: 'application/vnd.github+json' }, credentials: 'omit'
      });
      if (!response.ok) throw new Error('GitHub unavailable');
      const batch = await response.json();
      if (!Array.isArray(batch)) throw new Error('Invalid response');
      all.push(...batch);
      if (batch.length < 100) return all;
    }
    throw new Error('Incomplete total');
  }
  (async () => {
    try {
      const releases = await pages('releases');
      const assets = new Map();
      for (const release of releases) {
        if (release.draft) continue;
        if (!Number.isSafeInteger(release.id)) throw new Error('Invalid release');
        for (const asset of await pages(`releases/${release.id}/assets`)) {
          if (!/\.(dmg|zip|pkg)$/i.test(asset.name) || /uninstall/i.test(asset.name)) continue;
          if (!Number.isSafeInteger(asset.download_count) || asset.download_count < 0) throw new Error('Invalid count');
          assets.set(asset.id, asset.download_count);
        }
      }
      const total = [...assets.values()].reduce((sum, count) => sum + count, 0);
      const value = { total, updatedAt: new Date().toISOString() };
      if (!valid(value)) throw new Error('Invalid total');
      render(value);
      try { localStorage.setItem(cacheKey, JSON.stringify(value)); } catch (_) { /* Optional cache. */ }
    } catch (_) {
      // Keep the server-rendered snapshot (or cached total), never invent zero.
    } finally { clearTimeout(timeout); }
  })();
})();
