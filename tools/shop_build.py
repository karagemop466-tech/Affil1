#!/usr/bin/env python3
"""The Pantry Journal — static shop generator.

Reads src/shopdata/*.json and writes shop/ as plain HTML.

Design rules enforced by construction:
  * one template, so no page can ship without the disclosure strip or the footer;
  * every link inside shop/ is relative, because GitHub Pages serves this
    repository under /Affil1/;
  * every outbound Amazon link carries rel="sponsored nofollow noopener" and
    the Associates tag as a visible URL parameter;
  * no price, rating, review count or availability is emitted, ever.

Run:  python3 tools/shop_build.py
Then: python3 tools/shop_check.py
"""

import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "shopdata"
OUT = ROOT / "archive" / "2026-11-20-pantry-journal"

BASE = "https://karagemop466-tech.github.io/Affil1/archive/2026-11-20-pantry-journal/"
SITE = "The Pantry Journal"
TAG = "shopnow047c-20"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
BUILD_DATE = "2026-11-20"

PRODUCTS = json.loads((SRC / "products.json").read_text())
EDIT = json.loads((SRC / "editorial.json").read_text())
GUIDES = json.loads((SRC / "guides.json").read_text())
QUESTIONS = json.loads((SRC / "questions.json").read_text())
SUGGESTIONS = json.loads((SRC / "suggestions.json").read_text())
REGISTER = json.loads((SRC / "sources.json").read_text())

P = {p["slug"]: p for p in PRODUCTS["products"]}
G = {g["slug"]: g for g in GUIDES["guides"]}

NAV = [
    ("products/", "Shop", "shop"),
    ("categories/", "Categories", "categories"),
    ("guides/", "Guides", "guides"),
    ("suggestions/", "Suggestions", "suggestions"),
    ("about/", "About", "about"),
]

# Outbound-link counters, used by the checker to prove ordering.
LINK_AUDIT = []


def e(text):
    return html.escape(str(text), quote=True)


def href(depth, target):
    """Site-relative target -> href usable from a page at `depth`."""
    if target.startswith("http") or target.startswith("#") or target.startswith("mailto:"):
        return target
    if target == "":
        return "../" * depth if depth else "./"
    return "../" * depth + target


def canonical(target):
    return BASE + target


def buy_url(p):
    return p["affiliate_url"]


def amazon_link(p, label, depth, where, css="buy", arrow=True):
    """The only way an outbound product link is emitted."""
    LINK_AUDIT.append((depth, p["id"]))
    arw = '<span class="arw" aria-hidden="true">&#8599;</span>' if arrow else ""
    return (
        f'<a class="{css}" href="{e(buy_url(p))}" rel="sponsored nofollow noopener" '
        f'target="_blank" data-product="{e(p["id"])}" data-where="{e(where)}">'
        f'<span>{label}</span>{arw}</a>'
    )


def bullets(items):
    return "<ul>" + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def data_table(caption, cols, rows, wrap_class="t-wrap"):
    head = "".join(f"<th scope=\"col\">{c}</th>" for c in cols)
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows
    )
    cap = f"<caption>{caption}</caption>" if caption else ""
    return f'<div class="{wrap_class}"><table>{cap}<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def source_link(url, label):
    """A citation. Product URLs are affiliate paths, so they are marked
    sponsored; policy and documentation URLs are plain references."""
    if re.search(r"/dp/[A-Za-z0-9]{10}", url):
        return (f'<a href="{e(url)}" rel="sponsored nofollow noopener" target="_blank" '
                f'data-product="cite">{label}</a>')
    return f'<a href="{e(url)}" rel="noopener">{label}</a>'


def pill(kind, text):
    return f'<span class="pill pill-{kind}">{e(text)}</span>'


# --------------------------------------------------------------------------
# page shell
# --------------------------------------------------------------------------

def page(depth, target, title, description, body, active=None, jsonld=None,
         og_image="hero-counter.jpg", crumbs=None, og_type="website", noindex=True):
    nav_html = "".join(
        f'<a href="{href(depth, t)}"' + (' aria-current="page"' if key == active else "") + f'>{e(label)}</a>'
        for t, label, key in NAV
    )
    head_jsonld = ""
    if jsonld:
        head_jsonld = "\n".join(
            '<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False, separators=(",", ":")) + "</script>"
            for b in jsonld
        )

    crumb_html = ""
    if crumbs:
        parts = []
        for label, tgt in crumbs:
            if tgt:
                parts.append(f'<a href="{href(depth, tgt)}">{e(label)}</a>')
            else:
                parts.append(f"<span>{e(label)}</span>")
        crumb_html = '<nav class="breadcrumb wrap" aria-label="Breadcrumb">' + \
            '<span style="margin:0;color:var(--accent)">&#9679;</span>'.join(
                [""] + parts)[1:] + "</nav>"

    fav = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='3' fill='%231a1815'/%3E"
           "%3Ctext x='16' y='22' font-family='Georgia,serif' font-size='15' fill='%23fbf8f2' "
           "text-anchor='middle'%3EPJ%3C/text%3E%3C/svg%3E")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canonical(target))}">
{('<meta name="robots" content="noindex,follow">') if noindex else ''}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical(target))}">
<meta property="og:image" content="{BASE}assets/img/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="{SITE}" href="{href(depth, 'feed.xml')}">
<link rel="icon" href="{fav}">
<link rel="stylesheet" href="{href(depth, 'assets/css/shop.css')}">
<script src="{href(depth, 'assets/js/shop.js')}" defer></script>
{head_jsonld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="mast-in">
    <a class="wordmark" href="{href(depth, '')}">The Pantry Journal
      <span class="sub">Small appliances, chosen with care</span></a>
    <nav class="nav" aria-label="Sections">{nav_html}</nav>
  </div>
</header>
<div class="disc" role="region" aria-label="Affiliate disclosure">
  <div class="disc-in">
    <span class="lbl">Disclosure</span>
    <span><strong>{DISCLOSURE}</strong> Links marked with an arrow go to Amazon; if you buy through one this site may earn a commission at no extra cost to you. <a href="{href(depth, 'about/#disclosure')}">How this works</a>.</span>
  </div>
</div>
{crumb_html}
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <div class="wm">The Pantry Journal</div>
        <p>{e(EDIT['footer']['blurb'])}</p>
      </div>
      <div>
        <h4>Shop</h4>
        <ul>
          <li><a href="{href(depth, 'products/')}">All five appliances</a></li>
          <li><a href="{href(depth, 'categories/')}">Categories</a></li>
          <li><a href="{href(depth, 'guides/')}">Buying guides</a></li>
          <li><a href="{href(depth, 'feed.xml')}">RSS feed</a></li>
        </ul>
      </div>
      <div>
        <h4>The record</h4>
        <ul>
          <li><a href="{href(depth, 'table/')}">Table of record</a></li>
          <li><a href="{href(depth, 'questions/')}">Decisions &amp; open questions</a></li>
          <li><a href="{href(depth, 'flagged/')}">Flagged for review</a></li>
          <li><a href="{href(depth, 'sources/')}">Sources &amp; compliance</a></li>
        </ul>
      </div>
      <div>
        <h4>About</h4>
        <ul>
          <li><a href="{href(depth, 'about/')}">Who writes this</a></li>
          <li><a href="{href(depth, 'suggestions/')}">Suggestions</a></li>
          <li><a href="{href(depth, 'sitemap/')}">Site map</a></li>
          <li><a href="{href(depth, 'sitemap.xml')}">XML sitemap</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-disc">
      <span><strong>{DISCLOSURE}</strong> No price, star rating or stock figure appears on this site: Amazon permits them only where Amazon serves the data, and no such feed is connected here.</span>
      <span>Built {BUILD_DATE}</span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def write(target_dir, filename, text):
    path = OUT / target_dir / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# shared fragments
# --------------------------------------------------------------------------

def product_card(p, depth, where="card"):
    return f"""<article class="p-card">
  <figure>
    <img src="{href(depth, 'assets/img/' + p['image'])}" alt="{e(p['image_alt'])}" loading="lazy" width="1408" height="768">
    <span class="type">{e(p['type_label'])}</span>
  </figure>
  <div class="p-body">
    <p class="p-brand">{e(p['brand'])}</p>
    <h3><a href="{href(depth, 'products/' + p['slug'] + '/')}">{e(p['display_title'])}</a></h3>
    <p class="desc">{e(p['deck'])}</p>
    <div class="p-meta"><span>{e(p['shape'])}</span><span>ASIN {e(p['asin'])}</span></div>
    {amazon_link(p, 'See it on Amazon', depth, where)}
    <p class="buy-note">Sponsored link. Price and stock are shown by Amazon, not here. <a href="{href(depth, 'products/' + p['slug'] + '/')}">Read our notes</a></p>
  </div>
</article>"""


def guide_row(g, depth, n):
    state = "" if g["status"] == "published" else ' <span class="pill pill-quiet">Queued</span>'
    return f"""<article class="g-row">
  <div class="g-num">{n:02d}</div>
  <div class="g-body">
    <p class="kicker">{e(g['kicker'])}</p>
    <h3><a href="{href(depth, 'guides/' + g['slug'] + '/')}">{e(g['title'])}</a>{state}</h3>
    <p>{e(g['deck'])}</p>
  </div>
  <div class="rt">{e(g['read_time'])}</div>
</article>"""


def related_block(slugs, depth, label="Read next"):
    cards = []
    for s in slugs:
        g = G.get(s)
        if not g:
            continue
        cards.append(
            f'<a href="{href(depth, "guides/" + g["slug"] + "/")}">'
            f'<span class="rl">{label}</span><span class="rt">{e(g["short_title"])}</span></a>'
        )
    return '<div class="related">' + "".join(cards) + "</div>"


def org_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE,
        "url": BASE,
        "description": EDIT["brand"]["positioning"],
    }


def crumbs_jsonld(depth, crumbs):
    """crumbs: [(label, target_or_None)]; the last item is the current page."""
    items = []
    for i, (label, tgt) in enumerate(crumbs, 1):
        entry = {"@type": "ListItem", "position": i, "name": label}
        if tgt is not None:
            entry["item"] = canonical(tgt)
        items.append(entry)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


# --------------------------------------------------------------------------
# home
# --------------------------------------------------------------------------

def build_home():
    depth = 0
    f = EDIT["front"]
    picks = "".join(product_card(p, 0, "home-grid") for p in PRODUCTS["products"])
    guides = "".join(guide_row(g, 0, i + 1) for i, g in enumerate(GUIDES["guides"]))
    cmts = "".join(
        f"""<div class="cmt-item">
      <div class="cmt-n">{c['n']}</div>
      <div class="cmt-c">
        <h3>{e(c['title'])}</h3>
        <p>{e(c['body'])}</p>
        <p class="cmt-src">{'Source: <a href="' + e(c['source']) + '" rel="noopener">' + e(c['source_label']) + '</a>' if c['source'] else e(c['source_label'] or '')}</p>
      </div>
    </div>""" for c in EDIT["commitments"]
    )

    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="kicker">{e(f['kicker'])}</p>
      <h1>The countertop,<br><em>decided.</em></h1>
      <p class="deck">{e(f['deck'])}</p>
      <div class="btn-row">
        <a class="btn" href="{href(0, 'products/')}">{e(f['cta_primary']['label'])} <span aria-hidden="true">&#8594;</span></a>
        <a class="btn btn-ghost" href="{href(0, f['cta_secondary']['href'])}">{e(f['cta_secondary']['label'])}</a>
      </div>
      <p class="byline" style="margin-top:22px">
        <span>Five machines</span><span class="dot">&#183;</span>
        <span>Three guides</span><span class="dot">&#183;</span>
        <span>Updated 20 November 2026</span>
      </p>
    </div>
    <figure class="hero-figure">
      <img src="{href(0, 'assets/img/hero-counter.jpg')}" alt="Halved potatoes, olive oil, rosemary and sea salt on a wooden board in afternoon light." width="1376" height="768">
      <figcaption>{e(f['hero_caption'])}</figcaption>
    </figure>
  </div>
</section>

<section class="sect-tight">
  <div class="wrap">
    <div class="stat-row">
      <div class="stat"><div class="n">5</div><div class="l">Appliances in the shop</div></div>
      <div class="stat"><div class="n">3</div><div class="l">Live buying guides</div></div>
      <div class="stat"><div class="n">0</div><div class="l">Prices we cannot stand behind</div></div>
      <div class="stat"><div class="n">0</div><div class="l">Trackers on this page</div></div>
    </div>
  </div>
</section>

<section class="sect" id="shop">
  <div class="wrap">
    <div class="sect-head">
      <div>
        <p class="eyebrow">{e(EDIT['sections']['picks_title'])}</p>
        <h2>Five machines, and the question each one answers</h2>
        <p>{e(EDIT['sections']['picks_deck'])}</p>
      </div>
      <a class="btn btn-ghost" href="{href(0, 'table/')}">Table of record</a>
    </div>
    <div class="grid grid-3">{picks}</div>
  </div>
</section>

<section class="sect sect-alt" id="guides">
  <div class="wrap">
    <div class="sect-head">
      <div>
        <p class="eyebrow">Buying guides</p>
        <h2>{e(EDIT['sections']['guides_title'])}</h2>
        <p>{e(EDIT['sections']['guides_deck'])}</p>
      </div>
      <span class="side">One question per guide</span>
    </div>
    <div class="g-list">{guides}</div>
  </div>
</section>

<section class="sect" id="method">
  <div class="wrap">
    <div class="sect-head">
      <div>
        <p class="eyebrow">{e(EDIT['sections']['method_title'])}</p>
        <h2>Four commitments, and what each one costs us</h2>
        <p>{e(EDIT['sections']['method_deck'])}</p>
      </div>
    </div>
    <div class="cmt">{cmts}</div>
  </div>
</section>

<section class="sect sect-alt">
  <div class="wrap">
    <div class="panel panel-tint" style="display:grid;grid-template-columns:1fr auto;gap:28px;align-items:center">
      <div>
        <h3 class="mt0">Something here looks wrong?</h3>
        <p class="mb0" style="max-width:46em">Every figure on this site is traceable to a listing, a policy document or a dated observation. If one is not, that is a defect worth fixing rather than hiding. The Suggestions page is where changes are reviewed before anything ships.</p>
      </div>
      <a class="btn" href="{href(0, 'suggestions/')}">Review suggestions</a>
    </div>
  </div>
</section>
"""

    jsonld = [
        org_jsonld(),
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE,
            "url": BASE,
            "publisher": {"@type": "Organization", "name": SITE},
        },
        {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "Five countertop cooking appliances",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "url": canonical("products/" + p["slug"] + "/"),
                 "name": p["listing_title"]}
                for i, p in enumerate(PRODUCTS["products"])
            ],
        },
    ]
    write("", "index.html", page(
        0, "", "The Pantry Journal — the countertop, decided",
        "Five countertop cooking appliances and three question-shaped buying guides. No prices, ratings or stock figures we cannot stand behind, and an Amazon Associates disclosure above the first link.",
        body, active="shop", jsonld=jsonld))


# --------------------------------------------------------------------------
# shop index + category pages
# --------------------------------------------------------------------------

CATS = [
    {
        "slug": "air-fryers",
        "label": "Air fryers",
        "title": "Air fryers, by shape",
        "deck": "Three machines, two shapes: a drawer you shake and a door you open. The shape decides how you cook more than the badge does.",
        "intro": "An air fryer is a small, fast convection oven. The useful distinction is not brand or wattage — it is whether the food comes out in a basket you can shake or on a tray you slide into a cavity. Every other trade-off follows from that.",
        "products": ["chefman-6-quart-dual-basket", "emeril-lagasse-26qt-french-door", "chefman-turbofry-8-quart"],
        "compare": [
            ["How the food comes out", "A drawer you pull and shake", "A tray you pull from a cavity"],
            ["Two temperatures at once", "Yes, on the dual-basket model", "On separate shelves, where the model allows"],
            ["What needs washing", "Basket and crisper plate, removable", "Cavity walls, shelves, door glass"],
            ["Usual footprint", "Deep, needs clearance in front", "Wide and shallow, needs door swing"],
        ],
        "compare_cols": ["What to compare", "Basket machines", "Oven machines"],
        "guides": ["basket-or-oven-air-fryer", "air-fryer-capacity-checklist"],
    },
    {
        "slug": "thermometers",
        "label": "Thermometers",
        "title": "Thermometers, by job",
        "deck": "One checks the temperature now. One tells you when it will be ready. They answer different questions, and the cheap one is not the lesser one.",
        "intro": "An instant-read answers a safety question: is the middle of this chicken at 165°F. A wireless leave-in answers a timing question: when will it be. Most kitchens only need the first, and the second is a convenience rather than a requirement.",
        "products": ["thermomaven-instant-read-thermometer", "chef-iq-sense-wireless-thermometer"],
        "compare": [
            ["What it answers", "What is the temperature right now", "When will it reach temperature"],
            ["Where you are while it reads", "Standing at the cooker", "Anywhere the signal reaches"],
            ["Official guidance it serves", "USDA safe minimum internal temperatures", "The same temperatures, watched over time"],
            ["What can go wrong", "A probe that reads a few degrees off", "A lost connection and no display"],
        ],
        "compare_cols": ["What to compare", "Instant-read", "Wireless leave-in"],
        "guides": ["the-dial-is-not-the-temperature"],
        "extra_source": ("https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart",
                         "USDA FSIS — Safe Minimum Internal Temperature Chart"),
    },
]


def build_products_index():
    cards = "".join(product_card(p, 1, "shop-grid") for p in PRODUCTS["products"])
    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{href(1, '')}">Home</a><span>&#8250;</span><span>Shop</span></nav>
  <section style="padding:26px 0 34px;max-width:44em">
    <p class="kicker">The shop</p>
    <h1>Five machines</h1>
    <p class="deck">Three air fryers in two shapes, and two thermometers that answer different questions. Each page says what the listing claims, what we could not confirm, and what to check before you buy.</p>
    <p class="lede-sm">There is no price, star rating or stock figure on any of these cards. That is a rule, not an oversight: Amazon permits a site to show that data only where Amazon serves it, and no such feed is connected here. The listing will show you the current numbers.</p>
  </section>
  <div class="grid grid-3" style="padding-bottom:20px">{cards}</div>

  <section style="padding:46px 0 70px">
    <div class="panel">
      <h3 class="mt0">How the buy links work</h3>
      <p style="max-width:48em">Every arrow button goes to a direct <span class="mono">amazon.com/dp/</span> address carrying the Associates tag <span class="mono">{TAG}</span> as a URL parameter, with <span class="mono">rel="sponsored nofollow noopener"</span>. The five short links supplied to this project are listed on each product page for transparency, but the shop does not route you through them: their tracking behaviour is unconfirmed and their compliance status is unresolved. That is recorded on the <a href="{href(1, 'flagged/')}">Flagged for review</a> page rather than asserted here.</p>
    </div>
  </section>
</div>
"""
    write("products", "index.html", page(
        1, "products/", "Shop all five appliances — The Pantry Journal",
        "Three air fryers in two shapes and two thermometers, with what each listing claims, what is unverified, and what to check before buying.",
        body, active="shop",
        jsonld=[org_jsonld(), crumbs_jsonld(1, [("Home", ""), ("Shop", "products/")])]))


def build_category(cat):
    depth = 1
    prods = [P[s] for s in cat["products"]]
    cards = "".join(product_card(p, 1, "cat-" + cat["slug"]) for p in prods)
    cmp_rows = [[row[0], e(row[1]), e(row[2])] for row in cat["compare"]]
    compare = data_table(f"{cat['label']}, compared by shape", cat["compare_cols"], cmp_rows)
    compare = compare.replace('<div class="t-wrap"><table>', '<div class="t-wrap"><table data-compare="' + cat["slug"] + '">')
    guides = related_block(cat["guides"], 1, "Guide")
    src = ""
    if cat.get("extra_source"):
        url, label = cat["extra_source"]
        src = f'<p class="src" style="margin-top:20px">Official source used on this page: <a href="{e(url)}" rel="noopener">{e(label)}</a></p>'
    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{href(1, '')}">Home</a><span>&#8250;</span><a href="{href(1, 'categories/')}">Categories</a><span>&#8250;</span><span>{e(cat['label'])}</span></nav>
  <section style="padding:26px 0 10px;max-width:44em">
    <p class="kicker">{e(cat['label'])}</p>
    <h1>{e(cat['title'])}</h1>
    <p class="deck">{e(cat['deck'])}</p>
    <p class="lede-sm">{e(cat['intro'])}</p>
  </section>
  <div class="grid grid-3" style="padding:24px 0 8px">{cards}</div>
  <section style="padding:44px 0 0">
    <div class="sect-head" style="margin-bottom:18px"><div><p class="eyebrow">Side by side</p><h2 style="font-size:1.5rem">The comparison that changes the answer</h2></div></div>
    {compare}
    {src}
  </section>
  <section style="padding:44px 0 70px">
    <div class="sect-head" style="margin-bottom:18px"><div><p class="eyebrow">Read first</p><h2 style="font-size:1.5rem">The guides behind this page</h2></div></div>
    {guides}
  </section>
</div>
"""
    write("categories", cat["slug"] + ".html", page(
        1, f"categories/{cat['slug']}.html",
        f"{cat['title']} — The Pantry Journal", cat["deck"], body, active="categories",
        jsonld=[org_jsonld(), crumbs_jsonld(1, [("Home", ""), ("Categories", "categories/"), (cat["label"], None)])]))


def build_categories_index():
    cards = []
    for cat in CATS:
        n = len(cat["products"])
        cards.append(f"""<article class="p-card">
  <div class="p-body">
    <p class="p-brand">{n} machine{'s' if n != 1 else ''}</p>
    <h3><a href="{href(1, 'categories/' + cat['slug'] + '.html')}">{e(cat['label'])}</a></h3>
    <p class="desc">{e(cat['deck'])}</p>
    <a class="btn btn-ghost" href="{href(1, 'categories/' + cat['slug'] + '.html')}">Browse {e(cat['label'].lower())}</a>
  </div>
</article>""")
    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{href(1, '')}">Home</a><span>&#8250;</span><span>Categories</span></nav>
  <section style="padding:26px 0 30px;max-width:44em">
    <p class="kicker">Two categories</p>
    <h1>Shop by what you are deciding</h1>
    <p class="deck">Two categories, because the shop sells two jobs: cooking without oil, and knowing when food is done. Within each, the page organises by the distinction that actually changes the purchase.</p>
  </section>
  <div class="grid grid-2" style="padding-bottom:26px">{''.join(cards)}</div>
  <section style="padding:20px 0 70px">
    <div class="panel panel-warn">
      <h3 class="mt0">Why only two</h3>
      <p class="mb0" style="max-width:48em">A shop that lists forty categories is a directory. Five machines sit behind these two headings, and each has its own page stating what the listing claims and what remains unverified. If the shop grows, categories arrive when there is a decision to hang on them — not before.</p>
    </div>
  </section>
</div>
"""
    write("categories", "index.html", page(
        1, "categories/", "Categories — The Pantry Journal",
        "Air fryers by shape and thermometers by job: the two distinctions that decide which countertop appliance is right for your kitchen.",
        body, active="categories",
        jsonld=[org_jsonld(), crumbs_jsonld(1, [("Home", ""), ("Categories", "categories/")])]))


# --------------------------------------------------------------------------
# product pages
# --------------------------------------------------------------------------

def build_product(p):
    depth = 2
    cat = next(c for c in CATS if c["slug"] == p["category"])
    claims_rows = [[e(c["text"]), f'<span class="src">{e(c["kind"])}</span>'] for c in p["claims"]]
    claims = data_table("What the listing says", ["Claim, in the seller's words", "How to read it"], claims_rows)

    verify_rows = [[f"<code>{e(x)}</code>", '<span class="blank">not published</span>'] for x in p["not_verified"]]
    verify = data_table("Not published here, and why", ["Field", "Status"], verify_rows)

    facts = f"""<ul class="fact-list">
  <li><span class="k">Brand</span><span class="v">{e(p['brand'])}</span></li>
  <li><span class="k">Type</span><span class="v">{e(p['type_label'])}</span></li>
  <li><span class="k">ASIN</span><span class="v mono">{e(p['asin'])}</span></li>
  <li><span class="k">Category</span><span class="v">{e(p['category_path'].split(' > ')[-1])}</span></li>
  <li><span class="k">Observed</span><span class="v">20 Nov 2026</span></li>
</ul>"""

    read_next = related_block(p["read_next"], depth, "Guide")

    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{href(depth, '')}">Home</a><span>&#8250;</span><a href="{href(depth, 'products/')}">Shop</a><span>&#8250;</span><a href="{href(depth, 'categories/' + cat['slug'] + '.html')}">{e(cat['label'])}</a><span>&#8250;</span><span>{e(p['short_name'])}</span></nav>

  <div class="pd-grid">
    <div>
      <div class="pd-head">
        <p class="kicker">{e(cat['label'])} &#183; {e(p['type_label'])}</p>
        <h1>{e(p['display_title'])}</h1>
        <p class="deck">{e(p['deck'])}</p>
      </div>

      <figure class="pd-fig">
        <img src="{href(depth, 'assets/img/' + p['image'])}" alt="{e(p['image_alt'])}" width="1408" height="768">
        <figcaption>Illustration, not the product. This is the food, not the machine &#8212; the shop publishes no Amazon product photography and will not pass a stock image off as the appliance.</figcaption>
      </figure>

      <div class="panel" style="border-left:3px solid var(--accent);margin-bottom:30px">
        <p class="eyebrow" style="margin-bottom:8px">The quick take</p>
        <p class="mb0" style="font-size:1.02rem">{e(p['quick_take'])}</p>
      </div>

      <h2 style="font-size:1.5rem">Who this shape suits</h2>
      <ul class="checklist">{''.join(f'<li>{e(s)}</li>' for s in p['suits_if'])}</ul>

      <h2 style="font-size:1.5rem;margin-top:36px">Check these before you buy</h2>
      <ul class="checklist">{''.join(f'<li>{e(s)}</li>' for s in p['check_before_buying'])}</ul>

      <h2 style="font-size:1.5rem;margin-top:38px">What the listing claims</h2>
      <p class="lede-sm">Everything below is the seller's own language from the listing title, reproduced and labelled. None of it has been independently measured or tested by this site.</p>
      {claims}

      <h2 style="font-size:1.5rem;margin-top:38px">What is deliberately blank</h2>
      <p class="lede-sm">Amazon's Associates Program Policies allow a site to show price and availability only where Amazon serves that data through the link, or where it comes from the Creators API or PA API. No feed is connected, so the fields below are empty on purpose. A stale number would be worse than no number.</p>
      {verify}
      <p class="src" style="margin-top:14px">Policy source: <a href="https://affiliate-program.amazon.com/help/operating/policies" rel="noopener">Associates Program Policies, section 2(b)</a>, read 20 November 2026.</p>

      <h2 style="font-size:1.5rem;margin-top:38px">The record for this product</h2>
      {data_table("Input, observation and status", ["Field", "Value"], [[
          '<span class="src">Submitted short link</span>',
          f'<span class="mono">{e(p["submitted_link"])}</span>'
      ], [
          '<span class="src">Submitted code (9 characters)</span>',
          f'<code>{e(p["submitted_code"])}</code>'
      ], [
          '<span class="src">Observed ASIN (10 characters)</span>',
          f'<code>{e(p["asin"])}</code>'
      ], [
          '<span class="src">Observed destination</span>',
          f'<a href="{e(p["affiliate_url"])}" rel="sponsored nofollow noopener" target="_blank" class="mono">{e(p["listing_url"])}</a>'
      ], [
          '<span class="src">Listing title, as returned</span>',
          e(p["listing_title"])
      ], [
          '<span class="src">Breadcrumb, as returned</span>',
          e(p["category_path"])
      ], [
          '<span class="src">Observation</span>',
          f'{e(p["observed_at_utc"])} &#183; product page returned'
      ], [
          '<span class="src">Tracking confirmed in Associates report</span>',
          '<span class="blank">not confirmed</span>'
      ], [
          '<span class="src">Intended ASIN from the account holder</span>',
          '<span class="blank">not supplied</span>'
      ]])}
      <p class="src" style="margin-top:12px">The submitted code and the observed ASIN are different values and are kept in separate fields on purpose. The first is what was supplied; the second is what the destination page returned. Merging them would hide a mismatch rather than document it.</p>

      <h2 style="font-size:1.5rem;margin-top:38px">Read next</h2>
      {read_next}
    </div>

    <aside class="pd-aside">
      <div class="panel">
        <p class="eyebrow" style="margin-bottom:10px">Where to buy</p>
        {amazon_link(p, 'See this on Amazon', depth, 'product-side', arrow=True)}
        <p class="buy-note">Affiliate link. {DISCLOSURE} Price, stock and delivery are shown by Amazon on the listing. Nothing about them is stated here.</p>
        <div class="sep" style="margin:16px 0"></div>
        <p class="eyebrow" style="margin-bottom:10px">At a glance</p>
        {facts}
      </div>
      <div class="panel panel-warn">
        <p class="eyebrow" style="margin-bottom:8px">Unverified</p>
        <p class="mb0" style="font-size:.88rem">Not published because they cannot be sourced: <strong>{e(', '.join(p['not_verified'][:6]))}</strong>{' and more' if len(p['not_verified']) > 6 else ''}. The full list is under &#8220;What is deliberately blank&#8221;. The <a href="{href(depth, 'flagged/')}">Flagged for review</a> page explains each gap.</p>
      </div>
      <div class="panel">
        <p class="eyebrow" style="margin-bottom:8px">The short link supplied</p>
        <p class="mono" style="font-size:.78rem;word-break:break-all;margin-bottom:8px">{e(p['submitted_link'])}</p>
        <p class="mb0" style="font-size:.82rem;color:var(--ink-2)">Listed for transparency. The buy button above does not route through it: the short link&#8217;s tracking behaviour is unconfirmed and its compliance status is unresolved. <a href="{href(depth, 'flagged/')}">Why</a>.</p>
      </div>
    </aside>
  </div>
</div>
<div style="height:56px"></div>
"""

    jsonld = [
        org_jsonld(),
        crumbs_jsonld(depth, [("Home", ""), ("Shop", "products/"), (cat["label"], "categories/" + cat["slug"] + ".html"), (p["short_name"], None)]),
        {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": p["listing_title"],
            "sku": p["asin"],
            "brand": {"@type": "Brand", "name": p["brand"]},
            "category": p["category_path"],
            "url": canonical("products/" + p["slug"] + "/"),
            "description": p["deck"],
            # Deliberately no offers and no aggregateRating: the shop publishes
            # neither a price nor a rating, so marking either up would be a lie.
        },
    ]
    write("products/" + p["slug"], "index.html", page(
        depth, f"products/{p['slug']}/",
        f"{p['display_title']} — The Pantry Journal",
        p["deck"], body, active="shop", og_image=p["image"], og_type="article", jsonld=jsonld))


# --------------------------------------------------------------------------
# guides
# --------------------------------------------------------------------------

def build_guides_index():
    rows = "".join(guide_row(g, 1, i + 1) for i, g in enumerate(GUIDES["guides"]))
    cal_rows = [[e(c["slot"]), e(G[c["guide"]]["short_title"]), pill("ok", "published") if c["status"] == "published" else pill("quiet", "scheduled")] for c in GUIDES["meta"]["editorial_calendar"]]
    cal = data_table("The publishing calendar", ["Slot", "Guide", "Status"], cal_rows)
    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{href(1, '')}">Home</a><span>&#8250;</span><span>Guides</span></nav>
  <section style="padding:26px 0 10px;max-width:44em">
    <p class="kicker">Buying guides</p>
    <h1>Three questions, answered honestly</h1>
    <p class="deck">Each guide is built around one question a buyer actually asks. None of them claims to know which machine is best, because nobody here has tested one.</p>
  </section>
  <div class="g-list" style="margin-top:22px">{rows}</div>
  <section style="padding:44px 0 70px">
    <h2 style="font-size:1.5rem">What comes next, and when</h2>
    <p class="lede-sm">A publication keeps a schedule. Two guides are queued; both are published as drafts that state their question and what is missing, rather than padded out to look finished. <strong>{e(GUIDES['meta']['note'])}</strong></p>
    {cal}
    <p class="src" style="margin-top:14px">{e(GUIDES['meta']['next_topics_found_where'])}</p>
  </section>
</div>
"""
    write("guides", "index.html", page(
        1, "guides/", "Buying guides — The Pantry Journal",
        "Three question-shaped buying guides for air fryers and thermometers, plus the publishing calendar for what comes next.",
        body, active="guides",
        jsonld=[org_jsonld(), crumbs_jsonld(1, [("Home", ""), ("Guides", "guides/")])]))


def build_guide(g):
    depth = 2
    parts = []
    toc = []
    n = 0
    for s in g["sections"]:
        n += 1
        anchor = "s" + str(n)
        toc.append(f'<a href="#{anchor}">{e(s["h"])}</a>')
        chunk = [f'<h2 id="{anchor}">{e(s["h"])}</h2>']
        for para in s.get("paras", []):
            chunk.append(f"<p>{e(para)}</p>")
        if s.get("list"):
            chunk.append(bullets(s["list"]))
        if s.get("table"):
            t = s["table"]
            rows = [[e(c) for c in r] for r in t["rows"]]
            chunk.append(data_table(e(t["caption"]), [e(c) for c in t["cols"]], rows))
        parts.append("\n".join(chunk))
    body_sections = "\n".join(parts)

    faq_html = ""
    faq_jsonld = None
    if g["faq"]:
        items = "".join(
            f'<div class="panel" style="margin-bottom:12px"><h3 class="mt0" style="font-size:1.05rem">{e(f["q"])}</h3><p class="mb0">{e(f["a"])}</p></div>'
            for f in g["faq"]
        )
        faq_html = f'<h2 style="font-size:1.5rem;margin-top:44px">Questions people ask</h2>{items}'
        faq_jsonld = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": f["q"],
                            "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in g["faq"]],
        }

    src_html = ""
    if g["sources"]:
        links = "".join(f'<li><a href="{e(u)}" rel="noopener">{e(u)}</a></li>' for u in g["sources"])
        src_html = f'<h2 style="font-size:1.3rem;margin-top:36px">Sources on this page</h2><ul class="src" style="font-size:.84rem">{links}</ul>'

    prods = [P[s] for s in g["products"] if s in P]
    prod_html = ""
    if prods:
        cards = "".join(product_card(p, depth, "guide-" + g["slug"]) for p in prods)
        prod_html = f"""
<section class="sect sect-alt" style="margin-top:56px">
  <div class="wrap">
    <div class="sect-head" style="margin-bottom:24px"><div><p class="eyebrow">In the shop</p><h2 style="font-size:1.5rem">The machines this guide is talking about</h2></div><a class="btn btn-ghost" href="{href(depth, 'products/')}">All five</a></div>
    <div class="grid grid-3">{cards}</div>
  </div>
</section>"""

    state_note = ""
    if g["status"] != "published":
        state_note = f"""<div class="panel panel-warn" style="margin-bottom:28px">
      <p class="eyebrow" style="margin-bottom:8px">Draft</p>
      <p class="mb0">This guide is scheduled but not finished. What follows is the question it will answer and an honest note on what is missing. Publishing a page of filler would be worse than publishing a promise, so this is the promise. It is excluded from the sitemap and the feed until it is complete.</p>
    </div>"""

    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{href(depth, '')}">Home</a><span>&#8250;</span><a href="{href(depth, 'guides/')}">Guides</a><span>&#8250;</span><span>{e(g['short_title'])}</span></nav>
  <article class="prose" style="padding:26px 0 0" data-guide="{e(g['slug'])}">
    <p class="kicker">{e(g['kicker'])}</p>
    <h1>{e(g['title'])}</h1>
    <p class="deck">{e(g['deck'])}</p>
    <p class="byline" style="margin-bottom:26px">
      <span>Updated 20 November 2026</span><span class="dot">&#183;</span><span>{e(g['read_time'])}</span><span class="dot">&#183;</span><span>The Pantry Journal</span>
    </p>
    {state_note}
    <div class="toc">{''.join(toc)}</div>
    {body_sections}
    {faq_html}
    {src_html}
    <div class="panel panel-tint" style="margin-top:36px">
      <h3 class="mt0" style="font-size:1.02rem">What this guide will not do</h3>
      <p class="mb0" style="font-size:.92rem">It will not tell you which machine is best. Nobody here has tested one, and the FTC's guidance is clear that an endorsement has to reflect an honest experience. What the guide does is narrow the field using the questions a listing will not answer for you.</p>
    </div>
  </article>
</div>
{prod_html}
<div style="height:40px"></div>
"""

    jsonld = [
        org_jsonld(),
        crumbs_jsonld(depth, [("Home", ""), ("Guides", "guides/"), (g["short_title"], None)]),
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": g["title"],
            "description": g["deck"],
            "datePublished": "2026-11-20",
            "dateModified": g["updated"],
            "author": {"@type": "Organization", "name": SITE},
            "publisher": {"@type": "Organization", "name": SITE},
            "mainEntityOfPage": canonical("guides/" + g["slug"] + "/"),
        },
    ]
    if faq_jsonld:
        jsonld.append(faq_jsonld)
    write("guides/" + g["slug"], "index.html", page(
        depth, f"guides/{g['slug']}/",
        f"{g['title']} — The Pantry Journal", g["deck"], body, active="guides",
        og_type="article", jsonld=jsonld, noindex=True))


# --------------------------------------------------------------------------
# table of record
# --------------------------------------------------------------------------

def build_table():
    depth = 1
    rows = []
    for p in PRODUCTS["products"]:
        rows.append([
            f'<strong>{e(p["id"])}</strong>',
            f'<a href="{href(depth, "products/" + p["slug"] + "/")}">{e(p["brand"])} {e(p["short_name"])}</a>',
            f'<span class="mono">{e(p["submitted_code"])}</span><br><span class="src">9 characters</span>',
            f'<code>{e(p["asin"])}</code><br><span class="src">10 characters</span>',
            f'<span class="mono">/dp/{e(p["asin"])}</span>',
            e(p["observed_at_utc"]),
            '<span class="blank">not published</span>',
            '<span class="blank">not confirmed</span>',
            pill("ok", "observed"),
        ])
    table = data_table(
        "Five supplied links, resolved 20 November 2026",
        ["ID", "Product", "Submitted code", "Observed ASIN", "Observed listing", "Observed at (UTC)", "Price / rating", "Tracking confirmed", "Status"],
        rows)

    obs_rows = []
    for o in REGISTER["observations"]:
        obs_rows.append([
            f'<code>{e(o["id"])}</code>',
            f'<span class="mono">{e(o["submitted_code"])}</span>',
            f'<span class="mono">{e(o["observed_asin"])}</span>',
            e(o["outcome"]),
            e(o["breadcrumb"]),
            pill("ok", "agrees") if o["agrees_with_prior_records"] else pill("flag", "differs"),
        ])
    obs = data_table("Observation log", ["Ref", "Submitted", "Observed ASIN", "Outcome", "Breadcrumb as returned", "Earlier records"], obs_rows)

    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{href(1, '')}">Home</a><span>&#8250;</span><span>Table of record</span></nav>
  <section style="padding:26px 0 8px;max-width:46em">
    <p class="kicker">The record</p>
    <h1>Every value, and where it came from</h1>
    <p class="deck">This is the audit surface behind the shop. It exists so that a reader who wants to check the shop&#8217;s work can, without the shop pretending to be a spreadsheet on its front page.</p>
    <p class="lede-sm">All five rows were observed on 20 November 2026 by fetching each supplied link and reading the page that returned. Blank cells are unverified, not invalid. Nothing on this page is inferred, estimated or filled in from memory.</p>
  </section>

  <section style="padding:18px 0 0">{table}
    <p class="src" style="margin-top:14px">Source for the ASIN definition: <a href="https://sell.amazon.com/blog/what-is-an-asin" rel="noopener">Amazon, Understanding ASINs</a> (Jun 4, 2025) &#8212; &#8220;a unique 10-character alphanumeric code&#8221;. Source for the price rule: <a href="https://affiliate-program.amazon.com/help/operating/policies" rel="noopener">Associates Program Policies, section 2(b)</a>.</p>
  </section>

  <section style="padding:36px 0 0">
    <h2 style="font-size:1.5rem">The observation log</h2>
    <p class="lede-sm">What was requested, what came back, and whether that agrees with what earlier records said. Three links disagree with an earlier record; the disagreement is shown rather than smoothed over.</p>
    {obs}
  </section>

  <section style="padding:36px 0 70px">
    <h2 style="font-size:1.5rem">Method, in full</h2>
    <div class="panel">
      <p><strong>What was done.</strong> {e(REGISTER['meta']['method'])}</p>
      <p><strong>What limits it.</strong></p>
      <ul class="mb0">{''.join(f'<li>{e(l)}</li>' for l in REGISTER['meta']['limitations'])}</ul>
    </div>
    <p class="src" style="margin-top:16px">Full source list with quotations: <a href="{href(depth, 'sources/')}">Sources &amp; compliance</a>. Every unresolved item: <a href="{href(depth, 'flagged/')}">Flagged for review</a>.</p>
  </section>
</div>
"""
    write("table", "index.html", page(
        1, "table/", "Table of record — The Pantry Journal",
        "All five supplied links, the ASINs they resolved to, the date observed, and the fields deliberately left blank.",
        body, active=None,
        jsonld=[org_jsonld(), crumbs_jsonld(1, [("Home", ""), ("Table of record", "table/")])]))


# --------------------------------------------------------------------------
# flagged
# --------------------------------------------------------------------------

SEV_PILL = {"high": "stop", "medium": "open", "low": "quiet"}


def build_flagged():
    depth = 1
    blocks = []
    for f in REGISTER["flags"]:
        src = f'<p class="src">Check it: <a href="{e(f["source"])}" rel="noopener">{e(f["source"])}</a></p>' if f["source"] else '<p class="src">No external source: this is an observation about this repository.</p>'
        blocks.append(f"""<div class="flag {e(f['severity'])}">
  <h3>{pill(SEV_PILL[f['severity']], f['severity'])} {e(f['title'])} <span class="fid">{e(f['id'])}</span></h3>
  <p>{e(f['detail'])}</p>
  <div class="act"><strong>What you would do:</strong> {e(f['review_action'])}</div>
  {src}
</div>""")
    counts = {s: sum(1 for f in REGISTER["flags"] if f["severity"] == s) for s in ("high", "medium", "low")}
    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{href(1, '')}">Home</a><span>&#8250;</span><span>Flagged for review</span></nav>
  <section style="padding:26px 0 8px;max-width:46em">
    <p class="kicker">Flagged for review</p>
    <h1>What is unverified, and what it would take to settle it</h1>
    <p class="deck">Nothing on this page blocks the site from being live. That is the point of publishing it: a shop that hides its gaps has gaps you cannot see. Each item states what was seen, what could not be confirmed, and the one action that would close it.</p>
  </section>
  <div class="stat-row" style="margin:24px 0 30px">
    <div class="stat"><div class="n">{counts['high']}</div><div class="l">High &#183; affects earning or could mislead</div></div>
    <div class="stat"><div class="n">{counts['medium']}</div><div class="l">Medium &#183; limits a decision</div></div>
    <div class="stat"><div class="n">{counts['low']}</div><div class="l">Low &#183; procedural or cosmetic</div></div>
    <div class="stat"><div class="n">{sum(counts.values())}</div><div class="l">Total open items</div></div>
  </div>
  {''.join(blocks)}
  <div class="panel panel-tint" style="margin:28px 0 70px">
    <h3 class="mt0">Two older sections of this repository still exist</h3>
    <p class="mb0">Before this shop, this repository published two other sites from the same address. They are preserved rather than deleted, because they were built by other sessions working from the same brief. They are listed on the <a href="{href(depth, 'sitemap/')}">Site map</a>. Whether to retire them is your call, logged as SUG-16 on the <a href="{href(depth, 'suggestions/')}">Suggestions</a> page.</p>
  </div>
</div>
"""
    write("flagged", "index.html", page(
        1, "flagged/", "Flagged for review — The Pantry Journal",
        "Every unverified value and unresolved question on this site, with the source for each and the action that would settle it.",
        body, active=None,
        jsonld=[org_jsonld(), crumbs_jsonld(1, [("Home", ""), ("Flagged for review", "flagged/")])]))


# --------------------------------------------------------------------------
# questions / decisions
# --------------------------------------------------------------------------

STATE_LABEL = {
    "answered": ("ok", "Answered"),
    "open-doable": ("open", "Open &#183; we can close it"),
    "account-holder": ("flag", "Needs account access"),
    "blocked": ("stop", "Blocked"),
}


def build_questions():
    depth = 1
    groups = [
        ("Answered, with a source", ["answered"]),
        ("Open, and closable from here", ["open-doable"]),
        ("Only the account holder can answer", ["account-holder"]),
        ("Blocked with current access", ["blocked"]),
    ]
    sections = []
    for heading, states in groups:
        qs = [q for q in QUESTIONS["questions"] if q["state"] in states]
        if not qs:
            continue
        rows = []
        for q in qs:
            kind, label = STATE_LABEL[q["state"]]
            src = source_link(q["source"], e(q["source_label"])) if q["source"] else '<span class="src">local check, reproducible</span>'
            how = f'<br><span class="src">To close it: {e(q["how_to_answer"])}</span>' if q.get("how_to_answer") else ""
            rows.append([
                f'<code>{e(q["id"])}</code><br>{pill(kind, label)}',
                f'<strong>{e(q["question"])}</strong>',
                e(q["answer"]) + how,
                src,
            ])
        sections.append(f'<h2 style="font-size:1.5rem;margin-top:38px">{heading}</h2>' +
                        data_table(None, ["Ref", "Question", "Answer, or why there is none", "Where it comes from"], rows))

    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{href(1, '')}">Home</a><span>&#8250;</span><span>Decisions &amp; open questions</span></nav>
  <section style="padding:26px 0 8px;max-width:46em">
    <p class="kicker">Before any decision</p>
    <h1>The questions that come before a choice</h1>
    <p class="deck">Sixteen questions, split by what it would take to answer them. A decision made without the ones in the lower two groups is a decision made on a guess, and the shop would rather show you where the guess is.</p>
    <p class="lede-sm">Nothing on this page is a recommendation. The first group is settled and sourced; the second is work this project can do; the third needs you in the Associates dashboard; the fourth cannot be answered with the access this project has at all.</p>
  </section>
  {''.join(sections)}
  <section style="padding:40px 0 70px">
    <div class="panel panel-warn">
      <h3 class="mt0">The one question that unlocks the rest</h3>
      <p class="mb0">Does a click on a tagged link appear in the tracking report? Until that is answered once, nothing else about earning can be measured. It takes one click, signed in, and it is <a href="{href(depth, 'suggestions/')}#SUG-21">SUG-21</a>.</p>
    </div>
  </section>
</div>
"""
    write("questions", "index.html", page(
        1, "questions/", "Decisions and open questions — The Pantry Journal",
        "The questions that have to be answered before a decision is reasonable, split into answered, open, account-only and blocked.",
        body, active=None,
        jsonld=[org_jsonld(), crumbs_jsonld(1, [("Home", ""), ("Decisions", "questions/")])]))


# --------------------------------------------------------------------------
# suggestions
# --------------------------------------------------------------------------

STATUS_PILL = {
    "shipped": ("ok", "Shipped"),
    "proposed": ("open", "Proposed"),
    "needs-your-decision": ("flag", "Needs your decision"),
    "blocked-on-account": ("stop", "Blocked on account"),
    "blocked-on-testing": ("stop", "Blocked on testing"),
    "rejected": ("quiet", "Rejected"),
}


def build_suggestions():
    depth = 1
    shortlist = "".join(
        f'<li><strong>#{r["rank"]}</strong> &#183; <a href="#{e(r["id"])}">{e(r["id"])}</a> &#8212; {e(r["why"])}</li>'
        for r in SUGGESTIONS["shortlist"]
    )

    cards = []
    for s in SUGGESTIONS["suggestions"]:
        kind, label = STATUS_PILL[s["status"]]
        opts = ""
        if s.get("options"):
            opts = '<ul class="mb0" style="margin-top:8px;font-size:.9rem">' + "".join(f"<li>{e(o)}</li>" for o in s["options"]) + "</ul>"
        blocked = f'<p class="src" style="margin-top:8px">Blocked by: {e(s["blocked_by"])}</p>' if s.get("blocked_by") else ""
        evidence = f'<p class="src" style="margin-top:8px">Evidence needed: {e(s["evidence_needed"])}</p>' if s.get("evidence_needed") else ""
        note = f'<p class="src" style="margin-top:8px">{e(s["note"])}</p>' if s.get("note") else ""
        shipped = f'<p class="src" style="margin-top:8px"><strong>Done:</strong> {e(s["shipped_note"])}</p>' if s.get("shipped_note") else ""
        cards.append(f"""<div class="flag" id="{e(s['id'])}" data-status="{e(s['status'])}" style="border-left-color:{'#55634a' if s['status'] == 'shipped' else '#c08a2a' if s['status'] != 'rejected' else '#b9b2a6'}">
  <h3>{pill(kind, label.replace('&#183;', '&#183;'))} {e(s['title'])} <span class="fid">{e(s['id'])}</span></h3>
  <div class="tag-row" style="margin:8px 0 12px">
    <span class="pill pill-quiet">Impact {s['impact']}/5</span>
    <span class="pill pill-quiet">Effort {s['effort']}/5</span>
    <span class="pill pill-quiet">Confidence: {e(s['confidence'].split(';')[0].split('—')[0].strip())}</span>
  </div>
  <p>{e(s['why'])}</p>
  {shipped}{evidence}{opts}{blocked}{note}
</div>""")

    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{href(1, '')}">Home</a><span>&#8250;</span><span>Suggestions</span></nav>
  <section style="padding:26px 0 8px;max-width:46em">
    <p class="kicker">Review queue</p>
    <h1>Every change, before it ships</h1>
    <p class="deck">This is the page you asked for: a list you can review and choose from before anything is implemented. Each entry says what it would change, why, what it costs, and what would have to be true before it is safe.</p>
    <p class="lede-sm">{e(SUGGESTIONS['meta']['how_to_use'])}</p>
  </section>

  <div class="panel" style="margin:22px 0 30px">
    <p class="eyebrow" style="margin-bottom:10px">If you only read five</p>
    <ol class="mb0">{shortlist}</ol>
  </div>

  <div class="filters" role="group" aria-label="Filter suggestions">
    <button type="button" data-f="all" aria-pressed="true">All <span class="count">{len(SUGGESTIONS['suggestions'])}</span></button>
    <button type="button" data-f="needs-your-decision" aria-pressed="false">Needs your decision <span class="count">{sum(1 for s in SUGGESTIONS['suggestions'] if s['status'] == 'needs-your-decision')}</span></button>
    <button type="button" data-f="blocked" aria-pressed="false">Blocked <span class="count">{sum(1 for s in SUGGESTIONS['suggestions'] if s['status'].startswith('blocked'))}</span></button>
    <button type="button" data-f="proposed" aria-pressed="false">Proposed <span class="count">{sum(1 for s in SUGGESTIONS['suggestions'] if s['status'] == 'proposed')}</span></button>
    <button type="button" data-f="shipped" aria-pressed="false">Shipped <span class="count">{sum(1 for s in SUGGESTIONS['suggestions'] if s['status'] == 'shipped')}</span></button>
    <button type="button" data-f="rejected" aria-pressed="false">Rejected <span class="count">{sum(1 for s in SUGGESTIONS['suggestions'] if s['status'] == 'rejected')}</span></button>
  </div>

  {''.join(cards)}
  <div class="panel panel-tint" style="margin:28px 0 70px">
    <h3 class="mt0">How to choose</h3>
    <p class="mb0">Pick by the thing that is currently costing you money or credibility, not by the size of the idea. Right now that is SUG-21: if a click is never attributed, every other improvement is a nicer way to earn nothing. The five selected above are ranked on that basis, and the ranking is an opinion rather than a measurement.</p>
  </div>
</div>
<script>
(function(){{
  var btns = document.querySelectorAll('.filters button');
  var cards = document.querySelectorAll('[data-status]');
  btns.forEach(function(b){{
    b.addEventListener('click', function(){{
      var f = b.getAttribute('data-f');
      btns.forEach(function(x){{ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }});
      cards.forEach(function(c){{
        var st = c.getAttribute('data-status');
        var show = f === 'all' || st === f || (f === 'blocked' && st.indexOf('blocked') === 0);
        c.setAttribute('data-filtered', show ? 'false' : 'true');
      }});
    }});
  }});
}})();
</script>
"""
    write("suggestions", "index.html", page(
        1, "suggestions/", "Suggestions for review — The Pantry Journal",
        "A review queue of proposed changes, each with impact, effort, evidence needed and what would have to be true before it ships.",
        body, active="suggestions",
        jsonld=[org_jsonld(), crumbs_jsonld(1, [("Home", ""), ("Suggestions", "suggestions/")])]))


# --------------------------------------------------------------------------
# sources & compliance
# --------------------------------------------------------------------------

def build_sources():
    depth = 1
    rows = []
    for s in REGISTER["sources"]:
        rows.append([
            f'<code>{e(s["id"])}</code>',
            f'{e(s["publisher"])}<br><span class="src">{e(s["title"])}</span>',
            source_link(s["url"], f'<span class="mono" style="word-break:break-all">{e(s["url"])}</span>'),
            e(s["dated"]) if s["dated"] else '<span class="blank">undated</span>',
            f'<span class="src">{e(s["quote"])}</span>',
            f'<span class="src">{e(s["used_for"])}</span>',
        ])
    table = data_table("Every source, what it says, and what it is used for",
                       ["Ref", "Publisher and title", "URL", "Dated", "Quoted wording", "Used for"], rows)

    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{href(1, '')}">Home</a><span>&#8250;</span><span>Sources &amp; compliance</span></nav>
  <section style="padding:26px 0 8px;max-width:46em">
    <p class="kicker">Sources</p>
    <h1>Where every statement comes from</h1>
    <p class="deck">Twelve sources, quoted rather than paraphrased, each read on 20 November 2026. Two authorities govern this shop and neither substitutes for the other: Amazon decides whether a link earns, and the FTC decides whether a reader understands what the link is.</p>
    <p class="lede-sm">Quotations are reproduced as published. Where a page carries an update date, it is recorded, because a policy that changes silently is a policy you cannot rely on.</p>
  </section>
  <section style="padding:18px 0 0">{table}</section>

  <section style="padding:40px 0 0">
    <h2 style="font-size:1.5rem">The compliance position, in eight lines</h2>
    <div class="prose" style="max-width:none">
      <ol>
        <li><strong>The required sentence is on every page, above the first link.</strong> The Agreement&#8217;s wording is reproduced exactly, and the checker fails the build if it moves below an outbound link.</li>
        <li><strong>Every outbound Amazon link carries the tag as a URL parameter.</strong> Direct <span class="mono">/dp/</span> addresses with <span class="mono">?tag={TAG}</span>, which is what section 2(b) asks for in plain words.</li>
        <li><strong>Every outbound Amazon link is marked sponsored.</strong> <span class="mono">rel="sponsored nofollow noopener"</span>, per Google&#8217;s guidance on paid placements.</li>
        <li><strong>No price, stock, star rating or review count is published.</strong> No compliant data feed is connected, so the fields stay empty rather than going stale.</li>
        <li><strong>No Amazon imagery is used.</strong> The photographs are original editorial illustrations and each one says so.</li>
        <li><strong>No performance claim is made as our own.</strong> Listing language is reproduced and labelled; everything else is framed as a question or omitted.</li>
        <li><strong>No deal badges, countdowns or limited-time promotion references.</strong> Section 2(b) makes each one a removal obligation the moment it expires.</li>
        <li><strong>No third-party script, cookie or tracking pixel.</strong> The event script transmits nothing unless an endpoint you control is configured, and no endpoint is configured.</li>
      </ol>
    </div>
  </section>

  <section style="padding:40px 0 70px">
    <h2 style="font-size:1.5rem">What is still open</h2>
    <p class="lede-sm">Six things cannot be closed from outside the Associates account, and they are not hidden. Each is on the <a href="{href(depth, 'flagged/')}">Flagged for review</a> page with the action that would close it.</p>
    <div class="panel panel-warn">
      <ul class="mb0">
        <li>Whether a click is attributed to <span class="mono">{TAG}</span> &#8212; unconfirmed, and unconfirmable without the dashboard.</li>
        <li>Whether the supplied <span class="mono">link.amazon</span> short links are compliant Special Links &#8212; unresolved, and not asserted either way.</li>
        <li>The commission rate for these categories &#8212; behind the sign-in, so never printed here.</li>
        <li>Whether the Associates account is in good standing &#8212; unknown, and it decides whether any of this can earn.</li>
        <li>What readers do &#8212; unmeasured, because there is no collector and nowhere on GitHub Pages to run one.</li>
        <li>Whether the appliances perform as claimed &#8212; untested, and therefore never presented as a verdict.</li>
      </ul>
    </div>
  </section>
</div>
"""
    write("sources", "index.html", page(
        1, "sources/", "Sources and compliance — The Pantry Journal",
        "Twelve quoted sources behind every statement on this site, with URLs, dates, and the eight-line compliance position.",
        body, active=None,
        jsonld=[org_jsonld(), crumbs_jsonld(1, [("Home", ""), ("Sources", "sources/")])]))


# --------------------------------------------------------------------------
# about
# --------------------------------------------------------------------------

def build_about():
    depth = 1
    a = EDIT["about"]
    paras = "".join(f"<p>{e(p)}</p>" for p in a["paras"])
    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{href(1, '')}">Home</a><span>&#8250;</span><span>About</span></nav>
  <section class="prose" style="padding:26px 0 60px">
    <p class="kicker">About</p>
    <h1>{e(a['h1'])}</h1>
    <p class="deck">{e(a['deck'])}</p>
    {paras}

    <h2 id="disclosure">The disclosure, in full</h2>
    <div class="panel panel-warn">
      <p><strong>{DISCLOSURE}</strong></p>
      <p class="mb0">{e(EDIT['affiliate_statement_extended'])} The full sentence sits in the strip under the masthead on every page of this site, and again in the footer. Amazon&#8217;s Operating Agreement, section 5, requires the statement to be clearly and prominently displayed; the FTC&#8217;s guidance asks that it be close enough to the recommendation to be weighed at the moment of reading. A footer alone fails that test on a long page, so it is above the first link.</p>
    </div>
    <p class="src">Sources: <a href="https://affiliate-program.amazon.com/help/operating/agreement" rel="noopener">Associates Program Operating Agreement, section 5</a> &#183; <a href="https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking" rel="noopener">FTC Endorsement Guides: What People Are Asking</a>. Both read 20 November 2026.</p>

    <h2>{e(a['author_h'])}</h2>
    <p>{e(a['author_body'])}</p>
    <div class="panel">
      <p class="eyebrow" style="margin-bottom:8px">On the AI part</p>
      <p class="mb0">{e(a['ai_note'])}</p>
    </div>

    <h2>What this shop will not do</h2>
    <ul>
      <li>It will not publish a price, a star rating or a stock figure, because it cannot source them lawfully.</li>
      <li>It will not call a machine the best, because nobody here has tested one.</li>
      <li>It will not use urgency — no countdowns, no &#8220;today only&#8221;, no deal badges that expire silently.</li>
      <li>It will not repeat a manufacturer&#8217;s performance claim as though it were a fact.</li>
      <li>It will not track you. No cookie, no pixel, no third-party script.</li>
      <li>It will not hide a gap. Every unresolved item is on the <a href="{href(depth, 'flagged/')}">Flagged for review</a> page.</li>
    </ul>

    <h2>How to challenge something</h2>
    <p>Two routes, both public. The <a href="{href(depth, 'suggestions/')}">Suggestions</a> page is a review queue where a proposed change can be compared against the alternatives before anything ships. The <a href="{href(depth, 'questions/')}">Decisions</a> page lists what could not be answered and what would answer it. Neither page is decoration: they are how this shop stays honest as it grows.</p>
  </section>
</div>
"""
    write("about", "index.html", page(
        1, "about/", "About — The Pantry Journal",
        "Who writes this shop, how the sourcing standard works, the AI assistance disclosed in plain terms, and the full affiliate disclosure.",
        body, active="about",
        jsonld=[org_jsonld(), crumbs_jsonld(1, [("Home", ""), ("About", "about/")])]))


# --------------------------------------------------------------------------
# site map, robots, 404
# --------------------------------------------------------------------------

def build_sitemap_page():
    depth = 1
    groups = [
        ("The shop", [
            ("products/", "All five appliances"),
            ("categories/", "Categories"),
            ("categories/air-fryers.html", "Air fryers"),
            ("categories/thermometers.html", "Thermometers"),
        ] + [(f"products/{p['slug']}/", f"{p['brand']} {p['short_name']}") for p in PRODUCTS["products"]]),
        ("Guides", [(f"guides/{g['slug']}/", g["title"]) for g in GUIDES["guides"]]),
        ("The record", [
            ("table/", "Table of record"),
            ("questions/", "Decisions and open questions"),
            ("flagged/", "Flagged for review"),
            ("sources/", "Sources and compliance"),
        ]),
        ("About this site", [
            ("about/", "Who writes this"),
            ("suggestions/", "Suggestions for review"),
            ("sitemap/", "This page"),
        ]),
    ]
    blocks = []
    for heading, items in groups:
        lis = "".join(f'<li><a href="{href(depth, t)}">{e(l)}</a></li>' for t, l in items)
        blocks.append(f'<div><h3>{e(heading)}</h3><ul style="font-size:.94rem">{lis}</ul></div>')

    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{href(1, '')}">Home</a><span>&#8250;</span><span>Site map</span></nav>
  <section style="padding:26px 0 8px;max-width:46em">
    <p class="kicker">Site map</p>
    <h1>Everything in this shop</h1>
    <p class="deck">One navigation group, one canonical site, and a footer that reaches every inspection surface. This page is the human version of the XML sitemap.</p>
  </section>
  <div class="grid grid-2" style="padding:26px 0 40px">{''.join(blocks)}</div>

  <section class="prose" style="padding-bottom:70px;max-width:none">
    <h2>Two older sections still live at this address</h2>
    <p>This repository published earlier editions before this shop existed. They are preserved rather than deleted, and they are not part of this shop&#8217;s sitemap or feed.</p>
    <div class="t-wrap"><table>
      <caption>Earlier editions in this repository</caption>
      <thead><tr><th scope="col">Path</th><th scope="col">What it is</th><th scope="col">Status</th></tr></thead>
      <tbody>
        <tr><td><a href="https://karagemop466-tech.github.io/Affil1/" rel="noopener">/Affil1/</a></td><td>The original storefront, with its own guide set and dashboard.</td><td>{pill('quiet', 'preserved')}</td></tr>
        <tr><td><a href="https://karagemop466-tech.github.io/Affil1/crisp/" rel="noopener">/Affil1/crisp/</a></td><td>A separate publication built by another session from the same brief.</td><td>{pill('quiet', 'preserved')}</td></tr>
      </tbody>
    </table></div>
    <p class="src" style="margin-top:12px">Whether to redirect these into the shop, archive them, or leave them is logged as SUG-16 on the <a href="{href(depth, 'suggestions/')}">Suggestions</a> page. This session will not edit another session&#8217;s files without a decision.</p>
  </section>
</div>
"""
    write("sitemap", "index.html", page(
        1, "sitemap/", "Site map — The Pantry Journal",
        "Every page in the shop, plus the status of two earlier editions that still live at this address.",
        body, active=None, jsonld=[org_jsonld()]))


def build_robots_404():
    write("", "robots.txt", "User-agent: *\nDisallow: /\n\n"
          "# Archived design edition. Not part of the live site.\n")
    body = f"""
<div class="wrap" style="padding:80px 24px 120px;max-width:640px">
  <p class="kicker">404</p>
  <h1>That page is not in the shop</h1>
  <p class="deck">Either the address is wrong or the page was retired. The shop is small enough that the whole of it fits below.</p>
  <div class="btn-row" style="margin:24px 0 34px">
    <a class="btn" href="{href(0, 'products/')}">See all five appliances</a>
    <a class="btn btn-ghost" href="{href(0, 'sitemap/')}">Site map</a>
  </div>
  <div class="related">
    <a href="{href(0, 'guides/')}"><span class="rl">Start here</span><span class="rt">Buying guides</span></a>
    <a href="{href(0, 'categories/')}"><span class="rl">Browse</span><span class="rt">Categories</span></a>
    <a href="{href(0, '')}"><span class="rl">Return</span><span class="rt">Home</span></a>
  </div>
</div>
"""
    write("", "404.html", page(0, "404.html", "Page not found — The Pantry Journal",
                                 "That page is not in the shop.", body))


# --------------------------------------------------------------------------
# feeds and xml sitemap
# --------------------------------------------------------------------------

def build_feeds():
    published = [g for g in GUIDES["guides"] if g["status"] == "published"]
    items = []
    for g in published:
        items.append(f"""  <item>
    <title>{e(g['title'])}</title>
    <link>{canonical('guides/' + g['slug'] + '/')}</link>
    <guid isPermaLink="true">{canonical('guides/' + g['slug'] + '/')}</guid>
    <pubDate>Fri, 20 Nov 2026 09:00:00 GMT</pubDate>
    <description>{e(g['deck'])}</description>
  </item>""")
    for p in PRODUCTS["products"]:
        items.append(f"""  <item>
    <title>{e(p['display_title'])} — {e(p['type_label'])}</title>
    <link>{canonical('products/' + p['slug'] + '/')}</link>
    <guid isPermaLink="true">{canonical('products/' + p['slug'] + '/')}</guid>
    <pubDate>Fri, 20 Nov 2026 08:00:00 GMT</pubDate>
    <description>{e(p['deck'])}</description>
  </item>""")
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{SITE}</title>
  <link>{BASE}</link>
  <atom:link href="{BASE}feed.xml" rel="self" type="application/rss+xml"/>
  <description>{e(EDIT['brand']['positioning'])}</description>
  <language>en-us</language>
  <lastBuildDate>Fri, 20 Nov 2026 09:00:00 GMT</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
"""
    write("", "feed.xml", feed)

    urls = [("", "1.0", "weekly"), ("products/", "0.9", "weekly"), ("categories/", "0.8", "monthly"),
            ("categories/air-fryers.html", "0.8", "monthly"), ("categories/thermometers.html", "0.8", "monthly"),
            ("guides/", "0.9", "weekly"), ("table/", "0.5", "monthly"), ("questions/", "0.5", "monthly"),
            ("sources/", "0.6", "monthly"), ("suggestions/", "0.5", "monthly"),
            ("about/", "0.6", "monthly"), ("sitemap/", "0.4", "monthly")]
    urls += [(f"products/{p['slug']}/", "0.8", "monthly") for p in PRODUCTS["products"]]
    urls += [(f"guides/{g['slug']}/", "0.8", "monthly") for g in GUIDES["guides"] if g["status"] == "published"]
    entries = "\n".join(
        f'  <url><loc>{canonical(u)}</loc><lastmod>{BUILD_DATE}</lastmod>'
        f'<changefreq>{c}</changefreq><priority>{pr}</priority></url>' for u, pr, c in urls)
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
"""
    write("", "sitemap.xml", sitemap)


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(SRC.parent / "shopassets", OUT / "assets")

    build_home()
    build_products_index()
    build_categories_index()
    for cat in CATS:
        build_category(cat)
    for p in PRODUCTS["products"]:
        build_product(p)
    build_guides_index()
    for g in GUIDES["guides"]:
        build_guide(g)
    build_table()
    build_flagged()
    build_questions()
    build_suggestions()
    build_sources()
    build_about()
    build_sitemap_page()
    build_robots_404()
    build_feeds()

    pages = sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*.html"))
    print(f"built {len(pages)} pages into archive/2026-11-20-pantry-journal/")
    for p in pages:
        print("  ", p)



# --------------------------------------------------------------------------
# root front door
# --------------------------------------------------------------------------

if __name__ == "__main__":
    main()
