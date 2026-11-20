/* Affil1 — shared shell: masthead, navigation group, disclosure strip (above the fold),
   and footer with all dashboard surfaces repeated. Injected into every page so the
   site reads as one publication, not generated fragments. */

(function () {
  /* Root-relative paths break on GitHub Project Pages (site lives under /<user>/<repo>/).
     Compute a relative root from the current pathname so every injected link works
     from any depth. */
  function siteRoot() {
    var seg = location.pathname.split("/").filter(Boolean);
    var depth = Math.max(0, seg.length - 2); // segments after "<user>/<repo>"
    return depth ? "../".repeat(depth) : "";
  }
  var ROOT = siteRoot();
  window.affil1Root = ROOT;
  function toRoot(href) {
    return href === "/" ? ROOT + "index.html" : ROOT + href.slice(1);
  }

  var NAV = [
    { href: "/", label: "Home" },
    { href: "/categories/air-fryers.html", label: "Air Fryers" },
    { href: "/dashboard.html", label: "Dashboard" },
    { href: "/guides/", label: "Guides" },
    { href: "/suggestions.html", label: "Suggestions" },
    { href: "/reviews/flagged.html", label: "Flagged for Review" },
    { href: "/disclosure.html", label: "Affiliate Disclosure" },
    { href: "/privacy.html", label: "Privacy" },
  ];

  var FOOTER_GROUPS = [
    {
      title: "Shop by category",
      links: [
        { href: "/categories/air-fryers.html", label: "Air fryers" },
        { href: "/dashboard.html", label: "Findings & analysis" },
      ],
    },
    {
      title: "Guides",
      links: [
        { href: "/guides/basket-or-oven.html", label: "Basket or oven-style air fryer" },
        { href: "/guides/capacity-checklist.html", label: "Air fryer capacity checklist" },
        { href: "/guides/cleanup-counter-space.html", label: "Cleanup & counter space" },
        { href: "/guides/multi-function-appliance.html", label: "Multi-function appliances" },
      ],
    },
    {
      title: "Dashboard surfaces",
      links: [
        { href: "/dashboard.html", label: "Product findings table" },
        { href: "/suggestions.html", label: "Decision suggestions" },
        { href: "/reviews/flagged.html", label: "Flagged for review" },
      ],
    },
    {
      title: "Policy & legal",
      links: [
        { href: "/disclosure.html", label: "Affiliate disclosure" },
        { href: "/privacy.html", label: "Privacy" },
        { href: "/sitemap.xml", label: "Sitemap" },
      ],
    },
  ];

  var DISCLOSURE_TEXT =
    "As an Amazon Associate we earn from qualifying purchases. Links marked \u201csponsored\u201d are affiliate links. " +
    "Full statement: affiliate disclosure.";

  function buildHeader(currentPath) {
    var active = function (href) { return currentPath === href || currentPath === href.replace(/\.html$/, "/"); };
    var navLinks = NAV.map(function (n) {
      return '<a href="' + toRoot(n.href) + '"' + (active(n.href) ? ' class="active" aria-current="page"' : "") + '">' + n.label + "</a>";
    }).join("");
    return [
      '<header class="masthead" id="site-masthead"><div class="container">',
      '<a class="brand" href="' + toRoot("/") + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2L3 7l9 5 9-5-9-5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 17L3 22l9-5 9 5-9-5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span class="brand-mark">Affil1</span> <span style="font-weight:400;font-size:0.78rem;color:var(--muted);">shop now</span></a>',
      '<nav class="nav" id="site-nav">' + navLinks + '</nav>',
      '<button class="nav-toggle" id="nav-toggle" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>',
      '</div></header>',
      '<div class="disclosure-strip"><div class="container">',
      '<strong>Affiliate disclosure:</strong> ' + DISCLOSURE_TEXT + '. See the full <a href="' + toRoot("/disclosure.html") + '">affiliate disclosure</a>.',
      '</div></div>'
    ].join("");
  }

  function buildFooter() {
    var groups = FOOTER_GROUPS.map(function (g) {
      var items = g.links.map(function (l) {
        return '<li><a href="' + toRoot(l.href) + '">' + l.label + "</a></li>";
      }).join("");
      return '<div><h4>' + g.title + '</h4><ul>' + items + '</ul></div>';
    }).join("");
    return [
      '<footer class="footer"><div class="container">',
      '<div class="grid">' + groups + '</div>',
      '<div class="disclosure-repeat">',
      '<strong>Affiliate disclosure (repeated):</strong> As an Amazon Associate we earn from qualifying purchases. ' +
      'Links marked <strong>sponsored</strong> are affiliate links. Product findings are not endorsements; ' +
      'see the <a href="' + toRoot("/disclosure.html") + '">full affiliate disclosure</a> and our <a href="' + toRoot("/privacy.html") + '">privacy notice</a>. ' +
      'Associates tracking ID: shopnow047c-20.',
      '</div>',
      '</div></footer>'
    ].join("");
  }

  function init() {
    var path = location.pathname;
    var headerEl = document.getElementById("site-header");
    var footerEl = document.getElementById("site-footer");
    if (headerEl) headerEl.innerHTML = buildHeader(path);
    if (footerEl) footerEl.innerHTML = buildFooter();

    var toggle = document.getElementById("nav-toggle");
    var nav = document.getElementById("site-nav");
    if (toggle && nav) {
      toggle.addEventListener("click", function () {
        var open = nav.classList.toggle("open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      });
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
