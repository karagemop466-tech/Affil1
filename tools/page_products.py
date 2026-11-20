"""The shop: a category index and one page per product.

The product page leads with what the thing is and who it is for. Verification
sits underneath as a short, factual block, not as the headline. Every figure on
the page is either transcribed from the listing title or visibly blank.
"""

from layout import (AMAZON_NOTE, blank, breadcrumbs, breadcrumb_schema, buy_url,
                    esc, eyebrow, link, outbound, page, pagehead, product_link,
                    rel, section, table)
from page_home import img, product_card


def _by_category(products):
    order = ["air-fryers", "thermometers"]
    labels = {"air-fryers": ("Air fryers", "Three machines, three shapes. Pick the shape first."),
              "thermometers": ("Thermometers", "The cheapest way to know the middle is done.")}
    groups = {}
    for p in products:
        groups.setdefault(p.get("category", "other"), []).append(p)
    out = []
    for key in order:
        if key in groups:
            out.append((key, labels[key][0], labels[key][1], groups[key]))
    return out


def build_register(page_dir, products, meta):
    d = page_dir
    groups = _by_category(products)

    rows = []
    for p in products:
        rows.append([
            {"html": f'<strong>{esc(p["ref"])}</strong>'},
            {"html": esc(f"{p['brand']} {p['format_label']}")},
            {"html": esc(p.get("stated_capacity") or "")},
            {"html": blank(None)},
            {"html": blank(None)},
            {"html": product_link(
                d, buy_url(p["observed_asin"]), "See it <span aria-hidden=\"true\">&#8599;</span>",
                cls="tlink", aria=f"Open the Amazon listing for {p['ref']} (paid link, opens in a new tab)")},
        ])
    tbl = table(
        ["Ref", "Product", "Stated size", "Price", "Rating", "Listing"],
        rows, cls="register",
        caption="All five picks, with the two columns we refuse to fill",
        note="Price and rating are blank by rule, not by accident: Amazon serves that data and this site has no permitted feed for it. Every cell that does carry a value was transcribed from the listing title reached on 20 November 2026.",
    )

    cats = ""
    for key, label, blurb, items in groups:
        cats += section(f"""
<div class="sec-head">
  <div>{eyebrow(label)}<h2>{esc(label)}</h2></div>
  <p>{esc(blurb)}</p>
</div>
<div class="pcard-grid {'three' if len(items) == 3 else 'two'}">
{''.join(product_card(d, p) for p in items)}
</div>""", cls="shop" if key == "air-fryers" else "shop section-tint")

    glance = section(
        '<div class="sec-head"><div>' + eyebrow('At a glance') + '<h2>Everything in one table</h2></div>'
        '<p>The whole catalogue, including the two columns that stay empty and why.</p></div>'
        + tbl, cls="")

    callout = section(
        '<div class="callout">'
        '<h2>Why there is no price on this page</h2>'
        "<p>Amazon's Associates policies only allow a site to display price and availability when Amazon itself serves that data into the page, or when it arrives through the official product APIs. This site is static and has neither, so it shows none. A number copied onto a page is a number that goes stale; the listing is always current.</p>"
        '<p>The same rule covers star ratings, review counts and stock status. It is a shorter page than you are used to. It is also a page that cannot be wrong about a price.</p>'
        '<p class="callout-links"><a class="tlink" href="'
        + esc(rel(d, "about/index.html#why-blank"))
        + '">The policy, quoted <span aria-hidden="true">&rarr;</span></a></p>'
        "</div>", cls="")

    body = "".join([
        pagehead(
            "The edit",
            "Five things,<br>chosen for a reason",
            "Every link below was opened, followed to its Amazon listing and matched to the product named here. Two drawers, one basket, one door, two probes \u2014 and a plain explanation of who each one is for.",
            meta="Checked 20 November 2026 &middot; 5 of 5 identified &middot; no prices or ratings copied",
        ),
        cats, glance, callout,
    ])
    return page(
        d,
        title="The edit \u2014 five air fryers and thermometers | Crisp & Counter",
        description="The full shortlist: two basket air fryers, one French-door air fryer oven and two meat thermometers, each with a checked Amazon listing and a plain note on who it suits.",
        body=body,
        active="products/index.html",
        canonical="products/",
        structured=breadcrumb_schema([], "The edit", "products/"),
    )


def build_product(page_dir, p, meta):
    d = page_dir
    ref = p["ref"].lower()
    href = f"products/{ref}.html"
    asin = p["observed_asin"]
    pairs = None

    details = table(
        ["What the listing states", "Detail"],
        [[k, v] for k, v in [
            ("Brand", p["brand"]),
            ("Shape", p["format_label"]),
            ("Stated size", p.get("stated_capacity")),
            ("Stated features", p.get("stated_attributes")),
            ("Category on arrival", p["category_path"]),
            ("Listing title", p["listing_title"]),
        ]],
        cls="record",
        caption="Transcribed from the page the submitted link reached, 20 November 2026",
        note="Seller wording, repeated as stated. Nothing in this table was measured, inferred or tidied up.",
    )

    suits = "".join(f"<li>{esc(s)}</li>" for s in p.get("suits", []))
    skip = p.get("skip_if") or ""
    skip_html = (f'<div class="skip-block"><p class="q-label">Look elsewhere if</p><p>{esc(skip)}</p></div>'
                 if skip else "")

    body = f"""{breadcrumbs(d, [("products/index.html", "The edit")])}
<header class="product-hero"><div class="wrap">
  <div class="product-media">
    {img(d, p['photo'], p['photo_alt'], sizes='(max-width:820px) 100vw, 540px', loading='eager')}
    <span class="illus-tag">Illustration</span>
    <p class="fig-note">{esc(p['photo_note'])}</p>
  </div>
  <div class="product-copy">
    {eyebrow(p['brand'] + ' · ' + p['format_label'])}
    <h1>{esc(p['name'])}</h1>
    <p class="product-sub">{esc(p['listing_title_clean'])}</p>
    <p class="product-why">{esc(p['why'])}</p>
    <p class="product-buy">
      {product_link(d, buy_url(asin), 'See it on Amazon <span aria-hidden="true">&#8599;</span>', cls='btn', aria=f"Open the Amazon listing for {p['brand']} {p['format_label']} (paid link, opens in a new tab)")}
    </p>
    <p class="product-fine">Paid link &middot; {esc(AMAZON_NOTE)} &middot; tag <code>{esc(meta['tracking'])}</code></p>
    <dl class="fact-list">
      <div><dt>Stated size</dt><dd>{esc(p.get('stated_capacity') or '—')}</dd></div>
      <div><dt>Also stated</dt><dd>{esc((p.get('stated_attributes') or '—').split(';')[0])}</dd></div>
      <div><dt>Best for</dt><dd>{esc((p.get('suits') or ['—'])[0])}</dd></div>
    </dl>
  </div>
</div></header>
{section(f'''
<div class="record-grid">
  <div class="record-main">
    <h2>What it is, in plain terms</h2>
    <p>{esc(p['why'])}</p>
    <p>{esc(p['edit_note'])}</p>
    <h2 class="mt">Who it suits</h2>
    <ul class="suits">{suits}</ul>
    {skip_html}
  </div>
  <div class="record-side">
    <div class="side-card">
      <p class="q-label">At a glance</p>
      <dl class="side-dl">
        <div><dt>Shape</dt><dd>{esc(p['format_label'])}</dd></div>
        <div><dt>Stated size</dt><dd>{esc(p.get('stated_capacity') or '—')}</dd></div>
        <div><dt>Price</dt><dd><span class="blank">On Amazon</span></dd></div>
        <div><dt>Rating</dt><dd><span class="blank">On Amazon</span></dd></div>
        <div><dt>Checked</dt><dd>{esc(p['checked_on'])}</dd></div>
      </dl>
      {product_link(d, buy_url(asin), 'Check it on Amazon <span aria-hidden="true">&#8599;</span>', cls='btn btn-small', aria=f"Open the Amazon listing for {p['ref']} (paid link, opens in a new tab)")}
    </div>
  </div>
</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The record')}<h2>What the listing states</h2></div>
<p>Everything below is the seller's own description. It is the whole of what this page knows for certain.</p></div>
{details}''', cls='section-tint')}
{_verification(d, p, asin)}
{_pairs(d, p, meta)}"""
    return page(
        d,
        title=f"{p['brand']} {p['format_label']} \u2014 the note | Crisp & Counter",
        description=f"{p['name']}: {p['why'][:150]}",
        body=body,
        active="products/index.html",
        canonical=href,
        og_type="article",
        structured=[
            breadcrumb_schema([("products/index.html", "The edit")], p["name"], href),
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": f"{p['brand']} {p['format_label']}",
                "description": p["why"],
                "dateModified": "2026-11-20",
                "publisher": {"@type": "Organization", "name": "Crisp & Counter"},
                "mainEntityOfPage": f"https://karagemop466-tech.github.io/Affil1/{href}",
            },
        ],
    )


def _verification(d, p, asin):
    return section(f"""
<div class="sec-head"><div>{eyebrow('Provenance')}<h2>How this link was checked</h2></div>
<p>Short, because it is a receipt rather than a story.</p></div>
<div class="verify-strip">
  <div><span class="verify-k">Supplied</span><code>{esc(p['submitted_link'])}</code></div>
  <div><span class="verify-k">Opened</span><span>{esc(p['checked_on'])}</span></div>
  <div><span class="verify-k">Landed on</span><code>/dp/{esc(asin)}</code></div>
  <div><span class="verify-k">Paid link</span><code>tag={esc('shopnow047c-20')}</code></div>
</div>
<p class="verify-note">{esc(p['resolution_note'])} The nine-character code in the supplied link is a short-link slug, not an ASIN, so no intended ASIN is recorded. <a class="tlink" href="{esc(rel(d, 'review/index.html'))}">Everything still unverified <span aria-hidden="true">&rarr;</span></a></p>""",
                   cls="")


def _pairs(d, p, meta):
    ref = p.get("pairs_with")
    if not ref:
        return ""
    import json
    import pathlib
    root = pathlib.Path(__file__).resolve().parent.parent
    doc = json.loads((root / "src/data/products.json").read_text(encoding="utf-8"))
    other = next((x for x in doc["products"] if x["ref"] == ref), None)
    if not other:
        return ""
    return section(f"""
<div class="crosslink">
  <div>
    {eyebrow('Pairs with')}
    <h2>{esc(other['name'])}</h2>
    <p>{esc(other['why'])}</p>
    <a class="tlink" href="{esc(rel(d, 'products/' + other['ref'].lower() + '.html'))}">Read the note <span aria-hidden="true">&rarr;</span></a>
  </div>
  <div class="crosslink-media">{img(d, other['photo'], other['photo_alt'], sizes='(max-width:720px) 100vw, 320px')}</div>
</div>""", cls="section-tint")
