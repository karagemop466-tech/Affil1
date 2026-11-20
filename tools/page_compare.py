"""The comparison table. Blanks are shown as blanks."""

from layout import (blank, esc, eyebrow, page, pagehead, product_link, rel,
                    section, table)
from content import COMPARE_COLUMNS


def build(page_dir, products, meta):
    d = page_dir
    rows = []
    for p in products:
        r = {
            'ref': p['ref'], 'brand': p.get('brand'), 'shape': p.get('format_label'),
            'capacity': p.get('stated_capacity'), 'attributes': p.get('stated_attributes'),
            'asin': p.get('observed_asin'),
        }
        if r["asin"]:
            listing = product_link(
                d, f"https://www.amazon.com/dp/{r['asin']}", esc(r["asin"]),
                aria=f"Open the Amazon listing for {r['ref']} (opens in a new tab)")
            cap = blank(r["capacity"], "not applicable")
            attrs = esc(r["attributes"])
            shape = esc(r["shape"])
            brand = esc(r["brand"])
            status = '<span class="pill pill-ok">Observed</span>'
        else:
            listing = blank(None, "the link never reached a product page")
            cap = attrs = shape = brand = blank(None, "not identified")
            status = '<span class="pill pill-warn">Unresolved</span>'
        rows.append([
            {"html": f'<a href="{esc(rel(d, "products/" + r["ref"].lower() + ".html"))}"><strong>{esc(r["ref"])}</strong></a>'},
            {"html": brand},
            {"html": shape},
            {"html": cap},
            {"html": attrs},
            {"html": listing},
            {"html": status},
        ])

    tbl = table(
        ["Ref", "Brand", "Shape", "Stated capacity", "Stated attributes", "ASIN reached", "Status"],
        rows, cls="compare",
        caption="Listing details, side by side",
        note="Every word in the capacity and attribute columns is the seller's own wording from the listing title. None of it has been verified by testing, and no product was measured.",
    )

    body = f"""{pagehead(
        'Compare',
        'Compare by how you cook',
        'Three air fryers and two thermometers. Compare designs and listing details, then check the fit and cleanup trade-offs that matter to you.',
        meta='No price column &middot; no rating column &middot; no winner column &middot; on purpose',
    )}
{section(f'''
<div class="lede-prose">
  <p>Start with the job: two separate foods, one wider batch, or a tray you already own. For thermometers, decide whether you need a quick spot-check or a probe that stays in while you cook.</p>
  <p>What the table can do is put the sellers' claims next to each other so the shape of the choice is visible. Read the capacity column and you can see a dual-basket machine quoting six quarts across two three-quart baskets sitting beside a single eight-quart basket and a twenty-six-quart oven. Those numbers describe three different kinds of container, which is exactly why a single capacity figure is a poor way to compare.</p>
</div>
{tbl}''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Reading the table honestly')}<h2>What the columns are not</h2></div></div>
<div class="rule-grid">
  <div class="rule"><span class="rule-n">01</span><h3>The capacity column is a claim</h3><p>Quarts are quoted by the seller and transcribed here unchanged. No basket, cavity or portion was measured. A quart of volume and a quart of usable cooking surface are not the same thing.</p></div>
  <div class="rule"><span class="rule-n">02</span><h3>The attribute column is marketing copy</h3><p>"Sync finish", "one-touch presets" and "dishwasher-safe" are the seller's phrases. Whether a preset produces good food, or a coating survives your dishwasher, is not something a title can tell you.</p></div>
  <div class="rule"><span class="rule-n">03</span><h3>The empty columns are the honest ones</h3><p>Price, rating, review count and stock would be the most useful columns on the page. We do not have an approved source for publishing dynamic listing data. <a href="{esc(rel(d, 'about/index.html'))}#why-blank">The rule, quoted from the source</a>.</p></div>
</div>''', cls='')}
{section(f'''
<div class="callout">
  <h2>A comparison you can actually finish</h2>
  <p>Measure the space you have. Write down the meal you cook most. Then answer one question for each product: does my usual meal fit in one layer of this thing?</p>
  <p class="callout-links"><a class="btn" href="{esc(rel(d, 'guides/basket-or-oven-air-fryer.html'))}">Basket or oven</a> <a class="btn btn-ghost" href="{esc(rel(d, 'guides/air-fryer-capacity-checklist.html'))}">Capacity checklist</a></p>
</div>''', cls='')}"""
    return page(
        d,
        title="Compare the five \u2014 Crisp & Counter",
        description="The five submitted products side by side: brand, shape, the capacity and attributes their sellers state, the ASIN each link reached, and the fields left blank.",
        body=body,
        active="compare/index.html",
        canonical="compare/",
    )
