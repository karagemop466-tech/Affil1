"""Sources and quotations: the page a reviewer opens first.

Every claim on the site that is not the site's own observation is followed back
to one of these entries. The quotation is reproduced exactly, the retrieval date
is stated, and what could not be reached is listed rather than skipped.
"""

from layout import esc, eyebrow, outbound, page, pagehead, product_link, rel, section, table


def build(page_dir, sources, products, meta):
    d = page_dir
    doc = sources if isinstance(sources, dict) else {"sources": sources}
    entries = doc.get("sources", [])
    missing = doc.get("could_not_verify", [])

    blocks = []
    for s in entries:
        quotes = [("", s.get("quote") or "")]
        if s.get("quote_2"):
            quotes.append(("", s["quote_2"]))
        if s.get("quote_3"):
            quotes.append(("", s["quote_3"]))
        q_html = "".join(f'<blockquote class="quote"><p>{esc(q)}</p></blockquote>' for _, q in quotes if q)
        blocks.append(f"""<article class="source-card" id="{esc(s['id'])}">
  <div class="source-head">
    <span class="source-id">{esc(s['id'])}</span>
    <h2>{esc(s['title'])}</h2>
    <p class="source-pub">{esc(s['publisher'])} &middot; {esc(s.get('page_date') or 'date not shown')}</p>
  </div>
  {q_html or '<p class="source-none">Linked for reference; not quoted in this build.</p>'}
  <dl class="source-dl">
    <div><dt>Used for</dt><dd>{esc(s.get('used_for') or '')}</dd></div>
    <div><dt>Where it is applied</dt><dd>{esc(s.get('applied_in') or '')}</dd></div>
    <div><dt>Status</dt><dd>{esc(s.get('status') or '')}</dd></div>
  </dl>
  <p class="source-link">{outbound(d, s['url'], s['url'], cls='srclink')}</p>
</article>""")

    prod_rows = []
    for p in products:
        if p.get("observed_asin"):
            prod_rows.append([
                {"html": f'<a href="{esc(rel(d, "products/" + p["ref"].lower() + ".html"))}"><strong>{esc(p["ref"])}</strong></a>'},
                {"html": esc(p.get("brand") or "")},
                {"html": esc(p.get("format_label") or "")},
                {"html": product_link(d, p["affiliate_url"], esc(p["observed_asin"]),
                                       aria=f"Open the Amazon listing for {p['ref']} (affiliate link, opens in a new tab)")},
                {"html": esc(p.get("checked_on") or "")},
            ])
        else:
            prod_rows.append([
                {"html": f'<strong>{esc(p["ref"])}</strong>'},
                {"html": '<span class="blank">&mdash;</span>'},
                {"html": '<span class="blank">&mdash;</span>'},
                {"html": '<span class="pill pill-warn">Unresolved</span>'},
                {"html": esc(p.get("checked_on") or "")},
            ])

    prod_tbl = table(["Ref", "Brand", "Type", "Official listing (source)", "Checked"], prod_rows,
                     cls="register", caption="Every product row, with the Amazon page it came from",
                     note="The listing is the source for the brand, type, stated size and stated attributes. Nothing else on this site is a source for those.")

    rows = [[
        {"html": f"<strong>{esc(m['item'])}</strong>"},
        {"html": "<br>".join(esc(a) for a in m.get("attempted", [])[:2])},
        {"html": esc(m.get("reason") or "")},
    ] for m in missing]
    miss_tbl = table(["What could not be verified", "What was tried", "Why it stays blank"], rows,
                     cls="misses", caption="Unverified items, and the reason they are unverified")

    body = f"""{pagehead(
        'Sources',
        'Every claim,<br>linked to its origin',
        'Five official documents and five Amazon listings. Each quotation below was read on 20 November 2026 and reproduced '
        'exactly. What could not be reached is listed at the bottom, with nothing substituted for it.',
        meta='Retrieved 20 November 2026 &middot; Amazon Associates, the U.S. FTC and Google Search Central',
    )}
{section(f'''
<div class="lede-prose">
  <p>A rule this site enforces on itself: if a sentence needs a fact, the fact has a source and the source is on this page.
  If no source could be reached, the sentence does not ship and the gap appears in the last table instead.</p>
  <p>Two authorities apply at once. Amazon decides whether a link earns and whether the account stays in the programme. The
  U.S. Federal Trade Commission decides whether a reader understood that the link pays. Neither one substitutes for the other,
  which is why both are quoted rather than paraphrased.</p>
</div>''', cls='')}
{section(f'<div class="source-grid">{"".join(blocks)}</div>', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Product sources')}<h2>Where each product fact came from</h2></div>
<p>One row per product, linking the Amazon page that was opened. Brand, type and stated attributes are transcribed from those pages.</p></div>
{prod_tbl}''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('What is missing')}<h2>Unverified, and left that way</h2></div>
<p>Each row names what was attempted. A blank with a reason is worth more than a number with a guess behind it.</p></div>
{miss_tbl}''', cls='')}
{section(f'''
<div class="callout">
  <h2>How to re-check this page in ten minutes</h2>
  <ol class="tight">
    <li>Open the Operating Agreement and search for "I earn from qualifying purchases". It is section 5.</li>
    <li>Open the Program Policies, find Participation Requirements 2(b), and read the sentence about the tag parameter.</li>
    <li>Open the FTC FAQ and find "A disclosure should be placed where it easily catches consumers' attention".</li>
    <li>Open any product page on this site, take the ASIN, and open amazon.com/dp/&lt;ASIN&gt;. If the titles match, the register is right.</li>
    <li>If a check fails, note the date. Prices, titles and policies all change; a source is a snapshot, not a permanent fact.</li>
  </ol>
</div>''', cls='')}
"""
    return page(
        d,
        title="Sources and quotations \u2014 Crisp & Counter",
        description=("The official documents behind this site's claims: Amazon's Operating Agreement and Program Policies, the "
                     "FTC endorsement guidance, Google's outbound-link documentation, and the listing behind every product fact."),
        body=body,
        canonical="sources/",
        breadcrumb=[("Home", ""), ("Sources", "sources/")],
    )
