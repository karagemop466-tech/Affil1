"""The guide index (a cluster map) and the article template."""

from layout import (DISCLOSURE, SITE_NAME, esc, eyebrow, page, pagehead, rel,
                    section)
from content import CLUSTERS, GUIDES
from page_home import picture


def build_index(page_dir, meta):
    d = page_dir
    by_slug = {g["slug"]: g for g in GUIDES}
    cards = []

    # The cluster map first: a reader arrives with a problem, not a product.
    for i, c in enumerate(CLUSTERS):
        g = by_slug.get(c["slug"])
        if not g:
            continue
        href = rel(d, f"guides/{g['slug']}.html")
        cards.append(f"""<article class="cluster-card">
  <div class="cluster-head">
    <span class="path-n">{i + 1:02d}</span>
    <p class="gcard-kicker">{esc(c['name'])} &middot; {g['read_minutes']} min</p>
  </div>
  <h3><a href="{esc(href)}">{esc(c['question'])}</a></h3>
  <p>{esc(c['dek'])}</p>
  <a class="tlink" href="{esc(href)}">Read the guide <span aria-hidden="true">&rarr;</span></a>
</article>""")

    rest = [g for g in GUIDES if g["slug"] not in {c["slug"] for c in CLUSTERS}]
    extras = "".join(f"""<article class="gcard">
  <a class="gcard-media" href="{esc(rel(d, 'guides/' + g['slug'] + '.html'))}" tabindex="-1" aria-hidden="true">
    {picture(d, g['photo'], g['photo_alt'], sizes='(max-width:720px) 100vw, 380px')}
  </a>
  <div class="gcard-body">
    <p class="gcard-kicker">{esc(g['kicker'])} &middot; {g['read_minutes']} min read</p>
    <h3><a href="{esc(rel(d, 'guides/' + g['slug'] + '.html'))}">{esc(g['title'])}</a></h3>
    <p>{esc(g['dek'])}</p>
    <a class="tlink" href="{esc(rel(d, 'guides/' + g['slug'] + '.html'))}">Read the guide <span aria-hidden="true">&rarr;</span></a>
  </div>
</article>""" for g in rest)

    body = f"""{pagehead(
        'Buying guides',
        'Five questions,<br>five checklists',
        'Each guide starts from the thing that is making the choice hard, not from a product. They are written to be useful whether '
        'or not you buy anything through this site, and every product claim in them is quoted from the seller.',
        meta='No product tested &middot; no prices, ratings or winners &middot; each topic is a hypothesis, not a demand forecast',
    )}
{section(f'''
<div class="sec-head"><div>{eyebrow('The cluster map')}<h2>Start where the decision starts</h2></div>
<p>Four clusters, each with one anchor guide. Anything published later joins one of them rather than sitting on its own.</p></div>
<div class="cluster-grid">{''.join(cards)}</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Also worth reading')}<h2>The wider question</h2></div>
<p>One guide that is not about a single appliance shape, because the brief it answers is not either.</p></div>
<div class="gcard-grid">{extras}</div>
<p class="sec-foot">Every guide carries the same disclosure and the same limit: <a href="{esc(rel(d, 'about/index.html'))}#why-blank">nothing here was tested</a>.</p>''', cls='section-tint')}
{section(f'''
<div class="callout">
  <h2>How a topic gets chosen here</h2>
  <p>Not by instinct. The four clusters exist because they are the decisions the five products sit inside. The next topic is
  supposed to come from measured queries &mdash; and no query data exists yet, which is why the publishing cadence is a proposal on the
  <a href="{esc(rel(d, 'suggestions/index.html'))}">suggestions page</a> rather than a schedule you can hold this site to.</p>
</div>''', cls='')}
"""
    return page(
        d,
        title="Buying guides \u2014 five checklists for kitchen decisions | Crisp & Counter",
        description=("Five buying guides organised into clusters: basket or oven, real capacity, cleanup and counter space, "
                     "multi-function appliances, and choosing a thermometer. No test claims, no invented prices."),
        body=body,
        active="guides/index.html",
        canonical="guides/",
        breadcrumb=[("Home", ""), ("Guides", "guides/")],
    )


def build_guide(page_dir, g, meta):
    d = page_dir
    blocks = []
    for i, s in enumerate(g["sections"]):
        parts = [f"<h2>{esc(s['h'])}</h2>"]
        for para in s.get("p", []):
            parts.append(f"<p>{esc(para)}</p>")
        if s.get("items"):
            parts.append('<dl class="checks">')
            for term, desc in s["items"]:
                parts.append(f"<div><dt>{esc(term)}</dt><dd>{esc(desc)}</dd></div>")
            parts.append("</dl>")
        blocks.append(f'<section class="prose-block" id="s{i+1}">' + "".join(parts) + "</section>")

    toc = "".join(f'<li><a href="#s{i+1}">{esc(s["h"])}</a></li>' for i, s in enumerate(g["sections"]))
    cluster = next((c for c in CLUSTERS if c["slug"] == g["slug"]), None)

    products = meta.get("products", [])
    related = []
    if cluster and cluster["name"] == "Thermometers":
        related = [x for x in products if x.get("format") == "thermometer"]
    else:
        related = [x for x in products if x.get("format") != "thermometer"]

    rel_cards = "".join(f'''<a class="mini-product" href="{esc(rel(d, 'products/' + x['ref'].lower() + '.html'))}">
  <span class="mini-ref">{esc(x['ref'])}</span>
  <span class="mini-name">{esc(x.get('card_title') or x.get('format_label') or '')}</span>
  <span class="mini-note">{esc(x.get('brand') or '')} &middot; {esc(x.get('format_label') or '')}</span>
</a>''' for x in related[:3])

    others = [x for x in GUIDES if x["slug"] != g["slug"]][:2]
    next_html = "".join(f"""<a class="next-card" href="{esc(rel(d, 'guides/' + x['slug'] + '.html'))}">
  <p class="gcard-kicker">{esc(x['kicker'])} &middot; {x['read_minutes']} min</p>
  <h3>{esc(x['title'])}</h3>
  <span class="tlink">Read <span aria-hidden="true">&rarr;</span></span></a>""" for x in others)

    body = f"""{pagehead(
        g['kicker'],
        esc(g['title']),
        esc(g['dek']),
        meta=f"Updated {esc(g['updated'])} &middot; {g['read_minutes']} min read &middot; no product tested &middot; no prices or ratings",
    )}
<section class="section"><div class="wrap article-grid">
  <article class="article">
    <figure class="fig">
      {picture(d, g['photo'], g['photo_alt'], sizes='(max-width:900px) 100vw, 720px', loading='eager')}
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
    <div class="side-card">
      <h2>In the register</h2>
      {rel_cards}
      <p class="side-note"><a href="{esc(rel(d, 'products/index.html'))}">All five, with the source links</a></p>
    </div>
    <div class="side-card side-card-quiet">
      <h2>The limit</h2>
      <p>Nothing here comes from using a product. Where a fact was needed and could not be sourced, the guide says so instead
      of filling it in.</p>
      <p><a href="{esc(rel(d, 'about/index.html'))}#why-blank">Why the gaps exist</a></p>
    </div>
  </aside>
</div></section>
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
        description=g["dek"][:158],
        body=body,
        active="guides/index.html",
        canonical=f"guides/{g['slug']}.html",
        structured=structured,
        og_type="article",
        breadcrumb=[("Home", ""), ("Guides", "guides/"), (cluster["name"] if cluster else g["kicker"], f"guides/{g['slug']}.html")],
    )
