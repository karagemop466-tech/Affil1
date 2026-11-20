"""The comparison table. Blanks are shown as blanks."""

from layout import (blank, esc, eyebrow, page, pagehead, product_link, rel,
                    section, table)


def build(page_dir, products, meta):
    d = page_dir
    rows = []
    for p in products:
        r = {
            'ref': p['ref'], 'brand': p.get('brand'),
            'category': p.get('category_label'),
            'shape': p.get('format_label'),
            'capacity': p.get('stated_capacity'),
            'attributes': p.get('stated_attributes'),
            'asin': p.get('observed_asin'),
        }
        if r["asin"]:
            listing = product_link(
                d, f"https://www.amazon.com/dp/{r['asin']}", esc(r["asin"]),
                aria=f"Open the Amazon listing for {r['ref']} (affiliate link, opens in a new tab)")
            cap = esc(r["capacity"])
            attrs = esc(r["attributes"])
            shape = esc(r["shape"])
            brand = esc(r["brand"])
            cat = esc(r["category"])
            status = '<span class="pill pill-ok">Observed</span>'
        else:
            listing = blank(None, "the link never reached a product page")
            cap = attrs = shape = brand = cat = blank(None, "not identified")
            status = '<span class="pill pill-warn">Unresolved</span>'
        rows.append([
            {"html": f'<a href="{esc(rel(d, "products/" + r["ref"].lower() + ".html"))}"><strong>{esc(r["ref"])}</strong></a>'},
            {"html": cat},
            {"html": brand},
            {"html": shape},
            {"html": cap},
            {"html": attrs},
            {"html": listing},
            {"html": status},
        ])

    tbl = table(
        ["Ref", "Category", "Brand", "Format", "Stated capacity", "Stated attributes", "Observed ASIN", "Status"],
        rows, cls="compare",
        caption="All five verified listings side by side, with nothing measured",
        note="Every word in the capacity and attribute columns is the seller's own wording from the Amazon listing title verified on 2026-11-20. None of it has been verified by hands-on testing, and prices/ratings stay blank under Program Policies §2(b) (SRC-02).",
    )

    body = f"""{pagehead(
        'Compare',
        'Side by side,<br>with nothing measured',
        'Five verified listings across two categories (3 Air Fryers, 2 Meat Thermometers). The sellers&rsquo; own claims sit beside the official Amazon ASIN reached &mdash; with zero invented prices, scores or winners.',
        meta='5 of 5 observed &middot; no price column &middot; no rating column &middot; no winner column &middot; on purpose',
    )}
{section(f'''
<div class="lede-prose">
  <p>Most comparison tables rank things. This one cannot, because nothing here was tested, and a rank without a test is an opinion dressed as a measurement.</p>
  <p>What the table can do is put the sellers&rsquo; stated formats next to each other across both categories. In Air Fryers you can see a dual-basket machine quoting six quarts across two three-quart drawers beside a single eight-quart basket and a twenty-six-quart French-door oven. In Meat Thermometers you can see an instant-read handheld probe beside a leave-in three-probe wireless kit.</p>
</div>
{tbl}''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Reading the table honestly')}<h2>What the columns are not</h2></div></div>
<div class="rule-grid">
  <div class="rule"><span class="rule-n">01</span><h3>The capacity column is a claim</h3><p>Quarts are quoted by the seller and transcribed here unchanged. No basket, cavity or portion was measured. A quart of volume and a quart of usable cooking surface are not the same thing.</p></div>
  <div class="rule"><span class="rule-n">02</span><h3>The attribute column is seller copy</h3><p>&ldquo;Sync finish&rdquo;, &ldquo;1-second read&rdquo; and &ldquo;WiFi unlimited range&rdquo; are the sellers&rsquo; phrases. Whether a preset cooks evenly or a probe meets its stated accuracy requires independent testing.</p></div>
  <div class="rule"><span class="rule-n">03</span><h3>The missing columns are the honest ones</h3><p>Price, rating, review count and stock would be the most useful columns on the page. They are absent because Amazon permits them only from data Amazon serves or via its API. <a href="{esc(rel(d, 'about/index.html'))}#why-blank">The rule, quoted from the source</a>.</p></div>
</div>''', cls='section-tint')}
{section(f'''
<div class="callout">
  <h2>A comparison you can actually finish</h2>
  <p>Measure the counter space you have, write down the meal you cook most, and decide whether you need an instant-read spot-check or a leave-in wireless probe.</p>
  <p class="callout-links">
    <a class="btn" href="{esc(rel(d, 'guides/basket-or-oven-air-fryer.html'))}">Basket or oven</a>
    <a class="btn btn-ghost" href="{esc(rel(d, 'guides/instant-read-vs-wireless-meat-thermometer.html'))}">Instant-read or wireless</a>
    <a class="btn btn-ghost" href="{esc(rel(d, 'products/air-fryers.html'))}">Air Fryers</a>
    <a class="btn btn-ghost" href="{esc(rel(d, 'products/thermometers.html'))}">Meat Thermometers</a>
  </p>
</div>''', cls='')}"""
    return page(
        d,
        title="Compare all five \u2014 Crisp & Counter",
        description="All five verified products side by side across Air Fryers (3) and Meat Thermometers (2): brand, format, seller-stated attributes, observed ASIN, and why prices and ratings remain blank.",
        body=body,
        active="compare/index.html",
        canonical="compare/",
    )
