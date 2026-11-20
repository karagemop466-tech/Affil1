"""The journal: guide index and guide pages."""

from layout import (breadcrumbs, breadcrumb_schema, buy_url, esc, eyebrow, outbound, page,
                    pagehead, product_link, rel, section, table)
from page_home import guide_card, img
from content import GUIDES


def _product_index():
    import json
    import pathlib
    root = pathlib.Path(__file__).resolve().parent.parent
    doc = json.loads((root / "_src/data/products.json").read_text(encoding="utf-8"))
    return {p["ref"]: p for p in doc["products"]}


def build_index(page_dir):
    d = page_dir
    clusters = []
    for g in GUIDES:
        if g["cluster"] not in clusters:
            clusters.append(g["cluster"])
    blocks = ""
    for i, c in enumerate(clusters):
        items = [g for g in GUIDES if g["cluster"] == c]
        blocks += section(f"""
<div class="sec-head"><div>{eyebrow(c)}<h2>{esc(c)}</h2></div>
<p>{esc(_cluster_blurb(c))}</p></div>
<div class="gcard-grid {'two' if len(items) < 3 else 'three'}">
{''.join(guide_card(d, g) for g in items)}
</div>""", cls="" if i % 2 == 0 else "section-tint")

    body = f"""{pagehead(
        'The journal',
        'Buying guides that<br>start with your question',
        f'{len(GUIDES)} guides, each built around one decision a shopper actually faces: which shape, how big, how much washing, and whether the extra feature is worth the counter space.',
        meta='Updated 20 November 2026 &middot; no sponsored rankings, no invented test results',
    )}
{section(f'''
<div class="feature-guide">
  <div class="feature-guide-media">{img(d, GUIDES[0]['photo'], GUIDES[0]['photo_alt'], sizes='(max-width:820px) 100vw, 560px', loading='eager')}</div>
  <div class="feature-guide-copy">
    {eyebrow('Start here')}
    <h2>{esc(GUIDES[0]['title'])}</h2>
    <p class="dek">{esc(GUIDES[0]['dek'])}</p>
    <p>The single most useful thing you can do before buying an air fryer is decide whether you want a drawer or a door. Everything else in the category is downstream of that.</p>
    <a class="btn btn-small" href="{esc(rel(d, 'guides/' + GUIDES[0]['slug'] + '.html'))}">Read the guide</a>
  </div>
</div>''', cls='')}
{blocks}"""
    return page(
        d,
        title="Guides \u2014 air fryers, capacity and thermometers | Crisp & Counter",
        description=f"{len(GUIDES)} question-shaped buying guides: basket or oven, dual-zone, capacity, cleanup, small kitchens, multi-function appliances, thermometers, seasonal hosting, gift formats and the Black Friday checklist.",
        body=body,
        active="guides/index.html",
        canonical="guides/",
        structured=breadcrumb_schema([], "Guides", "guides/"),
    )


def _cluster_blurb(c):
    return {
        "Choosing": "Basket, oven, one drawer or two. The decision that makes the rest of the spec sheet irrelevant.",
        "Sizing": "How much food actually fits, in the units that matter rather than the ones on the box.",
        "Living with it": "Washing, storing and counter space \u2014 the parts that decide whether you keep using it.",
        "Before you buy": "The questions a listing will never volunteer an answer to.",
        "Tools": "Probes, leave-in thermometers, and what they change about cooking with an air fryer.",
        "Seasonal": "Cooking for a crowd, and where a countertop machine genuinely helps.",
    }.get(c, "")


def build_guide(page_dir, g, meta):
    d = page_dir
    href = f"guides/{g['slug']}.html"
    products = _product_index()

    article = []
    for s in g["sections"]:
        block = [f"<h2>{esc(s['h'])}</h2>"]
        for para in s.get("p", []):
            block.append(f"<p>{esc(para)}</p>")
        if s.get("table"):
            t = s["table"]
            rows = []
            for r in t["rows"]:
                row_cells = []
                for cell in r:
                    if isinstance(cell, dict) and cell.get("url"):
                        row_cells.append({"html": outbound(d, cell["url"], esc(cell["label"]))})
                    else:
                        row_cells.append(cell)
                rows.append(row_cells)
            block.append(table(t["headers"], rows, cls="guide-table", caption=t.get("caption")))
        if s.get("items"):
            block.append('<dl class="guide-items">')
            for term, text in s["items"]:
                block.append(f"<div><dt>{esc(term)}</dt><dd>{esc(text)}</dd></div>")
            block.append("</dl>")
        article.append("".join(block))

    related = "".join(
        f"""<article class="mini-product">
  <div class="mini-product-media">{img(d, products[r]['photo'], products[r]['photo_alt'], sizes='120px')}</div>
  <div>
    <p class="mini-kicker">{esc(products[r]['brand'])} &middot; {esc(products[r]['format_label'])}</p>
    <h3><a href="{esc(rel(d, 'products/' + r.lower() + '.html'))}">{esc(products[r]['name'])}</a></h3>
    {product_link(d, buy_url(products[r]['observed_asin']), 'See on Amazon <span aria-hidden="true">&#8599;</span>', cls='tlink', aria=f"Open the Amazon listing for {r} (paid link, opens in a new tab)")}
  </div>
</article>"""
        for r in g.get("related", []) if r in products
    )

    idx = [x["slug"] for x in GUIDES].index(g["slug"])
    nxt = GUIDES[(idx + 1) % len(GUIDES)]

    body = f"""{breadcrumbs(d, [("guides/index.html", "Guides")])}
<header class="article-head"><div class="wrap narrow">
  {eyebrow(g['cluster'] + ' · ' + str(g['read_minutes']) + ' min read')}
  <h1>{esc(g['title'])}</h1>
  <p class="dek">{esc(g['dek'])}</p>
  <p class="article-meta">Updated {esc(g['updated'])} &middot; Crisp &amp; Counter</p>
</div></header>
<div class="wrap article-hero">
  {img(d, g['photo'], g['photo_alt'], sizes='100vw', loading='eager')}
  <p class="fig-note">{esc(g['photo_caption'])}</p>
</div>
<div class="wrap article-layout">
  <article class="article-body">
    {''.join(article)}
    <p class="article-close">{esc(g['closing'])}</p>
  </article>
  <aside class="article-side">
    <div class="side-card">
      <p class="q-label">In this guide</p>
      <ul class="side-links">
        {''.join(f'<li><a href="#{esc(_anchor(s["h"]))}">{esc(s["h"])}</a></li>' for s in g["sections"])}
      </ul>
    </div>
    <div class="side-card-quiet">
      <p class="q-label">Paid links</p>
      <p>Product links in these guides earn a commission. They are marked <code>sponsored</code> and every one carries the site's Amazon tag.</p>
    </div>
  </aside>
</div>
<section class="section section-tint"><div class="wrap">
  <div class="sec-head"><div>{eyebrow('In this edit')}<h2>The products this guide refers to</h2></div>
  <p>Open the note for the full record, or go straight to the listing.</p></div>
  <div class="mini-grid">{related}</div>
</div></section>
<section class="section"><div class="wrap">
  <a class="next-card" href="{esc(rel(d, 'guides/' + nxt['slug'] + '.html'))}">
    <span class="eyebrow">Read next &middot; {esc(nxt['cluster'])}</span>
    <h2>{esc(nxt['title'])}</h2>
    <p>{esc(nxt['dek'])}</p>
    <span class="tlink">Continue <span aria-hidden="true">&rarr;</span></span>
  </a>
</div></section>"""
    # anchors must exist on the page for the in-guide contents list
    for s in g["sections"]:
        body = body.replace(f"<h2>{esc(s['h'])}</h2>",
                            f"<h2 id=\"{esc(_anchor(s['h']))}\">{esc(s['h'])}</h2>", 1)

    return page(
        d,
        title=f"{esc(g['title'])} | Crisp & Counter",
        description=g["dek"],
        body=body,
        active="guides/index.html",
        canonical=href,
        og_type="article",
        structured=[
            breadcrumb_schema([("guides/index.html", "Guides")], g["title"], href),
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": g["title"],
                "description": g["dek"],
                "datePublished": g["updated"],
                "dateModified": g["updated"],
                "author": {"@type": "Organization", "name": "Crisp & Counter"},
                "publisher": {"@type": "Organization", "name": "Crisp & Counter"},
                "mainEntityOfPage": f"https://karagemop466-tech.github.io/Affil1/{href}",
            },
        ],
    )


def _anchor(heading):
    out = []
    for ch in heading.lower():
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")
