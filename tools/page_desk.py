"""About, sources, ledger, brief and the 404 page."""

from layout import (DISCLOSURE, SITE_NAME, TRACKING_ID, blank, esc, eyebrow,
                    outbound, page, pagehead, rel, section, table)
from content import GUIDES


def build_about(page_dir, sources, products, meta):
    d = page_dir
    n_pages = meta.get("page_count", 27)
    n_total = len(products)
    n_ok = sum(1 for p in products if p.get("observed_asin"))
    n_af = sum(1 for p in products if p.get("category") == "air-fryers")
    n_th = sum(1 for p in products if p.get("category") == "thermometers")

    rows = []
    for s in sources["sources"]:
        quote = f'<blockquote class="quote">{esc(s["quote"])}</blockquote>' if s.get("quote") else '<span class="blank">&mdash;</span>'
        status_cls = "pill-ok" if s["status"].startswith("read") else "pill"
        rows.append([
            {"html": f'<strong>{esc(s["id"])}</strong>'},
            {"html": f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a><br><span class="tiny">{esc(s["publisher"])} &middot; {esc(s["page_date"])}</span>'},
            {"html": esc(s["used_for"])},
            {"html": quote},
            {"html": f'<span class="pill {status_cls}">{esc(s["status"])}</span>'},
        ])
    unverified = "".join(
        f"""<article class="reject"><h3>{esc(u['item'])}</h3>
        <p><strong>Tried:</strong></p><ul class="tight">{''.join(f'<li><code class="code">{esc(a)}</code></li>' for a in u['attempted'])}</ul>
        <p>{esc(u['reason'])}</p></article>""" for u in sources["could_not_verify"]
    )

    body = f"""{pagehead(
        'About',
        'A small, careful<br>shop window',
        f'{SITE_NAME} is a static publication about air fryers and meat thermometers. It has no backend, no cookies and no third-party requests. This page states its rules so you can hold it to them.',
        meta='Static HTML &middot; self-hosted fonts &middot; no analytics running &middot; no prices',
    )}
{section(f'''
<div class="about-grid">
  <div class="prose-block">
    <h2 id="what">What this site is</h2>
    <p>A buyer-facing guide to five verified Amazon listings across two complementary categories: {n_af} Air Fryers and {n_th} Meat Thermometers. Every submitted link was opened against Amazon.com, its observed ASIN and category breadcrumb recorded, and its seller-stated attributes separated cleanly from unverified fields.</p>
    <p>It is not a hands-on testing lab. Nothing here was bought, cooked with or measured. Safe minimum internal cooking temperatures are cited directly from USDA FSIS (SRC-06, SRC-07), and that limit is stated plainly on every product page and guide.</p>

    <h2 id="why-blank">Why so much is blank</h2>
    <p>Amazon&rsquo;s Associates Program Policies, section 2(b), permit showing prices and availability only if Amazon serves the link carrying that data, or if the site obtains it through the Creators API or the Product Advertising API (SRC-02). This build has access to neither. So price, star rating, review count and stock status are absent everywhere &mdash; by rule, not by omission.</p>
    <p>The same discipline applies to fields nobody regulates: dimensions, wattage, probe calibration and warranty terms were not confirmed from an official specification sheet in this build, so they stay blank until verified.</p>

    <h2 id="how-we-link">How the links work</h2>
    <p>Every link to an Amazon product listing on this site carries <code class="code">rel="sponsored nofollow noopener"</code> and opens in a new tab. Google&rsquo;s own documentation confirms that <code class="code">sponsored</code> is the documented marker for paid or advertising links (SRC-05). That rule is enforced automatically by <code class="code">tools/check.py</code>.</p>
    <p>The tracking ID supplied for this site is <code class="code">{esc(TRACKING_ID)}</code>. Whether clicks on the supplied short links are credited to it has not been confirmed, because confirming attribution requires a test click and a check inside Associates Central (<a href="{esc(rel(d, 'review/index.html'))}#FLG-002">FLG-002</a>).</p>

    <h2 id="disclosure">The disclosure</h2>
    <p>{esc(DISCLOSURE)}</p>
    <p>That exact sentence is required by section 5 of the Associates Program Operating Agreement (SRC-01). It appears in a disclosure strip directly beneath the masthead above the fold on every page, repeats in every footer, and sits beside outbound product links per FTC Endorsement Guides guidance (SRC-03, SRC-04).</p>

    <h2 id="privacy">Privacy</h2>
    <p>This site sets no cookies, loads no third-party scripts, calls no external APIs and embeds no fonts from a CDN. The typefaces are self-hosted in this repository. The analytics client is present and inert by default; no data leaves the browser. There is no form, no newsletter and no comment system.</p>

    <h2 id="imagery">Imagery</h2>
    <p>All editorial photographs are AI-generated illustrations, visibly labelled where they appear and never presented as photographs of the actual products. <a href="{esc(rel(d, 'review/images.html'))}">Every asset is listed</a> with the rule it follows.</p>

    <h2 id="who">Who wrote this</h2>
    <p>No author is named, because inventing a persona would be deceptive. This authority limit is recorded as <a href="{esc(rel(d, 'review/index.html'))}#FLG-006">FLG-006</a>, and naming a real editor with an accurate bio is proposal <a href="{esc(rel(d, 'suggestions/index.html'))}#S-03">S-03</a>.</p>
  </div>
  <aside class="record-side">
    <div class="side-card"><h2>At a glance</h2><dl class="side-dl">
      <div><dt>Built pages</dt><dd>{n_pages}</dd></div>
      <div><dt>Products</dt><dd>{n_total} submitted, {n_ok} observed</dd></div>
      <div><dt>Categories</dt><dd>{n_af} Air Fryers, {n_th} Thermometers</dd></div>
      <div><dt>Buying guides</dt><dd>{len(GUIDES)}</dd></div>
      <div><dt>Tested</dt><dd>0</dd></div>
      <div><dt>Prices shown</dt><dd>None</dd></div>
      <div><dt>Third-party requests</dt><dd>0</dd></div>
      <div><dt>Cookies</dt><dd>0</dd></div>
    </dl></div>
    <div class="side-card"><h2>Jump to</h2><ul class="side-links">
      <li><a href="#why-blank">Why values are blank</a></li>
      <li><a href="#how-we-link">How links are marked</a></li>
      <li><a href="#disclosure">Disclosure</a></li>
      <li><a href="#sources">Sources</a></li>
      <li><a href="{esc(rel(d, 'review/index.html'))}">Review queue</a></li>
    </ul></div>
  </aside>
</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Sources')}<h2 id="sources">Every source, with the words it was used for</h2></div>
<p>Each source below was requested and read directly on 20 November 2026. Quotes are copied verbatim from the official document.</p></div>
{table(['Ref', 'Source', 'Used for', 'Quoted wording', 'Status'], rows, cls='sources')}
<h2 style="margin-top:3rem">What still could not be checked from outside the account</h2>
<p class="lede-prose">Recorded openly as unverified gaps rather than guessed from blogs.</p>
<div class="reject-grid">{unverified}</div>''', cls='')}"""
    return page(
        d,
        title="About and sources \u2014 Crisp & Counter",
        description="What Crisp & Counter is, why prices and ratings remain blank, how sponsored links are enforced, and the full list of official Amazon, FTC, Google and USDA FSIS sources.",
        body=body,
        active="index.html",
        canonical="about/",
    )


def build_ledger(page_dir, meta):
    d = page_dir
    rows = [
        [{"html": blank(None)}, {"html": blank(None)}, {"html": blank(None)},
         {"html": blank(None)}, {"html": blank(None)}, {"html": blank(None)},
         {"html": blank(None)}]
    ]
    body = f"""{pagehead(
        'Campaign ledger',
        'An empty ledger,<br>with its columns defined',
        'Measurement comes before optimization. Every row in this ledger requires an authorised first-party report and a dated provenance note. None exist yet.',
        meta='0 rows &middot; 0 sessions &middot; 0 clicks &middot; 0 reported orders &middot; no forecast',
    )}
{section(f'''
<div class="lede-prose">
  <p>A ledger is only worth keeping if every row can be traced back to a report somebody was authorised to read. The columns below are fixed in advance, and a row is added only when the value comes from an authorised first-party report with the pull date and source recorded alongside it.</p>
  <p>There are no rows. Not because the table was forgotten, but because no Associates report has been supplied, no analytics endpoint is deployed, and there is no measured traffic yet. No conversion score or revenue forecast is presented here.</p>
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
<p>No conversion rate. No revenue estimate. No commission projection. Each would require an Associates rate card that has not been read, a traffic figure that has not been measured, and a conversion assumption with nothing behind it.</p>
<div class="callout"><h2>What puts the first row here</h2><p>One validated test click, then one Associates Central report. <a href="{esc(rel(d, 'suggestions/index.html'))}#S-01">Suggestion S-01</a>.</p></div>''', cls='')}"""
    return page(
        d,
        title="Campaign ledger \u2014 Crisp & Counter",
        description="An empty campaign ledger with its columns and provenance rule defined: date, source, channel, eligible sessions, clicks, reported orders and provenance note.",
        body=body,
        active="index.html",
        canonical="operations/ledger.html",
    )


def build_brief(page_dir, products, questions, flags, meta):
    d = page_dir
    n_pages = meta.get("page_count", 27)
    n_total = len(products)
    n_ok = sum(1 for p in products if p.get("observed_asin"))
    n_unres = n_total - n_ok
    n_af = sum(1 for p in products if p.get("category") == "air-fryers")
    n_th = sum(1 for p in products if p.get("category") == "thermometers")
    n_q = len(questions["questions"])
    n_open = sum(1 for q in questions["questions"] if not q.get("answered"))
    n_high = sum(1 for f in flags["flags"] if f["severity"] == "high")

    body = f"""{pagehead(
        'Executive summary',
        'The short version,<br>for someone with four minutes',
        'What was built, what was verified directly from official sources, what remains blocked on account access, and the exact next decisions.',
        meta=f'Updated 20 November 2026 &middot; {n_pages} pages &middot; {n_ok} of {n_total} listings verified &middot; tracking ID {esc(TRACKING_ID)}',
    )}
{section(f'''
<div class="exec">
  <div class="exec-block">
    <h2>What was asked for</h2>
    <p>An Amazon affiliate publication covering five supplied links (tracking ID <code class="code">{esc(TRACKING_ID)}</code>): verified product records, side-by-side comparison, buyer-question guides, privacy-preserving click measurement architecture, decision queues, a compliant disclosure layer, and a live GitHub Pages deployment.</p>
  </div>
  <div class="exec-block">
    <h2>What was built</h2>
    <p>A {n_pages}-page static publication (<code class="code">Crisp &amp; Counter</code>) organized into two verified categories ({n_af} Air Fryers and {n_th} Meat Thermometers) with {len(GUIDES)} buying guides, a five-row product-intent confirmation register, individual product records, a comparison table, {n_q} pre-decision questions, an interactive decision queue of proposals, {len(flags["flags"])} audit flags, 8 verified official sources with verbatim quotes, an empty provenance-gated campaign ledger, an inert analytics client, RSS feed, sitemap, and an automated CI checker (<code class="code">tools/check.py</code>).</p>
  </div>
  <div class="exec-block">
    <h2>What was directly verified on 20 November 2026</h2>
    <p>All {n_ok} of {n_total} submitted links resolved to live Amazon.com product pages and were independently re-verified: P-01 (<code class="code">B0CDY277D3</code>, CHEFMAN 6 Qt dual-basket air fryer), P-02 (<code class="code">B09B7SB46R</code>, Emeril Lagasse 26 Qt French-door air fryer oven), P-03 (<code class="code">B08DKYBTPH</code>, Chefman 8 Qt TurboFry), P-04 (<code class="code">B0DHZTCNR5</code>, ThermoMaven 1 Sec instant-read meat thermometer, previously gated by Amazon&rsquo;s continuity interstitial), and P-05 (<code class="code">B0DZFD6R9Z</code>, CHEF iQ Sense 3-probe wireless meat thermometer).</p>
    <p>Official policy and food-safety sources were read directly and quoted verbatim: Amazon Associates Operating Agreement &sect;5 (SRC-01), Amazon Associates Program Policies &sect;2(b) (SRC-02), FTC Endorsement Guides FAQ (SRC-03), 16 CFR Part 255 on eCFR (SRC-04), Google Search Central outbound-link docs (SRC-05), USDA FSIS Safe Minimum Internal Temperature Chart &amp; Food Thermometers factsheet (SRC-06, SRC-07), and Amazon SP-API Catalog Items Reference (SRC-08).</p>
  </div>
  <div class="exec-block exec-warn">
    <h2>The key verification finding</h2>
    <p>Every submitted path code is 9 characters with lowercase letters; every ASIN observed on arrival is 10 uppercase characters. The supplied codes are short-link slugs, not ASINs, and none of the five arrived-at URLs displayed a visible <code class="code">tag=</code> parameter for <code class="code">{esc(TRACKING_ID)}</code>. Intended ASIN and observed redirect target are therefore stored in separate fields and never merged, and attribution remains unconfirmed until one click is verified in Associates Central (FLG-001, FLG-002).</p>
  </div>
  <div class="exec-block">
    <h2>What remains unverified &mdash; and why</h2>
    <dl class="exec-dl">
      <div><dt>Intended ASINs &amp; tracking</dt><dd>Requires authenticated Associates Central access and a test click for <code class="code">{esc(TRACKING_ID)}</code> (FLG-001, FLG-002, FLG-003).</dd></div>
      <div><dt>Price, rating, availability</dt><dd>Omitted site-wide by Program Policies &sect;2(b) (SRC-02) because neither Amazon-served widgets nor PA API / Creators API is connected (FLG-005).</dd></div>
      <div><dt>Author &amp; hands-on testing</dt><dd>No named author and no physical product testing; every guide and product card discloses this openly (FLG-006).</dd></div>
      <div><dt>Commission rates &amp; traffic</dt><dd>Associates rate card sits behind sign-in; analytics beacon is inert until a first-party collector and privacy notice are deployed. No conversion score or revenue forecast is shown (FLG-010, FLG-013, FLG-014).</dd></div>
    </dl>
  </div>
  <div class="exec-block">
    <h2>Recommended decision order</h2>
    <p>First: confirm all five ASINs inside Associates Central, generate validated tagged Special Links for <code class="code">{esc(TRACKING_ID)}</code>, and verify one live click in the Associates click report (<a href="{esc(rel(d, 'suggestions/index.html'))}#S-01">S-01</a>, <a href="{esc(rel(d, 'suggestions/index.html'))}#S-02">S-02</a>). Second: verify the site in Google Search Console and submit <code class="code">sitemap.xml</code> (<a href="{esc(rel(d, 'suggestions/index.html'))}#S-07">S-07</a>). Third: deploy the first-party analytics collector behind a published privacy notice before writing additional guides (<a href="{esc(rel(d, 'suggestions/index.html'))}#S-06">S-06</a>, <a href="{esc(rel(d, 'suggestions/index.html'))}#S-14">S-14</a>).</p>
  </div>
  <div class="exec-block">
    <h2>Numbers on the record</h2>
    <div class="exec-stats">
      <div><span>{n_total}</span><p>links supplied</p></div>
      <div><span>{n_ok}</span><p>verified live listings</p></div>
      <div><span>{n_unres}</span><p>unresolved links</p></div>
      <div><span>{len(GUIDES)}</span><p>buying guides</p></div>
      <div><span>0</span><p>products tested</p></div>
      <div><span>0</span><p>prices shown</p></div>
      <div><span>{n_q}</span><p>questions ({n_open} open)</p></div>
      <div><span>{n_high}</span><p>high-severity flags</p></div>
    </div>
  </div>
</div>''', cls='')}"""
    return page(
        d,
        title="Executive summary \u2014 Crisp & Counter",
        description="Executive summary of Crisp & Counter: all 5 Amazon listings verified (3 Air Fryers + 2 Meat Thermometers), 8 official sources verified, compliance gates, and prioritized next decisions.",
        body=body,
        active="index.html",
        canonical="brief/",
    )


def build_404(page_dir, meta):
    d = page_dir
    body = f"""{pagehead(
        '404',
        'That page is not here',
        'Either the address was mistyped or a link inside this site is broken. The second would be a bug worth reporting.',
        meta='',
    )}
{section(f'''
<ul class="next-grid-3">
  <li><a class="tlink" href="{esc(rel(d, 'index.html'))}">Front page</a></li>
  <li><a class="tlink" href="{esc(rel(d, 'guides/index.html'))}">All guides</a></li>
  <li><a class="tlink" href="{esc(rel(d, 'products/index.html'))}">Product register</a></li>
</ul>''', cls='')}"""
    return page(d, title="Page not found \u2014 Crisp & Counter",
                description="That page does not exist on Crisp & Counter.",
                body=body, canonical="404.html")
