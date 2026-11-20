/* First-party event schema. Set window.SITE_ANALYTICS_ENDPOINT only after the self-hosted endpoint is deployed. */
(() => {
  const products = [
    {label: 'Submission 01', url: 'https://link.amazon/B04G1MEwY'},
    {label: 'Submission 02', url: 'https://link.amazon/B02NbDxp3'},
    {label: 'Submission 03', url: 'https://link.amazon/B00hJ57DV'},
    {label: 'Submission 04', url: 'https://link.amazon/B0c8moW59'},
    {label: 'Submission 05', url: 'https://link.amazon/B0f3GKalj'}
  ];
  const icon = '<svg viewBox="0 0 64 64" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M13 37h38l-3.5 13h-31zM17 37V24h30v13M22 24c0-6 4-10 10-10s10 4 10 10M20 50v4m24-4v4M24 29h16"/><path d="M9 27c2 1 4 1 6 0m34 0c2 1 4 1 6 0"/></svg>';
  const grid = document.getElementById('product-grid');
  if (grid) grid.innerHTML = products.map((p, i) => `<article class="product-card"><div class="product-art">${icon}</div><h3>${p.label}</h3><p>Listing identity and submitted-link destination are not yet confirmed.</p><a class="product-link" href="${p.url}" target="_blank" rel="sponsored nofollow noopener" data-event="outbound_product_click" data-item="submission-${i + 1}">Open supplied link · affiliate</a><small>Supplied link · unverified</small></article>`).join('');

  const allowed = new Set(['page_view','guide_open','outbound_product_click','comparison_tool_use','suggestion_choice']);
  function record(name, details = {}) {
    if (!allowed.has(name) || !window.SITE_ANALYTICS_ENDPOINT) return;
    const payload = JSON.stringify({event:name, path:location.pathname, item: details.item || undefined});
    try { navigator.sendBeacon(window.SITE_ANALYTICS_ENDPOINT, new Blob([payload], {type:'text/plain;charset=UTF-8'})); } catch (_) { /* analytics never blocks reading or outbound navigation */ }
  }
  record(document.body.dataset.page === 'guide' ? 'guide_open' : 'page_view');
  document.addEventListener('click', event => {
    const target = event.target.closest('[data-event]');
    if (target) record(target.dataset.event, {item:target.dataset.item});
  }, true);
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
  const form = document.querySelector('[data-decision-form]');
  if (form) form.addEventListener('submit', event => {
    event.preventDefault();
    const result = document.querySelector('[data-decision-result]');
    const vals = [...form.querySelectorAll('select')].map(s => s.value).filter(Boolean);
    result.innerHTML = `<strong>Your compare-first list</strong><p>${vals.length ? vals.map(v => `<span class="tag">${v}</span>`).join(' ') : 'Choose one or more priorities above to create your checklist.'}</p><p>Use each priority to compare the same details across candidate listings. Confirm dimensions and care instructions in the manufacturer’s documentation and the live Amazon listing before deciding.</p>`;
    result.style.display = 'block';
  });
})();
