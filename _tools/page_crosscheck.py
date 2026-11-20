"""The verification page: the site checked against itself, one page at a time.

Every other register on this site is organised by topic. A reviewer does not ask by
topic. They ask "this page says a thing — is it true?". That needs a row per page,
and it needs a verdict that is allowed to be unflattering.

The four verdicts are deliberately unequal. 'holds-with-caveat' exists because the
honest answer is usually not yes or no; it is 'yes, but narrower than the page
implies'. 'should-be-removed-or-reworded' exists so the page has somewhere to put a
finding it cannot fix, instead of softening it into a caveat.
"""

import json
import pathlib
import re

from layout import (breadcrumb_schema, esc, eyebrow, page, pagehead, rel, section,
                    table)

ROOT = pathlib.Path(__file__).resolve().parent.parent

VERDICT_PILL = {
    "holds": ("pill-ok", "Holds"),
    "holds-with-caveat": ("pill-warn", "Holds, with a caveat"),
    "unverifiable-here": ("pill-none", "Unverifiable here"),
    "should-be-removed-or-reworded": ("pill-block", "Needs rewording"),
}


BUY_DEST = re.compile(
    r"amazon\.[a-z.]+/(?:dp/|gp/product/|gp/aws/cart/add\.html)", re.I)


def _evidence_link(url, label="what was observed"):
    """A labelled citation that never pretends not to be what it is.

    An Amazon product URL in an evidence column is still an Amazon product URL.
    Marking it sponsored is the conservative choice and keeps it consistent with
    every other Amazon destination on the site; policy documents on other hosts
    stay nofollowed citations, because calling those paid would misdescribe them.
    """
    rels = "sponsored nofollow noopener" if BUY_DEST.search(url) else "nofollow noopener"
    if BUY_DEST.search(url):
        label = "listing observed"
    return (f'<a rel="{rels}" target="_blank" href="{esc(url)}">'
            f'{esc(label)} &nearr;</a>')


def load():
    return json.loads((ROOT / "_src/data/crosscheck.json").read_text(encoding="utf-8"))


def build(page_dir):
    d = page_dir
    doc = load()
    rows = doc["rows"]
    counts = {k: 0 for k in VERDICT_PILL}
    for r in rows:
        counts[r["verdict"]] += 1

    table_rows = []
    for r in rows:
        kind, label = VERDICT_PILL[r["verdict"]]
        src = (_evidence_link(r["source"]) if r.get("source")
               else '<span class="src-none">no document</span>')
        table_rows.append([
            {"html": f'<strong>{esc(r["page"])}</strong><br><span class="cc-sec">{esc(r["section"])}</span>'},
            {"html": esc(r["claim"])},
            {"html": esc(r["check"])},
            {"html": esc(r["checked"])},
            {"html": f'<span class="pill {kind}">{esc(label)}</span>'},
            {"html": src},
        ])
    main_table = table(
        ["Page", "Strongest claim", "How to check it", "Checked here", "Verdict", "Evidence"],
        table_rows, cls="cctable",
        caption=f"{len(rows)} sections checked, one row per surface",
        note="A row with no evidence link is not a claim without a source; it is a claim that rests on an "
             "observation this session made and recorded in the note below it.",
    )

    notes = "".join(
        f"""<article class="cc-note" id="cc-{esc(r['page'].replace('/', '-').replace('.', '-'))}">
  <p class="cc-note-head"><span class="cc-page">{esc(r['page'])}</span>
     <span class="cc-sec">{esc(r['section'])}</span>
     <span class="pill {VERDICT_PILL[r['verdict']][0]}">{esc(VERDICT_PILL[r['verdict']][1])}</span></p>
  <p>{esc(r['note'])}</p>
</article>"""
        for r in rows
    )

    findings = section(f"""
<div class="sec-head"><div>{eyebrow('What this session changed its mind about')}<h2>Three findings worth the scroll</h2></div>
<p>Each one was found by opening something, not by reasoning about it.</p></div>
<div class="finding-grid">
  <article class="finding">
    <p class="finding-k">Deploy scope</p>
    <h3>The site serves its own source code</h3>
    <p>Pages is set to publish the repository root, not the staged build. Opening
    <code>/tools/build.py</code> on the live host returns the build script. Opening
    <code>/archive/notes-edition/</code> returns a retired storefront with its own title and its own
    sponsored links. Five editions of one shop are live at five addresses.</p>
    <p class="finding-fix"><strong>Fix:</strong> one Pages setting. Logged as OFF-02, rank 2.</p>
  </article>
  <article class="finding">
    <p class="finding-k">Image rule</p>
    <h3>Half the pictures were photographs on a site that said they were drawings</h3>
    <p>My first pass found one photoreal image in the seasonal band and called it an outlier. Opening the
    rest showed the opposite: eight of the seventeen images in use were photographic renders, including
    the images on product pages P-02 and P-04, where a photograph beside a buy button reads as evidence
    of the product. The register called them all illustrations, and the disclaimer on each product page
    contradicted the picture above it.</p>
    <p class="finding-fix"><strong>Fix:</strong> all eight replaced with engravings this session; the rule
    now states one visual language. Logged as OFF-05, and corrected above rather than edited away.</p>
  </article>
  <article class="finding">
    <p class="finding-k">Conversion path</p>
    <h3>Every click cost the reader a second decision</h3>
    <p>All 133 tagged links in this repository pointed at a product-detail page. A reader who had
    already decided still had to land, scroll, and find Amazon's own button. The cart endpoint was
    opened to confirm it accepts the URL shape, and is now used on the front page.</p>
    <p class="finding-fix"><strong>Shipped:</strong> two cart doors now sit on the front page. Because no
    Special Link is approved, they carry no tag, so the click is a reference link until OFF-01 lands.</p>
  </article>
</div>""", cls="")

    body = (
        pagehead(
            "Verification",
            "What each page claims,<br><em>and whether it holds.</em>",
            f"{len(rows)} surfaces, one row each. For every page: the strongest thing it asserts, the click "
            "that would check it, whether this session made that click, and a verdict that is allowed to be "
            "unflattering.",
            meta=f"{counts['holds']} hold &middot; {counts['holds-with-caveat']} hold with a caveat &middot; "
                 f"{counts['should-be-removed-or-reworded']} need rewording &middot; "
                 f"{counts['unverifiable-here']} cannot be checked from here",
        )
        + section(f"""
<div class="stat-row">
  <div class="stat"><span class="stat-n">{len(rows)}</span><span class="stat-l">surfaces checked</span></div>
  <div class="stat"><span class="stat-n">{counts['holds']}</span><span class="stat-l">claims that hold as written</span></div>
  <div class="stat stat-warn"><span class="stat-n">{counts['holds-with-caveat']}</span><span class="stat-l">true only in a narrower form</span></div>
  <div class="stat stat-warn"><span class="stat-n">{counts['should-be-removed-or-reworded']}</span><span class="stat-l">should be reworded</span></div>
</div>
{main_table}""", cls="")
        + findings
        + section(f"""
<div class="sec-head"><div>{eyebrow('Row by row')}<h2>The detail behind each verdict</h2></div>
<p>Short, specific, and where possible naming the file or the URL to open.</p></div>
<div class="cc-notes">{notes}</div>""", cls="section-tint")
        + section(f"""
<div class="callout">
  <h2>What this page is not</h2>
  <p>It is not a guarantee that every sentence on the site is correct. It covers the strongest claim on each
  main surface, which is where an error does the most damage. A weaker sentence elsewhere can still be wrong,
  and finding it needs the same treatment: open the page, read the claim, open the source.</p>
  <p class="callout-links">
    <a class="tlink" href="{esc(rel(d, 'review/index.html'))}">The 22 pre-existing flags <span aria-hidden="true">&rarr;</span></a>
    <a class="tlink" href="{esc(rel(d, 'offers/index.html'))}">What to change, ranked <span aria-hidden="true">&rarr;</span></a>
  </p>
</div>""", cls="")
    )

    return page(
        d,
        title="What each page claims, and whether it holds | Crisp & Counter",
        description="A page-by-page audit: the strongest claim on each surface, the click that checks it, "
                    "whether it was made, and a verdict that is allowed to be unflattering.",
        body=body,
        active="verification/index.html",
        canonical="verification/",
        structured=breadcrumb_schema([], "Verification", "verification/"),
    )
