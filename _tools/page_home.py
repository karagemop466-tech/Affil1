"""The front page: a publication front page that happens to sell five things.

Structure is deliberate. Products first, in their categories, with a buy button
on every card. Guides second, as the reason to stay. The machinery of
verification is one line and a link, because a shopper does not need the audit
before the shortlist.
"""

import pathlib

from layout import (AMAZON_NOTE, esc, eyebrow, link, page, product_link, rel,
                    section, buy_url)
from content import GUIDES


def img(page_dir, path, alt, *, sizes, cls="", loading="lazy"):
    """Responsive image. Falls back to the single-size original when a source has
    no generated width variants, so a template can never emit a dead srcset."""
    root = pathlib.Path(__file__).resolve().parent.parent
    wide = root / (path + "-w900.jpg")
    small = root / (path + "-w560.jpg")
    base = root / (path + ".jpg")
    if wide.exists() and small.exists():
        srcset = f'srcset="{esc(rel(page_dir, path + "-w560.jpg"))} 560w, {esc(rel(page_dir, path + "-w900.jpg"))} 900w" '
        src = path + "-w900.jpg"
    elif base.exists():
        srcset = ""
        src = path + ".jpg"
    else:
        raise SystemExit(f"missing image asset: {path}.jpg")
    return (
        f'<img class="{esc(cls)}" src="{esc(rel(page_dir, src))}" '
        f'{srcset}'
        f'sizes="{esc(sizes)}" alt="{esc(alt)}" loading="{esc(loading)}" decoding="async">'
    )


def _chips(p):
    """Two stated facts, short enough to scan on a card."""
    chips = []
    cap = p.get("stated_capacity")
    if cap and not cap.startswith("Not applicable"):
        chips.append(cap.split(",")[0].strip())
    attrs = p.get("stated_attributes") or ""
    if attrs:
        chips.append(attrs.split(";")[0].strip())
    return "".join(f'<li>{esc(c)}</li>' for c in chips[:3])


def product_card(page_dir, p):
    href = rel(page_dir, f"products/{p['ref'].lower()}.html")
    media = (
        f'<a class="pcard-media" href="{esc(href)}" tabindex="-1" aria-hidden="true">'
        f'{img(page_dir, p["photo"], p["photo_alt"], sizes="(max-width:720px) 100vw, 340px")}'
        f'<span class="illus-tag">Illustration</span></a>'
    )
    return f"""<article class="pcard">
  {media}
  <div class="pcard-body">
    <p class="pcard-ref">{esc(p['brand'])} &middot; {esc(p['format_label'])}</p>
    <h3><a href="{esc(href)}">{esc(p['name'])}</a></h3>
    <p class="pcard-why">{esc(p['why'])}</p>
    <ul class="chips">{_chips(p)}</ul>
    <p class="pcard-actions">
      {product_link(page_dir, buy_url(p['observed_asin']), 'See it on Amazon <span aria-hidden="true">&#8599;</span>', cls='btn btn-small', aria=f"Open the Amazon listing for {p['brand']} {p['format_label']} (listing source, opens in a new tab)")}
      <a class="tlink" href="{esc(href)}">Read the note <span aria-hidden="true">&rarr;</span></a>
    </p>
    <p class="pcard-fine">Listing source &middot; {esc(AMAZON_NOTE)}</p>
  </div>
</article>"""


BUYER_NOTES = {
    "P-01": "Cooking dinner and a side? Compare the size of each basket, not just their combined volume.",
    "P-02": "Want room for a tray? Check the usable rack dimensions and how far the doors swing.",
    "P-03": "Prefer one basket? Check whether your usual batch fits in a single layer.",
}


def issue_card(page_dir, p):
    href = rel(page_dir, f"products/{p['ref'].lower()}.html")
    art, name, spec = {
        "P-01": ("dual", "Chefman Dual Basket", "6 qt · Two baskets"),
        "P-02": ("oven", "Emeril Lagasse French Door", "26 qt · Oven style"),
        "P-03": ("single", "Chefman TurboFry", "8 qt · Single basket"),
    }[p['ref']]
    return f"""<article class="edit-card">
  <a class="edit-art" href="{esc(href)}" aria-label="Read about {esc(name)}">
    <img src="{esc(rel(page_dir, 'assets/img/storefront-' + art + '-w900.jpg'))}" loading="lazy" alt="Editorial drawing of the {esc(p['format_label'])} format">
    <span class="folio">FIG. {esc(p['ref'][-2:])}</span><span class="art-note">Format illustration</span></a>
  <div class="edit-info"><span class="ink-label">{esc(spec)}</span>
    <h3><a href="{esc(href)}">{esc(name)}</a></h3><p>{esc(BUYER_NOTES[p['ref']])}</p>
    <a class="edit-more" href="{esc(href)}">Explore this format →</a>
  </div></article>"""


def guide_card(page_dir, g, *, feature=False):
    href = rel(page_dir, f"guides/{g['slug']}.html")
    cls = "gcard gcard-feature" if feature else "gcard"
    return f"""<article class="{cls}">
  <a class="gcard-media" href="{esc(href)}" tabindex="-1" aria-hidden="true">
    {img(page_dir, g['photo'], g['photo_alt'], sizes='(max-width:720px) 100vw, 380px')}
  </a>
  <div class="gcard-body">
    <p class="gcard-kicker">{esc(g['cluster'])} &middot; {g['read_minutes']} min read</p>
    <h3><a href="{esc(href)}">{esc(g['title'])}</a></h3>
    <p>{esc(g['dek'])}</p>
    <a class="tlink" href="{esc(href)}">Read the guide <span aria-hidden="true">&rarr;</span></a>
  </div>
</article>"""


def build(page_dir, products, meta):
    d = page_dir
    by_ref = {p["ref"]: p for p in products}
    categories = products_meta_categories(products, by_ref)
    air = categories[0]["items"]
    therm = categories[1]["items"]

    hero = f"""<section class="issue-cover wrap">
  <div class="issue-text"><p class="issue-line"><span class="edition">ISSUE Nº 01</span> THE COUNTERTOP EDIT</p>
    <h1>The air fryer<br><em>field guide.</em></h1>
    <p class="cover-dek">One basket, two baskets, or French doors? Find the format that fits your counter and the way you cook.</p>
    <div class="cover-actions"><a class="cover-btn" href="#shortlist">Explore the shortlist <span>→</span></a>
      <a class="cover-link" href="{esc(rel(d, 'fit/index.html'))}">Find your format ↗</a></div></div>
  <figure class="cover-art"><img fetchpriority="high" src="{esc(rel(d,'assets/img/storefront-hero-w1280.jpg'))}" alt="An engraved illustration of a basket air fryer with garlic and rosemary">
    <span class="cover-seal" aria-hidden="true">KITCHEN<br><b>✳</b><br>EDITION</span>
    <figcaption>FIG. 01 &nbsp;/&nbsp; FORMAT ILLUSTRATION</figcaption></figure>
</section>"""

    shop = section(f"""<div class="edit-head"><div><p class="ink-label"><i></i> SHOP BY FORMAT</p>
      <h2>The countertop shortlist<span>.</span></h2></div>
      <a class="edit-all" href="{esc(rel(d,'products/index.html'))}">All products <span>→</span></a></div>
      <div class="edit-grid">{''.join(issue_card(d,p) for p in air)}</div>""", cls="edit-shop", sid="shortlist")

    thermo = section(f"""
<div class="sec-head">
  <div>{eyebrow('The edit')}<h2>Thermometers, because browning lies</h2></div>
  <p>An air fryer can tell you the outside is done. Only a probe tells you the inside is.</p>
</div>
<div class="pcard-grid two">
{''.join(product_card(d, p) for p in therm)}
</div>
<p class="sec-foot"><a class="tlink" href="{esc(rel(d, 'guides/thermometer-pairing.html'))}">Which thermometer for an air fryer? <span aria-hidden="true">&rarr;</span></a></p>""",
                    cls="section-tint")

    paths = section(f"""
<div class="sec-head">
  <div>{eyebrow('Start here')}<h2>Three questions, three answers</h2></div>
  <p>If you are not ready to shop, start with the thing that is making the choice hard.</p>
</div>
<div class="path-grid">
  <a class="path" href="{esc(rel(d, 'guides/basket-or-oven-air-fryer.html'))}">
    <span class="path-n">01</span><h2>Which shape do I want?</h2>
    <p>A drawer and a door change how often you intervene, what fits inside and how much counter you give up.</p>
    <span class="tlink">Compare the shapes <span aria-hidden="true">&rarr;</span></span>
  </a>
  <a class="path" href="{esc(rel(d, 'guides/air-fryer-capacity-checklist.html'))}">
    <span class="path-n">02</span><h2>Is it big enough?</h2>
    <p>A quart is a volume. You cook on a surface. Convert one into the other before you buy.</p>
    <span class="tlink">Work out capacity <span aria-hidden="true">&rarr;</span></span>
  </a>
  <a class="path" href="{esc(rel(d, 'guides/cleanup-and-counter-space.html'))}">
    <span class="path-n">03</span><h2>Will I actually keep using it?</h2>
    <p>The parts you wash and the space it occupies decide that. Both are checkable in five minutes.</p>
    <span class="tlink">Check the everyday cost <span aria-hidden="true">&rarr;</span></span>
  </a>
</div>""", cls="paths")

    # The band used to be GUIDES[7] plus a paragraph of hand-written hosting copy.
    # Any change to the order in content.py silently decoupled the two: the front page
    # was labelled "Seasonal · hosting" and invited the reader to "Read the hosting
    # guide" underneath the thermometer article. Now the feature is chosen by cluster
    # and every word in the band comes from the chosen guide's own record, so a
    # mismatch is not representable.
    feature = next((g for g in reversed(GUIDES) if g["cluster"] in ("Seasonal", "Cooking")),
                   GUIDES[-1])
    feat_href = rel(d, f"guides/{feature['slug']}.html")
    # The band's supporting line is the guide's own opening paragraph, not a
    # separate caption someone might have to remember to update.
    feature_lede = next((para for s in feature["sections"] for para in s.get("p", [])),
                        feature["dek"])
    seasonal = section(f"""
<div class="seasonal">
  <div class="seasonal-media">{img(d, feature['photo'], feature['photo_alt'], sizes='(max-width:820px) 100vw, 520px')}</div>
  <div class="seasonal-copy">
    {eyebrow(f"{feature['cluster']} · {feature['kicker']}")}
    <h2>{esc(feature['title'])}</h2>
    <p class="dek">{esc(feature['dek'])}</p>
    <p>{esc(feature_lede)}</p>
    <a class="btn btn-small" href="{esc(feat_href)}">Read the guide</a>
  </div>
</div>""", cls="seasonal-band")

    # Most recently updated first, ties broken by the order the guides were added.
    picks = sorted(range(len(GUIDES)),
                   key=lambda i: (GUIDES[i]["updated"], i), reverse=True)[:4]

    latest = section(f"""
<div class="sec-head">
  <div>{eyebrow('The journal')}<h2>Guides worth your ten minutes</h2></div>
  <p>Question-shaped, answer-first, and honest about what a listing can and cannot tell you.</p>
</div>
<div class="gcard-grid">
{''.join(guide_card(d, GUIDES[i]) for i in picks)}
</div>
<p class="sec-foot"><a class="tlink" href="{esc(rel(d, 'guides/index.html'))}">All {len(GUIDES)} guides <span aria-hidden="true">&rarr;</span></a></p>""",
                    cls="")

    method = section(f"""
<div class="method-grid">
  <div>
    {eyebrow('How this works')}
    <h2>We check the link. You check your counter.</h2>
    <p>Crisp &amp; Counter is a small publication, not a retailer. Each of the five links you see was opened, followed to the Amazon listing it lands on, and matched to the product named here. What we cannot verify, we leave out.</p>
    <p>The result is a shop with fewer numbers than usual and no invented ones. Ratings, prices and stock are left where they belong: on Amazon, changing in real time.</p>
  </div>
  <ul class="method-list">
    <li><span>01</span><div><strong>Open the link.</strong> Record where it actually lands, on the day.</div></li>
    <li><span>02</span><div><strong>Read the listing.</strong> Transcribe what the seller states, in their words.</div></li>
    <li><span>03</span><div><strong>Say what it changes.</strong> Editorial notes explain the trade, not a test result.</div></li>
    <li><span>04</span><div><strong>Leave blanks blank.</strong> No price, rating or review count without a permitted source.</div></li>
  </ul>
</div>""", cls="section-tint method-band")

    capture = section(f"""
<div class="capture-card">
  <div>
    {eyebrow('Keep in touch')}
    <h2>One new guide a fortnight, no inbox required</h2>
    <p>There is no mailing list yet, and no form to fill in. The site publishes an RSS feed: point a reader at it and new guides arrive when they are written. When a mailing list exists, this is where it will be &mdash; with a date and a privacy page behind it.</p>
  </div>
  <p class="capture-actions">
    <a class="btn" href="{esc(rel(d, 'feed.xml'))}">Add the RSS feed</a>
    <a class="btn btn-ghost" href="{esc(rel(d, 'suggestions/index.html'))}">Suggest a topic</a>
  </p>
</div>""", cls="capture")

    body = hero + shop + thermo + paths + seasonal + latest + method + capture
    return page(
        d,
        title="Crisp & Counter \u2014 air fryers and thermometers, checked and explained",
        description="Five Amazon picks for air frying, each link opened and matched to its live listing: two basket air fryers, one French-door oven and two meat thermometers. Listing sources and disclosure on every page.",
        body=body,
        active="index.html",
        canonical="",
        body_class="home",
        structured=[
            {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": "Crisp & Counter",
                "url": "https://karagemop466-tech.github.io/Affil1/",
                "description": "Air fryer and thermometer buying guides, with each product link checked against the live Amazon listing.",
            },
            {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "name": "The Crisp & Counter edit",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1,
                     "name": f"{p['brand']} {p['format_label']}",
                     "url": f"https://karagemop466-tech.github.io/Affil1/products/{p['ref'].lower()}.html"}
                    for i, p in enumerate(products)
                ],
            },
        ],
    )


def products_meta_categories(products, by_ref):
    """Read categories from products.json so the order is data, not a template."""
    import json
    import pathlib
    root = pathlib.Path(__file__).resolve().parent.parent
    doc = json.loads((root / "_src/data/products.json").read_text(encoding="utf-8"))
    cats = doc["meta"].get("categories", [])
    out = []
    for c in cats:
        out.append({"id": c["id"], "label": c["label"], "blurb": c.get("blurb", ""),
                    "items": [by_ref[r] for r in c["refs"] if r in by_ref]})
    return out
