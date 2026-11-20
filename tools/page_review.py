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
            {"html": _urlish(next(c for c in f["to_check"] if c.startswith("https://")),d)},
            {"html": esc(f["severity"] == "high" and "Correctness or revenue" or (f["severity"] == "medium" and "Usefulness" or "Cosmetic"))},
        ])
    flag_table = table(["Ref", "Severity", "What is flagged", "Blocks", "Source", "Affects"], flag_rows,
                       cls="flags", caption="15 items, ordered by severity")

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
    from layout import AFFILIATE_HINT, product_link
    if text.startswith("http"):
        if AFFILIATE_HINT.search(text):
            return product_link(d, text, "Amazon listing",
                                aria="Open this Amazon listing (affiliate link, opens in a new tab)")
        return outbound(d, text, esc(text.split("/")[2]))
    return esc(text)


def build_images(page_dir, images, products, meta):
    d = page_dir
    rows = []
    for a in images["assets"]:
        rows.append([
            {"html": f'<strong>{esc(a["file"])}</strong><br><span class="tiny">{esc(a["alt"])}</span>'},
            {"html": outbound(d,'https://github.com/karagemop466-tech/Affil1/blob/main/src/data/images.json','Image provenance')},
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
        meta='9 generated assets &middot; 0 product photographs &middot; 3 uses declined',
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
    import json
    from layout import ROOT
    spec=json.loads((ROOT/'src/data/events.json').read_text())
    rows=[[e['name'],e['fires_when'],', '.join(e['props']),{'html':outbound(d,'https://github.com/karagemop466-tech/Affil1/blob/main/src/data/events.json','Event definition')}] for e in spec['events']]
    body=pagehead('Privacy & measurement','What gets counted?','Clicks are a signal of interest. Only an authorized Associates report can establish orders.')+section('<p>The self-hosted edition accepts the five events below at its own /api/e endpoint. The static GitHub Pages edition sends none: Pages cannot run the collector.</p>'+table(['Event','Trigger','Dimensions','Source'],rows)+'<p>Only daily totals are written. No IP, raw URL, query, referrer, user agent, cookie or visitor ID is stored by the counter. Entries older than 90 days are pruned on writes. Do Not Track and Global Privacy Control suppress collection. Saved picks and editorial decisions stay in your browser.</p><p>Do not mix preview or test activity with campaign reports. A permanent production collector and consent review remain open.</p>')
    return page(d,title='Privacy and measurement — Crisp &amp; Counter',description='Five first-party event definitions and their privacy limits.',body=body,canonical='review/measurement.html')
