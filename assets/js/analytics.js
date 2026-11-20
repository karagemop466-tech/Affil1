/* Crisp & Counter — first-party analytics client.
 *
 * FIVE EVENTS, DEFINED BEFORE ANY CODE SHIPPED
 *   page_view               a page was rendered
 *   outbound_product_click  a reader activated a link to an Amazon listing
 *   guide_read_75           a reader reached 75% of a guide's height
 *   compare_view            the comparison table was rendered
 *   flag_page_view          the review queue was opened
 *
 * WHAT IT COLLECTS: the event name, the page path with the query string
 * stripped, the product reference for a click, and a date.
 *
 * WHAT IT NEVER COLLECTS: no cookie, no local storage, no fingerprint, no IP
 * address (the collector discards it on arrival), no user agent, no referrer
 * URL, no query string, no cross-day identifier of any kind.
 *
 * CONSENT: Global Privacy Control and Do Not Track are honoured by not sending
 * anything at all. There is no consent banner because there is nothing to
 * consent to beyond an aggregate count.
 *
 * OFF BY DEFAULT. Nothing leaves the browser unless a page sets
 * window.CC_ANALYTICS_ENDPOINT to the URL of the self-hosted collector in
 * analytics/collect.js. See review/measurement.html for what has to be true
 * before that is switched on.
 */
(function () {
  "use strict";

  var EVENTS = [
    "page_view",
    "outbound_product_click",
    "guide_read_75",
    "compare_view",
    "flag_page_view"
  ];

  function optedOut() {
    var dnt = navigator.doNotTrack === "1" ||
      window.doNotTrack === "1" ||
      navigator.msDoNotTrack === "1";
    var gpc = navigator.globalPrivacyControl === true;
    return dnt || gpc;
  }

  var endpoint = window.CC_ANALYTICS_ENDPOINT || "";
  if (!endpoint || optedOut()) {
    /* Deliberate no-op. The names stay inspectable; nothing is sent. */
    window.CC_ANALYTICS = {
      enabled: false,
      reason: !endpoint ? "no endpoint configured" : "opt-out signal present",
      events: EVENTS.slice(),
      track: function () {}
    };
    return;
  }

  var buffer = [];
  var fired = {};

  function send() {
    if (!buffer.length) return;
    var body = JSON.stringify({ events: buffer.splice(0, buffer.length) });
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon(endpoint, new Blob([body], { type: "application/json" }));
      } else {
        fetch(endpoint, {
          method: "POST",
          body: body,
          keepalive: true,
          headers: { "Content-Type": "application/json" },
          credentials: "omit"
        });
      }
    } catch (e) {
      /* A failed beacon must never break the page. */
    }
  }

  function track(name, detail) {
    if (EVENTS.indexOf(name) === -1) return;
    if (fired[name]) return;           /* one per page per event */
    fired[name] = true;
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
  window.addEventListener("pagehide", send);

  track("page_view");

  var path = location.pathname;
  if (/\/compare\/?$/.test(path)) track("compare_view");
  if (/\/review\/?$/.test(path)) track("flag_page_view");

  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("a[rel~='sponsored']");
    if (!a) return;
    var m = (a.getAttribute("href") || "").match(/\/(?:dp\/)?(B0[0-9A-Z]{8})/);
    track("outbound_product_click", { ref: m ? m[1] : null });
  });

  /* A guide counts as read at 75% of its scrollable height, once. This is a
     crude measure and is described as crude on the measurement page. */
  if (/\/guides\/[^/]+\.html$/.test(path)) {
    var onScroll = function () {
      var doc = document.documentElement;
      var max = doc.scrollHeight - window.innerHeight;
      if (max > 0 && window.scrollY / max >= 0.75) {
        track("guide_read_75");
        window.removeEventListener("scroll", onScroll);
      }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  window.CC_ANALYTICS = { enabled: true, events: EVENTS.slice(), track: track };
})();
