/* Good Measure Kitchen - interaction layer.
 *
 * Progressive enhancement only: every page works with this file blocked.
 */
(function () {
  'use strict';

  /* ------------------------------------------------------------------ mobile nav */
  var toggle = document.querySelector('.nav-toggle');
  var mobileNav = document.getElementById('mobile-nav');
  if (toggle && mobileNav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', open ? 'false' : 'true');
      toggle.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
      mobileNav.hidden = open;
    });
  }

  /* --------------------------------------------------------------- table filter */
  var filter = document.getElementById('shop-filter');
  var table = document.getElementById('shop-table');
  if (filter && table) {
    var rows = Array.prototype.slice.call(table.tBodies[0].rows);
    filter.addEventListener('input', function () {
      var q = filter.value.trim().toLowerCase();
      rows.forEach(function (row) {
        var text = (row.textContent || '').toLowerCase();
        row.style.display = !q || text.indexOf(q) !== -1 ? '' : 'none';
      });
    });
  }

  /* --------------------------------------------- sponsored marking safety net ---- */
  /* Every outbound product link must say it is a paid placement. The publishing gate
     fails the build if this is not true in the markup; this is the runtime backstop
     for content pasted in later. */
  var AMZON_HOSTS = ['amazon.com', 'link.amazon', 'amzn.to', 'a.co', 'amzn.eu', 'amzn.asia'];
  function isAmazonHost(href) {
    try {
      var host = new URL(href, window.location.href).hostname;
      for (var i = 0; i < AMZON_HOSTS.length; i++) {
        if (host === AMZON_HOSTS[i] || host.endsWith('.' + AMZON_HOSTS[i])) return true;
      }
    } catch (e) { /* ignore */ }
    return false;
  }
  var links = document.querySelectorAll('a[href]');
  for (var i = 0; i < links.length; i++) {
    var a = links[i];
    var href = a.getAttribute('href') || '';
    if (!/^https?:/i.test(href)) continue;
    if (!isAmazonHost(href)) continue;
    var rel = (a.getAttribute('rel') || '').split(/\s+/).filter(Boolean);
    if (rel.indexOf('sponsored') === -1) rel.unshift('sponsored');
    if (rel.indexOf('nofollow') === -1) rel.push('nofollow');
    if (rel.indexOf('noopener') === -1) rel.push('noopener');
    a.setAttribute('rel', rel.join(' '));
  }

  /* ------------------------------------------------------- ledger report import */
  /* The campaign ledger may only be filled from an authorised first-party report.
     This control accepts a CSV whose header row matches the ledger schema exactly.
     Anything else is refused, and nothing is invented. */
  var fileInput = document.getElementById('report-file');
  var importButton = document.getElementById('report-import');
  var status = document.getElementById('report-status');
  var ledgerTable = document.querySelector('.ledger-table');

  var LEDGER_HEADERS = ['Date', 'Source', 'Channel', 'Eligible sessions', 'Clicks',
                        'Reported orders', 'Provenance', 'Logged by'];

  function setStatus(text, ok) {
    if (!status) return;
    status.textContent = text;
    status.className = 'ledger-status' + (ok ? ' ok' : '');
  }

  function parseCsv(text) {
    var rows = [];
    var row = [];
    var field = '';
    var inQuotes = false;
    for (var i = 0; i < text.length; i++) {
      var ch = text[i];
      if (inQuotes) {
        if (ch === '"') {
          if (text[i + 1] === '"') { field += '"'; i++; }
          else { inQuotes = false; }
        } else { field += ch; }
      } else if (ch === '"') {
        inQuotes = true;
      } else if (ch === ',') {
        row.push(field); field = '';
      } else if (ch === '\n' || ch === '\r') {
        if (ch === '\r' && text[i + 1] === '\n') i++;
        row.push(field); field = '';
        rows.push(row); row = [];
      } else { field += ch; }
    }
    if (field.length || row.length) { row.push(field); rows.push(row); }
    return rows.filter(function (r) {
      return r.length && r.join('').trim().length;
    });
  }

  function appendRow(values) {
    if (!ledgerTable) return;
    var tbody = ledgerTable.tBodies[0];
    var empty = tbody.querySelector('.ledger-empty');
    if (empty) empty.parentNode.removeChild(empty);
    var tr = document.createElement('tr');
    values.forEach(function (v) {
      var td = document.createElement('td');
      td.textContent = v;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  }

  if (fileInput && importButton) {
    importButton.addEventListener('click', function () {
      var file = fileInput.files && fileInput.files[0];
      if (!file) {
        setStatus('No report file chosen. Nothing was imported.');
        return;
      }
      var reader = new FileReader();
      reader.onload = function () {
        var rows = parseCsv(String(reader.result || ''));
        if (!rows.length) {
          setStatus('That file has no rows. Nothing was imported.');
          return;
        }
        var header = rows[0].map(function (h) { return h.trim(); });
        var mismatch = header.length !== LEDGER_HEADERS.length ||
          header.some(function (h, idx) { return h !== LEDGER_HEADERS[idx]; });
        if (mismatch) {
          setStatus('Refused. The header row must be exactly: ' +
            LEDGER_HEADERS.join(', ') + '. Nothing was imported.');
          return;
        }
        var imported = 0;
        rows.slice(1).forEach(function (r) {
          var values = LEDGER_HEADERS.map(function (_, idx) { return (r[idx] || '').trim(); });
          if (!values[0]) return;
          appendRow(values);
          imported++;
        });
        if (!imported) {
          setStatus('No rows with a date were found. Nothing was imported.');
          return;
        }
        var payload = {
          report: file.name,
          period: rows[1][0].trim(),
          rows: imported
        };
        var tracked = false;
        if (window.GMAnalytics && window.GMAnalytics.track) {
          tracked = window.GMAnalytics.track('report_import', payload);
        }
        setStatus('Imported ' + imported + ' row' + (imported === 1 ? '' : 's') +
          ' from ' + file.name + '. Provenance recorded.' +
          (tracked ? '' : ' The collector is not deployed, so no report_import event was sent.'), true);
      };
      reader.onerror = function () {
        setStatus('That file could not be read. Nothing was imported.');
      };
      reader.readAsText(file);
    });
  }
})();
