/* Crisp & Counter — analytics client, INERT BY DEFAULT.
 *
 * The five events the brief asked for are defined below. Nothing is recorded
 * and nothing leaves the browser unless a page sets window.CC_ANALYTICS_ENDPOINT
 * to a self-hosted URL. It is not set anywhere in this build, and an endpoint is
 * not deployed, so this file currently does nothing except define five names.
 *
 * What it would store if enabled: the event name, the page path (never the
 * query string), the product reference for a click, and a date. No cookie, no
 * persistent identifier, no IP address, no user agent, no referrer text.
 *
 * Before enabling: publish a privacy notice, deploy a collector, decide a
 * retention period, and take a view on consent. See review/measurement.html.
 */
(function () {
  "use strict";

  var EVENTS = ["page_view", "outbound_click", "guide_open", "search_query_referral", "report_import"];

  var endpoint = window.CC_ANALYTICS_ENDPOINT || "";
  if (!endpoint) {
    /* Deliberate no-op. Expose the names so they can be inspected, and stop. */
    window.CC_ANALYTICS = { enabled: false, events: EVENTS.slice(), track: function () {} };
    return;
  }

  var buffer = [];

  function send() {
    if (!buffer.length) return;
    var body = JSON.stringify({ events: buffer.splice(0, buffer.length) });
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon(endpoint, new Blob([body], { type: "application/json" }));
      } else {
        fetch(endpoint, { method: "POST", body: body, keepalive: true, headers: { "Content-Type": "application/json" } });
      }
    } catch (e) {
      /* A failed beacon must never break the page. */
    }
  }

  function track(name, detail) {
    if (EVENTS.indexOf(name) === -1) return;
    buffer.push({
      event: name,
      path: location.pathname,
      ref: (detail && detail.ref) || null,
      date: new Date().toISOString().slice(0, 10)
    });
    if (buffer.length >= 5) send();
  }

  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") send();
  });

  track("page_view");

  document.addEventListener("click", function (ev) {
    var a = ev.target.closest("a[rel~='sponsored']");
    if (!a) return;
    var m = (a.getAttribute("href") || "").match(/\/(?:dp\/)?(B0[0-9A-Z]{8})/);
    track("outbound_click", { ref: m ? m[1] : null });
  });

  if (document.referrer) {
    try {
      var host = new URL(document.referrer).hostname;
      if (/(^|\.)(google|bing|duckduckgo|yahoo|yandex|brave|ecosia)\.[a-z.]+$/.test(host)) {
        track("search_query_referral");
      }
    } catch (e) { /* ignore a malformed referrer */ }
  }

  window.CC_ANALYTICS = { enabled: true, events: EVENTS.slice(), track: track };
})();
