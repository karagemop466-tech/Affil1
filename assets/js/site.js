// Small progressive enhancements. No dependencies, no tracking.
(function () {
  "use strict";

  // Mobile navigation toggle.
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.getAttribute("data-open") === "true";
      nav.setAttribute("data-open", open ? "false" : "true");
      toggle.setAttribute("aria-expanded", open ? "false" : "true");
      toggle.textContent = open ? "Menu" : "Close";
    });
  }

  // Suggestion decision controls. Writes to localStorage only — this records the
  // owner's own choice in their own browser. It never writes to a server.
  var KEY = "crisp-decisions-v1";
  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { return {}; }
  }
  function write(o) {
    try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) { /* storage may be blocked */ }
  }

  var stored = read();
  document.querySelectorAll("[data-decide]").forEach(function (group) {
    var id = group.getAttribute("data-decide");
    var current = stored[id];
    group.querySelectorAll("button").forEach(function (btn) {
      var state = btn.getAttribute("data-state");
      if (current === state) btn.setAttribute("aria-pressed", "true");
      btn.addEventListener("click", function () {
        var next = read();
        if (next[id] === state) {
          delete next[id];
          btn.setAttribute("aria-pressed", "false");
        } else {
          next[id] = state;
          group.querySelectorAll("button").forEach(function (b) {
            b.setAttribute("aria-pressed", b === btn ? "true" : "false");
          });
        }
        write(next);
        var out = document.getElementById("decision-out-" + id);
        if (out) {
          var now = read()[id];
          out.textContent = now
            ? "Marked " + now + " in this browser. Nothing has been changed on the site."
            : "No decision recorded in this browser.";
        }
        if (window.crispTrack) {
          window.crispTrack("suggestion_decide", { suggestion_id: id, state: read()[id] || "cleared" });
        }
      });
    });
  });

  // Guide read depth.
  var endMarker = document.getElementById("guide-end");
  if (endMarker && "IntersectionObserver" in window && window.crispTrack) {
    var fired = false;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting && !fired) {
          fired = true;
          window.crispTrack("guide_read", { guide_id: endMarker.getAttribute("data-guide") });
          io.disconnect();
        }
      });
    }, { threshold: 0.5 });
    io.observe(endMarker);
  }
})();
