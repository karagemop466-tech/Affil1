"""Guide index and article template."""

from layout import (DISCLOSURE, SITE_NAME, esc, eyebrow, page, pagehead, rel,
                    section, table)
from content import GUIDES
from page_home import img, product_card


def build_index(page_dir, meta):
    d = page_dir
    cards = []
    for i, g in enumerate(GUIDES):
        href = rel(d, f"guides/{g['slug']}.html")
        cards.append(f"""<article class="gcard{' gcard-feature' if i == 0 else ''}">
  <a class="gcard-media" href="{esc(href)}" tabindex="-1" aria-hidden="true">{img(d, g['photo'], g['photo_alt'], sizes='(max-width:720px) 100vw, 380px')}</a>
  <div class="gcard-body">
    <p class="gcard-kicker">{esc(g['kicker'])} &middot; {g['read_minutes']} min</p>
    <h3><a href="{esc(href)}">{esc(g['title'])}</a></h3>
    <p>{esc(g['dek'])}</p>
    <a class="tlink" href="{esc(href)}">Read guide <span aria-hidden="true">&rarr;</span></a>
  </div>
</article>""")

    body = f"""{pagehead(
        'Buying guides',
        f'{len(GUIDES)} questions worth<br>answering before you buy',
        'Written to be useful whether or not you click a single link. Each guide is a practical checklist grounded in verified listing facts and official USDA FSIS food-safety charts.',
        meta='No product was tested &middot; every product claim is quoted from the seller &middot; no prices, ratings or winners',
    )}
{section(f'''
<div class="gcard-grid">{''.join(cards)}</div>
<p class="sec-foot">Browse by product category: <a href="{esc(rel(d, 'products/air-fryers.html'))}">Air Fryers (3)</a> &middot; <a href="{esc(rel(d, 'products/thermometers.html'))}">Meat Thermometers (2)</a> &middot; <a href="{esc(rel(d, 'about/index.html'))}#why-blank">Why nothing is rated or priced</a>.</p>''')}"""
    return page(
        d,
        title="Buying guides \u2014 Crisp & Counter",
        description=f"{len(GUIDES)} kitchen buying guides across air fryers and meat thermometers: basket vs. oven, instant-read vs. wireless probes with USDA safe temperatures, capacity, cleanup, meal prep and hosting.",
        body=body,
        active="guides/index.html",
        canonical="guides/",
    )


def build_guide(page_dir, g, products, meta):
    d = page_dir
    by_ref = {p["ref"]: p for p in products}
    blocks = []
    for i, s in enumerate(g["sections"]):
        parts = [f"<h2>{esc(s['h'])}</h2>"]
        for para in s.get("p", []):
            parts.append(f"<p>{esc(para)}</p>")
        if s.get("table"):
            t = s["table"]
            parts.append(table(t["headers"], t["rows"], cls="guide-table", caption=t.get("caption")))
        if s.get("items"):
            parts.append('<dl class="checks">')
            for term, desc in s["items"]:
                parts.append(f"<div><dt>{esc(term)}</dt><dd>{esc(desc)}</dd></div>")
            parts.append("</dl>")
        anchor = f' id="s{i+1}"'
        blocks.append(f'<section class="prose-block"{anchor}>' + "".join(parts) + "</section>")

    toc = "".join(
        f'<li><a href="#s{i+1}">{esc(s["h"])}</a></li>' for i, s in enumerate(g["sections"])
    )

    related_html = ""
    rel_prods = [by_ref[r] for r in g.get("related_refs", []) if r in by_ref]
    if rel_prods:
        grid_cls = "pcard-grid pcard-grid-3" if len(rel_prods) == 3 else "pcard-grid wide"
        related_html = section(f"""
<div class="sec-head"><div>{eyebrow('Referenced in this guide')}<h2>Listings mentioned above</h2></div>
<p>Every link below opens the verified Amazon listing as a marked sponsored link, or takes you to the full product-intent record.</p></div>
<div class="{grid_cls}">
  {''.join(product_card(d, p, compact=True) for p in rel_prods)}
</div>""", cls="")

    others = [x for x in GUIDES if x["slug"] != g["slug"]][:2]
    next_html = "".join(f"""<a class="next-card" href="{esc(rel(d, 'guides/' + x['slug'] + '.html'))}">
  <p class="gcard-kicker">{esc(x['kicker'])} &middot; {x['read_minutes']} min</p>
  <h3>{esc(x['title'])}</h3>
  <span class="tlink">Read guide <span aria-hidden="true">&rarr;</span></span></a>""" for x in others)

    body = f"""{pagehead(
        g['kicker'],
        esc(g['title']),
        esc(g['dek']),
        meta=f"Updated {esc(g['updated'])} &middot; {g['read_minutes']} min read &middot; no product tested &middot; no prices or ratings",
    )}
<section class="section"><div class="wrap article-grid">
  <article class="article">
    <figure class="fig">
      {img(d, g['photo'], g['photo_alt'], sizes='(max-width:900px) 100vw, 720px', loading='eager')}
      <figcaption><span class="illus-tag illus-inline">Illustration</span> {esc(g['photo_caption'])}</figcaption>
    </figure>
    {''.join(blocks)}
    <div class="article-end">
      <p class="article-close">{esc(g['closing'])}</p>
      <p class="fineprint">{DISCLOSURE} Links to Amazon on this site are affiliate links. A purchase through one does not change the price you pay.</p>
    </div>
  </article>
  <aside class="article-side">
    <nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>{toc}</ol></nav>
    <div class="side-card side-card-quiet">
      <h2>The limit</h2>
      <p>Nothing in this guide comes from testing a product. Product claims come strictly from live listing titles; food-safety figures come strictly from USDA FSIS (<a href="{esc(rel(d, 'about/index.html'))}#sources">Sources</a>).</p>
      <p><a href="{esc(rel(d, 'about/index.html'))}#why-blank">Why the gaps exist</a></p>
    </div>
  </aside>
</div></section>
{related_html}
<section class="section section-tint"><div class="wrap">
  <div class="sec-head"><div>{eyebrow('Keep reading')}<h2>Two more, same standard</h2></div></div>
  <div class="next-grid">{next_html}</div>
</div></section>"""

    structured = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": g["title"],
        "description": g["dek"],
        "datePublished": g["updated"],
        "dateModified": g["updated"],
        "author": {"@type": "Organization", "name": SITE_NAME},
        "publisher": {"@type": "Organization", "name": SITE_NAME},
        "isAccessibleForFree": True,
    }
    return page(
        d,
        title=f"{g['title']} \u2014 Crisp & Counter",
        description=g["dek"],
        body=body,
        active="guides/index.html",
        canonical=f"guides/{g['slug']}.html",
        structured=structured,
        og_type="article",
    )
