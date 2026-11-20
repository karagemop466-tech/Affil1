/* Crisp & Counter — first-party event client. Inert unless configured.
 *
 * Nine event names are defined, because two intervals of this project defined
 * their own and both sets are in use. Five are the core ones this site explains
 * on review/measurement.html:
 *   page_view              a page was rendered
 *   guide_open             a guide page was opened
 *   outbound_click         a sponsored Amazon link was clicked (records the product reference only)
 *   search_query_referral  the arrival came from a search engine (records the host, never the query)
 *   report_import          an authorised Associates report was entered by hand, never sent by a page
 * Four more are surface-specific signals used by the comparison and review pages:
 *   outbound_product_click, guide_read_75, compare_view, flag_page_view
 *
 * What is never collected: cookies, browser storage, fingerprints, IP addresses,
 * user agents, full referrer URLs, query strings, or anything typed by a reader.
 * The buffer lives in memory and is discarded when the tab closes. The collector
 * is same-origin and accepts exactly one event per request, of three fields.
 *
 * The client does nothing until a page sets window.CC_ANALYTICS_ENABLED (which
 * selects the same-origin collector) or window.CC_ANALYTICS_ENDPOINT. No
 * collector is deployed with this build, so today it only defines names.
 */
(function () {
  "use strict";

  var COLLECTOR_PATH = "/api/e";           // same-origin only, never a third party
  var EVENTS = [
    "page_view",
    "guide_open",
    "outbound_click",
    "search_query_referral",
    "report_import",
    "outbound_product_click",
    "guide_read_75",
    "compare_view",
    "flag_page_view"
  ];
  var BROWSER_ONLY = "report_import";      // an operator event: tracked, never posted

  var endpoint = window.CC_ANALYTICS_ENDPOINT ||
                 (window.CC_ANALYTICS_ENABLED ? COLLECTOR_PATH : "");
  var buffer = [];

  function send() {
    if (!endpoint || !buffer.length) return;
    var item = buffer.shift();
    var body = JSON.stringify([item]);     // the collector accepts one event per POST
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
    if (buffer.length) send();
  }

  function track(name, detail) {
    if (EVENTS.indexOf(name) === -1) return;
    if (!endpoint || name === BROWSER_ONLY) return;
    buffer.push({
      event: name,
      page: location.pathname + location.search.replace(/\?.*/, ""),  // path only, never a query
      product: (detail && detail.ref) || null
    });
    send();
  }

  function productRefFrom(href) {
    var m = /\/dp\/([A-Z0-9]{10})/.exec(href || "");
    return m ? m[1] : null;
  }

  document.addEventListener("click", function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest("a[rel~='sponsored']") : null;
    if (!a) return;
    track("outbound_click", { ref: productRefFrom(a.getAttribute("href")) });
  }, { passive: true });

  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") send();
  });
  window.addEventListener("pagehide", send);

  window.CC_ANALYTICS = {
    enabled: Boolean(endpoint),
    collector: COLLECTOR_PATH,
    events: EVENTS.slice(),
    track: track,
    reportImport: function () { return null; }  // recorded by the operator, not by a page
  };

  if (!endpoint) return;
  track("page_view");
  if (location.pathname.indexOf("/guides/") !== -1) track("guide_open");
})();
