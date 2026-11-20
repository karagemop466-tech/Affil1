"""About, sources, ledger, brief and the 404 page."""

from layout import (DISCLOSURE, SITE_NAME, TRACKING_ID, blank, esc, eyebrow,
                    outbound, page, pagehead, rel, section, table)


def build_about(page_dir, sources, meta):
    d = page_dir
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
        f'{SITE_NAME} is a static publication about air fryers and thermometers. This static publication has no active analytics backend or third-party tracking requests. This page states its rules so you can hold it to them.',
        meta='Static HTML &middot; self-hosted fonts &middot; no analytics running &middot; no prices',
    )}
{section(f'''
<div class="about-grid">
  <div class="prose-block">
    <h2 id="what">What this site is</h2>
    <p>A short guide to a small number of kitchen appliances, written for someone standing in a kitchen with a tape measure and a decision to make. Five destinations were observed, including two thermometers; product intent remains unconfirmed. Each link was opened and the destination recorded. The guides around them describe what to check, in what order, and why.</p>
    <p>It is not a review site. Nothing here was bought, cooked with, measured or compared by testing. That is a real limitation and it is stated on every product page and in every guide rather than in a footnote here.</p>

    <h2 id="why-blank">Why so much is blank</h2>
    <p>Amazon's Associates Program Policies, section 2(b), say that a site may show prices and availability only if Amazon serves the link carrying that data, or if the site obtains it through the Creators API or the Product Advertising API. This build has access to neither. So price, star rating, review count and stock status are absent everywhere &mdash; not because they are difficult to copy, but because copying them is the specific thing that clause forbids.</p>
    <p>The same discipline applies to fields nobody regulates: dimensions, wattage and warranty terms were not confirmed from an official specification sheet in this build, so they are empty too. An empty cell is a question mark. A filled-in cell that nobody verified is a lie with a font.</p>

    <h2 id="how-we-link">How the links work</h2>
    <p>Every link to Amazon on this site carries <code class="code">rel="sponsored nofollow noopener"</code> and opens in a new tab. Google's own documentation on qualifying outbound links confirms that <code class="code">sponsored</code> is the correct marker for paid or advertising links. That is applied by the build script to every Amazon anchor at once, and a check fails if any is missing it.</p>
    <p>The tracking ID supplied for this site is <code class="code">{esc(TRACKING_ID)}</code>. Whether a click is actually credited to it has not been confirmed, because confirming it needs a click from the operator's own device followed by a look at the Associates report. That is on the review queue as FLG-002 rather than being asserted here.</p>

    <h2 id="disclosure">The disclosure</h2>
    <p>{esc(DISCLOSURE)}</p>
    <p>That exact sentence is required by section 5 of the Associates Program Operating Agreement, and it appears in a strip after the masthead on every page of this site, and again in the footer. The FTC's guidance says a disclosure at the bottom of a page is easy to miss and that the closer a disclosure sits to the recommendation, the better &mdash; so an approved affiliate link will also be labelled paid next to the button. Listing citations are untagged.</p>

    <h2 id="privacy">Privacy</h2>
    <p>This site sets no cookies, loads no third-party scripts, calls no external APIs and embeds no fonts from a CDN. The typefaces are served from this repository. Analytics is off on GitHub Pages and does not transmit events there. <a href="https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection" target="_blank" rel="noopener">GitHub describes its own security logging</a>. The optional self-hosted edition is described in the <a href="{esc(rel(d, 'review/measurement.html'))}">measurement plan</a>.</p>

    <h2 id="imagery">Imagery</h2>
    <p>All eight photographs are AI-generated illustrations, labelled where they appear and never presented as a photograph of a product. <a href="{esc(rel(d, 'review/images.html'))}">Every asset is listed</a> with the rule it follows.</p>

    <h2 id="who">Who wrote this</h2>
    <p>No author is named, because there is no person whose name would be accurate to put here. This is the site's largest weakness and it is recorded as FLG-006 rather than papered over with a stock biography and an invented credential. A named editor with a true description of what they did is suggestion S-03.</p>
  </div>
  <aside class="record-side">
    <div class="side-card"><h2>At a glance</h2><dl class="side-dl">
      <div><dt>Pages</dt><dd>18</dd></div>
      <div><dt>Products</dt><dd>5 submitted, 5 observed</dd></div>
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
<p>Each was requested and read in the session that built this page on 20 November 2026. Where a quote is given, it is copied rather than paraphrased.</p></div>
{table(['Ref', 'Source', 'Used for', 'Quoted wording', 'Status'], rows, cls='sources')}
<h2 style="margin-top:3rem">Three things that could not be checked</h2>
<p class="lede-prose">These are recorded as failures rather than omitted, because a source list that only contains successes is not a source list.</p>
<div class="reject-grid">{unverified}</div>''', cls='')}"""
    return page(
        d,
        title="About and sources \u2014 Crisp & Counter",
        description="What this site is, why price and ratings are absent, how every Amazon link is marked, and the full source list with quoted wording and three sources that could not be reached.",
        body=body,
        active="index.html",
        canonical="about/",
    )


def build_ledger(page_dir, meta):
    d = page_dir
    rows = []
    body = f"""{pagehead(
        'Campaign ledger',
        'An empty ledger,<br>with its columns defined',
        'The brief asked for measurement before optimisation. The measurable unit here is a row, and a row needs a provenance note. There are none yet.',
        meta='0 ledger rows &middot; traffic and reported orders unmeasured &middot; no forecast',
    )}
{section(f'''
<div class="lede-prose">
  <p>A ledger is only worth keeping if every row can be traced back to a report somebody was authorised to read. The columns below are therefore fixed in advance, and the rule is that a row is added only when the value comes from an authorised first-party report, with the date and the source recorded alongside it.</p>
  <p>There are no rows. Not because the table was forgotten, but because no Associates report has been supplied, no analytics endpoint is live, and no traffic has been measured. A table with six plausible numbers in it would be the most damaging thing this site could publish.</p>
</div>
{table(['Report date / import timestamp', 'Source', 'Channel', 'Eligible sessions', 'Clicks', 'Reported orders', 'Provenance note'], rows, cls='ledger')}
<h2 style="margin-top:2.4rem">The provenance rule</h2>
<ol class="tight">
  <li><strong>Report date and import timestamp</strong> &mdash; keep both so the entry can be traced back to its reporting period.</li>
  <li><strong>Source</strong> &mdash; which report, in which account, exported by whom.</li>
  <li><strong>Channel</strong> &mdash; organic search, direct, referral or social, as the report labels it.</li>
  <li><strong>Eligible sessions</strong> &mdash; sessions that had a reasonable chance to reach a link, not raw page views.</li>
  <li><strong>Clicks</strong> &mdash; outbound clicks as recorded, not as estimated.</li>
  <li><strong>Reported orders</strong> &mdash; orders the Associates report attributes, including ones later returned.</li>
  <li><strong>Provenance note</strong> &mdash; one line a stranger could follow to check the row.</li>
</ol>
<h2 style="margin-top:2.4rem">What is deliberately absent</h2>
<p>No conversion rate. No revenue estimate. No commission projection. Each would require a rate card that has not been read, a traffic figure that has not been measured, and a conversion assumption with nothing behind it. The site says so instead of producing a number that looks like evidence.</p>
<div class="callout"><h2>What would put a row here</h2><p>An authorized report with a known date, scope and provenance. <a href="{esc(rel(d, 'suggestions/index.html'))}#S-01">Suggestion S-01</a>.</p></div>''', cls='')}"""
    return page(
        d,
        title="Campaign ledger \u2014 Crisp & Counter",
        description="An empty campaign ledger with its columns and provenance rule defined: date, source, channel, eligible sessions, clicks, reported orders and a note a stranger could follow.",
        body=body,
        active="index.html",
        canonical="operations/ledger.html",
    )


def build_brief(page_dir, products, questions, flags, meta):
    d = page_dir
    observed = sum(bool(p['observed_asin']) for p in products)
    rows = [
        ('Which product should each link promote?', 'Five public destinations observed; intended ASINs and attribution unconfirmed.',
         'Confirm the intended variant in Associates Central. Generate one enrolled link per product, check where it lands, and reconcile eligible credited activity before rollout.', 'https://affiliate-program.amazon.com/help/operating/policies'),
        ('What will readers search for?', 'No verified property or query dataset is on record.',
         'Verify the property and submit the sitemap. Review available page/query impressions every four weeks; refresh a guide or commission one new guide only if it answers a distinct question.', 'https://support.google.com/webmasters/answer/7576553'),
        ('Which niche or product converts?', 'No authorized order report; the tested five-event collector is off on GitHub Pages.',
         'Read first-party page and click counts alongside a separate dated Associates report. Keep denominators and reporting windows explicit; never infer orders from clicks.', 'https://affiliate-program.amazon.com/home/reports'),
        ('What can an AI drafting tool publish?', 'Drafting, not independent fact-finding or automatic publication.',
         'Require official sources for product claims, permission for imagery and API content, and a disclosure and link review before publication.', 'https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking'),
    ]
    evidence = [[esc(q), esc(known), esc(step), {'html': outbound(d, url, 'Official source')}]
                for q, known, step, url in rows]
    body = f"""{pagehead(
        'Executive summary', 'The next decisions for Crisp &amp; Counter',
        'Keep the shop useful now. Measure and confirm attribution before expanding the catalogue or making revenue claims.',
        meta='20 November 2026 &middot; evidence and next steps',
    )}
{section(f'''<div class="exec">
  <div class="exec-block">
    <h2>What shoppers can use today</h2>
    <p>Compare three air fryers and two thermometers, then use the buying guides to check fit, capacity and cleanup. The comparison reflects Amazon listing statements, not hands-on tests or rankings.</p>
    <p><strong>{observed} of {len(products)} submitted links</strong> reached listings in this recheck. That verifies observed destinations, not intended products or credit to <code class="code">{esc(TRACKING_ID)}</code>. P-04 reached a ThermoMaven listing after earlier checkpoint results. Another session observed the opposite P-04/P-05 mapping; the <a href="{esc(rel(d, 'review/index.html'))}#FLG-016">conflict remains flagged</a>. <a href="{esc(rel(d, 'products/index.html'))}">See the source for each product</a>.</p>
  </div>
  <div class="exec-block">
    <h2>What to decide, and what evidence would change the answer</h2>
    {table(['Question', 'What we know', 'How to find out', 'Source'], evidence, cls='compare')}
  </div>
  <div class="exec-block">
    <h2>Editorial brief for the next guide</h2>
    <p>Pick a meal the reader actually cooks. Open with one concrete decision, such as whether two foods finish together or whether the tray clears the door. Give a measuring step, a trade-off and a reason not to buy. Link to the relevant comparison or listing. Do not use “best,” trend claims, prices, ratings or a hands-on voice without evidence.</p>
    <p>Candidate questions: <em>Will two different sides fit without a second batch?</em> and <em>Do I need a leave-in probe or just a quick spot-check?</em> These are ideas, not verified demand. Review them against measured queries before scheduling new pieces.</p>
    <p><a class="btn" href="{esc(rel(d, 'suggestions/index.html'))}">Review suggestions</a> <a class="btn btn-ghost" href="{esc(rel(d, 'operations/launch-readiness.html'))}">Launch readiness</a> <a class="btn btn-ghost" href="{esc(rel(d, 'review/index.html'))}">Flagged for Review</a></p>
  </div>
</div>''', cls='')}"""

    return page(
        d,
        title="Executive summary \u2014 Crisp & Counter",
        description="What was built, what was verified against official sources, the one finding that changes the plan, and the next decision \u2014 in four minutes.",
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
