"""The front page: a shop window with a magazine's manners.

Order of the page is the whole argument. Products first, because that is what a
reader came for. The question-shaped guides second, because that is how a reader
decides. The machinery — how links are marked, what could not be verified — is
reachable from every card and owned by the review pages, not shouted here.

House rules that still apply on this page:
  * no price, star rating, review count or stock phrase (Associates Policies 2(b))
  * no claim that anything was tested
  * every Amazon link is a tagged Special Link, marked sponsored
"""

from layout import (DISCLOSURE, SITE_NAME, blank, esc, eyebrow, link, page,
                    product_link, rel, section)
from content import CLUSTERS, GUIDES

FEATURED = "basket-or-oven-air-fryer"


def picture(page_dir, base, alt, *, sizes, loading="lazy", widths=(560, 900), cls=""):
    """One illustration, two widths. Illustration assets ship as -w560/-w900."""
    small, large = widths
    return (
        f'<img class="{esc(cls)}" src="{esc(rel(page_dir, f"{base}-w{large}.jpg"))}" '
        f'srcset="{esc(rel(page_dir, f"{base}-w{small}.jpg"))} {small}w, '
        f'{esc(rel(page_dir, f"{base}-w{large}.jpg"))} {large}w" '
        f'sizes="{esc(sizes)}" alt="{esc(alt)}" loading="{esc(loading)}" decoding="async">'
    )


# The old name is used by page_products and page_guides.
def img(page_dir, base, alt, *, sizes, cls="", loading="lazy"):
    return picture(page_dir, base, alt, sizes=sizes, cls=cls, loading=loading)


def buy_button(page_dir, p, *, label="See it on Amazon", cls="btn btn-buy"):
    url = p.get("affiliate_url") or p.get("listing_url")
    if not url:
        return ""
    return product_link(
        page_dir, url, f'{esc(label)} <span aria-hidden="true">&#8599;</span>',
        cls=cls, aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")


def product_card(page_dir, p, *, wide=False):
    href = rel(page_dir, f"products/{p['ref'].lower()}.html")
    if not p.get("observed_asin"):
        return f"""<article class="pcard pcard-unresolved">
  <div class="pcard-media pcard-media-empty"><span>Not identified</span></div>
  <div class="pcard-body">
    <p class="pcard-ref">{esc(p['ref'])} &middot; unresolved</p>
    <h3><a href="{esc(href)}">This link did not open a product page</a></h3>
    <p class="pcard-note">No product has been guessed to fill the gap.</p>
    <p class="pcard-actions"><a class="tlink" href="{esc(href)}">What is known <span aria-hidden="true">&rarr;</span></a></p>
  </div>
</article>"""

    media = (
        f'<a class="pcard-media" href="{esc(href)}" tabindex="-1" aria-hidden="true">'
        f'{picture(page_dir, p["photo"], p["photo_alt"], sizes="(max-width:720px) 100vw, 300px")}'
        f'<span class="illus-tag">Illustration</span></a>'
    )
    return f"""<article class="pcard{' pcard-wide' if wide else ''}">
  {media}
  <div class="pcard-body">
    <p class="pcard-ref"><span class="pcard-brand">{esc(p.get('brand') or '')}</span> &middot; {esc(p.get('format_label') or '')}</p>
    <h3><a href="{esc(href)}">{esc(p.get('card_title') or p.get('format_label') or p['ref'])}</a></h3>
    <p class="pcard-angle">{esc(p.get('buyer_angle') or '')}</p>
    <dl class="pcard-specs">
      <div><dt>Stated</dt><dd>{esc(_stated(p))}</dd></div>
      <div><dt>Tested here</dt><dd>No</dd></div>
    </dl>
    <p class="pcard-actions">{buy_button(page_dir, p)}
      <a class="tlink" href="{esc(href)}">What to check <span aria-hidden="true">&rarr;</span></a></p>
  </div>
</article>"""


def _stated(p):
    cap = p.get("stated_capacity") or ""
    if not cap or cap.lower().startswith("not applicable"):
        first = (p.get("stated_attributes") or "").split(";")[0].strip()
        return first or "not stated"
    return cap


def guide_card(page_dir, g, *, feature=False):
    href = rel(page_dir, f"guides/{g['slug']}.html")
    cls = "gcard gcard-feature" if feature else "gcard"
    return f"""<article class="{cls}">
  <a class="gcard-media" href="{esc(href)}" tabindex="-1" aria-hidden="true">
    {picture(page_dir, g['photo'], g['photo_alt'], sizes='(max-width:720px) 100vw, 380px')}
  </a>
  <div class="gcard-body">
    <p class="gcard-kicker">{esc(g['kicker'])} &middot; {g['read_minutes']} min read</p>
    <h3><a href="{esc(href)}">{esc(g['title'])}</a></h3>
    <p>{esc(g['dek'])}</p>
    <a class="tlink" href="{esc(href)}">Read the guide <span aria-hidden="true">&rarr;</span></a>
  </div>
</article>"""


def build(page_dir, products, meta):
    d = page_dir
    items = products["products"] if isinstance(products, dict) else products
    featured = next(g for g in GUIDES if g["slug"] == FEATURED)

    cards = "".join(product_card(d, p) for p in items)

    paths = []
    for i, c in enumerate(CLUSTERS):
        paths.append(f"""<a class="path" href="{esc(rel(d, 'guides/' + c['slug'] + '.html'))}">
    <span class="path-n">{i + 1:02d}</span>
    <h3>{esc(c['question'])}</h3>
    <p>{esc(c['dek'])}</p>
    <span class="tlink">Read the guide <span aria-hidden="true">&rarr;</span></span>
  </a>""")

    structured = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": "https://karagemop466-tech.github.io/Affil1/",
        "description": ("An independent kitchen publication: three air fryers and two thermometers, "
                        "each listing opened and recorded, with buying guides written around the decisions."),
        "inLanguage": "en",
    }
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "The shortlist",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "name": f"{p.get('brand')} {p.get('format_label')}",
             "url": f"https://karagemop466-tech.github.io/Affil1/products/{p['ref'].lower()}.html"}
            for i, p in enumerate(items) if p.get("observed_asin")
        ],
    }

    body = f"""
<section class="hero">
  <div class="hero-media">
    {picture(d, 'assets/img/hero-counter', 'An unbranded air fryer on a wooden kitchen counter in morning light, with lemons, salt and thyme', sizes='100vw', widths=(760, 1280), loading='eager', cls='hero-img')}
    <span class="hero-illus">Illustration, not a product photo</span>
  </div>
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <p class="eyebrow">The kitchen edit &middot; November 2026</p>
      <h1>Cook better with<br><em>five honest choices.</em></h1>
      <p class="hero-dek">Three air fryers, one oven-style fryer and two thermometers &mdash; every link opened and recorded. Here is what each one is for, what to check before you buy it, and what this site will not pretend to know.</p>
      <p class="hero-actions">
        <a class="btn" href="{esc(rel(d, 'products/index.html'))}">See the five</a>
        <a class="btn btn-ghost" href="{esc(rel(d, 'guides/index.html'))}">Start with a question</a>
      </p>
      <p class="hero-fine">Illustrations, not product photographs. No prices and no star ratings: Amazon permits those only from data Amazon serves, so they are left out rather than guessed. <a href="{esc(rel(d, 'about/index.html'))}#why-blank">The rule, quoted</a>.</p>
    </div>
  </div>
</section>

<section class="section paths"><div class="wrap">
  <div class="sec-head">
    <div>{eyebrow('Start with what is bugging you')}<h2>Four questions worth settling before a product page</h2></div>
    <p>Each guide is a checklist, not a verdict. None of them needs you to buy anything here.</p>
  </div>
  <div class="path-grid">{''.join(paths)}</div>
</div></section>

<section class="section shortlist" id="shortlist"><div class="wrap">
  <div class="sec-head">
    <div>{eyebrow('The shortlist')}<h2>Five links, all five identified</h2></div>
    <p>Every listing was opened on 20 November 2026 and its title transcribed. Nothing here is ranked, because nothing here was tested.</p>
  </div>
  <div class="pcard-grid wide">{cards}</div>
  <p class="sec-foot">Each card labels what the seller states and what this site verified: the destination. <a href="{esc(rel(d, 'products/index.html'))}">The full register, with the fields that are blank</a>.</p>
</div></section>

<section class="section feature"><div class="wrap">
  <div class="feature-grid">
    <a class="feature-media" href="{esc(rel(d, 'guides/' + featured['slug'] + '.html'))}" tabindex="-1" aria-hidden="true">
      {picture(d, featured['photo'], featured['photo_alt'], sizes='(max-width:900px) 100vw, 560px')}
    </a>
    <div class="feature-copy">
      {eyebrow('The one to read first')}
      <h2>{esc(featured['title'])}</h2>
      <p>{esc(featured['dek'])}</p>
      <p class="feature-meta">{esc(featured['kicker'])} &middot; {featured['read_minutes']} min read &middot; updated {esc(featured['updated'])}</p>
      <p><a class="btn" href="{esc(rel(d, 'guides/' + featured['slug'] + '.html'))}">Read it</a></p>
    </div>
  </div>
</div></section>

<section class="section season"><div class="wrap">
  <div class="season-grid">
    <div class="season-copy">
      {eyebrow('Season · Holiday 2026')}
      <h2>Hosting is a timing problem, not a shopping problem</h2>
      <p>One oven, one fryer, one thermometer, and a table that has to land at the same moment. Start with the two shapes: a basket you shake, or a cavity you load with trays.</p>
      <p class="season-links">
        <a class="tlink" href="{esc(rel(d, 'guides/air-fryer-capacity-checklist.html'))}">Work out what fits <span aria-hidden="true">&rarr;</span></a>
        <a class="tlink" href="{esc(rel(d, 'guides/cleanup-and-counter-space.html'))}">Survive the washing-up <span aria-hidden="true">&rarr;</span></a>
        <a class="tlink" href="{esc(rel(d, 'guides/instant-read-or-probe-thermometer.html'))}">Choose a thermometer <span aria-hidden="true">&rarr;</span></a>
      </p>
    </div>
    <div class="season-media">
      {picture(d, 'assets/img/holiday-table', 'A holiday table with a roast on a platter and an unbranded air fryer softly out of focus on a sideboard behind', sizes='(max-width:900px) 100vw, 520px')}
      <span class="illus-tag">Illustration</span>
    </div>
  </div>
</div></section>

<section class="section trust"><div class="wrap">
  <div class="sec-head">
    <div>{eyebrow('How this shop works')}<h2>Three things you can check yourself</h2></div>
    <p>Not promises. Each one is a file in the repository and a rule the build enforces.</p>
  </div>
  <div class="rule-grid">
    <div class="rule"><span class="rule-n">01</span><h3>The link goes where it says</h3>
      <p>Every product page names the ASIN it was observed to reach, and links to that same ASIN with the Associates tag attached. <a href="{esc(rel(d, 'products/index.html'))}">The register</a>.</p></div>
    <div class="rule"><span class="rule-n">02</span><h3>Nothing is invented to fill a gap</h3>
      <p>No price, rating, review count or stock status appears anywhere, and no product is called a winner. Where a fact is missing, the page says so. <a href="{esc(rel(d, 'review/index.html'))}">Twenty flags</a>.</p></div>
    <div class="rule"><span class="rule-n">03</span><h3>The disclosure is above the fold</h3>
      <p>The Associates statement sits under the masthead on every page and again in the footer, because the FTC says readers miss footer-only disclosures. <a href="{esc(rel(d, 'sources/index.html'))}">The quotations</a>.</p></div>
  </div>
</div></section>

<section class="section follow"><div class="wrap follow-inner">
  <div>
    {eyebrow('Keep in touch')}
    <h2>New guides, by RSS</h2>
    <p>There is no newsletter yet &mdash; an address book is a promise to write regularly, and the publishing cadence is still a proposal rather than a fact. The feed is real and already lists every guide.</p>
  </div>
  <p class="follow-actions">
    <a class="btn" href="{esc(rel(d, 'feed.xml'))}">Subscribe by RSS</a>
    <a class="btn btn-ghost" href="{esc(rel(d, 'suggestions/index.html'))}">Suggest the next topic</a>
  </p>
</div></section>
"""
    return page(
        d,
        title="Crisp & Counter \u2014 five kitchen tools, checked link by link",
        description=("Three air fryers, one oven-style fryer and two thermometers: every Amazon link opened and recorded, "
                     "with buying guides built around the decision, not the badge."),
        body=body,
        canonical="",
        body_class="home",
        structured=item_list,
    )
