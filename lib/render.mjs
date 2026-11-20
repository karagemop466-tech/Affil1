// Rendering primitives shared by every page.
import { site, nav, footerGroups } from "./site.mjs";

const esc = (s) =>
  String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

export { esc };

export function abs(path) {
  if (/^https?:\/\//.test(path)) return path;
  return site.baseUrl + (path.startsWith("/") ? path : "/" + path);
}

// Internal href: base-path aware, always trailing-slash for directories.
export function href(path) {
  if (/^https?:/.test(path)) return path;
  if (path === "/feed.xml" || path === "/sitemap.xml" || path === "/robots.txt")
    return `${site.baseUrl}${path}`;
  if (path.startsWith("#")) return path;
  return `${site.baseUrl}${path}`;
}

function navMarkup(current) {
  return nav
    .map(
      (n) =>
        `<a href="${esc(href(n.href))}"${
          current === n.key ? ' aria-current="page"' : ""
        }>${esc(n.label)}</a>`
    )
    .join("");
}

function footerMarkup() {
  const groups = footerGroups
    .map(
      (g) => `<div>
        <h4>${esc(g.title)}</h4>
        <ul>${g.links
          .map((l) => `<li><a href="${esc(href(l.href))}">${esc(l.label)}</a></li>`)
          .join("")}</ul>
      </div>`
    )
    .join("");

  return `<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="${esc(href("/"))}">
          <span class="brand-mark">The <em>Crisp</em> Counter</span>
        </a>
        <p>${esc(site.tagline)} A small, honest shop for kitchen tools &mdash; organised by what you cook, not by what is on offer.</p>
      </div>
      ${groups}
    </div>
    <div class="footer-disclosure">
      <strong>${esc(site.disclosure)}</strong>
      Every outbound product link on this site is a sponsored affiliate link and is marked as such, with the destination listing named on the control.
      This site does not publish prices, star ratings, or review quotes, and makes no claim to have tested any product.
      Product details are quoted from the Amazon listing titles and feature text and are linked to their source on each page.
      <div class="footer-meta">
        <span>Associates ID ${esc(site.tag)}</span>
        <span>Records verified 2026-11-20</span>
        <span><a href="${esc(href("/records/"))}">All records</a></span>
        <span><a href="${esc(href("/feed.xml"))}">RSS</a></span>
      </div>
    </div>
  </div>
</footer>`;
}

/**
 * Renders a full page.
 * @param {object} o
 * @param {string} o.title        <title> text
 * @param {string} o.description  meta description
 * @param {string} o.path         canonical path, e.g. "/shop/"
 * @param {string} o.body         main content HTML
 * @param {string} [o.current]    nav key to mark current
 * @param {string} [o.bodyClass]
 * @param {boolean} [o.noindex]
 * @param {object[]} [o.jsonLd]   structured-data objects (JSON-LD)
 * @param {string} [o.ogImage]    absolute image URL for og:image / twitter
 */
export function page({ title, description, path, body, current = "", bodyClass = "", noindex = false, jsonLd = [], ogImage = "" }) {
  const canonical = abs(path);
  const image = ogImage || abs("/assets/img/hero-kitchen.jpg");
  const ld = jsonLd.length
    ? `\n<script type="application/ld+json">${JSON.stringify(jsonLd).replace(/</g, "\\u003c")}</script>`
    : "";
  return `<!doctype html>
<html lang="${esc(site.language)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(description)}">
<link rel="canonical" href="${esc(canonical)}">
${noindex ? '<meta name="robots" content="noindex, follow">' : '<meta name="robots" content="index, follow, max-image-preview:large">'}
<meta property="og:type" content="website">
<meta property="og:site_name" content="${esc(site.brand)}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:url" content="${esc(canonical)}">
<meta property="og:image" content="${esc(image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="${esc(image)}">${ld}
<link rel="alternate" type="application/rss+xml" title="${esc(site.brand)} &mdash; guides and new products" href="${esc(href("/feed.xml"))}">
<link rel="stylesheet" href="${esc(href("/assets/css/site.css"))}">
</head>
<body class="${esc(bodyClass)}">
<a class="skip" href="#main">Skip to content</a>

<header class="masthead">
  <div class="wrap masthead-inner">
    <a class="brand" href="${esc(href("/"))}">
      <span class="brand-mark">The <em>Crisp</em> Counter</span>
      <span class="brand-kicker">Kitchen tools</span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">${navMarkup(current)}</nav>
  </div>
</header>

<!-- Disclosure strip: directly under the masthead, present on every page. S01 / S18. -->
<div class="disclosure" role="complementary" aria-label="Affiliate disclosure">
  <div class="wrap">
    <span class="disclosure-badge">Sponsored links</span>
    <span>${esc(site.disclosure)} Outbound product links go to Amazon and are affiliate links. <a href="${esc(href("/about/#disclosure"))}">How this works</a></span>
  </div>
</div>

<main id="main">
${body}
</main>

${footerMarkup()}

<script src="${esc(href("/assets/js/site.js"))}" defer></script>
<script src="${esc(href("/assets/js/analytics.js"))}" defer></script>
</body>
</html>
`;
}

/** Outbound sponsored control. Always names its destination. */
export function outbound({ asin, productId, placement, label = "View the listing on Amazon" }) {
  const hrefAmazon = `https://www.amazon.com/dp/${asin}?tag=${site.tag}`;
  return `<a class="btn-out" href="${esc(hrefAmazon)}" rel="sponsored nofollow noopener" target="_blank"
     data-event="outbound_click" data-product="${esc(productId)}" data-placement="${esc(placement)}"
     aria-label="${esc(label)} (opens amazon.com in a new tab)">
    <span class="dot" aria-hidden="true"></span>${esc(label)}
  </a>`;
}

export function sponsorNote() {
  return `<span class="sponsor-note">Paid link &middot; Amazon</span>`;
}

export function breadcrumbs(trail) {
  const parts = trail
    .map((t, i) =>
      i === trail.length - 1
        ? `<span aria-current="page">${esc(t.label)}</span>`
        : `<a href="${esc(href(t.href))}">${esc(t.label)}</a><span aria-hidden="true">/</span>`
    )
    .join("");
  return `<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">${parts}</nav></div>`;
}

export function pageHead({ h1, lede }) {
  return `<div class="page-head"><div class="wrap"><h1>${h1}</h1>${lede ? `<p>${lede}</p>` : ""}</div></div>`;
}

export function badge(text, kind) {
  return `<span class="badge badge-${kind}">${esc(text)}</span>`;
}

/**
 * Citation link to an official source. Marked data-citation so the build gate
 * can tell a reference apart from an outbound product control: a citation is
 * evidence for a claim, not a sponsored product link, and must not carry a tag.
 */
export function srcLink(id, url) {
  return `<a class="src-link" href="${esc(url)}" rel="noopener" target="_blank" data-citation="true">${esc(id)}&nbsp;&#8599;</a>`;
}

/** Escapes then preserves nothing; use for trusted HTML fragments only. */
export function raw(s) {
  return s;
}
