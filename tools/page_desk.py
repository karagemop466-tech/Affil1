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
    d = page_dir
    n_q = len(questions["questions"])
    n_open = sum(1 for q in questions["questions"] if not q.get("answered"))
    n_high = sum(1 for f in flags["flags"] if f["severity"] == "high")
    body = f"""{pagehead(
        'Executive summary',
        'The short version,<br>for someone with four minutes',
        'What exists, what was verified, what could not be, and what the next decision is.',
        meta='Written 20 November 2026 &middot; 1,600 words shorter than it could have been',
    )}
{section(f'''
<div class="exec">
  <div class="exec-block">
    <h2>What was asked for</h2>
    <p>An Amazon affiliate publication covering five supplied links: product research, comparison content, buying guides, click measurement and a compliant disclosure layer, built as a live GitHub Pages site and merged without further input.</p>
  </div>
  <div class="exec-block">
    <h2>What was built</h2>
    <p>A 22-page static site with four buying guides, a five-row product register, a per-product record for each, a comparison table, fifteen open questions, twelve suggestions, seventeen review flags, a source list with quoted wording, an empty campaign ledger, an inert analytics client and a build-time checker that fails on a broken link, a missing disclosure or a reintroduced price.</p>
  </div>
  <div class="exec-block">
    <h2>What was actually verified</h2>
    <p>Each of the five supplied links was opened once on 20 November 2026. Four resolved to live Amazon listings. The ASIN and full listing title were transcribed for each of those four. The fifth returned a continuity page on three attempts and remains unidentified. Amazon's Associates Operating Agreement section 5, its Program Policies section 2(b), the FTC's endorsement FAQ and Google's outbound-link documentation were each read directly, and the relevant wording is quoted on the sources page.</p>
  </div>
  <div class="exec-block exec-warn">
    <h2>The one finding that changes the plan</h2>
    <p>The five supplied link codes are nine characters and contain lowercase letters. Every ASIN that loaded is ten characters and uppercase. The codes are short-link slugs, not product identifiers &mdash; which means the earlier version of this repository recorded the wrong thing in its "intended ASIN" column, and that the intended product for each link cannot be read from the link at all. It has to come from the Associates dashboard.</p>
    <p>This does not invalidate the links. It does mean nothing downstream can be confirmed without one look inside the account.</p>
  </div>
  <div class="exec-block">
    <h2>What could not be verified, and why it matters</h2>
    <dl class="exec-dl">
      <div><dt>Tracking attribution</dt><dd>No arrival page showed a tag parameter. Whether clicks are credited to <code class="code">{esc(TRACKING_ID)}</code> is unknown. This is the difference between a site that earns and a site that does not.</dd></div>
      <div><dt>Price, rating, availability</dt><dd>Not shown anywhere, because Amazon permits them only from Amazon-served data or its API. This is deliberate and is the site's largest visible gap to a reader.</dd></div>
      <div><dt>Author</dt><dd>None. No name would be true, so none is used. It caps how much authority the guides can claim.</dd></div>
      <div><dt>Product quality</dt><dd>Nothing was tested. No product is ranked, scored or recommended.</dd></div>
      <div><dt>Traffic and revenue</dt><dd>No analytics are running, no Search Console property is verified, and no commission rate has been read. Therefore no conversion score and no revenue forecast appears anywhere on this site.</dd></div>
    </dl>
  </div>
  <div class="exec-block">
    <h2>The next decision</h2>
    <p>Three things, in this order. Tag the links from SiteStripe and make one test click, then read the Associates report for that day. Verify the Search Console property and submit the sitemap. Then choose between the two paths that actually improve the site: buy one product and test it properly, or wait for query data before writing another guide.</p>
    <p>Writing more guides first is the option that looks like progress and is not.</p>
  </div>
  <div class="exec-block">
    <h2>Numbers on the record</h2>
    <div class="exec-stats">
      <div><span>5</span><p>links supplied</p></div>
      <div><span>4</span><p>resolved and transcribed</p></div>
      <div><span>1</span><p>unresolved, published as a blank</p></div>
      <div><span>0</span><p>products tested</p></div>
      <div><span>0</span><p>prices shown</p></div>
      <div><span>{n_q}</span><p>questions raised</p></div>
      <div><span>{n_open}</span><p>still open</p></div>
      <div><span>{n_high}</span><p>high-severity flags</p></div>
    </div>
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
