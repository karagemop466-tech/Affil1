"""The front page. Leads with products and guides; the machinery lives in the footer."""

from layout import (SITE_NAME, esc, eyebrow, page, product_link, rel, section)
from content import GUIDES


def img(page_dir, path, alt, *, sizes, cls="", loading="lazy"):
    return (
        f'<img class="{esc(cls)}" src="{esc(rel(page_dir, path + "-w900.jpg"))}" '
        f'srcset="{esc(rel(page_dir, path + "-w560.jpg"))} 560w, '
        f'{esc(rel(page_dir, path + "-w900.jpg"))} 900w" '
        f'sizes="{esc(sizes)}" alt="{esc(alt)}" loading="{esc(loading)}" decoding="async">'
    )


BUYER_NOTES = {
    "P-01": "Cooking dinner and a side? Compare the size of each basket, not just their combined volume.",
    "P-02": "Want room for a tray? Check the usable rack dimensions and how far the doors swing.",
    "P-03": "Prefer one basket? Check whether your usual batch fits in a single layer.",
}


def product_card(page_dir, p):
    href = rel(page_dir, f"products/{p['ref'].lower()}.html")
    return f"""<article class="pcard">
  <div class="pcard-media">{img(page_dir, p['photo'], p['photo_alt'], sizes='(max-width:720px) 100vw, 350px')}
    <span class="illus-tag">Format illustration</span></div>
  <div class="pcard-body">
    <p class="pcard-ref">{esc(p['stated_capacity'])} &middot; seller-stated</p>
    <h3><a href="{esc(href)}">{esc(_short(p))}</a></h3>
    <p>{esc(BUYER_NOTES[p['ref']])}</p>
    <p class="pcard-actions"><a class="tlink" href="{esc(href)}">Product details &rarr;</a>
      {product_link(page_dir, p['listing_url'], 'Listing source &#8599;', cls='tlink tlink-sponsor')}</p>
  </div>
</article>"""


def _short(p):
    shape = p.get("format_label") or ""
    brand = p.get("brand") or ""
    return f"{brand} {shape}".strip()


def guide_card(page_dir, g, *, feature=False):
    href = rel(page_dir, f"guides/{g['slug']}.html")
    cls = "gcard gcard-feature" if feature else "gcard"
    return f"""<article class="{cls}">
  <a class="gcard-media" href="{esc(href)}" tabindex="-1" aria-hidden="true">
    {img(page_dir, g['photo'], g['photo_alt'], sizes='(max-width:720px) 100vw, 380px')}
  </a>
  <div class="gcard-body">
    <p class="gcard-kicker">{esc(g['kicker'])} &middot; {g['read_minutes']} min</p>
    <h3><a href="{esc(href)}">{esc(g['title'])}</a></h3>
    <p>{esc(g['dek'])}</p>
    <a class="tlink" href="{esc(href)}">Read <span aria-hidden="true">&rarr;</span></a>
  </div>
</article>"""


def build(page_dir, products, meta):
    d = page_dir
    by_ref = {p["ref"]: p for p in products}
    mains = [by_ref[r] for r in ("P-01", "P-02", "P-03")]

    hero = f"""<section class="hero">
  <div class="hero-media">
    <img src="{esc(rel(d, 'assets/img/hero-counter-w1280.jpg'))}"
         srcset="{esc(rel(d, 'assets/img/hero-counter-w760.jpg'))} 760w, {esc(rel(d, 'assets/img/hero-counter-w1280.jpg'))} 1280w"
         sizes="100vw" alt="An unbranded air fryer on a wooden kitchen counter in morning light, with lemons, salt and thyme" fetchpriority="high" decoding="async">
    <span class="hero-illus">Illustration</span>
  </div>
  <div class="wrap hero-inner">
    <div class="hero-copy">
      {eyebrow('The kitchen edit')}
      <h1>Find the air fryer<br><em>that fits.</em></h1>
      <p class="hero-dek">One basket, two baskets or a countertop oven? Start with what you cook, how much counter space you have, and what you want to wash afterward.</p>
      <p class="hero-actions">
        <a class="btn" href="#compare">See the shortlist</a>
        <a class="btn btn-ghost" href="{esc(rel(d, 'guides/index.html'))}">Start with a guide</a>
      </p>
      <p class="hero-fine">Listing-based comparisons, not hands-on reviews.</p>
    </div>
  </div>
</section>"""

    paths = section(f"""
<div class="sec-head">
  <div>{eyebrow('Three ways in')}<h2>Start from the decision you are actually facing</h2></div>
  <p>Most air-fryer advice starts with a product. These start with the thing that is making the choice hard.</p>
</div>
<div class="path-grid">
  <a class="path" href="{esc(rel(d, 'guides/basket-or-oven-air-fryer.html'))}">
    <span class="path-n">01</span><h2>I do not know which shape I want</h2>
    <p>Basket or oven changes how often you intervene, how much door space you need, and what you can put inside.</p>
    <span class="tlink">Compare the shapes <span aria-hidden="true">&rarr;</span></span>
  </a>
  <a class="path" href="{esc(rel(d, 'guides/air-fryer-capacity-checklist.html'))}">
    <span class="path-n">02</span><h2>I cannot tell if it is big enough</h2>
    <p>A quart figure is a volume. You cook on a surface. Here is how to convert one into the other before you buy.</p>
    <span class="tlink">Work out capacity <span aria-hidden="true">&rarr;</span></span>
  </a>
  <a class="path" href="{esc(rel(d, 'guides/cleanup-and-counter-space.html'))}">
    <span class="path-n">03</span><h2>I am worried it will end up in a cupboard</h2>
    <p>The parts you wash and the space it occupies decide whether you keep using it. Both are checkable in five minutes.</p>
    <span class="tlink">Check the everyday cost <span aria-hidden="true">&rarr;</span></span>
  </a>
</div>""", cls="paths")

    shortlist = section(f"""
<div class="sec-head">
  <div>{eyebrow('The shortlist')}<h2>Three air fryer formats to compare</h2></div>
  <p>Start with the format that matches your weeknight cooking, then check the details before buying.</p>
</div>
<div class="pcard-grid wide">
  {''.join(product_card(d, p) for p in mains)}
</div>
<p class="sec-foot"><a href="{esc(rel(d, 'compare/index.html'))}">Compare the formats side by side &rarr;</a></p>""", cls="shortlist", sid="compare")

    thermometer = f"""<section class="thermo-band"><div class="wrap thermo-inner">
  <div class="thermo-art">{img(d, 'assets/img/thermometer', 'A probe thermometer resting in a roasted chicken beside a small display unit', sizes='(max-width:720px) 100vw, 420px')}<span class="illus-tag">Illustration</span></div>
  <div class="thermo-copy">
    {eyebrow('Cooking tools')}
    <h2>Instant-read or wireless?</h2>
    <p>For a quick spot check, compare instant-read models. For monitoring while food cooks, check the wireless probe’s app and device requirements.</p>
    <p class="thermo-actions"><a class="btn btn-light" href="{esc(rel(d, 'products/p-05.html'))}">CHEF iQ wireless details</a> <a class="btn btn-light" href="{esc(rel(d, 'products/p-04.html'))}">ThermoMaven instant-read details</a></p>
  </div>
</div></section>"""

    guides = section(f"""
<div class="sec-head">
  <div>{eyebrow('Buying guides')}<h2>Written to be useful before you click</h2></div>
  <p>Use these checklists before you measure the counter, compare capacity or decide which features you’ll actually use.</p>
</div>
<div class="gcard-grid">
  {guide_card(d, GUIDES[0], feature=True)}
  {''.join(guide_card(d, g) for g in GUIDES[1:])}
</div>""", cls="guides", sid="guides")

    subscribe = section(f"""
<div class="sec-head"><div>{eyebrow('Keep reading')}<h2>Get new guides in your feed reader</h2></div>
<p><a class="tlink" href="{esc(rel(d, 'feed.xml'))}">Follow Crisp &amp; Counter via RSS &rarr;</a></p></div>""")
    body = "\n".join([hero, shortlist, guides, paths, thermometer, subscribe])

    structured = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": "https://karagemop466-tech.github.io/Affil1/",
        "description": "Kitchen buying guides for air fryers and cooking thermometers, with product identities checked against the live Amazon listing.",
    }

    return page(
        d,
        title="Crisp & Counter \u2014 Air Fryer Comparisons & Buying Guides",
        description="Compare single-basket, dual-basket and countertop oven air fryers. Get practical buying guides on capacity, counter space and cleanup.",
        body=body,
        active="index.html",
        canonical="",
        body_class="home",
        structured=structured,
    )
