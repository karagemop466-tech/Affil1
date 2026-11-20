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
    art, name, spec = {
        "P-01": ("dual", "Chefman Dual Basket", "6 qt · Two baskets"),
        "P-02": ("oven", "Emeril Lagasse French Door", "26 qt · Oven style"),
        "P-03": ("single", "Chefman TurboFry", "8 qt · Single basket"),
    }[p['ref']]
    return f"""<article class="edit-card" data-category="air-fryers">
  <a class="edit-art" href="{esc(href)}" aria-label="Read about {esc(name)}">
    <img src="{esc(rel(page_dir, 'assets/img/storefront-' + art + '-w900.jpg'))}" loading="lazy" alt="Editorial drawing of the {esc(p['format_label'])} format">
    <span class="folio">FIG. {esc(p['ref'][-2:])}</span><span class="art-note">Format illustration</span></a>
  <div class="edit-info"><span class="ink-label">{esc(spec)}</span>
    <h3><a href="{esc(href)}">{esc(name)}</a></h3><p>{esc(BUYER_NOTES[p['ref']])}</p>
    <a class="edit-more" href="{esc(href)}">Explore this format →</a> &nbsp; {product_link(page_dir, p['listing_url'], 'Amazon listing ↗', cls='tlink')}
  </div></article>"""


SHELF = {
    'P-01': ('Two baskets', 'Chefman Dual Basket', 'Two sides on the menu? Check each drawer against the portion you usually cook.'),
    'P-02': ('Countertop oven', 'Emeril Lagasse French Door', 'Before you make room for the oven, make room for the open doors.'),
    'P-03': ('Single basket', 'Chefman TurboFry', 'For a tray of wedges, the width of the basket matters as much as the quarts.'),
    'P-04': ('Instant-read', 'ThermoMaven Digital', 'Compare the grip, display and probe length for a quick check at the stove.'),
    'P-05': ('Wireless probe', 'CHEF iQ Sense', 'Want to step away from the roast? Check the phone and connection requirements first.'),
}


def shelf_card(d, p):
    tag, name, note = SHELF[p['ref']]
    category = 'thermometers' if p['ref'] in ('P-04','P-05') else 'air-fryers'
    dest = esc(rel(d, f"products/{p['ref'].lower()}.html"))
    photo = img(d, p['photo'], p['photo_alt'], sizes='(max-width:700px) 92vw, 32vw')
    if p['ref'] == 'P-03':
        photo = img(d, 'assets/img/capacity', 'An illustrated single-layer portion beside a tape measure', sizes='(max-width:700px) 92vw, 32vw')
    source = product_link(d, p["listing_url"], "Listing source ↗", cls="textact")
    return f'''<article class="shelfcard" data-category="{category}"><a class="shelfphoto" href="{dest}" aria-label="Read about {esc(name)}">{photo}<span>{esc(tag)}</span><small class="format-credit">Format illustration</small></a>
    <div class="shelfmeta">FIELD NOTE &nbsp; / &nbsp; {esc(p['ref'][-2:])}</div><h3><a href="{dest}">{esc(name)}</a></h3><p>{esc(note)}</p>
    <a class="textact" href="{dest}">Product details &rarr;</a> &nbsp; {source}</article>'''


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

    tabs = '<div class="shelftabs" hidden aria-label="Filter products">'+''.join(f'<button data-filter="{key}" aria-pressed="false">{text}</button>' for key,text in [('air-fryers','Air fryers · 3'),('thermometers','Thermometers · 2'),('all','All products')])+'</div>'
    shortlist = section(f"""<div class="edit-head" id="shelf"><div><p class="ink-label"><i></i> SHOP BY FORMAT</p>
      <h2>The countertop shortlist<span>.</span></h2></div>
      <a class="edit-all" href="{esc(rel(d,'products/index.html'))}">All products <span>→</span></a></div>
      {tabs}
      <div class="edit-grid">{''.join(product_card(d,p) for p in mains)}{''.join(shelf_card(d,p) for p in products if p["ref"] in ("P-04", "P-05"))}</div>""", cls="edit-shop", sid="shortlist")

    thermometer = f"""<section class="thermo-band"><div class="wrap thermo-inner">
  <div class="thermo-art">{img(d, 'assets/img/thermometer', 'A probe thermometer resting in a roasted chicken beside a small display unit', sizes='(max-width:720px) 100vw, 420px')}<span class="illus-tag">Illustration</span></div>
  <div class="thermo-copy">
    {eyebrow('Cooking tools')}
    <h2>Instant-read or wireless?</h2>
    <p>For a quick spot check, compare instant-read models. For monitoring while food cooks, check the wireless probe’s app and device requirements.</p>
    <p>These two submitted links have opened different listings across checks. <a class="tlink" href="{esc(rel(d, 'review/index.html'))}#FLG-016">See the destination notes →</a></p>
    <p class="thermo-actions"><a class="btn btn-light" href="{esc(rel(d, 'products/p-05.html'))}">CHEF iQ wireless details</a> <a class="btn btn-light" href="{esc(rel(d, 'products/p-04.html'))}">ThermoMaven instant-read details</a></p>
  </div>
</div></section>"""

    featured = [next(g for g in GUIDES if g['slug'] == slug) for slug in
                ('holiday-hosting', 'small-kitchen-counter', 'meal-prep-sunday', 'thermometer-pairing')]
    guides = section(f"""
<div class="sec-head">
  <div>{eyebrow('Buying guides')}<h2>Before you clear the counter</h2></div>
  <p>Use these checklists before you measure the counter, compare capacity or decide which features you’ll actually use.</p>
</div>
<div class="gcard-grid">
  {guide_card(d, featured[0], feature=True)}
  {''.join(guide_card(d, g) for g in featured[1:])}
</div>""", cls="guides", sid="guides")

    subscribe = section(f"""
<div class="sec-head"><div>{eyebrow('Keep reading')}<h2>Get new guides in your feed reader</h2></div>
<p><a class="tlink" href="{esc(rel(d, 'feed.xml'))}">Follow Crisp &amp; Counter via RSS &rarr;</a></p></div>""")
    body = "\n".join([hero, shortlist, thermometer, guides, subscribe])

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
