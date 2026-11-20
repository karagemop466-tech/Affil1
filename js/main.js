/*! Affil1 — main.js
   Navigation toggle, disclosure strip, outbound-click instrumentation,
   sponsored-link marking, and accessibility helpers. */

(function () {
  'use strict';

  // ---------- Constants ----------
  const DISCLOSURE_TEXT =
    'Disclosure: As an Amazon Associate, we earn from qualifying purchases. ' +
    'This site contains affiliate links marked "sponsored." Learn more about our ' +
    'affiliate disclosure.';
  const _depth = Math.max(0, location.pathname.split('/').filter(Boolean).length - 2);
  const DISCLOSURE_LINK = (_depth ? '../'.repeat(_depth) : '') + 'disclosure.html';

  // ---------- Disclosure strip (above the fold, every page) ----------
  function ensureDisclosure() {
    if (document.querySelector('.disclosure-strip')) return;
    const strip = document.createElement('div');
    strip.className = 'disclosure-strip';
    strip.innerHTML =
      '<div class="inner">' +
      '<span aria-label="Affiliate disclosure" role="img" aria-hidden="true">&#128226;</span>' +
      '<b>Affiliate disclosure:</b> ' + DISCLOSURE_TEXT + ' ' +
      '<a href="' + DISCLOSURE_LINK + '">Read full disclosure &#8594;</a>' +
      '</div>';
    document.body.insertBefore(strip, document.body.firstChild);
  }

  // ---------- Navigation toggle ----------
  function initNav() {
    const toggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.primary-nav');
    if (!toggle || !nav) return;
    toggle.addEventListener('click', function () {
      const open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    // Close nav when a link is clicked
    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
    // Highlight current page
    const current = location.pathname.split('/').pop() || 'index.html';
    nav.querySelectorAll('a').forEach(function (link) {
      const href = link.getAttribute('href');
      if (href && (href === current || (current !== 'index.html' && href === current))) {
        link.classList.add('active');
      }
    });
  }

  // ---------- Sponsored outbound-link handling ----------
  // Every outbound affiliate/product link carries rel="sponsored" and data-affiliate="1".
  // On click we record an outbound_click event (self-hosted analytics), then allow navigation.
  function initOutboundLinks() {
    document.addEventListener('click', function (event) {
      const link = event.target.closest('a[rel="sponsored"], a[data-affiliate="1"]');
      if (!link) return;
      const href = link.getAttribute('href');
      if (!href) return;
      const isOutbound = href.startsWith('http') &&
        new URL(href).hostname !== location.hostname;
      if (!isOutbound) return;

      // Record the outbound click before navigation (best effort, non-blocking).
      try {
        if (window.affil1Analytics) {
          window.affil1Analytics.record('outbound_click', {
            target: href,
            linkText: (link.textContent || '').trim().slice(0, 120),
            element: link.getAttribute('data-affiliate-label') || '',
          });
        }
      } catch (e) {
        // Analytics must never break navigation.
      }
    }, { passive: true });

    // Annotate outbound links visually as sponsored and mark rel.
    document.querySelectorAll('a[href]').forEach(function (link) {
      const href = link.getAttribute('href');
      if (!href) return;
      try {
        const isOutbound = href.startsWith('http') &&
          new URL(href).hostname !== location.hostname;
        if (isOutbound) {
          link.setAttribute('rel', (link.getAttribute('rel') || '') + ' sponsored nofollow');
          link.setAttribute('data-affiliate', '1');
          if (!link.querySelector('.sponsored-tag')) {
            const tag = document.createElement('span');
            tag.className = 'sponsored-tag';
            tag.setAttribute('aria-hidden', 'true');
            tag.textContent = 'sponsored';
            link.style.position = 'relative';
            link.appendChild(tag);
          }
        }
      } catch (e) { /* ignore malformed URLs */ }
    });
  }

  // ---------- Sponsored tag styles ----------
  function injectSponsoredStyles() {
    if (document.getElementById('affil1-sponsored-styles')) return;
    const style = document.createElement('style');
    style.id = 'affil1-sponsored-styles';
    style.textContent =
      '.sponsored-tag{' +
      'position:absolute;top:-10px;right:-8px;' +
      'font-size:9px;font-weight:800;letter-spacing:0.5px;' +
      'color:#fff;background:#f59e0b;border-radius:999px;padding:1px 6px;' +
      'box-shadow:0 1px 2px rgb(0 0 0 / 0.15);' +
      '}' +
      'a[rel="sponsored"]{color:inherit;}' +
      'a[rel="sponsored"]:hover{text-decoration:underline;}';
    document.head.appendChild(style);
  }

  // ---------- Boot ----------
  function boot() {
    ensureDisclosure();
    injectSponsoredStyles();
    initNav();
    initOutboundLinks();
    if (window.affil1Analytics) {
      window.affil1Analytics.record('page_view', { path: location.pathname });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  // Expose for analytics module
  window.affil1Boot = boot;
})();
