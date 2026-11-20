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


BUYER_NOTES = {
    "P-01": "Two baskets, three quarts each. Cook the main and the side at the same time, or finish them together with sync finish.",
    "P-02": "A glass-front countertop oven that air-fries. Buy it if you want to put a tray, a pan or a plate inside, not loose food.",
    "P-03": "One deep 8-quart basket. Buy it if your usual meal fits in a single layer and you would rather have fewer parts to wash.",
    "P-04": "An instant-read probe that swings between the display and the point of the meat. The lowest-commitment way to stop guessing whether dinner is done.",
    "P-05": "Probes that stay in the meat while it cooks, so you can walk away and come back to a number rather than an anxiety.",
}

# Every card says what the product is *for*, because that is the only kind of
# claim this site is allowed to make about a product it has not used.
USE_TAG = {
    "P-01": "Cooking a main and a side",
    "P-02": "Trays, pans and family portions",
    "P-03": "One big batch, one basket",
    "P-04": "Checking that it is done",
    "P-05": "Walking away while it cooks",
}


def product_card(page_dir, p, *, wide=False):
    href = rel(page_dir, f"products/{p['ref'].lower()}.html")
    note = BUYER_NOTES.get(p["ref"], "")
    use = USE_TAG.get(p["ref"], "")
    return f"""<article class="pcard">
  <div class="pcard-media">{img(page_dir, p['photo'], p['photo_alt'], sizes='(max-width:720px) 100vw, 350px')}
    <span class="illus-tag">Illustration</span></div>
  <div class="pcard-body">
    <p class="pcard-ref">{esc(use)}</p>
    <h3><a href="{esc(href)}">{esc(_short(p))}</a></h3>
    <p class="pcard-use">{esc(note)}</p>
    <dl class="pcard-specs">
      <div><dt>Format</dt><dd>{esc(p['format_label'])}</dd></div>
      <div><dt>Seller states</dt><dd>{esc(p['stated_capacity'].replace('Not applicable &mdash; it is a thermometer', 'No capacity — a thermometer').replace('Not applicable', '—'))}</dd></div>
      <div><dt>Price</dt><dd>Not shown — no live Amazon feed</dd></div>
    </dl>
    <p class="pcard-actions">
      <a class="btn btn-small" href="{esc(href)}">What to check</a>
      {product_link(page_dir, p['special_link'], 'View on Amazon &#8599;', cls='tlink tlink-sponsor')}
    </p>
    <p class="paid-note">Paid link. {esc('As an Amazon Associate I earn from qualifying purchases.')}</p>
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
    hero_product = by_ref["P-01"]

    hero = f"""<section class="hero">
  <div class="hero-media">
    <img src="{esc(rel(d, 'assets/img/hero-counter-w1280.jpg'))}"
         srcset="{esc(rel(d, 'assets/img/hero-counter-w760.jpg'))} 760w, {esc(rel(d, 'assets/img/hero-counter-w1280.jpg'))} 1280w"
         sizes="100vw" alt="An unbranded air fryer on a wooden kitchen counter in morning light, with lemons, salt and thyme" fetchpriority="high" decoding="async">
    <span class="hero-illus">Illustration</span>
  </div>
  <div class="wrap hero-inner">
    <div class="hero-copy">
      {eyebrow('The countertop edit')}
      <h1>Five kitchen tools<br><em>worth the counter space.</em></h1>
      <p class="hero-dek">Two air fryers that cook differently, one oven that fries, and two ways to stop guessing whether dinner is done. Start with the job you actually do on a Tuesday.</p>
      <p class="hero-actions">
        <a class="btn" href="#shop">Shop all five</a>
        <a class="btn btn-ghost" href="{esc(rel(d, 'guides/index.html'))}">Read the guides</a>
      </p>
      <p class="hero-fine">No prices shown: Amazon only permits them when Amazon serves the data. Links are paid, and the price you pay is the same whether you use one or not.</p>
    </div>
  </div>
</section>"""

    # Shop by the decision, not by the product. This is the section that makes
    # the site read like a shop rather than an audit: what the shopper is
    # trying to do comes first, the product follows.
    paths = section(f"""
<div class="sec-head">
  <div>{eyebrow('Shop by what you cook')}<h2>Start with the job, not the brand</h2></div>
  <p>Most people do not want an air fryer. They want dinner to be easy on a Wednesday. Pick the sentence that sounds like your week.</p>
</div>
<div class="path-grid">
  <a class="path" href="{esc(rel(d, 'products/p-01.html'))}">
    <span class="path-n">01</span><h2>A main and a side, at once</h2>
    <p>Two baskets that run separately, so the chicken and the potatoes finish when you want them to. Six quarts in total, three each.</p>
    <span class="tlink">See the dual-basket pick <span aria-hidden="true">&rarr;</span></span>
  </a>
  <a class="path" href="{esc(rel(d, 'products/p-02.html'))}">
    <span class="path-n">02</span><h2>Trays, pans, and four plates</h2>
    <p>A French-door countertop oven with an air-fry setting. The right shape if you bake, reheat plated food or cook for a family.</p>
    <span class="tlink">See the oven pick <span aria-hidden="true">&rarr;</span></span>
  </a>
  <a class="path" href="{esc(rel(d, 'products/p-03.html'))}">
    <span class="path-n">03</span><h2>One big batch, one basket</h2>
    <p>Eight quarts in a single drawer and fewer pieces to wash. The simplest machine here, and the one that ends up staying on the counter.</p>
    <span class="tlink">See the single-basket pick <span aria-hidden="true">&rarr;</span></span>
  </a>
  <a class="path" href="{esc(rel(d, 'products/p-04.html'))}">
    <span class="path-n">04</span><h2>Not guessing if it is done</h2>
    <p>A probe tells you the internal temperature. The USDA publishes the numbers to aim for, and we link them rather than making them up.</p>
    <span class="tlink">See the thermometer pick <span aria-hidden="true">&rarr;</span></span>
  </a>
</div>""", cls="paths")

    shop = section(f"""
<div class="sec-head">
  <div>{eyebrow('The shortlist')}<h2>All five, and what each one is for</h2></div>
  <p>Every card answers three questions: what job it is for, what the seller states, and what this site could not verify. Nothing is ranked.</p>
</div>
<div class="pcard-grid wide">
  {''.join(product_card(d, by_ref[r], wide=True) for r in ('P-01', 'P-02', 'P-03'))}
</div>
<p class="sec-foot"><a class="tlink" href="{esc(rel(d, 'products/index.html'))}">Open the full register &rarr;</a> <span class="sec-foot-note">Five products, no ranking, no invented prices.</span></p>""", cls="shop", sid="shop")

    thermometer = f"""<section class="thermo-band"><div class="wrap thermo-inner">
  <div class="thermo-art">{img(d, 'assets/img/thermometer', 'A probe thermometer resting in a roasted chicken beside a small display unit', sizes='(max-width:720px) 100vw, 420px')}<span class="illus-tag">Illustration</span></div>
  <div class="thermo-copy">
    {eyebrow('Cooking tools')}
    <h2>Instant-read, or leave it in?</h2>
    <p>One probe you move from piece to piece and read in a second. One set of probes that stays in the meat and reports back while you do something else. Different jobs; both beat cutting into the chicken to see.</p>
    <p class="thermo-safe">Both are for the same question, and the answer is published by the USDA: poultry to <strong>165&nbsp;&deg;F</strong> (73.9&nbsp;&deg;C), ground meat to <strong>160&nbsp;&deg;F</strong> (71.1&nbsp;&deg;C), and steaks, chops and roasts to <strong>145&nbsp;&deg;F</strong> (62.8&nbsp;&deg;C) with a three-minute rest. <a href="https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart" rel="noopener" target="_blank">USDA Food Safety and Inspection Service &#8599;</a></p>
    <p class="thermo-actions"><a class="btn btn-light" href="{esc(rel(d, 'products/p-04.html'))}">The instant-read thermometer</a> <a class="btn btn-light" href="{esc(rel(d, 'products/p-05.html'))}">The leave-in thermometer</a></p>
  </div>
</div></section>"""

    guides = section(f"""
<div class="sec-head">
  <div>{eyebrow('The guides')}<h2>Ten minutes now, one receipt later</h2></div>
  <p>Written as checklists, because a checklist is the honest form for advice from people who have not used the products. Every guide ends with a decision you can act on.</p>
</div>
<div class="gcard-grid">
  {guide_card(d, GUIDES[0], feature=True)}
  {''.join(guide_card(d, g) for g in GUIDES[1:3])}
</div>
<p class="sec-foot"><a class="tlink" href="{esc(rel(d, 'guides/index.html'))}">Every guide &rarr;</a></p>""", cls="guides", sid="guides")

    trust = section(f"""
<div class="sec-head"><div>{eyebrow('How this shop works')}<h2>Four things that are true here, and one that is not</h2></div></div>
<div class="rule-grid">
  <div class="rule"><span class="rule-n">01</span><h3>Every link is a paid link</h3><p>Marked <code class="code">rel="sponsored"</code>, tagged, and disclosed above the masthead on every page. The price you pay is the same either way.</p></div>
  <div class="rule"><span class="rule-n">02</span><h3>No prices and no ratings</h3><p>Amazon permits them only when Amazon serves the data. It does not here, so they are absent. A price copied from a listing in April is a wrong price by June.</p></div>
  <div class="rule"><span class="rule-n">03</span><h3>Nothing was tested</h3><p>No product was bought, cooked with or measured. Seller claims are labelled &ldquo;seller-stated&rdquo; wherever they appear. Independent numbers are cited to the agency that published them.</p></div>
  <div class="rule"><span class="rule-n">04</span><h3>Nothing is ranked without evidence</h3><p>There is no winner, no &ldquo;best overall&rdquo; and no numbered top five. What the site offers is a shorter path to the right decision, not a verdict.</p></div>
</div>
<p class="rule-cost">The one thing that is not true yet: whether clicks are credited to this site&rsquo;s tracking ID has not been confirmed in the Associates report. It is recorded openly, with the date, on the <a href="{esc(rel(d, 'review/index.html'))}#FLG-002">review queue</a>.</p>""", cls="rules")

    subscribe = section(f"""
<div class="sec-head"><div>{eyebrow('Keep reading')}<h2>New guides, without an email address</h2></div>
<p>The feed carries every new guide and nothing else. No account, no newsletter, no pop-up.</p></div>
<p class="subscribe-row"><a class="btn" href="{esc(rel(d, 'feed.xml'))}">Follow via RSS</a> <a class="tlink" href="{esc(rel(d, 'questions/index.html'))}">Or send in a question &rarr;</a></p>""", cls="subscribe")

    body = "\n".join([hero, shop, paths, guides, thermometer, trust, subscribe])

    structured = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": "https://karagemop466-tech.github.io/Affil1/",
        "description": "A short buyer's guide to five countertop kitchen appliances, with seller-stated specifications and no invented prices.",
    }

    return page(
        d,
        title="Crisp & Counter \u2014 five kitchen tools worth the counter space",
        description="Two air fryers, a French-door air-fryer oven and two meat thermometers, each with the seller's stated specs, what to check before buying, and no invented prices or ratings.",
        body=body,
        active="index.html",
        canonical="",
        body_class="home",
        structured=structured,
    )
