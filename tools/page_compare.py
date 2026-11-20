"""Side-by-side comparison. Blank cells are the design, not a bug."""

from layout import (blank, breadcrumb_schema, buy_url, esc, eyebrow, page,
                    pagehead, product_link, rel, section, table)
from content import COMPARE_COLUMNS


def build(page_dir, products, meta):
    d = page_dir

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
        if col in ("Price", "Rating"):
            return {"html": blank(None)}
        if col == "Listing":
            return {"html": product_link(
                d, buy_url(p["observed_asin"]), "See it <span aria-hidden=\"true\">&#8599;</span>",
                cls="tlink", aria=f"Open the Amazon listing for {p['ref']} (paid link, opens in a new tab)")}
        return {"html": ""}

    headers = [c[0] for c in COMPARE_COLUMNS] + ["Listing"]
    rows = [[cell(p, c[0]) for c in COMPARE_COLUMNS] + [cell(p, "Listing")] for p in products]

    tbl = table(headers, rows, cls="compare",
                caption="All five, side by side, on 20 November 2026",
                note="Stated size and features are the sellers' own words from the listing titles. Price and rating are blank because Amazon serves that data and this site holds no permitted feed for it.")

    body = f"""{pagehead(
        'Compare',
        'Five things,<br>one table',
        'The whole edit on one screen. Two columns are deliberately empty: price and rating live on Amazon and change hourly, and a static page cannot show them without breaking a rule or going stale.',
        meta='Seller-stated values only &middot; no measured figures &middot; no winners declared',
    )}
{section(f'''
<div class="sec-head"><div>{eyebrow('The table')}<h2>Everything the listings state</h2></div>
<p>Read across a row to see one product. Read down a column to see what is genuinely comparable.</p></div>
{tbl}''', cls='')}
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
</div>''', cls='section-tint')}
{section(f'''
<div class="callout">
  <h2>Why the price column is empty on a comparison page</h2>
  <p>Because a comparison is exactly where a wrong price does the most damage. Amazon permits a site to show price and availability only when Amazon serves that data into the page, or when it arrives through the official product APIs. This site is a set of static files and has neither.</p>
  <p class="callout-links"><a class="tlink" href="{esc(rel(d, 'about/index.html#why-blank'))}">Read the rule and its source <span aria-hidden="true">&rarr;</span></a></p>
</div>''', cls='')}"""
    return page(
        d,
        title="Compare the five \u2014 air fryers and thermometers | Crisp & Counter",
        description="Every product in the edit side by side: shape, stated capacity, stated features, with price and rating deliberately blank and a link to each live listing.",
        body=body,
        active="compare/index.html",
        canonical="compare/",
        structured=breadcrumb_schema([], "Compare", "compare/"),
    )
