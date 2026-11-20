(function () {
  var list = document.getElementById('product-intent-table');
  if (!list || !window.PRODUCTS) return;

  window.PRODUCTS.forEach(function (p) {
    var row = document.createElement('tr');
    row.className = 'product-row';

    var statusBadge = document.createElement('span');
    statusBadge.className = 'status status-unverified';
    statusBadge.textContent = 'UNVERIFIED';

    var link = document.createElement('a');
    link.href = p.submitted;
    link.target = '_blank';
    link.rel = 'sponsored nofollow noopener';
    link.textContent = 'Check submitted listing';
    link.setAttribute('aria-label', 'Open submitted Amazon link ' + p.id + '; destination is unverified');

    var cells = [
      { text: String(p.id).padStart(2, '0'), className: 'product-number' },
      { html: link, className: 'submitted-link' },
      { text: p.intendedAsin, className: 'intended-asin' },
      { text: p.officialListingUrl || '—', className: 'official-listing' },
      { text: p.confirmationDate || '—', className: 'confirmation-date' },
      { text: p.confirmationSource || '—', className: 'confirmation-source' },
      { text: p.observedRedirectTarget || '—', className: 'observed-redirect' },
      { node: statusBadge, className: 'status-cell' }
    ];

    cells.forEach(function (c) {
      var td = document.createElement('td');
      td.className = c.className;
      if (c.node) td.appendChild(c.node);
      else if (c.html !== undefined) td.appendChild(c.html);
      else td.textContent = c.text;
      row.appendChild(td);
    });

    list.appendChild(row);
  });

  /* Record a guide_open analytics event when a guide page finishes loading. */
  if (window.GoodMeasureAnalytics) {
    var guideEl = document.querySelector('[data-guide]');
    if (guideEl && guideEl.getAttribute('data-guide')) {
      window.GoodMeasureAnalytics.guideOpen(guideEl.getAttribute('data-guide'));
    }
  }
})();
