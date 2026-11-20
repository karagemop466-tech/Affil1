"""Design brief for the next design pass: the copy-ready prompt, the house-style
register and the article bank. Alternatives are not work orders; this page is the
feed a designer or writer receives before touching a page."""

import json
import pathlib

from layout import esc, outbound, page, pagehead, rel, section, table

ROOT = pathlib.Path(__file__).resolve().parent.parent

HELPFUL = ('Google Search Central: people-first content', 'https://developers.google.com/search/docs/fundamentals/creating-helpful-content')
SEARCH = ('Google Search Console: Performance report', 'https://support.google.com/webmasters/answer/7576553')
FTC = ('FTC Endorsement Guides FAQ', 'https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking')
PAGES = ('GitHub Pages usage limits', 'https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits')
AMAZON = ('Amazon Associates Program Policies', 'https://affiliate-program.amazon.com/help/operating/policies')

OPTIONS = (
    ('A · Buyer’s field guide (recommended)', 'Keep the three-format shortlist and fit finder. Add a single, reusable photo-and-measurement template.', 'Which step stops someone choosing? Observe whether readers can independently find the comparison and tell what is not verified. Verify dimensions against the exact model manual before showing a fit claim.', HELPFUL),
    ('B · Seasonal editorial', 'Lead with a timely question and use a small set of evergreen follow-ons about space, batching, and doneness.', 'Do related queries show impressions or clicks on the guides? Compare a fixed 28-day window for the same canonical pages and market. Do not call the first topics trending without a baseline.', SEARCH),
    ('C · Hands-on review series', 'Show real kitchen measurements and repeatable tests, with product photos that match the exact variant.', 'Who tested what, when, and how? Capture the method, raw observations, variant, and any material relationship before adding a review label.', FTC),
    ('D · Commerce and automation (hold)', 'Use a commercial-capable host and one product pilot. Draft from authorized evidence; don’t autopublish a winner, deal, or rate.', 'Can the enrolled account confirm intended ASIN, Special Link destination, and a tracking report? Can the host run a privacy-reviewed collector and does it permit commercial use? If not, keep the evidence-only edition.', AMAZON),
)


def _topics():
    with open(ROOT / '_src' / 'data' / 'topics.json', encoding='utf-8') as fh:
        return json.load(fh)


def build(d):
    bank = _topics()
    rows = [[name, change, evidence, {"html": outbound(d, source[1], esc(source[0]))}]
            for name, change, evidence, source in OPTIONS]

    style_rows = [[f"<strong>{esc(r['id'])}</strong>", esc(r['rule']), esc(r['basis'])]
                  for r in bank['style_rules']]
    style_table = table(['Ref', 'Rule', 'Basis'], [[{"html": a}, {"html": b}, {"html": c}]
                      for a, b, c in style_rows], caption='The register a page must pass before it ships')

    topic_rows = []
    for t in bank['topics']:
        mapped = esc(t['maps_to'])
        if t.get('internal_links'):
            links = " · ".join(f'<a href="{esc(rel(d, p))}">{esc(p.split("/")[-1].replace(".html", ""))}</a>'
                               for p in t['internal_links'])
            mapped += f'<br><span class="fine">{links}</span>'
        topic_rows.append([
            {"html": f"<strong>{esc(t['id'])}</strong>"},
            {"html": f"{esc(t['working_title'])}<br><span class=\"fine\">{esc(t['shape'])} &middot; {esc(t['funnel'])} funnel &middot; {esc(t['season'])}</span>"},
            {"html": esc(t['evidence_before_writing'])},
            {"html": mapped},
        ])
    topic_table = table(['Ref', 'Working title', 'Evidence required before writing', 'Maps to'],
                        topic_rows, cls='register', caption='14 working titles · 5 clusters · none is a popularity claim')

    done_list = "".join(f"<li>{esc(x)}</li>" for x in bank['traffic_plan']['already_done'])
    gated_list = "".join(f"<li>{esc(x)}</li>" for x in bank['traffic_plan']['missing_and_gated'])
    reading = " · ".join(outbound(d, r['url'], esc(r['name'])) for r in bank['traffic_plan']['official_reading'])

    body = pagehead('Suggestions / design brief', 'What should the next version do?',
                    'Four paths, the copy-ready prompt, the house-style register and the article bank — everything a designer or writer needs, and nothing they must guess.',
                    meta='Decision brief &middot; November 2026 &middot; working titles are hypotheses, not popularity claims')
    body += section(f'''
<h2>Pick one direction to test</h2>
{table(['Direction', 'What changes', 'Question and how to answer it', 'Official reference'], rows, caption='Options for the next design pass')}
<div class="callout"><h2>Copy-ready design prompt</h2>
<p>Design Crisp &amp; Counter as an independent kitchen buying publication, not a review farm and not a dashboard. Warm paper background, one dark-green accent, legible serif headlines with generous leading, and food photography or visibly labelled editorial illustrations — never stock filler. The front page leads with the products: a seasonal feature, a short-format shortlist, then the guides. Registers, ledgers and decision tools live one click deep, reachable from the footer.</p>
<p>On mobile, the first screen answers one useful choice: single basket, dual basket, or oven. Every product card carries a concrete cooking scenario (the 6pm frozen-chips panic, the six-person Sunday dinner), one honest trade-off, and one thing to check next — never a score, a rank, or a superlative. Make the comparison table readable by keyboard and at 360 px. Give every guide a consistent byline slot, a sources block and related reading.</p>
<p><strong>Anti-slop rules, non-negotiable:</strong> no first-person testing claims; no superlatives, award language or ranking claims; no prices, ratings or review counts; no hollow meta (“in this article”, “look no further”); no two sentences with the same rhythm in a row; every factual product claim carries a source or is left blank and flagged. The disclosure strip goes under the masthead on every page and again in the footer, carrying “As an Amazon Associate I earn from qualifying purchases.” verbatim. Do not show a tracked shopping CTA until the destination and attribution are verified. The ten numbered house-style rules below are the gate; this paragraph is their summary.</p></div>
''')
    body += section(f'''
<div class="sec-head"><div><p class="eyebrow"><i></i> THE GATE</p>
<h2>House-style register</h2></div>
<p>Ten rules, each with its basis. Three of them are Amazon or FTC rules the build already enforces; the rest are the difference between a publication and a generated feed.</p></div>
{style_table}
<p class="table-note">Approving this register is S-22 on the <a href="{esc(rel(d, 'suggestions/index.html'))}">suggestions board</a>. It constrains only future pages; nothing published changes retroactively.</p>''', cls='section-tint')
    body += section(f'''
<div class="sec-head"><div><p class="eyebrow"><i></i> THE QUEUE</p>
<h2>The article bank</h2></div>
<p>Catchy where honesty allows, question-shaped wherever a buyer has a question. Clustered so internal links are deliberate, seasonal where the calendar helps.</p></div>
{topic_table}
<div class="callout"><h2>What this bank is not</h2>
<p>None of these titles is a claim about search volume, popularity or trend data — no keyword tool was consulted. They are shaped like the questions buyers ask because that is the only defensible way to guess before measurement exists. The gate is S-23: Search Console (S-03) confirms which questions are real, then those topics get written. T-07 is on hold until a citable source exists; a guessed safety answer is the one thing this site cannot ship.</p></div>''')
    body += section(f'''
<div class="sec-head"><div><p class="eyebrow"><i></i> ORGANIC LOOP</p>
<h2>How traffic is earned here</h2></div>
<p>{esc(bank['traffic_plan']['principle'])}</p></div>
<div class="two-col">
  <div><h3>Already in place</h3><ul class="tight">{done_list}</ul></div>
  <div><h3>Missing, and gated behind a decision</h3><ul class="tight">{gated_list}</ul></div>
</div>
<p>Official reading: {reading}</p>
<h2>A cadence that can respond to results</h2>
<ol class="tight">
<li><strong>Weekly:</strong> Check indexing and query/page patterns in the verified Search Console property. Log the date range and missing data. The first themes are small kitchens, meal prep, holiday sides, and food thermometers, not proven search trends.</li>
<li><strong>Every other week:</strong> Publish one distinct question or improve an existing guide. Update an existing page rather than creating a near-duplicate. The build adds each accepted guide to the sitemap and RSS feed.</li>
<li><strong>Every 28 days:</strong> Review query and landing-page data against the previous comparable window. Keep on-site outbound counts separate from Associates orders. If the data are sparse, improve the guide or keep collecting; don’t estimate demand, commissions, or conversion.</li>
</ol>
<p><strong>Hosting gate:</strong> {outbound(d, PAGES[1], esc(PAGES[0]))} restricts using Pages for sites primarily intended to facilitate commercial transactions. Treat this Pages release as editorial and move the monetized operation to appropriate hosting if it becomes primarily commercial.</p>
<p><a href="{esc(rel(d, 'suggestions/index.html'))}">All suggestions</a> &middot;
<a href="{esc(rel(d, 'questions/index.html'))}">Open questions</a> &middot;
<a href="{esc(rel(d, 'review/measurement.html'))}">Measurement status</a></p>''')
    return page(d, title='Design decision brief — Crisp & Counter', description='The copy-ready design prompt, ten house-style rules and a fourteen-title article bank for the next affiliate publication design pass, with evidence and release gates.',
                body=body, active='suggestions/index.html', canonical='suggestions/design.html')
