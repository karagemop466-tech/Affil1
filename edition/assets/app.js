/* Progressive enhancement for Fit Finder, Suggestions Decision Queue, and Design Prompt Builder */
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
      textarea.value = lines.join("\n");
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
