/* The Pantry Journal — event script.
 *
 * Ships inert. Nothing is transmitted unless the page sets
 * window.PANTRY_ENDPOINT to a first-party URL you control.
 *
 * What it sends: event name, page path, product id (for clicks), and a
 * coarse viewport class. No cookie, no local storage, no fingerprint, no
 * IP retention by this script, no third-party request.
 *
 * What it cannot tell you: whether anyone bought anything. That lives in
 * the Amazon Associates report and nowhere else.
 */
(function () {
  "use strict";

  var ENDPOINT = window.PANTRY_ENDPOINT || "";
  var SITE = "pantry-journal";
  var sent = {};
  var started = Date.now();

  function honourOptOut() {
    // Do Not Track and Global Privacy Control are treated as a no.
    if (navigator.doNotTrack === "1" || window.doNotTrack === "1") return true;
    if (navigator.globalPrivacyControl === true) return true;
    return false;
  }

  function viewportClass() {
    var w = window.innerWidth || 0;
    if (w < 600) return "s";
    if (w < 1000) return "m";
    return "l";
  }

  function send(event, props) {
    if (!ENDPOINT) return;          // inert by default
    if (honourOptOut()) return;     // respects DNT / GPC
    if (sent[event]) return;        // once per page view
    sent[event] = true;
    var body = {
      site: SITE,
      event: event,
      path: location.pathname,
      ts: new Date().toISOString(),
      props: props || {}
    };
    try {
      var payload = JSON.stringify(body);
      if (navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT, payload);
      } else {
        fetch(ENDPOINT, { method: "POST", body: payload, keepalive: true, mode: "cors" });
      }
    } catch (e) {
      /* measurement must never break the page */
    }
  }

  // E1 — page_view
  send("page_view", { vp: viewportClass(), ref: document.referrer ? "external" : "direct" });

  // E2 — outbound_product_click and E4 — compare_view
  document.addEventListener("click", function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest("a[data-product]") : null;
    if (!a) return;
    if (a.hostname && a.hostname.indexOf("amazon.") === -1) return;
    send("outbound_product_click", {
      product: a.getAttribute("data-product") || "",
      where: a.getAttribute("data-where") || ""
    });
  }, { passive: true });

  // E4 — a comparison table being rendered is a page-level fact
  if (document.querySelector("[data-compare]")) {
    send("compare_view", { table: document.querySelector("[data-compare]").getAttribute("data-compare") });
  }

  // E5 — flagged page opened
  if (/\/flagged\//.test(location.pathname)) {
    send("flag_page_view", { from: document.referrer ? "external" : "direct" });
  }

  // E3 — guide_read_75, once, after 75% of the article has been seen
  var article = document.querySelector("[data-guide]");
  if (article) {
    var fired = false;
    function check() {
      if (fired) return;
      var r = article.getBoundingClientRect();
      var seen = (window.innerHeight - r.top) / r.height;
      if (seen >= 0.75) {
        fired = true;
        send("guide_read_75", { guide: article.getAttribute("data-guide"), seconds: Math.round((Date.now() - started) / 1000) });
        window.removeEventListener("scroll", check);
      }
    }
    window.addEventListener("scroll", check, { passive: true });
  }
})();
