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
<p class="lede-prose">The three high flags share a cause: this site cannot see inside an Associates account. Everything that requires that view &mdash; which ASIN was intended, whether the tag applies, whether a click is credited &mdash; is unverifiable from outside it. The site responds by claiming less, not by guessing more.</p>''', cls='')}
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
    from layout import AFFILIATE_HINT, product_link, tag_url
    if text.startswith("http"):
        if AFFILIATE_HINT.search(text):
            return product_link(d, tag_url(text), esc(text),
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
        ("page_view", "Every page load", "Counts a visit. Stores the path only, never a query string, so nothing typed into a URL is kept."),
        ("outbound_click", "Any click on an Amazon link", "Records which product reference was clicked and the page it was clicked from. This is the number that matters for this site."),
        ("guide_open", "Opening a guide from the index", "Separates readers who arrive on a product page from those who arrive to read, which changes what the next guide should be."),
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
  <p>The client writes to <code class="code">sessionStorage</code> to keep one page view from being counted twice in a single tab, and sends nothing. It has no cookie, sets no identifier that persists across days, and contacts no third party. It is switched on by setting one flag on the page, and switching it on without an endpoint and a notice would be a mistake.</p>
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


def build_verification(page_dir, verification, sources, meta):
    """The dated line-by-line log: links opened, sources read, findings."""
    d = page_dir
    v = verification

    link_rows = []
    for r in v["links"]:
        cls = "pill-ok" if r["result"] == "resolved" else "pill-warn"
        link_rows.append([
            {"html": f'<a href="{esc(rel(d, "products/" + r["ref"].lower() + ".html"))}"><strong>{esc(r["ref"])}</strong></a>'},
            {"html": f'<code class="code">{esc(r["submitted"])}</code>'},
            {"html": f'<code class="code">{esc(r["asin"])}</code>'},
            {"html": f'<span class="pill {cls}">{esc(r["result"])}</span>'},
            {"html": esc(r["tag_in_final_url"])},
            {"html": esc(r["note"])},
        ])

    src_rows = []
    for s in sources["sources"]:
        status_cls = "pill-ok" if s["status"].startswith("read") else "pill-none"
        src_rows.append([
            {"html": f'<strong>{esc(s["id"])}</strong>'},
            {"html": f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a><br><span class="tiny">{esc(s["publisher"])}</span>'},
            {"html": esc(s.get("read_on", "\u2014"))},
            {"html": f'<span class="pill {status_cls}">{esc(s["status"])}</span>'},
            {"html": esc(s["used_for"])},
        ])

    finding_cards = "".join(f"""<article class="flag" id="{esc(f['id'])}">
  <div class="flag-top"><span class="flag-id">{esc(f['id'])}</span></div>
  <h3>{esc(f['title'])}</h3>
  <dl class="flag-dl">
    <div><dt>What was observed</dt><dd>{esc(f['what'])}</dd></div>
    <div><dt>What it means</dt><dd>{esc(f['means'])}</dd></div>
    <div><dt>What the site did about it</dt><dd>{esc(f['action'])}</dd></div>
  </dl>
  <div class="flag-check"><p class="q-label">Check it yourself</p><ul><li>{_urlish(f['check'], d)}</li></ul></div>
</article>""" for f in v["findings"])

    body = f"""{pagehead(
        'Verification log',
        'What was checked,<br>and what came back',
        f'Every supplied link and every policy claim on this site, re-opened on {esc(v["meta"]["checked_on"])}. {len(v["links"])} links, {len(sources["sources"])} sources, {len(v["findings"])} findings, including one that changes where the money goes.',
        meta='A row is confirmed here only when this session opened the source and read it',
    )}
{section(f'''
<div class="reg-lede">
  <div>
    <h2>Why a log rather than a badge</h2>
    <p>A verification badge is a claim about a process nobody can see. This page is the process: the link, the
    date, what came back, and what changed because of it. Where an earlier session recorded something different,
    both observations are kept, because the disagreement is information.</p>
    <p>{esc(v['meta']['method'])}</p>
  </div>
  <dl class="reg-stats">
    <div><dt>Links opened</dt><dd>{len(v['links'])}</dd></div>
    <div><dt>Resolved</dt><dd>{sum(1 for r in v['links'] if r['result'].startswith('resolved'))}</dd></div>
    <div><dt>Tag seen on arrival</dt><dd>0</dd></div>
    <div><dt>Sources read</dt><dd>{len(sources['sources'])}</dd></div>
  </dl>
</div>
{table(['Ref', 'Submitted link', 'ASIN on arrival', 'Result', 'Tag in final URL', 'Note'], link_rows, cls='register',
       caption='Five supplied links, requested on 2026-11-20',
       note='The submitted link is recorded here as text. It is not offered as a click target anywhere on the site; the buy links are built from the ASIN instead.')}''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Policy sources')}<h2>What was read, and when</h2></div>
<p>Quoted wording for each sits on the <a href="{esc(rel(d, 'about/index.html'))}#sources">sources page</a>.</p></div>
{table(['Ref', 'Source', 'Read on', 'Outcome', 'Used for'], src_rows, cls='sources')}''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Findings')}<h2>Nine things this pass changed</h2></div>
<p>Two of them changed what the site says. One of them changed whether the site can earn.</p></div>
<div class="dec-stack">{finding_cards}</div>''', cls='')}
{section(f'''
<div class="callout">
  <h2>What is still not verified</h2>
  <p>Whether a click is credited to <code class="code">shopnow047c-20</code>. That requires a click and a report,
  and neither exists yet. Until it does, every page on this site describes the links as tagged and the
  attribution as unconfirmed, which is exactly what is known.</p>
  <p><a class="tlink" href="{esc(rel(d, 'questions/decisions.html'))}#D-01">The decision that closes it <span aria-hidden="true">&rarr;</span></a></p>
</div>''', cls='')}"""

    return page(
        d,
        title="Verification log \u2014 what was checked on 2026-11-20 \u2014 Crisp & Counter",
        description=("Every supplied link opened, every policy source read, and nine findings from the pass "
                     "of 2026-11-20 \u2014 including the missing tracking parameter that the site now builds in."),
        body=body,
        active="review/index.html",
        canonical="review/verification.html",
    )
