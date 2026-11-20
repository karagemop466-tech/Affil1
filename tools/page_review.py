"""The review queue, the image policy, and the measurement plan."""

from layout import (blank, esc, eyebrow, outbound, page, pagehead, rel,
                    section, table)


def build_index(page_dir, flags, meta):
    d = page_dir
    fl = flags["flags"]
    order = {"high": 0, "medium": 1, "low": 2}
    fl = sorted(fl, key=lambda f: (order[f["severity"]], f["id"]))
    counts = {k: sum(1 for f in fl if f["severity"] == k) for k in order}

    cards = []
    for f in fl:
        sev = f["severity"]
        checks = "".join(
            f'<li>{_urlish(c, d)}</li>' for c in f.get("to_check", [])
        )
        cards.append(f"""<article class="flag flag-{sev}" id="{esc(f['id'])}">
  <div class="flag-top">
    <span class="flag-id">{esc(f['id'])}</span>
    <span class="pill pill-{ 'block' if sev=='high' else ('warn' if sev=='medium' else 'none') }">{esc(sev)}</span>
  </div>
  <h3>{esc(f['title'])}</h3>
  <dl class="flag-dl">
    <div><dt>Expected</dt><dd>{esc(f['expected'])}</dd></div>
    <div><dt>Found</dt><dd>{esc(f['found'])}</dd></div>
    <div><dt>How to read it</dt><dd>{esc(f['reading'])}</dd></div>
    <div><dt>What the site does about it</dt><dd>{esc(f['impact'])}</dd></div>
    <div><dt>Blocks</dt><dd>{esc(f['blocks'])}</dd></div>
  </dl>
  {'<div class="flag-check"><p class="q-label">Where to check it yourself</p><ul>' + checks + '</ul></div>' if checks else ''}
</article>""")

    flag_rows = []
    for f in fl:
        flag_rows.append([
            {"html": f'<a href="#{esc(f["id"])}"><strong>{esc(f["id"])}</strong></a>'},
            {"html": f'<span class="pill pill-{"block" if f["severity"]=="high" else ("warn" if f["severity"]=="medium" else "none")}">{esc(f["severity"])}</span>'},
            {"html": esc(f["title"])},
            {"html": esc(f["blocks"])},
            {"html": esc(f["severity"] == "high" and "Correctness or revenue" or (f["severity"] == "medium" and "Usefulness" or "Cosmetic"))},
        ])
    flag_table = table(["Ref", "Severity", "What is flagged", "Blocks", "Affects"], flag_rows,
                       cls="flags", caption=f"{len(fl)} items, ordered by severity")

    body = f"""{pagehead(
        'Review queue',
        'Flagged for review',
        f'{len(fl)} items where this site is less certain than it would like to be. Nothing here is hidden from the site &mdash; each flag names the page it affects and what a reviewer should check.',
        meta=f'{counts["high"]} high &middot; {counts["medium"]} medium &middot; {counts["low"]} low &middot; none of these block the site from being live',
    )}
{section(f'''
<div class="stat-row">
  <div class="stat stat-warn"><span class="stat-n">{counts['high']}</span><span class="stat-l">high &mdash; affects money or correctness</span></div>
  <div class="stat"><span class="stat-n">{counts['medium']}</span><span class="stat-l">medium &mdash; affects usefulness</span></div>
  <div class="stat"><span class="stat-n">{counts['low']}</span><span class="stat-l">low &mdash; cosmetic or administrative</span></div>
</div>
<p class="lede-prose">Several high flags share a cause: this site cannot see inside an Associates account. Everything that requires that view &mdash; which ASIN was intended, whether the tag applies, whether a click is credited &mdash; is unverifiable from outside it. The site responds by claiming less, not by guessing more.</p>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Index')}<h2>Every flag in one table</h2></div><p>Scan here, then read the card below for the detail and the source to check.</p></div>
{flag_table}
''', cls='')}
{section(''.join(cards), cls='')}
{section(f'''
<div class="crosslinks">
  <a class="crosslink" href="{esc(rel(d, 'review/images.html'))}"><h3>Image policy</h3><p>Every photograph on this site is generated. Here is every asset, where it appears, and the rule it follows.</p></a>
  <a class="crosslink" href="{esc(rel(d, 'review/measurement.html'))}"><h3>Measurement plan</h3><p>Five events, a collector that is written but switched off, and why it is off.</p></a>
  <a class="crosslink" href="{esc(rel(d, 'questions/index.html'))}"><h3>Open questions</h3><p>The same uncertainty, organised as questions with the document that would close each one.</p></a>
</div>''', cls='section-tint')}"""
    return page(
        d,
        title="Flagged for review \u2014 Crisp & Counter",
        description="Every uncertainty on this site in one place: unresolved links, unconfirmed tracking, missing prices, absent authorship and generated imagery, each with the source to check it against.",
        body=body,
        active="review/index.html",
        canonical="review/",
    )


def _urlish(text, d):
    from layout import AFFILIATE_HINT, product_link
    if text.startswith("http"):
        if AFFILIATE_HINT.search(text):
            return product_link(d, text, esc(text),
                                aria="Open this Amazon listing (affiliate link, opens in a new tab)")
        return outbound(d, text, esc(text))
    return esc(text)


def build_images(page_dir, images, products, meta):
    d = page_dir
    rows = []
    for a in images["assets"]:
        rows.append([
            {"html": f'<strong>{esc(a["file"])}</strong><br><span class="tiny">{esc(a["alt"])}</span>'},
            {"html": '<span class="pill pill-warn">AI generated</span>'},
            {"html": esc(a["used_on"])},
            {"html": esc(a["rules_met"])},
        ])
    rejected = "".join(
        f'<article class="reject"><h3>{esc(r["idea"])}</h3><p>{esc(r["why_not"])}</p>'
        f'<p class="tiny">Source: <a href="{esc(rel(d, r["source"]))}">{esc(r.get("source_id") or "sources")}</a></p></article>'
        for r in images["rejected"]
    )
    body = f"""{pagehead(
        'Image policy',
        'Every photograph here<br>is an illustration',
        images["meta"]["why"],
        meta='8 generated assets &middot; 0 product photographs &middot; 3 uses declined',
    )}
{section(f'''
<h2>The rule</h2>
<p class="lede-prose">{esc(images['meta']['rule'])}</p>
<h2 style="margin-top:2.4rem">Every asset</h2>
{table(['Asset', 'Source', 'Appears on', 'How the rule is met'], rows, cls='assets')}
<h2 style="margin-top:2.4rem">Three things this site declined to do</h2>
<div class="reject-grid">{rejected}</div>
<div class="callout">
  <h2>Why this page exists at all</h2>
  <p>A shopper scanning a product page does not carefully separate the photograph from the product. If an image of a beautiful uncluttered kitchen sits above a buy button, most people will read it as a picture of the thing being sold. That is the risk, and it is why every use carries a visible label rather than a footnote.</p>
  <p>The alternative &mdash; real photographs of the real products &mdash; requires owning them. That is item S-12 on the <a href="{esc(rel(d, 'suggestions/index.html'))}">suggestion queue</a>.</p>
</div>''', cls='')}"""
    return page(
        d,
        title="Image policy \u2014 Crisp & Counter",
        description="Every image on this site is AI-generated illustration, labelled where it appears. Here is the full asset list, the rule each follows, and what the site declined to do.",
        body=body,
        active="review/index.html",
        canonical="review/images.html",
    )


def build_measurement(page_dir, meta):
    d = page_dir
    events = [
        ("page_view", "Every page render", "Counts a visit. Stores the path with the query string stripped, so nothing typed into a URL is kept."),
        ("outbound_product_click", "Any click on an Amazon link", "Records which ASIN was clicked and the page it was clicked from. This is the number that matters for this site, and it is still not a sale."),
        ("guide_read_75", "A reader reaches 75% of a guide's height", "Separates readers who arrive to read from those who bounce. Crude: it measures scroll, not comprehension."),
        ("compare_view", "The comparison page renders", "Tests whether readers want side-by-side data more than prose. That answer decides what the next page should be."),
        ("flag_page_view", "The review queue is opened", "Shows whether the verification work is actually consulted, or whether it is furniture."),
    ]
    rows = [[{"html": '<code class="code">%s</code>' % esc(n)}, esc(t), esc(w)] for n, t, w in events]

    body = f"""{pagehead(
        'Measurement',
        'Five events,<br>and a collector that is off',
        'The client is written, the collector is written and tested, and neither is switched on. That is the state, and this page explains why it is the right one until an endpoint is deployed.',
        meta='Beacon disabled by default &middot; no cookies &middot; honouring GPC and DNT &middot; no third-party requests',
    )}
{section(f'''
<div class="lede-prose">
  <p>The brief asked for a privacy-preserving outbound-click counter and a self-hosted analytics endpoint, and for click and conversion measurement to exist before more writing. All three exist in this repository. The first two are live in code; the third is not live on the internet, because GitHub Pages serves static files and nothing else.</p>
  <p>What that means in plain terms: the site currently knows nothing about its readers. It has no sessions, no clicks, no conversion rate and no revenue. Those numbers are absent, not estimated.</p>
</div>
<h2>What each event answers</h2>
{table(['Event', 'Fires when', 'What it is for, and what it is not'], rows, cls='events')}
<h2 style="margin-top:2.4rem">What is collected, precisely</h2>
<p>Four fields per event: the event name, the page path with the query string removed, the product ASIN for a click, and the date. That is the complete list. The client sets no cookie, writes nothing to local storage, and sends nothing if Global Privacy Control or Do Not Track is present.</p>
<p>The collector in <code class="code">analytics/collect.py</code> does not read the client address, does not read the user agent, does not read the referer header, and rejects any field not on that list. It stores an integer count per day, per event, per path. There is no per-visitor record to retain, breach or join to anything else.</p>
<h2 style="margin-top:2.4rem">Why conversions are not an event</h2>
<p>A browser cannot see what happens after a click leaves for Amazon. Any site claiming to measure conversions from its own beacon is either guessing or describing Amazon's report. Reported orders, when they exist, will come from the Associates report and will be entered in the <a href="{esc(rel(d, 'operations/ledger.html'))}">campaign ledger</a> with a date and a provenance note.</p>
<h2 style="margin-top:2.4rem">What has to happen before it goes live</h2>
<ol class="tight">
  <li><strong>Deploy the collector somewhere that can run a process.</strong> A container, a small VPS or a serverless function all work. GitHub Pages cannot host it.</li>
  <li><strong>Set one line.</strong> <code class="code">window.CC_ANALYTICS_ENDPOINT</code> in the page shell in <code class="code">tools/layout.py</code>, then rebuild. That is the entire integration.</li>
  <li><strong>Publish the privacy notice.</strong> It exists at <a href="{esc(rel(d, 'privacy.html'))}">/privacy.html</a> and describes exactly these four fields.</li>
  <li><strong>Send one test event and read it back.</strong> The collector exposes an aggregate summary endpoint so the check is a number, not a hope.</li>
</ol>
<h2 style="margin-top:2.4rem">The order that actually works</h2>
<p>Tag the links, confirm one click in the Associates report, then measure. This site's links are now tagged and enforced by the build; the confirmation inside the account is still outstanding and is recorded as FLG-002. Measuring traffic before that confirmation would produce a chart of people arriving at a door that may not open.</p>
<div class="callout">
  <h2>What the campaign ledger holds</h2>
  <p>Nothing. It has a defined schema and a provenance rule, and no rows, because no authorised report has been supplied. <a href="{esc(rel(d, 'operations/ledger.html'))}">See the empty ledger</a>.</p>
</div>''', cls='')}"""
    return page(
        d,
        title="Measurement \u2014 Crisp & Counter",
        description="The five events this site records, the self-hosted collector that is written and tested but not deployed, and the four steps that would switch it on.",
        body=body,
        active="review/index.html",
        canonical="review/measurement.html",
    )
