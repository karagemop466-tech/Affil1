/* Site behaviour: the decision controls on the suggestions page.
   No framework. Nothing here sends anything anywhere. */

(function () {
  "use strict";

  var KEY = "cc:decisions";

  function read() {
    try {
      return JSON.parse(localStorage.getItem(KEY) || "{}");
    } catch (e) {
      return {};
    }
  }

  function write(state) {
    try {
      localStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) {
      /* Private mode or storage disabled: the page still works, it just
         forgets the choice. Nothing is lost that matters. */
    }
  }

  function paint(card, state) {
    var id = card.id;
    var note = card.querySelector("[data-note]");
    card.setAttribute("data-state", state || "");
    card.querySelectorAll(".decide").forEach(function (btn) {
      var isOn = btn.getAttribute("data-decision") === state;
      btn.setAttribute("aria-pressed", isOn ? "true" : "false");
    });
    if (note) {
      note.textContent =
        state === "accept" ? "Marked: accept" :
        state === "hold" ? "Marked: hold" :
        state === "reject" ? "Marked: reject" : "Undecided";
    }
    return id;
  }

  function count() {
    var state = read();
    var n = Object.keys(state).length;
    var total = document.querySelectorAll(".scard").length;
    var el = document.querySelector("[data-count]");
    if (el) {
      el.textContent = n + " of " + total + " decided";
    }
  }

  function init() {
    var state = read();
    document.querySelectorAll(".scard").forEach(function (card) {
      paint(card, state[card.id] || "");
      card.querySelectorAll(".decide").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var next = btn.getAttribute("data-decision");
          var current = read();
          if (current[card.id] === next) {
            delete current[card.id];
            next = "";
          } else {
            current[card.id] = next;
          }
          write(current);
          paint(card, next);
          count();
        });
      });
    });
    count();
  }

  function summary() {
    var state = read();
    var ids = Object.keys(state).sort();
    if (!ids.length) {
      return "No decisions recorded yet.";
    }
    var lines = ["Decisions recorded on the Crisp & Counter suggestions page:"];
    ids.forEach(function (id) {
      var card = document.getElementById(id);
      var title = card ? card.querySelector("h3").textContent.trim() : id;
      lines.push("- " + id + " [" + state[id] + "] " + title);
    });
    lines.push("");
    lines.push("Recorded locally in a browser on " + new Date().toISOString().slice(0, 10) +
      ". Nothing was transmitted by the site.");
    return lines.join("\n");
  }

  function toast(msg) {
    var el = document.createElement("p");
    el.className = "decide-toast";
    el.setAttribute("role", "status");
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(function () { el.remove(); }, 2600);
  }

  document.addEventListener("click", function (ev) {
    var btn = ev.target.closest("[data-action]");
    if (!btn) return;
    var action = btn.getAttribute("data-action");
    if (action === "copy") {
      var text = summary();
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          toast("Copied. Paste it wherever the decision is meant to go.");
        }, function () {
          window.prompt("Copy the decisions:", text);
        });
      } else {
        window.prompt("Copy the decisions:", text);
      }
    }
    if (action === "reset") {
      write({});
      document.querySelectorAll(".scard").forEach(function (c) { paint(c, ""); });
      count();
      toast("Cleared.");
    }
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

/* The offer board: choosing a row, and choosing a path. One choice at a time,
   remembered locally, nothing transmitted. A path clears an individual pick,
   because a path is a bundle and mixing them is the mistake the page prevents. */
(function () {
  "use strict";
  var KEY = "cc:offer";
  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || "{}"); }
    catch (e) { return {}; }
  }
  function write(state) {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* private mode */ }
  }
  function paint() {
    var state = read();
    document.querySelectorAll(".offer-pick").forEach(function (btn) {
      var offer = btn.getAttribute("data-offer");
      var path = btn.getAttribute("data-path");
      var on = offer ? state.offer === offer : path ? state.path === path : false;
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      if (offer) {
        var label = btn.parentNode.querySelector(".offer-picked");
        if (label) { label.textContent = on ? "Chosen" : ""; }
      }
    });
  }
  function init() {
    if (!document.querySelector(".offer-pick")) { return; }
    paint();
    document.addEventListener("click", function (ev) {
      var btn = ev.target.closest ? ev.target.closest(".offer-pick") : null;
      if (!btn) { return; }
      var state = read();
      var offer = btn.getAttribute("data-offer");
      var path = btn.getAttribute("data-path");
      if (offer) { state.offer = state.offer === offer ? null : offer; state.path = null; }
      else if (path) { state.path = state.path === path ? null : path; state.offer = null; }
      write(state); paint();
    });
  }
  if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", init); }
  else { init(); }
})();
