/* Privacy-preserving 5-event outbound & engagement counter.
 * Zero cookies, zero cross-site identifiers, honors DNT and Global Privacy Control.
 * Inert on static GitHub Pages unless window.COUNTERTOP_COLLECTOR_URL is configured.
 */
(function () {
  "use strict";

  var ALLOWED = {
    page_view: ["page"],
    product_card_click: ["page", "product_id"],
    guide_to_product_click: ["page", "guide_slug", "product_id"],
    comparison_filter_use: ["page", "filter_key"],
    suggestion_decision: ["page", "suggestion_id", "decision"]
  };

  var STORAGE_KEY = "countertop_almanac_event_preview_v1";

  function privacyBlocked() {
    if (typeof navigator === "undefined") return false;
    if (navigator.doNotTrack === "1" || window.doNotTrack === "1") return true;
    if (navigator.globalPrivacyControl === true) return true;
    return false;
  }

  function pageSlug() {
    var el = document.documentElement;
    return (el && el.getAttribute("data-page-slug")) || "index";
  }

  function saveLocalPreview(payload) {
    try {
      var raw = window.sessionStorage.getItem(STORAGE_KEY);
      var store = raw ? JSON.parse(raw) : {};
      var key = payload.event;
      store[key] = (store[key] || 0) + 1;
      window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify(store));
    } catch (_) {
      /* sessionStorage optional */
    }
  }

  function recordEvent(eventName, fields) {
    if (!ALLOWED[eventName] || privacyBlocked()) return false;
    var payload = { event: eventName };
    var required = ALLOWED[eventName];
    var src = fields || {};
    for (var i = 0; i < required.length; i++) {
      var k = required[i];
      var v = k === "page" ? (src.page || pageSlug()) : src[k];
      if (!v) return false;
      payload[k] = String(v).slice(0, 80);
    }

    saveLocalPreview(payload);

    var endpoint = window.COUNTERTOP_COLLECTOR_URL;
    if (endpoint && typeof endpoint === "string") {
      var body = JSON.stringify(payload);
      try {
        if (navigator.sendBeacon) {
          var blob = new Blob([body], { type: "application/json" });
          navigator.sendBeacon(endpoint, blob);
        } else if (window.fetch) {
          window.fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: body,
            keepalive: true
          }).catch(function () {});
        }
      } catch (_) {}
    }
    document.dispatchEvent(new CustomEvent("countertop:event", { detail: payload }));
    return true;
  }

  window.CountertopAnalytics = {
    record: recordEvent,
    getSessionCounts: function () {
      try {
        return JSON.parse(window.sessionStorage.getItem(STORAGE_KEY) || "{}");
      } catch (_) {
        return {};
      }
    }
  };

  document.addEventListener("DOMContentLoaded", function () {
    recordEvent("page_view", { page: pageSlug() });

    document.addEventListener("click", function (ev) {
      var link = ev.target && ev.target.closest ? ev.target.closest("a[data-track-event]") : null;
      if (!link) return;
      var evt = link.getAttribute("data-track-event");
      var pid = link.getAttribute("data-product-id");
      var gslug = link.getAttribute("data-guide-slug");
      recordEvent(evt, {
        page: pageSlug(),
        product_id: pid,
        guide_slug: gslug
      });
    });
  });
})();
