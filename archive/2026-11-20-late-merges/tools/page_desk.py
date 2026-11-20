"""About, ledger, executive brief and the 404 page."""

from layout import (BUILD_DATE, DISCLOSURE, SITE_NAME, SITE_URL, TRACKING_ID, blank,
                    cite_or_product, esc, eyebrow, outbound, page, pagehead, product_link, rel,
                    section, table)


def build_about(page_dir, sources, meta):
    d = page_dir
    n_products = len(meta.get("products", []))

    body = f"""{pagehead(
        'About',
        'A small shop window<br>with its receipts attached',
        f'{SITE_NAME} is a static publication about three air fryers and two thermometers. No backend, no cookies, no third-party '
        'requests. This page states the rules so you can hold the site to them.',
        meta='Static HTML &middot; self-hosted fonts &middot; no analytics running &middot; no prices or ratings',
    )}
{section(f'''
<div class="about-grid">
  <div class="prose-block">
    <h2 id="what">What this site is</h2>
    <p>A short guide to a small number of kitchen tools, written for someone standing in a kitchen with a tape measure and a
    decision to make. {n_products} links were supplied by the operator. Each was opened and its destination recorded. The guides
    around them describe what to check, in what order, and why.</p>
    <p>It is not a review site. Nothing here was bought, cooked with, measured or compared by testing. That limitation is stated on
    every product page and inside every guide, not only here.</p>

    <h2 id="why-blank">Why so much is blank</h2>
    <p>Amazon's Associates Program Policies, section 2(b), say a site may show prices and availability only where Amazon serves the
    link carrying that data, or where the site obtains it through the Creators API or the Product Advertising API. This build has
    access to neither, so price, star rating, review count and stock status are absent everywhere &mdash; not because they are hard to
    copy, but because copying them is the specific thing that clause forbids.</p>
    <p>The same discipline applies to fields nobody regulates: dimensions, wattage and warranty terms were not confirmed from an
    official specification sheet here, so they are empty too. An empty cell is a question mark; a filled-in cell nobody verified is
    a lie with a font.</p>

    <h2 id="how-we-link">How the links work</h2>
    <p>Every Amazon product link on this site is a tagged Special Link: the observed ASIN plus <code class="code">?tag={esc(TRACKING_ID)}</code>,
    which is the parameter form Program Policies 2(b) describes. Each one carries <code class="code">rel="sponsored nofollow noopener"</code>,
    opens in a new tab, and says so in its accessible label. Google documents <code class="code">sponsored</code> as the marker for paid links.</p>
    <p>Whether a click is actually credited to the ID has not been confirmed, because confirming it needs one click from the
    operator's device followed by a look at the Associates report. That is FLG-002 and Q-08 on the review queue rather than an
    assertion here.</p>

    <h2 id="disclosure">The disclosure</h2>
    <p>{esc(DISCLOSURE)}</p>
    <p>That exact sentence is required by section 5 of the Operating Agreement. It appears in a strip under the masthead on every
    page and again in the footer. The FTC's guidance says a disclosure at the bottom of a page is easy to miss and that it should sit
    close to the recommendation &mdash; so every product card also carries its own line, and every product page repeats it beside the button.</p>

    <h2 id="privacy">Privacy</h2>
    <p>This site sets no cookies, loads no third-party scripts, calls no external APIs and embeds no fonts from a CDN. The typefaces
    are served from this repository. The analytics client is present but inert: it transmits nothing unless an endpoint is configured,
    and none is. There is no form and no newsletter, so the site holds no personal data at all.</p>
    <p>If a reader marks decisions on the <a href="{esc(rel(d, 'suggestions/index.html'))}">suggestions page</a>, that choice is stored
    in their own browser and never sent anywhere.</p>

    <h2 id="imagery">Imagery</h2>
    <p>Every photograph here is an AI-generated illustration, labelled where it appears and never presented as a photograph of a
    product. None carries a brand mark. <a href="{esc(rel(d, 'review/images.html'))}">All eleven assets are listed</a> with the rule
    each one follows and the reason for it.</p>

    <h2 id="workflow">The publishing gate</h2>
    <p>No page publishes unless the build passes. <code class="code">tools/check.py</code> fails on a missing or misplaced disclosure,
    an Amazon link without <code class="code">sponsored</code>, any price or rating phrase in visible text, any root-absolute internal
    link, any broken link or anchor, any external resource load, more than one <code class="code">h1</code>, and any image without alt
    text. The same script runs in GitHub Actions before deployment, and a reproducibility step fails the build if a generated page was
    edited by hand.</p>

    <h2 id="who">Who wrote this</h2>
    <p>No author is named, because there is no person whose name would be accurate here. This is the site's largest weakness and it is
    recorded as FLG-019 rather than papered over with a stock biography. Supplying a name and two true sentences would fix it
    (S-12).</p>
  </div>
  <aside class="record-side">
    <div class="side-card"><h2>At a glance</h2><dl class="side-dl">
      <div><dt>Products</dt><dd>{n_products} submitted, {n_products} identified</dd></div>
      <div><dt>Tested</dt><dd>0</dd></div>
      <div><dt>Prices shown</dt><dd>None</dd></div>
      <div><dt>Third-party requests</dt><dd>0</dd></div>
      <div><dt>Cookies</dt><dd>0</dd></div>
      <div><dt>Last built</dt><dd>{esc(BUILD_DATE)}</dd></div>
    </dl></div>
    <div class="side-card"><h2>Jump to</h2><ul class="side-links">
      <li><a href="#why-blank">Why values are blank</a></li>
      <li><a href="#how-we-link">How links are marked</a></li>
      <li><a href="#disclosure">Disclosure</a></li>
      <li><a href="{esc(rel(d, 'sources/index.html'))}">Sources and quotations</a></li>
      <li><a href="{esc(rel(d, 'review/index.html'))}">Flagged for review</a></li>
    </ul></div>
  </aside>
</div>''', cls='')}
{section(f'''
<div class="callout">
  <h2>Where the receipts are</h2>
  <p>Every policy quotation, every retrieval date and every product source lives on the
  <a href="{esc(rel(d, 'sources/index.html'))}">sources page</a>. The items that could not be verified, and what was tried, are at the
  bottom of that page and on the <a href="{esc(rel(d, 'review/index.html'))}">review queue</a>.</p>
</div>''', cls='')}
"""
    return page(
        d,
        title="About, disclosure and privacy \u2014 Crisp & Counter",
        description=("What this site is, why prices and ratings are absent, how every Amazon link is tagged and marked, the "
                     "required disclosure, and the privacy position."),
        body=body,
        canonical="about/",
        breadcrumb=[("Home", ""), ("About", "about/")],
    )


def build_ledger(page_dir, meta):
    d = page_dir
    rows = [[{"html": blank(None)} for _ in range(7)]]
    body = f"""{pagehead(
        'Campaign ledger',
        'An empty ledger,<br>with its columns defined',
        'The brief asked for measurement before optimisation. The measurable unit is a row, and a row needs a provenance note. '
        'There are none yet.',
        meta='0 rows &middot; 0 sessions &middot; 0 clicks &middot; 0 reported orders &middot; no forecast',
    )}
{section(f'''
<div class="lede-prose">
  <p>A ledger is only worth keeping if every row can be traced to a report somebody was authorised to read. The columns are
  therefore fixed in advance, and the rule is that a row appears only when the value comes from an authorised first-party report,
  with the date and the source recorded beside it.</p>
  <p>There are no rows. Not because the table was forgotten, but because no Associates report has been supplied, no analytics
  endpoint is live, and there is no traffic to measure. A table with six plausible numbers in it would be the most damaging thing
  this site could publish.</p>
</div>
{table(['Date', 'Source', 'Channel', 'Eligible sessions', 'Clicks', 'Reported orders', 'Provenance note'], rows, cls='ledger')}
<h2 style="margin-top:2.4rem">The provenance rule</h2>
<ol class="tight">
  <li><strong>Date</strong> &mdash; the date of the report, not the date of entry.</li>
  <li><strong>Source</strong> &mdash; which report, in which account, exported by whom.</li>
  <li><strong>Channel</strong> &mdash; organic search, direct, referral or social, as the report labels it.</li>
  <li><strong>Eligible sessions</strong> &mdash; sessions that had a reasonable chance to reach a link, not raw page views.</li>
  <li><strong>Clicks</strong> &mdash; outbound clicks as recorded, not as estimated.</li>
  <li><strong>Reported orders</strong> &mdash; orders the Associates report attributes, including ones later returned.</li>
  <li><strong>Provenance note</strong> &mdash; one line a stranger could follow to check the row.</li>
</ol>
<h2 style="margin-top:2.4rem">What is deliberately absent</h2>
<p>No conversion rate, no revenue estimate and no commission projection. Each would need a rate card that has not been read, a
traffic figure that has not been measured, and a conversion assumption with nothing behind it.</p>
<div class="callout"><h2>What would put a row here</h2><p>One test click, then one Associates report. That is all.
<a href="{esc(rel(d, 'suggestions/index.html'))}#S-02">Suggestion S-02</a> · <a href="{esc(rel(d, 'review/measurement.html'))}">the measurement plan</a>.</p></div>''', cls='')}"""
    return page(
        d,
        title="Campaign ledger \u2014 Crisp & Counter",
        description=("An empty campaign ledger with its columns and provenance rule: date, source, channel, eligible sessions, "
                     "clicks, reported orders, and a provenance note."),
        body=body,
        canonical="operations/ledger.html",
        breadcrumb=[("Home", ""), ("Campaign ledger", "operations/ledger.html")],
    )


def build_brief(page_dir, products, questions, flags, meta):
    d = page_dir
    prods = products["products"] if isinstance(products, dict) else products
    qs = questions["questions"]
    openq = [q for q in qs if not q.get("answered")]
    blocking = [q for q in openq if str(q.get("blocking", "")).startswith("yes")]
    fl = flags["flags"]
    high = [f for f in fl if f["severity"] == "high"]
    high_fixed = [f for f in high if f.get("resolved")]

    prod_rows = []
    for p in prods:
        prod_rows.append([
            {"html": f"<strong>{esc(p['ref'])}</strong>"},
            {"html": product_link(d, p["submitted_link"], "link.amazon/" + esc(p["submitted_code"]),
                                   aria=f"Open submitted link {p['ref']} (affiliate link, opens in a new tab)")},
            {"html": esc(p.get("intended_asin") or "—")},
            {"html": cite_or_product(d, p["affiliate_url"], esc(p["observed_asin"])) if p.get("observed_asin") else "—"},
            {"html": esc(p.get("brand") or "—")},
            {"html": esc(p.get("format_label") or "—")},
            {"html": '<span class="pill pill-ok">Verified</span>' if p.get("observed_asin")
                     else '<span class="pill pill-warn">Unresolved</span>'},
        ])

    block_rows = [[
        {"html": f'<strong>{esc(q["id"])}</strong>'},
        {"html": esc(q["question"])},
        {"html": esc(q.get("what_is_missing") or "")},
        {"html": esc(q.get("owner") or "")},
    ] for q in blocking]

    body = f"""{pagehead(
        'Executive summary',
        'What was built, what was '
        'checked,<br>and what is still unknown',
        f'Prepared {esc(BUILD_DATE)} for the operator of {SITE_NAME}. Five submitted links, a five-guide publication around them, '
        'and a review queue that publishes its own gaps.',
        meta=f'Tracking ID {esc(TRACKING_ID)} &middot; branch arena/2ed69be3-affil1 &middot; static site on GitHub Pages',
    )}
{section(f'''
<div class="summary-grid">
  <div class="summary-card"><span class="summary-n">5 / 5</span><h3>Links identified</h3>
    <p>Every supplied link was opened on 20 November 2026 and its destination recorded. P-04 needed three attempts.</p></div>
  <div class="summary-card"><span class="summary-n">5</span><h3>Guides published</h3>
    <p>Four cluster guides plus one wider guide, each built around a decision rather than a product.</p></div>
  <div class="summary-card"><span class="summary-n">16</span><h3>Questions registered</h3>
    <p>Six answered with a source in this repository. Ten open, six of which hold up other work.</p></div>
  <div class="summary-card"><span class="summary-n">{len(fl)}</span><h3>Items flagged</h3>
    <p>Published with source links on the review page. {len(high)} are high severity; {len(high_fixed)} of those is fixed in this build and the rest are open.</p></div>
</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The products')}<h2>Five links, as verified</h2></div>
<p>Intended ASIN and observed ASIN are separate fields. Nothing was inferred to fill the intended column.</p></div>
{table(['Ref', 'Submitted', 'Intended ASIN', 'Observed ASIN', 'Brand', 'Type', 'Status'], prod_rows, cls='register',
       caption='Verification record, 20 November 2026')}
<p class="table-note">Source for every row: the Amazon listing in the observed-ASIN column, opened on 2026-11-20. The full record with
quotations is on the <a href="{esc(rel(d, 'sources/index.html'))}">sources page</a>.</p>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('What changed in this pass')}<h2>Seven decisions taken, with reasons</h2></div></div>
<ol class="tight">
  <li><strong>Tagged links.</strong> Program Policies 2(b) requires the Associates ID as a URL parameter. The previous build linked to bare
      <code class="code">/dp/</code> addresses; every product link is now <code class="code">/dp/ASIN?tag={esc(TRACKING_ID)}</code> (FLG-016).</li>
  <li><strong>P-04 resolved and corrected.</strong> A third request reached B0DHZTCNR5, a ThermoMaven instant-read thermometer. The old
      "unresolved" text was removed from the product record and kept in the flag log (FLG-004).</li>
  <li><strong>The front page leads with products.</strong> Three shapes of shop window, then the guides, then the machinery. The audit
      material moved to the review pages it belongs on.</li>
  <li><strong>Guides are clustered.</strong> Shape, size, upkeep and thermometers, each with one anchor guide, so a new article has a home
      rather than joining a flat list.</li>
  <li><strong>A thermometer guide exists</strong>, because two of five products are thermometers and the publication only spoke about air
      fryers.</li>
  <li><strong>One origin, one index.</strong> The superseded parallel edition is marked noindex and excluded from the sitemap rather than
      deleted (FLG-018).</li>
  <li><strong>The suggestion board is a decision tool.</strong> Fifteen proposals with cost, risk, evidence and dependencies, seven already
      implemented, each with an accept / hold / reject control.</li>
</ol>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('What is blocked')}<h2>Six questions hold up the next move</h2></div>
<p>Each needs one export, one screenshot or one written answer from the account owner.</p></div>
{table(['Ref', 'Question', 'Information needed', 'Held by'], block_rows, cls='register',
       caption='Blocking questions, in the order they unblock other work')}
<p class="table-note">The full register, including the answered rows and the evidence for each, is on the
<a href="{esc(rel(d, 'questions/index.html'))}">questions page</a>.</p>''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('What is not claimed')}<h2>The limits, in one place</h2></div></div>
<div class="two-col">
  <div>
    <h3>Not measured</h3>
    <ul class="ticks ticks-quiet">
      <li>Traffic, clicks and conversion &mdash; no endpoint, no reports</li>
      <li>Search demand for any topic</li>
      <li>Revenue, commission rate or forecast</li>
      <li>Whether a click attributes to the tracking ID</li>
    </ul>
  </div>
  <div>
    <h3>Not asserted</h3>
    <ul class="ticks ticks-quiet">
      <li>That any product performs well, or better than another</li>
      <li>That the short links are invalid &mdash; their status is unresolved (FLG-003)</li>
      <li>That any price or rating is current</li>
      <li>That this site tested anything</li>
    </ul>
  </div>
</div>
<div class="callout">
  <h2>Where to start reviewing</h2>
  <p><a href="{esc(rel(d, 'review/index.html'))}">Flagged for review</a> &mdash; {len(fl)} items with source links.
  <a href="{esc(rel(d, 'suggestions/index.html'))}">Suggestions</a> &mdash; the decisions waiting for you.
  <a href="{esc(rel(d, 'sources/index.html'))}">Sources</a> &mdash; the quotations and dates.</p>
</div>''', cls='')}"""
    return page(
        d,
        title="Executive summary \u2014 Crisp & Counter",
        description=("Five links verified, five guides built around them, the decisions taken, the questions still blocking, "
                     "and everything the site does not claim."),
        body=body,
        canonical="brief/",
        breadcrumb=[("Home", ""), ("Executive summary", "brief/")],
    )


def build_404(page_dir, meta):
    d = page_dir
    body = f"""{pagehead(
        '404',
        'That page is not here',
        'The link may be old, or the page may have been retired. Everything published is reachable from the front page.',
    )}
{section(f'''
<p class="hero-actions"><a class="btn" href="{esc(rel(d, 'index.html'))}">Front page</a>
<a class="btn btn-ghost" href="{esc(rel(d, 'products/index.html'))}">The shortlist</a>
<a class="btn btn-ghost" href="{esc(rel(d, 'guides/index.html'))}">Guides</a></p>''', cls='')}"""
    return page(d, title="Page not found \u2014 Crisp & Counter",
                description="That page is not here. Everything published is reachable from the front page.",
                body=body, canonical="404.html")
