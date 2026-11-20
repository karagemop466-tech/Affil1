/* Inert until an approved HTTPS collector is configured. No browser storage. */
(function () {
  'use strict';
  // report_import belongs to the authorized reporting ledger, not the browser.
  if (!window.CC_ANALYTICS_ENDPOINT || navigator.globalPrivacyControl ||
      navigator.doNotTrack === '1' || window.doNotTrack === '1') return;
  var endpoint;
  try { endpoint = new URL(window.CC_ANALYTICS_ENDPOINT, location.href); }
  catch (_) { return; }
  if (endpoint.protocol !== 'https:' || endpoint.username || endpoint.password || endpoint.search || endpoint.hash) return;

  function send(events) {
    try {
      fetch(endpoint.href, {
        method: 'POST', body: JSON.stringify(events), keepalive: true,
        credentials: 'omit', referrerPolicy: 'no-referrer', redirect: 'error'
      }).catch(function () {});
    } catch (_) { /* Measurement must not interrupt navigation. */ }
  }

  var pathname = location.pathname;
  var events = ['page_view'];
  if (/\/compare\/(?:index\.html)?$/.test(pathname)) events.push('compare_view');
  if (/\/review\/(?:index\.html)?$/.test(pathname)) events.push('flag_page_view');
  send(events);
  if (/\/guides\/(?!index\.html$)[^/]+\.html$/.test(pathname)) {
    var read = function () {
      var root = document.documentElement;
      if (root.scrollHeight <= innerHeight || scrollY <= 0 || scrollY + innerHeight < root.scrollHeight * 0.75) return;
      removeEventListener('scroll', read);
      send(['guide_read_75']);
    };
    addEventListener('scroll', read, { passive: true });
  }
  function click(event) {
    var link = event.target.closest && event.target.closest('a[rel~="sponsored"]');
    if (link && /^(www\.amazon\.com|link\.amazon)$/.test(link.hostname)) send(['outbound_product_click']);
  }
  document.addEventListener('click', click);
  document.addEventListener('auxclick', function (event) { if (event.button === 1) click(event); });
})();
