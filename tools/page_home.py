"""The front page. Leads with products organized by category and buying guides;
the verification machinery and desk surfaces live in the footer and a single nav group."""

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


def product_card(page_dir, p, *, compact=False, dark=False):
    href = rel(page_dir, f"products/{p['ref'].lower()}.html")
    if p["identity_confidence"] == "unresolved":
        return f"""<article class="pcard pcard-unresolved">
  <div class="pcard-media pcard-media-empty"><span>Not identified</span></div>
  <div class="pcard-body">
    <p class="pcard-ref">{esc(p['ref'])} &middot; unresolved</p>
    <h3>This link did not open a product page</h3>
    <p class="pcard-note">No product has been guessed to fill the gap.</p>
    <p class="pcard-actions"><a class="tlink" href="{esc(href)}">What is known <span aria-hidden="true">&rarr;</span></a></p>
  </div>
</article>"""

    media = (
        f'<div class="pcard-media">{img(page_dir, p["photo"], p["photo_alt"], sizes="(max-width:720px) 100vw, 340px")}'
        f'<span class="illus-tag">Illustration</span></div>'
    )
    attrs = "".join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in _specs(p))
    card_cls = "pcard pcard-dark" if dark else "pcard"
    if compact:
        body = f"""<div class="pcard-body">
    <p class="pcard-ref">{esc(p['ref'])} &middot; {esc(p['brand'])}</p>
    <h3><a href="{esc(href)}">{esc(_short(p))}</a></h3>
    <p class="pcard-actions"><a class="tlink" href="{esc(href)}">Read the record <span aria-hidden="true">&rarr;</span></a>
    {product_link(page_dir, p['listing_url'], 'See listing <span aria-hidden="true">&#8599;</span>', cls='tlink tlink-sponsor', aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")}</p>
    <p class="pcard-fine">Paid link &middot; Not tested &middot; No price or rating shown.</p>
  </div>"""
    else:
        body = f"""<div class="pcard-body">
    <p class="pcard-ref">{esc(p['ref'])} &middot; {esc(p.get('category_label') or '')} &middot; checked {esc(p['checked_on'])}</p>
    <h3><a href="{esc(href)}">{esc(_short(p))}</a></h3>
    <dl class="pcard-specs">{attrs}</dl>
    <p class="pcard-actions"><a class="tlink" href="{esc(href)}">Read the record <span aria-hidden="true">&rarr;</span></a>
    {product_link(page_dir, p['listing_url'], 'See listing <span aria-hidden="true">&#8599;</span>', cls='tlink tlink-sponsor', aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")}</p>
    <p class="pcard-fine">Paid link. Not tested here; no price or rating is shown because no permitted live Amazon feed is connected.</p>
  </div>"""
    return f'<article class="{card_cls}">{media}{body}</article>'


def _short(p):
    shape = p.get("format_label") or ""
    brand = p.get("brand") or ""
    return f"{brand} {shape}".strip()


def _specs(p):
    """Three factual lines from the verified listing, none repeating the heading."""
    rows = []
    cap = p.get("stated_capacity")
    if cap and not cap.lower().startswith("not applicable"):
        rows.append(("Stated size", cap))
    elif p.get("observed_asin"):
        rows.append(("Listing ASIN", p["observed_asin"]))
    attrs = p.get("stated_attributes")
    if attrs:
        first = attrs.split(";")[0].strip()
        rows.append(("Seller notes", first))
    rows.append(("Tested here", "No"))
    return rows


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
    <a class="tlink" href="{esc(href)}">Read guide <span aria-hidden="true">&rarr;</span></a>
  </div>
</article>"""


def build(page_dir, products, meta):
    d = page_dir
    air_fryers = [p for p in products if p.get("category") == "air-fryers"]
    thermometers = [p for p in products if p.get("category") == "thermometers"]

    hero = f"""<section class="hero">
  <div class="hero-media">
    <img src="{esc(rel(d, 'assets/img/hero-counter-w1280.jpg'))}"
         srcset="{esc(rel(d, 'assets/img/hero-counter-w760.jpg'))} 760w, {esc(rel(d, 'assets/img/hero-counter-w1280.jpg'))} 1280w"
         sizes="100vw" alt="An unbranded air fryer on a wooden kitchen counter in morning light, with lemons, salt and thyme" fetchpriority="high" decoding="async">
    <span class="hero-illus">Illustration</span>
  </div>
  <div class="wrap hero-inner">
    <div class="hero-copy">
      {eyebrow('The kitchen edit · 5 verified listings')}
      <h1>Buy once.<br><em>Cook better.</em></h1>
      <p class="hero-dek">Three air fryers and two meat thermometers &mdash; all five links opened and verified against Amazon on 20 November 2026, paired with plain buying guides on shape, capacity, cleanup and USDA safe internal temperatures.</p>
      <p class="hero-actions">
        <a class="btn" href="#air-fryers">Browse air fryers</a>
        <a class="btn btn-ghost" href="#thermometers">Meat thermometers</a>
        <a class="btn btn-ghost" href="{esc(rel(d, 'guides/index.html'))}">Read the guides</a>
      </p>
      <p class="hero-fine">No invented prices, star counts or test verdicts. Amazon permits live price and availability only from Amazon-served data or its API. <a href="{esc(rel(d, 'about/index.html'))}#why-blank">Why those fields stay blank</a>.</p>
    </div>
  </div>
</section>"""

    shortlist = section(f"""
<div class="sec-head">
  <div>{eyebrow('Category 01 · Air Fryers')}<h2>Three countertop formats, side by side</h2></div>
  <p>A 6-quart dual-basket drawer, a 26-quart French-door oven, and an 8-quart single basket &mdash; each linked directly to its verified Amazon listing.</p>
</div>
<div class="pcard-grid pcard-grid-3">
  {''.join(product_card(d, p) for p in air_fryers)}
</div>
<p class="sec-foot"><a href="{esc(rel(d, 'products/air-fryers.html'))}">Open the Air Fryers category page &rarr;</a> &middot; <a href="{esc(rel(d, 'compare/index.html'))}">Compare all five side by side</a> &middot; <a href="{esc(rel(d, 'products/index.html'))}">Full product-intent register</a>.</p>""", cls="shortlist", sid="air-fryers")

    thermometer = f"""<section class="thermo-band thermo-showcase" id="thermometers"><div class="wrap">
  <div class="sec-head sec-head-dark">
    <div>{eyebrow('Category 02 · Meat Thermometers')}<h2>Two ways to stop guessing when dinner is done</h2></div>
    <p>Two of the five submitted links resolve to Amazon&rsquo;s <em>Thermometers &amp; Timers &gt; Meat</em> category: one instant-read handheld probe and one leave-in three-probe wireless kit.</p>
  </div>
  <div class="pcard-grid wide">
    {''.join(product_card(d, p, dark=True) for p in thermometers)}
  </div>
  <p class="thermo-foot">
    <a class="btn btn-light" href="{esc(rel(d, 'products/thermometers.html'))}">Meat Thermometers category</a>
    <a class="btn btn-dark-ghost" href="{esc(rel(d, 'guides/instant-read-vs-wireless-meat-thermometer.html'))}">Instant-read vs. wireless + USDA chart</a>
  </p>
</div></section>"""

    paths = section(f"""
<div class="sec-head">
  <div>{eyebrow('Start from your question')}<h2>Four decisions that narrow the field fast</h2></div>
  <p>Good kitchen advice starts with the constraint on your counter &mdash; not a list of paid winners.</p>
</div>
<div class="path-grid path-grid-4">
  <a class="path" href="{esc(rel(d, 'guides/basket-or-oven-air-fryer.html'))}">
    <span class="path-n">01</span><h2>Basket or countertop oven?</h2>
    <p>How shape changes batch size, door clearance, shaking vs. flipping, and what pans fit inside.</p>
    <span class="tlink">Compare the shapes <span aria-hidden="true">&rarr;</span></span>
  </a>
  <a class="path" href="{esc(rel(d, 'guides/air-fryer-capacity-checklist.html'))}">
    <span class="path-n">02</span><h2>How big is big enough?</h2>
    <p>A quart figure is a volume. You cook on a surface. Convert your usual dinner into a real size.</p>
    <span class="tlink">Work out capacity <span aria-hidden="true">&rarr;</span></span>
  </a>
  <a class="path" href="{esc(rel(d, 'guides/instant-read-vs-wireless-meat-thermometer.html'))}">
    <span class="path-n">03</span><h2>Instant-read or wireless probe?</h2>
    <p>Spot-checking weeknight chicken vs. tracking a roast continuously &mdash; with the official USDA chart.</p>
    <span class="tlink">Compare thermometers <span aria-hidden="true">&rarr;</span></span>
  </a>
  <a class="path" href="{esc(rel(d, 'guides/cleanup-and-counter-space.html'))}">
    <span class="path-n">04</span><h2>Will it stay out or hit a cupboard?</h2>
    <p>Sink fit, washable piece count, and a five-minute counter tape test before you order.</p>
    <span class="tlink">Check everyday cost <span aria-hidden="true">&rarr;</span></span>
  </a>
</div>""", cls="paths section-tint")

    guides = section(f"""
<div class="sec-head">
  <div>{eyebrow('Buying guides · ' + str(len(GUIDES)) + ' articles')}<h2>Written to be useful before you click</h2></div>
  <p>Question-shaped guides across air fryers, meat thermometers, meal prep and holiday hosting. Every product claim is quoted from the seller; food-safety figures come straight from USDA FSIS.</p>
</div>
<div class="gcard-grid">
  {guide_card(d, GUIDES[0], feature=True)}
  {''.join(guide_card(d, g) for g in GUIDES[1:])}
</div>""", cls="guides")

    promise = section(f"""
<div class="sec-head">
  <div>{eyebrow('How this publication works')}<h2>Three rules, and what they cost</h2></div>
</div>
<div class="rule-grid">
  <div class="rule">
    <span class="rule-n">01</span>
    <h3>Every link is opened and separated</h3>
    <p>All five submitted short links were opened against Amazon and transcribed. Intended ASIN and observed redirect target stay in separate fields and are never merged.</p>
    <p class="rule-cost"><strong>The cost:</strong> intended ASINs stay blank until confirmed inside Associates Central.</p>
  </div>
  <div class="rule">
    <span class="rule-n">02</span>
    <h3>No price, no rating, no stars</h3>
    <p>Amazon&rsquo;s Program Policies allow price and availability only where Amazon serves them or they arrive through its API. Neither is connected, so neither appears.</p>
    <p class="rule-cost"><strong>The cost:</strong> product cards show facts without speculative prices.</p>
  </div>
  <div class="rule">
    <span class="rule-n">03</span>
    <h3>Nothing here was tested</h3>
    <p>No appliance or probe was bought or measured in a kitchen. Every photograph is a labelled illustration, and food-safety temperatures come solely from USDA FSIS.</p>
    <p class="rule-cost"><strong>The cost:</strong> these guides help you check &mdash; they never fake a verdict.</p>
  </div>
</div>
<p class="sec-foot">Every open uncertainty and compliance flag is published openly in <a href="{esc(rel(d, 'review/index.html'))}">Flagged for Review</a>.</p>""", cls="promise rules section-tint")

    dispatch = section(f"""
<div class="sec-head">
  <div>{eyebrow('Desk notes')}<h2>What was verified, and when</h2></div>
  <p>A dated receipt log. Affiliate pages age silently unless every check carries a date and a source.</p>
</div>
<ol class="dispatch">
  <li><time datetime="2026-11-20">20 Nov 2026</time><div><strong>All five submitted links verified (5 of 5).</strong> P-04 resolved on re-verification to ASIN <code class="code">B0DHZTCNR5</code> (ThermoMaven 1 Sec Digital Meat Thermometer), completing a two-category lineup of 3 Air Fryers and 2 Meat Thermometers. Earlier checkpoint gating stays documented in <a href="{esc(rel(d, 'review/index.html'))}#FLG-004">FLG-004</a>.</div></li>
  <li><time datetime="2026-11-20">20 Nov 2026</time><div><strong>USDA FSIS food-safety charts verified directly.</strong> Safe minimum internal temperatures and thermometer placement rules (<a href="{esc(rel(d, 'about/index.html'))}#sources">SRC-06, SRC-07</a>) now ground the thermometer and holiday hosting guides.</div></li>
  <li><time datetime="2026-11-20">20 Nov 2026</time><div><strong>Short-link codes separated from ASINs.</strong> All five submitted codes are 9 characters; all five arrival ASINs are 10. Intended ASIN stays blank until account-owner confirmation (<a href="{esc(rel(d, 'review/index.html'))}#FLG-001">FLG-001</a>).</div></li>
  <li><time datetime="2026-11-20">20 Nov 2026</time><div><strong>Analytics written and gated behind privacy review.</strong> Five events are defined and inert until a first-party collector and privacy notice are live (<a href="{esc(rel(d, 'review/measurement.html'))}">Measurement plan</a>).</div></li>
</ol>""", cls="dispatch-sec")

    capture = f"""<section class="capture"><div class="wrap capture-inner">
  <div>
    {eyebrow('Decision queue')}
    <h2>Review open questions and proposals before scaling</h2>
    <p>Every unresolved account question, compliance flag and proposed next step has its own workspace page so an owner can decide what to approve before touching production links or analytics.</p>
  </div>
  <div class="capture-card">
    <p class="capture-status"><span class="dot"></span> Owner review surfaces</p>
    <ul>
      <li><a href="{esc(rel(d, 'questions/index.html'))}">Open questions</a> &mdash; what is known, what is missing, and how to close each gap.</li>
      <li><a href="{esc(rel(d, 'suggestions/index.html'))}">Suggestions queue</a> &mdash; accept, hold or reject proposals one by one.</li>
      <li><a href="{esc(rel(d, 'review/index.html'))}">Flagged for review</a> &mdash; all 15 audit findings with official source links.</li>
    </ul>
  </div>
</div></section>"""

    body = "\n".join([hero, shortlist, thermometer, paths, guides, promise, dispatch, capture])

    structured = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": "https://karagemop466-tech.github.io/Affil1/",
        "description": "Kitchen buying guides for air fryers and meat thermometers, with all five product destinations verified against live Amazon listings.",
    }

    return page(
        d,
        title="Crisp & Counter \u2014 air fryer & meat thermometer buying guides",
        description="Three air fryers and two meat thermometers, all five verified against live Amazon listings. Plain guides on basket vs. oven, capacity, cleanup, and USDA safe internal temperatures.",
        body=body,
        active="index.html",
        canonical="",
        body_class="home",
        structured=structured,
    )
