#!/usr/bin/env python3
"""Render the Good Measure Kitchen site from site_data.py.

Everything the site shows comes from site_data.py. Run:

    python3 scripts/build_site.py

The rendered HTML is committed to the repository, so the site has no runtime build
dependency. scripts/check_site.py then gates the result.
"""

import os
import sys
import datetime
import html
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import site_data as D  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGIN = D.SITE["origin"].rstrip("/")

E = html.escape


# ---------------------------------------------------------------------------- helpers
def rel(path, root):
    return (root + path) if path else root


def src(path, root):
    return rel(path, root)


def byline(note=None):
    extra = f" &middot; {note}" if note else ""
    return (
        '<p class="byline"><span class="byline-name">%s</span>'
        '<span class="byline-role">%s</span>'
        '<span class="byline-date">Published %s &middot; Updated %s</span>%s</p>'
        % (E(D.SITE["author"]), E(D.SITE["author_role"]),
           E(D.SITE["published"]), E(D.SITE["updated"]), extra)
    )


def source_list(keys, root, extra=None):
    items = []
    for k in keys:
        s = D.SOURCES[k]
        items.append(
            '<li><a href="%s" rel="noopener" target="_blank">%s</a></li>'
            % (E(s["url"]), E(s["title"]))
        )
    if extra:
        items.append('<li>%s</li>' % extra)
    return '<ul class="source-list">%s</ul>' % "".join(items)


def chip(text, kind="muted"):
    return '<span class="chip chip-%s">%s</span>' % (kind, E(text))


def flag_chips(flags, root=""):
    if not flags:
        return chip("No open flags", "ok")
    return "".join(
        '<a class="chip chip-flag" href="%s#%s">%s</a>'
        % (rel("desk/flagged-for-review.html", root), f, f)
        for f in flags
    )


def product_by_asin(asin):
    for p in D.PRODUCTS:
        if p["intent_asin"] == asin:
            return p
    return None


def products_in(category):
    return [p for p in D.PRODUCTS if p["category"] == category]


def confirmed_products():
    return [p for p in D.PRODUCTS if p["intent_asin"]]


PRODUCT_LINK_RE = re.compile(
    r"^(?:https?://)?(?:[a-z0-9-]+\.)*amazon\.[a-z.]+/dp/|"
    r"^(?:https?://)?link\.amazon/|"
    r"^(?:https?://)?(?:amzn\.to|amzn\.eu|amzn\.asia|a\.co)/", re.I)


def is_product_link(url):
    """True for links to an Amazon product detail page or an Amazon short link.

    Those are placements and must be marked sponsored. Links to Amazon's own
    programme documentation, blogs, review pages or checkpoints are citations of
    evidence, not placements, and must NOT be marked sponsored."""
    return bool(PRODUCT_LINK_RE.match(url.strip()))


def cite_link(url, label, root, extra_class=""):
    """Render an evidence link. Product destinations are marked sponsored;
    everything else stays a plain citation."""
    if is_product_link(url):
        return ('<a class="%s" href="%s" target="_blank" rel="sponsored nofollow noopener">%s</a>'
                % (extra_class, E(url), E(label)))
    return ('<a class="%s" href="%s" target="_blank" rel="noopener">%s</a>'
            % (extra_class, E(url), E(label)))


def sponsored_link(url, label, root, extra_class=""):
    return (
        '<a class="btn %s" href="%s" target="_blank" rel="sponsored nofollow noopener">%s</a>'
        % (extra_class, E(url), E(label))
    )


def guide_href(slug, root):
    return rel("guides/%s.html" % slug, root)


# ---------------------------------------------------------------------------- chrome
def disclosure(root):
    return (
        '<div class="disclosure"><span class="disclosure-inner">'
        '<strong>%s</strong> <span class="disclosure-more">Every link to Amazon on this site is a '
        'paid placement. <a href="%s">How our links work</a></span>'
        '</span></div>'
        % (E(D.DISCLOSURE), rel("desk/methodology.html#disclosure", root))
    )


def masthead(root, active=""):
    parts = []
    for group in D.NAV:
        kids = "".join(
            '<a href="%s">%s</a>' % (E(rel(c["href"], root)), E(c["label"]))
            for c in group["children"]
        )
        label = E(group["label"])
        if group["label"].lower() == active.lower():
            label = '<span class="nav-current">%s</span>' % label
        parts.append(
            '<li class="nav-item"><a class="nav-top" href="%s">%s</a>'
            '<div class="menu">%s</div></li>' % (E(rel(group["href"], root)), label, kids)
        )
    return (
        '<header class="masthead"><div class="wrap masthead-inner">'
        '<a class="brand" href="%s"><span class="brand-mark">gm</span>'
        '<span class="brand-text">%s<span class="brand-sub">%s</span></span></a>'
        '<nav class="nav" aria-label="Main"><ul>%s</ul></nav>'
        '<a class="btn btn-small masthead-cta" href="%s">Shop the shelf</a>'
        '<button class="nav-toggle" aria-expanded="false" aria-controls="mobile-nav" '
        'aria-label="Open menu"><span></span><span></span><span></span></button>'
        '</div><div class="mobile-nav" id="mobile-nav" hidden>%s</div></header>'
        % (
            E(rel("index.html", root)),
            E(D.SITE["name"]),
            E(D.SITE["tagline"]),
            "".join(parts),
            E(rel("shop/index.html", root)),
            "".join(
                '<a href="%s">%s</a>' % (E(rel(c["href"], root)), E(c["label"]))
                for g in D.NAV for c in g["children"]
            ),
        )
    )


def footer(root):
    navs = []
    for group in D.NAV:
        links = ['<a href="%s">%s</a>' % (E(rel(c["href"], root)), E(c["label"]))
                 for c in group["children"]]
        links.append('<a href="%s">All %s</a>' % (E(rel(group["href"], root)), E(group["label"].lower())))
        navs.append('<div class="footer-nav"><b>%s</b>%s</div>'
                    % (E(group["label"]), "".join(links)))
    return (
        '<footer class="site-footer"><div class="wrap footer-main">'
        '<div class="footer-brand"><a class="brand" href="%s"><span class="brand-mark">gm</span>'
        '<span class="brand-text">%s<span class="brand-sub">%s</span></span></a>'
        '<p class="footer-blurb">Independent kitchen buying guides. We have not handled the '
        'appliances we write about, and we say what we could not confirm.</p>'
        '<p class="footer-disclosure"><strong>%s</strong></p></div>'
        '%s<div class="footer-nav"><b>The Desk</b>'
        '<a href="%s">Executive summary</a><a href="%s">Suggestions register</a>'
        '<a href="%s">Open questions</a><a href="%s">Campaign ledger</a>'
        '<a href="%s">Publishing gate</a><a href="%s">Flagged for review</a>'
        '<a href="%s">RSS feed</a><a href="%s">Sitemap</a></div>'
        '</div><div class="wrap footer-bottom"><span>%s &middot; %s &middot; %s</span>'
        '<span>Built from one verified data file. <a href="%s">How we verify</a></span></div></footer>'
        % (
            E(rel("index.html", root)),
            E(D.SITE["name"]),
            E(D.SITE["tagline"]),
            E(D.DISCLOSURE),
            "".join(navs),
            E(rel("desk/executive-summary.html", root)),
            E(rel("desk/suggestions.html", root)),
            E(rel("desk/questions.html", root)),
            E(rel("desk/ledger.html", root)),
            E(rel("desk/publishing-gate.html", root)),
            E(rel("desk/flagged-for-review.html", root)),
            E(rel("feed.xml", root)),
            E(rel("sitemap.xml", root)),
            E(D.SITE["name"]), E(D.SITE["issue"]), E(D.SITE["issue_date"]),
            E(rel("desk/methodology.html", root)),
        )
    )


def page(*, title, description, root, body, active="", path="", og_type="website", extra_head=""):
    canonical = ORIGIN + "/" + path
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(canonical)s">
<meta property="og:site_name" content="%(site)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="%(ogtype)s">
<meta property="og:url" content="%(canonical)s">
<meta name="twitter:card" content="summary">
<link rel="alternate" type="application/rss+xml" title="%(site)s — %(tagline)s" href="%(feed)s">
<link rel="stylesheet" href="%(css)s">
<script type="application/ld+json">%(ld)s</script>
%(extra)s</head>
<body class="%(cls)s">
%(disclosure)s
%(masthead)s
<main id="main">%(body)s</main>
%(footer)s
<script src="%(data)s" defer></script>
<script src="%(js)s" defer></script>
<script src="%(analytics)s" defer></script>
</body>
</html>
""" % {
        "title": E(title),
        "desc": E(description),
        "canonical": E(canonical),
        "ogtype": E(og_type),
        "site": E(D.SITE["name"]),
        "tagline": E(D.SITE["tagline"]),
        "feed": E(rel("feed.xml", root)),
        "css": E(rel("styles.css", root)),
        "data": E(rel("assets/site-config.js", root)),
        "js": E(rel("app.js", root)),
        "analytics": E(rel("assets/analytics.js", root)),
        "extra": extra_head,
        "cls": "",
        "disclosure": disclosure(root),
        "masthead": masthead(root, active),
        "footer": footer(root),
        "body": body,
        "ld": json_ld(title, description, canonical),
    }


def json_ld(title, description, canonical):
    import json
    data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": D.SITE["name"],
        "alternateName": D.SITE["tagline"],
        "url": ORIGIN + "/",
        "description": description,
    }
    return json.dumps(data, ensure_ascii=False)


# ---------------------------------------------------------------------------- front page
def product_card(p, root, compact=False):
    if not p["intent_special_link"]:
        return ""
    art = (
        '<div class="card-art art-%s"><span class="art-num">%02d</span>'
        '<span class="art-kind">%s</span></div>'
        % (p["art"], p["slot"], E(p["kicker"]))
    )
    fit = "".join("<li>%s</li>" % E(x) for x in p["fit"][:3])
    watch = "".join("<li>%s</li>" % E(x) for x in p["watch"][:2])
    return """<article class="product-card">
%(art)s<div class="card-body">
<p class="tag">%(brand)s</p>
<h3><a href="%(href)s">%(name)s</a></h3>
<p class="card-blurb">%(blurb)s</p>
<div class="card-cols"><div><h4>Why it is on the shelf</h4><ul class="tick">%(fit)s</ul></div>
<div><h4>Where it might not suit you</h4><ul class="cross">%(watch)s</ul></div></div>
<div class="card-foot"><p class="card-note">%(chip)s Listing observed %(seen)s.
 <a href="%(rec)s">Record</a></p>
%(cta)s</div></div></article>""" % {
        "art": art,
        "brand": E(p["brand"]),
        "name": E(p["name"]),
        "href": E(rel("shop/index.html#p-%s" % p["token"], root)),
        "blurb": E(p["blurb"]),
        "fit": fit,
        "watch": watch,
        "chip": chip("Intent recorded", "ok"),
        "seen": E(p["observed_on"]),
        "rec": E(rel("desk/product-records.html#%s" % p["token"], root)),
        "cta": sponsored_link(p["intent_special_link"], "Check the listing \u2197", root, "btn-dark"),
    }


def front_page(root):
    confirmed = confirmed_products()
    shelf = "".join(product_card(p, root) for p in confirmed[:3])

    rows = []
    for p in D.PRODUCTS:
        listing = (sponsored_link(p["intent_special_link"], "Listing \u2197", root, "btn-table")
                   if p["intent_special_link"] else
                   '<a href="%s" rel="sponsored nofollow noopener" target="_blank">Submitted link</a>'
                   % E(p["submitted"]))
        rows.append(
            "<tr><td class=\"num\">%02d</td><td><b>%s</b><small>%s</small></td>"
            "<td>%s</td><td class=\"mono\">%s</td>"
            "<td>%s <a href=\"%s\">Record</a></td></tr>"
            % (
                p["slot"],
                E(p["brand"] or "Unconfirmed"),
                E(p["name"]),
                E(p["kicker"]),
                E(p["intent_asin"] or "\u2014"),
                listing,
                E(rel("desk/product-records.html#%s" % p["token"], root)),
            )
        )

    guide_cards = ""
    for g in D.GUIDES[:3]:
        guide_cards += """<article class="guide-card">
<div class="card-art art-guide"><span class="art-num">%(cluster)s</span><span class="art-kind">%(read)s</span></div>
<div class="card-body"><p class="tag">%(cluster_label)s</p>
<h3><a href="%(href)s">%(title)s</a></h3><p class="card-blurb">%(dek)s</p>
<a class="text-link" href="%(href)s">Read the guide <span>\u2192</span></a></div></article>""" % {
            "cluster": E(g["cluster_label"].upper()),
            "read": E(g["read"]),
            "cluster_label": E(g["cluster_label"]),
            "href": E(guide_href(g["slug"], root)),
            "title": E(g["title"]),
            "dek": E(g["dek"]),
        }

    season_cards = ""
    for s in D.SEASONS:
        links = " ".join(
            '<a href="%s">%s</a>' % (E(guide_href(g, root)), E(_guide_title(g)))
            for g in s["guides"]
        )
        season_cards += """<div class="season-card"><h3>%(label)s</h3><p>%(blurb)s</p>
<div class="season-links">%(links)s</div></div>""" % {
            "label": E(s["label"]), "blurb": E(s["blurb"]), "links": links,
        }

    clusters = "".join(
        '<a class="cluster-pill" href="%s"><b>%s</b><span>%s</span></a>'
        % (E(rel("guides/index.html#%s" % c[0], root)), E(c[1]), E(c[2]))
        for c in D.CLUSTERS
    )

    body = """
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="issue-line">%(issue)s &middot; %(date)s &middot; Independent kitchen buying guides</p>
      <h1>Buy the thing that fits<br><em>your kitchen.</em></h1>
      <p class="lead">Four products on the shelf. Six questions that decide between them. No
      rankings we cannot justify, no prices we cannot source, and no pretending we have handled
      an appliance we have only read about.</p>
      <div class="hero-actions"><a class="btn" href="%(shop)s">Shop the shelf <span>\u2197</span></a>
      <a class="btn btn-ghost" href="%(guides)s">Start with a question</a></div>
      <p class="hero-note">Every product link on this site is a paid placement, and the disclosure
      sits above this line.</p>
    </div>
    <div class="hero-art" aria-hidden="true">
      <div class="art-card art-card-1"><span>01</span><b>Dual basket</b><i>6 qt</i></div>
      <div class="art-card art-card-2"><span>02</span><b>French door oven</b><i>26 qt</i></div>
      <div class="art-card art-card-3"><span>03</span><b>Single basket</b><i>8 qt</i></div>
      <div class="art-card art-card-4"><span>04</span><b>Probe</b><i>3</i></div>
      <p class="art-caption">Formats, not favourites.</p>
    </div>
  </div>
</section>

<div class="ticker"><div class="wrap ticker-inner"><span>THE SHELF</span><span>\u2726</span>
<span>THE QUESTIONS</span><span>\u2726</span><span>THE RECORD</span><span>\u2726</span>
<span>NO UNSOURCED CLAIMS</span><span>\u2726</span><span>THE SHELF</span></div></div>

<section class="wrap section" id="shelf">
  <div class="section-head"><div><p class="eyebrow">The shelf</p>
  <h2>What we would actually<br>put in front of you.</h2></div>
  <p class="section-note">Every card below is built from what the official listing states and
  nothing else. Where a figure was not confirmed, the line says so.</p></div>
  <div class="product-grid">%(shelf)s</div>
  <p class="editorial-note">These four records were confirmed from official Amazon product pages on
  20 November 2026. A fifth submitted link could not be resolved and is recorded as unresolved
  rather than described. We have not handled these appliances.</p>
</section>

<section class="wrap section section-tight">
  <div class="section-head"><div><p class="eyebrow">The shelf in one table</p>
  <h2>Every record, side by side.</h2></div>
  <p class="section-note">A blank cell means the value was not confirmed from an official source.
  It is never filled with an estimate.</p></div>
  <div class="table-wrap"><table class="data-table">
  <thead><tr><th>#</th><th>Product</th><th>Format</th><th>ASIN</th><th>Official listing</th></tr></thead>
  <tbody>%(rows)s</tbody></table></div>
  <p class="editorial-note">No price is shown here. Amazon's Associates IP License permits Product
  Advertising Content only through the Creators API or PA API, which this site has not connected.
  Dated observations are recorded on the desk, with their source. <a href="%(method)s">How we verify</a></p>
</section>

<section class="wrap section section-tight">
  <div class="section-head"><div><p class="eyebrow">Start with a question</p>
  <h2>The guides.</h2></div>
  <p class="section-note">Six guides, each answering one decision point. Their titles are editorial
  hypotheses, not claims about search volume.</p></div>
  <div class="guide-grid">%(guides)s</div>
  <p class="center-link"><a class="text-link" href="%(guides)s">See all six guides <span>\u2192</span></a></p>
</section>

<section class="season-band">
  <div class="wrap"><div class="section-head"><div><p class="eyebrow">The seasonal shelf</p>
  <h2>What this time of year is for.</h2></div>
  <p class="section-note">The shelf rotates with the season. The questions do not change.</p></div>
  <div class="season-grid">%(seasons)s</div></div>
</section>

<section class="wrap section section-tight">
  <div class="section-head"><div><p class="eyebrow">Clusters</p><h2>Six ways in.</h2></div>
  <p class="section-note">Every guide sits in a cluster, so a reader can follow a line of
  thinking instead of a list.</p></div>
  <div class="cluster-row">%(clusters)s</div>
</section>

<section class="desk-band">
  <div class="wrap desk-grid">
    <div><p class="eyebrow">The desk</p><h2>Where the receipts live.</h2>
    <p>Everything we could not confirm is written down, with the source that would settle it.
    Nothing on the shop pages is a guess, and nothing here is hidden.</p>
    <a class="btn btn-light" href="%(desk)s">Open the desk <span>\u2192</span></a></div>
    <div class="desk-cards">
      <a class="desk-card" href="%(summary)s"><b>Executive summary</b><span>The whole position in one page.</span></a>
      <a class="desk-card" href="%(records)s"><b>Product records</b><span>Intent and observation, kept apart.</span></a>
      <a class="desk-card" href="%(suggest)s"><b>Suggestions register</b><span>Fifteen proposals, each with a decision slot.</span></a>
      <a class="desk-card" href="%(questions)s"><b>Open questions</b><span>What we know, what we do not, how to find out.</span></a>
      <a class="desk-card" href="%(gate)s"><b>Publishing gate</b><span>Eight automated checks, four for a human.</span></a>
      <a class="desk-card" href="%(flags)s"><b>Flagged for review</b><span>Eight open items with sources.</span></a>
    </div>
  </div>
</section>
""" % {
        "issue": E(D.SITE["issue"]),
        "date": E(D.SITE["issue_date"]),
        "shop": E(rel("shop/index.html", root)),
        "guides": E(rel("guides/index.html", root)),
        "shelf": shelf,
        "rows": "".join(rows),
        "guide_cards": guide_cards,
        "seasons": season_cards,
        "clusters": clusters,
        "method": E(rel("desk/methodology.html", root)),
        "desk": E(rel("desk/index.html", root)),
        "summary": E(rel("desk/executive-summary.html", root)),
        "records": E(rel("desk/product-records.html", root)),
        "suggest": E(rel("desk/suggestions.html", root)),
        "questions": E(rel("desk/questions.html", root)),
        "gate": E(rel("desk/publishing-gate.html", root)),
        "flags": E(rel("desk/flagged-for-review.html", root)),
    }
    return body


def _guide_title(slug):
    for g in D.GUIDES:
        if g["slug"] == slug:
            return g["title"]
    return slug


# ---------------------------------------------------------------------------- shop
def product_row(p, root):
    link = (sponsored_link(p["intent_special_link"], "Listing \u2197", root, "btn-table")
            if p["intent_special_link"] else
            '<a href="%s" rel="sponsored nofollow noopener" target="_blank">Submitted link</a>'
            % E(p["submitted"]))
    return """<tr id="p-%(token)s"><td class="num">%(slot)d</td>
<td><b>%(name)s</b><small>%(brand)s</small></td>
<td>%(kicker)s</td>
<td class="mono">%(asin)s</td>
<td>%(link)s</td></tr>""" % {
        "token": E(p["token"]),
        "slot": p["slot"],
        "name": E(p["name"]),
        "brand": E(p["brand"] or "\u2014"),
        "kicker": E(p["kicker"]),
        "asin": E(p["intent_asin"] or "\u2014"),
        "link": link,
    }


def shop_index(root):
    rows = "".join(product_row(p, root) for p in D.PRODUCTS)
    cards = "".join(product_card(p, root) for p in confirmed_products())
    cat_cards = ""
    for c in D.CATEGORIES:
        count = len(products_in(c["slug"]))
        cat_cards += """<a class="cat-card" href="%(href)s"><span class="cat-kicker">%(kick)s</span>
<h3>%(title)s</h3><p>%(blurb)s</p><span class="cat-count">%(count)d record%(s)s</span></a>""" % {
            "href": E(rel("shop/%s.html" % c["slug"], root)),
            "kick": E(c["kicker"]),
            "title": E(c["title"]),
            "blurb": E(c["blurb"]),
            "count": count,
            "s": "" if count == 1 else "s",
        }

    pending = [p for p in D.PRODUCTS if not p["intent_asin"]]
    pending_rows = []
    for p in pending:
        pending_rows += """<tr id="p-%(token)s"><td class="num">%(slot)d</td>
<td><b>%(name)s</b><small>Submitted link</small></td>
<td>%(kicker)s</td><td class="mono">\u2014</td>
<td><a href="%(sub)s" rel="sponsored nofollow noopener" target="_blank">Submitted link</a></td>
<td>%(flags)s</td></tr>""" % {
            "token": E(p["token"]), "slot": p["slot"], "name": E(p["name"]),
            "sub": E(p["submitted"]), "kicker": E(p["kicker"]),
            "flags": flag_chips(p["flags"], root),
        }

    body = """
<section class="page-head"><div class="wrap"><p class="eyebrow">Shop</p>
<h1>The shelf.</h1>
<p class="lead">Four records confirmed against official Amazon product pages on 20 November 2026,
and one that could not be resolved. Nothing here is ranked. Choose a format, then read the guide
that decides it.</p></div></section>

<section class="wrap section section-tight"><div class="section-head"><div><p class="eyebrow">By category</p>
<h2>Three shelves.</h2></div><p class="section-note">A category is a shape of appliance and a set
of questions, not a ranking.</p></div><div class="cat-grid">%(cats)s</div></section>

<section class="wrap section section-tight"><div class="section-head"><div><p class="eyebrow">The shelf in one table</p>
<h2>Every record, side by side.</h2></div>
<div class="table-tools"><input type="search" id="shop-filter" class="table-filter"
placeholder="Filter by product, format or ASIN" aria-label="Filter products"></div></div>
<div class="table-wrap"><table class="data-table" id="shop-table"><thead><tr>
<th>#</th><th>Product</th><th>Format</th><th>ASIN</th><th>Official listing</th>
</tr></thead><tbody>%(rows)s</tbody></table></div>
<p class="editorial-note">No price is shown, because the Associates IP License permits Product
Advertising Content only through the Creators API or PA API. Dated observations are recorded on
the desk with their source. <a href="%(method)s">How we verify</a></p></section>

<section class="wrap section section-tight"><div class="section-head"><div><p class="eyebrow">Record by record</p>
<h2>The cards.</h2></div></div><div class="product-grid">%(cards)s</div></section>

<section class="wrap section section-tight"><div class="section-head"><div><p class="eyebrow">Unresolved</p>
<h2>One record we will not describe.</h2></div></div>
<div class="table-wrap"><table class="data-table"><thead><tr><th>#</th><th>Record</th>
<th>Status</th><th>ASIN</th><th>Submitted link</th><th>Flag</th></tr></thead><tbody>%(pending)s</tbody></table></div>
<p class="editorial-note">This link answered with an Amazon \u201cContinue shopping\u201d checkpoint on
20 November 2026. Until the destination is observed, we publish nothing about it.
<a href="%(records)s">See the record</a></p></section>

<section class="wrap section section-tight"><div class="callout callout-wide">
<h3>Why there is no price on this page</h3>
<p>Amazon's Associates IP License allows Product Advertising Content \u2014 price, availability,
ratings \u2014 to be obtained only through the Creators API or the Product Advertising API. This site
has not connected either. Rather than republish figures from a page read, the shop hands you to the
official listing and the desk records dated observations with their source.</p>
<p><a href="%(gate)s">See the publishing gate</a> &middot; <a href="%(suggest)s">See the suggestions register</a></p>
</div></section>
""" % {
        "cats": cat_cards,
        "rows": rows,
        "cards": cards,
        "pending": pending_rows,
        "method": E(rel("desk/methodology.html", root)),
        "records": E(rel("desk/product-records.html", root)),
        "gate": E(rel("desk/publishing-gate.html", root)),
        "suggest": E(rel("desk/suggestions.html", root)),
    }
    return body


def category_page(cat, root):
    prods = products_in(cat["slug"])
    cards = "".join(product_card(p, root) for p in prods)
    rows = "".join(product_row(p, root) for p in prods)
    guides = [g for g in D.GUIDES if g["cluster"] == cat["cluster"]]
    guide_links = "".join(
        '<li><a href="%s">%s</a></li>' % (E(guide_href(g["slug"], root)), E(g["title"]))
        for g in guides
    ) or '<li class="muted">No guide in this cluster yet.</li>'
    qs = "".join("<li>%s</li>" % E(q) for q in cat["questions"])

    body = """
<section class="page-head"><div class="wrap"><p class="eyebrow">%(kick)s &middot; Category</p>
<h1>%(title)s</h1><p class="lead">%(blurb)s</p></div></section>

<section class="wrap section section-tight"><div class="split">
<div><h2 class="h3">The questions this shelf answers</h2><ul class="question-list">%(qs)s</ul>
<h2 class="h3">Guides in this cluster</h2><ul class="guide-links">%(guides)s</ul></div>
<div class="panel"><h3>What is confirmed</h3>
<p>%(count)d record%(s)s, each read from its official Amazon product page on 20 November 2026.
Specifications on this page repeat what the listing states. Everything else is left blank.</p>
<p><a href="%(records)s">Open the product records</a></p></div></div></section>

<section class="wrap section section-tight"><div class="section-head"><div><p class="eyebrow">On this shelf</p>
<h2>%(count)d record%(s)s.</h2></div></div><div class="product-grid">%(cards)s</div></section>

<section class="wrap section section-tight"><div class="table-wrap"><table class="data-table">
<thead><tr><th>#</th><th>Product</th><th>Format</th><th>ASIN</th><th>Official listing</th></tr></thead>
<tbody>%(rows)s</tbody></table></div>
<p class="editorial-note">Live pricing and availability live on the official listing, which the
link takes you to. <a href="%(records)s">Product record</a></p></section>
""" % {
        "kick": E(cat["kicker"]),
        "title": E(cat["title"]),
        "blurb": E(cat["blurb"]),
        "qs": qs,
        "guides": guide_links,
        "count": len(prods),
        "s": "" if len(prods) == 1 else "s",
        "cards": cards,
        "rows": rows,
        "records": E(rel("desk/product-records.html", root)),
    }
    return body


# ---------------------------------------------------------------------------- guides
def guide_index(root):
    by_cluster = {}
    for g in D.GUIDES:
        by_cluster.setdefault(g["cluster_label"], []).append(g)
    sections = ""
    for slug, label, blurb in D.CLUSTERS:
        gs = by_cluster.get(label, [])
        if not gs:
            continue
        cards = ""
        for g in gs:
            cards += """<article class="guide-card"><div class="card-art art-guide">
<span class="art-num">%(num)02d</span><span class="art-kind">%(read)s</span></div>
<div class="card-body"><p class="tag">%(label)s</p><h3><a href="%(href)s">%(title)s</a></h3>
<p class="card-blurb">%(dek)s</p><a class="text-link" href="%(href)s">Read the guide <span>\u2192</span></a>
</div></article>""" % {
                "num": D.GUIDES.index(g) + 1,
                "read": E(g["read"]),
                "label": E(label),
                "href": E(guide_href(g["slug"], root)),
                "title": E(g["title"]),
                "dek": E(g["dek"]),
            }
        sections += """<section class="cluster-block" id="%(id)s">
<div class="section-head"><div><p class="eyebrow">Cluster</p><h2>%(label)s</h2></div>
<p class="section-note">%(blurb)s</p></div><div class="guide-grid">%(cards)s</div></section>""" % {
            "id": E(slug), "label": E(label), "blurb": E(blurb), "cards": cards,
        }

    body = """
<section class="page-head"><div class="wrap"><p class="eyebrow">Guides</p>
<h1>Start with the question.</h1>
<p class="lead">Six questions that decide between kitchen formats. The titles are editorial
hypotheses written to match how people ask, not claims about search volume, popularity or
product superiority.</p></div></section>
<section class="wrap section section-tight">%(sections)s</section>
<section class="wrap section section-tight"><div class="callout callout-wide">
<h3>What we leave out</h3><p>No winner badges, no star ratings we could not read from an
official source, no review summaries we did not verify, and no claim that we have used these
appliances. Where a figure is missing, the guide says which figure and where it would come from.</p>
<p><a href="%(method)s">How we verify</a> &middot; <a href="%(questions)s">Open questions</a></p>
</div></section>
""" % {
        "sections": sections,
        "method": E(rel("desk/methodology.html", root)),
        "questions": E(rel("desk/questions.html", root)),
    }
    return body


def guide_page(g, root):
    body_html = []
    for kind, text in g["body"]:
        if kind == "p":
            body_html.append("<p>%s</p>" % E(text))
        elif kind == "h2":
            body_html.append("<h2>%s</h2>" % E(text))
        elif kind == "callout":
            body_html.append(
                '<aside class="callout"><h3>Before you rely on this</h3><p>%s</p></aside>' % E(text)
            )
    body_html = "\n".join(body_html)

    shelf = ""
    for asin in g["products"]:
        p = product_by_asin(asin)
        if not p or not p["intent_special_link"]:
            continue
        shelf += """<div class="shelf-row">
<div><b>%(name)s</b><span>%(kicker)s</span></div>
<p>%(blurb)s</p>%(cta)s</div>""" % {
            "name": E(p["name"]), "kicker": E(p["kicker"]), "blurb": E(p["blurb"]),
            "cta": sponsored_link(p["intent_special_link"], "Check the listing \u2197", root, "btn-dark"),
        }

    related = ""
    for other in D.GUIDES:
        if other["slug"] == g["slug"]:
            continue
        if other["cluster"] == g["cluster"]:
            related += '<li><a href="%s">%s</a></li>' % (E(guide_href(other["slug"], root)), E(other["title"]))

    body = """
<article class="guide-article">
<div class="wrap article-grid">
<div class="article-main">
<p class="eyebrow">%(cluster)s &middot; %(read)s read</p>
<h1>%(title)s</h1>
<p class="dek">%(dek)s</p>
%(byline)s
<div class="prose">%(body)s</div>
</div>
<aside class="article-side">
<div class="side-panel"><h3>Shop the formats in this guide</h3>
<p class="side-note">These are paid placements. We have not handled these appliances; the lines
above repeat what the official listing states.</p>
%(shelf)s
<p class="side-note">Full record, including the intended listing and the observed redirect:
<a href="%(records)s">product records</a>.</p></div>
<div class="side-panel"><h3>Related in this cluster</h3><ul class="guide-links">%(related)s</ul></div>
<div class="side-panel side-panel-quiet"><h3>More guides</h3>
<ul class="guide-links">%(all)s</ul></div>
</aside>
</div></article>
""" % {
        "cluster": E(g["cluster_label"]),
        "read": E(g["read"]),
        "title": E(g["title"]),
        "dek": E(g["dek"]),
        "byline": byline(),
        "body": body_html,
        "shelf": shelf,
        "records": E(rel("desk/product-records.html", root)),
        "related": related or '<li class="muted">Nothing else in this cluster yet.</li>',
        "all": "".join(
            '<li><a href="%s">%s</a></li>' % (E(guide_href(o["slug"], root)), E(o["title"]))
            for o in D.GUIDES
        ),
    }
    return body


# ---------------------------------------------------------------------------- desk
def desk_index(root):
    cards = ""
    entries = [
        ("Executive summary", "desk/executive-summary.html",
         "The position in one page: what was confirmed, what was found, what is still open."),
        ("Product records", "desk/product-records.html",
         "The product-intent confirmation record. Intended listing and observed redirect, never merged."),
        ("Suggestions register", "desk/suggestions.html",
         "Fifteen proposals with evidence, effort, risk and an empty decision column."),
        ("Open questions", "desk/questions.html",
         "Eight questions with what we know, what we do not, and how to find the answer."),
        ("Campaign ledger", "desk/ledger.html",
         "An empty but fully defined ledger, to be filled only from authorised first-party reports."),
        ("Publishing gate", "desk/publishing-gate.html",
         "Eight checks a machine makes and four a person makes before anything is published."),
        ("How we verify", "desk/methodology.html",
         "The method, the sources, and the editorial standards the site is held to."),
        ("Flagged for review", "desk/flagged-for-review.html",
         "Eight open items, each with the source that would settle it."),
    ]
    for title, href, blurb in entries:
        cards += ('<a class="desk-card desk-card-lg" href="%s"><b>%s</b><span>%s</span></a>'
                  % (E(rel(href, root)), E(title), E(blurb)))
    return """
<section class="page-head"><div class="wrap"><p class="eyebrow">The desk</p>
<h1>Where the receipts live.</h1>
<p class="lead">The shop is for readers. The desk is for you: every record, every source, every
open item, and every suggestion with a decision slot left empty for review.</p></div></section>
<section class="wrap section section-tight"><div class="desk-cards desk-cards-lg">%(cards)s</div></section>
<section class="wrap section section-tight"><div class="callout callout-wide">
<h3>The one rule this desk follows</h3><p>Nothing is filled in unless it was read from an official
source, and the source is linked. Where a value could not be confirmed, the cell is blank and the
item is flagged. That rule applies to product specifications, prices, ratings, availability,
review counts, search demand, click counts, orders and revenue.</p></div></section>
""" % {"cards": cards}


def exec_summary(root):
    findings = ""
    for title, text, src_url in D.EXEC_SUMMARY["findings"]:
        findings += """<div class="finding"><h3>%(title)s</h3><p>%(text)s</p>
<p class="finding-source">Source: %(src)s</p></div>""" % {
            "title": E(title), "text": E(text),
            "src": cite_link(src_url, src_url, root),
        }

    decisions = ""
    for title, how, ref, skey in D.EXEC_SUMMARY["decisions"]:
        ref_html = " ".join(
            '<a href="%s#%s">%s</a>' % (E(rel("desk/suggestions.html", root)),
                                        E(r.strip()), E(r.strip()))
            for r in ref.split(",")
        )
        decisions += ("<tr><td><b>%s</b></td><td>%s</td><td>%s</td>"
                      "<td class=\"src-cell\"><a href=\"%s\" rel=\"noopener\" target=\"_blank\">%s</a></td></tr>"
                      % (E(title), E(how), ref_html,
                         E(D.SOURCES[skey]["url"]), E(D.SOURCES[skey]["title"])))

    done = "".join("<li>%s</li>" % E(x) for x in D.EXEC_SUMMARY["done"])

    flags = "".join(
        '<tr><td class="mono"><a href="%s#%s">%s</a></td><td><b>%s</b></td><td>%s</td>'
        '<td>%s</td></tr>'
        % (E(rel("desk/flagged-for-review.html", root)), f["id"], E(f["id"]),
           E(f["title"]), E(f["severity"]), cite_link(f["source"], "Source", root))
        for f in D.FLAGS
    )

    return """
<section class="page-head"><div class="wrap"><p class="eyebrow">The desk &middot; Executive summary</p>
<h1>The position,<br>in one page.</h1>
<p class="lead">What was confirmed, what was found, what is still open, and the five decisions
that would move this forward.</p></div></section>

<section class="wrap section section-tight"><div class="split">
<div><h2 class="h3">Situation</h2><p class="prose-lead">%(sit)s</p>
<h2 class="h3">What is already done</h2><ul class="tick-list">%(done)s</ul></div>
<div class="panel"><h3>Five decisions</h3><div class="table-wrap"><table class="data-table">
<thead><tr><th>Decision</th><th>How</th><th>Suggestion</th><th>Authority</th></tr></thead>
<tbody>%(decs)s</tbody></table></div>
<p class="side-note">Each maps to a suggestion in the register with an empty decision column.</p>
<p><a href="%(suggest)s">Open the suggestions register</a></p></div></div></section>

<section class="wrap section section-tight"><div class="section-head"><div><p class="eyebrow">Findings</p>
<h2>Five things the check turned up.</h2></div><p class="section-note">Each links to the official
source it was read from.</p></div><div class="finding-grid">%(findings)s</div></section>

<section class="wrap section section-tight"><div class="section-head"><div><p class="eyebrow">Open items</p>
<h2>What still needs a human.</h2></div><p class="section-note">Unverified items do not block the
site. They are published so they can be reviewed.</p></div>
<div class="table-wrap"><table class="data-table"><thead><tr><th>ID</th><th>Item</th><th>Severity</th><th>Source</th></tr></thead>
<tbody>%(flags)s</tbody></table></div>
<p class="editorial-note">Full detail on the <a href="%(flagspage)s">flagged for review</a> page.</p></section>
""" % {
        "sit": E(D.EXEC_SUMMARY["situation"]),
        "done": done,
        "decs": decisions,
        "findings": findings,
        "flags": flags,
        "flagspage": E(rel("desk/flagged-for-review.html", root)),
        "suggest": E(rel("desk/suggestions.html", root)),
    }


def product_records(root):
    rows = []
    for p in D.PRODUCTS:
        intent_asin = E(p["intent_asin"]) if p["intent_asin"] else '<span class="unverified">Not confirmed</span>'
        intent_listing = (
            cite_link(p["intent_listing"], p["intent_listing"], root)
            if p["intent_listing"] else '<span class="unverified">Not confirmed</span>'
        )
        special = (
            '<a href="%s" rel="sponsored nofollow noopener" target="_blank">Special Link</a>' % E(p["intent_special_link"])
            if p["intent_special_link"] else '<span class="unverified">Not confirmed</span>'
        )
        observed = (
            cite_link(p["observed_redirect"], p["observed_redirect"], root)
            if p["observed_redirect"] else '<span class="unverified">Not observed</span>'
        )
        source = (
            cite_link(p["observed_redirect"], "Official listing", root)
            if p["observed_redirect"] else
            cite_link(p["submitted"], "Amazon checkpoint", root)
        )
        rows.append("""<tr id="%(token)s"><td class="num">%(slot)d</td>
<td class="mono">%(submitted)s</td><td>%(asin)s</td><td>%(listing)s</td><td class="mono">%(special)s</td>
<td>%(seen)s</td><td>%(observed)s</td><td>%(source)s</td><td>%(flags)s</td></tr>""" % {
            "token": E(p["token"]), "slot": p["slot"],
            "submitted": E(p["submitted"]),
            "asin": intent_asin,
            "listing": intent_listing,
            "special": special,
            "seen": E(p["observed_on"]),
            "observed": observed,
            "source": source,
            "flags": flag_chips(p["flags"], root),
        })

    spec_blocks = ""
    for p in D.PRODUCTS:
        if not p["specs"]:
            continue
        srows = ""
        for label, value, origin in p["specs"]:
            if value:
                val = E(value)
                if origin == "Listing page":
                    val += ' <span class="cell-src">listing page</span>'
                elif origin:
                    val += ' <span class="cell-src">%s</span>' % E(origin.lower())
            else:
                val = '<span class="unverified">Not confirmed</span>'
            srows += "<tr><th scope=\"row\">%s</th><td>%s</td><td class=\"src-cell\">%s</td></tr>" % (
                E(label), val,
                cite_link(p["observed_redirect"], "official listing", root)
                if p["observed_redirect"] else
                cite_link(p["submitted"], "amazon.com", root),
            )
        spec_blocks += """<div class="spec-block" id="spec-%(token)s">
<h3>%(slot)02d &middot; %(name)s</h3>
<p class="spec-sub">%(sub)s</p>
<table class="data-table spec-table"><thead><tr><th>Attribute</th><th>Value</th><th>Source</th></tr></thead>
<tbody>%(rows)s</tbody></table>%(flags)s</div>""" % {
            "token": E(p["token"]), "slot": p["slot"], "name": E(p["name"]),
            "sub": E(p["observed_title"] or "No product identity observed for this record."),
            "rows": srows,
            "flags": ('<p class="spec-flags">%s</p>' % flag_chips(p["flags"], root)) if p["flags"] else "",
        }

    return """
<section class="page-head"><div class="wrap"><p class="eyebrow">The desk &middot; Product records</p>
<h1>The product-intent<br>confirmation record.</h1>
<p class="lead">For every submitted link: the intended ASIN, the official listing URL, the
confirmation date and the source \u2014 kept in their own fields, and never merged with the redirect
target that was actually observed.</p></div></section>

<section class="wrap section section-tight"><div class="callout callout-wide">
<h3>Why two fields and not one</h3><p>An Amazon Standard Identification Number is a unique
10-character alphanumeric code that appears after <span class="mono">/dp/</span> in a product detail
URL. Each of the five submitted tokens is nine characters long, so none of them is an ASIN. Keeping
the intent and the observation apart means a redirect can never quietly become a claim.</p>
<p>Source: <a href="%(asin)s" rel="noopener" target="_blank">Amazon Selling Partner Blog \u2014
Understanding ASINs</a></p></div></section>

<section class="wrap section section-tight"><div class="table-wrap"><table class="data-table records-table">
<thead><tr><th>#</th><th>Submitted link</th><th>Intended ASIN</th><th>Official listing URL</th>
<th>Special Link (intent)</th><th>Confirmed on</th><th>Observed redirect target</th><th>Source</th><th>Flags</th></tr></thead>
<tbody>%(rows)s</tbody></table></div>
<p class="editorial-note">The <em>Special Link</em> column is what this site publishes. It is built
from the tracking ID supplied by the site owner, <span class="mono">%(tag)s</span>. Whether that ID is
issued to an enrolled account, and whether a click appears in that account's own report, is
<a href="%(flagspage)s#FLG-003">FLG-003</a> and is not asserted here.</p></section>

<section class="wrap section section-tight"><div class="section-head"><div><p class="eyebrow">Record by record</p>
<h2>What each listing states.</h2></div><p class="section-note">Only what the official listing
states is repeated. A blank cell means it was not confirmed.</p></div>%(specs)s</section>

<section class="wrap section section-tight"><div class="callout callout-wide">
<h3>Reading these records correctly</h3><p>An observed redirect is evidence that a link resolved
to a listing on a given date. It is not evidence that the product is the one intended, that the
link carries a valid tag, or that it will earn a commission. Those are separate questions, and
they are recorded separately.</p></div></section>
""" % {
        "rows": "".join(rows),
        "specs": spec_blocks,
        "asin": E(D.SOURCES["asin"]["url"]),
        "tag": E(D.SITE["tracking_id_supplied"]),
        "flagspage": E(rel("desk/flagged-for-review.html", root)),
    }


def suggestions_page(root):
    groups = []
    for g in ("Now \u2014 before anything else", "Next \u2014 content and design",
              "Later \u2014 measurement and automation"):
        rows = []
        for s in D.SUGGESTIONS:
            if s["group"] != g:
                continue
            refs = "".join(
                '<a href="%s" rel="noopener" target="_blank">%s</a><br>'
                % (E(D.SOURCES[k]["url"]), E(D.SOURCES[k]["title"]))
                for k in D.SUGGESTION_SOURCES.get(s["id"], [])
            )
            rows.append("""<tr id="%(id)s"><td class="mono">%(id)s</td><td><b>%(title)s</b><p class="cell-why">%(why)s</p></td>
<td>%(effort)s</td><td>%(dep)s</td><td class="risk-%(riskslug)s">%(risk)s</td>
<td>%(ev)s</td><td class="src-cell">%(refs)s</td><td class="decision-cell"></td></tr>""" % {
                "id": E(s["id"]),
                "title": E(s["title"]),
                "why": E(s["why"]),
                "effort": E(s["effort"]),
                "dep": E(s["depends"]),
                "riskslug": E(s["risk"].lower()),
                "risk": E(s["risk"]),
                "ev": E(s["evidence"]),
                "refs": refs,
            })
        groups.append("""<section class="sugg-group"><h2 class="h3">%(g)s</h2>
<div class="table-wrap"><table class="data-table sugg-table"><thead><tr><th>ID</th><th>Suggestion and why</th>
<th>Effort</th><th>Depends on</th><th>Risk</th><th>Evidence</th><th>Official reference</th><th>Decision</th></tr></thead>
<tbody>%(rows)s</tbody></table></div></section>""" % {"g": E(g), "rows": "".join(rows)})

    return """
<section class="page-head"><div class="wrap"><p class="eyebrow">The desk &middot; Suggestions</p>
<h1>Suggestions,<br>with a decision slot.</h1>
<p class="lead">Fifteen proposals, each with the evidence behind it, what it depends on, how much
effort it takes, and what could go wrong. Nothing here has been applied automatically. The last
column is deliberately empty so a reviewer can choose.</p></div></section>

<section class="wrap section section-tight"><div class="callout callout-wide">
<h3>How to use this page</h3><p>Read the group headings in order. The <em>Now</em> group is what
should happen before the site is scaled or a product is written about at length. The
<em>Next</em> group is about how the site reads and looks. The <em>Later</em> group is about
measurement and automation, and it carries the highest risk items. Write a decision in the last
column, or on a copy, and it becomes the build order.</p></div></section>

%(groups)s

<section class="wrap section section-tight"><div class="callout callout-wide callout-flag">
<h3>One suggestion needs legal input first</h3><p>S-14 touches the Associates IP License, which
restricts using Special Links and Program Content to develop machine learning models without
express prior written approval. That is a different question from writing guides with an
assistant, and it should be answered in writing before anything is built.</p>
<p><a href="%(flagspage)s#FLG-008">FLG-008</a> &middot; <a href="%(policies)s">Amazon Associates Program Policies</a></p>
</div></section>
""" % {
        "groups": "".join(groups),
        "flagspage": E(rel("desk/flagged-for-review.html", root)),
        "policies": E(D.SOURCES["policies"]["url"]),
    }


def questions_page(root):
    rows = []
    for q in D.QUESTIONS:
        status_kind = {"Open": "flag", "Partly answered": "warn", "Answered": "ok"}.get(q["status"], "muted")
        srcs = "".join(
            '<a href="%s" rel="noopener" target="_blank">%s</a> '
            % (E(D.SOURCES[k]["url"]), E(D.SOURCES[k]["title"]))
            for k in q["sources"]
        )
        rows.append("""<tr id="%(id)s"><td class="mono">%(id)s</td><td><b>%(q)s</b></td>
<td>%(status)s</td><td>%(answer)s</td><td>%(known)s</td><td>%(missing)s</td><td>%(discovery)s</td>
<td class="src-cell">%(srcs)s</td></tr>""" % {
            "id": E(q["id"]),
            "q": E(q["question"]),
            "status": chip(q["status"], status_kind),
            "answer": E(q["answer"]),
            "known": E(q["known"]),
            "missing": E(q["missing"]),
            "discovery": E(q["discovery"]),
            "srcs": srcs,
        })
    rows = "".join(rows)

    return """
<section class="page-head"><div class="wrap"><p class="eyebrow">The desk &middot; Open questions</p>
<h1>What we need to know<br>before deciding anything.</h1>
<p class="lead">Eight questions, each with the answer so far, what is still missing, and the
specific discovery step that would settle it. This is the list to work through before the next
decision is reasonably made.</p></div></section>

<section class="wrap section section-tight"><div class="table-wrap"><table class="data-table q-table">
<thead><tr><th>ID</th><th>Question</th><th>Status</th><th>Answer so far</th><th>What we know</th>
<th>What is missing</th><th>Suggested discovery</th><th>Official sources</th></tr></thead>
<tbody>%(rows)s</tbody></table></div></section>

<section class="wrap section section-tight"><div class="split">
<div><h2 class="h3">How to close a question</h2>
<ol class="decisions">
<li>Find the authorised source \u2014 the enrolled Associates account, the Product Advertising API
response, or the official listing page.</li>
<li>Record the date you read it and the exact URL. A finding without a date goes stale silently.</li>
<li>Write the value into the record it belongs to, and leave every other field alone.</li>
<li>If the source does not answer it, say so in the record rather than closing the question.</li>
</ol></div>
<div class="panel"><h3>What a good answer looks like</h3>
<p>Traceable, dated, and specific enough that someone else repeating the same step gets the same
result. \u201cThe price is about seventy dollars\u201d fails all three tests. \u201cListed at $74.99 on
the official product page on 20 November 2026, source linked\u201d passes all three.</p>
<p><a href="%(method)s">How we verify</a></p></div></div></section>
""" % {
        "rows": rows,
        "method": E(rel("desk/methodology.html", root)),
    }


def ledger_page(root):
    head = "".join("<th>%s</th>" % E(name) for name, _ in D.LEDGER_SCHEMA)
    rows = "".join(
        "<tr>%s</tr>" % "".join("<td>%s</td>" % E(v) for v in row) for row in D.LEDGER_ROWS
    )
    if not rows:
        rows = ('<tr><td colspan="%d" class="ledger-empty">No authorised report data recorded yet. '
                'This ledger is empty by design and stays empty until a first-party report is '
                'imported with its provenance. Source of truth: '
                '<a href="%s" rel="noopener" target="_blank">Amazon Associates Program Policies</a>'
                '</td></tr>' % (len(D.LEDGER_SCHEMA), E(D.SOURCES["policies"]["url"])))

    events = "".join(
        "<tr><td class=\"mono\">%s</td><td>%s</td><td>%s</td><td class=\"src-cell\">%s</td></tr>"
        % (E(name), E(desc), E(where),
           cite_link(D.SOURCES["policies"]["url"], "IP License and Commission Income Statement", root))
        for name, desc, where in [
            ("page_view", "A page was opened.", "Every page."),
            ("outbound_click", "A reader clicked a link to Amazon.", "Every product link, marked sponsored."),
            ("guide_open", "A guide was opened.", "Every guide page, with the guide id."),
            ("search_query_referral", "A visit arrived from a search engine.",
             "Recorded on the landing page with the referring engine and any query term carried in the URL."),
            ("report_import", "An authorised report was imported into the ledger.",
             "Fired by the ledger import control, with the report name and date."),
        ]
    )

    return """
<section class="page-head"><div class="wrap"><p class="eyebrow">The desk &middot; Campaign ledger</p>
<h1>Evidence before<br>optimisation.</h1>
<p class="lead">A fixed schema with no rows. It will be filled only from authorised first-party
reports, each with a dated provenance trail. No conversion score and no revenue forecast appear
anywhere on this site.</p></div></section>

<section class="wrap section section-tight"><div class="table-wrap"><table class="data-table ledger-table">
<thead><tr>%(head)s</tr></thead><tbody>%(rows)s</tbody></table></div>
<p class="editorial-note">Source of truth for what a row may contain:
<a href="%(policies)s">Amazon Associates Program Policies</a> (Commission Income Statement, and the
IP License requirement to disclose accurately how visitor data is collected and stored).</p></section>

<section class="wrap section section-tight"><div class="split">
<div><h2 class="h3">The import control</h2>
<p>When an authorised report is available, load the file below. It records a
<span class="mono">report_import</span> event and a provenance row. It does not invent a figure,
and it does not fill a cell that the report does not contain.</p>
<p class="ledger-actions"><label class="file-label">Choose an authorised report
<input type="file" id="report-file" accept=".csv,.txt" class="file-input"></label>
<button class="btn btn-dark" id="report-import">Import and record provenance</button></p>
<p class="ledger-status" id="report-status" role="status">No report loaded.</p>
</div>
<div class="panel"><h3>What is collected by the tracker</h3>
<p>Event name, page path, referrer host, the outbound host a reader clicked, a guide id, a
timestamp, and a truncated salted hash of the IP address that changes daily. No cookies, no
advertising identifiers, no fingerprinting, no cross-site identifiers, and no storage of query
strings on outbound links. Retention is 90 days.</p>
<p><a href="%(method)s#privacy">Read the method</a></p></div></div></section>

<section class="wrap section section-tight"><div class="section-head"><div><p class="eyebrow">Event definitions</p>
<h2>Five events, defined once.</h2></div><p class="section-note">The collector ships in the
repository but is not deployed. Until it is, nothing is collected and no number on this site
moves.</p></div>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Event</th><th>Meaning</th>
<th>Where it fires</th><th>Authority</th></tr></thead><tbody>%(events)s</tbody></table></div></section>
""" % {
        "head": head,
        "rows": rows,
        "events": events,
        "policies": E(D.SOURCES["policies"]["url"]),
        "method": E(rel("desk/methodology.html", root)),
    }


def gate_page(root):
    rows = []
    for g in D.GATE:
        kind = "ok" if g["state"] == "pass" else "flag"
        rows.append("""<tr><td class="mono">%(id)s</td><td><b>%(check)s</b><p class="cell-why">%(why)s</p></td>
<td>%(how)s</td><td>%(type)s</td><td>%(state)s</td><td class="src-cell">
<a href="%(src)s" rel="noopener" target="_blank">%(srctitle)s</a></td></tr>""" % {
            "id": E(g["id"]),
            "check": E(g["check"]),
            "why": E(g["why"]),
            "how": E(g["how"]),
            "type": chip("Machine" if g["type"] == "machine" else "Human", "muted"),
            "state": chip("Pass" if g["state"] == "pass" else "Pending", kind),
            "src": E(D.SOURCES[g["source"]]["url"]),
            "srctitle": E(D.SOURCES[g["source"]]["title"]),
        })
    machine = sum(1 for g in D.GATE if g["type"] == "machine")
    human = len(D.GATE) - machine

    return """
<section class="page-head"><div class="wrap"><p class="eyebrow">The desk &middot; Publishing gate</p>
<h1>What has to be true<br>before we publish.</h1>
<p class="lead">%(machine)d checks a script makes on every build, and %(human)d that need a person.
The automated ones run in <span class="mono">scripts/check_site.py</span> and fail the deployment
if they break.</p></div></section>

<section class="wrap section section-tight"><div class="table-wrap"><table class="data-table gate-table">
<thead><tr><th>ID</th><th>Check</th><th>How it is enforced</th><th>Type</th><th>State</th><th>Authority</th></tr></thead>
<tbody>%(rows)s</tbody></table></div></section>

<section class="wrap section section-tight"><div class="split">
<div><h2 class="h3">The human half</h2>
<p>Four checks cannot be automated, because they are judgements about context and language:</p>
<ol class="decisions">
<li><b>The collector is really deployed.</b> Confirm the endpoint answers before enabling the
tracker everywhere.</li>
<li><b>The privacy notice matches reality.</b> Write it against what the deployed collector does,
not against what it was meant to do.</li>
<li><b>The endorsement context is honest.</b> Read each product card as a reader would. We have
not handled these appliances and the copy must not imply that we have.</li>
<li><b>One link per product has been tested</b> in the enrolled Associates workflow, with the
destination and the tracking report confirmed.</li>
</ol></div>
<div class="panel"><h3>Why the automated half exists</h3>
<p>A disclosure strip that is present on fourteen pages and missing from the fifteenth is a real
failure mode, and it is invisible until someone notices. Scripting the boring checks makes the
human checks the only ones that need attention.</p>
<p><a href="%(records)s">Product records</a></p></div></div></section>
""" % {
        "rows": "".join(rows),
        "machine": machine,
        "human": human,
        "records": E(rel("desk/product-records.html", root)),
    }


def flagged_page(root):
    blocks = []
    for f in D.FLAGS:
        kind = "ok" if f["severity"] == "Unverified" else "flag"
        blocks.append("""<article class="flag-block" id="%(id)s">
<div class="flag-head"><span class="flag-id">%(id)s</span>%(sev)s</div>
<h2>%(title)s</h2><p>%(detail)s</p>
<p class="flag-action"><b>What would settle it:</b> %(action)s</p>
<p class="flag-source">Source: %(src)s</p>
</article>""" % {
            "id": E(f["id"]),
            "sev": chip(f["severity"], kind),
            "title": E(f["title"]),
            "detail": E(f["detail"]),
            "action": E(f["action"]),
            "src": cite_link(f["source"], f["source"], root),
        })

    rows = "".join(
        '<tr><td class="mono"><a href="#%s">%s</a></td><td>%s</td><td>%s</td>'
        '<td class="src-cell">%s</td></tr>'
        % (E(f["id"]), E(f["id"]), E(f["title"]), E(f["severity"]),
           cite_link(f["source"], "source", root))
        for f in D.FLAGS
    )

    return """
<section class="page-head"><div class="wrap"><p class="eyebrow">The desk &middot; Flagged for review</p>
<h1>Flagged for<br>review.</h1>
<p class="lead">Every irregularity and unverified value on this site, in one place, with the
source that would settle it. None of these blocks the site going live. Unverified means
unverified, not invalid.</p></div></section>

<section class="wrap section section-tight"><div class="table-wrap"><table class="data-table">
<thead><tr><th>ID</th><th>Item</th><th>Severity</th><th>Source</th></tr></thead>
<tbody>%(rows)s</tbody></table></div></section>

<section class="wrap section section-tight">%(blocks)s</section>
""" % {"rows": rows, "blocks": "".join(blocks)}


def methodology_page(root):
    srcs = []
    for key, s in D.SOURCES.items():
        srcs += """<tr><td><b>%(title)s</b><p class="cell-why">%(note)s</p></td>
<td class="src-cell"><a href="%(url)s" rel="noopener" target="_blank">%(url)s</a></td></tr>""" % {
            "title": E(s["title"]), "note": E(s["note"]), "url": E(s["url"]),
        }

    return """
<section class="page-head"><div class="wrap"><p class="eyebrow">The desk &middot; Method</p>
<h1>How we verify,<br>and why.</h1>
<p class="lead">A short method, applied consistently, with the limit of each source stated next to
it. If a value is not on this list, it is not published.</p></div></section>

<section class="wrap section section-tight"><div class="split">
<div><h2 class="h3">The rule</h2>
<p class="prose-lead">A value appears on this site only if it was read from an official source,
with the URL and the date recorded. Where that is not possible, the cell is blank, the line is
flagged, and the reason is on the flagged-for-review page.</p>
<h2 class="h3">How a product record is built</h2>
<ol class="decisions">
<li><b>Intent.</b> Record the intended ASIN and the official listing URL separately, with the
date confirmed and the source named.</li>
<li><b>Observation.</b> Follow the submitted link and record where it resolves, in its own
field, with the date.</li>
<li><b>Never merge.</b> An observation never becomes an intent, and an intent is never treated
as an observation.</li>
<li><b>Specification.</b> Repeat only what the official listing states. Everything else is
blank.</li>
<li><b>Price and rating.</b> These are Product Advertising Content. The IP License permits them
only through the Creators API or PA API, so the shop pages show none, and the desk records dated
observations with their source.</li>
</ol></div>
<div class="panel"><h3>What we do not publish</h3>
<ul class="tick-list">
<li>Star ratings or review counts that were not read from an official source.</li>
<li>Review summaries written by anyone other than a reviewer.</li>
<li>Search volume, popularity, best-seller ranks or trend claims.</li>
<li>Commission rates, click counts, order counts or revenue.</li>
<li>Any statement that we have used or handled a product.</li>
<li>Any superlative we cannot evidence.</li>
</ul></div></div></section>

<section class="wrap section section-tight" id="disclosure"><div class="split">
<div><h2 class="h3">Disclosure and links</h2>
<p>The statement <strong>&ldquo;%(disc)s&rdquo;</strong> appears above the masthead on every page of this
site and is repeated in the footer. The FTC's Endorsement Guides say an affiliate relationship
should be disclosed clearly and conspicuously, that \u201caffiliate link\u201d on its own is not
adequate, and that the closer the disclosure is to the recommendation the better.</p>
<p>Every outbound product link carries <span class="mono">rel="sponsored nofollow noopener"</span>.
Product links are Special Links built from the tracking ID supplied by the site owner; whether that
ID is enrolled on an account is <a href="%(flagspage)s#FLG-003">FLG-003</a>.</p></div>
<div class="panel"><h3>The rules we apply</h3>
<ul class="tick-list">
<li>Disclosure above the masthead, on every page.</li>
<li>Sponsored marking on every outbound product link.</li>
<li>Disclosure repeated in the footer of every page.</li>
<li>No price, rating or availability on reader-facing pages until the API is connected.</li>
<li>No claim that we have handled the products we write about.</li>
</ul></div></div></section>

<section class="wrap section section-tight" id="privacy"><div class="split">
<div><h2 class="h3">Privacy and measurement</h2>
<p>The tracker on this site is privacy preserving by design: no cookies, no advertising
identifiers, no fingerprinting and no cross-site identifiers. It records five event types and
nothing else. The server keeps a truncated, daily-rotated salted hash of the IP address rather
than the address itself, and the referrer host rather than a full referrer URL, so a search query
in a referrer is not stored.</p>
<p>Nothing is collected until the endpoint is deployed. The collector code is in the repository,
and the ledger stays empty until an authorised first-party report is imported.</p></div>
<div class="panel"><h3>Retention and access</h3>
<ul class="tick-list">
<li>Events retained for 90 days, then discarded.</li>
<li>No personal identifiers, no account identifiers, no order data.</li>
<li>Outbound click events record the destination host only, never the query string.</li>
<li>The privacy notice must be written against the deployed behaviour before the collector is
switched on. That is gate row G-10.</li>
</ul></div></div></section>

<section class="wrap section section-tight" id="sources"><div class="section-head"><div>
<p class="eyebrow">Sources</p><h2>Every official source we rely on.</h2></div>
<p class="section-note">Read in order: program rules, then the standard they set, then the
measurement sources.</p></div>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Source and what it establishes</th>
<th>Link</th></tr></thead><tbody>%(srcs)s</tbody></table></div></section>
""" % {
        "srcs": "".join(srcs),
        "disc": E(D.DISCLOSURE),
        "flagspage": E(rel("desk/flagged-for-review.html", root)),
    }


# ---------------------------------------------------------------------------- writers
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    return path


def build_sitemap(paths):
    urls = []
    for p in paths:
        urls.append("  <url><loc>%s/%s</loc></url>" % (ORIGIN, p.lstrip("/")))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def build_feed():
    items = []
    for g in D.GUIDES:
        items.append(
            "<item><title>%s</title><link>%s/guides/%s.html</link>"
            "<guid isPermaLink=\"true\">%s/guides/%s.html</guid>"
            "<pubDate>%s</pubDate><description>%s</description></item>"
            % (E(g["title"]), ORIGIN, g["slug"], ORIGIN, g["slug"],
               _rfc822(g["published"]), E(g["dek"]))
        )
    for c in D.CATEGORIES:
        items.append(
            "<item><title>%s</title><link>%s/shop/%s.html</link>"
            "<guid isPermaLink=\"true\">%s/shop/%s.html</guid>"
            "<pubDate>%s</pubDate><description>%s</description></item>"
            % (E(c["title"]), ORIGIN, c["slug"], ORIGIN, c["slug"],
               _rfc822(D.SITE["published"]), E(c["blurb"]))
        )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n'
            "<title>%s \u2014 %s</title>\n<link>%s/</link>\n"
            "<description>Question-led kitchen buying guides and a sourced evidence desk.</description>\n"
            "<language>en-us</language>\n<lastBuildDate>%s</lastBuildDate>\n"
            '<atom:link href="%s/feed.xml" rel="self" type="application/rss+xml"/>\n'
            "%s\n</channel>\n</rss>\n"
            % (E(D.SITE["name"]), E(D.SITE["tagline"]), ORIGIN,
               _rfc822(D.SITE["updated"]), ORIGIN, "\n".join(items)))


def _rfc822(iso):
    d = datetime.datetime.strptime(iso, "%Y-%m-%d")
    return d.strftime("%a, %d %b %Y %H:%M:%S +0000")


ROBOTS = """User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
""" % ORIGIN


NOT_FOUND = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found &mdash; Good Measure Kitchen</title>
<meta name="description" content="That page is not here. Here is where everything moved to.">
<link rel="stylesheet" href="/styles.css"></head>
<body class="page-404">
<div class="disclosure"><span class="disclosure-inner"><strong>As an Amazon Associate I earn from qualifying purchases.</strong></span></div>
<header class="masthead"><div class="wrap masthead-inner">
<a class="brand" href="/"><span class="brand-mark">gm</span><span class="brand-text">Good Measure Kitchen<span class="brand-sub">Kitchen Notes</span></span></a>
<nav class="nav"><ul><li class="nav-item"><a class="nav-top" href="/shop/index.html">Shop</a></li>
<li class="nav-item"><a class="nav-top" href="/guides/index.html">Guides</a></li>
<li class="nav-item"><a class="nav-top" href="/desk/index.html">The Desk</a></li></ul></nav>
</div></header>
<main id="main"><section class="wrap section"><p class="eyebrow">404</p>
<h1>That page is not here.</h1><p class="lead">It may have moved. Everything the site publishes is
one click away.</p>
<ul class="guide-links">
<li><a href="/">Front page</a></li><li><a href="/shop/index.html">The shelf</a></li>
<li><a href="/guides/index.html">All guides</a></li><li><a href="/desk/index.html">The desk</a></li>
<li><a href="/desk/executive-summary.html">Executive summary</a></li>
<li><a href="/desk/flagged-for-review.html">Flagged for review</a></li></ul>
</section></main>
<footer class="site-footer"><div class="wrap footer-bottom"><span>Good Measure Kitchen</span></div></footer>
</body></html>
"""


def main():
    written = []

    # root
    written.append(write("index.html", page(
        title="%s \u2014 %s" % (D.SITE["name"], D.SITE["tagline"]),
        description="Question-led kitchen buying guides and a sourced evidence desk. Four products "
                    "confirmed against official Amazon listings, six guides, and every unverified "
                    "value flagged with the source that would settle it.",
        root="", body=front_page(""), active="Shop", path="index.html")))

    # shop
    written.append(write("shop/index.html", page(
        title="The shelf \u2014 %s" % D.SITE["name"],
        description="Every product record on the site, with the format, the ASIN, the dated price "
                    "observation and a link to the official listing. Blank cells were not confirmed.",
        root="../", body=shop_index("../"), active="Shop", path="shop/index.html")))
    for c in D.CATEGORIES:
        written.append(write("shop/%s.html" % c["slug"], page(
            title="%s \u2014 %s" % (c["title"], D.SITE["name"]),
            description=c["blurb"],
            root="../", body=category_page(c, "../"), active="Shop",
            path="shop/%s.html" % c["slug"])))

    # guides
    written.append(write("guides/index.html", page(
        title="Guides \u2014 %s" % D.SITE["name"],
        description="Six question-shaped guides on kitchen formats, capacity, cleanup, "
                    "versatility, technique and seasonal cooking.",
        root="../", body=guide_index("../"), active="Guides", path="guides/index.html")))
    for g in D.GUIDES:
        written.append(write("guides/%s.html" % g["slug"], page(
            title="%s \u2014 %s" % (g["title"], D.SITE["name"]),
            description=g["dek"],
            root="../", body=guide_page(g, "../"), active="Guides",
            path="guides/%s.html" % g["slug"])))

    # desk
    desk_pages = [
        ("desk/index.html", "The desk \u2014 %s" % D.SITE["name"],
         "Every record, source, open item and suggestion, in one place.",
         desk_index, "Desk"),
        ("desk/executive-summary.html", "Executive summary \u2014 %s" % D.SITE["name"],
         "The position in one page: what was confirmed, what was found, what is still open.",
         exec_summary, "Desk"),
        ("desk/product-records.html", "Product records \u2014 %s" % D.SITE["name"],
         "The product-intent confirmation record. Intended ASIN, listing URL, confirmation date and "
         "source, kept separate from the observed redirect target.",
         product_records, "Desk"),
        ("desk/suggestions.html", "Suggestions register \u2014 %s" % D.SITE["name"],
         "Fifteen proposals with evidence, effort, dependency, risk and an empty decision column.",
         suggestions_page, "Desk"),
        ("desk/questions.html", "Open questions \u2014 %s" % D.SITE["name"],
         "Eight questions with the answer so far, what is missing, and the discovery step that "
         "would settle it.",
         questions_page, "Desk"),
        ("desk/ledger.html", "Campaign ledger \u2014 %s" % D.SITE["name"],
         "An empty but fully defined campaign ledger, to be filled only from authorised "
         "first-party reports.",
         ledger_page, "Desk"),
        ("desk/publishing-gate.html", "Publishing gate \u2014 %s" % D.SITE["name"],
         "Eight checks a script makes on every build, and four that need a person.",
         gate_page, "Desk"),
        ("desk/flagged-for-review.html", "Flagged for review \u2014 %s" % D.SITE["name"],
         "Every irregularity and unverified value on the site, with the source that would settle it.",
         flagged_page, "Desk"),
        ("desk/methodology.html", "How we verify \u2014 %s" % D.SITE["name"],
         "The verification method, the disclosure standard, the privacy approach and every "
         "official source the site relies on.",
         methodology_page, "Desk"),
    ]
    for path, title, desc, fn, active in desk_pages:
        written.append(write(path, page(
            title=title, description=desc, root="../", body=fn("../"),
            active=active, path=path)))

    written.append(write("404.html", NOT_FOUND))
    written.append(write("robots.txt", ROBOTS))
    written.append(write(".nojekyll", ""))

    paths = ["index.html", "shop/index.html", "guides/index.html", "desk/index.html"]
    paths += ["shop/%s.html" % c["slug"] for c in D.CATEGORIES]
    paths += ["guides/%s.html" % g["slug"] for g in D.GUIDES]
    paths += [p for p, _, _, _, _ in desk_pages]

    written.append(write("sitemap.xml", build_sitemap(paths)))
    written.append(write("feed.xml", build_feed()))

    print("Rendered %d files." % len(written))
    for p in sorted(written):
        print("  %s" % p)


if __name__ == "__main__":
    main()
