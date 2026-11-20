/* Good Measure Kitchen — privacy-preserving client-side analytics.
   Five defined events: page_view, outbound_click, guide_open, search_query_referral,
   report_import. No cookies, no personal data, no third-party scripts. Events are
   held in memory and sent as one best-effort beacon batch. The beacon endpoint is
   relative (/analytics/collect) so no third party is contacted; it must be
   self-hosted by the operator (see analytics/endpoint.py) before any data leaves
   the browser. Until enabled, nothing is sent anywhere. */
(function(){
  const ENDPOINT = '/analytics/collect';
  const BATCH_LIMIT = 6;
  const EVENTS = [];
  const SESSION_KEY = 'gmk:session';
  let sessionId = null;
  try {
    sessionId = localStorage.getItem(SESSION_KEY);
    if (!sessionId) {
      sessionId = (globalThis.crypto && crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + '.' + String(Math.random()));
      localStorage.setItem(SESSION_KEY, sessionId);
    }
  } catch (e) { sessionId = String(Date.now()); }

  function enabled() { return !!globalThis.__GMK_ANALYTICS_ENABLED; }

  function track(name, payload) {
    if (!enabled()) return;
    EVENTS.push({
      name: name,
      session: sessionId,
      path: location.pathname,
      referrer: document.referrer || '',
      ts: new Date().toISOString(),
      ...payload
    });
    if (EVENTS.length >= BATCH_LIMIT) flush();
  }

  function flush() {
    if (!enabled() || !EVENTS.length) return;
    const batch = EVENTS.splice(0, EVENTS.length);
    const payload = JSON.stringify({ events: batch });
    if (globalThis.navigator && navigator.sendBeacon) {
      navigator.sendBeacon(ENDPOINT, payload);
    } else {
      fetch(ENDPOINT, {
        method: 'POST',
        body: payload,
        keepalive: true,
        headers: { 'Content-Type': 'application/json' }
      }).catch(function(){});
    }
  }

  /* 1. page_view — fired on every page load */
  track('page_view');

  /* 4. search_query_referral — fired when the reader arrived from a search engine */
  if (/(google|bing|duckduckgo|yahoo|yandex|brave|ecosia)\./i.test(document.referrer || '')) {
    track('search_query_referral');
  }

  /* 3. guide_open — fired when a buyer guide loads */
  if (document.body && document.body.dataset.guide === 'true') {
    track('guide_open');
  }

  /* 2. outbound_click — interception of every sponsored outbound link.
     Records destination separately from the navigation itself. */
  globalThis.addEventListener('click', function(event) {
    const link = event.target.closest('a[rel*="sponsored"]');
    if (!link) return;
    track('outbound_click', { destination: link.href, text: (link.textContent || '').trim() });
    /* Navigation proceeds normally; the beacon is best-effort. */
  }, { capture: true, passive: true });

  /* 5. report_import — reserved. Fired only when campaign ledger records are
     imported from an authorized first-party report. No import UI exists yet;
    call gmkAnalytics.track('report_import', { source, records }) from that flow. */

  globalThis.addEventListener('visibilitychange', function() {
    if (document.hidden) flush();
  });
  globalThis.addEventListener('beforeunload', function() { flush(); });

  globalThis.gmkAnalytics = { track: track, flush: flush, enabled: enabled };
})();