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
<p class="lede-prose">Two of the three high flags come from the same place: this site cannot see inside an Associates account, so which ASIN was intended and whether a click is credited are unverifiable from outside it. The third was a real defect &mdash; outbound links carried no tag parameter &mdash; and it is fixed rather than explained away. The site responds to the rest by claiming less, not by guessing more.</p>''', cls='')}
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
        description="Every uncertainty in one place: unresolved links, unconfirmed tracking, missing prices, no named author, generated imagery \u2014 each with a source to check.",
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
        meta=f'{len(images["assets"])} generated assets &middot; 0 product photographs &middot; 3 uses declined',
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
        description="Every image here is an AI-generated illustration, labelled where it appears: the asset list, the rule each follows, and what the site declined to do.",
        body=body,
        active="review/index.html",
        canonical="review/images.html",
    )


def build_measurement(page_dir, meta):
    d = page_dir
    events = [
        ("page_view", "Every page load", "Counts a visit. Stores the path only, never a query string, so nothing typed into a URL is kept."),
        ("outbound_click", "Any click on an Amazon link", "Records which product reference was clicked and the page it was clicked from. This is the number that matters for this site."),
        ("guide_open", "Opening any page under /guides/", "Separates readers who arrive on a product page from those who arrive to read, which changes what the next guide should be."),
        ("search_query_referral", "Arrival from a search engine", "Records that a referral happened and the referring host, not the query. Search Console supplies queries; this does not try to reconstruct them."),
        ("report_import", "A manual import of an Associates report", "A dated record that a first-party report was added to the ledger, with its provenance. Never an automated scrape."),
    ]
    rows = [[{"html": f'<code class="code">{esc(n)}</code>'}, esc(t), esc(w)] for n, t, w in events]
    body = f"""{pagehead(
        'Measurement plan',
        'Measurement is written,<br>and switched off',
        'Five events are defined, a client exists, and nothing is being recorded. That is the current state and it is deliberate.',
        meta='Beacon disabled by default &middot; no cookies &middot; no third-party requests &middot; no endpoint deployed',
    )}
{section(f'''
<div class="lede-prose">
  <p>The brief asked for a privacy-preserving outbound-click counter and a self-hosted analytics endpoint. Both exist in this repository. Neither is live, because shipping a live beacon before a privacy notice exists would be the wrong order of operations.</p>
  <p>The client keeps its buffer in memory and sends nothing while no endpoint is configured. It sets no cookie, writes nothing to local storage, keeps no identifier that survives a tab, and contacts no third party. It switches on when a page sets <code class="code">window.CC_ANALYTICS_ENDPOINT</code> to a first-party URL, and switching it on without an endpoint and a notice would be a mistake.</p>
</div>
<h2>What would be measured</h2>
{table(['Event', 'Fires when', 'What is stored'], rows, cls='events')}
<h2 style="margin-top:2.4rem">What has to happen before it goes live</h2>
<ol class="tight">
  <li><strong>A privacy notice.</strong> What is collected, why, for how long, and who to contact. This does not exist yet.</li>
  <li><strong>A deployed collector.</strong> The endpoint is in this repository and is not hosted anywhere. GitHub Pages serves static files only.</li>
  <li><strong>A retention decision.</strong> Raw event rows have a half-life; the ledger does not. A retention period has to be chosen, not defaulted.</li>
  <li><strong>A consent decision.</strong> Whether visitor consent is required depends on jurisdiction and on what is collected. That is a legal question, not an engineering one, and it has not been answered.</li>
</ol>
<h2 style="margin-top:2.4rem">Why the site currently claims nothing about traffic</h2>
<p>Every traffic statement on this site is an absence: no sessions, no clicks, no conversions, no revenue. That is not modesty. With the beacon off, the site genuinely has no numbers, and inventing plausible ones would be the single fastest way to make everything else on the site untrustworthy.</p>
<div class="callout">
  <h2>What the campaign ledger holds</h2>
  <p>Nothing. It has a defined schema &mdash; date, source, channel, eligible sessions, clicks, reported orders &mdash; and every row has to arrive with a provenance note. <a href="{esc(rel(d, 'operations/ledger.html'))}">See the empty ledger</a>.</p>
</div>''', cls='')}"""
    return page(
        d,
        title="Measurement plan \u2014 Crisp & Counter",
        description="The five events this site would record, the collector that is written but switched off, and the four things that must exist before any of it is switched on.",
        body=body,
        active="review/index.html",
        canonical="review/measurement.html",
    )
