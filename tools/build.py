#!/usr/bin/env python3
"""Build the static site.

Design intent: the disclosure strip and footer are generated once, in one
template function, so a new page cannot ship without them. Every product card
is rendered from src/data/products.json, so no figure can drift between pages.
"""

import html
import json
import pathlib
import shutil
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data"
SITE_NAME = "Crisp & Counter"
TRACKING_ID = "shopnow047c-20"
# The storefront built by the parallel sessions lives at the repo root. This
# publication is a section within it, so a reader can always get back.
STORE_HOME = "@STORE@"
BUILD_DATE = "2026-11-20"

# Canonical host. GitHub Pages serves this repository at this URL.
SITE_ROOT = "https://karagemop466-tech.github.io/Affil1"
BASE = "/crisp"
SITE_URL = SITE_ROOT + BASE

# Relative prefix per page depth. Root of the app is /crisp/; any page below it
# links back with ../ per level. Absolute root paths would break a project Pages
# deploy (which serves the repo under /Affil1/), so all links are relative.
def rel(path):
    depth = path.strip("/").count("/")
    if path.endswith("/") and path != "/":
        depth += 1
    return "../" * depth if depth else "./"

NAV = [
    ("", "Home"),
    ("guides/", "Buying guides"),
    ("compare/", "Compare"),
    ("products/", "All products"),
    ("about/", "About"),
]


def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return json.load(fh)


PRODUCTS = load("products.json")
COMPLIANCE = load("compliance.json")
QUESTIONS = load("questions-open.json")
SUGGESTIONS = load("suggestions.json")
FLAGS = load("flags.json")
EVENTS = load("events.json")

from content import GUIDES, COMPARE_ROWS, PRICE_BLANK_NOTE  # noqa: E402

PRODUCT_BY_ID = {p["id"]: p for p in PRODUCTS["products"]}


def esc(text):
    return html.escape(str(text), quote=True)


def short_title(p):
    """A human label. Built from brand + form, both of which are verified."""
    if p["brand"] and p["form"]:
        return f"{p['brand']} {p['form']}"
    return p.get("listing_title") or p["id"]


# ---------------------------------------------------------------- templates

def disclosure():
    return f"""<div class="disclosure" role="region" aria-label="Affiliate disclosure">
  <div class="wrap">
    <span class="tag">Disclosure</span>
    <span>As an Amazon Associate, {esc(SITE_NAME)} earns from qualifying purchases. Links to Amazon are affiliate links: if you buy through one, we may earn a commission at no extra cost to you. <a href="/about/#disclosure">Read the full disclosure</a>.</span>
  </div>
</div>"""


def masthead(active):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links.append(f'<a href="/{href}"{cur}>{esc(label)}</a>')
    return f"""<header class="masthead">
  <div class="masthead-inner">
    <a class="brand" href="/">Crisp <span class="amp">&amp;</span> Counter<span class="brand-tag">Kitchen buying guides</span></a>
    <nav class="nav" aria-label="Sections">
      {''.join(links)}
    </nav>
  </div>
</header>"""


def footer():
    return f"""<footer>
  <div class="wrap">
    <div class="foot-disclosure">
      <strong>Affiliate disclosure.</strong> {esc(SITE_NAME)} is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. As an Amazon Associate we earn from qualifying purchases. Prices and availability are set by Amazon and are not shown on this site, because we have no live product feed. Product capability statements are quoted from the seller's listing title; nothing on this site is a test result.
    </div>
    <div class="foot-grid">
      <div>
        <a class="foot-brand" href="/">Crisp <span class="amp">&amp;</span> Counter</a>
        <p style="margin:0 0 10px;max-width:34ch;color:var(--ink-2)">Plain-language buying guides for countertop cooking appliances. No prices we cannot stand behind, no verdicts we have not earned.</p>
        <p style="margin:0;font-size:.76rem;color:var(--ink-3)">Publishing ID: <span class="mono">{esc(TRACKING_ID)}</span></p>
      </div>
      <div>
        <h4>Read</h4>
        <ul>
          <li><a href="/guides/">Buying guides</a></li>
          <li><a href="/compare/">Compare the range</a></li>
          <li><a href="/products/">All products</a></li>
          <li><a href="/about/">About &amp; method</a></li>
        </ul>
      </div>
      <div>
        <h4>Registers</h4>
        <ul>
          <li><a href="/sources/">Source register</a></li>
          <li><a href="/suggestions/">Suggestion board</a></li>
          <li><a href="/questions/">Open questions</a></li>
          <li><a href="/flagged/">Flagged for review</a></li>
        </ul>
      </div>
      <div>
        <h4>Elsewhere</h4>
        <ul>
          <li><a href="/feed.xml">RSS feed</a></li>
          <li><a href="/sitemap.xml">Sitemap</a></li>
          <li><a href="@STORE@">Kitchen Notes storefront</a></li>
          <li><a href="/about/#privacy">Privacy &amp; cookies</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-legal">
      <p>&copy; {BUILD_DATE[:4]} {esc(SITE_NAME)}. Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates. This site is not endorsed by or affiliated with Amazon beyond participation in the Associates Program. Information is provided for general guidance and is not professional advice.</p>
      <p style="white-space:nowrap;color:var(--ink-3)">Built {BUILD_DATE}</p>
    </div>
  </div>
</footer>"""


def page(path, title, description, body, active="/", extra_head="", crumbs=None):
    """Write one page. Disclosure is always the first thing under the masthead."""
    canonical = SITE_URL + (path if path != "/" else "/")
    crumb_html = ""
    if crumbs:
        bits = []
        for href, label in crumbs:
            if href:
                bits.append(f'<a href="{href}">{esc(label)}</a>')
            else:
                bits.append(f"<span>{esc(label)}</span>")
        sep = '<span class="sep">/</span>'
        crumb_html = '<div class="wrap"><div class="crumbs">' + sep.join(bits) + '</div></div>'

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<link rel="alternate" type="application/rss+xml" title="{esc(SITE_NAME)}" href="/feed.xml">
<link rel="stylesheet" href="/assets/css/site.css">
<script src="/assets/js/events.js" defer></script>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%231b1a17'/%3E%3Ctext x='16' y='22' font-family='Georgia,serif' font-size='17' fill='%23c9743a' text-anchor='middle'%3EC%3C/text%3E%3C/svg%3E">
{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{masthead(active)}
{disclosure()}
{crumb_html}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""
    # Rewrite every root-absolute link to a document-relative one. A project
    # Pages deploy serves this repo under /Affil1/, so "/guides/" would resolve
    # to the domain root and 404. Relative links work at any mount point.
    prefix = rel(path)
    doc = re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{prefix or "./"}', doc)
    doc = doc.replace('url(/assets/', 'url(./assets/')
    doc = doc.replace("@STORE@", prefix + "../")

    out = (ROOT / BASE.strip("/") / path.lstrip("/") / "index.html") if path.endswith("/") \
        else (ROOT / BASE.strip("/") / path.lstrip("/"))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    return out


# ---------------------------------------------------------------- components

def badge(text, kind="none"):
    return f'<span class="badge {kind}">{esc(text)}</span>'


def product_link(p, label=None, cls="btn"):
    """An outbound button, or an honest disabled state if the listing is unknown.

    The supplied short link is used as the destination because that is the link
    the account owner supplied. The observed listing URL is published separately
    as a citation, not as the affiliate destination, so the two are never merged.
    """
    if not p.get("official_listing_url"):
        return (
            '<span class="btn" aria-disabled="true">Listing not identified</span>'
            '<p class="paid-note">No button shown: this supplied link never resolved '
            'to a product, so we cannot name what you would be buying.</p>'
        )
    label = label or "Check the listing"
    klass = "btn" if cls in ("btn", "") else f"btn {cls}"
    return (
        f'<a class="{klass}" href="{esc(p["supplied_link"])}" rel="sponsored nofollow noopener" '
        f'target="_blank">{esc(label)}<span class="sr-only"> at Amazon (affiliate link, opens in a new tab)</span></a>'
        f'<p class="paid-note"><strong>Paid link.</strong> We earn a commission if you buy.</p>'
    )


def spec_rows(p):
    rows = [
        ("Brand", p.get("brand") or ""),
        ("Category", (p.get("category_path") or "").split(" > ")[-1] if p.get("category_path") else ""),
        ("ASIN", f'<span class="asin">{esc(p["observed_redirect_asin"])}</span>' if p.get("observed_redirect_asin") else '<span class="asin missing">not identified</span>'),
        ("Price", ""),
        ("Rating", ""),
    ]
    out = []
    for k, v in rows:
        if v:
            out.append(f'<li><span class="k">{esc(k)}</span><span class="v">{v}</span></li>')
        else:
            out.append(f'<li><span class="k">{esc(k)}</span><span class="v" style="color:var(--ink-3);font-style:italic">not shown</span></li>')
    return "".join(out)


def product_card(p, rank=None):
    form = p.get("form") or ""
    rank_html = f'<span class="rank">{rank}</span>' if rank else ""
    title = p.get("listing_title") or "Listing could not be identified"
    claims = "".join(f'<li><span class="v">{esc(c)}</span></li>' for c in p.get("title_claims", [])[:4])
    return f"""<article class="card" id="{esc(p['id'])}">
  <div class="card-top">
    <span class="pill form">{esc(form) if form else 'unidentified'}</span>
    {rank_html}
  </div>
  <div class="brandline">{esc(p.get('brand') or 'Unknown brand')}</div>
  <h3 title="{esc(title)}">{esc(title)}</h3>
  <ul class="spec-list">
    {spec_rows(p)}
  </ul>
  {'<ul class="spec-list">' + claims + '</ul>' if claims else ''}
  <p class="blank-note">Price, rating and stock are left blank on purpose: Amazon permits them here only when it serves the data or it arrives through its API. <a href="/about/#why-blank">Why</a></p>
  <div class="card-foot">
    {product_link(p)}
  </div>
</article>"""


def inline_products(ids):
    cards = "".join(product_card(PRODUCT_BY_ID[i]) for i in ids if i in PRODUCT_BY_ID)
    return f'<div class="product-grid">{cards}</div>'


# ---------------------------------------------------------------- pages

def build_home():
    p1, p2, p3 = PRODUCT_BY_ID["P-01"], PRODUCT_BY_ID["P-02"], PRODUCT_BY_ID["P-03"]

    lead = f"""
<div class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <p class="kicker">Countertop cooking &middot; buying guides</p>
        <h1>Pick the air fryer that survives your kitchen.</h1>
        <p class="deck">Two shapes, three sizes, one honest question: which one fits the food you actually cook and the counter you actually have. We tell you what each listing claims, and what we could not confirm.</p>
        <div class="byline">
          <span>Updated {BUILD_DATE}</span><span class="dot">&middot;</span>
          <span>4 guides</span><span class="dot">&middot;</span>
          <span>0 prices published, on purpose</span>
        </div>
      </div>
      <div class="fp-panel">
        <p class="kicker" style="margin-bottom:12px">Start here</p>
        <ul class="spec-list">
          <li><span class="k">Deciding</span><span class="v"><a href="/guides/basket-or-oven-air-fryer/">Basket or oven-style?</a></span></li>
          <li><span class="k">Sizing</span><span class="v"><a href="/guides/air-fryer-capacity-checklist/">Capacity checklist</a></span></li>
          <li><span class="k">Living with it</span><span class="v"><a href="/guides/cleanup-and-counter-space/">Cleanup &amp; space</a></span></li>
          <li><span class="k">Shortlisting</span><span class="v"><a href="/compare/">Compare the range</a></span></li>
        </ul>
      </div>
    </div>
  </div>
</div>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>The shortlist</h2>
      <p>The three appliances in this set, described in the seller's own words. No stars, no prices, no invented scores.</p>
    </div>
    <div class="product-grid">
      {product_card(p1, '01')}
      {product_card(p2, '02')}
      {product_card(p3, '03')}
    </div>
    <p style="margin-top:22px;font-size:.82rem;color:var(--ink-3)">
      A fourth product, a wireless meat thermometer, belongs to the same cooking decision and is on the
      <a href="/products/">products page</a>. A fifth supplied link never resolved to a listing; that gap is
      <a href="/flagged/#FLG-014">published here</a> rather than filled in.
    </p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Buying guides</h2>
      <p>Written as questions, because that is how the decision arrives.</p>
    </div>
    {guide_rows()}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>The one thing we will not do</h2>
      <p>What this site refuses to publish, and why it is a rule rather than a gap.</p>
    </div>
    <div class="article-body">
      <p>Amazon allows a site to show a price only when Amazon serves the link that carries it, or when the figure comes through the Creators API or PA API. This site has neither, so it shows no price, no star rating, no review count and no stock status. Not because the numbers are hard to find, but because publishing them without that feed is prohibited and, more plainly, because a price that was true last month is a lie this month.</p>
      <p>The same discipline applies to the writing. Every capability sentence here is either quoted from the seller's listing title or left out. We have not tested these machines. We do not tell you which one cooks better, because we would be making that up.</p>
      <p><a class="btn ghost" href="/about/">How this site works &rarr;</a></p>
    </div>
  </div>
</section>
"""

    path = page("/", f"{SITE_NAME} — kitchen buying guides that admit what they don't know",
                "Plain-language buying guides for air fryers and countertop cooking appliances. No prices we cannot stand behind, no verdicts we have not earned.",
                lead, active="/")
    return path


def guide_rows():
    rows = []
    for i, (slug, g) in enumerate(GUIDES.items(), start=1):
        rows.append(f"""<a class="guide-row" href="/guides/{slug}/">
  <span class="guide-num">{i:02d}</span>
  <div>
    <h3>{esc(g['title'])}</h3>
    <p>{esc(g['deck'])}</p>
  </div>
  <span class="guide-meta"><span class="cl">{esc(g['cluster'])}</span>{g['minutes']} min</span>
</a>""")
    return f'<div class="guide-list">{"".join(rows)}</div>'


def build_guides_index():
    body = f"""
<div class="wrap">
  <div class="page-head">
    <h1>Buying guides</h1>
    <p>Four questions that come before the checkout page. Each one ends by stating what it does not claim, because a guide that cannot name its limits is an advertorial.</p>
  </div>
  {guide_rows()}
</div>"""
    return page("/guides/", f"Buying guides — {SITE_NAME}",
                "Question-shaped guides for choosing an air fryer: shape, capacity, cleanup and counter space, and multi-function claims.",
                body, active="/guides/", crumbs=[("/", "Home"), (None, "Buying guides")])


def build_guide(slug, g):
    others = [s for s in GUIDES if s != slug][:2]
    next_html = "".join(
        f'<a class="next-guide" href="/guides/{s}/"><span class="ng-lbl">Read next</span>'
        f'<strong>{esc(GUIDES[s]["title"])}</strong></a>' for s in others)

    body_html = g["body"].replace('<div class="product-inline" data-products="', '<div class="product-grid" data-products="')
    # expand inline product blocks
    def expand(m):
        ids = m.group(1).split(",")
        return inline_products(ids)
    body_html = re.sub(r'<div class="product-grid" data-products="([^"]+)"></div>', expand, body_html)

    body = f"""
<div class="wrap">
  <article>
    <div class="hero" style="border-bottom:0;padding-bottom:8px">
      <p class="kicker">{esc(g['cluster'])}</p>
      <h1>{esc(g['title'])}</h1>
      <p class="deck">{esc(g['deck'])}</p>
      <div class="byline">
        <span>{SITE_NAME} editorial</span><span class="dot">&middot;</span>
        <span>{g['minutes']} min read</span><span class="dot">&middot;</span>
        <span>Updated {BUILD_DATE}</span><span class="dot">&middot;</span>
        <span>Affiliate links, disclosed above</span>
      </div>
    </div>
    <div class="article-body">
      {body_html}
    </div>
    <div class="article-foot">
      <h2>How to read the product cards in this guide</h2>
      <p>Brand, category and ASIN were read from the Amazon listing each supplied link resolved to on {BUILD_DATE}. Capability statements are the seller's listing-title wording, not our findings. Price, rating, review count and stock are omitted because Amazon permits them only when it serves the data or it arrives through its API. Every gap is listed on the <a href="/flagged/">Flagged for review</a> page with its source.</p>
    </div>
    <div class="next-guides">{next_html}</div>
  </article>
</div>"""

    return page(f"/guides/{slug}/", f"{g['title']} — {SITE_NAME}", g["deck"], body,
                active="/guides/",
                crumbs=[("/", "Home"), ("/guides/", "Buying guides"), (None, g["title"][:48])])


def build_products():
    rows = []
    for p in PRODUCTS["products"]:
        asin = p.get("observed_redirect_asin")
        asin_cell = f'<span class="asin">{esc(asin)}</span>' if asin else '<span class="asin missing">not identified</span>'
        rows.append(f"""<tr>
  <td><strong>{esc(p['id'])}</strong></td>
  <td>{esc(p.get('brand') or '')}</td>
  <td style="min-width:260px">{esc(p.get('listing_title') or '') or '<span class="blank">—</span>'}</td>
  <td>{esc(p.get('form') or '') or '<span class="blank">—</span>'}</td>
  <td>{asin_cell}</td>
  <td><span class="mono">{esc(p['supplied_path_code'])}</span><br><span style="font-size:.72rem;color:var(--ink-3)">{p['supplied_path_code_length']} chars</span></td>
  <td>{badge('10 chars', 'ok') if asin and p.get('observed_redirect_asin_length') == 10 else badge('unresolved', 'bad')}</td>
</tr>""")

    cards = "".join(product_card(p) for p in PRODUCTS["products"])

    body = f"""
<div class="wrap">
  <div class="page-head">
    <h1>All products in this set</h1>
    <p>Five links were supplied. Four resolved to an identifiable Amazon listing; one did not. The table records what was observed, the card below each entry says what the listing claims, and nothing is filled in where the observation failed.</p>
  </div>

  <div class="note-box">
    <p><strong>Read the two identifier columns separately.</strong> The supplied code is what appeared in the link. The ASIN is what the destination page actually carries. On this set they are never the same string, because the supplied code is a short-link slug of nine characters, not a product identifier. They are stored in separate fields and are never merged.</p>
  </div>

  <div class="table-wrap">
    <table>
      <caption class="sr-only">Products supplied, with observed redirect identifiers</caption>
      <thead>
        <tr><th>Ref</th><th>Brand</th><th>Listing title (seller's wording)</th><th>Form</th><th>Observed ASIN</th><th>Supplied code</th><th>ASIN check</th></tr>
      </thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
  </div>

  <div class="section-head" style="margin-top:42px">
    <h2>Product cards</h2>
    <p>Price, rating and stock are blank throughout. That is the correct state, not an oversight.</p>
  </div>
  <div class="product-grid">{cards}</div>

  <h2 style="margin-top:46px">Why four cards and not five</h2>
  <p style="max-width:68ch">The fifth supplied link (<span class="mono">link.amazon/B0c8moW59</span>) returned Amazon's continue-shopping interstitial on every attempt, including repeats several minutes apart. That page is official, but it identifies no product. We could not name the item, its brand, or its category, so there is no card and no outbound button. A button pointing at something we cannot name would be the one thing this project is built to avoid. The gap is recorded as <a href="/flagged/#FLG-014">FLG-014</a> and will close as soon as someone reads the product off a normal browser session.</p>
</div>"""

    return page("/products/", f"All products — {SITE_NAME}",
                "The four identified products in this set, with observed ASINs, the seller's own capability wording, and every unverified field left blank.",
                body, active="/products/", crumbs=[("/", "Home"), (None, "All products")])


def build_compare():
    cols = ["P-01", "P-02", "P-03", "P-05"]
    head = "".join(
        f'<th>{esc(PRODUCT_BY_ID[c]["brand"])}<br><span style="font-weight:400;text-transform:none;letter-spacing:0;font-size:.7rem;color:var(--ink-3)">{esc(PRODUCT_BY_ID[c].get("form") or "")}</span></th>'
        for c in cols)
    body_rows = []
    for row in COMPARE_ROWS:
        cells = []
        for c in cols:
            v = row.get(c, "")
            if row["label"].startswith("Price"):
                cells.append('<td class="blank">not published</td>')
            else:
                cells.append(f"<td>{esc(v)}</td>")
        body_rows.append(f'<tr><th scope="row">{esc(row["label"])}</th>{"".join(cells)}</tr>')

    cards = "".join(product_card(PRODUCT_BY_ID[c]) for c in cols)

    body = f"""
<div class="wrap">
  <div class="page-head">
    <h1>Compare the range</h1>
    <p>Compared on the things a listing can actually tell you: shape, how many things cook at once, what the seller states, and who each machine suits. Deliberately not compared: which cooks better. We have not tested them.</p>
  </div>

  <div class="table-wrap">
    <table>
      <caption class="sr-only">Comparison of the four identified products</caption>
      <thead><tr><th>Decision</th>{head}</tr></thead>
      <tbody>{''.join(body_rows)}</tbody>
    </table>
  </div>
  <p style="font-size:.8rem;color:var(--ink-3);max-width:72ch">
    {esc(PRICE_BLANK_NOTE)}
  </p>

  <div class="callout" style="margin-top:30px">
    <p class="callout-label">How to use this table</p>
    <p>Read down, not across. Pick the row that describes the problem you have — counter width, two things at once, or a small kitchen — and let the column that satisfies it narrow the field. A table that names a winner is a table that has stopped being useful.</p>
  </div>

  <h2 style="margin-top:44px">What the sellers claim, in their own words</h2>
  <p style="max-width:68ch">These are listing-title claims. They are not measurements, and we have not verified any of them by testing. Where a claim could mislead if read as a measured fact, the guide for that decision says so.</p>
  <div class="product-grid" style="margin-top:22px">{cards}</div>

  <h2 style="margin-top:44px">What this page does not claim</h2>
  <p style="max-width:68ch">It does not rank the products. It does not state wattage, dimensions, weight, warranty, energy use or noise, because none of those could be confirmed for these units from an official source with the access available. See <a href="/flagged/#FLG-007">FLG-007</a> for the full list of missing specifications and what would close it.</p>
</div>"""

    return page("/compare/", f"Compare — {SITE_NAME}",
                "Side-by-side comparison of air fryer shapes and what each seller states, with prices deliberately omitted because no live feed is connected.",
                body, active="/compare/", crumbs=[("/", "Home"), (None, "Compare")])


def build_sources():
    rows = []
    for p in PRODUCTS["products"]:
        rows.append(f"""<tr>
  <td><strong>{esc(p['id'])}</strong></td>
  <td><a href="{esc(p['source'])}" rel="nofollow noopener" target="_blank" class="mono">{esc(p['supplied_link'].replace('https://',''))}</a></td>
  <td>{f'<a href="{esc(p["observed_source_url"])}" rel="nofollow noopener" target="_blank" class="mono">amazon.com/dp/{esc(p["observed_redirect_asin"])}</a>' if p.get('observed_source_url') else '<span class="blank">did not resolve</span>'}</td>
  <td>{f'<span class="asin">{esc(p["observed_redirect_asin"])}</span>' if p.get('observed_redirect_asin') else '<span class="asin missing">—</span>'}</td>
  <td>{esc(p.get('category_path') or '') or '<span class="blank">—</span>'}</td>
</tr>""")

    comp_rows = []
    for s in COMPLIANCE["sources"]:
        comp_rows.append(f"""<tr>
  <td><strong>{esc(s['id'])}</strong></td>
  <td>{esc(s['publisher'])}</td>
  <td style="min-width:240px">{esc(s['title'])}<br><span style="font-size:.74rem;color:var(--ink-3)">{esc(s.get('dated',''))}</span></td>
  <td style="min-width:300px;font-family:var(--serif);font-size:.83rem;color:var(--ink-2)">&ldquo;{esc(s['quote'])}&rdquo;</td>
  <td style="min-width:180px;font-size:.8rem">{esc(s['supports'])}</td>
  <td><a href="{esc(s['url'])}" rel="nofollow noopener" target="_blank">Open source</a></td>
</tr>""")

    ev_rows = []
    for e in EVENTS["events"]:
        ev_rows.append(f"""<tr>
  <td><strong>{esc(e['id'])}</strong></td>
  <td class="mono">{esc(e['name'])}</td>
  <td>{esc(e['fires_when'])}</td>
  <td class="mono" style="font-size:.76rem">{esc(', '.join(e['props']))}</td>
  <td>{esc(e['answers'])}</td>
  <td>{badge('not deployed', 'warn')}</td>
</tr>""")

    body = f"""
<div class="wrap">
  <div class="page-head">
    <h1>Source register</h1>
    <p>Everything this site asserts, and the official page it came from. Where a source could not be read, the row says so and the value is blank. This page exists so that any claim can be checked in two clicks rather than taken on trust.</p>
  </div>

  <h2>Product observations</h2>
  <p style="max-width:68ch;font-size:.92rem;color:var(--ink-2)">Each supplied link was requested on {BUILD_DATE}, redirects were followed, and the destination page was read. The ASIN column is what the destination page returned — observed, not assumed.</p>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Ref</th><th>Supplied link</th><th>Resolved destination</th><th>Observed ASIN</th><th>Category path</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
  </div>

  <h2 style="margin-top:44px">Policy and legal sources</h2>
  <p style="max-width:68ch;font-size:.92rem;color:var(--ink-2)">Direct quotations. Each row states what the quotation is being used to support, so a reviewer can check the inference and not just the text.</p>
  <div class="table-wrap">
    <table>
      <thead><tr><th>ID</th><th>Publisher</th><th>Document</th><th>Quoted text</th><th>What it supports</th><th>Link</th></tr></thead>
      <tbody>{''.join(comp_rows)}</tbody>
    </table>
  </div>

  <h2 id="events" style="margin-top:44px">Measurement events</h2>
  <p style="max-width:68ch;font-size:.92rem;color:var(--ink-2)">Five events, defined before any optimisation is attempted. None is live. Publishing the definitions now means the next decision can be argued from a schema instead of a feeling — and it makes clear that no data has been collected yet.</p>
  <div class="table-wrap">
    <table>
      <thead><tr><th>ID</th><th>Event</th><th>Fires when</th><th>Properties</th><th>Question it answers</th><th>State</th></tr></thead>
      <tbody>{''.join(ev_rows)}</tbody>
    </table>
  </div>

  <div class="note-box" style="margin-top:26px">
    <p><strong>Campaign ledger:</strong> empty by design. No conversion count, revenue figure or forecast appears anywhere on this site, because no authorised first-party report has been read. An empty ledger with defined columns is an honest starting position; a filled one would be fiction.</p>
  </div>

  <h2 style="margin-top:40px">What is not in this register</h2>
  <ul class="tick" style="max-width:68ch">
    <li>Commission rates — the rate card requires a sign-in. <a href="/flagged/#FLG-004">FLG-004</a></li>
    <li>Prices, ratings, review counts and stock — prohibited without an Amazon-served price feed. <a href="/flagged/#FLG-006">FLG-006</a></li>
    <li>Wattage, dimensions, weight, warranty — not obtainable from an official source here. <a href="/flagged/#FLG-007">FLG-007</a></li>
    <li>Search volume for any guide topic — never obtained, so never claimed. <a href="/flagged/#FLG-013">FLG-013</a></li>
  </ul>
</div>"""

    return page("/sources/", f"Source register — {SITE_NAME}",
                "Every observation and every policy claim on this site, with the official page it came from and a note on what was used to support what.",
                body, active="/sources/", crumbs=[("/", "Home"), (None, "Source register")])


def build_suggestions():
    order = ["shipped", "proposed", "blocked-on-account", "blocked-on-decision", "rejected"]
    counts = {k: sum(1 for s in SUGGESTIONS["suggestions"] if s["status"] == k) for k in order}
    filters = ['<span class="flbl">Filter</span>']
    filters.append('<button class="filter-btn" data-filter="all" aria-pressed="true">All <span style="opacity:.6">' + str(len(SUGGESTIONS["suggestions"])) + "</span></button>")
    for k in order:
        if counts[k]:
            label = k.replace("-", " ")
            filters.append(f'<button class="filter-btn" data-filter="{k}" aria-pressed="false">{esc(label)} <span style="opacity:.6">{counts[k]}</span></button>')

    items = []
    for s in SUGGESTIONS["suggestions"]:
        badge_kind = {"shipped": "ok", "proposed": "none", "blocked-on-account": "warn",
                      "blocked-on-decision": "warn", "rejected": "bad"}[s["status"]]
        note = s.get("shipped_note") or s.get("blocked_note") or ""
        note_lbl = "What shipped" if s["status"] == "shipped" else ("Why it is blocked" if s["status"].startswith("blocked") else "Note")
        if s["status"] == "rejected":
            note_lbl = "Why not"
        items.append(f"""<article class="sug" data-status="{esc(s['status'])}">
  <div class="sug-head">
    <span class="flag-id">{esc(s['id'])}</span>
    <h3>{esc(s['title'])}</h3>
    {badge(s['status'].replace('-', ' '), badge_kind)}
  </div>
  <div class="sug-scores">
    <span class="score">impact <b>{s['impact']}</b>/5</span>
    <span class="score">effort <b>{s['effort']}</b>/5</span>
    <span class="score">confidence <b style="font-weight:600">{esc(s['confidence'])}</b></span>
  </div>
  <p><span class="lbl">Why</span>{esc(s['why'])}</p>
  <p><span class="lbl">Evidence needed</span>{esc(s['evidence_needed'])}</p>
  <p><span class="lbl">{esc(note_lbl)}</span>{esc(note)}</p>
</article>""")

    body = f"""
<div class="wrap">
  <div class="page-head">
    <h1>Suggestion board</h1>
    <p>Eighteen proposals, scored, with what each one would change and what it would need before it is safe to ship. Four are blocked on things only the account owner can supply. One is rejected outright. Read the scores as an argument, not a gospel: impact is judged against this site's purpose, not against a generic growth playbook.</p>
  </div>

  <div class="note-box">
    <p><strong>How to review this board.</strong> Start with the two rows marked <em>rejected</em> and <em>blocked on account</em> — those are the ones where acting without information would cost money or trust. Then pick by the ratio of impact to effort. Nothing on this page has been implemented silently; what shipped is labelled shipped and says so.</p>
  </div>

  <div class="filters">{''.join(filters)}</div>
  <div id="sug-list">{''.join(items)}</div>

  <h2 style="margin-top:40px">The three that need a decision from you first</h2>
  <ol class="steps" style="max-width:68ch">
    <li><strong>Connect the API, or accept no prices forever.</strong> Without the Creators API or PA API the site cannot legally show a price, and price is the number readers want most. This is the single highest-leverage unblock on the board.</li>
    <li><strong>Run the one-link test.</strong> One product, one link, confirmed in the Associates click report. Everything downstream — scaling to five, writing more guides, buying a domain — is premature until that single click is observed.</li>
    <li><strong>Give the site an author.</strong> A name and two sentences buy more credibility than any redesign, and it is the one thing that cannot be generated.</li>
  </ol>
</div>
<script>
(function () {{
  var btns = document.querySelectorAll('.filter-btn');
  var items = document.querySelectorAll('#sug-list .sug');
  btns.forEach(function (b) {{
    b.addEventListener('click', function () {{
      var f = b.getAttribute('data-filter');
      btns.forEach(function (x) {{ x.setAttribute('aria-pressed', String(x === b)); }});
      items.forEach(function (it) {{
        it.style.display = (f === 'all' || it.getAttribute('data-status') === f) ? '' : 'none';
      }});
    }});
  }});
}})();
</script>"""

    return page("/suggestions/", f"Suggestion board — {SITE_NAME}",
                "Eighteen scored proposals for improving the site, each with the evidence it needs and what is blocking it, so a reviewer can choose a path before anything is built.",
                body, active="/suggestions/", crumbs=[("/", "Home"), (None, "Suggestion board")])


def build_questions():
    status_kind = {
        "answered": "ok", "partly-answered": "warn", "blocked-on-account": "bad",
        "blocked-on-decision": "warn", "needs-routine": "none",
    }
    rows = []
    for q in QUESTIONS["questions"]:
        flag = f'<a href="/flagged/#{esc(q["flag"])}">{esc(q["flag"])}</a>' if q.get("flag") else '<span class="blank">—</span>'
        src = f'<a href="{esc(q["source"])}" rel="noopener" target="_blank">Source</a>' if q.get("source", "").startswith("http") else esc(q.get("source", ""))
        rows.append(f"""<tr>
  <td><strong>{esc(q['id'])}</strong></td>
  <td style="min-width:240px">{esc(q['question'])}</td>
  <td style="min-width:220px">{esc(q['needed_info'])}</td>
  <td style="min-width:240px">{esc(q['answer'])}</td>
  <td>{badge(q['status'].replace('-', ' '), status_kind.get(q['status'], 'none'))}</td>
  <td style="min-width:220px">{esc(q['how_to_unblock'])}</td>
  <td>{flag}</td>
</tr>""")

    answered = sum(1 for q in QUESTIONS["questions"] if q["status"] == "answered")
    blocked = sum(1 for q in QUESTIONS["questions"] if q["status"].startswith("blocked"))

    body = f"""
<div class="wrap">
  <div class="page-head">
    <h1>Questions that need answers before decisions</h1>
    <p>Fourteen questions, each with the information required to answer it and a plain statement of whether this session could. {answered} are answered. {blocked} are blocked, and none of them is blocked for want of effort — they are blocked because the answer needs an account, a decision or a person.</p>
  </div>

  <div class="note-box">
    <p><strong>The rule behind this table.</strong> A blocked question is not an invitation to guess. Where the answer is unknown, the value on the site is blank and the row below says why. That is why a product card shows no price and a guide names no winner.</p>
  </div>

  <div class="table-wrap">
    <table>
      <thead><tr><th>ID</th><th>Question</th><th>Information needed</th><th>What we know</th><th>State</th><th>How to unblock</th><th>Flag</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
  </div>

  <h2 style="margin-top:40px">Missing information, grouped by who can supply it</h2>
  <div class="compare-two">
    <div class="compare-col">
      <h3>Only the account owner can supply</h3>
      <ul class="tick">
        <li>Whether each link carries the tracking ID</li>
        <li>Whether the short links are compliant Special Links</li>
        <li>The intended ASIN for each product</li>
        <li>The commission rate for each category</li>
        <li>Search Console access for the domain</li>
        <li>API credentials, if live prices are wanted</li>
      </ul>
    </div>
    <div class="compare-col">
      <h3>Only a decision can supply</h3>
      <ul class="tick">
        <li>The publishing name and author identity</li>
        <li>Whether the site will ever test products</li>
        <li>Whether a third-party analytics provider is acceptable</li>
        <li>Whether the site stays on the Pages URL or gets a domain</li>
        <li>Whether email capture is worth the compliance surface</li>
      </ul>
    </div>
  </div>

  <h2 style="margin-top:36px">What could be answered from here, and was</h2>
  <p style="max-width:68ch;font-size:.94rem;color:var(--ink-2)">Four questions had official answers available to anyone, so they are answered rather than deferred: what the FTC requires of an affiliate disclosure, whether a price comparison table is permitted without a feed, what the program requires of a Special Link, and what state this repository was in. Those are in the table above with the source page for each.</p>
</div>"""

    return page("/questions/", f"Open questions — {SITE_NAME}",
                "Fourteen questions with the information needed to answer each, which ones are answered, and exactly what would unblock the rest.",
                body, active="/questions/", crumbs=[("/", "Home"), (None, "Open questions")])


def build_flagged():
    order = {"high": 0, "medium": 1, "low": 2}
    flags = sorted(FLAGS["flags"], key=lambda f: (order[f["severity"]], f["id"]))
    items = []
    for f in flags:
        items.append(f"""<article class="flag sev-{esc(f['severity'])}" id="{esc(f['id'])}">
  <div class="flag-head">
    <span class="flag-id">{esc(f['id'])}</span>
    <h3>{esc(f['title'])}</h3>
    {badge(f['severity'], 'bad' if f['severity'] == 'high' else ('warn' if f['severity'] == 'medium' else 'none'))}
  </div>
  <dl>
    <dt>What we observed</dt><dd>{esc(f['what_we_saw'])}</dd>
    <dt>Why it matters</dt><dd>{esc(f['why_it_matters'])}</dd>
    <dt>What we could not determine</dt><dd>{esc(f['what_we_could_not_determine'])}</dd>
    <dt>Source</dt><dd>{'<a href="' + esc(f['source']) + '" rel="nofollow noopener" target="_blank">' + esc(f['source']) + '</a>' if f['source'].startswith('http') else '<span class="mono" style="font-size:.78rem">' + esc(f['source']) + '</span>'}</dd>
    <dt>What you can do</dt><dd>{esc(f['review_action'])}</dd>
  </dl>
</article>""")

    high = sum(1 for f in flags if f["severity"] == "high")
    med = sum(1 for f in flags if f["severity"] == "medium")

    body = f"""
<div class="wrap">
  <div class="page-head">
    <h1>Flagged for review</h1>
    <p>Everything this project could not confirm, and every irregularity found while checking. {len(flags)} items: {high} high severity, {med} medium. None of them blocks publication, and none of them is hidden — each states what was observed, what was checked, what it means, and what would resolve it.</p>
  </div>

  <div class="note-box">
    <p><strong>Why these are published rather than fixed.</strong> Every item below needs something this session does not have: an Associates dashboard, an API credential, a real name, or a product page that will load. Inventing a plausible value would have made the site look finished and made it wrong. Leaving the value blank and saying so is the only version of this page that survives being checked.</p>
  </div>

  <div class="filters">
    <span class="flbl">Jump to</span>
    <a class="filter-btn" href="#FLG-001">Identifier &amp; tracking</a>
    <a class="filter-btn" href="#FLG-006">Data we do not publish</a>
    <a class="filter-btn" href="#FLG-009">Measurement</a>
    <a class="filter-btn" href="#FLG-013">Identity &amp; imagery</a>
  </div>

  {''.join(items)}

  <div class="section-head" style="margin-top:40px">
    <h2>How to clear this page</h2>
    <p>In the order that unblocks the most.</p>
  </div>
  <ol class="steps" style="max-width:68ch">
    <li><strong>Read one product off a browser session.</strong> That clears FLG-005 and FLG-014 and turns four products into five.</li>
    <li><strong>Click one link while signed in.</strong> That answers FLG-002 and FLG-003 with a measurement instead of an inference, and tells you whether any of this can earn.</li>
    <li><strong>Read the rate card.</strong> Clears FLG-004 and makes any future revenue statement possible.</li>
    <li><strong>Decide on the API.</strong> Clears FLG-006, FLG-007 and FLG-015 at once, and is the only route to a page with prices and photographs.</li>
    <li><strong>Supply a name and a bio.</strong> Clears FLG-013 and gives readers a reason to trust the rest.</li>
  </ol>
</div>"""

    return page("/flagged/", f"Flagged for review — {SITE_NAME}",
                "Fifteen published irregularities and unverified values, each with the source examined, what it means, and what would resolve it.",
                body, active="/flagged/", crumbs=[("/", "Home"), (None, "Flagged for review")])


def build_about():
    body = f"""
<div class="wrap">
  <div class="page-head">
    <h1>About this site, and how it decides what to publish</h1>
    <p>A short, checkable account of the editorial rule, the disclosure, and why several obvious things are missing.</p>
  </div>

  <div class="article-body">
    <h2 id="disclosure">The disclosure</h2>
    <p>{esc(SITE_NAME)} participates in the Amazon Services LLC Associates Program. As an Amazon Associate, we earn from qualifying purchases. When you follow a link to Amazon from this site, we may receive a commission. It costs you nothing extra, and it does not change what Amazon charges you.</p>
    <p>The disclosure appears as a strip under the masthead on every page of this site, and again in the footer. That placement is deliberate. The U.S. Federal Trade Commission asks that an affiliate relationship be disclosed clearly and conspicuously, so that a reader can decide how much weight to give the recommendation. A disclosure buried at the bottom of a long page does not do that job.</p>
    <p>Every outbound link to Amazon on this site is marked as a paid link, carries <span class="mono">rel="sponsored"</span>, and opens in a new tab with that fact announced to screen readers. We do not use link cloaking, and we do not use a redirect that hides where a link goes.</p>

    <h2 id="why-blank">Why so much is blank</h2>
    <p>Three separate rules produce the white space on this site, and it is worth keeping them apart.</p>
    <ul class="tick">
      <li><strong>Prices, ratings and stock are prohibited without a feed.</strong> Amazon permits price and availability display only when Amazon serves the link carrying that data, or when the figure arrives through the Creators API or PA API. No such feed is connected here, so no price appears. A price copied from a page today is wrong within weeks, and wrong prices about a named product are a real problem, not a cosmetic one.</li>
      <li><strong>Specifications could not be confirmed.</strong> Wattage, dimensions, weight, warranty and noise are not stated in a citable form for these units with the access available. They are omitted rather than estimated.</li>
      <li><strong>We have not tested anything.</strong> So we do not rank the products or tell you which cooks better. A verdict without a test is a guess wearing a lab coat.</li>
    </ul>

    <h2>The editorial rule</h2>
    <p>One rule governs every sentence about a product on this site: <strong>a capability is stated only if it appears in the seller's own listing title.</strong> When you read &ldquo;6 quart, two baskets,&rdquo; that is the seller's claim, quoted. When you read &ldquo;check the swing of the door before you buy,&rdquo; that is advice about your kitchen, which needs no sourcing because it makes no claim about the product.</p>
    <p>Where a listing claim could be read as a measured fact and would mislead if it were, the guide says so in the same paragraph. Where the site cannot answer a question a reader will have, the guide names the question and tells you where to find the answer.</p>

    <h2>How the links are handled</h2>
    <p>Five links were supplied for this project. Each was followed and the destination was read. Four resolved to an identifiable listing; one did not, and rather than guess at it, that gap is published on the <a href="/flagged/">Flagged for review</a> page.</p>
    <p>Two identifiers are kept in strictly separate fields for every product: the code that appeared in the supplied link, and the ASIN that the destination page actually carries. They are never merged, because merging them would destroy the only record that could catch a link pointing at the wrong product. On this set they are never the same string — the supplied codes are nine characters, and an ASIN is ten.</p>

    <h2 id="privacy">Privacy and cookies</h2>
    <p>This site sets no cookies, writes nothing to your browser's storage, and loads no third-party script. There is no analytics running, because there is nowhere on a static host for a first-party collector to run and a third-party one was judged not worth the disclosure surface before there is traffic to measure. The measurement plan is published on the <a href="/sources/#events">source register</a> so that when it is switched on, you can see exactly what it would collect.</p>
    <p>Clicking a product link takes you to Amazon, where Amazon's own privacy notice applies. We receive no information about what you do after you leave this site.</p>

    <h2>Corrections</h2>
    <p>Everything factual on this site is traceable to an official page, listed on the <a href="/sources/">source register</a>. If something here is wrong, the more useful response is to say which row and which source contradicts it. Corrections are made to the data, and the page is rebuilt from the data, so a fix lands everywhere at once rather than on one page and not another.</p>

    <h2>What this site is not</h2>
    <p>It is not affiliated with Amazon beyond participation in the Associates Program. It is not a review site in the sense of having tested anything. It is not professional advice. It is a set of buying guides that would rather leave a cell empty than fill it with something you cannot check.</p>
  </div>
</div>"""

    return page("/about/", f"About &amp; method — {SITE_NAME}",
                "The disclosure, the editorial rule, why prices and specifications are blank, and exactly what this site does and does not collect.",
                body, active="/about/", crumbs=[("/", "Home"), (None, "About")])


def build_legacy():
    body = f"""
<div class="wrap">
  <div class="page-head">
    <h1>Registers and dashboard surfaces</h1>
    <p>The verification and review surfaces, kept reachable from the footer so the buyer-facing front page can stay buyer-facing.</p>
  </div>
  <div class="legacy-banner">
    <strong>Where this page came from.</strong> The front page was rebuilt to lead with the products rather than the audit trail. The audit trail is not gone, it moved here. One correction to the record: this repository had no earlier site to preserve &mdash; at the starting commit it held a single eight-byte README. Nothing was deleted. What this page collects is the register set built in this pass, so a reviewer can reach every surface from one place.
  </div>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Surface</th><th>What it holds</th><th>Open</th></tr></thead>
      <tbody>
        <tr><td>Products register</td><td>Identifiers, observed ASINs and the blank-field policy</td><td><a href="/products/">Open</a></td></tr>
        <tr><td>Compare</td><td>Form-factor and stated-claim comparison</td><td><a href="/compare/">Open</a></td></tr>
        <tr><td>Source register</td><td>Every observation and policy quotation, with its official link</td><td><a href="/sources/">Open</a></td></tr>
        <tr><td>Measurement events</td><td>The five defined events and the empty campaign ledger</td><td><a href="/sources/#events">Open</a></td></tr>
        <tr><td>Suggestion board</td><td>Eighteen scored proposals and what blocks each one</td><td><a href="/suggestions/">Open</a></td></tr>
        <tr><td>Open questions</td><td>Fourteen questions with the information needed to answer each</td><td><a href="/questions/">Open</a></td></tr>
        <tr><td>Flagged for review</td><td>Every unverified value and irregularity</td><td><a href="/flagged/">Open</a></td></tr>
      </tbody>
    </table>
  </div>
  <h2 style="margin-top:36px">Why these are not in the main navigation</h2>
  <p style="max-width:68ch">A reader deciding between two air fryers does not need a register of policy quotations. A reviewer does. Splitting them keeps one navigation group that reads like a shop, while leaving every register one click from the footer &mdash; which also means no dashboard surface is unreachable, only undemoted.</p>
</div>"""
    return page("/legacy/", f"Registers — {SITE_NAME}",
                "Every verification and review surface in one place, reachable from the footer so the front page can stay buyer-facing.",
                body, active="/", crumbs=[("/", "Home"), (None, "Registers")])


# ---------------------------------------------------------------- sitemap / feed

def build_sitemap():
    urls = ["/", "/guides/", "/compare/", "/products/", "/about/", "/sources/",
            "/suggestions/", "/questions/", "/flagged/", "/legacy/"]
    urls += [f"/guides/{s}/" for s in GUIDES]
    entries = []
    locs = []
    for u in urls:
        loc = SITE_URL + u
        locs.append(loc)
        entries.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{BUILD_DATE}</lastmod>\n"
            f"    <changefreq>{'weekly' if u in ('/', '/guides/') else 'monthly'}</changefreq>\n"
            f"    <priority>{'1.0' if u == '/' else ('0.8' if u.startswith('/guides') else '0.5')}</priority>\n  </url>\n")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(entries) + "</urlset>\n")
    (ROOT / "crisp" / "sitemap.xml").write_text(xml, encoding="utf-8")

    # Union into the repository sitemap that the storefront publishes, so search
    # engines reach this section too. Existing entries are preserved verbatim.
    root_map = ROOT / "sitemap.xml"
    if root_map.exists():
        existing = root_map.read_text(encoding="utf-8")
        have = set(re.findall(r"<loc>([^<]+)</loc>", existing))
        add = [loc for loc in locs if loc not in have]
        if add:
            block = "".join(
                f"  <url><loc>{loc}</loc><lastmod>{BUILD_DATE}</lastmod>"
                f"<changefreq>monthly</changefreq><priority>0.4</priority></url>\n" for loc in add)
            existing = existing.replace("</urlset>", block + "</urlset>")
            root_map.write_text(existing, encoding="utf-8")


def build_feed():
    items = []
    for slug, g in GUIDES.items():
        items.append(f"""  <item>
    <title>{esc(g['title'])}</title>
    <link>{SITE_URL}/guides/{slug}/</link>
    <guid isPermaLink="true">{SITE_URL}/guides/{slug}/</guid>
    <pubDate>Thu, 20 Nov 2026 09:00:00 +0000</pubDate>
    <category>{esc(g['cluster'])}</category>
    <description>{esc(g['deck'])}</description>
  </item>""")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{esc(SITE_NAME)}</title>
  <link>{SITE_URL}/</link>
  <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml" />
  <description>Plain-language buying guides for countertop cooking appliances.</description>
  <language>en-us</language>
  <lastBuildDate>Thu, 20 Nov 2026 09:00:00 +0000</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
"""
    (ROOT / "crisp" / "feed.xml").write_text(xml, encoding="utf-8")


def build_robots():
    (ROOT / "crisp" / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")


def build_404():
    body = """<div class="wrap"><div class="page-head"><h1>That page is not here</h1>
<p>The link may be old, or the page may have moved into the registers. Try the buying guides, or the source register if you were looking for a citation.</p></div>
<p><a class="btn ghost" href="/guides/">Buying guides &rarr;</a> <a class="btn ghost" href="/sources/">Source register &rarr;</a></p></div>"""
    out = ROOT / "404.html"
    page("/404.html", f"Not found — {SITE_NAME}", "Page not found.", body,
         extra_head='<meta name="robots" content="noindex">')


def main():
    # clear generated pages so a deleted page cannot linger
    for d in ["guides", "compare", "products", "about", "sources", "suggestions",
              "questions", "flagged", "legacy"]:
        p = ROOT / "crisp" / d
        if p.exists():
            shutil.rmtree(p)

    build_home()
    build_guides_index()
    for slug, g in GUIDES.items():
        build_guide(slug, g)
    build_compare()
    build_products()
    build_about()
    build_sources()
    build_suggestions()
    build_questions()
    build_flagged()
    build_legacy()
    build_sitemap()
    build_feed()
    build_robots()
    build_404()

    js_dst = ROOT / "crisp" / "assets" / "js" / "events.js"
    js_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "assets" / "js" / "events.js", js_dst)

    dst = ROOT / "crisp" / "assets" / "css" / "site.css"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "assets" / "css" / "site.css", dst)

    n = len(list((ROOT / "crisp").rglob("*.html")))
    print(f"built {n} pages under /crisp/")


if __name__ == "__main__":
    main()
