/* Affil1 analytics client — v2. Records the five canonical events defined in
 * src/data/events.json. Inert by default: nothing is recorded and nothing is
 * sent until a page sets window.CC_ANALYTICS_ENDPOINT to a self-hosted URL.
 *
 * Privacy rules (src/data/events.json "principles"):
 *  - first-party only; the endpoint is same-origin or self-hosted
 *  - no cookie, no local storage, no IP address, no user agent, no query string
 *  - no destination data is collected after the click
 *  - aggregate only: the POST carries the event id and its props; the endpoint
 *    keeps counts per day per event per prop value; raw events are discarded
 *  - Do Not Track and Global Privacy Control headers are honoured by skipping
 *    the send
 */
(function () {
  'use strict';

  var EVENTS = ['page_view', 'outbound_product_click', 'guide_read_75', 'compare_view', 'flag_page_view'];
  var endpoint = window.CC_ANALYTICS_ENDPOINT || '';

  function dntOn() {
    return navigator.doNotTrack === '1' ||
      (typeof navigator.globalPrivacyControl === 'boolean' && navigator.globalPrivacyControl);
  }

  if (!endpoint || dntOn()) {
    window.CC_ANALYTICS = { enabled: false, events: EVENTS.slice(), track: function () {} };
    return;
  }

  var ASIN_RE = /\/(?:dp|gp\/product)\/([A-Z0-9]{10})/i;
  var buffer = [];

  function flush() {
    if (!buffer.length) return;
    var body = JSON.stringify({ day: new Date().toISOString().slice(0, 10), events: buffer.splice(0, buffer.length) });
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon(endpoint, new Blob([body], { type: 'application/json' }));
      } else {
        fetch(endpoint, { method: 'POST', body: body, keepalive: true, headers: { 'Content-Type': 'application/json' } });
      }
    } catch (e) { /* a failed send must never break the page */ }
  }

  function track(name, props) {
    if (EVENTS.indexOf(name) === -1) return;
    var rec = { event: name };
    var k;
    for (k in props || {}) {
      if (Object.prototype.hasOwnProperty.call(props, k)) rec[k] = props[k];
    }
    buffer.push(rec);
    if (buffer.length >= 10) flush();
  }

  function referrerHost() {
    try { return document.referrer ? new URL(document.referrer).hostname : null; }
    catch (e) { return null; }
  }

  function referrerPath() {
    try { return document.referrer ? new URL(document.referrer).pathname : null; }
    catch (e) { return null; }
  }

  function viewportClass() {
    var w = window.innerWidth || document.documentElement.clientWidth;
    return w >= 1280 ? 'wide' : (w >= 768 ? 'medium' : 'narrow');
  }

  function guideSlug() {
    var seg = location.pathname.replace(/\/+$/, '').split('/').pop() || '';
    return seg.replace(/\.html$/, '') || null;
  }

  function tableId() {
    var t = document.querySelector('table');
    return t && t.id ? t.id : null;
  }

  // E1 — a guide, category or register page is rendered
  track('page_view', { path: location.pathname, referrer_host: referrerHost(), viewport_class: viewportClass() });

  // E2 — a reader activates an outbound link to a product listing; counted
  // locally before navigation, so it does not prove a purchase or commission
  var links = document.querySelectorAll("a[rel~='sponsored'], a[href*='amazon.com/dp'], a[href*='link.amazon']");
  for (var i = 0; i < links.length; i++) {
    (function (a, pos) {
      a.addEventListener('click', function () {
        var m = ASIN_RE.exec(a.getAttribute('href') || '');
        track('outbound_product_click', {
          product_id: a.getAttribute('data-product-id') || null,
          asin: m ? m[1] : null,
          page_path: location.pathname,
          position_in_page: pos
        });
      });
    })(links[i], i);
  }

  // E3 — a reader reaches 75% of a guide
  if (/\/guides\//.test(location.pathname) || document.querySelector('[data-guide]')) {
    var seen75 = false;
    function onScroll() {
      if (seen75) return;
      var h = document.documentElement.scrollHeight || document.body.scrollHeight || 0;
      if (h > 0 && window.scrollY + window.innerHeight >= 0.75 * h) {
        seen75 = true;
        track('guide_read_75', { guide_slug: guideSlug() });
      }
    }
    window.addEventListener('scroll', onScroll);
    window.addEventListener('load', onScroll);
  }

  // E4 — the comparison page or a comparison table is rendered
  if (/\/compare\b/.test(location.pathname) || document.querySelector('table.compare, table[data-compare]')) {
    track('compare_view', { table_id: tableId() });
  }

  // E5 — the Flagged for Review page is opened
  if (/\/review\//.test(location.pathname)) {
    track('flag_page_view', { referrer_path: referrerPath() });
  }

  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') flush();
  });
  window.addEventListener('pagehide', flush);
  setInterval(flush, 5000);

  window.CC_ANALYTICS = { enabled: true, events: EVENTS.slice(), track: track };
})();
