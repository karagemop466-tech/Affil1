"""The line-by-line audit: one row per claim the site makes about itself.

This page exists because the brief asked for every entry and finding in a table
with a source link, and for anything that could not be confirmed from an
official source to be left blank and flagged rather than filled in. A row here
is a claim, the check that produced it, and either the document it rests on or
the word "unverified".

The register lives in src/data/audit.json. tools/check_audit.py fails if a row
in that file is missing from this page, so the table cannot drift from the data.
"""

import re

from layout import (breadcrumb_schema, esc, eyebrow, outbound, page, pagehead,
                    rel, section, table)

PILL = {
    "pass": ("pill-ok", "Pass"),
    "fixed": ("pill-warn", "Fixed this pass"),
    "unverified": ("pill-block", "Unverified"),
    "open": ("pill", "Open"),
}


def source_cell(d, r):
    """An official URL where one exists; otherwise the repository check itself.

    A row like "the build is reproducible" has no external document to cite.
    Its source is the script a reader can run, and the cell says so instead of
    pretending a policy page covers it.
    """
    src = (r.get("source") or "").strip()
    if src.startswith("repo:"):
        path = src[len("repo:"):]
        return (f'<code class="code">{esc(path)}</code><br>'
                '<span class="tiny">repository check, not an external document</span>')
    if src.startswith("http"):
        # A listing citation is still a link to an Amazon Site, so Program
        # Policies 2(b) applies to it exactly as it does to a buy button: tagged,
        # sponsored, nofollow. It is evidence, not a recommendation, and it is
        # labelled as the ASIN rather than as a call to action.
        m = re.search(r"amazon\.com/dp/([A-Z0-9]{10})", src)
        if m:
            from layout import buy_url, product_link
            return product_link(d, buy_url(m.group(1)),
                                f'<code class="code">{esc(m.group(1))}</code>',
                                aria=f"Open Amazon listing {m.group(1)} to check this row (paid link, opens in a new tab)")
        return outbound(d, src, r.get("source_id") or src.split("//")[-1].split("/")[0])
    return '<span class="blank" title="no official document covers this row">unverified</span>'


def build(page_dir, audit, meta):
    d = page_dir
    rows = audit["rows"]
    legend = audit["meta"]["legend"]
    counts = {k: sum(1 for r in rows if r["result"] == k) for k in PILL}
    order = ["pass", "fixed", "unverified", "open"]

    table_rows = []
    for r in rows:
        cls, label = PILL[r["result"]]
        src = source_cell(d, r)
        table_rows.append([
            {"html": f'<strong id="{esc(r["id"])}">{esc(r["id"])}</strong><br><span class="tiny">{esc(r["area"])}</span>'},
            {"html": esc(r["claim"])},
            {"html": f'<span class="pill {cls}">{esc(label)}</span>'},
            {"html": esc(r["evidence"])},
            {"html": f'<code class="code">{esc(r["verify"])}</code>'},
            {"html": src},
        ])

    tbl = table(
        ["Ref", "The claim", "Result", "What the check found", "Re-run it", "Source"],
        table_rows,
        cls="register audit",
        caption=f"{len(rows)} claims audited on {audit['meta']['audited_on']}",
        note="A blank source is not an omission: where no official document settles a row, the cell says unverified and the value is left out of the site rather than guessed.",
    )

    legend_html = "".join(
        f'<div class="stat{" stat-warn" if k in ("fixed", "unverified") else ""}">'
        f'<span class="stat-n">{counts[k]}</span>'
        f'<span class="stat-l">{esc(v)} &mdash; {esc(legend[k].split(".")[0].lower())}</span></div>'
        for k, v in [(k, PILL[k][1]) for k in order]
    )

    body = f"""{pagehead(
        'Audit',
        'Every claim,<br>and the check behind it',
        f'This site makes {len(rows)} claims about itself: that its disclosure sits above the fold, that every Amazon link is marked, that no price is invented, that the build is reproducible. Each one is a row below, with the command that reproduces it and the official document it rests on. Where nothing official settles a row, the row says so and the site publishes nothing on that subject.',
        meta=f'Audited {audit["meta"]["audited_on"]} &middot; {counts["pass"]} pass &middot; {counts["fixed"]} fixed in this pass &middot; {counts["unverified"]} unverified &middot; {counts["open"]} open',
    )}
{section(f'''<div class="stat-row">{legend_html}</div>
<p class="lede-prose">{esc(audit["meta"]["method"])}</p>
<p class="lede-prose">The rule: {esc(audit["meta"]["rule"])}</p>''', cls='')}
{section(tbl, cls='')}
{section(f'''<div class="crosslinks">
  <a class="crosslink" href="{esc(rel(d, 'review/index.html'))}"><h3>Flagged for review</h3><p>The same findings, organised by severity, with what a reviewer should check.</p></a>
  <a class="crosslink" href="{esc(rel(d, 'questions/index.html'))}"><h3>Open questions</h3><p>What remains unknown and the specific document that would close each one.</p></a>
  <a class="crosslink" href="{esc(rel(d, 'about/index.html#sources'))}"><h3>Source register</h3><p>Every official document this site quotes, with the wording it quotes.</p></a>
</div>''', cls='section-tint')}"""

    return page(
        d,
        title="Audit: every claim and the check behind it | Crisp & Counter",
        description=f"{len(rows)} claims this site makes about itself, each with the command that reproduces it and the official document it rests on, and {counts['unverified']} rows that stay blank because nothing official settles them.",
        body=body,
        active="review/index.html",
        canonical="review/audit.html",
        structured=breadcrumb_schema([("review/index.html", "Flagged for review")], "Audit", "review/audit.html"),
    )
