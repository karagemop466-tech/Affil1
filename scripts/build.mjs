#!/usr/bin/env node
// Build: renders every page from data + content, then writes sitemap, feed and
// robots. Deterministic output. Writes only into the paths listed in PAGES.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { site, footerGroups } from "../lib/site.mjs";
import { page, outbound, sponsorNote, breadcrumbs, pageHead, badge, srcLink, esc, href, abs } from "../lib/render.mjs";
import { products, heldProduct, categories, productUrl, sponsoredHref } from "../content/products.mjs";
import { guides, guideUrl } from "../content/guides.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const readJSON = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), "utf8"));

const D = {
  sources: readJSON("data/sources.json"),
  intent: readJSON("data/product-intent.json"),
  questions: readJSON("data/questions.json"),
  suggestions: readJSON("data/suggestions.json"),
  ledger: readJSON("data/campaign-ledger.json"),
  events: readJSON("data/events.json"),
};

// Page registry: drives write order, sitemap, and the link checker.
const written = [];
function emit(relPath, html) {
  const full = path.join(ROOT, relPath);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, html, "utf8");
  written.push(relPath);
}

const byId = Object.fromEntries(products.map((p) => [p.id, p]));
const guideById = Object.fromEntries(guides.map((g) => [g.id, g]));

// ---------------------------------------------------------------- front page

function productCard(p, placement) {
  return `<article class="card">
  <div class="card-tagrow">
    <span class="pill">${esc(p.style)}</span>
    <span class="pill pill-accent">${esc(p.brand)}</span>
  </div>
  <h3><a href="${esc(href(productUrl(p)))}">${esc(p.name)}</a></h3>
  <p class="card-hook">${esc(p.hook)}</p>
  <ul class="card-specs">
    ${p.specs.slice(0, 3).map((s) => `<li><span>${esc(s.label)}</span><span>${esc(s.value)}</span></li>`).join("")}
  </ul>
  <div class="card-foot">
    <a class="card-link" href="${esc(href(productUrl(p)))}">Read the breakdown</a>
    ${outbound({ asin: p.asin, productId: p.id, placement, label: "Check it on Amazon" })}
  </div>
</article>`;
}

function frontPage() {
  const lead = byId.P2;
  const shelf = [byId.P1, byId.P3, byId.P5];

  const body = `
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">${esc(site.season.label)} &middot; Issue 01</p>
      <h1>The air fryer question is not <em>which one</em>. It is which <em>kind</em>.</h1>
      <p class="hero-dek">Four kitchen tools, three of them air fryers of genuinely different shapes, and four guides written to help you rule things out. No prices, no star ratings, no invented testing &mdash; just the comparisons that actually change the decision.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="${esc(href("/shop/"))}">Browse the shop <span class="arrow" aria-hidden="true">&rarr;</span></a>
        <a class="btn btn-ghost" href="${esc(href("/guides/basket-vs-oven-air-fryer/"))}">Start with the guide</a>
      </div>
    </div>
    <aside class="season-card">
      <p class="season-label">In season</p>
      <h2>Cooking for a full house?</h2>
      <p>Counter space is the binding constraint in November, not wattage. Three things worth reading before you buy:</p>
      <ul class="season-list">
        <li><a href="${esc(href("/guides/air-fryer-capacity-checklist/"))}"><span>Capacity, without the hype</span><span>5 min</span></a></li>
        <li><a href="${esc(href("/guides/air-fryer-cleaning-counter-space/"))}"><span>Cleanup vs. counter space</span><span>5 min</span></a></li>
        <li><a href="${esc(href("/guides/questions-before-buying-multifunction-appliance/"))}"><span>Six questions before you buy</span><span>6 min</span></a></li>
      </ul>
    </aside>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <h2>On the shelf</h2>
        <p>The four products this shop stocks, described by shape and trade-off rather than by spec-sheet volume.</p>
      </div>
      <a class="section-link" href="${esc(href("/shop/"))}">All products &rarr;</a>
    </div>

    <article class="card" style="margin-bottom:22px">
      <div class="card-tagrow">
        <span class="pill pill-accent">Lead pick &middot; ${esc(lead.style)}</span>
        <span class="pill">${esc(lead.brand)}</span>
      </div>
      <h3><a href="${esc(href(productUrl(lead)))}">${esc(lead.name)}</a></h3>
      <p class="card-hook">${esc(lead.hook)}</p>
      <p style="margin:0 0 18px;font-size:15.5px;color:var(--ink-2);max-width:78ch">${esc(lead.oneLine)} It is the one to look at if you are replacing a toaster oven rather than adding a second appliance &mdash; and the one to skip if the counter cannot spare the depth.</p>
      <div class="card-foot">
        <a class="card-link" href="${esc(href(productUrl(lead)))}">Read the breakdown</a>
        ${outbound({ asin: lead.asin, productId: lead.id, placement: "front-lead", label: "See the listing on Amazon" })}
        ${sponsorNote()}
      </div>
    </article>

    <div class="shelf">
      ${shelf.map((p) => productCard(p, "front-shelf")).join("\n")}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <h2>Guides</h2>
        <p>Each one is a single question, answered in the order that rules options out fastest.</p>
      </div>
      <a class="section-link" href="${esc(href("/guides/"))}">All guides &rarr;</a>
    </div>
    <div class="guide-list">
      ${guides
        .map(
          (g) => `<a class="guide-row" href="${esc(href(guideUrl(g)))}">
        <div class="guide-kicker">${esc(g.kicker)}</div>
        <div>
          <h3>${esc(g.question)}</h3>
          <p>${esc(g.dek)}</p>
        </div>
        <div class="guide-meta">${g.readMinutes} min</div>
      </a>`
        )
        .join("")}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <h2>How this shop works</h2>
        <p>Three commitments, stated plainly, because a shop that hides them is asking to be distrusted.</p>
      </div>
      <a class="section-link" href="${esc(href("/about/"))}">The full policy &rarr;</a>
    </div>
    <div class="shelf shelf-3">
      <div class="panel">
        <h3 style="color:var(--accent)">What we show</h3>
        <ul>
          <li>The shape of each appliance and what it is for</li>
          <li>The trade-offs we would want flagged before buying</li>
          <li>A direct link to the live listing for price and rating</li>
        </ul>
      </div>
      <div class="panel">
        <h3 style="color:var(--accent)">What we do not</h3>
        <ul>
          <li>Prices, which change hourly and are not ours to publish</li>
          <li>Star ratings or review quotes, which Amazon restricts</li>
          <li>Any claim that we have tested a product we have not touched</li>
        </ul>
      </div>
      <div class="panel">
        <h3 style="color:var(--accent)">Why you can check</h3>
        <ul>
          <li>Every product detail is quoted from the listing and linked</li>
          <li>Every open question is published, not buried</li>
          <li>One held link is flagged rather than quietly guessed</li>
        </ul>
      </div>
    </div>
    <div class="record-note">
      <strong>One thing is unresolved.</strong> Five links were submitted; four resolved to a product listing and one did not. The unresolved link is held back rather than guessed at, and it is published on the
      <a href="${esc(href("/records/flagged/"))}">Flagged for Review</a> page with the exact evidence.
    </div>
  </div>
</section>`;

  return page({
    title: `${site.brand} — kitchen tools, chosen by what you actually cook`,
    description:
      "An honest shop for kitchen tools: three air fryers of genuinely different shapes and one wireless thermometer, with buying guides written to rule options out. Sponsored Amazon links, clearly marked.",
    path: "/",
    body,
    current: "",
  });
}

// ---------------------------------------------------------------- shop

function shopIndex() {
  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Shop" }])}
<div class="page-head">
  <div class="wrap">
    <h1>Everything on the shelf</h1>
    <p>Four products, grouped by what they are for. Each page describes the shape of the appliance, what it suits, and what it costs you in counter space and washing up &mdash; then links straight to the live listing.</p>
  </div>
</div>

${categories
  .map((c) => {
    const list = products.filter((p) => p.category === c.id);
    return `<section class="section" id="${esc(c.id)}">
  <div class="wrap">
    <div class="section-head">
      <div>
        <h2>${esc(c.label)}</h2>
        <p>${esc(c.blurb)}</p>
      </div>
    </div>
    <div class="shelf">${list.map((p) => productCard(p, "shop-index")).join("\n")}</div>
  </div>
</section>`;
  })
  .join("\n")}

<section class="section">
  <div class="wrap wrap-narrow" style="margin-inline:auto">
    <div class="callout alert">
      <h3>One submitted link is not on this page</h3>
      <p>${esc(heldProduct.reason)}</p>
      <p>${esc(heldProduct.effect)}</p>
      <p><a href="${esc(href("/records/held-link/"))}">What happened to that link, in full &rarr;</a></p>
    </div>
  </div>
</section>`;

  return page({
    title: "Shop — every product on the shelf | " + site.brand,
    description:
      "Three air fryers and one wireless meat thermometer, described by shape and trade-off. Sponsored Amazon links, clearly marked, with no prices or ratings republished.",
    path: "/shop/",
    body,
    current: "shop",
  });
}

function productPage(p) {
  const g = p.pairingGuide ? guides.find((x) => x.slug === p.pairingGuide) : null;
  const others = products.filter((x) => x.id !== p.id && x.category === p.category);

  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Shop", href: "/shop/" }, { label: p.name }])}

<div class="product-hero">
  <div class="wrap product-grid">
    <div>
      <div class="card-tagrow">
        <span class="pill">${esc(p.style)}</span>
        <span class="pill pill-accent">${esc(p.brand)}</span>
      </div>
      <h1>${esc(p.name)}</h1>
      <p class="hook">${esc(p.hook)}</p>
      <p style="font-size:17px;color:var(--ink-2);line-height:1.65;margin:0">${esc(p.oneLine)}</p>
    </div>
    <aside class="buy-box">
      <p class="label">Where to buy</p>
      ${outbound({ asin: p.asin, productId: p.id, placement: "product-buybox", label: "See price on Amazon" })}
      <p class="note">${esc(site.affiliateNote)}</p>
      <div class="asin"><span>ASIN ${esc(p.asin)}</span><span>${p.asinStatus === "observed" ? "observed" : "confirmed"}</span></div>
    </aside>
  </div>
</div>

<div class="wrap">
  <section class="prose wrap-narrow" style="margin-inline:auto;padding-top:40px">
    <h2>What it is</h2>
    <table class="spec-table">
      <caption class="sr-only" style="position:absolute;left:-9999px">Specifications as stated on the Amazon listing</caption>
      <tbody>
        ${p.specs.map((s) => `<tr><th scope="row">${esc(s.label)}</th><td>${esc(s.value)}</td></tr>`).join("")}
      </tbody>
    </table>
    <p style="font-size:13px;color:var(--ink-3);margin-top:12px">Quoted from the listing title and feature text. Prices and ratings are on the live listing, not here.</p>

    <div class="two-col">
      <div class="panel good">
        <h3>Suits</h3>
        <ul>${p.bestFor.map((b) => `<li>${esc(b)}</li>`).join("")}</ul>
      </div>
      <div class="panel caution">
        <h3>Think twice if</h3>
        <ul>${p.thinkTwice.map((b) => `<li>${esc(b)}</li>`).join("")}</ul>
      </div>
    </div>

    <h2>How to decide on this one</h2>
    ${p.criteria
      .map(
        (c) => `<h3 style="font-family:var(--display);font-size:20px;margin:28px 0 8px;font-weight:600">${esc(c.heading)}</h3>
      <p>${esc(c.body)}</p>`
      )
      .join("")}

    ${
      g
        ? `<div class="pullquote">
      <p class="label">Read next</p>
      <p>${esc(g.dek)}</p>
      <p style="margin-top:12px;font-family:var(--body);font-size:14px;font-style:normal"><a href="${esc(href(guideUrl(g)))}">${esc(g.question)} &rarr;</a></p>
    </div>`
        : ""
    }

    <h2>Before you buy</h2>
    <p>Two checks worth doing on the listing itself, because they change between variants and over time: confirm the exact size or probe count selected in the buy box, and confirm the seller. Both are shown on Amazon and neither is something this page can vouch for on your behalf.</p>

    <div class="callout" style="margin-top:34px">
      <h3>About the link on this page</h3>
      <p>${esc(site.disclosure)} The button above carries the Associates ID <code style="font-family:var(--mono);font-size:13px">${esc(site.tag)}</code> and is marked as sponsored in the page markup.</p>
      <p>The destination product was identified by following the link that was submitted for this shop on 2026-11-20. That observation is recorded separately from any intent to promote a specific variant, and the record is published at <a href="${esc(href("/records/product-intent/"))}">Product intent</a>.</p>
    </div>
  </section>

  ${
    others.length
      ? `<section class="section" style="border-top:1px solid var(--rule);margin-top:40px">
    <div class="wrap">
      <div class="section-head"><div><h2>Also in air fryers</h2><p>Comparing shapes is more useful than comparing numbers.</p></div></div>
      <div class="shelf">${others.map((o) => productCard(o, "product-cross-sell")).join("")}</div>
    </div>
  </section>`
      : ""
  }
</div>`;

  return page({
    title: `${p.name} — what it is and who it suits | ${site.brand}`,
    description: `${p.oneLine} A buyer's breakdown of shape, trade-offs and who this suits, with a clearly marked sponsored link to the Amazon listing.`,
    path: productUrl(p),
    body,
    current: "shop",
  });
}

function heldLinkPage() {
  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Shop", href: "/shop/" }, { label: "Held link" }])}
<div class="page-head">
  <div class="wrap">
    <h1>A link we have not published</h1>
    <p>One of the five links submitted for this shop did not resolve to a product listing. No page has been built for it, because building one would mean guessing which product it was meant to be.</p>
  </div>
</div>
<div class="wrap wrap-narrow" style="margin-inline:auto;padding:38px 0">
  <div class="callout alert">
    <h3>What was submitted</h3>
    <p><code style="font-family:var(--mono);font-size:13.5px">${esc(heldProduct.submitted_link)}</code></p>
  </div>
  <h2 style="font-family:var(--display);font-size:24px;margin:32px 0 10px">What happened when it was checked</h2>
  <p>${esc(heldProduct.reason)}</p>
  <p>It was tried repeatedly on 2026-11-20. The two outcomes were a bot-check interstitial and the Amazon homepage; neither is a product listing. A direct lookup of the code as an ASIN returned no product.</p>

  <h2 style="font-family:var(--display);font-size:24px;margin:32px 0 10px">Why it is held instead of guessed</h2>
  <p>${esc(heldProduct.effect)} A shop page has to be able to say what a product is and who it suits. With no listing to read, none of that can be stated honestly, and a guessed link would send readers somewhere the shop cannot describe.</p>

  <h2 style="font-family:var(--display);font-size:24px;margin:32px 0 10px">What would fix it</h2>
  <p>${esc(heldProduct.next_step)}</p>

  <div class="callout">
    <h3>How this is recorded</h3>
    <p>The link is entered in the <a href="${esc(href("/records/product-intent/"))}">product intent record</a> with status <strong>unresolved</strong>, and on the <a href="${esc(href("/records/flagged/"))}">Flagged for Review</a> page as FLG-001. Nothing about it has been inferred.</p>
  </div>
</div>`;

  return page({
    title: "A submitted link we have not published | " + site.brand,
    description:
      "One submitted Amazon short link did not resolve to a product listing. Rather than guess the product, the link is held and the evidence published.",
    path: "/records/held-link/",
    body,
    current: "shop",
  });
}

// ---------------------------------------------------------------- guides

function guidesIndex() {
  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Guides" }])}
<div class="page-head">
  <div class="wrap">
    <h1>Buying guides</h1>
    <p>Four questions, each answered in the order that eliminates options fastest. These are working topics chosen as hypotheses about what a comparison shopper asks &mdash; not a claim about what is popular, and not a ranking of products.</p>
  </div>
</div>
<div class="wrap" style="padding:8px 0 20px">
  <div class="guide-list">
    ${guides
      .map(
        (g) => `<a class="guide-row" href="${esc(href(guideUrl(g)))}">
      <div class="guide-kicker">${esc(g.kicker)}</div>
      <div>
        <h3>${esc(g.question)}</h3>
        <p>${esc(g.dek)}</p>
      </div>
      <div class="guide-meta">${g.readMinutes} min</div>
    </a>`
      )
      .join("")}
  </div>
  <div class="record-note">
    <strong>Why these four.</strong> Each one is narrow enough to answer without pretending to test anything, and specific enough that a reader who searches it is already close to a decision. The fifth topic will be chosen from measured search data, not from instinct &mdash; see open question <a href="${esc(href("/records/questions/"))}">Q-05</a>.
  </div>
</div>`;

  return page({
    title: "Buying guides — air fryers and kitchen thermometers | " + site.brand,
    description:
      "Four question-shaped buying guides: basket versus oven style, capacity without the hype, cleanup versus counter space, and the questions to ask before buying a multi-function appliance.",
    path: "/guides/",
    body,
    current: "guides",
  });
}

function guidePage(g) {
  const related = (g.relatedProducts || []).map((id) => byId[id]).filter(Boolean);
  const others = guides.filter((x) => x.id !== g.id).slice(0, 3);

  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Guides", href: "/guides/" }, { label: g.kicker }])}

<div class="article-head">
  <div class="wrap-narrow" style="margin-inline:auto">
    <p class="eyebrow">${esc(g.kicker)}</p>
    <h1>${esc(g.question)}</h1>
    <p class="article-dek">${esc(g.dek)}</p>
    <div class="byline">
      <span>By <strong>${esc(site.desk)}</strong></span>
      <span>${g.readMinutes} min read</span>
      <span>Reviewed 2026-11-20</span>
      <span>No hands-on testing claimed</span>
    </div>
  </div>
</div>

<div class="wrap-narrow" style="margin-inline:auto">
  <article class="prose">
    ${g.sections
      .map(
        (s) => `<h2>${esc(s.heading)}</h2>
      ${s.body.map((p) => `<p>${esc(p)}</p>`).join("")}`
      )
      .join("")}

    <div class="pullquote">
      <p class="label">The short version</p>
      <p>${esc(g.bottomLine)}</p>
    </div>

    <div id="guide-end" data-guide="${esc(g.id)}"></div>

    ${
      related.length
        ? `<h2>Where these criteria apply here</h2>
      <p>The shop stocks ${related.length} product${related.length > 1 ? "s" : ""} that this comparison bears on directly. Each page repeats the criteria rather than a verdict:</p>
      <div class="shelf" style="margin-top:22px">${related.map((p) => productCard(p, `guide-${g.id}`)).join("")}</div>`
        : ""
    }

    <div class="callout" style="margin-top:36px">
      <h3>What this guide does not do</h3>
      <p>It does not rate products, quote reviews, or report a price. Those are on the live listing, where Amazon serves them. It also does not claim any appliance was tested for this article &mdash; the criteria come from how the appliances are built and from the feature sets stated on the listings.</p>
      <p>${esc(site.disclosure)}</p>
    </div>
  </article>

  <section class="section" style="border-top:1px solid var(--rule)">
    <div class="section-head"><div><h2 style="font-size:26px">Keep reading</h2></div><a class="section-link" href="${esc(href("/guides/"))}">All guides &rarr;</a></div>
    <div class="guide-list">
      ${others
        .map(
          (o) => `<a class="guide-row" href="${esc(href(guideUrl(o)))}">
        <div class="guide-kicker">${esc(o.kicker)}</div>
        <div><h3>${esc(o.question)}</h3><p>${esc(o.dek)}</p></div>
        <div class="guide-meta">${o.readMinutes} min</div>
      </a>`
        )
        .join("")}
    </div>
  </section>
</div>`;

  return page({
    title: `${g.question} | ${site.brand}`,
    description: g.dek,
    path: guideUrl(g),
    body,
    current: "guides",
  });
}

// ---------------------------------------------------------------- about

function aboutPage() {
  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "About" }])}
<div class="page-head">
  <div class="wrap">
    <h1>How this shop works</h1>
    <p>A shop is a set of promises about what it will and will not do. These are ours, in plain language, with the reasoning attached.</p>
  </div>
</div>

<div class="wrap-narrow" style="margin-inline:auto">
  <article class="prose">
    <h2 id="disclosure">The disclosure, and why it is at the top of every page</h2>
    <p><strong>${esc(site.disclosure)}</strong></p>
    <p>That sentence appears directly under the masthead on every page of this site, and again in the footer. It is the exact wording Amazon's Associates Operating Agreement requires, and the placement is deliberate: the FTC's guidance for endorsements says a disclosure is likely to be missed if it appears only on an about page, at the end of a post, or anywhere that requires a click.</p>
    <p>So it is not on this page alone. It is on all of them, above the fold, before any product.</p>

    <h2>Every outbound product link is marked as sponsored</h2>
    <p>Each button that leaves this site for Amazon carries the Associates ID ${esc(site.tag)} in its url and is marked <code>rel="sponsored"</code> in the page markup. Each one names its destination on the button itself, rather than hiding behind a shortened link.</p>

    <h2>What we publish, and what we deliberately do not</h2>
    <table class="spec-table">
      <tbody>
        <tr><th scope="row">Product details</th><td>Quoted from the listing title and feature text, with the ASIN shown so you can check it.</td></tr>
        <tr><th scope="row">Prices</th><td><strong>Not published.</strong> Amazon permits showing a price only when Amazon serves it or when it comes from an approved API. Prices also change hourly, so a copied price is a wrong price.</td></tr>
        <tr><th scope="row">Star ratings and review quotes</th><td><strong>Not published.</strong> Amazon restricts the display of customer reviews and star ratings to data obtained through its APIs. The live listing shows them; this site links there.</td></tr>
        <tr><th scope="row">Hands-on testing</th><td><strong>Not claimed.</strong> No product here has been tested by this desk. The FTC is explicit that you cannot describe experience with a product you have not tried, so the copy is written as comparison criteria instead of verdicts.</td></tr>
        <tr><th scope="row">Rankings and "best of" lists</th><td><strong>Not published.</strong> A ranking implies a comparison that was actually performed. These pages help you eliminate options; they do not crown a winner.</td></tr>
      </tbody>
    </table>

    <h2>How products get on the shelf</h2>
    <p>A link is submitted, the destination is checked on a dated pass, and a page is built only for links that resolve to a listing the shop can describe. Where a link does not resolve, it is held and published as a defect rather than guessed at.</p>
    <p>The shop currently stocks four products from five submitted links. What happened to the fifth is documented on the <a href="${esc(href("/records/held-link/"))}">held link page</a>.</p>

    <h2>What we cannot yet tell you</h2>
    <p>Several things a reader might reasonably want to know are not established, and rather than paper over them they are listed in public:</p>
    <ul>
      <li>Which exact product each submitted link was <em>intended</em> to promote. The destinations were observed; intent has not been confirmed.</li>
      <li>Whether the short-link format used in the submission is itself a compliant link format. That question is open, not answered.</li>
      <li>Who writes this desk. The byline is an organisation name because no named author was supplied.</li>
    </ul>
    <p>All of it sits on the <a href="${esc(href("/records/questions/"))}">open questions</a> page and the <a href="${esc(href("/records/flagged/"))}">Flagged for Review</a> page.</p>

    <h2>Measurement, and what we do not collect</h2>
    <p>This site counts outbound clicks without a cookie, without a session identifier, and without collecting an IP address or user agent. It runs no third-party analytics script. The counter is described in full on the <a href="${esc(href("/records/measurement/"))}">measurement page</a> &mdash; including the fact that it is currently switched off because no endpoint has been configured.</p>

    <h2>The records</h2>
    <p>Everything behind the shop is published: the <a href="${esc(href("/records/source-register/"))}">source register</a> with a link for every verified claim, the <a href="${esc(href("/records/product-intent/"))}">product intent record</a>, the <a href="${esc(href("/records/compliance/"))}">compliance checks</a>, the <a href="${esc(href("/records/campaign-ledger/"))}">campaign ledger</a> (deliberately empty), the <a href="${esc(href("/records/suggestions/"))}">suggestion register</a>, and the <a href="${esc(href("/records/flagged/"))}">flagged items</a>.</p>
  </article>
</div>`;

  return page({
    title: "How this shop works — disclosure, sourcing and limits | " + site.brand,
    description:
      "The disclosure that appears on every page, how products get on the shelf, what this shop deliberately does not publish, and what remains unconfirmed.",
    path: "/about/",
    body,
    current: "about",
  });
}

// ---------------------------------------------------------------- records: index

function recordsIndex() {
  const cards = [
    ["Source register", "/records/source-register/", "Every verified claim with the official page it came from, and every claim that could not be verified, left blank.", `${D.sources.sources.filter((s) => s.status === "verified").length} verified · ${D.sources.sources.filter((s) => s.status === "unverified").length} unverified`],
    ["Product intent", "/records/product-intent/", "Intended ASIN kept in a separate field from the observed redirect target. Never merged.", `${D.intent.products.filter((p) => p.status === "observed_only").length} observed · 1 unresolved`],
    ["Compliance", "/records/compliance/", "Each obligation checked against the official policy text, with the gate that enforces it.", "12 checks"],
    ["Measurement", "/records/measurement/", "The five defined events, the no-identifier design, and why the counter is currently off.", `${D.events.events.length} events`],
    ["Campaign ledger", "/records/campaign-ledger/", "Empty on purpose. Columns defined in advance; rows added only from a first-party report.", `${D.ledger.rows.length} rows`],
    ["Open questions", "/records/questions/", "What we hold, what is missing, what it blocks, and how to get it.", `${D.questions.questions.length} questions`],
    ["Suggestions", "/records/suggestions/", "Proposed changes with a recommended path, alternatives considered, and a decision control.", `${D.suggestions.suggestions.filter((s) => s.state === "accepted").length} accepted · ${D.suggestions.suggestions.filter((s) => s.state === "proposed").length} open`],
    ["Flagged for review", "/records/flagged/", "Irregularities, unresolved items and known gaps, with the evidence for each.", "4 open"],
  ];

  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Records" }])}
<div class="page-head">
  <div class="wrap">
    <h1>The records</h1>
    <p>The verification layer behind the shop, published rather than filed. Every claim that has a source links to it; every claim without one is left blank and marked as such. Nothing here blocks a reader from shopping &mdash; it exists so the shop can be checked.</p>
  </div>
</div>
<div class="wrap">
  <div class="shelf shelf-2 pad-y">
    ${cards
      .map(
        ([title, url, desc, meta]) => `<a class="card" href="${esc(href(url))}" style="text-decoration:none">
      <div class="card-tagrow"><span class="pill">Record</span></div>
      <h3>${esc(title)}</h3>
      <p style="margin:0 0 16px;font-size:15px;color:var(--ink-2);line-height:1.6">${esc(desc)}</p>
      <div class="card-foot"><span class="sponsor-note">${esc(meta)}</span></div>
    </a>`
      )
      .join("")}
  </div>
  <div class="record-note">
    <strong>How to read these.</strong> A value is only present when an official source states it. Where a value could not be confirmed, the cell is empty and the row is marked unverified. No value on these pages was inferred, averaged, or estimated.
  </div>
</div>`;

  return page({
    title: "Records — sources, intent, compliance and open questions | " + site.brand,
    description:
      "The verification layer behind the shop: a source register with official links, product intent kept separate from observed redirects, compliance checks, an empty campaign ledger, and open questions.",
    path: "/records/",
    body,
    noindex: false,
  });
}

// ---------------------------------------------------------------- records: source register

function sourceRegister() {
  const rows = D.sources.sources
    .map((s) => {
      const st = s.status === "verified" ? badge("verified", "verified") : badge("unverified", "unverified");
      return `<tr>
      <td><code>${esc(s.id)}</code></td>
      <td>${esc(s.claim)}</td>
      <td>${s.value ? esc(s.value) : '<span class="empty-cell">— left blank, not confirmed by an official source</span>'}</td>
      <td>${esc(s.publisher) || '<span class="empty-cell">—</span>'}</td>
      <td>${s.url ? srcLink(new URL(s.url).hostname.replace(/^www\./, ""), s.url) : '<span class="empty-cell">—</span>'}</td>
      <td>${esc(s.verified_at)}</td>
      <td>${st}</td>
    </tr>`;
    })
    .join("");

  const verified = D.sources.sources.filter((s) => s.status === "verified").length;
  const unverified = D.sources.sources.filter((s) => s.status === "unverified").length;

  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Records", href: "/records/" }, { label: "Source register" }])}
<div class="page-head">
  <div class="wrap">
    <h1>Source register</h1>
    <p>Every claim this site relies on, the official page that states it, and whether the value could be read directly. A row marked unverified has had its value column left blank on purpose.</p>
  </div>
</div>
<div class="wrap">
  <div class="stat-row">
    <div class="stat"><div class="n">${D.sources.sources.length}</div><div class="l">Rows</div></div>
    <div class="stat"><div class="n">${verified}</div><div class="l">Verified</div></div>
    <div class="stat"><div class="n">${unverified}</div><div class="l">Unverified</div></div>
    <div class="stat"><div class="n">${esc(D.sources.verified_at)}</div><div class="l">Pass date</div></div>
  </div>

  <div class="table-scroll">
    <table class="data-table">
      <thead><tr>
        <th>ID</th><th>Claim</th><th>Value as stated by the source</th><th>Publisher</th><th>Official source</th><th>Checked</th><th>Status</th>
      </tr></thead>
      <tbody>${rows}</tbody>
    </table>
  </div>

  <div class="record-note">
    <strong>What "verified" means here.</strong> The value was read directly off the linked page during the 2026-11-20 pass. It does not mean the page will never change &mdash; several of these policies carry future effective dates, and those are recorded exactly as published. <strong>What "unverified" means:</strong> no official source states the value in a form this session could read, so the cell is empty. Two examples: the commission rate schedule sits behind an Associates sign-in, and the compliance status of the submitted short-link format is genuinely unresolved.
  </div>
</div>`;

  return page({
    title: "Source register — every claim and its official source | " + site.brand,
    description:
      "A row-by-row register of every claim this site relies on, with a link to the official Amazon, FTC, Google or GitHub page that states it, and empty cells where a value could not be confirmed.",
    path: "/records/source-register/",
    body,
  });
}

// ---------------------------------------------------------------- records: product intent

function productIntent() {
  const rows = D.intent.products
    .map((p) => {
      const st =
        p.status === "confirmed"
          ? badge("confirmed", "verified")
          : p.status === "observed_only"
          ? badge("observed only", "observed")
          : badge("unresolved", "unresolved");
      return `<tr>
      <td><code>${esc(p.id)}</code></td>
      <td><code style="font-size:11.5px">${esc(p.submitted_code)}</code></td>
      <td>${p.intended_asin ? `<code>${esc(p.intended_asin)}</code>` : '<span class="empty-cell">not confirmed</span>'}</td>
      <td>${p.official_listing_url ? `<a class="src-link" href="${esc(p.official_listing_url)}" rel="noopener" target="_blank">listing&nbsp;&#8599;</a>` : '<span class="empty-cell">—</span>'}</td>
      <td>${p.observed_redirect_target ? `<code style="font-size:11.5px">${esc(p.observed_redirect_target.replace("https://www.amazon.com/dp/", ""))}</code>` : '<span class="empty-cell">no listing reached</span>'}</td>
      <td>${esc(p.observed_at.slice(0, 10))}</td>
      <td>${p.flag ? `<a class="src-link" href="${esc(href("/records/flagged/"))}">${esc(p.flag)}</a>` : "—"}</td>
      <td>${st}</td>
    </tr>`;
    })
    .join("");

  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Records", href: "/records/" }, { label: "Product intent" }])}
<div class="page-head">
  <div class="wrap">
    <h1>Product intent record</h1>
    <p>For every submitted link: the ASIN and listing this shop <em>intended</em> to promote, and &mdash; in a separate field &mdash; the destination that was actually observed. The two are never merged, because an observation is evidence of behaviour and intent is a statement by a person.</p>
  </div>
</div>
<div class="wrap">
  <div class="record-note" style="margin-top:26px">
    <strong>Why two fields.</strong> Amazon identifies a product by a 10-character ASIN, which makes intent checkable. If a redirect is written into the intent field, the record stops being checkable &mdash; it just restates what the link did, and a wrong redirect becomes indistinguishable from a correct decision. So <code>intended_asin</code> stays empty until the person who submitted the link says which product they meant, or until an Associates report shows it.
  </div>

  <div class="table-scroll">
    <table class="data-table">
      <thead><tr>
        <th>ID</th><th>Submitted code</th><th>Intended ASIN</th><th>Official listing</th><th>Observed redirect target</th><th>Observed</th><th>Flag</th><th>Status</th>
      </tr></thead>
      <tbody>${rows}</tbody>
    </table>
  </div>

  <h2 style="font-family:var(--display);font-size:26px;margin:44px 0 6px">Field rules</h2>
  <p style="color:var(--ink-2);font-size:15px;max-width:78ch;margin:0 0 18px">These rules are part of the record, not documentation about it:</p>
  <div class="table-scroll">
    <table class="data-table">
      <thead><tr><th>Field</th><th>Rule</th></tr></thead>
      <tbody>
        ${Object.entries(D.intent.field_rules)
          .map(([k, v]) => `<tr><td><code>${esc(k)}</code></td><td>${esc(v)}</td></tr>`)
          .join("")}
      </tbody>
    </table>
  </div>

  <div class="record-note">
    <strong>The honest state of it.</strong> Four of five links resolved to a real product listing on 2026-11-20 and those four are described on the site using the canonical listing URL for the observed ASIN plus the supplied Associates tag. None of the five intended ASINs has been confirmed, so every row reads <em>observed only</em>. One link reached no listing at all and is published as unresolved. All five are open questions &mdash; see <a href="${esc(href("/records/questions/"))}">Q-01</a> and <a href="${esc(href("/records/questions/"))}">Q-13</a>.
  </div>
</div>`;

  return page({
    title: "Product intent record — intended ASIN vs. observed destination | " + site.brand,
    description:
      "For each submitted Amazon link, the intended ASIN and official listing kept in a separate field from the observed redirect target. No intended ASIN has been confirmed; every row is marked observed only.",
    path: "/records/product-intent/",
    body,
  });
}

// ---------------------------------------------------------------- records: compliance

function compliancePage() {
  const checks = [
    ["C01", "Disclosure statement present in exact required wording", "S01", "Pass", "Rendered in the strip under the masthead and repeated in the footer of every generated page. The build fails if the string is missing from any page."],
    ["C02", "Disclosure placed above the fold, not only on an about page", "S18", "Pass", "The strip sits directly beneath the masthead, before any content. The FTC guidance explicitly warns that an about-page-only disclosure is likely to be missed."],
    ["C03", "Every outbound product link carries the Associates tag", "S02", "Pass", "All outbound product anchors are built from the tag constant; the build fails on any amazon.com link without it."],
    ["C04", "Every outbound product link is marked as sponsored", "S02", "Pass", "Anchors carry rel=\"sponsored nofollow noopener\". The build gate rejects an outbound Amazon anchor without rel=sponsored."],
    ["C05", "Outbound link destination is not obscured or shortened on our side", "S03", "Pass", "Buttons name Amazon as the destination. The anchors point at the canonical /dp/ URL, not a redirect."],
    ["C06", "No price is displayed", "S05", "Pass", "No price appears on any generated page. Enforced by the build gate, which rejects a currency pattern in page content."],
    ["C07", "No star rating or customer review text is displayed", "S04", "Pass", "No rating or review text appears. The build gate checks for rating markup and review-quote patterns."],
    ["C08", "No hands-on testing claim is made", "S19", "Pass", "Every guide states 'No hands-on testing claimed' in the byline, and each closes with a paragraph saying what it does not do."],
    ["C09", "No click redirect sits between the reader and Amazon", "S08, S09", "Pass", "The measurement beacon is fire-and-forget on a real activation. The browser navigates to Amazon directly; the endpoint never redirects."],
    ["C10", "No cookie or user identifier is set by this site", "S24", "Pass", "No cookie, no localStorage identifier, no third-party script. The suggestion control writes only the owner's own choices, locally."],
    ["C11", "No paid search placement on Amazon marks", "S06", "Not attempted", "No advertising is bought on any channel. Recorded as a standing constraint rather than a completed check; see suggestion SG-11."],
    ["C12", "Commission rate published accurately", "S17", "Cannot verify", "The rate schedule requires an Associates sign-in, so no rate could be read. No commission figure is published anywhere."],
  ];

  const rows = checks
    .map(([id, obligation, src, result, how]) => {
      const kind = result === "Pass" ? "verified" : result === "Not attempted" ? "open" : "unverified";
      return `<tr>
      <td><code>${esc(id)}</code></td>
      <td>${esc(obligation)}</td>
      <td>${esc(src)}</td>
      <td>${badge(result, kind)}</td>
      <td>${esc(how)}</td>
    </tr>`;
    })
    .join("");

  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Records", href: "/records/" }, { label: "Compliance" }])}
<div class="page-head">
  <div class="wrap">
    <h1>Compliance checks</h1>
    <p>Twelve obligations, each traced to the policy text that creates it and to the mechanism that enforces it. Ten pass and are enforced by the build. One is a standing decision not to act. One cannot be verified at all.</p>
  </div>
</div>
<div class="wrap">
  <div class="stat-row">
    <div class="stat"><div class="n">12</div><div class="l">Checks</div></div>
    <div class="stat"><div class="n">10</div><div class="l">Pass, gate-enforced</div></div>
    <div class="stat"><div class="n">1</div><div class="l">Standing constraint</div></div>
    <div class="stat"><div class="n">1</div><div class="l">Not verifiable</div></div>
  </div>

  <div class="table-scroll">
    <table class="data-table">
      <thead><tr><th>ID</th><th>Obligation</th><th>Source</th><th>Result</th><th>How it is met or why it cannot be</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
  </div>

  <div class="record-note">
    <strong>Source IDs.</strong> S01&ndash;S17 are Amazon Associates pages, S18&ndash;S19 are FTC guidance, S24 is the Associates Influencer Program Policy. Each is linked with its full url on the <a href="${esc(href("/records/source-register/"))}">source register</a>. Two of the most load-bearing points, quoted from the source register: the disclosure sentence must be stated clearly and prominently (S01), and the site must contain original content with commentary, analysis or transformation (S14).
  </div>

  <div class="callout alert" style="margin-top:34px">
    <h3>Two things this page cannot tell you</h3>
    <p><strong>The commission rate.</strong> The Standard Commission Income schedule sits behind an Associates sign-in. No rate is published on this site, and none is implied. (S17)</p>
    <p><strong>The compliance status of the submitted short links.</strong> The Operating Agreement requires Special Links in the tagged format and prohibits shortening that obscures an Amazon destination. Whether the submitted link.amazon format is compliant is not established by anything read in this pass. That is why it is an open flag, not a finding. See <a href="${esc(href("/records/flagged/"))}">FLG-003</a>.</p>
  </div>
</div>`;

  return page({
    title: "Compliance checks — disclosure, sponsored links and content rules | " + site.brand,
    description:
      "Twelve Amazon Associates and FTC obligations traced to policy text and to the build gate that enforces them, including the two that cannot be verified.",
    path: "/records/compliance/",
    body,
  });
}

// ---------------------------------------------------------------- records: measurement

function measurementPage() {
  const rows = D.events.events
    .map(
      (e) => `<tr>
      <td><code>${esc(e.name)}</code></td>
      <td>${esc(e.fires_when)}</td>
      <td>${e.payload.map((x) => `<code>${esc(x)}</code>`).join(", ")}</td>
      <td>${badge("endpoint off", "open")}</td>
    </tr>`
    )
    .join("");

  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Records", href: "/records/" }, { label: "Measurement" }])}
<div class="page-head">
  <div class="wrap">
    <h1>Measurement</h1>
    <p>Five events, one rule: count the click without following the reader. The counter is built and shipped, and it is currently swinging at nothing because no endpoint has been configured.</p>
  </div>
</div>
<div class="wrap">
  <div class="stat-row">
    <div class="stat"><div class="n">5</div><div class="l">Defined events</div></div>
    <div class="stat"><div class="n">0</div><div class="l">Click counts recorded</div></div>
    <div class="stat"><div class="n">0</div><div class="l">Cookies set</div></div>
    <div class="stat"><div class="n">Off</div><div class="l">Endpoint</div></div>
  </div>

  <div class="callout" style="margin-top:30px">
    <h3>Read this before reading anything into a number</h3>
    <p>The client beacon makes no network request at all while <code>CRISP_ENDPOINT</code> is unset. Every count on this page is therefore zero because nothing is being measured &mdash; not because nobody clicked. Web Analytics are not connected either. Treat this page as a wiring diagram, not a report.</p>
  </div>

  <div class="table-scroll">
    <table class="data-table">
      <thead><tr><th>Event</th><th>When it fires</th><th>Payload (non-identifying)</th><th>Status</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
  </div>

  <h2 style="font-family:var(--display);font-size:26px;margin:44px 0 6px">The endpoint contract</h2>
  <p style="color:var(--ink-2);font-size:15px;max-width:78ch;margin:0 0 16px">What a host has to implement, written down so the design cannot drift once someone deploys it:</p>
  <div class="table-scroll">
    <table class="data-table">
      <thead><tr><th>Requirement</th><th>Detail</th></tr></thead>
      <tbody>
        <tr><td>Accepts</td><td><code>POST</code> of a JSON body: <code>{ e, p, d, t }</code> where <code>d</code> is a date at day granularity.</td></tr>
        <tr><td>Stores</td><td>An aggregate counter increment keyed by <code>e</code>, <code>p.path</code> or <code>p.product_id</code>, <code>p.placement</code>, and <code>d</code>.</td></tr>
        <tr><td>Must not store</td><td>IP address, user agent, referrer string, cookies, or any request header that identifies a device.</td></tr>
        <tr><td>Must not do</td><td>Issue a redirect, set a cookie, or return anything the browser needs. The response is fire-and-forget.</td></tr>
        <tr><td>Retention</td><td>Decided by the operator and stated publicly before the endpoint goes live. See open question <a href="${esc(href("/records/questions/"))}">Q-06</a>.</td></tr>
        <tr><td>Precondition</td><td>A published privacy notice naming the counter. See <a href="${esc(href("/records/questions/"))}">Q-09</a>.</td></tr>
      </tbody>
    </table>
  </div>

  <h2 style="font-family:var(--display);font-size:26px;margin:44px 0 6px">Why it is not a redirect</h2>
  <p style="color:var(--ink-2);font-size:15px;max-width:78ch;margin:0 0 16px">The obvious way to count an outbound click is to route it through <code>/go/&lt;id&gt;</code> and issue a 302. That design creates two problems the Associates policies speak to directly: purchases referred through an intermediate site that does not require an affirmative click are disqualified, and associates may not obscure the url of the site containing their links. A fire-and-forget beacon avoids both, because the reader's browser navigates to Amazon itself and the counter never touches the navigation.</p>
  <p style="color:var(--ink-2);font-size:15px;max-width:78ch;margin:0 0 16px">The cost of that choice is honest to state: a blocked beacon under-counts, and the figure can never be reconciled exactly against Amazon's own session count. That is acceptable, because Amazon's reports are the only authoritative conversion source anyway.</p>

  <div class="record-note">
    <strong>What would make this real.</strong> Three things, in order: a host for the endpoint, a published privacy notice, then a retention period set and stated. Until all three exist the counter stays off, because a half-configured counter collects data someone has to be responsible for.
  </div>
</div>`;

  return page({
    title: "Measurement — five events, no identifiers, endpoint off | " + site.brand,
    description:
      "The outbound-click counter design: five defined events, no cookie or identifier, fire-and-forget rather than a redirect, and currently switched off because no endpoint is configured.",
    path: "/records/measurement/",
    body,
  });
}

// ---------------------------------------------------------------- records: ledger

function ledgerPage() {
  const cols = D.ledger.columns;

  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Records", href: "/records/" }, { label: "Campaign ledger" }])}
<div class="page-head">
  <div class="wrap">
    <h1>Campaign ledger</h1>
    <p>Opened on 2026-11-20 and deliberately empty. The columns are defined in advance so that the first real number has somewhere honest to go, and so that no estimate can be mistaken for a measurement.</p>
  </div>
</div>
<div class="wrap">
  <div class="stat-row">
    <div class="stat"><div class="n">${D.ledger.rows.length}</div><div class="l">Rows recorded</div></div>
    <div class="stat"><div class="n">${cols.length}</div><div class="l">Columns defined</div></div>
    <div class="stat"><div class="n">0</div><div class="l">Conversions claimed</div></div>
    <div class="stat"><div class="n">0</div><div class="l">Revenue forecast</div></div>
  </div>

  <div class="callout" style="margin-top:30px">
    <h3>Why an empty table is the honest table</h3>
    <p>There are no conversions to report. No campaign has run, no Associates report has been pulled, and the click counter is not connected. A filled-in table at this point would be a forecast wearing a measurement's clothes, so the values are absent and the schema is published instead.</p>
  </div>

  <div class="table-scroll">
    <table class="data-table">
      <thead><tr>${cols.map((c) => `<th>${esc(c.label)}</th>`).join("")}</tr></thead>
      <tbody>
        <tr>${cols.map(() => '<td class="empty-cell">—</td>').join("")}</tr>
      </tbody>
    </table>
  </div>
  <p style="font-size:13px;color:var(--ink-3);margin-top:10px">A single empty row is shown so the shape is readable. No data row exists.</p>

  <h2 style="font-family:var(--display);font-size:26px;margin:44px 0 6px">Column definitions</h2>
  <div class="table-scroll">
    <table class="data-table">
      <thead><tr><th>Column</th><th>Definition</th></tr></thead>
      <tbody>
        ${cols.map((c) => `<tr><td><code>${esc(c.key)}</code></td><td>${esc(c.definition)}</td></tr>`).join("")}
      </tbody>
    </table>
  </div>

  <h2 style="font-family:var(--display);font-size:26px;margin:44px 0 6px">The rule for adding a row</h2>
  <p style="color:var(--ink-2);font-size:15px;max-width:78ch">A row may be added only when all four of these are true:</p>
  <div class="table-scroll">
    <table class="data-table">
      <tbody>
        <tr><td style="width:60px"><strong>1</strong></td><td>The figure comes from an authorized first-party report &mdash; an Amazon Associates report, or this site's own click counter once it is connected.</td></tr>
        <tr><td><strong>2</strong></td><td>The report name and pull date are recorded in the provenance column.</td></tr>
        <tr><td><strong>3</strong></td><td>No field is derived. If a report does not state eligible sessions, that cell stays empty.</td></tr>
        <tr><td><strong>4</strong></td><td>Nobody has to guess what a number means. If the definition is unclear, the row waits.</td></tr>
      </tbody>
    </table>
  </div>

  <div class="record-note">
    <strong>Two timing facts that shape this.</strong> Commission income is paid roughly 60 days after the month in which it is earned (S11), so a reported-order figure lags the click by about two months and any table that fills in same-week conversions is not reporting Amazon's numbers. And a qualifying session ends after 24 hours, at order placement, or when the reader clicks another associate's link (S10) &mdash; so 'sessions' in this ledger means something narrower than 'visits'.
  </div>
</div>`;

  return page({
    title: "Campaign ledger — empty by design, with defined columns | " + site.brand,
    description:
      "An empty campaign ledger opened on 2026-11-20 with columns defined in advance. Rows are added only from an authorized first-party report, with a dated provenance note. No forecast.",
    path: "/records/campaign-ledger/",
    body,
  });
}

// ---------------------------------------------------------------- records: questions

function questionsPage() {
  const cards = D.questions.questions
    .map(
      (q) => `<article class="qcard">
      <h3><code style="font-family:var(--mono);font-size:12px;color:var(--accent);display:block;margin-bottom:6px">${esc(q.id)}</code>${esc(q.question)}</h3>
      <dl class="qgrid">
        <dt>We hold</dt><dd>${esc(q.have)}</dd>
        <dt>Missing</dt><dd class="none">${esc(q.missing)}</dd>
        <dt>Why it matters</dt><dd>${esc(q.why_it_matters)}</dd>
        <dt>Blocks</dt><dd>${esc(q.blocks)}</dd>
        <dt>Who can answer</dt><dd>${esc(q.who_can_answer)}</dd>
        <dt>How to get it</dt><dd>${esc(q.how_to_get)}</dd>
        <dt>Handled today</dt><dd>${esc(q.current_handling)}</dd>
      </dl>
    </article>`
    )
    .join("");

  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Records", href: "/records/" }, { label: "Open questions" }])}
<div class="page-head">
  <div class="wrap">
    <h1>What we do not yet know</h1>
    <p>Fourteen questions that stand between this site and a confident decision. For each: what we actually hold, what is missing, what the gap blocks, who can close it, and the smallest step that would close it. Nothing here has been filled in by inference.</p>
  </div>
</div>
<div class="wrap" style="padding-top:32px">
  <div class="record-note" style="margin-top:0">
    <strong>How to use this page.</strong> Each row is a blocker, not a to-do. If a question here is still open, the decision it blocks should not be made &mdash; that is the whole point of listing them. The three that block the most are <strong>Q-01</strong> (which ASIN was intended), <strong>Q-02</strong> (whether the submitted link format is compliant) and <strong>Q-06</strong> (where the counter will run).
  </div>
  <div class="qlist">${cards}</div>

  <div class="callout" style="margin-top:40px">
    <h3>What would let all of this be decided at once</h3>
    <p>Three short inputs would close five of the fourteen questions: the intended ASIN for each link, a named author, and a decision on whether the short-link format will be kept. That is a small amount of information carrying a large amount of unblocking, which is why it is listed here rather than asked quietly by email.</p>
  </div>
</div>`;

  return page({
    title: "Open questions — what is missing and what it blocks | " + site.brand,
    description:
      "Fourteen unresolved questions, each with what we hold, what is missing, what it blocks, and how to close it. Every gap is left open rather than filled by inference.",
    path: "/records/questions/",
    body,
  });
}

// ---------------------------------------------------------------- records: suggestions

function suggestionsPage() {
  const cards = D.suggestions.suggestions
    .map((s) => {
      const stateBadge =
        s.state === "accepted"
          ? badge(s.implemented ? "accepted & shipped" : "accepted, not shipped", "done")
          : badge(s.state, "open");
      return `<article class="scard">
      <div class="scard-top">
        <div>
          <code style="font-family:var(--mono);font-size:11px;color:var(--accent)">${esc(s.id)}</code>
          <h3>${esc(s.title)}</h3>
        </div>
        <div>${stateBadge}</div>
      </div>
      <p class="body">${esc(s.problem)}</p>
      <dl>
        <dt>Recommended path</dt><dd>${esc(s.recommended_path)}</dd>
        <dt>Alternatives considered</dt><dd>${s.alternatives.map((a) => esc(a)).join(" &middot; ")}</dd>
        ${s.constrained_by.length ? `<dt>Constrained by</dt><dd>${s.constrained_by.map((c) => esc(c)).join(", ")}</dd>` : ""}
        <dt>Effort</dt><dd>${esc(s.effort)} &middot; Risk: ${esc(s.risk)}</dd>
        <dt>Success measure</dt><dd>${esc(s.success_measure)}</dd>
      </dl>
      <div class="decide" data-decide="${esc(s.id)}">
        <span class="lbl">Your call</span>
        <button type="button" data-state="accepted">Accept</button>
        <button type="button" data-state="deferred">Defer</button>
        <button type="button" data-state="rejected">Reject</button>
        <span class="local-note" id="decision-out-${esc(s.id)}">Recorded in this browser only</span>
      </div>
    </article>`;
    })
    .join("");

  const accepted = D.suggestions.suggestions.filter((s) => s.state === "accepted").length;
  const proposed = D.suggestions.suggestions.filter((s) => s.state === "proposed").length;

  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Records", href: "/records/" }, { label: "Suggestions" }])}
<div class="page-head">
  <div class="wrap">
    <h1>Suggestion register</h1>
    <p>Every proposed change to this site, with the problem it solves, the recommended path, the alternatives that were rejected and why, and the policy that constrains it. Read it, then pick a path &mdash; nothing below ships because it was suggested.</p>
  </div>
</div>
<div class="wrap">
  <div class="stat-row">
    <div class="stat"><div class="n">${D.suggestions.suggestions.length}</div><div class="l">Suggestions</div></div>
    <div class="stat"><div class="n">${accepted}</div><div class="l">Accepted</div></div>
    <div class="stat"><div class="n">${proposed}</div><div class="l">Open for decision</div></div>
    <div class="stat"><div class="n">${D.suggestions.suggestions.filter((s) => s.constrained_by.length).length}</div><div class="l">Policy-constrained</div></div>
  </div>

  <div class="record-note" style="margin-top:26px">
    <strong>How the decision control works.</strong> Accept, Defer or Reject writes only to this browser's local storage &mdash; it records your choice for your own reference and changes nothing on the site. That is deliberate: a page that let a visitor rewrite a published policy with one click would be worse than one that does not. To act on a decision, the change is made in the source and the build gate re-checks it.
  </div>

  <div class="slist">${cards}</div>

  <div class="callout" style="margin-top:40px">
    <h3>If you only read one</h3>
    <p><strong>SG-02</strong> is the one that matters most. Four links resolve to real listings and could be published immediately on that evidence &mdash; but a redirect tells you what a link did, not what someone meant. Confirming the intended ASIN for each link is the single highest-value input available, because it converts four <em>observed only</em> rows into four <em>confirmed</em> ones and lets the copy describe a chosen product instead of a discovered one.</p>
  </div>
</div>`;

  return page({
    title: "Suggestion register — proposed changes with decisions | " + site.brand,
    description:
      "Fifteen proposed changes to this site, each with the problem, the recommended path, the rejected alternatives, the policy constraint, and a local decision control.",
    path: "/records/suggestions/",
    body,
  });
}

// ---------------------------------------------------------------- records: flagged

function flaggedPage() {
  const flags = [
    {
      id: "FLG-001",
      title: "One submitted link does not resolve to a product",
      severity: "Open — unresolved",
      what: "The link https://link.amazon/B0c8moW59 returned an Amazon bot-check interstitial on first fetch, then the Amazon homepage on retry. A direct request to the ASIN page for B0C8MOW59 returned no product. No listing was ever reached.",
      impact: "One of five submitted products is absent from the shop. No page has been created for it and it appears nowhere on the site except as a held link.",
      evidence: "Repeat fetches on 2026-11-20. Two outcomes only: /checkpoint/continue interstitial, and amazon.com homepage.",
      action: "Regenerate the link in Associates Central or send the product name. The page will be built on receipt.",
      source: "/records/held-link/",
    },
    {
      id: "FLG-002",
      title: "No intended ASIN has been confirmed for any link",
      severity: "Open — needs owner input",
      what: "All four resolvable links were followed and their destinations recorded. What was never supplied is the ASIN each link was meant to point at. The record therefore shows four observed targets and zero confirmed intentions.",
      impact: "Product pages describe the listing that the link actually reached. If a link was meant to point at a different variant — and two of these listings offer multiple sizes or probe counts — a published page could be promoting a variant nobody chose.",
      evidence: "See the product intent record; every row is marked observed only.",
      action: "Confirm the intended ASIN and, where the listing offers variants, the intended variant.",
      source: "/records/product-intent/",
    },
    {
      id: "FLG-003",
      title: "Compliance status of the link.amazon short-link format is unresolved",
      severity: "Open — not a finding either way",
      what: "The submitted links use the link.amazon shortener and carry no visible Associates tag in the supplied form. The Operating Agreement requires Special Links in the tagged format and forbids shortening that makes it unclear a link goes to Amazon. Whether this specific format, generated inside Associates Central, satisfies that is not established by anything read in this pass.",
      impact: "This record deliberately makes no claim that the links are invalid. It also cannot claim they are valid. Published outbound links therefore use the canonical /dp/ url with the supplied tag instead of the short form, which is compliant on its face regardless of how the short-link question resolves.",
      evidence: "Program Policies, Participation Requirements, especially the Special Links section and the shortening clause. The supplied codes are also not 10-character ASINs, which is an observation about shape and not a compliance conclusion.",
      action: "Regenerate one link in Associates Central's link builder and compare the url shape; optionally open a support case with Amazon Associates.",
      source: "/records/source-register/",
    },
    {
      id: "FLG-004",
      title: "The click counter is shipped but cannot record anything",
      severity: "Open — needs a host",
      what: "The measurement beacon, the endpoint contract and the five event definitions are all in place. CRISP_ENDPOINT is null, so the beacon returns before making any request.",
      impact: "Every click figure on the site is zero because nothing is being measured, not because nothing happened. No conversion or traffic claim can be made from this site's own data.",
      evidence: "assets/js/analytics.js, and the measurement record.",
      action: "Choose a host, publish a privacy notice, set a retention period, then set the endpoint constant.",
      source: "/records/measurement/",
    },
    {
      id: "FLG-005",
      title: "No named author, and therefore no first-hand product claims",
      severity: "Open — needs owner input",
      what: "The byline is an organisation name because no person was named as the author of record.",
      impact: "Copy is written as comparison criteria rather than experience. That is the correct response to the constraint, but it limits how persuasive the guides can honestly be, and it is the single largest difference between this site and a publication.",
      evidence: "Every guide byline reads 'No hands-on testing claimed'.",
      action: "Supply a name and a one-line credential.",
      source: "/records/questions/",
    },
    {
      id: "FLG-006",
      title: "Commission rates could not be read",
      severity: "Blocked by sign-in",
      what: "The Commission Income Statement appendix links to a Standard Commission Income schedule. That url redirects to an Amazon sign-in page, so no rate was retrievable.",
      impact: "Nothing on this site ranks products by commission potential, and no revenue estimate is offered. A category rate that would change which products are worth stocking is unknown.",
      evidence: "S17 in the source register, marked unverified with the value column left blank.",
      action: "Open the schedule while signed in to Associates Central.",
      source: "/records/source-register/",
    },
    {
      id: "FLG-007",
      title: "Search Console is not connected, so topic choice is still a hypothesis",
      severity: "Open — needs verification",
      what: "The sitemap and feed exist and are discoverable, but no Search Console property is verified, so there is no query data.",
      impact: "The four published guides were chosen as editorial hypotheses. Whether anyone searches them is unknown, and the fifth topic cannot be chosen from measured data as intended.",
      evidence: "Open question Q-05.",
      action: "Verify the property and submit sitemap.xml.",
      source: "/records/questions/",
    },
    {
      id: "FLG-008",
      title: "No outbound link-health check",
      severity: "Known gap",
      what: "The build gate checks internal links only. It cannot fetch amazon.com at build time, so a delisted product or a changed ASIN would not be caught automatically.",
      impact: "Amazon requires removal of program content that is no longer displayed. A dead product page is a compliance defect, not merely a broken link.",
      evidence: "scripts/check.mjs scope.",
      action: "Add a scheduled workflow that fetches each outbound url weekly and opens an issue on failure.",
      source: "/records/compliance/",
    },
  ];

  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Records", href: "/records/" }, { label: "Flagged for review" }])}
<div class="page-head">
  <div class="wrap">
    <h1>Flagged for review</h1>
    <p>Every irregularity, unresolved item and known gap behind this site, with the evidence attached. None of these blocked publication &mdash; the shop is live and shoppable &mdash; but each one is a real thing to look at, and pretending otherwise would be the actual problem.</p>
  </div>
</div>
<div class="wrap" style="padding-top:34px">
  <div class="record-note" style="margin-top:0">
    <strong>How to triage this list.</strong> FLG-002 and FLG-003 are the two that need a person, not an engineering session: one is a question of intent, the other a question of policy. FLG-001 needs a corrected link. The rest are engineering or account work that can be scheduled. Nothing here is a fabricated finding invented to look thorough &mdash; if it is listed, it was encountered.
  </div>
  ${flags
    .map(
      (f) => `<article class="flag" style="margin-top:18px">
    <div class="id">${esc(f.id)} &middot; ${esc(f.severity)}</div>
    <h3>${esc(f.title)}</h3>
    <dl>
      <dt>What was found</dt><dd>${esc(f.what)}</dd>
      <dt>Why it matters</dt><dd>${esc(f.impact)}</dd>
      <dt>Evidence</dt><dd>${esc(f.evidence)}</dd>
      <dt>Suggested action</dt><dd>${esc(f.action)}</dd>
      <dt>Record</dt><dd><a class="src-link" href="${esc(href(f.source))}">${esc(f.source)}&nbsp;&rarr;</a></dd>
    </dl>
  </article>`
    )
    .join("")}
</div>`;

  return page({
    title: "Flagged for review — irregularities and open gaps | " + site.brand,
    description:
      "Eight flagged items behind this site: an unresolved submitted link, unconfirmed intended ASINs, the unresolved short-link compliance question, an unconnected counter, and known gaps.",
    path: "/records/flagged/",
    body,
  });
}

// ---------------------------------------------------------------- executive summary

function summaryPage() {
  const body = `
${breadcrumbs([{ label: "Home", href: "/" }, { label: "Executive summary" }])}
<div class="page-head">
  <div class="wrap">
    <h1>Executive summary</h1>
    <p>What was built, what was verified, what could not be, and the three decisions that would move this furthest. Written for someone who has five minutes.</p>
  </div>
</div>
<div class="wrap-narrow" style="margin-inline:auto">
  <article class="prose">
    <h2>What this is</h2>
    <p>A publisher-style shop for four kitchen appliances, built as a static site and deployed to GitHub Pages, with the verification layer published alongside it instead of hidden in a spreadsheet. The site has a front page, a shop index, four product pages, four buying guides, an about page, and eight record pages covering sources, intent, compliance, measurement, the ledger, open questions, suggestions and flagged items.</p>

    <h2>What was verified, line by line</h2>
    <p>Twenty-four claims were checked against official pages during a single pass on 2026-11-20. Seventeen came from Amazon Associates pages, two from FTC guidance, one from Google's sitemap documentation, one from GitHub's Pages documentation, one from Amazon's own ASIN definition. Two are marked unverified with the value column left empty rather than guessed.</p>
    <p>The single most load-bearing finding for the build: Amazon's Operating Agreement requires the disclosure sentence in specific words, and the FTC's guidance says a disclosure at the bottom of a page or on an about page is likely to be missed. Those two together are why the disclosure strip sits directly under the masthead on every page, in the required wording, and again in the footer.</p>

    <h2>What was verified about the five links</h2>
    <table class="spec-table">
      <tbody>
        <tr><th scope="row">Resolved to a listing</th><td>Four of five. B04G1MEwY, B02NbDxp3, B00hJ57DV and B0f3GKalj each reached a product page, and those destinations are recorded.</td></tr>
        <tr><th scope="row">Did not resolve</th><td>One. B0c8moW59 returned a bot-check interstitial, then the homepage, and no product on a direct lookup. Held, not guessed.</td></tr>
        <tr><th scope="row">Intended ASINs confirmed</th><td>None. Intent was never stated, so it is recorded as empty and kept in a separate field from the observations.</td></tr>
        <tr><th scope="row">Short-link compliance status</th><td>Unresolved. Not ruled invalid, and not assumed valid.</td></tr>
      </tbody>
    </table>

    <h2>The three decisions that matter most</h2>
    <div class="callout">
      <h3>1. Confirm the intended ASIN for each link</h3>
      <p>Four products are already published on observed destinations. Stating the intended ASIN converts four unconfirmed rows into confirmed ones, and catches any variant mismatch &mdash; two of the listings offer multiple sizes or probe counts.</p>
    </div>
    <div class="callout">
      <h3>2. Decide whether to keep the short-link format</h3>
      <p>Whether link.amazon links count as compliant Special Links is genuinely open. Published outbound links use the canonical tagged url instead, which sidesteps the question rather than answering it. If the short form is confirmed fine, nothing changes; if it is not, nothing published is at risk.</p>
    </div>
    <div class="callout">
      <h3>3. Name an author and connect Search Console</h3>
      <p>A named author is what makes the guides claimable as a publication rather than a comparison sheet. Search Console is what makes guide five a measured decision instead of a hunch. Both are small inputs with outsized effects.</p>
    </div>

    <h2>What was deliberately not done</h2>
    <p>No price is published, because Amazon permits prices only when Amazon serves them or when they come from an approved API, and a copied price is wrong within the hour. No star rating or review quote is published, for the same class of reason. No product is claimed to have been tested, because none was &mdash; and the FTC is direct on that point. No revenue is forecast, and the campaign ledger is empty rather than illustrative. No paid traffic is recommended, because two separate rules bear on it.</p>

    <h2>The honest weakness</h2>
    <p>The site is strongest on what it can prove and weakest on the thing every affiliate site needs most: why these five products, chosen by whom, on what basis. That is not a design failure to be hidden; it is the largest single input missing, and it is first on the flagged list for that reason. A shop with a named buyer and a stated criterion would be a materially different proposition, and none of that can be invented without lying about it.</p>

    <h2>Where to look next</h2>
    <p><a href="${esc(href("/records/flagged/"))}">Flagged for review</a> for the eight open items, <a href="${esc(href("/records/questions/"))}">open questions</a> for what blocks what, <a href="${esc(href("/records/suggestions/"))}">suggestions</a> for the paths not taken, and the <a href="${esc(href("/records/source-register/"))}">source register</a> for a link behind every claim.</p>
  </article>
</div>`;

  return page({
    title: "Executive summary | " + site.brand,
    description:
      "What was built and verified: four of five submitted links resolved, no intended ASINs confirmed, twenty-four claims checked against official sources, two left unverified, and three decisions that matter most.",
    path: "/summary/",
    body,
  });
}


// ---------------------------------------------------------------- 404

function notFound() {
  const body = `
<div class="page-head"><div class="wrap">
  <h1>That page is not on the shelf</h1>
  <p>The address you followed does not exist here. It may have been a product we never published, or a typo.</p>
</div></div>
<div class="wrap-narrow" style="margin-inline:auto;padding:38px 0">
  <div class="shelf shelf-2">
    <a class="card" href="${href("/shop/")}" style="text-decoration:none">
      <h3>Shop</h3><p style="margin:0;color:var(--ink-2)">Everything on the shelf, grouped by what it is for.</p>
    </a>
    <a class="card" href="${href("/guides/")}" style="text-decoration:none">
      <h3>Guides</h3><p style="margin:0;color:var(--ink-2)">Four questions answered in the order that rules options out.</p>
    </a>
  </div>
  <div class="record-note">
    <strong>Looking for a product page that 404s?</strong> One submitted link never resolved to a listing, so no page was built for it. The evidence is on the <a href="${href("/records/held-link/")}">held link page</a> and <a href="${href("/records/flagged/")}">Flagged for Review</a>.
  </div>
</div>`;
  return page({
    title: "Page not found | " + site.brand,
    description: "That page is not on the shelf. Browse the shop or the buying guides instead.",
    path: "/404/",
    body,
    noindex: true,
  });
}

// ---------------------------------------------------------------- sitemap, feed, robots

function sitemap() {
  const urls = [
    ["/", "1.0", "weekly"],
    ["/shop/", "0.9", "weekly"],
    ["/guides/", "0.9", "weekly"],
    ...products.map((p) => [productUrl(p), "0.8", "monthly"]),
    ...guides.map((g) => [guideUrl(g), "0.8", "monthly"]),
    ["/about/", "0.5", "monthly"],
    ["/summary/", "0.4", "monthly"],
    ["/records/", "0.5", "monthly"],
    ["/records/source-register/", "0.5", "monthly"],
    ["/records/product-intent/", "0.5", "monthly"],
    ["/records/compliance/", "0.5", "monthly"],
    ["/records/measurement/", "0.4", "monthly"],
    ["/records/campaign-ledger/", "0.4", "monthly"],
    ["/records/questions/", "0.5", "monthly"],
    ["/records/suggestions/", "0.4", "monthly"],
    ["/records/flagged/", "0.5", "monthly"],
    ["/records/held-link/", "0.3", "monthly"],
  ];
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls
  .map(
    ([u, pri, freq]) => `  <url>
    <loc>${abs(u)}</loc>
    <lastmod>2026-11-20</lastmod>
    <changefreq>${freq}</changefreq>
    <priority>${pri}</priority>
  </url>`
  )
  .join("\n")}
</urlset>
`;
}

function feed() {
  const items = [
    ...guides.map((g) => ({
      title: g.question,
      link: abs(guideUrl(g)),
      desc: g.dek,
      date: "Thu, 20 Nov 2026 09:00:00 +0000",
      cat: "Guide",
    })),
    ...products.map((p) => ({
      title: `${p.name}: what it is and who it suits`,
      link: abs(productUrl(p)),
      desc: p.oneLine,
      date: "Thu, 20 Nov 2026 08:00:00 +0000",
      cat: "Product",
    })),
  ];
  const xmlEsc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${xmlEsc(site.brand)}</title>
    <link>${site.baseUrl}/</link>
    <description>${xmlEsc(site.tagline)} Buying guides and new products from a small, honest kitchen shop. Sponsored Amazon links, clearly marked.</description>
    <language>${site.language}</language>
    <lastBuildDate>Thu, 20 Nov 2026 09:00:00 +0000</lastBuildDate>
    <atom:link href="${site.baseUrl}/feed.xml" rel="self" type="application/rss+xml"/>
${items
  .map(
    (i) => `    <item>
      <title>${xmlEsc(i.title)}</title>
      <link>${i.link}</link>
      <guid isPermaLink="true">${i.link}</guid>
      <category>${xmlEsc(i.cat)}</category>
      <pubDate>${i.date}</pubDate>
      <description>${xmlEsc(i.desc)}</description>
    </item>`
  )
  .join("\n")}
  </channel>
</rss>
`;
}

function robots() {
  return `# ${site.brand}
User-agent: *
Allow: /

# Preserved sections kept for the record, not part of the shop.
# One site is indexed: the canonical pages listed in sitemap.xml.
Disallow: /archive/
Disallow: /crisp/
Disallow: /docs/

Sitemap: ${site.baseUrl}/sitemap.xml
`;
}

// ---------------------------------------------------------------- run

emit("index.html", frontPage());
emit("shop/index.html", shopIndex());
products.forEach((p) => emit(`shop/${p.slug}/index.html`, productPage(p)));
emit("records/held-link/index.html", heldLinkPage());
emit("guides/index.html", guidesIndex());
guides.forEach((g) => emit(`guides/${g.slug}/index.html`, guidePage(g)));
emit("about/index.html", aboutPage());
emit("summary/index.html", summaryPage());
emit("records/index.html", recordsIndex());
emit("records/source-register/index.html", sourceRegister());
emit("records/product-intent/index.html", productIntent());
emit("records/compliance/index.html", compliancePage());
emit("records/measurement/index.html", measurementPage());
emit("records/campaign-ledger/index.html", ledgerPage());
emit("records/questions/index.html", questionsPage());
emit("records/suggestions/index.html", suggestionsPage());
emit("records/flagged/index.html", flaggedPage());
emit("404.html", notFound());

fs.writeFileSync(path.join(ROOT, "sitemap.xml"), sitemap(), "utf8");
fs.writeFileSync(path.join(ROOT, "feed.xml"), feed(), "utf8");
fs.writeFileSync(path.join(ROOT, "robots.txt"), robots(), "utf8");
fs.writeFileSync(path.join(ROOT, ".nojekyll"), "", "utf8");

console.log(`Built ${written.length} pages + sitemap, feed, robots, .nojekyll`);
written.forEach((w) => console.log("  " + w));
