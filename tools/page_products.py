"""Product register, category subpages, and per-product confirmation records."""

from layout import (blank, esc, eyebrow, link, outbound, page, pagehead,
                    product_link, rel, section, table, DISCLOSURE)
from page_home import img, product_card, guide_card
from content import GUIDES

FIELDS = [
    ("submitted_link", "Submitted link", "The exact URL supplied by the operator, unchanged."),
    ("submitted_code", "Submitted path code", "The 9-character code after link.amazon/. Kept verbatim, never treated as an ASIN."),
    ("intended_asin", "Intended ASIN", "What the operator meant to promote. Blank until confirmed from Associates Central — never merged with observed ASIN."),
    ("observed_asin", "Observed ASIN (redirect target)", "The 10-character /dp/ identifier observed on the live Amazon listing. Stored separately from intended ASIN."),
    ("listing_title", "Official listing title", "Transcribed verbatim from the live Amazon product page reached on 2026-11-20."),
    ("brand", "Brand", "As stated on the Amazon listing."),
    ("category_path", "Amazon category path", "The category breadcrumb displayed on the arrival page."),
    ("checked_on", "Last verified on", "Date the link and official Amazon listing were checked directly."),
]


def _short(p):
    if not p.get("brand"):
        return p["ref"]
    return f"{p['brand']} {p.get('format_label', '')}".strip()


def _register_table(d, products, caption):
    rows = []
    for p in products:
        link_cell = product_link(
            d, p["submitted_link"], esc(p["submitted_code"]),
            aria=f"Open submitted link {p['ref']} (affiliate link, opens in a new tab)")
        intended_cell = blank(p.get("intended_asin"), "not confirmed by account owner — never inferred from 9-character slug")
        if p["observed_asin"]:
            listing = product_link(
                d, p["listing_url"], esc(p["observed_asin"]),
                aria=f"Open the official Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")
            name = esc(_short(p))
            cat = esc(p.get("category_label") or "")
            status = '<span class="pill pill-ok">Observed</span>'
        else:
            listing = '<span class="blank">&mdash;</span>'
            name = '<span class="blank">&mdash;</span>'
            cat = '<span class="blank">&mdash;</span>'
            status = '<span class="pill pill-warn">Unresolved</span>'
        rows.append([
            {"html": f'<a href="{esc(rel(d, "products/" + p["ref"].lower() + ".html"))}"><strong>{esc(p["ref"])}</strong></a>'},
            {"html": cat},
            {"html": link_cell},
            {"html": intended_cell},
            {"html": listing},
            {"html": name},
            {"html": status},
        ])

    return table(
        ["Ref", "Category", "Submitted link", "Intended ASIN", "Observed ASIN (source)", "Product", "Status"],
        rows, cls="register",
        caption=caption,
        note="Intended ASIN and Observed ASIN are stored in separate columns and never merged (FLG-001). Every observed row links directly to the official Amazon.com listing; prices, ratings and availability remain blank by Program Policies §2(b) (SRC-02)."
    )


def build_register(page_dir, products, meta):
    d = page_dir
    n_total = len(products)
    n_ok = sum(1 for p in products if p.get("observed_asin"))
    n_unres = n_total - n_ok
    n_af = sum(1 for p in products if p.get("category") == "air-fryers")
    n_th = sum(1 for p in products if p.get("category") == "thermometers")

    tbl = _register_table(d, products, f"All {n_total} submitted links verified against Amazon.com on 20 November 2026")

    body = f"""{pagehead(
        'The register',
        'Five submitted links,<br>verified one by one',
        'Every submitted link, its separate intended-ASIN field, the live Amazon listing it actually reached, and the fields left blank where no permitted source exists.',
        meta=f'Verified 20 November 2026 &middot; {n_total} links &middot; {n_ok} observed &middot; {n_af} Air Fryers &middot; {n_th} Meat Thermometers &middot; 0 tested',
    )}
{section(f'''
<div class="cat-bar" aria-label="Filter by category">
  <a class="cat-pill cat-pill-active" href="{esc(rel(d, 'products/index.html'))}">All products ({n_total})</a>
  <a class="cat-pill" href="{esc(rel(d, 'products/air-fryers.html'))}">Air Fryers ({n_af})</a>
  <a class="cat-pill" href="{esc(rel(d, 'products/thermometers.html'))}">Meat Thermometers ({n_th})</a>
  <a class="cat-pill" href="{esc(rel(d, 'compare/index.html'))}">Side-by-side comparison</a>
</div>
<div class="reg-lede">
  <div>
    <h2>Product-intent confirmation register</h2>
    <p>All five submitted short links were opened directly against Amazon.com and transcribed on 20 November 2026. Three resolve to Air Fryers (P-01, P-02, P-03) and two resolve to Meat Thermometers (P-04, P-05).</p>
    <p>Nothing in this table was inferred. Intended ASIN stays blank until confirmed inside Associates Central; observed redirect targets sit in their own column and are never merged with intended ASINs.</p>
  </div>
  <dl class="reg-stats">
    <div><dt>Links submitted</dt><dd>{n_total}</dd></div>
    <div><dt>Observed live listings</dt><dd>{n_ok}</dd></div>
    <div><dt>Unresolved</dt><dd>{n_unres}</dd></div>
    <div><dt>Categories</dt><dd>2</dd></div>
    <div><dt>Tested here</dt><dd>0</dd></div>
  </dl>
</div>
{tbl}''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Category 01 · Air Fryers')}<h2>Three countertop air-fryer formats</h2></div>
<p><a class="tlink" href="{esc(rel(d, 'products/air-fryers.html'))}">Open Air Fryers category page <span aria-hidden="true">&rarr;</span></a></p></div>
<div class="pcard-grid pcard-grid-3">
{''.join(product_card(d, p) for p in products if p.get('category') == 'air-fryers')}
</div>''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Category 02 · Meat Thermometers')}<h2>Two probe formats: instant-read &amp; wireless</h2></div>
<p><a class="tlink" href="{esc(rel(d, 'products/thermometers.html'))}">Open Meat Thermometers category page <span aria-hidden="true">&rarr;</span></a></p></div>
<div class="pcard-grid wide">
{''.join(product_card(d, p) for p in products if p.get('category') == 'thermometers')}
</div>''', cls='')}
{section(f'''
{eyebrow('Reading the register')}
<h2>Four things a reviewer should check</h2>
<ol class="tight">
  <li><strong>The submitted codes are nine characters; the arrival ASINs are ten.</strong> B04G1MEwY, B02NbDxp3, B00hJ57DV, B0c8moW59 and B0f3GKalj all contain lowercase letters and are 9 characters long. Every ASIN that loaded is 10 uppercase characters. The two fields stay separate (<a href="{esc(rel(d, 'review/index.html'))}#FLG-001">FLG-001</a>).</li>
  <li><strong>Attribution is still unconfirmed.</strong> No arrived-at page showed a <code class="code">tag=</code> parameter. That does not prove the short links are untagged, because a redirector may apply tracking server-side, but it means attribution to <code class="code">shopnow047c-20</code> requires a live click test in Associates Central (<a href="{esc(rel(d, 'review/index.html'))}#FLG-002">FLG-002</a>).</li>
  <li><strong>Intermittent short-link gating happened.</strong> P-04 initially hit Amazon&rsquo;s <code class="code">/checkpoint/continue</code> interstitial three times before resolving cleanly on two independent re-verifications to <code class="code">B0DHZTCNR5</code> (<a href="{esc(rel(d, 'review/index.html'))}#FLG-004">FLG-004</a>).</li>
  <li><strong>Empty columns are required by policy.</strong> Price, star rating, review count and stock status require Amazon-served data or PA API / Creators API access (SRC-02). Neither is connected, so they stay blank site-wide.</li>
</ol>''', cls='section-tint')}
"""
    return page(
        d,
        title="Product register \u2014 Crisp & Counter",
        description="All five submitted Amazon links verified on 20 November 2026: 3 Air Fryers and 2 Meat Thermometers, with intended ASIN and observed redirect target kept in separate columns.",
        body=body,
        active="products/index.html",
        canonical="products/",
    )


def build_category(page_dir, products, *, slug, label, kicker, headline, dek, note_html, meta):
    d = page_dir
    cat_products = [p for p in products if p.get("category") == slug]
    cat_guides = [g for g in GUIDES if g.get("category") == slug]
    n_total = len(products)
    n_af = sum(1 for p in products if p.get("category") == "air-fryers")
    n_th = sum(1 for p in products if p.get("category") == "thermometers")

    grid_cls = "pcard-grid pcard-grid-3" if len(cat_products) == 3 else "pcard-grid wide"
    tbl = _register_table(d, cat_products, f"Verified {label} listings ({len(cat_products)} of {n_total} submitted links)")

    body = f"""{pagehead(
        kicker,
        headline,
        dek,
        meta=f'{len(cat_products)} verified listings &middot; Amazon breadcrumb verified 20 November 2026 &middot; 0 tested &middot; no prices shown',
    )}
{section(f'''
<div class="cat-bar" aria-label="Filter by category">
  <a class="cat-pill" href="{esc(rel(d, 'products/index.html'))}">All products ({n_total})</a>
  <a class="cat-pill{' cat-pill-active' if slug == 'air-fryers' else ''}" href="{esc(rel(d, 'products/air-fryers.html'))}">Air Fryers ({n_af})</a>
  <a class="cat-pill{' cat-pill-active' if slug == 'thermometers' else ''}" href="{esc(rel(d, 'products/thermometers.html'))}">Meat Thermometers ({n_th})</a>
  <a class="cat-pill" href="{esc(rel(d, 'compare/index.html'))}">Side-by-side comparison</a>
</div>
<div class="{grid_cls}">
  {''.join(product_card(d, p) for p in cat_products)}
</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Verified findings table')}<h2>{esc(label)} register</h2></div>
<p>Every row carries its official Amazon.com source link and keeps intended ASIN separate from observed ASIN.</p></div>
{tbl}
{note_html}''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Category guides')}<h2>Read before you click</h2></div>
<p>Question-shaped guides tailored to {esc(label.lower())}.</p></div>
<div class="gcard-grid">
  {''.join(guide_card(d, g) for g in cat_guides)}
</div>''', cls='')}"""

    return page(
        d,
        title=f"{label} \u2014 Crisp & Counter",
        description=dek,
        body=body,
        active="products/index.html",
        canonical=f"products/{slug}.html",
    )


def build_product(page_dir, p, meta):
    d = page_dir
    if p["identity_confidence"] == "unresolved":
        return _build_unresolved(d, p)

    short = _short(p)
    facts = []
    for key, label, note in FIELDS:
        value = p.get(key)
        if key == "submitted_link":
            cell = product_link(d, value, esc(value), aria=f"Open submitted link for {p['ref']} (affiliate link, opens in a new tab)")
        elif key == "observed_asin":
            cell = product_link(d, p["listing_url"], esc(value), aria=f"Open the official Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")
        elif key == "intended_asin":
            cell = blank(value, "not confirmed by account owner — never merged with observed ASIN")
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

    is_thermo = p.get("category") == "thermometers"
    cat_href = rel(d, "products/thermometers.html" if is_thermo else "products/air-fryers.html")
    cat_label = p.get("category_label") or "Products"
    guide_href = rel(d, "guides/instant-read-vs-wireless-meat-thermometer.html" if is_thermo else "guides/basket-or-oven-air-fryer.html")
    guide_label = "Instant-read vs. wireless + USDA chart" if is_thermo else "Basket or oven?"

    attention_html = ""
    if p.get("attention"):
        attention_html = f'<div class="callout"><h2>Category note</h2><p>{esc(p["attention"])}</p></div>'

    body = f"""{_producthead(p, short, meta)}
<section class="section"><div class="wrap record-grid">
  <div class="record-main">
    {photo}
    <h2>Product-intent confirmation record</h2>
    <p class="lede">Submitted link details, intended ASIN (blank until account confirmation), and the live Amazon listing observed on {esc(p['checked_on'])} are stored in separate fields and never merged.</p>
    {table(['Field', 'Recorded value'], facts, cls='fields', caption=f"Confirmation record for {p['ref']}")}

    <h2>What the seller states, in the seller&rsquo;s words</h2>
    <p class="lede">These are not test results. They are the claims written into the listing title by whoever sells the product, transcribed once and never paraphrased into something stronger.</p>
    <ul class="claims">{stated_html}</ul>

    {attention_html}

    <h2>What was not established</h2>
    <p class="lede">Each row below is a field a shopper would normally expect to see. None of them has a source this build is permitted to use, so none of them is filled in.</p>
    {table(['Field', 'Value', 'Reason'], not_stated, cls='fields')}

    <h2>How the link was checked</h2>
    <p>{esc(p['resolution_note'])}</p>
    <p>The submitted link was opened; the page it landed on was read; the ASIN inside the address, the breadcrumb category, and the listing title were transcribed into this record. That establishes destination identity. It does not establish quality, price or availability.</p>

    <div class="cta">
      <div>
        <p class="cta-label">Amazon listing &middot; Paid link</p>
        <p>Opens in a new tab. Marked <code class="code">rel=&quot;sponsored nofollow noopener&quot;</code>.</p>
      </div>
      {product_link(d, p['listing_url'], 'See the listing on Amazon <span aria-hidden="true">&#8599;</span>', cls='btn', aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")}
    </div>
    <p class="fineprint">{DISCLOSURE} A purchase through this link does not change the price you pay. Whether a click is credited to this site&rsquo;s tracking ID is not confirmed &mdash; see <a href="{esc(rel(d, 'review/index.html'))}#FLG-002">FLG-002</a>.</p>
  </div>

  <aside class="record-side">
    <div class="side-card">
      <h2>At a glance</h2>
      <dl class="side-dl">
        <div><dt>Reference</dt><dd>{esc(p['ref'])}</dd></div>
        <div><dt>Category</dt><dd><a href="{esc(cat_href)}">{esc(cat_label)}</a></dd></div>
        <div><dt>Brand</dt><dd>{esc(p['brand'])}</dd></div>
        <div><dt>Format</dt><dd>{esc(p['format_label'])}</dd></div>
        <div><dt>Observed ASIN</dt><dd><code class="code">{esc(p['observed_asin'])}</code></dd></div>
        <div><dt>Intended ASIN</dt><dd><span class="blank" title="not confirmed">&mdash;</span></dd></div>
        <div><dt>Verified</dt><dd>{esc(p['checked_on'])}</dd></div>
        <div><dt>Tested by us</dt><dd><span class="pill pill-warn">No</span></dd></div>
      </dl>
    </div>
    <div class="side-card">
      <h2>Next</h2>
      <ul class="side-links">
        <li><a href="{esc(cat_href)}">All {esc(cat_label)}</a></li>
        <li><a href="{esc(rel(d, 'compare/index.html'))}">Compare all five</a></li>
        <li><a href="{esc(guide_href)}">{esc(guide_label)}</a></li>
        <li><a href="{esc(rel(d, 'questions/index.html'))}">What is still unknown</a></li>
      </ul>
    </div>
    <div class="side-card side-card-quiet">
      <h2>Read this before trusting the page</h2>
      <p>No product on this site has been bought, used or measured. The photograph above is a labelled editorial illustration. The guides tell you what to check; they cannot tell you that this model passed the check.</p>
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
        description=f"{p['ref']}: the submitted link, the Amazon listing it reached ({p['observed_asin']}), the seller's stated attributes, and every field left blank.",
        body=body,
        active="products/index.html",
        canonical=f"products/{p['ref'].lower()}.html",
        structured=structured,
        og_type="article",
    )


def _producthead(p, short, meta):
    return pagehead(
        f"Record {p['ref']} &middot; {p.get('category_label') or ''} &middot; checked {p['checked_on']}",
        f"{esc(short)}<br><span class='head-asin'>{esc(p['observed_asin'])}</span>",
        f"<strong>{esc(p['brand'])}</strong> &middot; {esc(p['format_label'])}. This record separates submitted link, intended ASIN, observed listing, seller claims, and unverified fields.",
        meta='<span class="pill pill-ok">Destination observed</span> <span class="pill pill-warn">Not tested</span> <span class="pill">No price shown</span>',
    )


def _build_unresolved(d, p):
    body = f"""{pagehead(
        f"Record {p['ref']} &middot; unresolved",
        "This link did not<br>open a product",
        "Rather than fill the gap, the gap is published.",
        meta='<span class="pill pill-warn">Unresolved</span> <span class="pill">No product invented</span>',
    )}
<section class="section"><div class="wrap narrow">
  <h2>What was attempted</h2>
  <p>{esc(p['resolution_note'])}</p>
  <div class="cta">
    <div><p class="cta-label">Still open</p><p>This product has no card, no photograph and no buy link until it can be identified.</p></div>
    <a class="btn btn-ghost" href="{esc(rel(d, 'review/index.html'))}#FLG-004">See the flag</a>
  </div>
</div></section>"""
    return page(
        d,
        title=f"Unresolved link \u2014 record {p['ref']}",
        description=f"{p['ref']} did not open a product page. This record shows what was attempted and why nothing was filled in.",
        body=body,
        active="products/index.html",
        canonical=f"products/{p['ref'].lower()}.html",
    )
