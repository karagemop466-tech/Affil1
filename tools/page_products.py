"""The shortlist (shop grid + verification register) and one record per product.

Two audiences, one data file. A shopper reads the card; a reviewer reads the
table under it. Neither is asked to trust the other's column.
"""

from layout import (blank, esc, eyebrow, flag_count, link, outbound, page, product_link, rel,
                    section, spelled, table, pagehead)
from page_home import buy_button, img, picture

FIELDS = [
    ("submitted_link", "Submitted link", "The exact URL supplied by the operator, unchanged."),
    ("submitted_code", "Path code", "The characters after link.amazon/. Kept verbatim, including case."),
    ("intended_asin", "Intended ASIN", "What the operator meant to ship. Blank: a nine-character slug is not an identifier."),
    ("observed_asin", "Observed ASIN", "The /dp/ segment of the page that actually loaded. Separate field, never merged."),
    ("listing_title", "Listing title", "Transcribed from the page reached, in the seller's own words."),
    ("brand", "Brand", "As stated on the listing."),
    ("category_path", "Category path", "The breadcrumb Amazon displayed on the arrival page."),
    ("checked_on", "Checked on", "The date the link was opened for this build."),
]


def _name(p):
    return f"{p.get('brand') or ''} {p.get('format_label') or ''}".strip()


def build_register(page_dir, products, meta):
    d = page_dir
    identified = [p for p in products if p.get("observed_asin")]
    rows = []
    for p in products:
        code_cell = {"html": f'<code class="code">{esc(p["submitted_code"])}</code><br><span class="tiny">{p["submitted_code_length"]} characters</span>'}
        submitted = {"html": product_link(d, p["submitted_link"], "link.amazon/" + esc(p["submitted_code"]),
                                  aria=f"Open submitted link {p['ref']} (affiliate link, opens in a new tab)")}
        if p.get("observed_asin"):
            listing = {"html": product_link(
                d, p["affiliate_url"], esc(p["observed_asin"]),
                aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")}
            rows.append([
                {"html": f'<a href="{esc(rel(d, "products/" + p["ref"].lower() + ".html"))}"><strong>{esc(p["ref"])}</strong></a>'},
                {"html": f'<strong>{esc(_name(p))}</strong>'},
                submitted, code_cell, listing,
                {"html": '<span class="pill pill-ok">Identified</span>'},
            ])
        else:
            rows.append([
                {"html": f'<a href="{esc(rel(d, "products/" + p["ref"].lower() + ".html"))}"><strong>{esc(p["ref"])}</strong></a>'},
                {"html": blank(None, "not identified")}, submitted, code_cell,
                {"html": blank(None, "no listing reached")},
                {"html": '<span class="pill pill-warn">Unresolved</span>'},
            ])

    tbl = table(
        ["Ref", "Product", "Submitted link", "Code in the link", "Listing reached", "Status"],
        rows, cls="register",
        caption="Every submitted link, opened on 20 November 2026",
        note=("The code in the link and the ASIN on arrival are different fields in different columns on purpose. "
              "A nine-character code is not an ASIN, and the listing column links to the tagged Special Link the site actually uses."),
    )

    fryers = [p for p in products if p.get("format") in ("basket", "oven")]
    therms = [p for p in products if p.get("format") == "thermometer"]
    cards = (
        f'<div class="cat-head" id="air-fryers"><h2>Air fryers</h2>'
        f'<p>{len(fryers)} products: two basket shapes and one oven shape.</p></div>'
        f'<div class="pcard-grid wide">{"".join(_card(d, p) for p in fryers)}</div>'
        f'<div class="cat-head" id="thermometers"><h2>Thermometers</h2>'
        f'<p>{len(therms)} products: one instant-read, one wireless multi-probe. A different category, and not called air fryers here.</p></div>'
        f'<div class="pcard-grid wide">{"".join(_card(d, p) for p in therms)}</div>'
    )

    body = f"""{pagehead(
        'The shortlist',
        'Five links,<br>all five identified',
        'Three air fryers and two thermometers. Each listing was opened on 20 November 2026, its title transcribed, and the '
        'destination recorded before any copy was written about it.',
        meta='Checked 20 November 2026 &middot; 5 submitted &middot; 5 identified &middot; 0 tested &middot; no prices, ratings or rankings',
    )}
{section(f'''
<div class="stat-row">
  <div class="stat"><span class="stat-n">{len(products)}</span><span class="stat-l">links submitted</span></div>
  <div class="stat"><span class="stat-n">{len(identified)}</span><span class="stat-l">destinations identified</span></div>
  <div class="stat"><span class="stat-n">0</span><span class="stat-l">products tested</span></div>
  <div class="stat"><span class="stat-n">0</span><span class="stat-l">prices or ratings shown</span></div>
</div>
<p class="cat-chips"><a href="#air-fryers">Air fryers &middot; 3</a> <a href="#thermometers">Thermometers &middot; 2</a></p>
<p class="lede-prose">This is a shortlist, not a leaderboard. Nothing here has been handled, cooked with, measured or ranked, and
the site says so on every card rather than in a footnote. What has been done is narrower and more useful: each link was
followed, and the product on the other end was identified.</p>''', cls='')}
{section(cards, cls='shortlist')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The register')}<h2>Every submitted link, and where it lands</h2></div>
<p>One row per link, with the source column pointing at the Amazon page that was actually reached.</p></div>
{tbl}''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Reading the register')}<h2>Four things worth knowing</h2></div></div>
<ol class="tight">
  <li><strong>The codes are nine characters.</strong> Every supplied slug is 9 characters and contains lowercase letters;
      every ASIN that loaded is 10 and uppercase. The codes are short-link slugs, so the intended ASIN column stays empty
      rather than repeating the slug in a column labelled ASIN.</li>
  <li><strong>The links are tagged by this site, not by the shortener.</strong> None of the five final URLs contained a tag
      parameter. Every outbound product link here is <code class="code">/dp/ASIN?tag=shopnow047c-20</code>, which is the form
      Program Policies 2(b) describes. Whether the ID itself is active is a separate question (Q-07).</li>
  <li><strong>Two products are not air fryers.</strong> P-04 and P-05 are meat thermometers, filed under a different category
      path. No page on this site calls them air fryers.</li>
  <li><strong>The empty columns are the honest ones.</strong> Price, rating, review count and availability would be the most
      useful columns here and are absent because Amazon permits them only from data Amazon serves or via its API.
      <a href="{esc(rel(d, 'about/index.html'))}#why-blank">The rule, quoted</a>.</li>
</ol>''', cls='')}
"""
    return page(
        d,
        title="The shortlist \u2014 five kitchen tools, checked link by link | Crisp & Counter",
        description=("All five submitted Amazon links, each opened and recorded: the ASIN reached, the seller's title, what "
                     "each product is for, and what stays blank."),
        body=body,
        active="products/index.html",
        canonical="products/",
        breadcrumb=[("Home", ""), ("Shortlist", "products/")],
    )


def _stated(p):
    cap = p.get("stated_capacity") or ""
    if not cap or cap.lower().startswith("not applicable"):
        first = (p.get("stated_attributes") or "").split(";")[0].strip()
        return first or "not stated"
    return cap


def _card(d, p):
    href = rel(d, f"products/{p['ref'].lower()}.html")
    if not p.get("observed_asin"):
        return f'''<article class="pcard pcard-unresolved">
  <div class="pcard-media pcard-media-empty"><span>Not identified</span></div>
  <div class="pcard-body"><p class="pcard-ref">{esc(p['ref'])}</p>
  <h3><a href="{esc(href)}">This link did not open a product page</a></h3></div></article>'''
    return f'''<article class="pcard">
  <a class="pcard-media" href="{esc(href)}" tabindex="-1" aria-hidden="true">
    {img(d, p['photo'], p['photo_alt'], sizes='(max-width:720px) 100vw, 320px')}<span class="illus-tag">Illustration</span></a>
  <div class="pcard-body">
    <p class="pcard-ref"><span class="pcard-brand">{esc(p.get('brand') or '')}</span> &middot; {esc(p.get('format_label') or '')}</p>
    <h3><a href="{esc(href)}">{esc(p.get('card_title') or _name(p))}</a></h3>
    <p class="pcard-angle">{esc(p.get('buyer_angle') or '')}</p>
    <dl class="pcard-specs">
      <div><dt>Stated</dt><dd>{esc(_stated(p))}</dd></div>
      <div><dt>Tested here</dt><dd>No</dd></div>
    </dl>
    <p class="pcard-actions">{buy_button(d, p)}
      <a class="tlink" href="{esc(href)}">What to check <span aria-hidden="true">&rarr;</span></a></p>
  </div>
</article>'''


def build_product(page_dir, p, meta):
    d = page_dir
    ref = p["ref"]
    href_back = rel(d, "index.html")

    facts = [
        ("Reference", esc(ref), "This site's own label, not the seller's."),
        ("Brand", esc(p.get("brand")), "As stated on the listing."),
        ("Type", esc(p.get("format_label")), "Read from the listing title and category path."),
        ("Category path", esc(p.get("category_path")), "The breadcrumb Amazon displayed on arrival."),
        ("Observed ASIN", product_link(d, p["affiliate_url"], esc(p["observed_asin"]),
                                       aria=f"Open the Amazon listing for {ref} (affiliate link, opens in a new tab)")
         if p.get("observed_asin") else blank(None, "no listing reached"), "The /dp/ segment of the page that loaded."),
        ("Intended ASIN", blank(p.get("intended_asin"), "not supplied and not inferable"),
         "Separate field. A nine-character slug does not establish this."),
        ("Submitted link", product_link(d, p["submitted_link"], "link.amazon/" + esc(p["submitted_code"]),
                                       aria=f"Open submitted link {ref} (affiliate link, opens in a new tab)"),
         "The URL supplied by the operator, unchanged."),
        ("Stated size", esc(p.get("stated_capacity")), "The seller's words, not a measurement."),
        ("Stated attributes", esc(p.get("stated_attributes")), "The seller's words, not a test."),
        ("Price", blank(None, "only permitted from Amazon-served data or the API"), "Policies 2(b)."),
        ("Rating", blank(None, "only permitted from Amazon-served data or the API"), "Policies 2(b)."),
        ("Availability", blank(None, "only permitted from Amazon-served data or the API"), "Policies 2(b)."),
        ("Tested here", "No", "Nothing on this site was handled or cooked with."),
        ("Checked on", esc(p.get("checked_on")), "The date the listing was opened."),
    ]

    fact_rows = [[
        {"html": f"<strong>{esc(k)}</strong>"},
        {"html": v},
        {"html": f'<span class="tiny">{esc(why)}</span>'},
    ] for k, v, why in facts]

    facts_tbl = table(["Field", "Value", "Where it comes from"], fact_rows, cls="facts",
                      caption=f"{ref} — what is known and what is deliberately blank")

    stated = "".join(f"<li>{esc(s)}</li>" for s in p.get("title_stated") or [])
    suits = "".join(f"<li>{esc(s)}</li>" for s in p.get("suits") or [])
    check = "".join(f"<li>{esc(s)}</li>" for s in p.get("check_first") or [])
    unverified = "".join(f"<li>{esc(s)}</li>" for s in p.get("unverified") or [])

    others = [x for x in meta.get("products", []) if x["ref"] != ref and x.get("observed_asin")][:2]
    nxt = "".join(f'''<a class="next-card" href="{esc(rel(d, 'products/' + x['ref'].lower() + '.html'))}">
  <p class="gcard-kicker">{esc(x['ref'])} &middot; {esc(x.get('format_label') or '')}</p>
  <h3>{esc(x.get('card_title') or _name(x))}</h3>
  <span class="tlink">Read the record <span aria-hidden="true">&rarr;</span></span></a>''' for x in others)

    note = ""
    if p.get("attention"):
        note = f'<aside class="note"><p class="note-label">Category note</p><p>{esc(p["attention"])}</p></aside>'

    body = f"""{pagehead(
        f"{ref} · {p.get('format_label') or 'product record'}",
        esc(_name(p)),
        esc(p.get("buyer_angle") or ""),
        meta=f"Identity checked {esc(p.get('checked_on'))} &middot; not tested &middot; no price or rating shown",
    )}
<section class="section"><div class="wrap product-grid">
  <div class="product-media">
    {picture(d, p['photo'], p['photo_alt'], sizes='(max-width:900px) 100vw, 620px', loading='eager') if p.get('photo') else ''}
    <p class="figcap"><span class="illus-tag illus-inline">Illustration</span> {esc(p.get('photo_note') or '')}</p>
  </div>
  <div class="product-buy">
    <p class="pcard-ref"><span class="pcard-brand">{esc(p.get('brand') or '')}</span> &middot; {esc(p.get('format_label') or '')} &middot; {esc(p.get('card_title') or '')}</p>
    <p class="product-lede">{esc(p.get('buyer_angle') or '')}</p>
    {note}
    <div class="buy-block">
      {buy_button(d, p, label='See the listing on Amazon', cls='btn btn-buy btn-wide')}
      <p class="buy-fine">Opens a tagged Amazon listing in a new tab. As an Amazon Associate this site earns from qualifying purchases. The destination ASIN was observed on {esc(p.get('checked_on'))}.</p>
    </div>
    <div class="product-lists">
      <div><h3>What the listing states</h3><ul class="ticks">{stated}</ul></div>
      <div><h3>Who it suits</h3><ul class="ticks">{suits}</ul></div>
      <div><h3>What to check before you buy</h3><ul class="checks-list">{check}</ul></div>
    </div>
  </div>
</div></section>
<section class="section section-tint"><div class="wrap">
  <div class="sec-head"><div>{eyebrow('The record')}<h2>Every field, including the blanks</h2></div>
  <p>This is the reviewer's view. The rows that are empty are empty on purpose, and the last column says why.</p></div>
  {facts_tbl}
  <div class="two-col">
    <div><h3>Not verified here</h3><ul class="ticks ticks-quiet">{unverified}</ul></div>
    <div><h3>How this page is limited</h3>
      <p>Nothing on this page comes from using the product. The seller's claims are quoted as claims; the destination is the one
      fact this site established by opening the link. Where a useful number would need Amazon's API or a test, the page has
      neither and says so.</p>
      <p><a class="tlink" href="{esc(rel(d, 'review/index.html'))}">All {esc(spelled(flag_count()))} flags <span aria-hidden="true">&rarr;</span></a></p>
    </div>
  </div>
</div></section>
<section class="section"><div class="wrap">
  <div class="sec-head"><div>{eyebrow('Keep looking')}<h2>Two more records</h2></div></div>
  <div class="next-grid">{nxt}</div>
</div></section>"""

    structured = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": _name(p),
        "brand": {"@type": "Brand", "name": p.get("brand") or ""},
        "url": f"https://karagemop466-tech.github.io/Affil1/products/{ref.lower()}.html",
        "description": p.get("buyer_angle") or "",
    }
    return page(
        d,
        title=f"{_name(p)} \u2014 what the listing states | Crisp & Counter",
        description=(p.get("buyer_angle") or "")[:150],
        body=body,
        active="products/index.html",
        canonical=f"products/{ref.lower()}.html",
        structured=structured,
        breadcrumb=[("Home", ""), ("Shortlist", "products/"), (ref, f"products/{ref.lower()}.html")],
    )
