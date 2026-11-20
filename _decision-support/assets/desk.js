/* Good Measure Kitchen · Decision Desk behaviour.
   Progressive enhancement only: every table and page is fully readable with JS disabled.
   No network calls, no analytics, no cookies. Decisions live in this browser only (localStorage). */
(function () {
  "use strict";

  /* Numeric cell detection: only clean numbers, currency, percentages and simple units. */
  function num(s) {
    if (!/^[-+$]?[\d,]+(\.\d+)?\s?(%|x|min|hrs?|days?|wks?)?$/.test(s)) return null;
    var v = parseFloat(s.replace(/[$,]/g, ""));
    return isNaN(v) ? null : v;
  }

  /* ---------- sortable tables ---------- */
  function sortable(table) {
    var heads = table.querySelectorAll("thead th");
    Array.prototype.forEach.call(heads, function (th, idx) {
      if (th.dataset.nosort === "") return;
      th.tabIndex = 0;
      th.setAttribute("role", "columnheader");
      th.addEventListener("click", function () { apply(th, idx, table); });
      th.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); apply(th, idx, table); }
      });
    });
  }
  function apply(th, idx, table) {
    var asc = th.getAttribute("aria-sort") === "ascending";
    Array.prototype.forEach.call(table.querySelectorAll("thead th"), function (h) {
      h.removeAttribute("aria-sort"); h.classList.remove("sorted-asc", "sorted-desc");
    });
    th.setAttribute("aria-sort", asc ? "descending" : "ascending");
    th.classList.add(asc ? "sorted-desc" : "sorted-asc");
    var body = table.tBodies[0]; if (!body) return;
    var rows = Array.prototype.slice.call(body.rows).filter(function (r) { return r.cells.length > idx; });
    rows.sort(function (a, b) {
      var x = a.cells[idx].textContent.trim(), y = b.cells[idx].textContent.trim();
      var nx = num(x), ny = num(y);
      if (nx !== null && ny !== null) return asc ? ny - nx : nx - ny;
      return asc ? x.localeCompare(y) : y.localeCompare(x);
    });
    rows.forEach(function (r) { body.appendChild(r); });
  }

  /* ---------- search + segmented filters ---------- */
  function toolbar(root) {
    var search = root.querySelector("[data-filter-search]");
    var segs = root.querySelectorAll("[data-filter-group]");
    var out = root.querySelector("[data-filter-count]");
    var table = root.querySelector("[data-filterable]");
    if (!table) return;
    var rows = Array.prototype.slice.call(table.tBodies[0].rows);
    function refresh() {
      var q = search && search.value ? search.value.toLowerCase() : "";
      var active = {};
      Array.prototype.forEach.call(segs, function (g) {
        var on = g.querySelector('[aria-pressed="true"]');
        if (on) active[g.dataset.filterGroup] = on.dataset.value || "all";
      });
      var shown = 0;
      rows.forEach(function (r) {
        var ok = true;
        if (q && r.textContent.toLowerCase().indexOf(q) === -1) ok = false;
        Object.keys(active).forEach(function (key) {
          if (active[key] === "all") return;
          var vals = (r.getAttribute("data-" + key) || "").split(" ");
          if (vals.indexOf(active[key]) === -1) ok = false;
        });
        r.hidden = !ok; if (ok) shown++;
      });
      if (out) out.textContent = shown + " of " + rows.length + " rows shown";
    }
    if (search) search.addEventListener("input", refresh);
    Array.prototype.forEach.call(segs, function (g) {
      Array.prototype.forEach.call(g.querySelectorAll("button"), function (b) {
        b.addEventListener("click", function () {
          Array.prototype.forEach.call(g.querySelectorAll("button"), function (o) {
            o.setAttribute("aria-pressed", String(o === b));
          });
          refresh();
        });
      });
    });
    refresh();
  }

  /* ---------- decision board (this browser only) ---------- */
  var KEY = "gmk-desk-decisions-v1";
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) { /* private mode: decisions simply are not remembered */ } }
  function board(root) {
    var table = root.querySelector("[data-board]"); if (!table) return;
    var store = load();
    Array.prototype.forEach.call(table.querySelectorAll("tbody tr"), function (row) {
      var id = row.dataset.id; if (!id) return;
      var cell = row.querySelector("[data-decide]"); if (!cell) return;
      Array.prototype.forEach.call(cell.querySelectorAll("button"), function (btn) {
        if (store[id] === btn.dataset.choice) btn.classList.add("on");
        btn.addEventListener("click", function () {
          var same = store[id] === btn.dataset.choice;
          if (same) { delete store[id]; } else { store[id] = btn.dataset.choice; }
          Array.prototype.forEach.call(cell.querySelectorAll("button"), function (o) {
            o.classList.toggle("on", !same && o === btn);
          });
          save(store); paint(root, table);
        });
      });
    });
    paint(root, table);
    var exp = root.querySelector("[data-export]");
    if (exp) exp.addEventListener("click", function () { exportBoard(table, store); });
    var clr = root.querySelector("[data-clear]");
    if (clr) clr.addEventListener("click", function () {
      store = {}; save(store);
      Array.prototype.forEach.call(table.querySelectorAll("[data-decide] button"), function (b) { b.classList.remove("on"); });
      paint(root, table);
    });
  }
  function paint(root, table) {
    var counts = { adopt: 0, park: 0, reject: 0, open: 0 };
    Array.prototype.forEach.call(table.querySelectorAll("tbody tr"), function (row) {
      var id = row.dataset.id; if (!id) return;
      var v = load()[id];
      if (v) { counts[v] = (counts[v] || 0) + 1; row.dataset.decided = v; } else { counts.open++; row.removeAttribute("data-decided"); }
    });
    var total = counts.adopt + counts.park + counts.reject + counts.open;
    var bar = root.querySelector("[data-meter] i.p-adopt");
    if (bar) {
      root.querySelector("[data-meter] .p-adopt").style.flex = counts.adopt || 0;
      root.querySelector("[data-meter] .p-park").style.flex = counts.park || 0;
      root.querySelector("[data-meter] .p-reject").style.flex = counts.reject || 0;
    }
    Array.prototype.forEach.call(root.querySelectorAll("[data-count]"), function (el) {
      var k = el.getAttribute("data-count");
      el.textContent = k === "total" ? total : (counts[k] || 0);
    });
  }
  function exportBoard(table, store) {
    var lines = ["# Decision desk — your selections", "",
      "Exported " + new Date().toISOString().slice(0, 10) + " from this browser. Nothing was uploaded.", ""];
    Array.prototype.forEach.call(table.querySelectorAll("tbody tr"), function (row) {
      var id = row.dataset.id; if (!id) return;
      var title = row.dataset.title || (row.cells[1] ? row.cells[1].textContent.trim() : id);
      var why = row.dataset.why || "";
      lines.push("- **" + id + " " + title + "** — " + (store[id] ? store[id].toUpperCase() : "unselected") + (why ? " · " + why : ""));
    });
    var blob = new Blob([lines.join("\n")], { type: "text/markdown" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "gmk-decision-desk.md";
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 400);
  }

  /* ---------- boot ---------- */
  document.querySelectorAll("table[data-sortable]").forEach(sortable);
  document.querySelectorAll("[data-panel]").forEach(function (p) { toolbar(p); board(p); });
})();
