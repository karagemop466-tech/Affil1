/* Privacy-preserving outbound-click counter and event tracker.
 *
 * Design rules, applied by this file:
 *   - No cookies. No localStorage. No advertising identifiers. No fingerprinting.
 *   - No cross-site identifiers of any kind.
 *   - The referrer is reduced to a host name before it leaves the browser, and a
 *     search query is only sent when the referring host is a known search engine
 *     and the landing URL itself carried the query.
 *   - Outbound clicks record the destination host only, never the query string,
 *     because a Special Link's query string carries the tracking tag.
 *   - Nothing is sent until the collector answers its health check.
 *
 * Five events are recorded:
 *   page_view, outbound_click, guide_open, search_query_referral, report_import
 */
(function () {
  'use strict';

  var site = window.GM_SITE;
  if (!site || !site.collector) return;

  var cfg = site.collector;
  var settings = site.tracking || {};
  var events = settings.events || [];
  var queue = [];
  var active = false;
  var probeDone = false;

  function hostOf(url) {
    try { return new URL(url, window.location.href).hostname; } catch (e) { return ''; }
  }

  function isSearchEngine(host) {
    var list = settings.searchEngines || [];
    for (var i = 0; i < list.length; i++) {
      if (host.indexOf(list[i]) !== -1) return true;
    }
    return false;
  }

  /* The landing URL may carry the query the visitor actually typed, e.g. ?q=... or
     ?utm_term=... . We only keep it when the visit came from a search engine. */
  function queryFromLanding() {
    try {
      var params = new URLSearchParams(window.location.search);
      var q = params.get('q') || params.get('query') || params.get('utm_term') || params.get('p');
      if (!q) return '';
      return q.slice(0, 120);
    } catch (e) { return ''; }
  }

  function guideId() {
    var m = window.location.pathname.match(/\/guides\/([a-z0-9-]+)\.html$/i);
    return m ? m[1] : '';
  }

  function send(event, extra) {
    if (!active) return;
    if (events.indexOf(event) === -1) return;
    var payload = { event: event, path: window.location.pathname, ts: Date.now() };
    if (extra) {
      for (var k in extra) {
        if (Object.prototype.hasOwnProperty.call(extra, k) && extra[k] !== '' && extra[k] !== undefined) {
          payload[k] = extra[k];
        }
      }
    }
    var body = JSON.stringify(payload);
    var url = cfg.endpoint;
    if (navigator.sendBeacon) {
      try {
        navigator.sendBeacon(url, new Blob([body], { type: 'application/json' }));
        return;
      } catch (e) { /* fall through to fetch */ }
    }
    if (window.fetch) {
      try {
        fetch(url, { method: 'POST', body: body, keepalive: true, headers: { 'Content-Type': 'application/json' } })
          .catch(function () {});
      } catch (e) { /* ignore */ }
    }
  }

  /* Probe once. If the collector is not deployed the tracker stays quiet and says so
     in the document, so nobody can read "we measure this" into a page that does not. */
  function probe() {
    if (probeDone) return;
    probeDone = true;
    var health = cfg.endpoint.replace(/\/$/, '') + cfg.healthPath;
    var done = function (ok) {
      active = ok;
      document.documentElement.setAttribute('data-collector', ok ? 'active' : 'inactive');
      if (ok) { flushQueue(); boot(); }
    };
    if (!window.fetch) { done(false); return; }
    var controller = ('AbortController' in window) ? new AbortController() : null;
    var timer = null;
    var opts = { method: 'GET', cache: 'no-store' };
    if (controller) {
      opts.signal = controller.signal;
      timer = setTimeout(function () { controller.abort(); }, cfg.timeoutMs || 2500);
    }
    fetch(health, opts).then(function (r) {
      if (timer) clearTimeout(timer);
      done(!!r && r.ok);
    }).catch(function () {
      if (timer) clearTimeout(timer);
      done(false);
    });
  }

  function flushQueue() {
    while (queue.length) {
      var item = queue.shift();
      send(item.event, item.extra);
    }
  }

  function boot() {
    send('page_view');

    var g = guideId();
    if (g) send('guide_open', { guide: g });

    var ref = document.referrer;
    if (ref) {
      var refHost = hostOf(ref);
      if (refHost && isSearchEngine(refHost)) {
        send('search_query_referral', { referrer: refHost, q: queryFromLanding() });
      }
    }
  }

  /* Delegated listener: one handler for every sponsored outbound link on the site. */
  document.addEventListener('click', function (ev) {
    var node = ev.target;
    while (node && node.nodeType !== 1) node = node.parentNode;
    if (!node) return;
    var link = node.closest ? node.closest('a[rel~="sponsored"]') : null;
    if (!link) return;
    var target = hostOf(link.getAttribute('href') || '');
    var label = (link.textContent || '').trim().slice(0, 60);
    send('outbound_click', { target: target, label: label });
  }, true);

  /* Public helper so the ledger's import control can record a report_import event. */
  window.GMAnalytics = {
    track: function (event, extra) {
      if (!active) return false;
      send(event, extra);
      return true;
    },
    isActive: function () { return active; }
  };

  /* Queue events that happen before the health probe finishes, then replay them. */
  var originalSend = send;
  send = function (event, extra) {
    if (!probeDone) { queue.push({ event: event, extra: extra }); return; }
    originalSend(event, extra);
  };

  /* The collector is not deployed by default. While `deployed` is false the
     tracker makes no network request at all and stays inert, so a reader never
     waits on a probe that cannot succeed. Setting `deployed` to true switches it
     on: the tracker then probes the health endpoint and stays inert unless the
     collector answers. */
  if (cfg.deployed) {
    probe();
  } else {
    document.documentElement.setAttribute('data-collector', 'inactive');
  }
})();
