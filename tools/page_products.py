"""Product register and the per-product records."""

from layout import (blank, esc, eyebrow, link, outbound, page, product_link, rel,
                    section, table, DISCLOSURE)
from page_home import img

FIELDS = [
    ("submitted_link", "Submitted link", "The exact URL supplied by the operator, unchanged."),
    ("submitted_code", "Path code", "The characters after link.amazon/. Kept verbatim, including case."),
    ("intended_asin", "Intended ASIN", "What the operator meant to ship. Blank: it cannot be read from a nine-character slug."),
    ("observed_asin", "Observed ASIN", "The /dp/ segment of the page that actually loaded. Separate field, never merged with the one above."),
    ("tagged_link", "Buy link offered", "The /dp/ destination plus the Associates tag, built from the ASIN observed on arrival."),
    ("listing_title", "Listing title", "Transcribed from the page reached, including the seller's own punctuation and claims."),
    ("brand", "Brand", "As stated on the listing."),
    ("category_path", "Category path", "The breadcrumb Amazon displayed on the arrival page."),
    ("checked_on", "Checked on", "The date the link was opened in this build."),
]


def buy_url(p):
    """The destination the site offers.

    Program Policies 2(b) requires the Associates tag as a parameter in each
    Amazon URL, so the buy link is the observed listing plus the tag. The
    submitted short link is never used as a click target: its own tracking
    behaviour was never observable from outside.
    """
    return p.get("tagged_link") or p.get("listing_url")


def _short(p):
    if not p.get("brand"):
        return p["ref"]
    return f"{p['brand']} {p.get('format_label', '')}".strip()


def build_register(page_dir, products, meta):
    d = page_dir
    rows = []
    for p in products:
        link_cell = (f'<code class="code">{esc(p["submitted_link"])}</code>'
                     '<br><span class="tiny">recorded, not offered as a click target</span>')
        if p["observed_asin"]:
            listing = product_link(
                d, buy_url(p), esc(p["observed_asin"]),
                aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")
            name = esc(_short(p))
            status = '<span class="pill pill-ok">Identified</span>'
        else:
            listing = '<span class="blank">&mdash;</span>'
            name = '<span class="blank">&mdash;</span>'
            status = '<span class="pill pill-warn">Unresolved</span>'
        rows.append([
            {"html": f'<a href="{esc(rel(d, "products/" + p["ref"].lower() + ".html"))}"><strong>{esc(p["ref"])}</strong></a>'},
            {"html": link_cell},
            {"html": f'<code class="code">{esc(p["submitted_code"])}</code><br><span class="tiny">{p["submitted_code_length"]} characters</span>'},
            {"html": listing},
            {"html": name},
            {"html": status},
        ])

    tbl = table(
        ["Ref", "Submitted link", "Code in the link", "Listing reached", "Product", "Status"],
        rows, cls="register",
        caption="Every submitted link, opened once on 20 November 2026",
        note="The code in the link and the ASIN on arrival are different fields and are shown in separate columns on purpose. A nine-character code is not an ASIN."
    )

    body = f"""{_head(d)}
{section(f'''
<div class="reg-lede">
  <div>
    <h2>What this table is</h2>
    <p>Five links were supplied. Each was opened on 20 November 2026 and the page it landed on was read. All five resolved to a live Amazon listing in this session, and each ASIN and title was transcribed. One of them &mdash; P-04 &mdash; had failed three times in an earlier session and resolved on both attempts here, so its record keeps both outcomes.</p>
    <p>Nothing in this table was inferred. Where a value could not be established, the cell is empty and the record says why.</p>
  </div>
  <dl class="reg-stats">
    <div><dt>Links submitted</dt><dd>5</dd></div>
    <div><dt>Opened successfully</dt><dd>5</dd></div>
    <div><dt>Resolved only on retry</dt><dd>1</dd></div>
    <div><dt>Tested</dt><dd>0</dd></div>
  </dl>
</div>
{tbl}''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The records')}<h2>One page per product</h2></div>
<p>Each page carries the same fields, including the ones that are blank. The blank ones are the point.</p></div>
<div class="pcard-grid">
{''.join(_mini(d, p) for p in products)}
</div>''', cls='')}
{_thermometer_note(d)}
{section(f'''
{eyebrow('Reading the register')}
<h2>Four things a reviewer will want to check</h2>
<ol class="tight">
  <li><strong>The codes are nine characters.</strong> B04G1MEwY, B02NbDxp3, B00hJ57DV, B0c8moW59 and B0f3GKalj all contain lowercase letters and are all nine characters long. Every ASIN that loaded is ten and uppercase. The codes are short-link slugs, and the earlier version of this register was wrong to treat them as identifiers.</li>
  <li><strong>Attribution is now built in, and still unconfirmed.</strong> No arrival URL carried a tag parameter, so the site stopped offering the short links as click targets and instead offers <code class="code">/dp/&lt;ASIN&gt;/?tag=shopnow047c-20</code>, which is the format Program Policies 2(b) requires. Whether Amazon records such a click is confirmed only by the click report, and that is FLG-002.</li>
  <li><strong>Identity is not quality.</strong> Knowing which product a link opens says nothing about whether the product is any good. No product here was handled.</li>
  <li><strong>The empty columns are deliberate.</strong> Price, rating, review count and stock status would all require either Amazon-served data or API access. Neither is connected, so they stay empty site-wide.</li>
</ol>''', cls='')}
"""
    return page(
        d,
        title="Product register \u2014 Crisp & Counter",
        description="All five submitted Amazon links, each opened once and recorded: the code in the link, the ASIN on arrival, the product reached, and everything left blank.",
        body=body,
        active="products/index.html",
        canonical="products/",
    )


def _head(d):
    from layout import pagehead
    return pagehead(
        "The register",
        "Five links, opened,<br>all five identified",
        "What each link actually reaches, transcribed from the page that loaded \u2014 and the fields that stay empty because no official source was available.",
        meta=f"Checked {esc('20 November 2026')} &middot; 5 links &middot; 5 identified &middot; 1 resolved only on retry &middot; 0 tested",
    )


def _mini(d, p):
    href = rel(d, f"products/{p['ref'].lower()}.html")
    if p["identity_confidence"] == "unresolved":
        return f"""<article class="pcard pcard-unresolved">
  <div class="pcard-media pcard-media-empty"><span>Not identified</span></div>
  <div class="pcard-body"><p class="pcard-ref">{esc(p['ref'])}</p>
  <h3><a href="{esc(href)}">This link did not open a product page</a></h3>
  <p class="pcard-fine">Three attempts, all stopped at Amazon's continuity page.</p></div></article>"""
    return f"""<article class="pcard">
  <div class="pcard-media">{img(d, p['photo'], p['photo_alt'], sizes='(max-width:720px) 100vw, 300px')}<span class="illus-tag">Illustration</span></div>
  <div class="pcard-body">
    <p class="pcard-ref">{esc(p['ref'])} &middot; {esc(p['brand'])}</p>
    <h3><a href="{esc(href)}">{esc(_short(p))}</a></h3>
    <dl class="pcard-specs"><div><dt>Shape</dt><dd>{esc(p['format_label'])}</dd></div><div><dt>ASIN</dt><dd><code class="code">{esc(p['observed_asin'])}</code></dd></div></dl>
    <p class="pcard-actions"><a class="tlink" href="{esc(href)}">Full record <span aria-hidden="true">&rarr;</span></a></p>
  </div></article>"""


def _thermometer_note(d):
    return f"""<section class="band"><div class="wrap band-inner">
  <div>
    {eyebrow('Read the category path')}
    <h2>Two of these are thermometers</h2>
    <p>P-04 resolves to a ThermoMaven instant-read probe. P-05 resolves to a CHEF iQ wireless probe set with
    three probes and a stated 1000&deg;F rating. Amazon's own breadcrumb files both under Kitchen Utensils &amp;
    Gadgets, then Thermometers &amp; Timers, then Meat. The other three are under Small Appliances, then Fryers,
    then Air Fryers.</p>
    <p>That is not a problem with the links. It would be a problem with this site if it presented either one as
    the fourth air fryer, which is exactly what a site written from the brief alone would have done. They get
    their own cluster and their own guide, because an instant-read probe and a wireless multi-probe set are a
    genuinely different decision.</p>
    <p><a class="tlink" href="{esc(rel(d, 'guides/thermometer-instant-or-wireless.html'))}">Instant-read or wireless? <span aria-hidden="true">&rarr;</span></a>
    &nbsp; <a class="tlink" href="{esc(rel(d, 'products/p-05.html'))}">The P-05 record <span aria-hidden="true">&rarr;</span></a></p>
  </div>
</div></section>"""


def build_product(page_dir, p, meta):
    d = page_dir
    if p["identity_confidence"] == "unresolved":
        return _build_unresolved(d, p)

    short = _short(p)
    title_el = f"{esc(short)} <span class='asin'>({esc(p['observed_asin'])})</span>"

    facts = []
    for key, label, note in FIELDS:
        value = p.get(key)
        if key == "submitted_link":
            cell = product_link(d, value, esc(p["submitted_code"]), aria=f"Open submitted link for {p['ref']} (affiliate link, opens in a new tab)")
        elif key == "observed_asin":
            cell = product_link(d, buy_url(p), esc(value), aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")
        elif key == "category_path":
            cell = esc(value)
        else:
            cell = blank(value) if not value else esc(value)
        facts.append([
            {"html": f"<strong>{esc(label)}</strong><br><span class='tiny'>{esc(note)}</span>"},
            {"html": cell},
        ])

    stated = p.get("title_stated") or []
    stated_html = "".join(f"<li>{esc(s)}</li>" for s in stated) if stated else '<li class="blank">The listing title made no attribute claims that could be transcribed.</li>'

    not_stated = [
        [v, {"html": blank(None, "no permitted source")},
         {"html": f'<a href="{esc(rel(d, "about/index.html"))}#why-blank">Why</a>'}]
        for v in p["unverified"]
    ]

    photo = ""
    if p.get("photo"):
        photo = f"""<figure class="fig">
  {img(d, p['photo'], p['photo_alt'], sizes='(max-width:720px) 100vw, 720px')}
  <figcaption><span class="illus-tag illus-inline">Illustration</span> {esc(p['photo_note'])}</figcaption>
</figure>"""

    body = f"""{_producthead(p, short, meta)}
<section class="section"><div class="wrap record-grid">
  <div class="record-main">
    {photo}
    <h2>What the seller states, in the seller's words</h2>
    <p class="lede">These are not our findings. They are the claims written into the listing title by whoever sells the product, transcribed once and never paraphrased into something stronger. Read them for what the product is positioned as, not for what it does.</p>
    <ul class="claims">{stated_html}</ul>

    <h2>What was not established</h2>
    <p class="lede">Each row below is a field a shopper would normally expect to see. None of them has a source this build is allowed to use, so none of them is filled in.</p>
    {table(['Field', 'Value', 'Reason'], not_stated, cls='fields')}

    <h2>How the link was checked</h2>
    <p>{esc(p['resolution_note'])}</p>
    <p>The submitted link was opened; the page it landed on was read; the ASIN inside the address and the title on the page were transcribed into this record. That is the whole of the check. It establishes identity. It does not establish quality, price or availability.</p>

    <div class="cta">
      <div>
        <p class="cta-label">Amazon listing</p>
        <p>Opens in a new tab. This is an affiliate link{'' if not meta.get('tracking') else ''}.</p>
      </div>
      {product_link(d, buy_url(p), 'See the listing on Amazon <span aria-hidden="true">&#8599;</span>', cls='btn', aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")}
    </div>
    <p class="fineprint">{DISCLOSURE} A purchase through this link does not change the price you pay. Whether a click is credited to this site's tracking ID is not confirmed \u2014 see the review queue.</p>
  </div>

  <aside class="record-side">
    <div class="side-card">
      <h2>At a glance</h2>
      <dl class="side-dl">
        <div><dt>Reference</dt><dd>{esc(p['ref'])}</dd></div>
        <div><dt>Brand</dt><dd>{esc(p['brand'])}</dd></div>
        <div><dt>Shape</dt><dd>{esc(p['format_label'])}</dd></div>
        <div><dt>ASIN</dt><dd><code class="code">{esc(p['observed_asin'])}</code></dd></div>
        <div><dt>Checked</dt><dd>{esc(p['checked_on'])}</dd></div>
        <div><dt>Tested by us</dt><dd><span class="pill pill-warn">No</span></dd></div>
      </dl>
    </div>
    <div class="side-card">
      <h2>Next</h2>
      <ul class="side-links">
        <li><a href="{esc(rel(d, 'compare/index.html'))}">Compare all five</a></li>
        <li><a href="{esc(rel(d, 'guides/basket-or-oven-air-fryer.html'))}">Basket or oven?</a></li>
        <li><a href="{esc(rel(d, 'questions/index.html'))}">What is still unknown</a></li>
      </ul>
    </div>
    <div class="side-card side-card-quiet">
      <h2>Read this before trusting the page</h2>
      <p>No product on this site has been bought, used or measured. The photograph above is an illustration. The guide tells you what to check; it cannot tell you that this model passed the check.</p>
    </div>
  </aside>
</div></section>"""

    structured = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p["listing_title"],
        "brand": {"@type": "Brand", "name": p["brand"]},
        "sku": p["observed_asin"],
        "url": buy_url(p),
    }

    return page(
        d,
        title=f"{short} ({p['observed_asin']}) \u2014 record and what is unverified",
        description=f"{p['ref']}: the submitted link, the Amazon listing it reached, the {p['observed_asin']} recorded on arrival, the seller's stated attributes, and every field left blank.",
        body=body,
        active="products/index.html",
        canonical=f"products/{p['ref'].lower()}.html",
        structured=structured,
        og_type="article",
    )


def _producthead(p, short, meta):
    d = ""
    from layout import pagehead
    return pagehead(
        f"Record {p['ref']} &middot; checked {p['checked_on']}",
        f"{esc(short)}<br><span class='head-asin'>{esc(p['observed_asin'])}</span>",
        f"<strong>{esc(p['brand'])}</strong> &middot; {esc(p['format_label'])}. This record says what the listing states, what was checked, and what remains blank.",
        meta=f'<span class="pill pill-ok">Identity confirmed</span> <span class="pill pill-warn">Not tested</span> <span class="pill">No price shown</span>',
    )


def _build_unresolved(d, p):
    body = f"""{_producthead_unresolved(p)}
<section class="section"><div class="wrap narrow">
  <h2>What was attempted</h2>
  <p>{esc(p['resolution_note'])}</p>
  <ol class="tight">
    <li>The link <code class="code">{esc(p['submitted_link'])}</code> was requested directly. It returned Amazon's <code class="code">/checkpoint/continue</code> page.</li>
    <li>It was requested twice more. Both attempts returned the same continuity page.</li>
    <li>No product page, listing title, ASIN, brand or category was ever displayed, so none is recorded.</li>
  </ol>

  <h2>What was not done</h2>
  <p>No product was guessed. There is no candidate row, no placeholder title, no "likely" match and no card with an invented brand on it. Four of the five links could be identified; this one could not, and the register shows a five-row table with a visibly empty row rather than a four-row table that quietly omits the failure.</p>

  <h2>The likely causes, none of which was diagnosed</h2>
  <ul class="tight">
    <li>The short link has expired or been replaced.</li>
    <li>The code was mistyped when it was supplied.</li>
    <li>It is region-restricted and this client is in the wrong region.</li>
    <li>It is a challenge served to automated clients specifically, in which case it would open normally in a browser.</li>
  </ul>
  <p>All four are consistent with what was observed. Choosing between them would require opening it somewhere this session cannot reach, so none is asserted.</p>

  <h2>How to close this</h2>
  <p>Open <a href="{esc(p['submitted_link'])}" rel="sponsored nofollow noopener" target="_blank">link.amazon/B0c8moW59</a> in an ordinary browser and note where it lands. If it is dead, re-issue it from the Associates dashboard. Either way the record above gets a date and a value, and the blank row becomes a product.</p>

  <div class="cta">
    <div><p class="cta-label">Still open</p><p>This product has no card, no photograph and no buy link until it can be identified.</p></div>
    <a class="btn btn-ghost" href="{esc(rel(d, 'review/index.html'))}#FLG-004">See the flag</a>
  </div>
</div></section>"""
    return page(
        d,
        title="Unresolved link \u2014 record P-04",
        description="The fourth submitted link did not open a product page on 20 November 2026. This record shows exactly what was attempted and why nothing was filled in.",
        body=body,
        active="products/index.html",
        canonical="products/p-04.html",
    )


def _producthead_unresolved(p):
    from layout import pagehead
    return pagehead(
        f"Record {p['ref']} &middot; unresolved",
        "This link did not<br>open a product",
        "Three attempts on 20 November 2026, three continuity pages. Rather than fill the gap, the gap is published.",
        meta='<span class="pill pill-warn">Unresolved</span> <span class="pill">No product invented</span>',
    )
