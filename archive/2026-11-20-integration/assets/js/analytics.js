/* Affil1 — self-hosted, privacy-preserving analytics
   Five defined events (documented here; no other events are recorded):
     1. page_view     — a page is loaded
     2. outbound_click — a user clicks an outbound (affiliate) link
     3. guide_read     — a user finishes reading a buying guide
     4. suggestion_review — a user reviews a decision suggestion
     5. session_start  — first page view of a browser session

   Design:
   - No cookies, no personal identifiers, no IP logging in the client code.
   - Events are queued in memory and persisted to localStorage ("affil1_events").
   - A self-hosted collector endpoint (server/collect.js) accepts POST /analytics/collect
     and appends events to data/events.jsonl. Run it on your own host; GitHub Pages
     is static, so the endpoint must be self-hosted elsewhere or enabled via your host.
   - The beacon falls back silently if the endpoint is unreachable — the page never
     breaks because of analytics.
   - Outbound product links are counted automatically; each link keeps its own
     counter so clicks can be compared against orders in first-party reports.
*/

(function () {
  var ENDPOINT = (window.affil1Root || "") + "analytics/collect";
  var STORAGE_KEY = "affil1_events";
  var MAX_QUEUE = 50;
  var sessionId = sessionStorage.getItem("affil1_session");
  if (!sessionId) {
    sessionId = "s" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
    sessionStorage.setItem("affil1_session", sessionId);
  }

  var queue = [];

  function enqueue(event, payload) {
    var item = {
      t: new Date().toISOString(),
      e: event,
      s: sessionId,
      p: payload || {},
      l: location.href,
      r: document.referrer || "",
    };
    queue.push(item);
    persist();
    flush();
  }

  function persist() {
    try {
      var stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
      stored = stored.concat(queue.slice(-MAX_QUEUE));
      localStorage.setItem(STORAGE_KEY, JSON.stringify(stored.slice(-MAX_QUEUE)));
    } catch (e) { /* storage unavailable — ignore */ }
    queue = [];
  }

  function flush() {
    try {
      var stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
      if (!stored.length) return;
      var pending = stored.slice(0);
      var xhr = new XMLHttpRequest();
      xhr.open("POST", ENDPOINT, true);
      xhr.setRequestHeader("Content-Type", "application/x-ndjson");
      xhr.onerror = function () { /* endpoint unreachable — keep in localStorage */ };
      xhr.onabort = function () {};
      xhr.ontimeout = function () {};
      xhr.send(
        pending
          .map(function (e) { return JSON.stringify(e); })
          .join("\n") + "\n"
      );
      localStorage.setItem(STORAGE_KEY, JSON.stringify([]));
    } catch (e) { /* ignore */ }
  }

  /* Public API: affil1.record(event, payload) */
  window.affil1 = window.affil1 || {};
  window.affil1.record = enqueue;

  /* Automatic page view */
  enqueue("page_view", { title: document.title });

  /* Automatic outbound click counter for affiliate links */
  document.addEventListener("click", function (ev) {
    var link = ev.target.closest && ev.target.closest("a[href]");
    if (!link) return;
    var href = link.getAttribute("href") || "";
    if (!href) return;
    try {
      var isOutbound = href.startsWith("http") && !href.includes(location.hostname);
      var isSponsored = link.rel && link.rel.split(/\s+/).indexOf("sponsored") !== -1;
      var isProduct = link.classList.contains("product-link");
      if (isOutbound && (isSponsored || isProduct)) {
        enqueue("outbound_click", {
          url: href,
          text: (link.textContent || "").trim().slice(0, 120),
          sponsored: isSponsored,
          product: isProduct,
        });
      }
    } catch (e) { /* ignore malformed links */ }
  }, { passive: true });

  /* Periodic flush every 30 seconds */
  setInterval(flush, 30000);
})();

/* Helper used by guides: mark a guide as read */
function affil1GuideRead(slug) {
  if (window.affil1 && window.affil1.record) {
    window.affil1.record("guide_read", { guide: slug });
  }
}

/* Helper used by suggestions page */
function affil1SuggestionReviewed(id) {
  if (window.affil1 && window.affil1.record) {
    window.affil1.record("suggestion_review", { suggestion: id });
  }
}

/* Helper: session start already recorded on first load */
function affil1SessionStart() {
  if (window.affil1 && window.affil1.record) {
    window.affil1.record("session_start", {});
  }
}
affil1SessionStart();
