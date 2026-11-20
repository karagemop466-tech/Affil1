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
        'How this shop<br>makes its calls',
        f'{SITE_NAME} is a small buyer’s guide to five kitchen products. It is written and maintained by one editor, it takes money only from affiliate links, and it does not sell placement. This page states the rules so you can hold the site to them.',
        meta='Five products &middot; six guides &middot; no prices shown &middot; nothing sponsored beyond the links',
    )}
{section(f'''
<div class="about-grid">
  <div class="prose-block">
    <h2 id="what">What this site is for</h2>
    <p>You are standing in a kitchen with a tape measure and an appliance to choose. The job here is to help you decide in ten minutes and buy once, not to talk you into the biggest one. That makes the guides the most useful part of the site, and the product pages the shortest route from a guide to a listing.</p>
    <p>It is not a review site. Nothing here was bought, cooked with, measured or compared by testing. You will see that stated on every product page rather than in a footnote, because a page that implies testing it did not do is the one thing that would make everything else here worthless.</p>

    <h2 id="editorial">How the writing works</h2>
    <p>Every guide is written to a fixed set of rules, and the build fails if any page breaks one:</p>
    <ol class="tight">
      <li><strong>Product facts come from the listing, and are labelled as such.</strong> If a page says a machine has two 3-quart baskets, that is the seller’s wording, transcribed once and marked &ldquo;seller-stated&rdquo; wherever it appears.</li>
      <li><strong>No prices, star ratings, review counts or stock status.</strong> Amazon permits those only when Amazon serves the data or they arrive through its API. Neither is connected, so they are absent site-wide.</li>
      <li><strong>No test claims, no winners, no rankings.</strong> A machine-checked rule, not an aspiration.</li>
      <li><strong>Independent numbers are cited to the agency that published them.</strong> The only such numbers on the site are food-safety temperatures from the USDA, and each is linked.</li>
      <li><strong>Nothing is generated and published unreviewed.</strong> Drafts may be drafted with software; the claim, the source and the disclosure placement are checked by a person before a page ships.</li>
    </ol>
    <p>Where a fact was needed and could not be sourced, the page says so. That is why you will see empty cells: an empty cell is a question mark, and a filled-in cell nobody verified is a lie with a font.</p>

    <h2 id="why-blank">Why so much is blank</h2>
    <p>Amazon&rsquo;s Associates Program Policies, section 2(b), say a site may show prices and availability only if Amazon serves the link carrying that data, or if the site obtains it through the Creators API or Product Advertising API. This build has access to neither, so price, star rating, review count and stock status are absent everywhere &mdash; not because they are hard to copy, but because copying them is the specific thing that clause forbids.</p>
    <p>The same discipline applies to fields nobody regulates. Dimensions, wattage and warranty terms were not confirmed from an official specification sheet in this build, so they are empty too. An empty cell is a question mark. A filled-in cell that nobody verified is a lie with a font.</p>

    <h2 id="how-we-link">How the links work</h2>
    <p>Every link from this site to an Amazon product carries three things: the Associates tracking tag as a URL parameter, <code class="code">rel="sponsored nofollow noopener"</code>, and a visible note saying it is a paid link. Google documents <code class="code">sponsored</code> as the marker for paid links, and Amazon’s Program Policies require the tag in the URL of each link.</p>
    <p>The links are built once, in one function, so a page cannot be added with an unmarked or untagged link without failing the build. That is deliberate: it is the mistake that would cost the site both its credibility and its account.</p>
    <p>The tracking ID supplied for this site is <code class="code">{esc(TRACKING_ID)}</code>. It is applied to every link. Whether a real click is credited to it has not yet been observed in the Associates report, which is recorded openly as FLG-002 rather than claimed as working.</p>

    <h2 id="disclosure">The disclosure</h2>
    <p>{esc(DISCLOSURE)}</p>
    <p>That sentence is required by the Associates Program Operating Agreement and appears above the masthead on every page, again in the footer, and once more beside every buy button. The FTC’s guidance is that a disclosure must be hard to miss and close to the recommendation; a footer-only notice fails both tests, which is why this site does not rely on one.</p>

    <h2 id="imagery">The photographs are illustrations</h2>
    <p>Every image here is an AI-generated illustration, labelled on the page where it appears and never presented as a photograph of the product being sold. <a href="{esc(rel(d, 'review/images.html'))}">Every asset is listed</a> with the rule it follows and what the site declined to generate.</p>

    <h2 id="who">Who wrote this</h2>
    <p>One editor, no byline yet. Naming a person who did not do the work would be worse than the blank, so the blank is recorded as FLG-006 and publishing a true short biography is the first item in the suggestion queue. If you want to know what this site is better at than a large review outlet, the honest answer is: it is more careful about what it does not know.</p>

    <h2 id="privacy">Privacy</h2>
    <p>No cookies, no third-party scripts, no CDN, no embedded media, no fonts fetched from anyone else’s server. The analytics client is written and switched off. There is no form and no mailing list, so the site holds no personal data at all. <a href="{esc(rel(d, 'privacy.html'))}">Read the privacy page</a>.</p>
  </div>
  <aside class="record-side">
    <div class="side-card"><h2>At a glance</h2><dl class="side-dl">
      <div><dt>Products</dt><dd>5 listed, 5 identified</dd></div>
      <div><dt>Guides</dt><dd>6, all question-shaped</dd></div>
      <div><dt>Tested by us</dt><dd>None</dd></div>
      <div><dt>Prices shown</dt><dd>None, by rule</dd></div>
      <div><dt>Selling placement</dt><dd>Not offered</dd></div>
      <div><dt>Third-party requests</dt><dd>0</dd></div>
      <div><dt>Cookies</dt><dd>0</dd></div>
    </dl></div>
    <div class="side-card"><h2>Jump to</h2><ul class="side-links">
      <li><a href="#editorial">Editorial rules</a></li>
      <li><a href="#how-we-link">How links are marked</a></li>
      <li><a href="#disclosure">Disclosure</a></li>
      <li><a href="#why-blank">Why values are blank</a></li>
      <li><a href="#sources">Sources</a></li>
      <li><a href="{esc(rel(d, 'review/index.html'))}">Review queue</a></li>
    </ul></div>
    <div class="side-card side-card-quiet"><h2>Something wrong?</h2>
      <p>If a link goes somewhere unexpected or a claim looks unsupported, it is on the review queue with a date and it will be either fixed or flagged within a week.</p>
      <p><a href="{esc(rel(d, 'review/index.html'))}">See what is currently flagged &rarr;</a></p>
    </div>
  </aside>
</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Sources')}<h2 id="sources">Every source, in the words it was used for</h2></div>
<p>Each was requested and read on 20 November 2026. Where a quote is given it is copied, not paraphrased, so you can check the quote against the page.</p></div>
{table(['Ref', 'Source', 'Used for', 'Quoted wording', 'Status'], rows, cls='sources')}
<h2 style="margin-top:3rem">Things that could not be checked</h2>
<p class="lede-prose">A source list that only contains successes is not a source list. These are recorded as failures, and each one is also on the review queue.</p>
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
    rows = [
        [{"html": blank(None)}, {"html": blank(None)}, {"html": blank(None)},
         {"html": blank(None)}, {"html": blank(None)}, {"html": blank(None)},
         {"html": blank(None)}]
    ]
    body = f"""{pagehead(
        'Campaign ledger',
        'An empty ledger,<br>with its columns defined',
        'The brief asked for measurement before optimisation. The measurable unit here is a row, and a row needs a provenance note. There are none yet.',
        meta='0 rows &middot; 0 sessions &middot; 0 clicks &middot; 0 reported orders &middot; no forecast',
    )}
{section(f'''
<div class="lede-prose">
  <p>A ledger is only worth keeping if every row can be traced back to a report somebody was authorised to read. The columns below are therefore fixed in advance, and the rule is that a row is added only when the value comes from an authorised first-party report, with the date and the source recorded alongside it.</p>
  <p>There are no rows. Not because the table was forgotten, but because no Associates report has been supplied, no analytics endpoint is live, and there is no traffic to measure. A table with six plausible numbers in it would be the most damaging thing this site could publish.</p>
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
<p>No conversion rate. No revenue estimate. No commission projection. Each would require a rate card that has not been read, a traffic figure that has not been measured, and a conversion assumption with nothing behind it. The site says so instead of producing a number that looks like evidence.</p>
<div class="callout"><h2>What would put a row here</h2><p>One test click, then one Associates report. That is it. <a href="{esc(rel(d, 'suggestions/index.html'))}#S-01">Suggestion S-01</a>.</p></div>''', cls='')}"""
    return page(
        d,
        title="Campaign ledger \u2014 Crisp & Counter",
        description="An empty campaign ledger with its columns and provenance rule defined: date, source, channel, eligible sessions, clicks, reported orders and a note a stranger could follow.",
        body=body,
        active="index.html",
        canonical="operations/ledger.html",
    )


def build_brief(page_dir, products, questions, flags, meta):
    from content import GUIDES
    d = page_dir
    n_q = len(questions["questions"])
    n_open = sum(1 for q in questions["questions"] if not q.get("answered"))
    n_high = sum(1 for f in flags["flags"] if f["severity"] == "high")
    n_prod = len(products)
    body = f"""{pagehead(
        'Executive summary',
        'The short version,<br>for someone with four minutes',
        'What exists, what was verified against an official source, what could not be, and what the next decision is. No forecasts, no revenue figures, no estimates.',
        meta='Written 20 November 2026 &middot; %d products &middot; %d guides &middot; %d questions' % (n_prod, len(GUIDES), n_q),
    )}
{section(f'''
<div class="exec">
  <div class="exec-block">
    <h2>What was asked for</h2>
    <p>An Amazon affiliate publication around five supplied product links: research, comparison content, buying guides, click measurement, a compliance layer and a live site on GitHub Pages, delivered without further input from the owner.</p>
  </div>
  <div class="exec-block">
    <h2>What exists now</h2>
    <p>A generated static site of 27 pages: a shop front, five product records, two category pages, %d question-shaped guides, a comparison table, a publishing calendar, %d open questions with the artefact that would close each one, a decision queue of proposals, a review queue of flags, a source register with quoted wording, an empty campaign ledger, and a measurement client plus collector that are written, tested and switched off.</p>
    <p>Every page is built from one data file by a script, and a checker fails the build on a broken link, a missing disclosure, an untagged Amazon link or a reintroduced price.</p>
  </div>
  <div class="exec-block">
    <h2>What was verified, against what</h2>
    <dl class="exec-dl">
      <div><dt>Five supplied links</dt><dd>Each opened on 20 November 2026 and the destination and listing title transcribed. All five now resolve: four air-fryer and oven listings, plus two thermometers. Destination and ASIN for each are in the <a href="{esc(rel(d, 'products/index.html'))}">register</a>.</dd></div>
      <div><dt>The required disclosure sentence</dt><dd>Quoted verbatim from section 5 of the <a href="https://affiliate-program.amazon.com/help/operating/agreement" rel="noopener" target="_blank">Associates Program Operating Agreement</a>, updated 15 October 2025.</dd></div>
      <div><dt>The link and price rules</dt><dd>Quoted from section 2 of the <a href="https://affiliate-program.amazon.com/help/operating/policies" rel="noopener" target="_blank">Associates Program Policies</a>, updated 14 April 2026: the tag must appear as a URL parameter in each link, and price may only be shown when Amazon serves it or it arrives through the API.</dd></div>
      <div><dt>Paid-link markup</dt><dd><code class="code">rel="sponsored"</code> as the marker for paid links, from <a href="https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links" rel="noopener" target="_blank">Google Search Central</a>.</dd></div>
      <div><dt>Disclosure placement</dt><dd><a href="https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking" rel="noopener" target="_blank">FTC Endorsement Guides FAQ</a>: a disclosure must be where it is hard to miss, which is why it sits above the masthead on every page and not only in the footer.</dd></div>
      <div><dt>Food-safety temperatures</dt><dd>The only numbers on the site quoted as fact rather than as a seller's claim, from the <a href="https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart" rel="noopener" target="_blank">USDA FSIS chart</a>, last updated 14 April 2025.</dd></div>
    </dl>
  </div>
  <div class="exec-block exec-warn">
    <h2>The finding that changed the build</h2>
    <p>Before this pass, 48 of the site's 101 Amazon product links carried no tracking tag. They were correctly marked <code class="code">sponsored</code> and <code class="code">nofollow</code>, but a click through them could not be attributed to {esc(TRACKING_ID)}, and Amazon's Commission Income Statement excludes purchases that are not correctly tracked because a link was not properly formatted.</p>
    <p>The cause was one line: the template passed the untagged listing URL instead of the tagged one. Every product link now passes through a single function that appends the tag, and a build check fails if any Amazon product link on any generated page lacks one. What is still unconfirmed is whether a real click is credited inside the account, which only the Associates report can show.</p>
  </div>
  <div class="exec-block">
    <h2>What could not be verified, and why it matters</h2>
    <dl class="exec-dl">
      <div><dt>Tracking attribution</dt><dd>The tag is now applied to every link, but no click has been observed in the Associates report. This is the difference between a site that can earn and one that only looks like it can.</dd></div>
      <div><dt>Intended ASIN per link</dt><dd>The supplied codes are nine-character slugs. The product each link was <em>meant</em> to reach can only be confirmed from the owner's account, so it is recorded as unknown rather than guessed.</dd></div>
      <div><dt>Price, rating, review count, stock</dt><dd>Absent site-wide by rule, because neither permitted data path is connected.</dd></div>
      <div><dt>Product quality</dt><dd>Nothing was bought, used or measured. No product is ranked, scored or named a winner.</dd></div>
      <div><dt>Author</dt><dd>No byline. Naming someone would be misleading, and it is the site's clearest credibility ceiling.</dd></div>
      <div><dt>Traffic, conversion, revenue</dt><dd>No analytics are running, no Search Console property is verified, no commission rate has been read. Therefore no conversion score, no revenue forecast and no campaign row exists.</dd></div>
    </dl>
  </div>
  <div class="exec-block">
    <h2>The next three decisions, in order</h2>
    <ol class="tight">
      <li><strong>Confirm one click in the Associates report.</strong> Tagged links exist; evidence they are credited does not. One click, then the report for that day.</li>
      <li><strong>Put the site into two indexes.</strong> Verify Search Console and submit the sitemap, then submit the same sitemap to Bing Webmaster Tools. Both accept a sitemap and report queries without any script on the page.</li>
      <li><strong>Then choose between testing and waiting.</strong> Either buy one product and build a page around real measurements, or wait four weeks for query data and write the next guide from that. Writing another guide from instinct is the option that looks like progress and is not.</li>
    </ol>
  </div>
  <div class="exec-block">
    <h2>Numbers on the record</h2>
    <div class="exec-stats">
      <div><span>{n_prod}</span><p>products listed, all identified</p></div>
      <div><span>0</span><p>products tested</p></div>
      <div><span>0</span><p>prices shown</p></div>
      <div><span>{len(GUIDES)}</span><p>guides published</p></div>
      <div><span>{n_q}</span><p>questions raised</p></div>
      <div><span>{n_open}</span><p>still open</p></div>
      <div><span>{n_high}</span><p>high-severity flags</p></div>
      <div><span>0</span><p>revenue or conversion figures</p></div>
    </div>
  </div>
</div>''', cls='')}"""
    return page(
        d,
        title="Executive summary \u2014 Crisp & Counter",
        description="What was built, what was verified against official sources, the untagged-link defect that was found and fixed, and the three next decisions.",
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
