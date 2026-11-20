/*! Affil1 — analytics.js
   Self-hosted, privacy-preserving analytics + outbound click counter.

   Five defined events:
     1. page_view        — a page loads
     2. outbound_click   — a sponsored/affiliate outbound link is clicked
     3. guide_engagement — a reader opens or reads a question-shaped guide
     4. suggestion_action — a reviewer acts on a suggestion (approve/decline/park)
     5. conversion_attempt — a reader reaches an outbound product destination

   Design:
   - No third-party scripts, no cookies, no personal data.
   - Events are counted client-side and beaconed to /api/collect (same origin).
   - /api/collect is a defined endpoint; on GitHub Pages it requires a serverless
     function to persist. Until then, events are kept in localStorage and exposed
     through window.affil1Analytics.events() so the dashboard can show them.
   - All network calls are best-effort and never block navigation. */

(function () {
  'use strict';

  const ENDPOINT = '/api/collect';
  const STORAGE_KEY = 'affil1_events';
  const MAX_EVENTS = 500;

  const state = { queue: [] };

  function load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) state.queue = JSON.parse(raw);
    } catch (e) { state.queue = []; }
    if (!Array.isArray(state.queue)) state.queue = [];
  }

  function persist() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state.queue.slice(-MAX_EVENTS)));
    } catch (e) { /* storage unavailable; events live in memory only */ }
  }

  function beacon(eventName, payload) {
    const event = {
      id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random(),
      ts: new Date().toISOString(),
      event: eventName,
      path: location.pathname,
      referrer: document.referrer || '',
      ua: navigator.userAgent,
      payload: payload || {},
    };
    state.queue.push(event);
    persist();

    // Best-effort beacon to self-hosted endpoint; never throws, never waits.
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT, JSON.stringify(event));
      } else {
        fetch(ENDPOINT, {
          method: 'POST',
          body: JSON.stringify(event),
          headers: { 'Content-Type': 'application/json' },
          keepalive: true,
        }).catch(function () { /* endpoint not yet wired — acceptable */ });
      }
    } catch (e) { /* ignore */ }
  }

  function record(eventName, payload) {
    beacon(eventName, payload);
  }

  function events() {
    return state.queue.slice();
  }

  function counts() {
    const c = {};
    state.queue.forEach(function (e) { c[e.event] = (c[e.event] || 0) + 1; });
    return c;
  }

  // Public API
  window.affil1Analytics = {
    record: record,
    events: events,
    counts: counts,
    ENDPOINT: ENDPOINT,
  };

  load();

  // Auto-record page_view on load (also called from main.js)
  if (typeof window.affil1Boot === 'function') {
    const orig = window.affil1Boot;
    window.affil1Boot = function () {
      orig();
      record('page_view', { path: location.pathname });
    };
  } else {
    record('page_view', { path: location.pathname });
  }
})();
