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
    ref = p['ref']
    href = rel(page_dir, f"products/{ref.lower()}.html")
    texts = {"P-01":("Two-basket cooking", "Chefman Dual Basket", "Two 3-quart baskets for a main and a side."),
             "P-02":("Oven-style cooking", "Emeril Lagasse French Door", "A 26-quart countertop oven. Check the tray size against your favourite pan."),
             "P-03":("Single-basket cooking", "Chefman TurboFry", "One 8-quart basket. Compare its cooking surface with your usual batch."),
             "P-04":("Spot checks", "ThermoMaven Instant Read", "For cooks who want to check a roast without pairing a phone."),
             "P-05":("Wireless monitoring", "CHEF iQ Sense", "Compare probe count and app requirements before you choose.")}
    label,title,note = texts[ref]
    photo, alt = (('assets/img/multifunction','A basket air fryer beside a countertop oven') if ref == 'P-03' else (p['photo'],p['photo_alt']))
    return f"""<article class="shelf-card" data-category="{'air' if ref in BUYER_NOTES else 'thermo'}"><a class="shelf-media" href="{href}" aria-label="{esc(title)} details">{img(page_dir,photo,alt,sizes='(max-width:720px) 100vw, 380px')}<span class="shelf-label">{esc(label)}</span><span class="art-credit">Illustration</span></a>
<div class="shelf-meta">SHOP NOTE &nbsp; / &nbsp; {ref[-2:]}</div><h3><a href="{href}">{esc(title)}</a></h3><p>{esc(note)}</p><a class="cover-link" href="{href}">View details →</a></article>"""


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

    hero = f"""<section class="cover wrap">
  <div class="cover-copy"><p class="edition"><span></span> THE SEASONAL EDIT <i>/</i> NO. 01</p>
    <h1>The countertop<br><em>edit.</em></h1>
    <p class="cover-dek">One basket, two baskets, or an oven? Find the air fryer that fits your counter and the way you cook.</p>
    <div class="cover-actions"><a class="btn" href="#compare">Shop the edit <b aria-hidden="true">→</b></a><a class="cover-link" href="{rel(d,'guides/basket-or-oven-air-fryer.html')}">Read the guide ↗</a></div>
  </div>
  <figure class="cover-image"><img src="assets/img/hero-counter-w1280.jpg" srcset="assets/img/hero-counter-w760.jpg 760w, assets/img/hero-counter-w1280.jpg 1280w" sizes="(max-width:720px) 100vw, 58vw" alt="Sage-green air fryer on a sunlit counter beside halved lemons" fetchpriority="high"><span class="cover-issue">✳ &nbsp; FALL / WINTER 2026</span><figcaption>FIG. 01 &nbsp; / &nbsp; THE AIR FRYER &nbsp; · &nbsp; ILLUSTRATION</figcaption></figure>
</section>"""

    paths = section(f"""
<div class="sec-head">
  <div>{eyebrow('Three ways in')}<h2>What’s holding up dinner?</h2></div>
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
    <p>A quart figure is a volume. You cook on a surface. Check the basket floor before buying.</p>
    <span class="tlink">Work out capacity <span aria-hidden="true">&rarr;</span></span>
  </a>
  <a class="path" href="{esc(rel(d, 'guides/cleanup-and-counter-space.html'))}">
    <span class="path-n">03</span><h2>I am worried it will end up in a cupboard</h2>
    <p>The parts you wash and the space it occupies decide whether you keep using it. Both are checkable in five minutes.</p>
    <span class="tlink">Check the everyday cost <span aria-hidden="true">&rarr;</span></span>
  </a>
</div>""", cls="paths")

    shortlist = section(f"""
<div class="shelf-heading"><div><p class="edition"><span></span> THE SHOP</p><h2>The kitchen shortlist</h2></div><a class="cover-link" href="{rel(d,'compare/index.html')}">Compare products →</a></div>
<div class="shelf-tabs" hidden aria-label="Product category"><button data-filter="air" aria-pressed="true">Air fryers <small>03</small></button><button data-filter="thermo" aria-pressed="false">Thermometers <small>02</small></button></div>
<div class="shelf-grid">{''.join(product_card(d,p) for p in products)}</div>""", cls="shop-section", sid="compare")

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
  <div>{eyebrow('Buying guides')}<h2>From the field guide</h2></div>
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
