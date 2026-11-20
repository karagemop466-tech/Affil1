#!/usr/bin/env python3
"""Static CSS, privacy-preserving JS, interactive workbench JS, and SVG assets for edition/."""

from __future__ import annotations

STYLE_CSS = """/* Countertop Almanac — Editorial Storefront & Verification Desk */
:root {
  --bg: #faf7f2;
  --surface: #ffffff;
  --surface-alt: #f3ede3;
  --ink: #191816;
  --ink-muted: #524e48;
  --border: #dfd8cc;
  --border-strong: #c5bba9;
  --accent: #b84a27;
  --accent-hover: #96381a;
  --accent-soft: #fbeee9;
  --ok-bg: #e6f3ec;
  --ok-ink: #1b4d37;
  --warn-bg: #fef3c7;
  --warn-ink: #854d0e;
  --info-bg: #e8eef5;
  --info-ink: #1e3a5f;
  --max-w: 1180px;
  --serif: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif;
  --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

*, *::before, *::after { box-sizing: border-box; }

html {
  font-size: 16px;
  scroll-behavior: smooth;
  background: var(--bg);
  color: var(--ink);
}

body {
  margin: 0;
  font-family: var(--sans);
  line-height: 1.62;
  color: var(--ink);
  background: var(--bg);
}

a {
  color: var(--accent);
  text-underline-offset: 3px;
}
a:hover { color: var(--accent-hover); }
a:focus-visible, button:focus-visible, select:focus-visible, input:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

.skip-link {
  position: absolute;
  left: -9999px;
  top: 0;
  background: var(--ink);
  color: #fff;
  padding: 0.5rem 1rem;
  z-index: 1000;
}
.skip-link:focus { left: 0.75rem; top: 0.75rem; }

.container {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 1.25rem;
}

/* Masthead + single primary nav group */
.site-header {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
}

.masthead-inner {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 0;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: var(--ink);
}
.brand-mark {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  flex-shrink: 0;
}
.brand-title {
  display: block;
  font-family: var(--serif);
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: -0.015em;
  line-height: 1.15;
}
.brand-sub {
  display: block;
  font-size: 0.78rem;
  color: var(--ink-muted);
  letter-spacing: 0.02em;
}

.primary-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 0.9rem;
  align-items: center;
}
.primary-nav a {
  text-decoration: none;
  color: var(--ink);
  font-size: 0.92rem;
  font-weight: 550;
  padding: 0.35rem 0.6rem;
  border-radius: 6px;
}
.primary-nav a:hover,
.primary-nav a[aria-current="page"] {
  background: var(--surface-alt);
  color: var(--accent);
}

/* Above-the-fold Associates & FTC disclosure strip */
.disclosure {
  background: #f2ebe0;
  border-bottom: 1px solid var(--border);
  font-size: 0.84rem;
  color: var(--ink);
  padding: 0.55rem 0;
}
.disclosure-inner {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem 1rem;
  align-items: center;
  justify-content: space-between;
}
.disclosure strong {
  font-weight: 650;
}
.annex-note {
  background: #12261f;
  color: #f2ebe0;
  font-size: 0.84rem;
  padding: 0.7rem 0;
}
.annex-inner {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem 1rem;
  align-items: center;
  justify-content: space-between;
}
.annex-note a {
  color: #12261f;
  background: #e9b44c;
  border-color: #e9b44c;
}
.disclosure-meta {
  color: var(--ink-muted);
  font-size: 0.8rem;
}

main {
  padding: 2rem 0 3.5rem;
}

/* Editorial Hero */
.hero {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 1px 3px rgba(25, 24, 22, 0.04);
}
.eyebrow {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--accent);
  margin-bottom: 0.5rem;
}
h1 {
  font-family: var(--serif);
  font-size: clamp(1.75rem, 3vw, 2.45rem);
  line-height: 1.18;
  letter-spacing: -0.02em;
  margin: 0 0 0.75rem;
  color: var(--ink);
}
h2 {
  font-family: var(--serif);
  font-size: clamp(1.3rem, 2.1vw, 1.7rem);
  line-height: 1.25;
  margin: 2.2rem 0 0.75rem;
}
h3 {
  font-family: var(--serif);
  font-size: 1.15rem;
  line-height: 1.3;
  margin: 1.25rem 0 0.45rem;
}
.lede {
  font-size: 1.08rem;
  color: var(--ink-muted);
  max-width: 72ch;
  margin: 0 0 1.1rem;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.15rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.62rem 1.05rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  border: 1px solid transparent;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.15s ease, border-color 0.15s ease;
}
.btn-primary {
  background: var(--accent);
  color: #fff;
}
.btn-primary:hover {
  background: var(--accent-hover);
  color: #fff;
}
.btn-secondary {
  background: var(--surface);
  color: var(--ink);
  border-color: var(--border-strong);
}
.btn-secondary:hover {
  background: var(--surface-alt);
  color: var(--ink);
}
.btn-sm {
  padding: 0.38rem 0.72rem;
  font-size: 0.82rem;
}

/* Interactive Filter Bar */
.filter-bar {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  margin: 1.25rem 0 1.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  align-items: center;
}
.filter-label {
  font-size: 0.84rem;
  font-weight: 650;
  color: var(--ink-muted);
  margin-right: 0.35rem;
}
.chip-btn {
  background: var(--bg);
  border: 1px solid var(--border-strong);
  color: var(--ink);
  padding: 0.36rem 0.78rem;
  border-radius: 999px;
  font-size: 0.83rem;
  font-weight: 550;
  cursor: pointer;
}
.chip-btn:hover,
.chip-btn[aria-pressed="true"] {
  background: var(--ink);
  color: #fff;
  border-color: var(--ink);
}

/* Product Shortlist Grid */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
  gap: 1.25rem;
  margin-top: 1rem;
}
.product-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.35rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1rem;
}
.product-card[hidden] { display: none; }

.card-media {
  background: var(--surface-alt);
  border-radius: 9px;
  padding: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border);
}
.card-media img {
  width: 100%;
  max-width: 240px;
  height: 135px;
  object-fit: contain;
}
.media-caption {
  font-size: 0.74rem;
  color: var(--ink-muted);
  margin-top: 0.35rem;
}

.card-top-meta {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 0.4rem;
  align-items: center;
}

.badge {
  display: inline-block;
  padding: 0.18rem 0.55rem;
  border-radius: 999px;
  font-size: 0.74rem;
  font-weight: 650;
  letter-spacing: 0.01em;
  font-variant-numeric: tabular-nums;
}
.badge-ok { background: var(--ok-bg); color: var(--ok-ink); }
.badge-warn { background: var(--warn-bg); color: var(--warn-ink); }
.badge-info { background: var(--info-bg); color: var(--info-ink); }

.spec-list {
  margin: 0.5rem 0;
  padding-left: 1.15rem;
  font-size: 0.9rem;
}
.spec-list li { margin-bottom: 0.28rem; }

.fit-box {
  background: var(--bg);
  border-left: 3px solid var(--accent);
  padding: 0.65rem 0.85rem;
  font-size: 0.87rem;
  border-radius: 0 6px 6px 0;
}
.fit-box p { margin: 0.25rem 0; }

.paid-microcopy {
  font-size: 0.77rem;
  color: var(--ink-muted);
  margin-top: 0.4rem;
}

/* Editorial Guide Cards */
.guide-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.15rem;
  margin-top: 1rem;
}
.guide-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.guide-card h3 { margin-top: 0.35rem; }
.guide-card h3 a {
  color: var(--ink);
  text-decoration: none;
}
.guide-card h3 a:hover { color: var(--accent); }

/* Dashboard Tables */
.table-wrap {
  overflow-x: auto;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  margin: 1rem 0 1.75rem;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.88rem;
  font-variant-numeric: tabular-nums;
}
th, td {
  text-align: left;
  vertical-align: top;
  padding: 0.72rem 0.85rem;
  border-bottom: 1px solid var(--border);
}
th {
  background: var(--surface-alt);
  font-weight: 650;
  font-size: 0.79rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--ink-muted);
}
tr:last-child td { border-bottom: none; }
code {
  font-family: var(--mono);
  font-size: 0.83em;
  background: var(--surface-alt);
  padding: 0.12rem 0.35rem;
  border-radius: 4px;
}

.cell-blank {
  background: #fdfaf3;
}

/* Callouts & Panels */
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.35rem 1.5rem;
  margin: 1.25rem 0;
}
.panel-warn {
  background: #fffbeb;
  border-color: #f3d37a;
}

.kpi-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
  gap: 0.9rem;
  margin: 1.25rem 0;
}
.kpi-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.95rem 1.1rem;
}
.kpi-num {
  display: block;
  font-family: var(--serif);
  font-size: 1.55rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}
.kpi-label {
  font-size: 0.8rem;
  color: var(--ink-muted);
}

/* Prompt Workbench */
.prompt-output {
  width: 100%;
  min-height: 250px;
  font-family: var(--mono);
  font-size: 0.84rem;
  line-height: 1.5;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid var(--border-strong);
  background: #fcfaf7;
  color: var(--ink);
}
.module-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
  gap: 0.85rem;
  margin: 1rem 0;
}
.module-item {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.85rem 1rem;
}
.decision-group {
  display: inline-flex;
  gap: 0.35rem;
  flex-wrap: wrap;
}
.decision-btn[aria-pressed="true"] {
  background: var(--ink);
  color: #fff;
  border-color: var(--ink);
}

/* Article body */
.article-shell {
  max-width: 78ch;
}
.article-shell p {
  font-size: 1.02rem;
  margin: 0 0 1.05rem;
}

/* Footer */
.site-footer {
  background: var(--surface);
  border-top: 1px solid var(--border);
  padding: 2.5rem 0 2rem;
  margin-top: 2rem;
  font-size: 0.88rem;
}
.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.75rem;
}
.footer-col h4 {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--ink-muted);
  margin: 0 0 0.65rem;
}
.footer-col ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.footer-col li { margin-bottom: 0.4rem; }
.footer-col a {
  color: var(--ink);
  text-decoration: none;
}
.footer-col a:hover { color: var(--accent); }
.footer-disclosure {
  border-top: 1px solid var(--border);
  padding-top: 1.15rem;
  color: var(--ink-muted);
  font-size: 0.82rem;
}

@media (max-width: 680px) {
  .hero { padding: 1.35rem; }
  .masthead-inner { flex-direction: column; align-items: flex-start; }
}
"""

ANALYTICS_JS = """/* Privacy-preserving 5-event outbound & engagement counter.
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
"""

APP_JS = """/* Progressive enhancement for Fit Finder, Suggestions Decision Queue, and Design Prompt Builder */
(function () {
  "use strict";

  var DECISIONS_KEY = "countertop_almanac_suggestion_decisions_v1";

  function track(eventName, data) {
    if (window.CountertopAnalytics && typeof window.CountertopAnalytics.record === "function") {
      window.CountertopAnalytics.record(eventName, data || {});
    }
  }

  function initFitFilters() {
    var groups = document.querySelectorAll("[data-filter-root]");
    groups.forEach(function (root) {
      var targetSelector = root.getAttribute("data-filter-target");
      var buttons = root.querySelectorAll("[data-filter-value]");
      buttons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          var val = btn.getAttribute("data-filter-value");
          buttons.forEach(function (b) {
            b.setAttribute("aria-pressed", b === btn ? "true" : "false");
          });
          var items = document.querySelectorAll(targetSelector);
          items.forEach(function (item) {
            if (val === "all") {
              item.hidden = false;
              return;
            }
            var tags = (item.getAttribute("data-tags") || "").split(/\s+/);
            item.hidden = tags.indexOf(val) === -1;
          });
          track("comparison_filter_use", { filter_key: val });
        });
      });
    });
  }

  function loadDecisions() {
    try {
      return JSON.parse(window.localStorage.getItem(DECISIONS_KEY) || "{}");
    } catch (_) {
      return {};
    }
  }

  function saveDecisions(map) {
    try {
      window.localStorage.setItem(DECISIONS_KEY, JSON.stringify(map));
    } catch (_) {}
  }

  function updateSuggestionSummary() {
    var rows = document.querySelectorAll("[data-suggestion-row]");
    if (!rows.length) return;
    var counts = { approved: 0, hold: 0, rejected: 0 };
    rows.forEach(function (row) {
      var active = row.querySelector(".decision-btn[aria-pressed='true']");
      var state = active ? active.getAttribute("data-decision") : row.getAttribute("data-default-decision");
      if (counts[state] !== undefined) counts[state] += 1;
    });
    var summaryEl = document.getElementById("suggestion-decision-summary");
    if (summaryEl) {
      summaryEl.textContent =
        "Approved: " + counts.approved + " · On Hold: " + counts.hold + " · Rejected: " + counts.rejected;
    }
  }

  function initSuggestionsQueue() {
    var rows = document.querySelectorAll("[data-suggestion-row]");
    if (!rows.length) return;
    var stored = loadDecisions();

    rows.forEach(function (row) {
      var sid = row.getAttribute("data-suggestion-id");
      var initial = stored[sid] || row.getAttribute("data-default-decision") || "hold";
      var buttons = row.querySelectorAll(".decision-btn");
      buttons.forEach(function (btn) {
        var d = btn.getAttribute("data-decision");
        btn.setAttribute("aria-pressed", d === initial ? "true" : "false");
        btn.addEventListener("click", function () {
          buttons.forEach(function (b) {
            b.setAttribute("aria-pressed", b === btn ? "true" : "false");
          });
          stored[sid] = d;
          saveDecisions(stored);
          updateSuggestionSummary();
          track("suggestion_decision", { suggestion_id: sid, decision: d });
        });
      });
    });
    updateSuggestionSummary();

    var exportBtn = document.getElementById("export-decisions-btn");
    if (exportBtn) {
      exportBtn.addEventListener("click", function () {
        var out = {};
        rows.forEach(function (row) {
          var sid = row.getAttribute("data-suggestion-id");
          var active = row.querySelector(".decision-btn[aria-pressed='true']");
          out[sid] = active ? active.getAttribute("data-decision") : "hold";
        });
        var blob = new Blob([JSON.stringify({ exported_on: "2026-11-20", decisions: out }, null, 2)], {
          type: "application/json"
        });
        var url = URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = "suggestion-decisions.json";
        a.click();
        URL.revokeObjectURL(url);
      });
    }
  }

  function initPromptBuilder() {
    var textarea = document.getElementById("generated-design-prompt");
    if (!textarea) return;
    var checkboxes = document.querySelectorAll("[data-prompt-module]");
    var focusSelect = document.getElementById("prompt-season-focus");
    var copyBtn = document.getElementById("copy-prompt-btn");
    var copyStatus = document.getElementById("copy-prompt-status");

    function rebuildPrompt() {
      var season = focusSelect ? focusSelect.value : "Year-round weeknight + holiday hosting";
      var lines = [
        "Design and build a polished, trustworthy Amazon Associates culinary-equipment publication (Tracking ID: shopnow047c-20) that converts organic search readers without AI-slop filler or unverified claims.",
        "",
        "Catalog Scope: 3 Countertop Air Fryers / Convection Ovens (P-01 Dual-Basket 6 Qt, P-02 French-Door 26 Qt Oven, P-03 Single-Basket 8 Qt) + 2 Meat Thermometers (P-04 Instant-Read Digital, P-05 3-Probe Wireless).",
        "Editorial & Seasonal Focus: " + season,
        "",
        "Selected Architecture, Content & Compliance Directives:"
      ];
      var idx = 1;
      checkboxes.forEach(function (cb) {
        if (cb.checked) {
          lines.push(idx + ". [" + cb.getAttribute("data-module-id") + "] " + cb.getAttribute("data-prompt-text"));
          idx += 1;
        }
      });
      textarea.value = lines.join("\\n");
    }

    checkboxes.forEach(function (cb) {
      cb.addEventListener("change", rebuildPrompt);
    });
    if (focusSelect) focusSelect.addEventListener("change", rebuildPrompt);
    rebuildPrompt();

    if (copyBtn) {
      copyBtn.addEventListener("click", function () {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(textarea.value).then(function () {
            if (copyStatus) copyStatus.textContent = "Copied prompt to clipboard.";
          });
        } else {
          textarea.select();
          document.execCommand("copy");
          if (copyStatus) copyStatus.textContent = "Selected prompt text.";
        }
      });
    }
  }

  function initEventInspector() {
    var box = document.getElementById("local-event-inspector");
    if (!box || !window.CountertopAnalytics) return;
    function render() {
      var counts = window.CountertopAnalytics.getSessionCounts();
      var keys = ["page_view", "product_card_click", "guide_to_product_click", "comparison_filter_use", "suggestion_decision"];
      box.textContent = keys
        .map(function (k) {
          return k + ": " + (counts[k] || 0);
        })
        .join("  |  ");
    }
    render();
    document.addEventListener("countertop:event", render);
  }

  document.addEventListener("DOMContentLoaded", function () {
    initFitFilters();
    initSuggestionsQueue();
    initPromptBuilder();
    initEventInspector();
  });
})();
"""

SVG_ASSETS: dict[str, str] = {
    "favicon.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36">
  <rect width="36" height="36" rx="8" fill="#191816"/>
  <rect x="6" y="9" width="24" height="18" rx="3" fill="none" stroke="#faf7f2" stroke-width="2"/>
  <line x1="18" y1="9" x2="18" y2="27" stroke="#b84a27" stroke-width="2"/>
  <circle cx="12" cy="18" r="2" fill="#e6b89c"/>
  <circle cx="24" cy="18" r="2" fill="#e6b89c"/>
</svg>""",
    "dual-basket.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 150" role="img" aria-label="Dual-basket air fryer diagram">
  <rect width="260" height="150" rx="10" fill="#f3ede3"/>
  <rect x="38" y="20" width="184" height="112" rx="14" fill="#2c2a28" stroke="#191816" stroke-width="2"/>
  <rect x="50" y="28" width="160" height="22" rx="4" fill="#191816"/>
  <circle cx="92" cy="39" r="4" fill="#b84a27"/>
  <circle cx="168" cy="39" r="4" fill="#b84a27"/>
  <rect x="48" y="58" width="76" height="64" rx="7" fill="#3d3a36" stroke="#c5bba9" stroke-width="1.5"/>
  <rect x="136" y="58" width="76" height="64" rx="7" fill="#3d3a36" stroke="#c5bba9" stroke-width="1.5"/>
  <rect x="58" y="76" width="56" height="24" rx="3" fill="#e9c89b" opacity="0.85"/>
  <rect x="146" y="76" width="56" height="24" rx="3" fill="#e9c89b" opacity="0.85"/>
  <rect x="82" y="64" width="8" height="36" rx="4" fill="#faf7f2"/>
  <rect x="170" y="64" width="8" height="36" rx="4" fill="#faf7f2"/>
</svg>""",
    "french-door-oven.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 150" role="img" aria-label="French-door countertop convection oven diagram">
  <rect width="260" height="150" rx="10" fill="#f3ede3"/>
  <rect x="26" y="22" width="208" height="108" rx="8" fill="#d8d2c7" stroke="#191816" stroke-width="2"/>
  <rect x="36" y="32" width="80" height="84" rx="4" fill="#faf7f2" stroke="#524e48" stroke-width="1.8"/>
  <rect x="120" y="32" width="80" height="84" rx="4" fill="#faf7f2" stroke="#524e48" stroke-width="1.8"/>
  <line x1="42" y1="62" x2="194" y2="62" stroke="#b84a27" stroke-width="2" stroke-dasharray="5 3"/>
  <line x1="42" y1="88" x2="194" y2="88" stroke="#b84a27" stroke-width="2" stroke-dasharray="5 3"/>
  <rect x="108" y="52" width="5" height="42" rx="2" fill="#191816"/>
  <rect x="123" y="52" width="5" height="42" rx="2" fill="#191816"/>
  <circle cx="218" cy="48" r="7" fill="#191816"/>
  <circle cx="218" cy="74" r="7" fill="#b84a27"/>
  <circle cx="218" cy="100" r="7" fill="#191816"/>
</svg>""",
    "single-basket.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 150" role="img" aria-label="Single-basket 8-quart air fryer diagram">
  <rect width="260" height="150" rx="10" fill="#f3ede3"/>
  <rect x="64" y="18" width="132" height="114" rx="16" fill="#595550" stroke="#191816" stroke-width="2"/>
  <rect x="78" y="28" width="104" height="22" rx="5" fill="#191816"/>
  <circle cx="130" cy="39" r="4.5" fill="#b84a27"/>
  <rect x="74" y="58" width="112" height="64" rx="9" fill="#2c2a28" stroke="#dfd8cc" stroke-width="1.5"/>
  <rect x="124" y="68" width="12" height="44" rx="5" fill="#faf7f2"/>
</svg>""",
    "instant-probe.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 150" role="img" aria-label="Handheld instant-read digital thermometer diagram">
  <rect width="260" height="150" rx="10" fill="#f3ede3"/>
  <rect x="34" y="56" width="118" height="38" rx="16" fill="#191816"/>
  <rect x="52" y="64" width="64" height="22" rx="4" fill="#2b3d34"/>
  <text x="84" y="79" text-anchor="middle" fill="#a7f3d0" font-family="monospace" font-size="12">PROBE</text>
  <circle cx="134" cy="75" r="7" fill="#b84a27"/>
  <line x1="152" y1="75" x2="230" y2="75" stroke="#7c776f" stroke-width="4" stroke-linecap="round"/>
  <polygon points="230,73 238,75 230,77" fill="#524e48"/>
</svg>""",
    "wireless-probes.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 150" role="img" aria-label="Three-probe wireless meat thermometer hub diagram">
  <rect width="260" height="150" rx="10" fill="#f3ede3"/>
  <rect x="52" y="26" width="156" height="98" rx="14" fill="#2c2a28" stroke="#191816" stroke-width="2"/>
  <line x1="74" y1="50" x2="186" y2="50" stroke="#dfd8cc" stroke-width="4" stroke-linecap="round"/>
  <circle cx="74" cy="50" r="6" fill="#b84a27"/>
  <line x1="74" y1="75" x2="186" y2="75" stroke="#dfd8cc" stroke-width="4" stroke-linecap="round"/>
  <circle cx="74" cy="75" r="6" fill="#b84a27"/>
  <line x1="74" y1="100" x2="186" y2="100" stroke="#dfd8cc" stroke-width="4" stroke-linecap="round"/>
  <circle cx="74" cy="100" r="6" fill="#b84a27"/>
</svg>""",
}
