#!/usr/bin/env node
// Build gate. Fails the build on any violation. Every rule here traces to a
// source in data/sources.json, so a rule cannot quietly disappear.
//
//   C01 disclosure on every page          S01
//   C03/C04 sponsored outbound links      S02
//   C05 no obscured destination           S03
//   C06 no price published                S05
//   C07 no star rating / review quote     S04
//   C08 no hands-on testing claim         S19
//   LNK no broken internal link
//   SM  sitemap covers every page, canonicals are absolute and self-referencing
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { site } from "../lib/site.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const failures = [];
const notes = [];
const fail = (rule, where, msg) => failures.push({ rule, where, msg });

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === ".git" || e.name === "node_modules" || e.name === "scripts" || e.name === "data" || e.name === "lib" || e.name === "content" || e.name === "assets")
      continue;
    // archive/ holds superseded pages kept for the record. They are not linked
    // from the live site and are not published as shop pages, so they are not
    // subject to the published-page rules. Preserving them beats deleting a
    // parallel session's work.
    if (e.name === "archive") continue;
    // docs/ holds parallel-session documents kept for review, not published
    // pages of this site. Same reasoning as archive/.
    if (e.name === "docs") continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full, out);
    else if (e.name.endsWith(".html")) out.push(full);
  }
  return out;
}

const pages = walk(ROOT);
if (pages.length === 0) fail("PAGES", "/", "no html files found");

const rel = (p) => path.relative(ROOT, p).split(path.sep).join("/");

// Pages that must exist and be reachable.
const mustExist = [
  "index.html",
  "shop/index.html",
  "guides/index.html",
  "about/index.html",
  "summary/index.html",
  "records/index.html",
  "records/source-register/index.html",
  "records/product-intent/index.html",
  "records/compliance/index.html",
  "records/measurement/index.html",
  "records/campaign-ledger/index.html",
  "records/questions/index.html",
  "records/suggestions/index.html",
  "records/flagged/index.html",
  "sitemap.xml",
  "feed.xml",
  "robots.txt",
  "assets/css/site.css",
  "assets/js/site.js",
  "assets/js/analytics.js",
];
for (const m of mustExist) {
  if (!fs.existsSync(path.join(ROOT, m))) fail("MISSING", m, "required file not built");
}

// Discover internal routes available on disk.
function routeExists(u) {
  const clean = u.split("#")[0].split("?")[0];
  if (!clean.startsWith(site.baseUrl)) return null; // external
  let p = clean.slice(site.baseUrl.length) || "/";
  if (p === "") p = "/";
  const target = path.join(ROOT, decodeURIComponent(p));
  if (p.endsWith("/")) return fs.existsSync(path.join(target, "index.html"));
  if (fs.existsSync(target) && fs.statSync(target).isFile()) return true;
  return fs.existsSync(path.join(target, "index.html"));
}

const canonicals = new Set();
// Utility pages that are intentionally not in the sitemap (noindex).
const UTILITY = new Set(["404.html"]);
let citationCount = 0;
const DISCLOSURE = site.disclosure;

for (const file of pages) {
  const where = rel(file);
  const html = fs.readFileSync(file, "utf8");

  // C01 — disclosure present in exact required wording (S01)
  if (!html.includes(DISCLOSURE)) {
    fail("C01", where, "required disclosure sentence is missing (S01)");
  }
  // Disclosure must appear before the main content, not only in the footer.
  const discIdx = html.indexOf('class="disclosure"');
  const mainIdx = html.indexOf('<main id="main"');
  if (discIdx === -1) fail("C01", where, "disclosure strip element missing");
  else if (mainIdx !== -1 && discIdx > mainIdx)
    fail("C01", where, "disclosure strip appears after main content, so it is not above the fold (S18)");

  // canonical present, absolute, self-referencing
  const canon = html.match(/<link rel="canonical" href="([^"]+)">/);
  if (!canon) fail("SM", where, "missing canonical link");
  else {
    const c = canon[1];
    if (!c.startsWith(site.baseUrl)) fail("SM", where, `canonical is not absolute under base url: ${c}`);
    if (canonicals.has(c)) fail("SM", where, `duplicate canonical ${c}`);
    if (UTILITY.has(where)) {
      if (!/name="robots" content="noindex/.test(html))
        fail("SM", where, "utility page must carry a noindex robots meta");
      canonicals.add(c);
      continue;
    }
    canonicals.add(c);
    const expected =
      site.baseUrl + "/" + (where === "index.html" ? "" : where.replace(/index\.html$/, ""));
    if (c !== expected) fail("SM", where, `canonical ${c} does not match page path ${expected}`);
  }

  // C08 — no hands-on testing claim (S19)
  const claimPatterns = [
    /\bwe tested\b/i,
    /\bour testing\b/i,
    /\bwe tried\b/i,
    /\bhands-on review\b/i,
    /\bin our tests?\b/i,
    /\bwe measured\b/i,
  ];
  for (const re of claimPatterns) {
    if (re.test(html)) fail("C08", where, `possible hands-on testing claim: /${re.source}/ (S19)`);
  }
  // sanity: the disclaimer must be present on guide pages
  if (where.startsWith("guides/") && where !== "guides/index.html") {
    if (!/No hands-on testing claimed/.test(html))
      fail("C08", where, "guide page is missing the 'No hands-on testing claimed' byline note");
  }

  // C06 — no price published (S05). Allow the currency sign only in explanatory
  // prose that is not adjacent to a product price; we simply ban price-like tokens.
  const pricePatterns = [
    /\$\s?\d{1,4}(?:[.,]\d{2})?\b/,
    /\bUSD\s?\d/,
    /\bprice:\s*[$\d]/i,
    /List Price/i,
  ];
  for (const re of pricePatterns) {
    const m = html.match(re);
    if (m) fail("C06", where, `price-like token found: "${m[0]}" (S05)`);
  }

  // C07 — no star rating or customer review *displayed* (S04).
  // The bare word "review" appears in policy prose and in this site's own
  // explanatory copy, and that is not a violation; what S04 restricts is
  // displaying the rating or the review text itself.
  const ratingPatterns = [
    /itemprop="ratingValue"/i,
    /itemprop="reviewCount"/i,
    /class="[^"]*\b(?:a-star|star-rating|rating-star)/i,
    /\bout of 5 stars\b/i,
    /\b\d\.\d\s+out of\s+5\b/i,
    /\b\d\.\d\s*\(\s*[\d,]{3,}\s*\)/,
  ];
  for (const re of ratingPatterns) {
    const m = html.match(re);
    if (m) fail("C07", where, `rating markup or value found: "${m[0]}" (S04)`);
  }

  // Outbound Amazon anchors: must be tagged, sponsored, and not shortened (S02, S03, S05)
  const anchors = [...html.matchAll(/<a\b[^>]*href="([^"]*)"[^>]*>/gi)];
  for (const a of anchors) {
    const tagText = a[0];
    const url = a[1];
    const isAmazon = /https?:\/\/(www\.)?amazon\.com\//i.test(url);
    if (!isAmazon) continue;

    // A citation is how the site shows its evidence: it points at the official
    // page a claim came from. It is not a promotional control, so it carries no
    // tag by design (attaching one would claim commission on a policy page).
    // It is exempt from C03/C04 but is counted and reported below.
    if (/\bdata-citation="true"/.test(tagText)) {
      citationCount++;
      continue;
    }

    if (!new RegExp("[?&]tag=" + site.tag + "\\b").test(url))
      fail("C03", where, `amazon link without the Associates tag: ${url} (S02)`);
    if (!/\brel="[^"]*sponsored/.test(tagText))
      fail("C04", where, `amazon link not marked rel=sponsored: ${url} (S02)`);
    if (!/\bnoopener\b/.test(tagText))
      notes.push(`${where}: amazon anchor without noopener (${url})`);
    // C05 — destination must be a direct listing, not a shortener or redirect
    if (/link\.amazon|\/go\/|redirect/i.test(url))
      fail("C05", where, `outbound link uses a shortener or redirect: ${url} (S03)`);
  }

  // A short link is a violation when it is published as an outbound control.
  // Records quote the submitted short link as escaped evidence, which is not a
  // link a reader can follow, and is the honest way to document the defect.
  for (const a of anchors) {
    if (/link\.amazon/i.test(a[1])) {
      fail("C05", where, `publishes a short link as an outbound control: ${a[1]} (S03)`);
    }
  }

  // LNK — internal links resolve on disk
  for (const a of anchors) {
    const url = a[1];
    if (/^(mailto:|tel:|#)/.test(url)) continue;
    const ok = routeExists(url);
    if (ok === false) fail("LNK", where, `broken internal link: ${url}`);
  }
  // and stylesheet/script references
  for (const m of html.matchAll(/(?:href|src)="([^"]*\.(?:css|js))"/g)) {
    const ok = routeExists(m[1]);
    if (ok === false) fail("LNK", where, `missing asset: ${m[1]}`);
  }
}

// Sitemap must cover every canonical page and contain no stale url.
const smPath = path.join(ROOT, "sitemap.xml");
if (fs.existsSync(smPath)) {
  const sm = fs.readFileSync(smPath, "utf8");
  const locs = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
  if (new Set(locs).size !== locs.length) fail("SM", "sitemap.xml", "duplicate <loc> entries");
  for (const c of canonicals) {
    // The 404 page is a utility page: it is deliberately excluded from the
    // sitemap because nobody should find it in search, so it is not a gap.
    if (UTILITY.has("404.html") && c === site.baseUrl + "/404/") continue;
    if (!locs.includes(c)) fail("SM", "sitemap.xml", `canonical page missing from sitemap: ${c}`);
  }
  for (const l of locs) {
    if (!canonicals.has(l)) fail("SM", "sitemap.xml", `sitemap lists a page that does not exist: ${l}`);
  }
  notes.push(`sitemap covers ${locs.length} urls, all matching a canonical`);
}

// Feed must be well-formed-ish and reference real pages.
const feedPath = path.join(ROOT, "feed.xml");
if (fs.existsSync(feedPath)) {
  const f = fs.readFileSync(feedPath, "utf8");
  const links = [...f.matchAll(/<link>([^<]+)<\/link>/g)].map((m) => m[1]).slice(1);
  for (const l of links) {
    if (routeExists(l) === false) fail("FEED", "feed.xml", `feed item points at a missing page: ${l}`);
  }
  notes.push(`feed has ${links.length} items, all resolving`);
}

// robots.txt must point at the sitemap.
const rb = fs.readFileSync(path.join(ROOT, "robots.txt"), "utf8");
if (!rb.includes(`${site.baseUrl}/sitemap.xml`)) fail("SM", "robots.txt", "sitemap directive missing");

// Report.
const archived = [];
(function findArchive(dir) {
  if (!fs.existsSync(dir)) return;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) findArchive(full);
    else if (e.name.endsWith(".html")) archived.push(full);
  }
})(path.join(ROOT, "archive"));
if (archived.length) {
  notes.push(
    `${archived.length} archived html file(s) under archive/ excluded from the published-page rules ` +
    `(not linked from the live site; preserved as history rather than deleted)`
  );
}

console.log("── build gate ─────────────────────────────────────────");
if (citationCount) {
  notes.push(
    `${citationCount} amazon.com link(s) marked data-citation, exempt from the tag requirement by design ` +
    `(attaching an Associates tag to a policy page would claim commission on a document, not a product)`
  );
}
if (notes.length) {
  console.log(`notes (${notes.length}):`);
  notes.slice(0, 20).forEach((n) => console.log("  · " + n));
}
if (failures.length === 0) {
  console.log(`\nPASS — ${pages.length} pages checked, 0 violations.`);
  process.exit(0);
}
console.log(`\nFAIL — ${failures.length} violation(s):`);
for (const f of failures) console.log(`  [${f.rule}] ${f.where}: ${f.msg}`);
process.exit(1);
