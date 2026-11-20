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


def product_card(page_dir, p, *, compact=False):
    href = rel(page_dir, f"products/{p['ref'].lower()}.html")
    if p["identity_confidence"] == "unresolved":
        return f"""<article class="pcard pcard-unresolved">
  <div class="pcard-media pcard-media-empty"><span>Not identified</span></div>
  <div class="pcard-body">
    <p class="pcard-ref">{esc(p['ref'])} &middot; unresolved</p>
    <h3>This link did not open a product page</h3>
    <p class="pcard-note">Requested three times on 20 November 2026 and it stopped at an Amazon continuity page each time. No product has been guessed to fill the gap.</p>
    <p class="pcard-actions"><a class="tlink" href="{esc(href)}">What is known <span aria-hidden="true">&rarr;</span></a></p>
  </div>
</article>"""

    media = (
        f'<div class="pcard-media">{img(page_dir, p["photo"], p["photo_alt"], sizes="(max-width:720px) 100vw, 300px")}'
        f'<span class="illus-tag">Illustration</span></div>'
    )
    attrs = "".join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in _specs(p))
    if compact:
        body = f"""<div class="pcard-body">
    <p class="pcard-ref">{esc(p['ref'])} &middot; {esc(p['brand'])}</p>
    <h3>{esc(_short(p))}</h3>
    <p class="pcard-actions"><a class="tlink" href="{esc(href)}">Read the record <span aria-hidden="true">&rarr;</span></a>
    {product_link(page_dir, p['listing_url'], 'See listing <span aria-hidden="true">&#8599;</span>', cls='tlink tlink-sponsor', aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")}</p>
  </div>"""
    else:
        body = f"""<div class="pcard-body">
    <p class="pcard-ref">{esc(p['ref'])} &middot; identity checked {esc(p['checked_on'])}</p>
    <h3><a href="{esc(href)}">{esc(_short(p))}</a></h3>
    <dl class="pcard-specs">{attrs}</dl>
    <p class="pcard-actions"><a class="tlink" href="{esc(href)}">Read the record <span aria-hidden="true">&rarr;</span></a>
    {product_link(page_dir, p['listing_url'], 'See listing <span aria-hidden="true">&#8599;</span>', cls='tlink tlink-sponsor', aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")}</p>
    <p class="pcard-fine">Not tested. No price or rating is shown here because this site has no permitted live data source.</p>
  </div>"""
    return f'<article class="pcard">{media}{body}</article>'


def _short(p):
    shape = p.get("format_label") or ""
    brand = p.get("brand") or ""
    return f"{brand} {shape}".strip()


def _specs(p):
    """Three facts, none of them repeating the heading above."""
    rows = []
    cap = p.get("stated_capacity")
    if cap:
        rows.append(("Stated size", cap))
    attrs = p.get("stated_attributes")
    if attrs:
        first = attrs.split(";")[0].strip()
        rows.append(("Also stated", first))
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
    <a class="tlink" href="{esc(href)}">Read <span aria-hidden="true">&rarr;</span></a>
  </div>
</article>"""


def build(page_dir, products, meta):
    d = page_dir
    by_ref = {p["ref"]: p for p in products}
    mains = [by_ref[r] for r in ("P-01", "P-02", "P-03", "P-04")]
    therm = by_ref["P-05"]

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
      <h1>Buy once.<br><em>Cook better.</em></h1>
      <p class="hero-dek">Five links, opened and read one by one. Three air fryers, one air-fryer oven, one thermometer &mdash; and plain guidance on shape, size and washing-up. Nothing here was tested, and the site says so on every page.</p>
      <p class="hero-actions">
        <a class="btn" href="{esc(rel(d, 'products/index.html'))}">See the shortlist</a>
        <a class="btn btn-ghost" href="{esc(rel(d, 'guides/index.html'))}">Start with a guide</a>
      </p>
      <p class="hero-fine">No prices, no ratings, no star counts. Not because they are hard to copy &mdash; because Amazon only permits them from data Amazon serves. <a href="{esc(rel(d, 'about/index.html'))}#why-blank">Why the gaps</a>.</p>
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
  <div>{eyebrow('The shortlist')}<h2>Five links, four of them identified</h2></div>
  <p>Each page was opened on 20 November 2026 and the listing transcribed. One did not open at all, and it is still on the page.</p>
</div>
<div class="pcard-grid wide">
  {''.join(product_card(d, p) for p in mains)}
</div>
<p class="sec-foot">Identity is the only thing confirmed. <a href="{esc(rel(d, 'products/index.html'))}">The full register, including the fields left blank</a> &middot; <a href="{esc(rel(d, 'compare/index.html'))}">compare them side by side</a>.</p>""", cls="shortlist")

    thermometer = f"""<section class="thermo-band"><div class="wrap thermo-inner">
  <div class="thermo-art">{img(d, 'assets/img/thermometer', 'A probe thermometer resting in a roasted chicken beside a small display unit', sizes='(max-width:720px) 100vw, 420px')}<span class="illus-tag">Illustration</span></div>
  <div class="thermo-copy">
    {eyebrow('A note on the fifth link')}
    <h2>The fifth product is not an air fryer</h2>
    <p>It resolves to a wireless meat thermometer filed under <em>Thermometers &amp; Timers</em>, not <em>Air Fryers</em>. A generated site would have called it the fifth air fryer and moved on. It gets its own page instead, because describing it as cookware would be false.</p>
    <p class="thermo-actions"><a class="btn btn-light" href="{esc(rel(d, 'products/p-05.html'))}">Read the thermometer record</a></p>
  </div>
</div></section>"""

    guides = section(f"""
<div class="sec-head">
  <div>{eyebrow('Buying guides')}<h2>Written to be useful before you click</h2></div>
  <p>Four guides. Every product claim in them is the seller's own wording, quoted. Nothing was tested, so nothing is rated. Also read our <a href="{esc(rel(d, 'guides/holiday-hosting.html'))}">holiday hosting checklist</a> and <a href="{esc(rel(d, 'reviews/verification-audit.html'))}">independent verification audit</a>.</p>
</div>
<div class="gcard-grid">
  {guide_card(d, GUIDES[0], feature=True)}
  {''.join(guide_card(d, g) for g in GUIDES[1:])}
</div>""", cls="guides")

    promise = section(f"""
<div class="sec-head">
  <div>{eyebrow('How this works')}<h2>Three rules, and what they cost</h2></div>
</div>
<div class="rule-grid">
  <div class="rule">
    <span class="rule-n">01</span>
    <h3>A link is opened, not trusted</h3>
    <p>Every submitted link was requested and the arrival page read. Where the page could not be reached, the row says so and stays empty.</p>
    <p class="rule-cost"><strong>The cost:</strong> one of five products is still a blank.</p>
  </div>
  <div class="rule">
    <span class="rule-n">02</span>
    <h3>No price, no rating, no stars</h3>
    <p>Amazon's Program Policies allow price and availability only where Amazon serves them or they arrive through its API. This site has neither, so it shows neither.</p>
    <p class="rule-cost"><strong>The cost:</strong> the cards look thinner than every competitor's.</p>
  </div>
  <div class="rule">
    <span class="rule-n">03</span>
    <h3>Nothing here was tested</h3>
    <p>No product was bought, cooked with or measured. Every photograph is an illustration and says so. That is a real limitation, not a style choice.</p>
    <p class="rule-cost"><strong>The cost:</strong> these guides cannot tell you which one to buy.</p>
  </div>
</div>
<p class="sec-foot">The full reasoning, including the parts that are uncomfortable, sits in <a href="{esc(rel(d, 'review/index.html'))}">the review queue</a>.</p>""", cls="promise rules")

    dispatch = section(f"""
<div class="sec-head">
  <div>{eyebrow('Desk notes')}<h2>What changed, and when</h2></div>
  <p>A dated record. Affiliate pages age badly and silently, so the site keeps its own receipt.</p>
</div>
<ol class="dispatch">
  <li><time datetime="2026-11-20">20 Nov 2026</time><div><strong>All five links opened and read.</strong> Four resolved to live listings; their ASINs and titles are recorded. One stopped at a continuity page and stays unresolved. <a href="{esc(rel(d, 'products/index.html'))}">Register</a></div></li>
  <li><time datetime="2026-11-20">20 Nov 2026</time><div><strong>Corrected an earlier error.</strong> A previous version of this repository treated the supplied link codes as intended ASINs. They are nine characters; the ASINs on arrival are ten. The two fields are now separate. <a href="{esc(rel(d, 'review/index.html'))}#FLG-001">Flagged</a></div></li>
  <li><time datetime="2026-11-20">20 Nov 2026</time><div><strong>Prices removed by rule.</strong> No price, rating or stock status appears anywhere, because neither permitted data source is connected. <a href="{esc(rel(d, 'review/index.html'))}#FLG-005">Flagged</a></div></li>
  <li><time datetime="2026-11-20">20 Nov 2026</time><div><strong>Analytics written but switched off.</strong> Nothing is measured yet, so no traffic claim is made. <a href="{esc(rel(d, 'review/measurement.html'))}">Measurement plan</a></div></li>
</ol>""", cls="dispatch-sec")

    capture = f"""<section class="capture"><div class="wrap capture-inner">
  <div>
    {eyebrow('Reader questions')}
    <h2>What should this site answer next?</h2>
    <p>The honest answer today is: we do not know, because nothing is being measured. Reader capture opens once a privacy notice exists and an endpoint is live. Until then, the topic list is a set of labelled hypotheses, not a plan.</p>
  </div>
  <div class="capture-card">
    <p class="capture-status"><span class="dot"></span> Capture not live</p>
    <ul>
      <li>No form, because there is nowhere to send a reply yet.</li>
      <li>No newsletter, because there is no list and no consent record.</li>
      <li>Read the <a href="{esc(rel(d, 'suggestions/index.html'))}">suggestion queue</a> instead &mdash; it is what a reader would be voting on.</li>
    </ul>
  </div>
</div></section>"""

    body = "\n".join([hero, paths, shortlist, thermometer, guides, promise, dispatch, capture])

    structured = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": "https://karagemop466-tech.github.io/Affil1/",
        "description": "Kitchen buying guides for air fryers and cooking thermometers, with product identities checked against the live Amazon listing.",
    }

    return page(
        d,
        title="Crisp & Counter \u2014 air fryer buying guides that check the link first",
        description="Four air fryers and a thermometer, each checked against its live Amazon listing. Plain guidance on basket versus oven, capacity and cleanup \u2014 with no invented prices, ratings or test results.",
        body=body,
        active="index.html",
        canonical="",
        body_class="home",
        structured=structured,
    )
