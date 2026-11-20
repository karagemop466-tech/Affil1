"""Side-by-side comparison, built so a reader can act on it.

The old version carried two permanently empty columns and explained why. That is
honest but it is not a comparison. This version compares the things a listing
actually states \u2014 format, stated capacity, cooking surfaces, stated features \u2014
and puts the price question where it belongs: a sponsored link to the live
listing, because Amazon permits price display only when Amazon serves the data
(Program Policies, Participation Requirements 2(b)).
"""

from layout import (breadcrumb_schema, buy_url, esc, eyebrow, page, pagehead,
                    product_link, rel, section, table)
from content import COMPARE_COLUMNS
from page_products import decision_rows


def build(page_dir, products, meta):
    d = page_dir
    decisions, price_rule = decision_rows()

    def cell(p, col):
        if col == "Product":
            return {"html": (
                f'<a href="{esc(rel(d, "products/" + p["ref"].lower() + ".html"))}">'
                f'<strong>{esc(p["name"])}</strong></a>'
                f'<br><span class="tiny">{esc(p["brand"])} &middot; {esc(p["ref"])}</span>')}
        if col == "Shape":
            return {"html": esc(p["format_label"])}
        if col == "Stated size":
            return {"html": esc(p.get("stated_capacity") or "")}
        if col == "Stated features":
            return {"html": esc(p.get("stated_attributes") or "")}
        if col == "Price":
            return {"html": '<span class="blank" title="Amazon serves the price into the listing">On the listing</span>'}
        if col == "Rating":
            return {"html": '<span class="blank" title="Amazon serves the rating into the listing">On the listing</span>'}
        if col == "Listing":
            return {"html": product_link(
                d, buy_url(p["observed_asin"]), "See it <span aria-hidden=\"true\">&#8599;</span>",
                cls="tlink", aria=f"Open the Amazon listing for {p['ref']} (paid link, opens in a new tab)")}
        return {"html": ""}

    headers = [c[0] for c in COMPARE_COLUMNS] + ["Listing"]
    rows = [[cell(p, c[0]) for c in COMPARE_COLUMNS] + [cell(p, "Listing")] for p in products]

    tbl = table(headers, rows, cls="compare",
                caption="All five, side by side, on 20 November 2026",
                note="Stated size and features are the sellers' own words from the listings reached on 20 November 2026. Price and rating sit on the listing, where Amazon maintains them; this site holds no permitted feed for either.")

    # A second, purpose-built table: the decision, not the specification.
    dec_rows = []
    for p in products:
        dec = decisions.get(p["ref"], {})
        dec_rows.append([
            {"html": f'<a href="{esc(rel(d, "products/" + p["ref"].lower() + ".html"))}"><strong>{esc(p["name"])}</strong></a>'},
            {"html": esc(dec.get("decision") or "")},
            {"html": esc(dec.get("check_before") or "")},
            {"html": product_link(
                d, buy_url(p["observed_asin"]), "Check price <span aria-hidden=\"true\">&#8599;</span>",
                cls="tlink", aria=f"Open the Amazon listing for {p['ref']} (paid link, opens in a new tab)")},
        ])
    dec_tbl = table(["Product", "The decision it answers", "Check before you buy", "Live price"],
                    dec_rows, cls="compare",
                    caption="The same five, sorted by the choice rather than the spec",
                    note="These are editorial trade-off notes, not test results. Nothing here was measured, and no winner is declared.")

    body = f"""{pagehead(
        'Compare',
        'Five things,<br>one table',
        'Two tables. The first is what the listings state, read across for one product and down for what is genuinely comparable. The second is the decision each product is for, because a specification is not a reason to buy.',
        meta='Seller-stated values only &middot; no measured figures &middot; no winners declared',
    )}
{section(f'''
<div class="sec-head"><div>{eyebrow('The specification')}<h2>Everything the listings state</h2></div>
<p>Read across a row to see one product. Read down a column to see what is genuinely comparable.</p></div>
{tbl}''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The decision')}<h2>What each one is actually for</h2></div>
<p>Pick the row that describes your evening, not the row with the biggest number.</p></div>
{dec_tbl}''', cls='section-tint')}
{section(f'''
<div class="compare-notes">
  <div>
    {eyebrow('How to read it')}
    <h2>Three honest observations</h2>
    <ol class="tight">
      <li><strong>Sizes are not interchangeable.</strong> P-01's 6 quarts is two 3-quart drawers; P-03's 8 quarts is one basket; P-02's 26 quarts is a different shape again. Compare like with like.</li>
      <li><strong>Thermometers have no capacity.</strong> Two of these five are probes. They are in the table so the catalogue is complete, not so they can be ranked against an oven.</li>
      <li><strong>Nothing here says which is better.</strong> No product was tested. The notes explain what each shape changes, and the rest is your kitchen.</li>
    </ol>
  </div>
  <div class="side-card">
    <p class="q-label">Choose by shape</p>
    <dl class="side-dl">
      <div><dt>One drawer</dt><dd>P-03 &mdash; one thing at a time, largest single basket</dd></div>
      <div><dt>Two drawers</dt><dd>P-01 &mdash; two foods, two temperatures, sync finish stated</dd></div>
      <div><dt>A door and racks</dt><dd>P-02 &mdash; trays, pans, layers, more counter needed</dd></div>
      <div><dt>A quick reading</dt><dd>P-04 &mdash; instant read, lives in a drawer</dd></div>
      <div><dt>A watched cook</dt><dd>P-05 &mdash; leave-in probes, app-based</dd></div>
    </dl>
  </div>
</div>''', cls='')}
{section(f'''
<div class="callout">
  <h2>Why the price column points instead of printing</h2>
  <p>Because a comparison is exactly where a wrong price does the most damage. Amazon permits a site to show price and availability only when Amazon serves that data into the page, or when it arrives through the Creators API or the Product Advertising API. This site is a set of static files and has neither.</p>
  <p>A number copied onto this page would be a number that goes stale; the listing is always current. That is why every price cell is a link.</p>
  <p class="callout-links"><a class="tlink" href="{esc(rel(d, 'about/index.html#why-blank'))}">Read the rule and its source <span aria-hidden="true">&rarr;</span></a></p>
</div>''', cls='')}"""
    return page(
        d,
        title="Compare the five \u2014 air fryers and thermometers | Crisp & Counter",
        description="Every product in the edit side by side: shape, stated capacity, stated features, and the decision each one answers, with a sponsored link to each live listing for the current price.",
        body=body,
        active="compare/index.html",
        canonical="compare/",
        structured=breadcrumb_schema([], "Compare", "compare/"),
    )
