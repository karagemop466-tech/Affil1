/* Good Measure Kitchen — storefront behavior
   Session arena/ac649871-affil1 (2026-11-20).

   The front page and guides are deliberately static HTML so search engines
   see the full content without rendering JavaScript. This file only:
     1. marks outbound sponsored product links with `product-link` so the
        five-event collector records them as product clicks,
     2. renders the product-intent register table when a page provides a
        container for it (data-driven, never hand-typed),
     3. records a guide_read event on guide pages (body[data-guide]).          */

(function () {
  /* 1. Mark sponsored product links (analytics.js counts rel="sponsored" too;
        the extra class distinguishes product clicks from citation links). */
  try {
    document.querySelectorAll('a[href*="amazon.com/dp"]').forEach(function (a) {
      var rel = (a.getAttribute('rel') || '').split(/\s+/);
      if (rel.indexOf('sponsored') !== -1) a.classList.add('product-link');
    });
  } catch (e) { /* older engines — ignore */ }

  /* 2. Render the product-intent confirmation register, if the page asks for it. */
  var tbody = document.getElementById('intent-table-body');
  if (tbody && window.PRODUCTS) {
    window.PRODUCTS.forEach(function (p) {
      var tr = document.createElement('tr');

      var tdLink = document.createElement('td');
      var a = document.createElement('a');
      a.href = p.submitted;
      a.textContent = p.submitted.replace('https://', '');
      a.target = '_blank';
      a.rel = 'nofollow noopener';
      tdLink.appendChild(a);

      var tdSlug = document.createElement('td');
      tdSlug.textContent = p.submitted.split('/').pop() + ' (9 chars — token, not an ASIN)';

      var tdOfficial = document.createElement('td');
      if (p.officialListingUrl) {
        var oa = document.createElement('a');
        oa.href = p.officialListingUrl;
        oa.textContent = p.officialListingUrl;
        oa.target = '_blank';
        oa.rel = 'nofollow noopener';
        tdOfficial.appendChild(oa);
      } else {
        tdOfficial.textContent = '— blank (unverified)';
      }

      var tdObserved = document.createElement('td');
      tdObserved.textContent = p.observedRedirect || '— blank';

      var tdDate = document.createElement('td');
      tdDate.textContent = p.confirmedDate || '— blank';

      var tdStatus = document.createElement('td');
      var chip = document.createElement('span');
      chip.className = 'status-tag ' + (p.status === 'verified' ? 'status-verified' : 'status-pending');
      chip.textContent = p.status === 'verified' ? 'Verified' : 'Pending';
      tdStatus.appendChild(chip);

      tr.append(tdLink, tdSlug, tdOfficial, tdObserved, tdDate, tdStatus);
      tbody.appendChild(tr);
    });
  }

  /* 3. Guide-read event for pages that declare data-guide. */
  if (document.body && document.body.dataset && document.body.dataset.guide) {
    if (typeof affil1GuideRead === 'function') {
      affil1GuideRead(document.body.dataset.guide);
    }
  }
})();
