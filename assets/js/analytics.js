// Privacy-preserving measurement. INERT UNTIL CONFIGURED.
//
// Design constraints, all deliberate:
//   * No redirect. The anchor's real href is the Amazon URL, and the browser
//     navigates to it directly. This keeps the site clear of the "Redirecting
//     Link" disqualification and the URL-obscuring prohibition (S08, S09).
//   * No cookie, no localStorage, no session id, no IP collection, no user agent,
//     no fingerprint. Only an aggregate counter keyed by event name and a small
//     set of non-identifying values (page path, product id, placement).
//   * sendBeacon so the request survives the navigation.
//
// Set CRISP_ENDPOINT to a URL to turn collection on. While it is null the beacon
// does nothing and no network request is made. See /records/measurement/.
(function () {
  "use strict";

  var CRISP_ENDPOINT = null; // e.g. "/api/collect" or an absolute HTTPS URL.

  function track(name, payload) {
    if (!CRISP_ENDPOINT) return;
    var body = JSON.stringify({
      e: name,
      p: payload || {},
      // Day granularity only. Not a timestamp-to-the-second that could single
      // out a visitor; the endpoint aggregates by day.
      d: new Date().toISOString().slice(0, 10),
      t: "shopnow047c-20"
    });
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon(CRISP_ENDPOINT, new Blob([body], { type: "application/json" }));
      } else {
        fetch(CRISP_ENDPOINT, { method: "POST", body: body, headers: { "Content-Type": "application/json" }, keepalive: true }).catch(function () {});
      }
    } catch (e) { /* measurement must never break navigation */ }
  }

  window.crispTrack = track;

  // page_view
  track("page_view", { path: location.pathname });

  // outbound_click — fire, then let the browser follow the real link.
  document.addEventListener("click", function (ev) {
    var el = ev.target.closest ? ev.target.closest("[data-event='outbound_click']") : null;
    if (!el) return;
    track("outbound_click", {
      product_id: el.getAttribute("data-product") || "",
      placement: el.getAttribute("data-placement") || ""
    });
    // No preventDefault. The navigation is the user's, to Amazon, directly.
  }, { capture: true });
})();
