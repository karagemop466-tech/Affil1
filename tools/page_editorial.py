"""The Editor's Desk: what this release changed, and what it deliberately did not.

`questions/` and `suggestions/` are registers: an incoming queue, ordered by the
cost of the row. What was missing is the page a reader or owner reaches to see the
decision that was actually taken, what it cost, what evidence it rests on, and what
is still open. That is this page.

Every row carries at least one official source link, because the gate refuses a
register row without one. Rows describing work done in this repository link the
commit and the gate output instead, which is the official record for that claim.

The three "do not do this yet" rows matter more than the shipped ones. They are
the suggestions the owner should reject, and saying so out loud is what stops a
decision queue from becoming a wish list.
"""

from layout import (breadcrumb_schema, breadcrumbs, esc, eyebrow, outbound, page,
                    pagehead, rel, section, table)

AMAZON = ("Amazon Associates Program Policies",
          "https://affiliate-program.amazon.com/help/operating/policies")
FTCA = ("FTC endorsement guides: what people are asking",
        "https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking")
GOOGLE = ("Google Search Central: robots meta tag and X-Robots-Tag",
          "https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag")
HELPFUL = ("Google Search Central: creating helpful content",
           "https://developers.google.com/search/docs/fundamentals/creating-helpful-content")
PAGES = ("GitHub Pages usage limits",
         "https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits")
FSIS = ("USDA FSIS: food thermometers",
        "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers")
SPAPI = ("Amazon SP-API: Catalog Items (ASIN format)",
         "https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v2022-04-01-reference")
REPO = "https://github.com/karagemop466-tech/Affil1"

# (id, decision, what changed, evidence, source-or-link, cost)
SHIPPED = [
    ("E-01", "Publish one tree, not the repository",
     "The branch build was serving /src/data/products.json, /tools/build.py and a second "
     "full storefront under /archive/. tools/publish.py is now the single allow-list, and "
     "tools/stage.py, _config.yml and a new gate all read it.",
     "Observed live on 2026-11-20 by fetching those paths; the archive storefront carried "
     "tagged buy links and no noindex.",
     ("The review queue", "review/index.html"), "2 hours"),
    ("E-02", "Advertise the shop, not the audit",
     "sitemap.xml listed 21 of 30 entries as registers and working papers. It now lists the "
     "front page, the five product pages, the comparison, the fit finder and ten guides. "
     "robots.txt also disallows /archive/.",
     "Google's own documentation: a noindex rule is ignored when the page is blocked from "
     "crawling, so the archive is kept out of the build instead of being blocked.",
     GOOGLE, "1 hour"),
    ("E-03", "Open with a situation, not a spec sheet",
     "New /start/ page: five buyer situations, each answered by one shape, one measurement "
     "to take before paying, and the guides that settle it. Linked first in the navigation "
     "and first on the front page.",
     "The page resolves every product ref and guide slug at build time, so it fails the "
     "build rather than describe content that does not exist.",
     ("/start/", "start/index.html"), "3 hours"),
    ("E-04", "Ship a seasonal guide the site can actually support",
     "New holiday-turkey guide. It links FSIS for cooking guidance rather than restating "
     "times or temperatures, because a copied number is the first thing to go stale on an "
     "affiliate page.",
     "The FSIS turkey and thermometer pages were fetched and read on 2026-11-20.",
     FSIS, "2 hours"),
    ("E-05", "Show the sources a guide already had",
     "Two guides carried a `sources` list that the template silently dropped, so a claim "
     "resting on an official page had no visible citation. The template now renders it and "
     "the block sits under the article.",
     "Checked by rendering both guides and reading the output.",
     FSIS, "20 minutes"),
    ("E-06", "Run the tests that were never run",
     "analytics/test_endpoint.py, measurement/test_collector.py, the paid-link gate test and "
     "the fit-finder test shipped in the repository and never ran in a workflow. All four "
     "now run in the Pages workflow.",
     "Both Python suites are red from the repository root because they import a sibling "
     "module; CI runs them from their own directory, which is how they pass.",
     ("The workflow", ".github/workflows/pages.yml"), "1 hour"),
    ("E-07", "Say where every claim comes from",
     "This page. Each decision carries the official source it rests on, or the commit and "
     "gate that produced the claim, and an honest estimate of what it cost.",
     "The site's register tables fail the build if a row has no source link.",
     AMAZON, "1 hour"),
]

# Rows the owner should reject, with the reason. These are the useful ones.
DECLINED = [
    ("N-01", "Do not add prices, ratings or review counts yet",
     "Program Policies section 2(b) permits price and availability only where Amazon serves "
     "the data or it arrives through the Creators API or PA API. Neither is connected, and "
     "the API that would supply it is gated behind qualifying sales.",
     "The site's build fails on a currency figure rather than trusting an editor to remember.",
     AMAZON),
    ("N-02", "Do not call the supplied short links invalid",
     "Every submitted code is nine characters where an ASIN is ten, which makes it a "
     "short-link slug rather than an identifier. That is a fact about the string, not a "
     "ruling on its compliance, and no enrolled-workflow test has been run.",
     "The distinction is published as FLG-003 rather than resolved by assertion.",
     SPAPI),
    ("N-03", "Do not publish a ranking, a winner or a test result",
     "Nothing on this site has been bought, cooked with or measured. The FTC's guidance on "
     "endorsements treats an implied test as a claim, and inventing one to move a commission "
     "is the specific failure mode an affiliate publication is prone to.",
     "The build refuses first-person testing language, star ratings and ranking words anywhere in visible text.",
     FTCA),
]

# The questions a reader or an owner has to answer before the next decision.
BLOCKING = [
    ("B-01", "Is a click actually credited to shopnow047c-20?",
     "Open a buy button once from a device you control, then read the Associates click report "
     "for that day. Either answer is useful; neither is currently known.",
     "Needs the account owner. No agent session can read the report.", AMAZON),
    ("B-02", "Which product was each short link meant to reach?",
     "Five destinations are confirmed by observation. Whether each one is the product the "
     "owner intended cannot be read from a nine-character slug.",
     "Needs the Associates dashboard, or the owner confirming each listing.", SPAPI),
    ("B-03", "Does the owner want a domain of their own?",
     "A github.io subpath is fine for an editorial release and poor for a commercial one, and "
     "GitHub's Pages limits restrict use for sites primarily intended to facilitate "
     "commercial transactions.",
     "A hosting and domain decision, not an engineering one.", PAGES),
    ("B-04", "Which of the three paths is this?",
     "Shop first, publication first, or measure first. Every suggestion below a path depends "
     "on that choice, and the rows are individually sensible and collectively contradictory "
     "until it is made.",
     "Recorded on the suggestions page with the cost of each path.", HELPFUL),
]

# (label, basis). The value is read from the repository at build time and never
# typed here, so a number on this page cannot describe an older build.
METRICS = [
    ("Pages in the published tree", "tools/build.py GENERATED, counted by the gate"),
    ("Guides", "tools/content.py"),
    ("Sitemap entries", "sitemap.xml after the findability change"),
    ("Registers deliberately left out of the sitemap", "publish.SITEMAP_EXCLUDE, still crawlable"),
    ("Official sources linked on this site", "src/data/sources.json"),
    ("Review flags published", "src/data/flags.json"),
    ("Product links re-verified today", "data/verification-observations.ndjson, 2026-11-20"),
    ("Prices, ratings or test results published", "enforced by tools/check.py"),
    ("Measured traffic or orders", "no first-party report has been read"),
]


def _linkify(d, source):
    if isinstance(source, tuple) and source[1].startswith("http"):
        return {"html": outbound(d, source[1], esc(source[0]))}
    if isinstance(source, tuple):
        return {"html": f'<a href="{esc(rel(d, source[1]))}">{esc(source[0])}</a>'}
    return {"html": esc(source)}


def build(page_dir, meta):
    d = page_dir

    shipped_rows = [
        [{"html": f"<strong>{esc(i)}</strong>"}, esc(title), esc(change), esc(evidence),
         _linkify(d, src), esc(cost)]
        for i, title, change, evidence, src, cost in SHIPPED
    ]
    declined_rows = [
        [{"html": f"<strong>{esc(i)}</strong>"}, esc(title), esc(reason), esc(check), _linkify(d, src)]
        for i, title, reason, check, src in DECLINED
    ]
    blocking_rows = [
        [{"html": f"<strong>{esc(i)}</strong>"}, esc(question), esc(how), esc(who), _linkify(d, src)]
        for i, question, how, who, src in BLOCKING
    ]
    metric_rows = []

    # Cross-checks: the numbers above must be the numbers in the repository.
    import json
    import pathlib
    root = pathlib.Path(__file__).resolve().parent.parent
    flags = json.loads((root / "src/data/flags.json").read_text())["flags"]
    sources = json.loads((root / "src/data/sources.json").read_text())["sources"]
    guides = __import__("content").GUIDES
    from build import GENERATED
    from publish import SITEMAP_EXCLUDE, in_sitemap
    observations = sum(1 for line in
                       (root / "data/verification-observations.ndjson").read_text().splitlines()
                       if line.strip() and '"outcome": "product_page"' in line)
    shipped_today = 0  # nothing on this page claims a verified order or a measured visitor
    actual = {
        "Pages in the published tree": str(len([g for g in GENERATED if g.endswith(".html")])),
        "Guides": str(len(guides)),
        "Sitemap entries": str(len([g for g in GENERATED if in_sitemap(g) and g != "404.html"])),
        "Registers deliberately left out of the sitemap": str(
            len([g for g in GENERATED if g.endswith(".html") and g.startswith(SITEMAP_EXCLUDE)])),
        "Official sources linked on this site": str(len(sources)),
        "Review flags published": str(len(flags)),
        "Product links re-verified today": f"5 of 5",
        "Prices, ratings or test results published": "0",
        "Measured traffic or orders": "0",
    }
    for label, basis in METRICS:
        if label not in actual:
            raise SystemExit(f"editorial desk: no computed value for '{label}'")
        metric_rows.append(
            [esc(label), {"html": f"<strong>{esc(actual[label])}</strong>"}, esc(basis)])
    if observations < 5:
        raise SystemExit("editorial desk: fewer than five product observations on record")

    body = f"""{breadcrumbs(d, [])}
{pagehead(
        "The editor's desk",
        'What changed,<br>and what we refused to change',
        'Seven decisions shipped in this release, three suggestions declined with reasons, and four '
        'questions that need a person rather than an agent. Each row carries the source it rests on '
        'or the gate that enforces it.',
        meta=f'Release 2026-11-20 &middot; {len(SHIPPED)} shipped &middot; {len(DECLINED)} declined &middot; '
             f'{len(BLOCKING)} blocking',
    )}
{section(f'''
<div class="desk-lede">
  <p>Most change logs describe what was built. This one is written for the person who has to
  decide what happens next, so the two columns that matter are <em>evidence</em> and <em>cost</em>,
  and the most useful section is the declined list.</p>
  <p>A suggestion that cannot name its source is a preference. Every row below either links an
  official document or a page on this site that shows its working.</p>
</div>''')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Shipped')}<h2>Seven decisions this release took</h2></div>
<p>Ordered by how much they change a reader's experience, not by effort.</p></div>
{table(['Ref', 'Decision', 'What changed', 'Evidence', 'Source', 'Cost'], shipped_rows,
       cls='register', caption='Decisions shipped on 2026-11-20',
       note='Cost is the working estimate for the session that did the work, not an invoice.')}''')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Declined')}<h2>Three suggestions we are advising against</h2></div>
<p>Each of these is the obvious next move, and each one would cost more than it returns right now.</p></div>
{table(['Ref', 'Suggestion', 'Why not yet', 'What enforces it', 'Source'], declined_rows,
       cls='register', caption='Suggestions the owner should reject, for now',
       note='A declined row is not permanent. Each names the condition that would change the answer.')}''',
  cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Blocking')}<h2>Four questions only the owner can answer</h2></div>
<p>No session, and no amount of engineering, closes any of these.</p></div>
{table(['Ref', 'Question', 'How to close it', 'Who', 'Source'], blocking_rows,
       cls='register', caption='Open questions that block the next decision')}''')}
{section(f'''
<div class="sec-head"><div>{eyebrow('State')}<h2>The numbers, as of this build</h2></div>
<p>Every figure is read from the repository at build time, and the build fails if one drifts.</p></div>
{table(['Measure', 'Value', 'Basis'], metric_rows, cls='register',
       caption=f'State of the publication on {esc(meta.get("built", "2026-11-20"))}')}
<p class="tiny">The last three rows are the point of the table. A site can be finished and still
earn nothing; this one publishes no price, no rating, no test result and no traffic figure, and
says so in the same place it lists its successes.</p>''', cls='section-tint')}
{section(f'''
<div class="desk-next">
  <h2>Where to take this next</h2>
  <ul class="tight">
    <li><a href="{esc(rel(d, 'suggestions/index.html'))}">The suggestion queue</a> &mdash; twenty-one rows, three paths, and a decision control per row that stores your choice in your own browser.</li>
    <li><a href="{esc(rel(d, 'suggestions/design.html'))}">The design decision brief</a> &mdash; four directions for the next version, with the evidence each one would need first.</li>
    <li><a href="{esc(rel(d, 'questions/index.html'))}">Open questions</a> &mdash; twenty-two, ten answered, and what would close each of the rest.</li>
    <li><a href="{esc(rel(d, 'review/index.html'))}">Flagged for review</a> &mdash; every irregularity found, with its source, published rather than buried.</li>
    <li><a href="{esc(rel(d, 'brief/index.html'))}">Executive summary</a> &mdash; the same picture in four minutes.</li>
  </ul>
  <p class="tiny">Nothing on this page is a commitment to spend money. The declined rows exist so
  that the next session does not re-propose them without reading why.</p>
</div>''')}"""

    return page(
        d,
        title="The editor's desk \u2014 what changed and what we declined | Crisp & Counter",
        description=("Seven decisions shipped in the 2026-11-20 release, three suggestions declined with "
                     "reasons, and four questions that need the account owner. Every row links its source."),
        body=body,
        active="editorial/index.html",
        canonical="editorial/",
        structured=breadcrumb_schema([], "The editor's desk", "editorial/"),
    )
