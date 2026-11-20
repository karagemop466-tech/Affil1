/* Crisp & Counter — saved shortlist.
 *
 * The one interactive feature on this site, chosen because it needs no server,
 * no account and no data collection: it writes a list of product ids into
 * localStorage in this browser and nowhere else. Nothing is transmitted. If the
 * reader clears site data, it is gone — which is the correct privacy posture for
 * a "come back later" affordance on a static page.
 */
(function () {
  "use strict";

  var KEY = "cc.shortlist.v1";

  function read() {
    try {
      var raw = window.localStorage.getItem(KEY);
      var arr = raw ? JSON.parse(raw) : [];
      return Array.isArray(arr) ? arr : [];
    } catch (err) {
      return []; // private mode, quota, or malformed JSON: the page still works.
    }
  }

  function write(list) {
    try {
      window.localStorage.setItem(KEY, JSON.stringify(list));
    } catch (err) { /* ignored by design */ }
  }

  function init() {
    var list = read();
    var buttons = Array.prototype.slice.call(document.querySelectorAll("[data-save]"));
    if (!buttons.length && !document.getElementById("saved-list")) { return; }

    function paint() {
      buttons.forEach(function (b) {
        var on = list.indexOf(b.getAttribute("data-save")) !== -1;
        b.setAttribute("aria-pressed", on ? "true" : "false");
        b.textContent = on ? "Saved" : "Save";
      });
      var panel = document.getElementById("saved-list");
      if (panel) {
        panel.hidden = list.length === 0;
        var n = panel.querySelector("[data-saved-count]");
        if (n) { n.textContent = String(list.length); }
        var items = panel.querySelector("[data-saved-items]");
        if (items) {
          items.innerHTML = "";
          list.forEach(function (id) {
            var card = document.getElementById(id);
            var label = card ? (card.querySelector("h3") || {}).textContent || id : id;
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.href = "#" + id;
            a.textContent = (label || "").trim().slice(0, 90);
            var x = document.createElement("button");
            x.type = "button";
            x.className = "save-btn";
            x.textContent = "Remove";
            x.addEventListener("click", function () { toggle(id); });
            li.appendChild(a); li.appendChild(x); items.appendChild(li);
          });
        }
      }
      var chips = document.querySelectorAll("[data-saved-total]");
      Array.prototype.forEach.call(chips, function (c) {
        c.textContent = String(list.length);
        c.hidden = list.length === 0;
      });
    }

    function toggle(id) {
      var i = list.indexOf(id);
      if (i === -1) { list.push(id); } else { list.splice(i, 1); }
      write(list);
      paint();
    }

    buttons.forEach(function (b) {
      b.addEventListener("click", function () { toggle(b.getAttribute("data-save")); });
    });
    var clear = document.getElementById("clear-saved");
    if (clear) {
      clear.addEventListener("click", function () { list = []; write(list); paint(); });
    }
    paint();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
