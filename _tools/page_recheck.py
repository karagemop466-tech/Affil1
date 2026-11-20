"""The second read: every published product row opened again by another session.

The verification page asks whether each surface holds. This page answers the question
a reviewer asks next -- did a *second* session get the same answer, from the official
page, on a dated request? -- because a register verified only by the session that
wrote it is a single point of failure.

The misses are printed at the same size as the matches. Rows that did not reproduce
are described as what they are (an unstable route, a failed fetch), never as proof
that an earlier observation was wrong, and they change no stored value.

Values are copied from _src/data/recheck.json, written by the session that made the
requests. Nothing here is inferred, summarised from memory, or carried over from a
search result.
"""

import json
import pathlib
import re

from layout import (breadcrumb_schema, esc, eyebrow, page, pagehead, rel, section,
                    table)

ROOT = pathlib.Path(__file__).resolve().parent.parent

# An Amazon product URL in an evidence column is still an Amazon product URL: every
# one of them is marked sponsored, nofollow and noopener, exactly as the buy buttons
# are, because a checker reading the page cannot tell a citation from a destination.
# Documents on other hosts are never marked sponsored -- calling a federal page or a
# policy page a paid link would misdescribe it. Both halves are what _tools/check.py
# enforces, so this file enforces them the same way rather than inventing a third.
BUY_DEST = re.compile(r"amazon\.[a-z.]+/(?:dp/|gp/product/|gp/aws/cart/add\.html)", re.I)

VERDICT = {
    "matched": ("pill-ok", "Matched"),
    "reached the recorded listing": ("pill-ok", "Reached the listing"),
    "fell back to the marketplace home page": ("pill-block", "Fell to the home page"),
    "fetch failed, no observation": ("pill-none", "No observation"),
    "fixed on the page, flagged for review": ("pill-warn", "Found here, fixed here"),
}


def _source_cell(url, label=None):
    if BUY_DEST.search(url):
        rels, text = "sponsored nofollow noopener", label or "listing observed"
    else:
        rels = "nofollow noopener"
        text = label or url.split("//", 1)[-1].split("/", 1)[0].replace("www.", "")
    return (f'<a rel="{rels}" target="_blank" href="{esc(url)}">'
            f'{esc(text)} &nearr;</a>')


def _pill(verdict):
    kind, label = VERDICT.get(verdict, ("pill", verdict))
    return f'<span class="pill {kind}">{esc(label)}</span>'


def load():
    return json.loads((ROOT / "_src/data/recheck.json").read_text(encoding="utf-8"))


def build(page_dir):
    d = page_dir
    doc = load()
    meta = doc["meta"]
    listings, links = doc["listings"], doc["short_links"]
    matched = sum(1 for r in listings if r["verdict"] == "matched")
    reached = sum(1 for r in links if r["verdict"] == "reached the recorded listing")
    missed = len(links) - reached

    lrows = [[
        {"html": f'<strong>{esc(r["ref"])}</strong>'},
        {"html": f'<code class="code">{esc(r["published_value"].split(" · ")[0])}</code>'},
        {"html": esc(r["field"])},
        {"html": esc(r["this_session_saw"])},
        {"html": _pill(r["verdict"]) + f'<br><span class="tiny">{esc(r["checked_at_utc"])}</span>'},
        {"html": esc(r["note"])},
        {"html": _source_cell(r["official_source"])},
    ] for r in listings]

    krows = [[
        {"html": f'<strong>{esc(r["ref"])}</strong>'},
        {"html": f'<code class="code">{esc(r["submitted_link"])}</code><br>'
                 f'<span class="tiny">slug is {r["slug_length"]} characters; an ASIN is 10</span>'},
        {"html": f'<code class="code">{esc(r.get("reached") or "nothing — the request failed")}</code>'},
        {"html": esc(r.get("document_title") or "no page title was reached")},
        {"html": _pill(r["verdict"]) + f'<br><span class="tiny">{esc(r["checked_at_utc"])}</span>'},
        {"html": esc(r["note"])},
        {"html": _source_cell(r["source"])},
    ] for r in links]

    grows = [[
        {"html": f'<strong>{esc(g["id"])}</strong>'},
        {"html": esc(g["gap"])},
        {"html": esc(g["why_it_blocks"])},
        {"html": esc(g["how_to_discover"])},
        {"html": esc(g["who_can_answer"])},
        {"html": _source_cell(g["source"], "the document that sets the requirement")},
    ] for g in doc["gaps"]]

    body = f"""{pagehead(
        'Verification / second read',
        'Every published row,<br>opened again by someone else.',
        f'{len(listings)} product rows and {len(links)} submitted links were re-read on 20 November 2026 by a second '
        f'session, against the official page rather than against the register. {matched} of {len(listings)} rows '
        f'matched in full. {missed} of {len(links)} submitted links did not reach a product page from here, and that '
        f'is printed at the same size as the {reached} that did.',
        meta=f'{esc(meta["title"])} &middot; window {esc(meta["window_utc"])} UTC &middot; session '
             f'{esc(meta["session"])}',
    )}
{section(f'''
<div class="stat-row">
  <div class="stat"><span class="stat-n">{len(listings)}</span><span class="stat-l">product rows re-read</span></div>
  <div class="stat"><span class="stat-n">{matched}</span><span class="stat-l">matched title and category</span></div>
  <div class="stat stat-warn"><span class="stat-n">{missed}</span><span class="stat-l">submitted links that did not reach a product</span></div>
  <div class="stat stat-warn"><span class="stat-n">{len(doc["gaps"])}</span><span class="stat-l">gaps with a discovery step attached</span></div>
</div>
<div class="callout">
  <h2>Method, in one paragraph</h2>
  <p>{esc(meta["method"])}</p>
  <p class="tiny">{esc(meta["rule"])}</p>
</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The five rows')}<h2>What the official pages still say</h2></div>
<p>A row reads 'matched' only when the string this site publishes is the string the official page served on the
day. Price, rating and stock are absent from this table because this site is not permitted to hold them.</p></div>
{table(['Row', 'ASIN published here', 'Fields compared', 'What the second read saw', 'Verdict', 'What it means', 'Source'],
       lrows, cls='register',
       caption=f'{len(listings)} product rows re-read independently · {matched} matched in full')
}''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The part that did not reproduce')}<h2>The submitted links, re-followed</h2></div>
<p>{esc(doc["reading"]["headline"])}</p></div>
{table(['Row', 'Link as submitted', 'Where this session actually landed', 'Title served', 'Verdict', 'What it does and does not mean', 'Source'],
       krows, cls='register',
       caption=f'{len(links)} submitted links re-followed · {reached} reached the recorded listing')}
<div class="callout">
  <h2>How to read that, without over-reading it</h2>
  <p>{esc(doc["reading"]["body"])}</p>
  <p><strong>{esc(doc["reading"]["what_would_change_this"])}</strong></p>
  <p class="tiny">{esc(meta["what_this_page_is_not"])}</p>
</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Before any further decision')}<h2>What is still missing, and how to go and find it out</h2></div>
<p>{esc(meta["counting"])}</p></div>
{table(['Ref', 'What is missing', 'What it holds up', 'The one thing that settles it', 'Who can answer', 'Source'],
       grows, cls='register',
       caption=f'{len(doc["gaps"])} gaps, each with a discovery step rather than a guess')}
<p class="table-note">Nothing in this table is answered by inference. Where the answer lives in an account, a
dashboard or a decision this repository cannot reach, the field stays blank on the site, the gap stays open here,
and the row names who can close it. The raw observations behind the two tables above are appended, session by
session, to <code class="code">_data/verification-observations.ndjson</code> and are not published as source
code on this host.</p>
<p class="sec-foot">
  <a class="tlink" href="{esc(rel(d, 'verification/index.html'))}">The page-by-page audit <span aria-hidden="true">&rarr;</span></a> &middot;
  <a class="tlink" href="{esc(rel(d, 'review/index.html'))}">Everything flagged for review <span aria-hidden="true">&rarr;</span></a> &middot;
  <a class="tlink" href="{esc(rel(d, 'questions/index.html'))}">The decision register <span aria-hidden="true">&rarr;</span></a> &middot;
  <a class="tlink" href="{esc(rel(d, 'suggestions/index.html'))}">Paths and proposals <span aria-hidden="true">&rarr;</span></a>
</p>''', cls='section-tint')}"""
    return page(
        d,
        title="Second read: every product row, opened again | Crisp & Counter",
        description=(f"A second session re-opened every product row this shop publishes on 20 November 2026. "
                     f"{matched} of {len(listings)} matched title and category; the submitted links that did not "
                     f"reproduce are listed with the ones that did, with a dated source per row."),
        body=body,
        active="verification/index.html",
        canonical="verification/recheck.html",
        structured=breadcrumb_schema([("verification/index.html", "Verification")],
                                     "Second read", "verification/recheck.html"),
    )
