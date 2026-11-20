/* Crisp & Counter — first-party event client. Inert unless configured.
 *
 * Five events, defined here and nowhere else:
 *   page_view              a page was rendered
 *   guide_open             a guide page was opened (fires with page_view on /guides/*)
 *   outbound_click         a sponsored Amazon link was clicked (records the product ref only)
 *   search_query_referral  the arrival came from a search engine (records the host, never the query)
 *   report_import          a first-party Associates report was imported (called by hand, not automatic)
 *
 * What is never collected: cookies, local storage, fingerprints, IP addresses, user agents, full
 * referrer URLs, query strings, or anything typed by a reader. The buffer lives in memory and is
 * discarded when the tab closes.
 *
 * The client does nothing until a page sets window.CC_ANALYTICS_ENDPOINT to a first-party URL.
 * No endpoint is deployed with this build, so today it only defines the names — see
 * review/measurement.html. Do not point it at a third party: the whole design assumes the
 * collector is on a host the operator controls.
 */
(function () {
  "use strict";

  var EVENTS = [
    "page_view",
    "guide_open",
    "outbound_click",
    "search_query_referral",
    "report_import"
  ];

  var endpoint = window.CC_ANALYTICS_ENDPOINT || "";
  var buffer = [];

  function send() {
    if (!endpoint || !buffer.length) return;
    var body = JSON.stringify({ events: buffer.splice(0, buffer.length) });
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon(endpoint, new Blob([body], { type: "application/json" }));
      } else {
        fetch(endpoint, {
          method: "POST",
          body: body,
          keepalive: true,
          headers: { "Content-Type": "application/json" }
        });
      }
    } catch (e) {
      /* A failed beacon must never break a page. */
    }
  }

  function track(name, detail) {
    if (EVENTS.indexOf(name) === -1) return;
    if (!endpoint) return;                    // inert by default, by design
    buffer.push({
      event: name,
      path: location.pathname,                // no query string, ever
      ref: (detail && detail.ref) || null,    // product reference for a click
      host: (detail && detail.host) || null,  // referring host for a search arrival
      date: new Date().toISOString().slice(0, 10)
    });
    if (buffer.length >= 10) send();
  }

  function productRefFrom(href) {
    var m = /\/dp\/([A-Z0-9]{10})/.exec(href || "");
    return m ? m[1] : null;
  }

  function searchHost() {
    try {
      var r = document.referrer;
      if (!r) return null;
      var h = new URL(r).hostname;
      return /(^|\.)(google|bing|duckduckgo|yahoo|ecosia|startpage)\./.test(h) ? h : null;
    } catch (e) {
      return null;
    }
  }

  document.addEventListener("click", function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest("a[rel~='sponsored']") : null;
    if (!a) return;
    track("outbound_click", { ref: productRefFrom(a.getAttribute("href")) });
    send();
  }, { passive: true });

  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") send();
  });

  window.addEventListener("pagehide", send);

  window.CC_ANALYTICS = {
    enabled: Boolean(endpoint),
    events: EVENTS.slice(),
    track: track,
    /* Called by hand when an authorised report is added to the ledger. */
    reportImport: function (detail) { track("report_import", detail || {}); }
  };

  if (!endpoint) return;

  track("page_view");
  if (location.pathname.indexOf("/guides/") !== -1) track("guide_open");
  var host = searchHost();
  if (host) track("search_query_referral", { host: host });
})();
