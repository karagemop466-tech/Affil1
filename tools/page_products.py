"""Product register and the per-product records."""

from layout import (blank, esc, eyebrow, link, outbound, page, pagehead,
                    product_link, rel, section, table, DISCLOSURE)
from page_home import img

FIELDS = [
    ("submitted_link", "Submitted link", "The exact URL supplied by the operator, unchanged."),
    ("submitted_code", "Path code", "The characters after link.amazon/. Kept verbatim, including case."),
    ("intended_asin", "Intended ASIN", "What the operator meant to ship. Blank: it cannot be read from a nine-character slug."),
    ("observed_asin", "Observed ASIN", "The /dp/ segment of the page that actually loaded. Separate field, never merged with the one above."),
    ("listing_title", "Listing title", "Transcribed from the page reached, including the seller's own punctuation and claims."),
    ("brand", "Brand", "As stated on the listing."),
    ("category_path", "Category path", "The breadcrumb Amazon displayed on the arrival page."),
    ("checked_on", "Checked on", "The date the link was opened in this build."),
]


def _short(p):
    if not p.get("brand"):
        return p["ref"]
    return f"{p['brand']} {p.get('format_label', '')}".strip()


def build_register(page_dir, products, meta):
    d = page_dir
    rows = []
    for p in products:
        link_cell = product_link(
            d, p["submitted_link"], esc(p["submitted_code"]),
            aria=f"Open submitted link {p['ref']} (affiliate link, opens in a new tab)")
        if p["observed_asin"]:
            listing = product_link(
                d, p["special_link"], esc(p["observed_asin"]),
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

    body = f"""{pagehead(
        "The five",
        "Five products,<br>and the job each one does",
        "Two air fryers, one French-door oven that fries, and two ways to answer the same question about dinner. Every card says what the job is, what the seller states, and what this site could not check.",
        meta="Five links checked on 20 November 2026 &middot; nothing tested &middot; no prices shown",
    )}
{section(f'''
<div class="pcard-grid wide">
{''.join(_shop_card(d, p) for p in products)}
</div>
<p class="sec-foot"><a class="tlink" href="{esc(rel(d, 'compare/index.html'))}">See them side by side &rarr;</a> <span class="sec-foot-note">Seven columns, and the blanks left blank.</span></p>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The register')}<h2>What was submitted, and what each link reached</h2></div>
<p>This is the bookkeeping behind the cards above: the link as supplied, the code in it, and the listing that actually opened. It is here so the record can be checked, not so it can be admired.</p></div>
{tbl}
<div class="reg-note">
  <h3>Why the code and the ASIN are different columns</h3>
  <p>The code in each supplied link is nine characters and contains lowercase letters. Every ASIN observed on arrival is ten characters and uppercase. They are not the same kind of identifier, so they are never shown in the same column and never merged into one field.</p>
  <p><a class="tlink" href="{esc(rel(d, 'review/index.html'))}#FLG-001">Read the full flag &rarr;</a></p>
</div>''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Before you buy from any of them')}<h2>Four questions worth two minutes</h2></div></div>
<ol class="tight">
  <li><strong>Measure the gap, not the machine.</strong> Width, depth and height of the space, including the room a door or drawer needs while it is open.</li>
  <li><strong>Name the meal you cook most.</strong> Then check whether it fits in one layer with air around it. That is your real capacity, whatever the quarts say.</li>
  <li><strong>Count what you will wash.</strong> Baskets, trays, racks and probes are all separate objects with separate jobs and separate sink space.</li>
  <li><strong>Check the care instructions in the manual, not the listing.</strong> A claim that a basket is dishwasher-safe is a seller statement until the manufacturer's own document says it for your model.</li>
</ol>
<p class="sec-foot"><a class="tlink" href="{esc(rel(d, 'guides/index.html'))}">All six guides &rarr;</a></p>''', cls='')}
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
        "Five submitted links,<br>opened one by one",
        "What each link actually reaches, transcribed from the page that loaded \u2014 and the fields that stay empty because no official source was available.",
        meta=f"Checked {esc('20 November 2026')} &middot; 5 links &middot; 4 identified &middot; 0 tested",
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


def _shop_card(d, p):
    href = rel(d, f"products/{p['ref'].lower()}.html")
    use = {
        "P-01": "A main and a side, at the same time",
        "P-02": "Trays, pans and family portions",
        "P-03": "One big batch in one deep basket",
        "P-04": "A number instead of a guess",
        "P-05": "Walk away while it cooks",
    }.get(p["ref"], "")
    return f"""<article class="pcard">
  <div class="pcard-media">{img(d, p['photo'], p['photo_alt'], sizes='(max-width:720px) 100vw, 350px')}<span class="illus-tag">Illustration</span></div>
  <div class="pcard-body">
    <p class="pcard-ref">{esc(use)}</p>
    <h3><a href="{esc(href)}">{esc(_short(p))}</a></h3>
    <dl class="pcard-specs">
      <div><dt>Format</dt><dd>{esc(p['format_label'])}</dd></div>
      <div><dt>Seller states</dt><dd>{esc(p['stated_capacity'])}</dd></div>
      <div><dt>ASIN</dt><dd><code class="code">{esc(p['observed_asin'])}</code></dd></div>
    </dl>
    <p class="pcard-actions"><a class="btn btn-small" href="{esc(href)}">What to check</a>{product_link(d, p['special_link'], 'Amazon &#8599;', cls='tlink tlink-sponsor')}</p>
    <p class="paid-note">Paid link. Price not shown: Amazon does not serve one to this site.</p>
  </div></article>"""


def _thermometer_note(d):
    return f"""<section class="band"><div class="wrap band-inner">
  <div>
    {eyebrow('Read the category path')}
    <h2>One of these is filed under thermometers</h2>
    <p>An earlier P-05 observation reached a wireless meat thermometer; a later check reached a different thermometer. Amazon's own breadcrumb puts it under Kitchen Utensils &amp; Gadgets, then Thermometers &amp; Timers, then Meat. P-04 was unresolved in that earlier check and later reached a thermometer listing.</p>
    <p>That is not a problem with the link. It would be a problem with this site if it presented a thermometer as the fifth air fryer, which is exactly what a site written from the brief alone would have done.</p>
    <p><a class="tlink" href="{esc(rel(d, 'products/p-05.html'))}">The thermometer record <span aria-hidden="true">&rarr;</span></a></p>
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
            cell = product_link(d, p["special_link"], esc(value), aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")
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

    use_note = {
        "P-01": ("Buy it if you cook a main and a side on the same night.",
                 "Two separate 3-quart baskets, a sync-finish function and viewing windows, all as stated in the listing title. Two drawers means two jobs at once; it also means twice as many things to wash."),
        "P-02": ("Buy it if you want to put a tray, a pan or a plate inside.",
                 "A 26-quart French-door cavity stated on the listing, with 24 one-touch presets and six accessories included. The oven shape is what lets you use a dish; the trade is counter space and a door that needs room to open."),
        "P-03": ("Buy it if your usual meal fits in one deep basket.",
                 "A single 8-quart basket stated on the listing, described as 4-in-1 with a 450&deg;F option. The simplest machine in the set: one drawer, fewer parts, and a shape that suits loose food rather than dishes."),
        "P-04": ("Buy it if you want a number instead of a guess.",
                 "A quick-read probe, described in the listing as 1-second with &plusmn;0.5&deg;F accuracy and IP67 waterproofing. Use it for the USDA targets below, which are quoted from the agency and not from the seller."),
        "P-05": ("Buy it if you would rather walk away while it cooks.",
                 "A leave-in thermometer, described in the listing as wireless with three probes and a 1000&deg;F heat rating, with air fryers among its stated uses. The probes stay in the food; the reading comes to you."),
    }.get(p["ref"], ("", ""))

    safe_temps = ""
    if p["format"] == "thermometer":
        safe_temps = f"""
    <h2>What to aim for, from the agency that publishes it</h2>
    <p class="lede">The one set of numbers on this site that is not a seller's claim. These are minimum internal temperatures published by the USDA Food Safety and Inspection Service, measured with a food thermometer before the food leaves the heat.</p>
    {table(['Food', 'Minimum internal temperature', 'Rest'], [
        ['All poultry, including ground poultry and stuffing', '165&nbsp;&deg;F (73.9&nbsp;&deg;C)', '&mdash;'],
        ['Ground meats', '160&nbsp;&deg;F (71.1&nbsp;&deg;C)', '&mdash;'],
        ['Beef, pork, veal and lamb steaks, chops and roasts', '145&nbsp;&deg;F (62.8&nbsp;&deg;C)', 'At least 3 minutes'],
        ['Fish and shellfish', '145&nbsp;&deg;F (62.8&nbsp;&deg;C)', '&mdash;'],
        ['Leftovers and casseroles', '165&nbsp;&deg;F (73.9&nbsp;&deg;C)', '&mdash;'],
    ], cls='temps', note='Source: <a href="https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart" rel="noopener" target="_blank">USDA FSIS, Safe Minimum Internal Temperature Chart</a>, last updated 14 April 2025. Quoted, not paraphrased.')}
    <p class="fineprint">This site has not tested any thermometer against a reference instrument. A thermometer that is several degrees out will mislead you confidently, so the manufacturer's calibration instructions matter more than any claim on this page.</p>
"""

    side = f"""<div class="side-card">
      <h2>At a glance</h2>
      <dl class="side-dl">
        <div><dt>Brand</dt><dd>{esc(p['brand'])}</dd></div>
        <div><dt>Format</dt><dd>{esc(p['format_label'])}</dd></div>
        <div><dt>Seller states</dt><dd>{esc(p['stated_capacity'])}</dd></div>
        <div><dt>ASIN reached</dt><dd><code class="code">{esc(p['observed_asin'])}</code></dd></div>
        <div><dt>Checked</dt><dd>{esc(p['checked_on'])}</dd></div>
        <div><dt>Price shown</dt><dd><span class="pill pill-warn">No</span></dd></div>
        <div><dt>Tested by us</dt><dd><span class="pill pill-warn">No</span></dd></div>
      </dl>
    </div>"""

    body = f"""{_producthead(p, short, meta, use_note)}
<section class="section"><div class="wrap record-grid">
  <div class="record-main">
    {photo}
    <div class="verdict">
      <p class="eyebrow">The short version</p>
      <h2>{esc(use_note[0])}</h2>
      <p>{use_note[1]}</p>
      <p class="verdict-cta">{product_link(d, p['special_link'], 'Check it on Amazon <span aria-hidden="true">&#8599;</span>', cls='btn', aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")} <span class="verdict-note">Paid link. No price is shown here because Amazon does not serve one to this site.</span></p>
    </div>

    <h2>What the seller states, in the seller&rsquo;s words</h2>
    <p class="lede">Not our findings. These are the claims in the listing title, transcribed once and never paraphrased into something stronger. Read them for what the product is positioned as, not for what it does.</p>
    <ul class="claims">{stated_html}</ul>
{safe_temps}
    <h2>What this page does not know</h2>
    <p class="lede">Every row below is something a shopper would normally want. None has a source this build is allowed to use, so none is filled in. That is the trade this site makes: no numbers rather than numbers nobody checked.</p>
    {table(['Field', 'Value', 'Why it is blank'], not_stated, cls='fields')}

    <h2>How the link was checked</h2>
    <p>{esc(p['resolution_note'])}</p>
    <p>The submitted link was opened, the page it landed on was read, and the ASIN in the address and the title on the page were transcribed into this record. That establishes which product the link reaches. It says nothing about quality, price or availability &mdash; and it is a dated observation, not a guarantee that the link will reach the same place next month.</p>

    <div class="cta">
      <div>
        <p class="cta-label">The listing</p>
        <p>Opens Amazon in a new tab. This is a paid link, the price does not change, and nothing about your visit is sent to this site.</p>
      </div>
      {product_link(d, p['special_link'], 'See the listing on Amazon <span aria-hidden="true">&#8599;</span>', cls='btn', aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")}
    </div>
    <p class="fineprint">{DISCLOSURE} A purchase through this link does not change the price you pay. Whether a click is credited to this site&rsquo;s tracking ID is not yet confirmed &mdash; <a href="{esc(rel(d, 'review/index.html'))}#FLG-002">see the review queue</a>.</p>
  </div>

  <aside class="record-side">
    {side}
    <div class="side-card">
      <h2>Next</h2>
      <ul class="side-links">
        <li><a href="{esc(rel(d, 'compare/index.html'))}">Compare all five</a></li>
        <li><a href="{esc(rel(d, 'guides/basket-or-oven-air-fryer.html'))}">Basket or oven?</a></li>
        <li><a href="{esc(rel(d, 'guides/air-fryer-capacity-checklist.html'))}">Will it fit my batch?</a></li>
        <li><a href="{esc(rel(d, 'questions/index.html'))}">What is still unknown</a></li>
      </ul>
    </div>
    <div class="side-card side-card-quiet">
      <h2>Read this before trusting the page</h2>
      <p>No product on this site has been bought, used or measured, and the photograph above is an illustration. The page tells you what to check; it cannot tell you that this model passed the check.</p>
    </div>
  </aside>
</div></section>"""

    structured = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p["listing_title"],
        "brand": {"@type": "Brand", "name": p["brand"]},
        "sku": p["observed_asin"],
        "url": p["listing_url"],
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


def _producthead(p, short, meta, use_note):
    from layout import pagehead
    return pagehead(
        f"{p['ref']} &middot; {p['format_label']} &middot; checked {p['checked_on']}",
        esc(short),
        f"<strong>{esc(p['brand'])}</strong>. {esc(use_note[0])} Below: what the seller states, the numbers from the USDA where they apply, and every field this page cannot fill.",
        meta='<span class="pill pill-ok">Link checked ' + esc(p['checked_on']) + '</span> <span class="pill pill-warn">Not tested</span> <span class="pill">No price shown</span>',
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
