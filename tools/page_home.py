"""The front page. Leads with products and guides; the machinery lives in the footer."""

from layout import (DISCLOSURE, SITE_NAME, blank, esc, eyebrow, link, page,
                    product_link, rel, section, table)
from content import GUIDES


def img(page_dir, path, alt, *, sizes, cls="", loading="lazy"):
    return (
        f'<img class="{esc(cls)}" src="{esc(rel(page_dir, path + "-w900.jpg"))}" '
        f'srcset="{esc(rel(page_dir, path + "-w560.jpg"))} 560w, '
        f'{esc(rel(page_dir, path + "-w900.jpg"))} 900w" '
        f'sizes="{esc(sizes)}" alt="{esc(alt)}" loading="{esc(loading)}" decoding="async">'
    )



def build(d, products, meta):
    guide='guides/basket-or-oven-air-fryer.html'
    picks=[('Dual-basket air fryer','Chefman Dual Basket','Two separate baskets for the main and the side.','Air fryers','format-basket'),('Countertop oven','Emeril Lagasse French Door','Tray space for cooks who prefer an oven layout.','Ovens','format-oven'),('Single-basket air fryer','Chefman TurboFry','One roomy basket instead of a divided drawer.','Air fryers','hero-counter'),('Kitchen thermometer','ThermoMaven Digital','A handheld option for a quick spot check.','Thermometers','thermometer'),('Wireless thermometer','CHEF iQ Sense','A three-probe option for tracking different cuts.','Thermometers','thermometer')]
    cards=[]
    for p,(kind,name,dek,group,photo) in zip(products,picks):
        url=f"products/{p['ref'].lower()}.html"
        image=f'assets/img/{photo}-w'+('760' if photo=='hero-counter' else '560')+'.jpg'
        cards.append(f'''<article class="shop-card" data-group="{group}"><div class="shop-art"><a href="{url}" aria-label="Explore {name}"><img src="{image}" alt="{esc('Sage air fryer on a wooden kitchen counter' if photo=='hero-counter' else p['photo_alt'])}" loading="lazy"></a><button class="save-pick" data-id="{p['ref'].lower()}" data-name="{name}" aria-label="Save {name}" aria-pressed="false"><svg viewBox="0 0 24 24" width="17" height="18" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M6 4h12v17l-6-4-6 4z"/></svg></button><span class="art-label">FORMAT ILLUSTRATION</span></div><div class="shop-copy"><span class="rubric">{kind}</span><h3><a href="{url}">{name}</a></h3><p>{dek}</p><a class="ink-link" href="{url}">Explore product →</a></div></article>''')
    articles=''.join(f'<a class="read-card" href="guides/{g["slug"]}.html"><img src="{g["photo"]}-w560.jpg" alt="{esc(g["photo_alt"])}" loading="lazy"><span class="rubric">{g["read_minutes"]} MIN READ</span><h3>{esc(g["title"])}</h3></a>' for g in GUIDES[1:4])
    body=f'''<div class="wrap front"><div class="editionline"><span><b></b> THE COUNTERTOP EDIT</span><span>VOL. 01 <i>/</i> NOVEMBER 2026</span></div>
<section class="cover"><div class="cover-copy"><div class="cover-rubric"><span>Cover story</span><small>BUYING GUIDE</small></div><h1>Air fryers,<br><em>without the fuss.</em></h1><p>Basket or oven? Start with what you cook, how much fits, and the space you actually have.</p><div class="cover-actions"><a href="{guide}">Read the guide <b>→</b></a><span>◷ &nbsp;{GUIDES[0]['read_minutes']} min read</span></div></div><div class="cover-art"><img src="assets/img/cover-air-fryer.jpg" alt="Sage air fryer with golden potato wedges on a sunlit kitchen counter" fetchpriority="high"><span class="figure-stamp">FIG. 01 &nbsp; / &nbsp; BASKET AIR FRYER · ILLUSTRATION</span></div></section>
<section class="shelf"><div class="rubric shelf-label">01 <i></i> THE SHOPPING LIST</div><div class="shelf-head"><div><h2>The countertop shortlist</h2><p>Five kitchen picks, with the details that matter before you buy.</p></div><a href="compare/index.html" class="ink-link compare-link">Compare products &nbsp;→</a></div><div class="filters" aria-label="Filter products">{''.join(f'<button type="button" aria-pressed="{str(i==0).lower()}" data-filter="{x}">{x}</button>' for i,x in enumerate(['All picks','Air fryers','Ovens','Thermometers']))}</div><div class="shop-grid">{''.join(cards)}</div></section>
<section class="shelf"><div class="rubric shelf-label">02 <i></i> FIELD NOTES</div><div class="shelf-head"><h2>Before you buy</h2><a class="ink-link" href="guides/index.html">All guides →</a></div><div class="shop-grid">{articles}</div></section><div class="follow"><div><span class="rubric">THE NEXT EDITION</span><h2>Keep up with the kitchen desk.</h2></div><a class="ink-link" href="feed.xml">Follow via RSS ↗</a></div><p class="photo-credit"><a class="ink-link" href="https://github.com/karagemop466-tech/Affil1/issues/new?title=Reader%20question" rel="noopener">Ask the kitchen desk ↗</a> · Public reader questions via GitHub. Please leave out personal details.</p><p class="photo-credit">Kitchen imagery is illustrative, not product photography.</p></div>'''
    return page(d,title='Crisp &amp; Counter — The Countertop Edit',description='Air fryer buying guides, countertop ovens and kitchen thermometers. Compare the details that matter for your kitchen.',body=body,canonical='')
