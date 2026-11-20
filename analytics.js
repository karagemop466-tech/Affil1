/* Good Measure Kitchen — privacy-preserving analytics.
 *
 * Self-hosted (same-origin) analytics endpoint contract:
 *   POST /api/analytics/collect  { event, ...payload }
 *
 * Notes:
 * - This is a STATIC GitHub Pages site. The /api/analytics/collect route is a
 *   reserved same-origin path; until a backend is wired and authorized, posts
 *   fail and events are queued in localStorage so nothing is lost.
 * - No personal data, no IP addresses, no fingerprinting, no cross-site tracking.
 * - Event set (proposed, not deployed until access/privacy/consent is confirmed):
 *     page_view, outbound_click, guide_open, search_query_referral, report_import
 * - Outbound clicks on sponsored product links are counted here; the conversion
 *   ledger itself stays empty until authorized first-party reports exist.
 */

(function () {
  var ENDPOINT = '/api/analytics/collect';
  var STORAGE_KEY = 'gm_analytics_queue';
  var SESSION_KEY = 'gm_session_id';
  var MAX_QUEUE = 50;

  function sessionId() {
    var sid = localStorage.getItem(SESSION_KEY);
    if (!sid) {
      sid = (Math.random().toString(36) + Date.now().toString(36)).slice(2, 14);
      try { localStorage.setItem(SESSION_KEY, sid); } catch (e) {}
    }
    return sid;
  }

  function queue(event, payload) {
    var item = { t: new Date().toISOString(), s: sessionId(), e: event, p: payload || {} };
    var q = [];
    try { q = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch (e) {}
    if (q.length >= MAX_QUEUE) q.shift();
    q.push(item);
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(q)); } catch (e) {}
    flush();
  }

  function flush() {
    var q = [];
    try { q = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch (e) {}
    if (!q.length) return;
    if (navigator && navigator.sendBeacon) {
      var form = new FormData();
      q.forEach(function (item) { form.append('events[]', JSON.stringify(item)); });
      navigator.sendBeacon(ENDPOINT, form);
      try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
      return;
    }
    var xhr = new XMLHttpRequest();
    xhr.open('POST', ENDPOINT, true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xhr.onload = function () {
      if (xhr.status >= 200 && xhr.status < 300) {
        try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
      }
    };
    xhr.onerror = function () {};
    try { xhr.send(JSON.stringify({ events: q })); } catch (e) {}
  }

  function track(event, payload) {
    queue(event, payload);
  }

  /* Auto page view on load. */
  if (typeof window !== 'undefined') {
    track('page_view', { path: window.location.pathname, referrer: document.referrer || '' });

    /* Outbound-click counter: intercept clicks on sponsored outbound product links. */
    document.addEventListener('click', function (ev) {
      var link = ev.target.closest && ev.target.closest('a[href]');
      if (!link) return;
      var href = link.getAttribute('href') || '';
      var rel = link.getAttribute('rel') || '';
      var isOutbound = href.startsWith('http://') || href.startsWith('https://');
      var isSponsored = rel.indexOf('sponsored') !== -1;
      if (isOutbound && isSponsored) {
        var productId = '';
        var m = href.match(/[Bb][0-9]{2}[A-Z0-9]{7}/);
        if (m) productId = m[0];
        track('outbound_click', {
          url: href,
          product: productId,
          label: link.textContent ? link.textContent.trim().slice(0, 80) : ''
        });
      }
    });

    /* Expose helpers for guides and dashboards to record the remaining events. */
    window.GoodMeasureAnalytics = {
      track: track,
      guideOpen: function (guide) { track('guide_open', { guide: guide }); },
      searchReferral: function (query) { track('search_query_referral', { query: query }); },
      reportImport: function (source) { track('report_import', { source: source }); }
    };
  }
})();
