#!/usr/bin/env python3
"""Deterministic static site builder for edition/ from platform/data/*.json."""

from __future__ import annotations

import html
import json
import pathlib
import posixpath
import sys
from typing import Any

PLATFORM_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = PLATFORM_DIR.parent
DATA_DIR = PLATFORM_DIR / "data"
EDITION_DIR = ROOT_DIR / "edition"

sys.path.insert(0, str(PLATFORM_DIR))
from compliance_gate import EXACT_ASSOCIATES_DISCLOSURE, validate_data_layer  # noqa: E402
from edition_assets import ANALYTICS_JS, APP_JS, STYLE_CSS, SVG_ASSETS  # noqa: E402

SITE_TITLE = "Countertop Almanac"
SITE_SUBTITLE = "Kitchen Equipment Publication & Verification Desk"
BASE_URL = "https://karagemop466-tech.github.io/Affil1/edition"
BUILD_DATE = "2026-11-20"

PRIMARY_NAV = [
    ("index.html", "Shop Shortlist"),
    ("categories/index.html", "Categories"),
    ("guides/index.html", "Buying Guides"),
    ("compare/index.html", "Compare"),
    ("suggestions/index.html", "Decision Desk"),
]


def esc(val: Any) -> str:
    if val is None:
        return ""
    return html.escape(str(val), quote=True)


def rel_href(from_rel_page: str, to_rel_target: str) -> str:
    from_dir = posixpath.dirname(from_rel_page)
    return posixpath.relpath(to_rel_target, from_dir or ".")


def canonical_url(rel_page: str) -> str:
    if rel_page == "index.html":
        return f"{BASE_URL}/"
    if rel_page.endswith("/index.html"):
        return f"{BASE_URL}/{rel_page[:-len('index.html')]}"
    return f"{BASE_URL}/{rel_page}"


def buy_href(prod: dict[str, Any]) -> str:
    """The only Amazon destination the annex may offer as a buy path.

    ``submitted_url`` is the short link the owner supplied. It stays on the page as
    the artefact under verification, printed and never linked, because the register
    records its redirect as unstable (several re-checks returned the Amazon homepage
    or a checkpoint page rather than a listing). The observed /dp/ listing is the
    destination a reader can actually be sent to, and it is the same rule the root
    site enforces through ``permitted_amazon_urls`` in _tools/layout.py: an
    unvalidated short link is not a monetisation path. If the account ever issues a
    Special Link, that approved URL wins, exactly as it does at the root.
    """
    intent = prod.get("intent_confirmation") or {}
    approved = intent.get("validated_special_link_url") or intent.get("approved_special_link")
    if approved:
        return approved
    return prod["observed_redirect"]["observed_redirect_url"]


def evidence_ref(prod: dict[str, Any]) -> str:
    """The supplied short link, as evidence: shown, not clickable.

    A reader who wants to re-run the check can copy it; a reader who wants to buy
    gets the listing. Linking the short link is what sent people to Amazon's home
    page, which is a broken buy path on a page whose whole claim is that the links
    were checked.
    """
    return f'<code>{esc(prod["submitted_url"])}</code>'


def sponsored_link(
    url: str,
    label: str,
    *,
    cls: str = "",
    track_event: str | None = None,
    product_id: str | None = None,
    guide_slug: str | None = None,
) -> str:
    attrs = [
        f'href="{esc(url)}"',
        'rel="sponsored nofollow noopener"',
        'target="_blank"',
    ]
    if cls:
        attrs.append(f'class="{esc(cls)}"')
    if track_event:
        attrs.append(f'data-track-event="{esc(track_event)}"')
    if product_id:
        attrs.append(f'data-product-id="{esc(product_id)}"')
    if guide_slug:
        attrs.append(f'data-guide-slug="{esc(guide_slug)}"')
    return f'<a {" ".join(attrs)}>{label}</a>'


def official_link(url: str, label: str, *, cls: str = "") -> str:
    # If an official source happens to be an Amazon /dp/ product listing, keep it marked sponsored
    # so 100% of outbound product links carry rel="sponsored".
    if "link.amazon/" in url or "amazon.com/dp/" in url:
        return sponsored_link(url, label, cls=cls)
    attrs = [f'href="{esc(url)}"', 'rel="noopener"', 'target="_blank"']
    if cls:
        attrs.append(f'class="{esc(cls)}"')
    return f'<a {" ".join(attrs)}>{label}</a>'


def blank_cell(flag_href: str, flag_code: str = "Unverified") -> str:
    return (
        f'<td class="cell-blank" data-unverified="true">'
        f'<a class="badge badge-warn" href="{esc(flag_href)}" title="Unconfirmed from official source — left blank">{esc(flag_code)}</a>'
        f"</td>"
    )


def render_source_badges(source_ids: list[str], sources_by_id: dict[str, dict[str, Any]]) -> str:
    links = []
    for sid in source_ids:
        src = sources_by_id[sid]
        links.append(official_link(src["url"], f"{esc(sid)} · {esc(src['publisher'])}"))
    return "<br>".join(links)


def render_shell(
    rel_page: str,
    *,
    title: str,
    description: str,
    body_html: str,
    active_nav: str,
    include_canonical: bool = True,
) -> str:
    css_href = rel_href(rel_page, "assets/style.css")
    fav_href = rel_href(rel_page, "assets/img/favicon.svg")
    feed_href = rel_href(rel_page, "feed.xml")
    analytics_src = rel_href(rel_page, "assets/analytics.js")
    app_src = rel_href(rel_page, "assets/app.js")
    home_href = rel_href(rel_page, "index.html")
    root_store_href = posixpath.relpath("..", posixpath.dirname(rel_page) or ".") + "/index.html"
    if posixpath.dirname(rel_page) == "":
        root_store_href = "../index.html"

    nav_items = []
    for target, label in PRIMARY_NAV:
        href = rel_href(rel_page, target)
        cur = ' aria-current="page"' if target == active_nav else ""
        nav_items.append(f'<a href="{esc(href)}"{cur}>{esc(label)}</a>')

    # This edition is a preserved, non-canonical duplicate: the maintained shop
    # publishes at the repository root. It stays reachable for review, but every
    # page tells a crawler not to index it, so two editions cannot compete for
    # the same query. A self-referencing canonical does not consolidate a second
    # copy of the same catalogue. Recorded as FLG-030.
    canon_tag = (
        f'\n  <link rel="canonical" href="{esc(canonical_url(rel_page))}">'
        if include_canonical
        else ""
    )
    canon_tag += '\n  <meta name="robots" content="noindex, follow">'

    page_slug = rel_page.replace("/index.html", "").replace(".html", "") or "home"

    # This edition is a maintained working copy, not a second shop. `edition/`
    # is served from the branch root like everything else, so without this it
    # presents itself to a crawler as a complete second publication with its own
    # sitemap — two sites competing for the same product pages, which is the
    # exact condition the canonical consolidation exists to prevent.
    #
    # Nothing is deleted: every page, guide and register stays readable, and
    # `noindex, follow` keeps its outbound links useful. Only the instruction to
    # index it is withdrawn. The Countertop Almanac stays reviewable at
    # /edition/ and its maintained data lives in _platform/data/.
    robots_tag = (
        '\n  <meta name="robots" content="noindex, follow">'
        '\n  <meta name="googlebot" content="noindex, follow">'
    )

    return f"""<!DOCTYPE html>
<html lang="en" data-page-slug="{esc(page_slug)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} — {esc(SITE_TITLE)}</title>
  <meta name="description" content="{esc(description)}">{canon_tag}{robots_tag}
  <link rel="icon" href="{esc(fav_href)}" type="image/svg+xml">
  <link rel="alternate" type="application/rss+xml" title="{esc(SITE_TITLE)} Buying Guides RSS" href="{esc(feed_href)}">
  <link rel="stylesheet" href="{esc(css_href)}">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <header class="site-header">
    <div class="container masthead-inner">
      <a class="brand" href="{esc(home_href)}">
        <img class="brand-mark" src="{esc(fav_href)}" alt="{esc(SITE_TITLE)} emblem" width="36" height="36">
        <span>
          <span class="brand-title">{esc(SITE_TITLE)}</span>
          <span class="brand-sub">{esc(SITE_SUBTITLE)}</span>
        </span>
      </a>
      <nav class="primary-nav" aria-label="Primary navigation">
        {" ".join(nav_items)}
      </nav>
    </div>
  </header>
  <div class="disclosure" role="note" aria-label="Affiliate disclosure">
    <div class="container disclosure-inner">
      <span><strong>{esc(EXACT_ASSOCIATES_DISCLOSURE)}</strong> Paid links to Amazon are marked <code>rel="sponsored"</code> (selected Tracking ID: <code>shopnow047c-20</code>).</span>
      <span class="disclosure-meta">
        <a href="{esc(rel_href(rel_page, 'compliance/index.html'))}">Disclosure &amp; API rules</a> ·
        <a href="{esc(rel_href(rel_page, 'flagged/index.html'))}">Flagged for Review</a>
      </span>
    </div>
  </div>
  <div class="annex-note" role="note">
    <div class="container annex-inner">
      <span><strong>This is the verification annex.</strong> The reader edition of this
      publication &mdash; the shop, the guides and the product notes &mdash; is published at
      the site root, and it is the copy this project asks search engines to read.</span>
      <a class="btn btn-sm" href="{esc(root_store_href)}">Go to the shop</a>
    </div>
  </div>
  <main id="main-content" class="container">
{body_html}
  </main>
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <h4>Shop &amp; Categories</h4>
          <ul>
            <li><a href="{esc(rel_href(rel_page, 'index.html'))}">Storefront Shortlist</a></li>
            <li><a href="{esc(rel_href(rel_page, 'categories/index.html'))}">All Categories</a></li>
            <li><a href="{esc(rel_href(rel_page, 'categories/air-fryers.html'))}">Countertop Air Fryers (3)</a></li>
            <li><a href="{esc(rel_href(rel_page, 'categories/thermometers.html'))}">Meat Thermometers (2)</a></li>
            <li><a href="{esc(rel_href(rel_page, 'compare/index.html'))}">Side-by-Side Comparison</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Buying Guides &amp; Feed</h4>
          <ul>
            <li><a href="{esc(rel_href(rel_page, 'guides/index.html'))}">All 8 Buying Guides</a></li>
            <li><a href="{esc(rel_href(rel_page, 'guides/basket-or-oven-air-fryer.html'))}">Basket vs Oven Air Fryer</a></li>
            <li><a href="{esc(rel_href(rel_page, 'guides/air-fryer-capacity-checklist.html'))}">Capacity Checklist</a></li>
            <li><a href="{esc(rel_href(rel_page, 'guides/thanksgiving-countertop-oven-relief.html'))}">Holiday Oven Relief</a></li>
            <li><a href="{esc(rel_href(rel_page, 'feed.xml'))}">RSS 2.0 Feed</a> · <a href="{esc(rel_href(rel_page, 'sitemap.xml'))}">XML Sitemap</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Decision &amp; Operations Desk</h4>
          <ul>
            <li><a href="{esc(rel_href(rel_page, 'suggestions/index.html'))}">Suggestions &amp; Design Prompt Studio</a></li>
            <li><a href="{esc(rel_href(rel_page, 'questions/index.html'))}">Pre-Decision Questions (12)</a></li>
            <li><a href="{esc(rel_href(rel_page, 'executive-summary/index.html'))}">Executive Summary</a></li>
            <li><a href="{esc(rel_href(rel_page, 'operations/index.html'))}">Measurement &amp; Empty Campaign Ledger</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Verification &amp; Governance</h4>
          <ul>
            <li><a href="{esc(rel_href(rel_page, 'products/index.html'))}">Product-Intent Confirmation Register</a></li>
            <li><a href="{esc(rel_href(rel_page, 'flagged/index.html'))}">Flagged for Review (10 + 6 Repo Audit)</a></li>
            <li><a href="{esc(rel_href(rel_page, 'compliance/index.html'))}">Official Sources &amp; Compliance Gate</a></li>
            <li><a href="{esc(root_store_href)}">Root Storefront Edition</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-disclosure">
        <p><strong>{esc(EXACT_ASSOCIATES_DISCLOSURE)}</strong> Outbound product links carry <code>rel="sponsored nofollow noopener"</code>. Prices, customer ratings, review counts, and live stock are shown only on Amazon in accordance with Amazon Associates Program Policies §2(b) and §6(t). Verified line by line on {esc(BUILD_DATE)}.</p>
      </div>
    </div>
  </footer>
  <script src="{esc(analytics_src)}" defer></script>
  <script src="{esc(app_src)}" defer></script>
</body>
</html>
"""


def render_product_card(
    rel_page: str,
    prod: dict[str, Any],
    *,
    guide_slug: str | None = None,
) -> str:
    ed = prod["editorial"]
    obs = prod["observed_redirect"]
    pid = prod["id"]
    tags = " ".join([prod["category"]] + ed["workflow_tags"])
    img_src = rel_href(rel_page, ed["illustration"])
    detail_href = rel_href(rel_page, f"products/{prod['slug']}.html")
    flag_href = rel_href(rel_page, "flagged/index.html#FLG-003")

    features_html = "".join(f"<li>{esc(f)}</li>" for f in ed["stated_features"])
    track_evt = "guide_to_product_click" if guide_slug else "product_card_click"

    cta_html = sponsored_link(
        buy_href(prod),
        "View it on Amazon (Paid link)",
        cls="btn btn-primary",
        track_event=track_evt,
        product_id=pid,
        guide_slug=guide_slug,
    )
    obs_link_html = sponsored_link(
        obs["observed_redirect_url"],
        f"Observed /dp/{esc(obs['observed_asin'])}",
    )

    return f"""    <article class="product-card" data-product-card data-tags="{esc(tags)}" id="card-{esc(pid)}">
      <div>
        <div class="card-top-meta">
          <span class="badge badge-info">{esc(pid)} · {esc(ed['role_badge'])}</span>
          <a class="badge badge-warn" href="{esc(flag_href)}">Intent &amp; tag unconfirmed</a>
        </div>
        <h3><a href="{esc(detail_href)}">{esc(ed['display_name'])}</a></h3>
        <div class="card-media">
          <img src="{esc(img_src)}" alt="{esc(ed['illustration_alt'])}" width="240" height="135" loading="lazy">
        </div>
        <div class="media-caption">Format diagram (not a product photo). Stated capacity: {esc(ed['stated_capacity'])}.</div>
        <ul class="spec-list">
          {features_html}
        </ul>
        <div class="fit-box">
          <p><strong>Fits best when:</strong> {esc(ed['best_fit_hypothesis'])}</p>
          <p><strong>Trade-off:</strong> {esc(ed['tradeoff_note'])}</p>
        </div>
      </div>
      <div>
        <div class="hero-actions">
          {cta_html}
          <a class="btn btn-secondary" href="{esc(detail_href)}">Verification dossier</a>
        </div>
        <div class="paid-microcopy">
          Paid link · Supplied URL: <code>{esc(prod['submitted_url'])}</code> · {obs_link_html} · Live price &amp; stock shown on Amazon.
        </div>
      </div>
    </article>"""


def build_home_page(
    products_doc: dict[str, Any],
    guides_doc: dict[str, Any],
    flags_doc: dict[str, Any],
    sources_by_id: dict[str, dict[str, Any]],
) -> str:
    rel_page = "index.html"
    cards = "\n".join(render_product_card(rel_page, p) for p in products_doc["products"])
    featured_guides = "\n".join(
        f"""    <article class="guide-card">
      <div>
        <span class="eyebrow">{esc(g['cluster'])}</span>
        <h3><a href="{esc(rel_href(rel_page, f'guides/{g["slug"]}.html'))}">{esc(g['title'])}</a></h3>
        <p>{esc(g['dek'])}</p>
      </div>
      <div>
        <span class="badge badge-ok">{esc(g['read_time'])}</span> ·
        <span class="badge badge-info">{esc(g['hypothesis_type'])}</span>
      </div>
    </article>"""
        for g in guides_doc["guides"][:6]
    )

    snap_rows = []
    for p in products_doc["products"]:
        obs = p["observed_redirect"]
        src = sources_by_id[obs["source_id"]]
        snap_rows.append(
            f"""        <tr>
          <td><strong><a href="{esc(rel_href(rel_page, f'products/{p["slug"]}.html'))}">{esc(p['id'])}</a></strong></td>
          <td>{esc(p['editorial']['display_name'])}</td>
          <td>{esc(p['editorial']['stated_capacity'])}</td>
          <td><code>{esc(obs['observed_asin'])}</code></td>
          {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-001'), 'Blank · FLG-001')}
          {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-004'), 'Blank · FLG-004')}
          <td>{official_link(src['url'], f"Amazon /dp/{esc(obs['observed_asin'])} ({esc(obs['source_id'])})")}</td>
        </tr>"""
        )

    body = f"""    <section class="hero">
      <span class="eyebrow">Weeknight &amp; Holiday Kitchen Shortlist · Verified {esc(BUILD_DATE)}</span>
      <h1>Choose the countertop cavity shape first — then check doneness with a real probe.</h1>
      <p class="lede">Five submitted Amazon links organized into two clear kitchen jobs: three countertop air-fryer formats (two 3-quart drawers, one 8-quart drawer, and a 26-quart French-door toaster oven) paired with two meat thermometers (instant-read spot check and 3-probe wireless). Every specification below is traced line by line to the live Amazon listing title; unconfirmed values stay blank and flagged.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="#shortlist">Browse the 5-product shortlist</a>
        <a class="btn btn-secondary" href="{esc(rel_href(rel_page, 'compare/index.html'))}">Compare side by side</a>
        <a class="btn btn-secondary" href="{esc(rel_href(rel_page, 'suggestions/index.html'))}">Review Suggestions &amp; Design Prompt</a>
      </div>
    </section>

    <section id="shortlist" aria-labelledby="shortlist-heading">
      <h2 id="shortlist-heading">Shoppable Shortlist &amp; Interactive Fit Finder</h2>
      <p>Filter the five submitted products by category or kitchen bottleneck. Prices, ratings, and stock status are intentionally blank here per Amazon Associates Program Policies §2(b) and shown live on Amazon.</p>
      <div class="filter-bar" data-filter-root data-filter-target="[data-product-card]">
        <span class="filter-label">Filter by kitchen job:</span>
        <button type="button" class="chip-btn" data-filter-value="all" aria-pressed="true">All 5 products</button>
        <button type="button" class="chip-btn" data-filter-value="air-fryers" aria-pressed="false">Air Fryers (3)</button>
        <button type="button" class="chip-btn" data-filter-value="thermometers" aria-pressed="false">Meat Thermometers (2)</button>
        <button type="button" class="chip-btn" data-filter-value="two-foods-at-once" aria-pressed="false">Two foods at once</button>
        <button type="button" class="chip-btn" data-filter-value="single-layer-batches" aria-pressed="false">Wide single-layer batches</button>
        <button type="button" class="chip-btn" data-filter-value="holiday-overflow" aria-pressed="false">Holiday oven overflow</button>
      </div>
      <div class="product-grid">
{cards}
      </div>
    </section>

    <section aria-labelledby="guides-heading">
      <h2 id="guides-heading">Question-Shaped &amp; Seasonal Buying Guides</h2>
      <p>Working editorial hypotheses designed around real kitchen geometry and seasonal bottlenecks — never fabricated search-volume or lab-ranking claims. <a href="{esc(rel_href(rel_page, 'guides/index.html'))}">Read all 8 guides</a> or subscribe via <a href="{esc(rel_href(rel_page, 'feed.xml'))}">RSS</a>.</p>
      <div class="guide-grid">
{featured_guides}
      </div>
    </section>

    <section aria-labelledby="snapshot-heading">
      <h2 id="snapshot-heading">At-a-Glance Verification Table</h2>
      <p>Every row links to its official Amazon source page verified on {esc(BUILD_DATE)}. Intended ASIN and live pricing remain blank until confirmed via Associates Central and Creators API / PA API.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Ref</th>
              <th>Observed Listing</th>
              <th>Seller-Stated Capacity</th>
              <th>Observed ASIN</th>
              <th>Intended ASIN</th>
              <th>Price / Rating / Stock</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
{chr(10).join(snap_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="panel" aria-labelledby="desk-gateway">
      <h2 id="desk-gateway">Decision Support, Governance &amp; Platform Desk</h2>
      <p>Review open blockers, select site and prompt upgrades before implementation, or inspect the empty Campaign Ledger and Flagged for Review register ({len(flags_doc['flags'])} product/policy flags + {len(flags_doc['repo_audit'])} repo audit items).</p>
      <div class="hero-actions">
        <a class="btn btn-secondary" href="{esc(rel_href(rel_page, 'suggestions/index.html'))}">Suggestions &amp; Prompt Workbench</a>
        <a class="btn btn-secondary" href="{esc(rel_href(rel_page, 'questions/index.html'))}">Pre-Decision Questions</a>
        <a class="btn btn-secondary" href="{esc(rel_href(rel_page, 'executive-summary/index.html'))}">Executive Summary</a>
        <a class="btn btn-secondary" href="{esc(rel_href(rel_page, 'flagged/index.html'))}">Flagged for Review</a>
      </div>
    </section>"""

    return render_shell(
        rel_page,
        title="Countertop Air Fryers & Meat Thermometers",
        description="Shoppable countertop air fryer and meat thermometer shortlist with line-by-line official Amazon verification, buyer guides, and decision desk.",
        body_html=body,
        active_nav="index.html",
    )


def build_categories_index(
    products_doc: dict[str, Any],
    sources_by_id: dict[str, dict[str, Any]],
) -> str:
    rel_page = "categories/index.html"
    rows = []
    cards = []
    for cat in products_doc["categories"]:
        src = sources_by_id[cat["source_id"]]
        cat_href = rel_href(rel_page, f"categories/{cat['slug']}.html")
        cards.append(
            f"""      <article class="guide-card">
        <div>
          <span class="eyebrow">{len(cat['product_ids'])} Submitted Links</span>
          <h3><a href="{esc(cat_href)}">{esc(cat['title'])}</a></h3>
          <p>{esc(cat['summary'])}</p>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary btn-sm" href="{esc(cat_href)}">Open {esc(cat['short_label'])}</a>
        </div>
      </article>"""
        )
        rows.append(
            f"""          <tr>
            <td><strong><a href="{esc(cat_href)}">{esc(cat['title'])}</a></strong></td>
            <td>{esc(", ".join(cat['product_ids']))}</td>
            <td>{esc(cat['summary'])}</td>
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-001'), 'Blank · FLG-001')}
            <td>{official_link(src['url'], f"Official Amazon category listing ({esc(cat['source_id'])})")}</td>
          </tr>"""
        )

    body = f"""    <section class="hero">
      <span class="eyebrow">Catalog Structure · FLG-007 Resolved by Explicit Grouping</span>
      <h1>Browse by Kitchen Category</h1>
      <p class="lede">Line-by-line breadcrumb inspection on {esc(BUILD_DATE)} confirmed that the five submitted links span two distinct Amazon departments: three countertop air fryers and two digital/wireless meat thermometers.</p>
    </section>
    <div class="guide-grid">
{chr(10).join(cards)}
    </div>
    <h2>Category Verification Summary</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Category</th>
            <th>Submitted Refs</th>
            <th>Observed Scope</th>
            <th>Confirmed Intended Count</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table>
    </div>"""
    return render_shell(
        rel_page,
        title="Product Categories",
        description="Countertop air fryers and meat thermometers organized into verified Amazon product categories.",
        body_html=body,
        active_nav="categories/index.html",
    )


def build_category_detail(
    cat: dict[str, Any],
    products_doc: dict[str, Any],
    sources_by_id: dict[str, dict[str, Any]],
) -> str:
    rel_page = f"categories/{cat['slug']}.html"
    cat_prods = [p for p in products_doc["products"] if p["category"] == cat["slug"]]
    cards = "\n".join(render_product_card(rel_page, p) for p in cat_prods)

    rows = []
    for p in cat_prods:
        obs = p["observed_redirect"]
        src = sources_by_id[obs["source_id"]]
        rows.append(
            f"""          <tr>
            <td><strong><a href="{esc(rel_href(rel_page, f'products/{p["slug"]}.html'))}">{esc(p['id'])}</a></strong></td>
            <td><code>{esc(p['submitted_slug'])}</code> (9 chars)</td>
            <td><code>{esc(obs['observed_asin'])}</code> (10 chars)</td>
            <td>{esc(obs['listing_title_verbatim'])}</td>
            <td>{esc(obs['breadcrumb'])}</td>
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-001'), 'Blank · FLG-001')}
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-004'), 'Blank · FLG-004')}
            <td>{official_link(src['url'], f"Amazon /dp/{esc(obs['observed_asin'])}")}</td>
          </tr>"""
        )

    body = f"""    <section class="hero">
      <span class="eyebrow">Category Subpage · <a href="{esc(rel_href(rel_page, 'categories/index.html'))}">All Categories</a></span>
      <h1>{esc(cat['title'])}</h1>
      <p class="lede">{esc(cat['summary'])}</p>
    </section>
    <div class="product-grid">
{cards}
    </div>
    <h2>Line-by-Line Category Verification Table</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Ref</th>
            <th>Supplied Token</th>
            <th>Observed ASIN</th>
            <th>Verbatim Listing Title on Amazon ({esc(BUILD_DATE)})</th>
            <th>Observed Amazon Breadcrumb</th>
            <th>Intended ASIN</th>
            <th>Price &amp; Rating</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table>
    </div>"""
    return render_shell(
        rel_page,
        title=cat["title"],
        description=cat["summary"],
        body_html=body,
        active_nav="categories/index.html",
    )


def build_compare_page(
    products_doc: dict[str, Any],
    sources_by_id: dict[str, dict[str, Any]],
) -> str:
    rel_page = "compare/index.html"
    rows = []
    for p in products_doc["products"]:
        obs = p["observed_redirect"]
        ed = p["editorial"]
        src = sources_by_id[obs["source_id"]]
        tags = " ".join([p["category"], ed["format"]] + ed["workflow_tags"])
        cta = sponsored_link(
            buy_href(p),
            "Amazon listing (Paid link)",
            cls="btn btn-primary btn-sm",
            track_event="product_card_click",
            product_id=p["id"],
        )
        rows.append(
            f"""          <tr data-compare-row data-tags="{esc(tags)}">
            <td><strong><a href="{esc(rel_href(rel_page, f'products/{p["slug"]}.html'))}">{esc(p['id'])}</a></strong><br><span class="badge badge-info">{esc(ed['role_badge'])}</span></td>
            <td><strong>{esc(ed['display_name'])}</strong><br>{cta}</td>
            <td>{esc(ed['stated_capacity'])}</td>
            <td>{esc("; ".join(ed['stated_features']))}</td>
            <td>{esc(ed['best_fit_hypothesis'])}</td>
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-008'), 'Blank · FLG-008')}
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-004'), 'Blank · FLG-004')}
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-001'), 'Blank · FLG-001')}
            <td>{official_link(src['url'], f"Amazon /dp/{esc(obs['observed_asin'])}")}</td>
          </tr>"""
        )

    body = f"""    <section class="hero">
      <span class="eyebrow">Side-by-Side Comparison Matrix</span>
      <h1>Compare All Five Products Without Guessed Specs</h1>
      <p class="lede">Seller-stated capabilities sit beside explicitly blank cells for wattage, exterior dimensions, warranty, price, ratings, and intended ASIN — because none of those fields was verified through official manufacturer manuals or Creators API / PA API.</p>
    </section>
    <div class="filter-bar" data-filter-root data-filter-target="[data-compare-row]">
      <span class="filter-label">Filter rows:</span>
      <button type="button" class="chip-btn" data-filter-value="all" aria-pressed="true">All 5 rows</button>
      <button type="button" class="chip-btn" data-filter-value="air-fryers" aria-pressed="false">Air Fryers (3)</button>
      <button type="button" class="chip-btn" data-filter-value="thermometers" aria-pressed="false">Meat Thermometers (2)</button>
      <button type="button" class="chip-btn" data-filter-value="two-foods-at-once" aria-pressed="false">Dual-zone / multi-item</button>
      <button type="button" class="chip-btn" data-filter-value="holiday-overflow" aria-pressed="false">Holiday hosting</button>
    </div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Ref &amp; Format</th>
            <th>Observed Listing &amp; Paid Link</th>
            <th>Stated Capacity</th>
            <th>Seller-Title Stated Attributes</th>
            <th>Buyer Fit Hypothesis</th>
            <th>Wattage / Dimensions</th>
            <th>Price / Rating / Stock</th>
            <th>Intended ASIN</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table>
    </div>"""
    return render_shell(
        rel_page,
        title="Side-by-Side Product Comparison",
        description="Line-by-line comparison matrix across all five submitted countertop air fryer and meat thermometer links.",
        body_html=body,
        active_nav="compare/index.html",
    )


def build_products_register(
    products_doc: dict[str, Any],
    sources_by_id: dict[str, dict[str, Any]],
) -> str:
    rel_page = "products/index.html"
    s_asin = sources_by_id["S03"]
    s_pol = sources_by_id["S02"]

    intent_rows = []
    observed_rows = []
    for p in products_doc["products"]:
        obs = p["observed_redirect"]
        src = sources_by_id[obs["source_id"]]
        intent_rows.append(
            f"""          <tr>
            <td><strong><a href="{esc(rel_href(rel_page, f'products/{p["slug"]}.html'))}">{esc(p['id'])}</a></strong></td>
            <td>{evidence_ref(p)}</td>
            <td><code>{esc(p['submitted_slug'])}</code> ({p['submitted_slug_length']} chars)</td>
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-001'), 'Blank · FLG-001')}
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-001'), 'Blank · FLG-001')}
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-001'), 'Blank · FLG-001')}
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-001'), 'Blank · FLG-001')}
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-003'), 'Blank · FLG-003')}
            <td>{official_link(s_asin['url'], 'Amazon ASIN Spec (S03)')}<br>{official_link(s_pol['url'], 'Associates Policies §2 (S02)')}</td>
          </tr>"""
        )
        observed_rows.append(
            f"""          <tr>
            <td><strong><a href="{esc(rel_href(rel_page, f'products/{p["slug"]}.html'))}">{esc(p['id'])}</a></strong></td>
            <td><code>{esc(obs['observed_asin'])}</code> ({obs['observed_asin_length']} chars)</td>
            <td>{sponsored_link(obs['observed_redirect_url'], f"/dp/{esc(obs['observed_asin'])}")}</td>
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-002'), 'None observed · FLG-002')}
            <td>{esc(obs['observed_date'])}</td>
            <td>{esc(obs['historical_observations'])}</td>
            <td>{official_link(src['url'], f"Amazon /dp/{esc(obs['observed_asin'])} ({esc(obs['source_id'])})")}</td>
          </tr>"""
        )

    body = f"""    <section class="hero">
      <span class="eyebrow">Strict Schema Separation · S03 ASIN Invariant</span>
      <h1>Product-Intent Confirmation Record vs Observed Redirect Targets</h1>
      <p class="lede">Per project governance and Amazon's 10-character ASIN specification, operator intent fields (<code>intended_asin</code>, <code>official_listing_url</code>, <code>confirmation_date</code>, <code>confirmation_source</code>) are stored separately from observed redirect destinations and are never merged.</p>
    </section>

    <h2>Table A — Product-Intent Confirmation Record (Operator-Owned Fields)</h2>
    <p>All five confirmation fields remain blank and flagged until the Associates account holder confirms the intended 10-character ASIN and tests a generated Special Link in Associates Central.</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Ref</th>
            <th>Submitted Short Link (Paid Link)</th>
            <th>Path Token</th>
            <th>Intended ASIN (10-char)</th>
            <th>Official Listing URL</th>
            <th>Confirmation Date</th>
            <th>Confirmation Source</th>
            <th>Validated Special Link</th>
            <th>Official Policy / Spec Source</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(intent_rows)}
        </tbody>
      </table>
    </div>

    <h2>Table B — Observed Redirect Target Record (Dated Verification Evidence)</h2>
    <p>Observed on {esc(BUILD_DATE)} via redirect-following fetch. Supplied short links are not claimed to be invalid; their Associates Special Link compliance status remains unresolved in <a href="{esc(rel_href(rel_page, 'flagged/index.html#FLG-003'))}">FLG-003</a>.</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Ref</th>
            <th>Observed ASIN</th>
            <th>Observed Landing URL</th>
            <th>Observed <code>tag=</code> Param</th>
            <th>Verified Date</th>
            <th>Cross-Session &amp; Historical Notes</th>
            <th>Official Listing Source</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(observed_rows)}
        </tbody>
      </table>
    </div>

    <section class="panel">
      <h2>Workflow to Replace Ambiguous Links with Validated Special Links</h2>
      <ol>
        <li>Sign into {official_link(sources_by_id['S14']['url'], 'Amazon Associates Central')} under account <code>shopnow047c-20</code> and confirm <code>https://karagemop466-tech.github.io/Affil1/</code> appears on the approved Website List ({official_link(s_pol['url'], 'Program Policies §1')}).</li>
        <li>Confirm the intended 10-character ASIN and exact variant for each row P-01..P-05 and populate <code>intent_confirmation</code> in <code>platform/data/products.json</code> without altering <code>observed_redirect</code>.</li>
        <li>Generate one canonical Special Link per confirmed ASIN using Associates Central / SiteStripe, verify destination resolution and click credit in Associates Reports (without self-purchasing per §6(u)), and only then set <code>validated_special_link_url</code>.</li>
      </ol>
    </section>"""
    return render_shell(
        rel_page,
        title="Product-Intent Confirmation & Link Register",
        description="Separate product-intent confirmation records and observed Amazon redirect targets for P-01 through P-05.",
        body_html=body,
        active_nav="index.html",
    )


def build_product_detail(
    prod: dict[str, Any],
    products_by_id: dict[str, dict[str, Any]],
    guides_by_slug: dict[str, dict[str, Any]],
    sources_by_id: dict[str, dict[str, Any]],
) -> str:
    rel_page = f"products/{prod['slug']}.html"
    ed = prod["editorial"]
    obs = prod["observed_redirect"]
    src = sources_by_id[obs["source_id"]]
    s_pol = sources_by_id["S02"]
    s_asin = sources_by_id["S03"]
    paired = products_by_id[ed["paired_product"]]

    guide_links = "".join(
        f'<li><a href="{esc(rel_href(rel_page, f"guides/{gslug}.html"))}">{esc(guides_by_slug[gslug]["title"])}</a></li>'
        for gslug in ed["related_guides"]
        if gslug in guides_by_slug
    )

    cta = sponsored_link(
        buy_href(prod),
        "Open the Amazon listing (Paid link)",
        cls="btn btn-primary",
        track_event="product_card_click",
        product_id=prod["id"],
    )

    body = f"""    <section class="hero">
      <span class="eyebrow"><a href="{esc(rel_href(rel_page, 'products/index.html'))}">Product Register</a> · {esc(prod['id'])} · {esc(ed['role_badge'])}</span>
      <h1>{esc(ed['display_name'])}</h1>
      <p class="lede">Observed Amazon title ({esc(obs['observed_date'])}): <em>“{esc(obs['listing_title_verbatim'])}”</em></p>
      <div class="hero-actions">
        {cta}
        <a class="btn btn-secondary" href="{esc(rel_href(rel_page, f'products/{paired["slug"]}.html'))}">Pairs with {esc(paired['id'])}: {esc(paired['editorial']['display_name'])}</a>
      </div>
      <p class="paid-microcopy">Paid link · <code>rel="sponsored nofollow noopener"</code> · Price, rating, review count, and stock are checked directly on Amazon.</p>
    </section>

    <div class="product-grid">
      <div class="panel">
        <div class="card-media">
          <img src="{esc(rel_href(rel_page, ed['illustration']))}" alt="{esc(ed['illustration_alt'])}" width="240" height="135">
        </div>
        <p class="media-caption">Editorial format illustration — not a manufacturer product photo.</p>
        <h3>Seller-Stated Listing Attributes</h3>
        <ul class="spec-list">
          {"".join(f"<li>{esc(f)}</li>" for f in ed["stated_features"])}
        </ul>
      </div>
      <div class="panel">
        <h3>Buyer Fit &amp; Kitchen Trade-Offs</h3>
        <p><strong>Fits best when:</strong> {esc(ed['best_fit_hypothesis'])}</p>
        <p><strong>When to pause or skip:</strong> {esc(ed['tradeoff_note'])}</p>
        <h3>Related Buying Guides</h3>
        <ul class="spec-list">{guide_links}</ul>
      </div>
    </div>

    <h2>Line-by-Line Verification Record ({esc(prod['id'])})</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Field</th>
            <th>Record Group</th>
            <th>Verified Value</th>
            <th>Status</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Submitted Short Link</td>
            <td>Submitted Input</td>
            <td>{evidence_ref(prod)} (9-char token <code>{esc(prod['submitted_slug'])}</code>)</td>
            <td><span class="badge badge-warn">FLG-003 Unresolved</span></td>
            <td>{official_link(s_pol['url'], 'Associates Program Policies §2 (S02)')}</td>
          </tr>
          <tr>
            <td>Intended ASIN / Official Listing URL</td>
            <td>Product-Intent Record</td>
            <td class="cell-blank" data-unverified="true"><a class="badge badge-warn" href="{esc(rel_href(rel_page, 'flagged/index.html#FLG-001'))}">Blank · Unverified (FLG-001)</a></td>
            <td><span class="badge badge-warn">Needs Operator Confirmation</span></td>
            <td>{official_link(s_asin['url'], 'Amazon 10-Char ASIN Spec (S03)')}</td>
          </tr>
          <tr>
            <td>Observed Redirect ASIN &amp; URL</td>
            <td>Observed Redirect Record</td>
            <td><code>{esc(obs['observed_asin'])}</code> · {sponsored_link(obs['observed_redirect_url'], esc(obs['observed_redirect_url']))}</td>
            <td><span class="badge badge-ok">Observed {esc(obs['observed_date'])}</span></td>
            <td>{official_link(src['url'], f"Amazon /dp/{esc(obs['observed_asin'])} ({esc(obs['source_id'])})")}</td>
          </tr>
          <tr>
            <td>Observed Category Breadcrumb</td>
            <td>Observed Redirect Record</td>
            <td>{esc(obs['breadcrumb'])}</td>
            <td><span class="badge badge-ok">Observed {esc(obs['observed_date'])}</span></td>
            <td>{official_link(src['url'], f"Amazon /dp/{esc(obs['observed_asin'])} ({esc(obs['source_id'])})")}</td>
          </tr>
          <tr>
            <td>Observed Redirect <code>tag=</code> Parameter</td>
            <td>Observed Redirect Record</td>
            <td class="cell-blank" data-unverified="true"><a class="badge badge-warn" href="{esc(rel_href(rel_page, 'flagged/index.html#FLG-002'))}">Blank · None on arrival (FLG-002)</a></td>
            <td><span class="badge badge-warn">Needs Associates Report Check</span></td>
            <td>{official_link(s_pol['url'], 'Associates Program Policies §2(b) (S02)')}</td>
          </tr>
          <tr>
            <td>Price, Star Rating, Reviews &amp; Stock</td>
            <td>API-Gated Commercial Data</td>
            <td class="cell-blank" data-unverified="true"><a class="badge badge-warn" href="{esc(rel_href(rel_page, 'flagged/index.html#FLG-004'))}">Blank · Omitted (FLG-004)</a></td>
            <td><span class="badge badge-warn">Requires Creators / PA API</span></td>
            <td>{official_link(s_pol['url'], 'Associates Policies §2(b) & §6(t) (S02)')}</td>
          </tr>
          <tr>
            <td>Wattage, Exterior Dimensions &amp; Warranty</td>
            <td>Technical Manual Specs</td>
            <td class="cell-blank" data-unverified="true"><a class="badge badge-warn" href="{esc(rel_href(rel_page, 'flagged/index.html#FLG-008'))}">Blank · Unverified (FLG-008)</a></td>
            <td><span class="badge badge-warn">Awaiting Brand Manual</span></td>
            <td>{official_link(sources_by_id['S05']['url'], '16 CFR Part 255 Substantiation (S05)')}</td>
          </tr>
        </tbody>
      </table>
    </div>"""
    return render_shell(
        rel_page,
        title=f"{prod['id']} · {ed['display_name']}",
        description=f"Verification dossier and buyer fit analysis for {ed['display_name']} ({obs['observed_asin']}).",
        body_html=body,
        active_nav="index.html",
    )


def build_guides_index(
    guides_doc: dict[str, Any],
    sources_by_id: dict[str, dict[str, Any]],
) -> str:
    rel_page = "guides/index.html"
    cards = []
    rows = []
    for g in guides_doc["guides"]:
        ghref = rel_href(rel_page, f"guides/{g['slug']}.html")
        first_src = sources_by_id[g["checklist_rows"][0]["source_id"]]
        cards.append(
            f"""      <article class="guide-card">
        <div>
          <span class="eyebrow">{esc(g['cluster'])}</span>
          <h3><a href="{esc(ghref)}">{esc(g['title'])}</a></h3>
          <p>{esc(g['dek'])}</p>
        </div>
        <div>
          <span class="badge badge-ok">{esc(g['read_time'])}</span> ·
          <span class="badge badge-info">{esc(g['hypothesis_type'])}</span>
        </div>
      </article>"""
        )
        rows.append(
            f"""          <tr>
            <td><strong><a href="{esc(ghref)}">{esc(g['title'])}</a></strong></td>
            <td>{esc(g['cluster'])}</td>
            <td>{esc(", ".join(g['featured_products']))}</td>
            <td><span class="badge badge-info">{esc(g['hypothesis_type'])}</span></td>
            <td>{official_link(first_src['url'], f"{esc(first_src['id'])} · {esc(first_src['publisher'])}")}<br>{official_link(sources_by_id['S07']['url'], 'S07 · Google Search Console')}</td>
          </tr>"""
        )

    body = f"""    <section class="hero">
      <span class="eyebrow">Editorial Buying Guides · Shipped in Sitemap &amp; RSS</span>
      <h1>Question-Shaped &amp; Seasonal Kitchen Guides</h1>
      <p class="lede">{esc(guides_doc['cadence_note'])}</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="{esc(rel_href(rel_page, 'feed.xml'))}">Subscribe via RSS 2.0</a>
        <a class="btn btn-secondary" href="{esc(rel_href(rel_page, 'operations/index.html'))}">See Search Console &amp; Click Measurement Plan</a>
      </div>
    </section>
    <div class="guide-grid">
{chr(10).join(cards)}
    </div>
    <h2>Editorial Cluster &amp; Verification Index</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Guide Working Title</th>
            <th>Buyer Cluster</th>
            <th>Products Referenced</th>
            <th>Hypothesis Classification</th>
            <th>Official Sources</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table>
    </div>"""
    return render_shell(
        rel_page,
        title="Buying Guides & Seasonal Kitchen Topics",
        description="Eight question-shaped and seasonal air fryer and meat thermometer buying guides backed by official sources.",
        body_html=body,
        active_nav="guides/index.html",
    )


def build_guide_page(
    guide: dict[str, Any],
    products_by_id: dict[str, dict[str, Any]],
    sources_by_id: dict[str, dict[str, Any]],
) -> str:
    rel_page = f"guides/{guide['slug']}.html"
    sections_html = []
    for sec in guide["sections"]:
        paras = "".join(f"<p>{esc(p)}</p>" for p in sec["paragraphs"])
        sections_html.append(f"      <h2>{esc(sec['heading'])}</h2>\n      {paras}")

    checklist_html = []
    for row in guide["checklist_rows"]:
        src = sources_by_id[row["source_id"]]
        checklist_html.append(
            f"""          <tr>
            <td><strong>{esc(row['check'])}</strong></td>
            <td>{esc(row['what_to_verify'])}</td>
            <td>{official_link(src['url'], f"{esc(src['id'])} · {esc(src['title'])}")}</td>
          </tr>"""
        )

    cards = "\n".join(
        render_product_card(rel_page, products_by_id[pid], guide_slug=guide["slug"])
        for pid in guide["featured_products"]
    )

    body = f"""    <article>
      <section class="hero">
        <span class="eyebrow"><a href="{esc(rel_href(rel_page, 'guides/index.html'))}">Buying Guides</a> · {esc(guide['cluster'])} · {esc(guide['read_time'])}</span>
        <h1>{esc(guide['title'])}</h1>
        <p class="lede">{esc(guide['dek'])}</p>
        <span class="badge badge-info">{esc(guide['hypothesis_type'])} — working editorial hypothesis, not a popularity or lab-test claim</span>
      </section>

      <div class="article-shell">
{chr(10).join(sections_html)}
      </div>

      <h2>Line-by-Line Verification Checklist for This Guide</h2>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Comparison Dimension</th>
              <th>Verified Fact vs Unverified Boundary</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
{chr(10).join(checklist_html)}
          </tbody>
        </table>
      </div>

      <h2>Referenced Products in This Guide</h2>
      <div class="product-grid">
{cards}
      </div>
    </article>"""
    return render_shell(
        rel_page,
        title=guide["title"],
        description=guide["dek"],
        body_html=body,
        active_nav="guides/index.html",
    )


def build_suggestions_page(
    suggestions_doc: dict[str, Any],
    sources_by_id: dict[str, dict[str, Any]],
) -> str:
    rel_page = "suggestions/index.html"
    rows = []
    for sg in suggestions_doc["suggestions"]:
        sid = sg["id"]
        default_dec = sg["default_decision"]
        rows.append(
            f"""          <tr id="{esc(sid)}" data-suggestion-row data-suggestion-id="{esc(sid)}" data-default-decision="{esc(default_dec)}">
            <td><strong><code>{esc(sid)}</code></strong><br><span class="badge badge-info">{esc(sg['track'])}</span></td>
            <td><strong>{esc(sg['title'])}</strong><br><span class="disclosure-meta">{esc(sg['problem'])}</span></td>
            <td>{esc(sg['proposal'])}</td>
            <td><code>{esc(sg['implementation_state'])}</code></td>
            <td>
              <div class="decision-group" role="group" aria-label="Decision for {esc(sid)}">
                <button type="button" class="btn btn-secondary btn-sm decision-btn" data-decision="approved" aria-pressed="{str(default_dec == 'approved').lower()}">Approve</button>
                <button type="button" class="btn btn-secondary btn-sm decision-btn" data-decision="hold" aria-pressed="{str(default_dec == 'hold').lower()}">Hold</button>
                <button type="button" class="btn btn-secondary btn-sm decision-btn" data-decision="rejected" aria-pressed="{str(default_dec == 'rejected').lower()}">Reject</button>
              </div>
            </td>
            <td>{render_source_badges(sg['source_ids'], sources_by_id)}</td>
          </tr>"""
        )

    module_boxes = []
    default_prompt_lines = [
        "Design and build a polished, trustworthy Amazon Associates culinary-equipment publication (Tracking ID: shopnow047c-20) that converts organic search readers without AI-slop filler or unverified claims.",
        "",
    ]
    for idx, mod in enumerate(suggestions_doc["prompt_modules"], start=1):
        checked = " checked" if mod["default_enabled"] else ""
        if mod["default_enabled"]:
            default_prompt_lines.append(f"{idx}. [{mod['id']}] {mod['prompt_instruction']}")
        module_boxes.append(
            f"""        <label class="module-item">
          <input type="checkbox" data-prompt-module data-module-id="{esc(mod['id'])}" data-prompt-text="{esc(mod['prompt_instruction'])}"{checked}>
          <strong>{esc(mod['id'])} · {esc(mod['label'])}</strong>
          <p class="disclosure-meta">{esc(mod['why_it_converts'])}</p>
        </label>"""
        )

    body = f"""    <section class="hero">
      <span class="eyebrow">Decision Review Board &amp; Prompt Engineering Workbench</span>
      <h1>Review Site Suggestions &amp; Assemble the Design Prompt</h1>
      <p class="lede">Select which site, measurement, SEO, and compliance improvements to approve, hold, or reject before changing production workflows — then generate a copy-ready, non-AI-slop site design and content prompt below.</p>
      <div class="hero-actions">
        <span class="badge badge-ok" id="suggestion-decision-summary">Review states loaded from verified defaults</span>
        <button type="button" class="btn btn-secondary btn-sm" id="export-decisions-btn">Export Decisions JSON</button>
        <a class="btn btn-secondary btn-sm" href="{esc(rel_href(rel_page, 'questions/index.html'))}">Open Pre-Decision Questions</a>
      </div>
    </section>

    <section aria-labelledby="prompt-studio-heading" class="panel">
      <span class="eyebrow">Prompt Feed · Anti-AI-Slop Storefront &amp; Organic Search Generator</span>
      <h2 id="prompt-studio-heading">Interactive Site Design &amp; Trendy Content Prompt Builder</h2>
      <p>Toggle the verified design, conversion-UX, seasonal topic-cluster, and Amazon/FTC compliance modules below to compose the exact prompt for iterating this affiliate publication.</p>
      <p>
        <label for="prompt-season-focus"><strong>Editorial &amp; Seasonal Focus:</strong></label>
        <select id="prompt-season-focus">
          <option value="Year-round weeknight dinners + November holiday oven-overflow hosting">Year-round weeknight dinners + November holiday hosting</option>
          <option value="Small-apartment countertop consolidation &amp; easy dishwasher cleanup">Small-apartment countertop consolidation &amp; cleanup</option>
          <option value="Precision protein doneness: pairing air fryers with instant &amp; wireless probes">Precision protein doneness (air fryer + meat thermometer pairing)</option>
          <option value="Game-day wings, crispy reheated leftovers &amp; dual-zone batching">Game-day batch cooking &amp; crispy leftovers</option>
        </select>
      </p>
      <div class="module-list">
{chr(10).join(module_boxes)}
      </div>
      <label for="generated-design-prompt"><strong>Assembled Design &amp; SEO Prompt (Copy-Ready):</strong></label>
      <textarea id="generated-design-prompt" class="prompt-output" readonly>{esc(chr(10).join(default_prompt_lines))}</textarea>
      <div class="hero-actions">
        <button type="button" class="btn btn-primary btn-sm" id="copy-prompt-btn">Copy Assembled Prompt</button>
        <span id="copy-prompt-status" class="disclosure-meta" aria-live="polite"></span>
      </div>
    </section>

    <section aria-labelledby="queue-heading">
      <h2 id="queue-heading">Dedicated Suggestions Queue (Approve / Hold / Reject Before Implementing)</h2>
      <p>Includes Priority Tracks 1–5, parallel polish items <code>SG-27..SG-30</code>, and policy-rejected anti-patterns (<code>SG-31..SG-32</code>). Decisions persist locally in your browser without transmitting personal data.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID &amp; Track</th>
              <th>Suggestion &amp; Problem Addressed</th>
              <th>Actionable Proposal</th>
              <th>Current State</th>
              <th>Operator Decision</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
{chr(10).join(rows)}
          </tbody>
        </table>
      </div>
    </section>"""
    return render_shell(
        rel_page,
        title="Suggestions Queue & Site Design Prompt Studio",
        description="Dedicated suggestions review queue and interactive anti-AI-slop affiliate website design prompt builder.",
        body_html=body,
        active_nav="suggestions/index.html",
    )


def build_questions_page(
    questions_doc: dict[str, Any],
    sources_by_id: dict[str, dict[str, Any]],
) -> str:
    rel_page = "questions/index.html"
    rows = []
    for q in questions_doc["questions"]:
        badge_cls = "badge-ok" if q["status"].startswith("answered") else "badge-warn"
        rows.append(
            f"""          <tr id="{esc(q['id'])}" data-q-row data-tags="{esc(q['status'])}">
            <td><strong><code>{esc(q['id'])}</code></strong><br><span class="badge {badge_cls}">{esc(q['status'])}</span></td>
            <td><strong>{esc(q['question'])}</strong><br><span class="disclosure-meta">Gate: {esc(q['gate'])}</span></td>
            <td>{esc(q['known'])}</td>
            <td>{esc(q['missing'])}</td>
            <td>{esc(q['current_answer'])}</td>
            <td>{esc(q['discovery_suggestion'])}</td>
            <td>{render_source_badges(q['source_ids'], sources_by_id)}</td>
          </tr>"""
        )

    body = f"""    <section class="hero">
      <span class="eyebrow">Pre-Decision Evidence Matrix · 12 Gate Questions</span>
      <h1>Questions, Known vs Missing Information &amp; Discovery Plan</h1>
      <p class="lede">Every question that must be answered before scaling ad spend, changing outbound Special Links, publishing technical measurements, or enabling live analytics — grounded strictly in what is verified today versus what remains missing.</p>
    </section>
    <div class="filter-bar" data-filter-root data-filter-target="[data-q-row]">
      <span class="filter-label">Filter by status:</span>
      <button type="button" class="chip-btn" data-filter-value="all" aria-pressed="true">All 12 questions</button>
      <button type="button" class="chip-btn" data-filter-value="needs-operator" aria-pressed="false">Needs Operator Account (7)</button>
      <button type="button" class="chip-btn" data-filter-value="needs-source-fetch" aria-pressed="false">Needs Brand Manual (1)</button>
      <button type="button" class="chip-btn" data-filter-value="answered-by-policy" aria-pressed="false">Answered by Policy</button>
      <button type="button" class="chip-btn" data-filter-value="answered-and-enforced" aria-pressed="false">Enforced in CI</button>
    </div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>ID &amp; State</th>
            <th>Decision Question</th>
            <th>What We Already Have (Verified)</th>
            <th>What We Do Not Have (Missing)</th>
            <th>Current Working Rule</th>
            <th>Suggestion to Discover Missing Info</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table>
    </div>"""
    return render_shell(
        rel_page,
        title="Pre-Decision Questions & Missing Information Discovery",
        description="Clear matrix of pre-decision questions, known facts, missing data, answers, and discovery actions.",
        body_html=body,
        active_nav="suggestions/index.html",
    )


def build_executive_summary_page(
    products_doc: dict[str, Any],
    flags_doc: dict[str, Any],
    questions_doc: dict[str, Any],
    suggestions_doc: dict[str, Any],
    sources_by_id: dict[str, dict[str, Any]],
) -> str:
    rel_page = "executive-summary/index.html"
    prod_rows = []
    for p in products_doc["products"]:
        obs = p["observed_redirect"]
        src = sources_by_id[obs["source_id"]]
        prod_rows.append(
            f"""          <tr>
            <td><strong><a href="{esc(rel_href(rel_page, f'products/{p["slug"]}.html'))}">{esc(p['id'])}</a></strong></td>
            <td>{evidence_ref(p)}</td>
            <td><code>{esc(obs['observed_asin'])}</code></td>
            <td>{esc(p['editorial']['display_name'])}</td>
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-001'), 'Blank · FLG-001')}
            {blank_cell(rel_href(rel_page, 'flagged/index.html#FLG-002'), 'Unconfirmed · FLG-002')}
            <td>{official_link(src['url'], f"Amazon /dp/{esc(obs['observed_asin'])}")}</td>
          </tr>"""
        )

    body = f"""    <section class="hero">
      <span class="eyebrow">Executive Briefing · Tracking ID <code>shopnow047c-20</code></span>
      <h1>Executive Summary</h1>
      <p class="lede">Verification posture, product portfolio findings, policy guardrails, automation architecture, and operator launch gates as of {esc(BUILD_DATE)}.</p>
    </section>

    <div class="kpi-strip">
      <div class="kpi-card"><span class="kpi-num">5 / 5</span><span class="kpi-label">Supplied links resolved to 10-char /dp/ ASINs on {esc(BUILD_DATE)}</span></div>
      <div class="kpi-card"><span class="kpi-num">0 / 5</span><span class="kpi-label">Intended ASINs or arrival <code>tag=</code> params confirmed (left blank)</span></div>
      <div class="kpi-card"><span class="kpi-num">8</span><span class="kpi-label">Question-shaped &amp; seasonal buyer guides in sitemap &amp; RSS</span></div>
      <div class="kpi-card"><span class="kpi-num">{len(flags_doc['flags']) + len(flags_doc['repo_audit'])}</span><span class="kpi-label">Flagged items &amp; repo audit findings published with sources</span></div>
      <div class="kpi-card"><span class="kpi-num">0</span><span class="kpi-label">Ledger orders, conversion scores, or revenue forecasts</span></div>
    </div>

    <h2>1. Submitted Product Links &amp; Verification Outcome</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Ref</th>
            <th>Submitted Short Link (Paid Link)</th>
            <th>Observed ASIN</th>
            <th>Observed Product Scope</th>
            <th>Intended ASIN</th>
            <th>Arrival Tag Status</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(prod_rows)}
        </tbody>
      </table>
    </div>

    <h2>2. Platform Capabilities vs Mandatory Human/API Gates</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Subsystem</th>
            <th>What Is Automated Today</th>
            <th>What Is Intentionally Gated</th>
            <th>Official Governing Source</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Storefront &amp; Static Build</strong> (<code>platform/build_edition.py</code>)</td>
            <td>Generates 22 mobile-ready pages, category subpages, comparison tables, <code>sitemap.xml</code>, and <code>feed.xml</code> with subpath-safe relative URLs.</td>
            <td>Never overwrites <code>intended_asin</code> with <code>observed_asin</code>.</td>
            <td>{official_link(sources_by_id['S03']['url'], 'S03 · Amazon ASIN Spec')}</td>
          </tr>
          <tr>
            <td><strong>Compliance Gate</strong> (<code>platform/compliance_gate.py</code> &amp; <code>verify_edition.py</code>)</td>
            <td>Fails CI if any page omits the verbatim §5 disclosure, omits <code>rel="sponsored"</code> on retail links, introduces dollar prices, or breaks an anchor.</td>
            <td>Prices, star ratings, review counts, stock, and price-alert widgets remain blocked until Creators API / PA API &amp; Amazon approval exist.</td>
            <td>{official_link(sources_by_id['S01']['url'], 'S01 · Operating Agreement §5')}<br>{official_link(sources_by_id['S02']['url'], 'S02 · Policies §2(b), §6(t), §6(y)')}</td>
          </tr>
          <tr>
            <td><strong>5-Event Analytics &amp; Ledger</strong> (<code>platform/collector.py</code> &amp; <code>ledger.py</code>)</td>
            <td>Self-hostable zero-cookie HTTP collector for the 5 defined events + SHA-256 provenance CSV importer.</td>
            <td>Inert on static GitHub Pages until operator deploys a first-party endpoint; ledger stays empty until signed-in Associates CSVs are imported.</td>
            <td>{official_link(sources_by_id['S08']['url'], 'S08 · GitHub Pages Docs')}<br>{official_link(sources_by_id['S14']['url'], 'S14 · Associates Reports')}</td>
          </tr>
          <tr>
            <td><strong>Topic &amp; Prompt Engine</strong> (<code>platform/research_engine.py</code>)</td>
            <td>Ranks real Google Search Console query exports by impression/CTR gap and builds policy-locked article briefs + design prompts ({len(suggestions_doc['suggestions'])} suggestions, {len(questions_doc['questions'])} questions).</td>
            <td>Never auto-publishes unreviewed AI copy or fabricates search-volume / conversion scores.</td>
            <td>{official_link(sources_by_id['S07']['url'], 'S07 · Search Console Performance')}<br>{official_link(sources_by_id['S05']['url'], 'S05 · 16 CFR Part 255')}</td>
          </tr>
        </tbody>
      </table>
    </div>"""
    return render_shell(
        rel_page,
        title="Executive Summary",
        description="Executive summary of product link verification, Amazon Associates compliance, platform automation, and open operator gates.",
        body_html=body,
        active_nav="suggestions/index.html",
    )


def build_operations_page(
    events_doc: dict[str, Any],
    ledger_doc: dict[str, Any],
    sources_by_id: dict[str, dict[str, Any]],
) -> str:
    rel_page = "operations/index.html"
    ev_rows = []
    for ev in events_doc["events"]:
        src = sources_by_id[ev["source_id"]]
        ev_rows.append(
            f"""          <tr>
            <td><code>{esc(ev['name'])}</code></td>
            <td>{esc(ev['trigger'])}</td>
            <td><code>{esc(", ".join(ev['allowed_keys']))}</code></td>
            <td>{esc(ev['purpose'])}</td>
            <td>{official_link(src['url'], f"{esc(src['id'])} · {esc(src['publisher'])}")}</td>
          </tr>"""
        )

    prov_rows = []
    for pr in ledger_doc["provenance_trail"]:
        src = sources_by_id[pr["source_id"]]
        prov_rows.append(
            f"""          <tr>
            <td><code>{esc(pr['date'])}</code></td>
            <td>{esc(pr['action'])}</td>
            <td><code>{esc(pr['actor'])}</code></td>
            <td>{esc(pr['note'])}</td>
            <td>{official_link(src['url'], f"{esc(src['id'])} · {esc(src['title'])}")}</td>
          </tr>"""
        )

    s14 = sources_by_id["S14"]
    body = f"""    <section class="hero">
      <span class="eyebrow">Priority 4 · Evidence-Based Iteration</span>
      <h1>Privacy-Preserving Measurement &amp; Empty Campaign Ledger</h1>
      <p class="lede">Click and engagement telemetry is restricted to five aggregate events with zero cookies and full DNT/GPC respect. Campaign Ledger rows are accepted exclusively from signed-in first-party exports via <code>platform/ledger.py</code> — no conversion score or revenue forecast appears anywhere on this site.</p>
    </section>

    <section class="panel">
      <h2>Live In-Tab Session Preview (Zero Network Transmission on Static Pages)</h2>
      <p>Because GitHub Pages is static-only (<a href="{esc(rel_href(rel_page, 'flagged/index.html#FLG-009'))}">FLG-009</a>), outbound beacons stay off until <code>window.COUNTERTOP_COLLECTOR_URL</code> points to a self-hosted <code>platform/collector.py</code> instance. Current tab preview counters:</p>
      <p><code id="local-event-inspector">page_view: 0 | product_card_click: 0 | guide_to_product_click: 0 | comparison_filter_use: 0 | suggestion_decision: 0</code></p>
    </section>

    <h2>1. Five Defined Analytics Events (<code>platform/collector.py</code>)</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Event Name</th>
            <th>Trigger Condition</th>
            <th>Allowed Payload Keys</th>
            <th>Decision Purpose</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(ev_rows)}
        </tbody>
      </table>
    </div>

    <h2>2. Campaign Ledger (Intentionally Empty at Launch)</h2>
    <p>{esc(ledger_doc['policy_note'])}</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>timestamp</th>
            <th>source</th>
            <th>channel</th>
            <th>eligible_sessions</th>
            <th>clicks</th>
            <th>reported_orders</th>
            <th>Official Report Source</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="cell-blank" data-unverified="true"><span class="badge badge-warn">Empty</span></td>
            <td class="cell-blank" data-unverified="true"><span class="badge badge-warn">Awaiting CSV</span></td>
            <td class="cell-blank" data-unverified="true"><span class="badge badge-warn">Blank</span></td>
            <td class="cell-blank" data-unverified="true"><span class="badge badge-warn">Blank</span></td>
            <td class="cell-blank" data-unverified="true"><span class="badge badge-warn">Blank</span></td>
            <td class="cell-blank" data-unverified="true"><span class="badge badge-warn">Blank</span></td>
            <td>{official_link(s14['url'], 'S14 · Amazon Associates Central Reports')}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>3. Dated Provenance Trail</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Action</th>
            <th>Actor</th>
            <th>Provenance Note</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(prov_rows)}
        </tbody>
      </table>
    </div>"""
    return render_shell(
        rel_page,
        title="Measurement & Empty Campaign Ledger",
        description="Five-event privacy-preserving click measurement specification and empty provenance-gated campaign ledger.",
        body_html=body,
        active_nav="suggestions/index.html",
    )


def build_compliance_page(sources_doc: dict[str, Any]) -> str:
    rel_page = "compliance/index.html"
    rows = []
    for s in sources_doc["sources"]:
        badge = "badge-ok" if s["status"] == "verified" else "badge-warn"
        rows.append(
            f"""          <tr id="{esc(s['id'])}">
            <td><strong><code>{esc(s['id'])}</code></strong><br><span class="badge {badge}">{esc(s['status'])}</span></td>
            <td><strong>{esc(s['title'])}</strong><br><span class="disclosure-meta">{esc(s['publisher'])} · {esc(s['document_date'])}</span></td>
            <td>{esc(s['key_rule'])}</td>
            <td><code>{esc(s['verified_on'])}</code></td>
            <td>{official_link(s['url'], f"Open official source ({esc(s['id'])})")}</td>
          </tr>"""
        )

    body = f"""    <section class="hero">
      <span class="eyebrow">Priority 5 · Compliance Gate &amp; Official Source Register</span>
      <h1>Official Trusted Sources &amp; Publishing Rules</h1>
      <p class="lede">Every policy rule, identifier format, and product listing cited across this publication was checked firsthand on {esc(BUILD_DATE)} and is enforced automatically by <code>platform/compliance_gate.py</code> and <code>platform/verify_edition.py</code>.</p>
    </section>

    <section class="panel">
      <h2>Automated Pre-Publish Gate Checklist</h2>
      <ul class="spec-list">
        <li><strong>Operating Agreement §5 verbatim disclosure:</strong> <em>“{esc(EXACT_ASSOCIATES_DISCLOSURE)}”</em> appears above <code>&lt;main&gt;</code> and in <code>&lt;footer&gt;</code> on every published page.</li>
        <li><strong>Outbound paid-link qualification:</strong> Every Amazon destination on these pages is an <code>/dp/</code> listing and carries <code>rel="sponsored nofollow noopener"</code>. The <code>link.amazon/...</code> short links the owner supplied appear here as <code>evidence, printed not linked</code>: the register records several of them resolving to the Amazon homepage or a checkpoint page, so a buy button would be a coin flip, and Program Policies 2(a) require a Special Link to carry the assigned ID. Regulatory and technical citations carry <code>rel="noopener"</code> only.</li>
        <li><strong>API-gated commercial fields:</strong> Zero static prices, star ratings, customer review excerpts/counts, stock claims, or price-alert tools appear on static pages (Program Policies §2(b), §6(t), §6(y)).</li>
        <li><strong>Identifier separation:</strong> <code>intended_asin</code> and <code>observed_asin</code> are stored in distinct schema objects and never merged (S03).</li>
      </ul>
    </section>

    <h2>Line-by-Line Official Source Register (S01–S15)</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>ID &amp; Status</th>
            <th>Official Document &amp; Publisher</th>
            <th>Verified Rule / Observation Summary</th>
            <th>Checked On</th>
            <th>Official Source Link</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table>
    </div>"""
    return render_shell(
        rel_page,
        title="Official Sources & Compliance Gate",
        description="Line-by-line register of official Amazon Associates, FTC, eCFR, Google Search Central, and Amazon product listing sources.",
        body_html=body,
        active_nav="suggestions/index.html",
    )


def build_flagged_page(
    flags_doc: dict[str, Any],
    sources_by_id: dict[str, dict[str, Any]],
) -> str:
    rel_page = "flagged/index.html"
    flag_rows = []
    for f in flags_doc["flags"]:
        flag_rows.append(
            f"""          <tr id="{esc(f['id'])}" data-flag-row data-tags="product-policy">
            <td><strong><code>{esc(f['id'])}</code></strong><br><span class="badge badge-warn">{esc(f['severity'])}</span></td>
            <td><strong>{esc(f['title'])}</strong><br><span class="disclosure-meta">Scope: {esc(f['scope'])}</span></td>
            <td>{esc(f['finding'])}</td>
            <td>{esc(f['resolution_step'])}</td>
            <td>{render_source_badges(f['source_ids'], sources_by_id)}</td>
          </tr>"""
        )

    audit_rows = []
    for xr in flags_doc["repo_audit"]:
        audit_rows.append(
            f"""          <tr id="{esc(xr['id'])}" data-flag-row data-tags="repo-audit">
            <td><strong><code>{esc(xr['id'])}</code></strong><br><span class="badge badge-warn">{esc(xr['status'])}</span></td>
            <td><code>{esc(xr['file_scope'])}</code></td>
            <td>{esc(xr['finding'])}</td>
            <td>{render_source_badges(xr['source_ids'], sources_by_id)}</td>
          </tr>"""
        )

    body = f"""    <section class="hero panel-warn">
      <span class="eyebrow">Transparent Review Register · Non-Blocking Audit Items</span>
      <h1>Flagged for Review</h1>
      <p class="lede">All unverified fields, redirect discrepancies, account-gated Associates checks, and cross-repository line-by-line audit findings discovered on {esc(BUILD_DATE)}. Every row links directly to the governing official source.</p>
    </section>

    <div class="filter-bar" data-filter-root data-filter-target="[data-flag-row]">
      <span class="filter-label">Filter review items:</span>
      <button type="button" class="chip-btn" data-filter-value="all" aria-pressed="true">All {len(flags_doc['flags']) + len(flags_doc['repo_audit'])} items</button>
      <button type="button" class="chip-btn" data-filter-value="product-policy" aria-pressed="false">Product, Link &amp; Policy Flags ({len(flags_doc['flags'])})</button>
      <button type="button" class="chip-btn" data-filter-value="repo-audit" aria-pressed="false">Repository Line-by-Line Audit ({len(flags_doc['repo_audit'])})</button>
    </div>

    <h2>1. Product, Link, Attribution &amp; Policy Flags (FLG-001..FLG-010)</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Flag ID</th>
            <th>Item &amp; Scope</th>
            <th>Verified Finding</th>
            <th>Operator Resolution Action</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(flag_rows)}
        </tbody>
      </table>
    </div>

    <h2>2. Repository-Wide Line-by-Line Audit Log (XR-01..XR-06)</h2>
    <p>Findings across sibling/archived repository files logged in <code>COORDINATION.md</code> without overwriting other sessions' claimed scopes.</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Audit ID</th>
            <th>Repository File Scope</th>
            <th>Line-by-Line Finding</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(audit_rows)}
        </tbody>
      </table>
    </div>"""
    return render_shell(
        rel_page,
        title="Flagged for Review",
        description="Unverified items, link attribution flags, and line-by-line repository audit findings with official source links.",
        body_html=body,
        active_nav="suggestions/index.html",
    )


def build_404_page() -> str:
    rel_page = "404.html"
    body = f"""    <section class="hero">
      <span class="eyebrow">404 · Page Not Found</span>
      <h1>That kitchen note or register path is not at this URL.</h1>
      <p class="lede">Use the links below to return to the verified product shortlist, buying guides, or verification registers.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="{esc(rel_href(rel_page, 'index.html'))}">Open Storefront Shortlist</a>
        <a class="btn btn-secondary" href="{esc(rel_href(rel_page, 'guides/index.html'))}">Browse Buying Guides</a>
        <a class="btn btn-secondary" href="{esc(rel_href(rel_page, 'flagged/index.html'))}">Flagged for Review</a>
      </div>
    </section>"""
    return render_shell(
        rel_page,
        title="Page Not Found",
        description="404 navigation recovery page for Countertop Almanac.",
        body_html=body,
        active_nav="",
        include_canonical=False,
    )


def build_sitemap(rel_pages: list[str]) -> str:
    entries = []
    for rp in sorted(rel_pages):
        if rp == "404.html":
            continue
        entries.append(f"  <url>\n    <loc>{esc(canonical_url(rp))}</loc>\n    <lastmod>{BUILD_DATE}</lastmod>\n  </url>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )


def build_rss_feed(guides_doc: dict[str, Any]) -> str:
    items = []
    for g in guides_doc["guides"]:
        url = f"{BASE_URL}/guides/{g['slug']}.html"
        items.append(
            f"""    <item>
      <title>{esc(g['title'])}</title>
      <link>{esc(url)}</link>
      <guid isPermaLink="true">{esc(url)}</guid>
      <pubDate>Fri, 20 Nov 2026 00:00:00 GMT</pubDate>
      <category>{esc(g['cluster'])}</category>
      <description>{esc(g['dek'])}</description>
    </item>"""
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{esc(SITE_TITLE)} — Buying Guides</title>
    <link>{BASE_URL}/</link>
    <atom:link href="{BASE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Question-shaped and seasonal countertop air fryer and meat thermometer buying guides.</description>
    <language>en-us</language>
    <lastBuildDate>Fri, 20 Nov 2026 00:00:00 GMT</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""


def write_text(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_all() -> list[str]:
    gate_errors = validate_data_layer(DATA_DIR)
    if gate_errors:
        raise RuntimeError("Data compliance gate failed:\n" + "\n".join(gate_errors))

    sources_doc = json.loads((DATA_DIR / "sources.json").read_text(encoding="utf-8"))
    products_doc = json.loads((DATA_DIR / "products.json").read_text(encoding="utf-8"))
    flags_doc = json.loads((DATA_DIR / "flags.json").read_text(encoding="utf-8"))
    questions_doc = json.loads((DATA_DIR / "questions.json").read_text(encoding="utf-8"))
    suggestions_doc = json.loads((DATA_DIR / "suggestions.json").read_text(encoding="utf-8"))
    events_doc = json.loads((DATA_DIR / "events.json").read_text(encoding="utf-8"))
    ledger_doc = json.loads((DATA_DIR / "ledger.json").read_text(encoding="utf-8"))
    guides_doc = json.loads((DATA_DIR / "guides.json").read_text(encoding="utf-8"))

    sources_by_id = {s["id"]: s for s in sources_doc["sources"]}
    products_by_id = {p["id"]: p for p in products_doc["products"]}
    guides_by_slug = {g["slug"]: g for g in guides_doc["guides"]}

    # Static assets
    write_text(EDITION_DIR / "assets/style.css", STYLE_CSS)
    write_text(EDITION_DIR / "assets/analytics.js", ANALYTICS_JS)
    write_text(EDITION_DIR / "assets/app.js", APP_JS)
    for name, svg in SVG_ASSETS.items():
        write_text(EDITION_DIR / "assets/img" / name, svg + "\n")

    pages: dict[str, str] = {
        "index.html": build_home_page(products_doc, guides_doc, flags_doc, sources_by_id),
        "categories/index.html": build_categories_index(products_doc, sources_by_id),
        "compare/index.html": build_compare_page(products_doc, sources_by_id),
        "products/index.html": build_products_register(products_doc, sources_by_id),
        "guides/index.html": build_guides_index(guides_doc, sources_by_id),
        "suggestions/index.html": build_suggestions_page(suggestions_doc, sources_by_id),
        "questions/index.html": build_questions_page(questions_doc, sources_by_id),
        "executive-summary/index.html": build_executive_summary_page(
            products_doc, flags_doc, questions_doc, suggestions_doc, sources_by_id
        ),
        "operations/index.html": build_operations_page(events_doc, ledger_doc, sources_by_id),
        "compliance/index.html": build_compliance_page(sources_doc),
        "flagged/index.html": build_flagged_page(flags_doc, sources_by_id),
        "404.html": build_404_page(),
    }

    for cat in products_doc["categories"]:
        pages[f"categories/{cat['slug']}.html"] = build_category_detail(cat, products_doc, sources_by_id)

    for prod in products_doc["products"]:
        pages[f"products/{prod['slug']}.html"] = build_product_detail(
            prod, products_by_id, guides_by_slug, sources_by_id
        )

    for g in guides_doc["guides"]:
        pages[f"guides/{g['slug']}.html"] = build_guide_page(g, products_by_id, sources_by_id)

    for rel_p, html_text in sorted(pages.items()):
        write_text(EDITION_DIR / rel_p, html_text)

    write_text(EDITION_DIR / "sitemap.xml", build_sitemap(list(pages.keys())))
    write_text(EDITION_DIR / "feed.xml", build_rss_feed(guides_doc))
    # Robots here mirrors the per-page `noindex, follow` above rather than
    # contradicting it. The previous file said `Allow: /` and advertised a
    # sitemap, which invited the crawl the meta tag now declines. One site to
    # index means one sitemap on the host, and it is the root one.
    write_text(
        EDITION_DIR / "robots.txt",
        "User-agent: *\n"
        "# Second published surface, kept for review. Not the site to index.\n"
        "# Canonical publication: https://karagemop466-tech.github.io/Affil1/\n"
        "Disallow: /\n",
    )
    return sorted(pages.keys())


if __name__ == "__main__":
    built = build_all()
    print(f"platform/build_edition.py: built {len(built)} HTML pages + sitemap.xml + feed.xml + robots.txt")
