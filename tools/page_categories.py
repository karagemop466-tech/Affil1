"""Category pages: a place to browse from, generated from the same register.

A shop needs a shelf. These pages exist so a reader who arrives from search on
"air fryer oven" or "meat thermometer" lands somewhere that lists the products
in that category rather than on a general front page.

Every product fact here is read from src/data/products.json, so a category page
cannot contradict a product record. Nothing is added by hand.
"""

from layout import (DISCLOSURE, esc, eyebrow, page, pagehead, product_link,
                    rel, section, table)
from page_home import img

CATEGORIES = [
    {
        "slug": "air-fryers",
        "label": "Air fryers",
        "refs": ["P-01", "P-02", "P-03"],
        "kicker": "Air fryers",
        "title": "Three air fryers, three different shapes",
        "dek": "A dual basket, a French-door oven and a single deep drawer. The shape decides how you cook far more than the quart figure does.",
        "intro": [
            "Every air fryer moves hot air over food. What changes between these three is the container the food sits in, and that change is bigger than any difference in badge or wattage.",
            "A dual basket lets you run two jobs at once and wash four pieces afterwards. A single deep basket is the simplest machine here and the easiest to live with if your meals fit in one layer. A countertop oven with an air-fry setting is the only one of the three that accepts a tray, a pan or a plate, which is what makes it useful for baking and reheating as well as frying.",
        ],
        "decision": [
            ("Do you cook two different things at once?", "Then a second basket earns its keep. If the two things need different temperatures, one basket means two sessions."),
            ("Do you want to put a dish inside?", "Only the oven shape takes a tray or a plate. A deep drawer takes loose food."),
            ("How much counter and door room do you have?", "Measure the space with the drawer open or the door swung. That is the footprint, not the closed dimensions."),
        ],
        "guides": [
            ("guides/basket-or-oven-air-fryer.html", "Basket or oven-style air fryer: what should you compare?"),
            ("guides/air-fryer-capacity-checklist.html", "A no-hype checklist for comparing air-fryer capacity"),
        ],
    },
    {
        "slug": "thermometers",
        "label": "Meat thermometers",
        "refs": ["P-04", "P-05"],
        "kicker": "Meat thermometers",
        "title": "Two thermometers, and the numbers worth aiming for",
        "dek": "An instant-read probe you move from piece to piece, and a leave-in set that reports while you do something else. Both answer the same question.",
        "intro": [
            "The question a thermometer answers is not whether the food looks done. It is what the internal temperature is, measured at the thickest part, away from bone and fat. The USDA publishes the minimums, and they are the only numbers on this site quoted as fact rather than as a seller's claim.",
            "The choice between these two is about how you cook. A probe you move is right when you are standing at the pan. A set that stays in is right when the food goes into an oven, a smoker or an air fryer and you would rather not open the door to check.",
        ],
        "decision": [
            ("Will you be standing there?", "If yes, an instant-read is faster to use and cheaper to own."),
            ("Does the food cook behind a closed door?", "Then a leave-in probe avoids opening the oven and losing heat, which is the main practical argument for it."),
            ("Do you need more than one reading at once?", "A joint and a bird, or four steaks, need more than one probe or more than one check."),
        ],
        "guides": [
            ("guides/thermometer-pairing.html", "How to pair a thermometer with an air fryer"),
            ("guides/multi-function-kitchen-appliance-questions.html", "Questions to ask before buying a multi-function kitchen appliance"),
        ],
        "temps": True,
    },
]


SAFE_TEMPS = [
    ["All poultry, including ground poultry and stuffing", "165&nbsp;&deg;F (73.9&nbsp;&deg;C)", "&mdash;"],
    ["Ground meats", "160&nbsp;&deg;F (71.1&nbsp;&deg;C)", "&mdash;"],
    ["Beef, pork, veal and lamb steaks, chops and roasts", "145&nbsp;&deg;F (62.8&nbsp;&deg;C)", "At least 3 minutes"],
    ["Fish and shellfish", "145&nbsp;&deg;F (62.8&nbsp;&deg;C)", "&mdash;"],
    ["Leftovers and casseroles", "165&nbsp;°F (73.9&nbsp;°C)", "&mdash;"],
]

TEMP_NOTE = ('Source: <a href="https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/'
             'food-safety-basics/safe-temperature-chart" rel="noopener" target="_blank">USDA Food Safety '
             'and Inspection Service, Safe Minimum Internal Temperature Chart</a>, last updated '
             '14 April 2025. Quoted, not paraphrased.')


def _card(d, p):
    href = rel(d, "products/%s.html" % p["ref"].lower())
    return f"""<article class="pcard">
  <div class="pcard-media">{img(d, p['photo'], p['photo_alt'], sizes='(max-width:720px) 100vw, 350px')}<span class="illus-tag">Illustration</span></div>
  <div class="pcard-body">
    <p class="pcard-ref">{esc(p['format_label'])}</p>
    <h3><a href="{esc(href)}">{esc(p['brand'])} {esc(p['format_label'])}</a></h3>
    <dl class="pcard-specs">
      <div><dt>Seller states</dt><dd>{esc(p['stated_capacity'])}</dd></div>
      <div><dt>ASIN reached</dt><dd><code class="code">{esc(p['observed_asin'])}</code></dd></div>
      <div><dt>Price</dt><dd>Not shown &mdash; no live Amazon feed</dd></div>
    </dl>
    <p class="pcard-actions"><a class="btn btn-small" href="{esc(href)}">What to check</a>
      {product_link(d, p['special_link'], 'Amazon &#8599;', cls='tlink tlink-sponsor')}</p>
    <p class="paid-note">Paid link. {esc(DISCLOSURE)}</p>
  </div></article>"""


def build(page_dir, products, meta):
    """Emit one page per category. Returns [(path, html)]."""
    by_ref = {p["ref"]: p for p in products}
    out = []
    for c in CATEGORIES:
        d = page_dir
        items = [by_ref[r] for r in c["refs"] if r in by_ref]
        intro = "".join("<p>%s</p>" % esc(t) for t in c["intro"])
        decision = "".join(
            "<div><dt>%s</dt><dd>%s</dd></div>" % (esc(q), esc(a)) for q, a in c["decision"]
        )
        temps = ""
        if c.get("temps"):
            temps = f"""
    <h2>What to aim for</h2>
    <p class="lede">Measured with a food thermometer at the thickest part, before the food leaves the heat. The USDA calls these minimums; you may prefer higher.</p>
    {table(['Food', 'Minimum internal temperature', 'Rest'], SAFE_TEMPS, cls='temps', note=TEMP_NOTE)}
    <p class="fineprint">No thermometer on this site was checked against a reference instrument. The manufacturer's calibration instructions are more useful than any claim on these pages.</p>
"""
        guide_links = "".join(
            '<li><a href="%s">%s</a></li>' % (esc(rel(d, t)), esc(label))
            for t, label in c["guides"]
        )
        body = f"""{pagehead(
            c['kicker'],
            esc(c['title']),
            esc(c['dek']),
            meta='%d products &middot; nothing tested &middot; no prices shown' % len(items),
        )}
{section(f'''
<div class="article-grid">
  <div class="article">
    {intro}
    <h2>What actually decides it</h2>
    <dl class="checks">{decision}</dl>
    {temps}
  </div>
  <aside class="article-side">
    <nav class="toc" aria-label="In this category"><h2>In this category</h2>
      <ol>{''.join('<li><a href="%s">%s</a></li>' % (esc(rel(d, 'products/%s.html' % p['ref'].lower())), esc(p['brand'] + ' ' + p['format_label'])) for p in items)}</ol>
    </nav>
    <div class="side-card">
      <h2>Read next</h2>
      <ul class="side-links">{guide_links}</ul>
    </div>
    <div class="side-card side-card-quiet">
      <h2>The limit, stated once</h2>
      <p>No product here was bought, used or measured. Everything in the specification columns is the seller's own wording. The guides tell you what to check; they cannot tell you that a model passed.</p>
    </div>
  </aside>
</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The shelf')}<h2>{len(items)} products in {esc(c['label'].lower())}</h2></div>
<p>Each card leads to a record with the seller's claims, the numbers this page can support, and every field left blank.</p></div>
<div class="pcard-grid wide">{''.join(_card(d, p) for p in items)}</div>''', cls='section-tint')}
{section(f'''
<p class="fineprint">{esc(DISCLOSURE)} Every Amazon link above is a paid link and is marked sponsored. No price appears because Amazon does not serve one to this site.</p>''', cls='')}"""
        html = page(
            d,
            title="%s \\u2014 Crisp & Counter" % c["label"],
            description="%s. Seller-stated specifications, what to check before buying, and no invented prices." % c["dek"],
            body=body,
            active="categories/%s.html" % c["slug"],
            canonical="categories/%s.html" % c["slug"],
        )
        out.append(("categories/%s.html" % c["slug"], html))
    return out
