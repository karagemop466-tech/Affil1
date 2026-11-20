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


def build(page_dir, products, meta):
    d = page_dir
    guide = 'guides/basket-or-oven-air-fryer.html'
    seal = '''<svg viewBox="0 0 100 100" width="85" height="85" aria-hidden="true"><defs><path id="ring" d="M50 50m-34 0a34 34 0 1 1 68 0a34 34 0 1 1-68 0"/></defs><circle cx="50" cy="50" r="48" fill="#f4e6b2" stroke="#493c22"/><circle cx="50" cy="50" r="26" fill="none" stroke="#786a45"/><text fill="#493c22" font-size="9.6" letter-spacing="2.15"><textPath href="#ring">KITCHEN FIELD NOTES • C&amp;C • </textPath></text><path d="M41 55q4-19 19-20-1 16-17 19m-4 6 15-20" stroke="#493c22" stroke-width="2" fill="none"/></svg>'''
    hero = f'''<section class="cover"><div class="coverstory"><p class="editionkicker"><span></span> THE SEASONAL EDIT</p><h1>The countertop<br><em>edit.</em></h1><p class="coverdek">One basket, two drawers, or French doors? Find the right shape for your counter and the way you cook.</p>
    <div class="coveractions"><a class="coverbtn" href="{guide}">Read the guide <span>→</span></a><a href="#shelf">Browse the products ↓</a></div><div class="byline">By Crisp &amp; Counter <b>·</b> 7 min read</div></div>
    <div class="coverphoto"><img src="assets/img/hero-counter-w1280.jpg" srcset="assets/img/hero-counter-w760.jpg 760w, assets/img/hero-counter-w1280.jpg 1280w" sizes="(max-width:720px) 94vw, 55vw" alt="A sage-green air fryer beside cut lemons on a sunlit kitchen counter" fetchpriority="high"><div class="seal">{seal}</div><span class="figlabel">FIG. 01 &nbsp; / &nbsp; FORMAT ILLUSTRATION</span></div></section>'''
    tabs = '<div class="shelftabs" hidden aria-label="Filter products">'+''.join(f'<button data-filter="{key}" aria-pressed="false">{text}</button>' for key,text in [('air-fryers','Air fryers · 3'),('thermometers','Thermometers · 2'),('all','All five')])+'</div>'
    shelf = f'''<section class="shelf" id="shelf"><div class="division"><span>01</span> SHOP THE EDIT<i></i></div><div class="shelfhead"><h2>The kitchen shortlist</h2>{tabs}</div><div class="shelfgrid">{''.join(shelf_card(d,p) for p in products)}</div><p class="shelffoot">Format illustrations, not product photos. <a class="sourcenote" href="review/index.html#FLG-016">Thermometer destination note</a>. <a href="compare/index.html">Compare listings side by side →</a></p></section>'''
    stories = ''.join(f'''<a href="guides/{esc(g['slug'])}.html" class="storytile">{img(d,g['photo'],g['photo_alt'],sizes='(max-width:700px) 92vw, 27vw')}<div><small>{esc(g['kicker'])} &nbsp; / &nbsp; {g['read_minutes']} MIN</small><h3>{esc(g['title'])}</h3></div></a>''' for g in GUIDES)
    guides = f'''<section class="journal"><div class="division"><span>02</span> FROM THE JOURNAL<i></i></div><div class="shelfhead"><h2>Before you buy</h2><a class="textact" href="guides/index.html">All buying guides →</a></div><div class="journalgrid">{stories}</div></section><aside class="rsscall"><div><small>THE READING LIST</small><h2>Fresh notes from the counter.</h2></div><a href="feed.xml" class="textact">Follow via RSS →</a></aside>'''
    return page(d, title='Crisp & Counter — The Kitchen Journal', description='Find an air fryer that fits your dinner routine. Compare kitchen tools, explore the product shelf, and read practical buying guides.', active='index.html',body_class='home',body='<div class="wrap issue">'+hero+shelf+guides+'</div>', canonical='',structured={'@context':'https://schema.org','@type':'WebSite','name':SITE_NAME,'url':'https://karagemop466-tech.github.io/Affil1/'})
