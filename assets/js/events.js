/* Crisp & Counter — five events, no collector.
 *
 * The parallel sessions own the collector contract:
 *   POST /analytics/collect, newline-delimited JSON, implemented in server/collect.js.
 * This file implements the five names defined in src/data/events.json. It
 * previously shipped a different five (outbound_click, guide_read,
 * suggestion_review, session_start), so the published spec and the published
 * code disagreed. tools/validate.py now fails the build on that.
 *
 * It is inert by default. Nothing is sent unless window.CRISP_ANALYTICS_ENDPOINT
 * is set to a real host, because GitHub Pages is static and cannot receive a POST.
 * No cookie, no localStorage, no fingerprint, no third-party script.
 */
(function () {
  "use strict";

  var ENDPOINT = window.CRISP_ANALYTICS_ENDPOINT || null;

  // The five defined events. Kept in one place so the spec and the code cannot drift.
  var EVENTS = ["page_view", "outbound_product_click", "guide_read_75", "compare_view", "flag_page_view"];

  var queue = [];

  function record(name, payload) {
    if (EVENTS.indexOf(name) === -1) { return; }
    if (!ENDPOINT) { return; } // inert until a first-party host exists
    payload = payload || {};
    payload.path = location.pathname;
    queue.push({ event: name, props: payload });
    flush();
  }

  function flush() {
    if (!queue.length || !ENDPOINT) { return; }
    var body = queue.map(function (e) { return JSON.stringify(e); }).join("\n");
    queue = [];
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT, new Blob([body + "\n"], { type: "application/x-ndjson" }));
      } else {
        fetch(ENDPOINT, {
          method: "POST",
          headers: { "Content-Type": "application/x-ndjson" },
          body: body + "\n",
          keepalive: true
        });
      }
    } catch (err) {
      // Measurement must never break the page.
    }
  }

  // E1: every page load is a view.
  record("page_view", { page: location.pathname });

  // E2: outbound product clicks. Counted locally before navigation; nothing about
  // what happens after the click is knowable from this site.
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest ? ev.target.closest("a.btn") : null;
    if (!a || !a.href) { return; }
    if (a.href.indexOf("link.amazon") === -1 && a.href.indexOf("/dp/") === -1) { return; }
    var card = a.closest(".card");
    record("outbound_product_click", { product: card ? card.id : "" });
  }, true);

  // E3: a guide counts as read at 75% of its scrollable height.
  var guide = document.querySelector(".article-body");
  if (guide) {
    var fired = false;
    var onScroll = function () {
      if (fired) { return; }
      var total = document.documentElement.scrollHeight - window.innerHeight;
      if (total <= 0) { return; }
      if ((window.scrollY / total) >= 0.75) {
        fired = true;
        record("guide_read_75", { guide: location.pathname });
        window.removeEventListener("scroll", onScroll);
      }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // E4 / E5: the two page-level events, keyed off the page's own body class so
  // the rule travels with the page rather than with a URL pattern.
  var bodyClass = (document.body && document.body.className) || "";
  if (bodyClass.indexOf("compare") !== -1) { record("compare_view", { page: location.pathname }); }
  if (bodyClass.indexOf("review") !== -1 || bodyClass.indexOf("flagged") !== -1) {
    record("flag_page_view", { page: location.pathname });
  }
})();
