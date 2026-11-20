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
      {product_link(page_dir, buy_url(p['observed_asin']), 'See it on Amazon <span aria-hidden="true">&#8599;</span>', cls='btn btn-small', aria=f"Open the Amazon listing for {p['brand']} {p['format_label']} (paid link, opens in a new tab)")}
      <a class="tlink" href="{esc(href)}">Read the note <span aria-hidden="true">&rarr;</span></a>
    </p>
    <p class="pcard-fine">Paid link &middot; {esc(AMAZON_NOTE)}</p>
  </div>
</article>"""


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

    hero = f"""<section class="hero">
  <div class="hero-media">
    <img src="{esc(rel(d, 'assets/img/hero-counter-w1280.jpg'))}"
         srcset="{esc(rel(d, 'assets/img/hero-counter-w760.jpg'))} 760w, {esc(rel(d, 'assets/img/hero-counter-w1280.jpg'))} 1280w"
         sizes="100vw" alt="An unbranded air fryer on a wooden kitchen counter in morning light, with lemons, salt and thyme" fetchpriority="high" decoding="async">
    <span class="hero-illus">Illustration</span>
  </div>
  <div class="wrap hero-inner">
    <div class="hero-copy">
      {eyebrow('The kitchen edit · winter 2026')}
      <h1>Crisp, without<br><em>the guesswork.</em></h1>
      <p class="hero-dek">Five things worth putting on your counter, chosen for how you actually cook: two air fryers with one drawer, one with two, an oven with a door, and two probes that stop the guessing. Every listing opened and checked before it earned a place.</p>
      <p class="hero-actions">
        <a class="btn" href="{esc(rel(d, 'products/index.html'))}">Shop the edit</a>
        <a class="btn btn-ghost" href="{esc(rel(d, 'guides/index.html'))}">Find your shape</a>
      </p>
      <p class="hero-fine">Paid links. Prices live on Amazon, where they are always right.</p>
    </div>
  </div>
</section>

<div class="trust-row"><div class="wrap">
  <p><strong>5 of 5</strong> links opened and matched to a live listing on 20 Nov 2026</p>
  <p><strong>0</strong> prices or ratings copied &mdash; Amazon serves those, not us</p>
  <p><strong>Every</strong> product link tagged, sponsored and disclosed</p>
</div></div>"""

    shop = section(f"""
<div class="sec-head">
  <div>{eyebrow('The edit')}<h2>Air fryers, by shape</h2></div>
  <p>Choose the shape first. Two drawers, one basket, or a door with racks inside &mdash; everything else follows.</p>
</div>
<div class="pcard-grid three">
{''.join(product_card(d, p) for p in air)}
</div>
<p class="sec-foot"><a class="tlink" href="{esc(rel(d, 'compare/index.html'))}">Compare all three side by side <span aria-hidden="true">&rarr;</span></a></p>""",
                    cls="shop")

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

    feature = GUIDES[7]
    feat_href = rel(d, f"guides/{feature['slug']}.html")
    seasonal = section(f"""
<div class="seasonal">
  <div class="seasonal-media">{img(d, feature['photo'], feature['photo_alt'], sizes='(max-width:820px) 100vw, 520px')}</div>
  <div class="seasonal-copy">
    {eyebrow('Seasonal · hosting')}
    <h2>{esc(feature['title'])}</h2>
    <p class="dek">{esc(feature['dek'])}</p>
    <p>Work backwards from the moment you sit down and give the air fryer the last twenty minutes, not the first two hours.</p>
    <a class="btn btn-small" href="{esc(feat_href)}">Read the hosting guide</a>
  </div>
</div>""", cls="seasonal-band")

    latest = section(f"""
<div class="sec-head">
  <div>{eyebrow('The journal')}<h2>Guides worth your ten minutes</h2></div>
  <p>Question-shaped, answer-first, and honest about what a listing can and cannot tell you.</p>
</div>
<div class="gcard-grid">
{''.join(guide_card(d, g) for g in GUIDES[:4])}
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
        description="Five Amazon picks for air frying, each link opened and matched to its live listing: two basket air fryers, one French-door oven and two meat thermometers. Paid links disclosed on every page.",
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
    doc = json.loads((root / "src/data/products.json").read_text(encoding="utf-8"))
    cats = doc["meta"].get("categories", [])
    out = []
    for c in cats:
        out.append({"id": c["id"], "label": c["label"], "blurb": c.get("blurb", ""),
                    "items": [by_ref[r] for r in c["refs"] if r in by_ref]})
    return out
