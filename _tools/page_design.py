"""Design brief for the next design pass: the copy-ready prompt, the design-token
pack, the house-style register and the topic bank. Alternatives are not work
orders; this page is the feed a designer or writer receives before touching a
page. Two sessions' banks share one id space: T-01..T-16 are the brief's
hypotheses (earlier design pack), T-17..T-30 are the session additions.
Nothing here is a claim about popularity, search volume or product superiority."""

import json
import pathlib

from layout import esc, outbound, page, pagehead, rel, section, table

ROOT = pathlib.Path(__file__).resolve().parent.parent

HELPFUL = ('Google Search Central: people-first content', 'https://developers.google.com/search/docs/fundamentals/creating-helpful-content')
SITENAMES = ('Google Search Central: site names', 'https://developers.google.com/search/docs/appearance/site-names')
SEARCH = ('Google Search Console: Performance report', 'https://support.google.com/webmasters/answer/7576553')
FTC = ('FTC Endorsement Guides FAQ', 'https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking')
PAGES = ('GitHub Pages usage limits', 'https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits')
AMAZON = ('Amazon Associates Program Policies', 'https://affiliate-program.amazon.com/help/operating/policies')

OPTIONS = (
    ('A · Buyer’s field guide (recommended)', 'Keep the three-format shortlist and fit finder. Add a single, reusable photo-and-measurement template.', 'Which step stops someone choosing? Observe whether readers can independently find the comparison and tell what is not verified. Verify dimensions against the exact model manual before showing a fit claim.', HELPFUL),
    ('B · Seasonal editorial', 'Lead with a timely question and use a small set of evergreen follow-ons about space, batching, and doneness.', 'Do related queries show impressions or clicks on the guides? Compare a fixed 28-day window for the same canonical pages and market. Do not call the first topics trending without a baseline.', SEARCH),
    ('C · Hands-on review series', 'Show real kitchen measurements and repeatable tests, with product photos that match the exact variant.', 'Who tested what, when, and how? Capture the method, raw observations, variant, and any material relationship before adding a review label.', FTC),
    ('D · Commerce and automation (hold)', 'Use a commercial-capable host and one product pilot. Draft from authorized evidence; don’t autopublish a winner, deal, or rate.', 'Can the enrolled account confirm intended ASIN, Special Link destination, and a tracking report? Can the host run a privacy-reviewed collector and does it permit commercial use? If not, keep the evidence-only edition.', AMAZON),
)

# Design-token pack (session arena/76128338-affil1 lineage). These are proposals
# for the design prompt, not verified facts, so the Basis column cites official
# guidance where one exists and says "design decision" where none does.
TOKENS = (
    ('Typography', 'Serif display headlines (Fraunces), a plain sans body, a tight type scale, and one voice for cards and guides.', 'design decision'),
    ('Colour', 'Warm paper background, a dark green accent, one warm highlight for the buy action; no more than three colours in view.', 'design decision'),
    ('Layout', 'One useful choice first on mobile (single basket, dual basket, or oven), then detail; a persistent shortlist rail on desktop.', 'design decision'),
    ('Imagery', 'Food photography or visibly labelled illustrations only. No invented test result, star rating, sale or ranking.', FTC),
    ('Disclosure', 'The Associates statement under the masthead on every page and repeated in the footer; never behind a link or a hover.', FTC),
    ('Accessibility', 'Keyboard-reachable cards and tables, real alt text, sufficient contrast, and no motion that cannot be reduced.', 'design decision'),
)

# The brief's hypothesis bank (T-01..T-16), operationalized. Each row names the
# evidence required before it is written; none is a claim that the topic is
# popular or that any product is best.
TOPICS = (
    ('T-01', 'Basket or oven-style air fryer: what should you compare?', 'Air fryers', 'A recorded comparison of the two formats on the dimensions that change a weeknight; not a winner.', 'design decision'),
    ('T-02', 'A no-hype checklist for comparing air-fryer capacity', 'Air fryers', 'A worked conversion from quart volume to a cooking surface, checked against a published model manual.', 'design decision'),
    ('T-03', 'How to assess cleanup and counter-space trade-offs', 'Air fryers', 'A parts-and-footprint table for the exact models on the shelf; no invented measurements.', 'design decision'),
    ('T-04', 'Two baskets or one: is dual-zone worth the counter space?', 'Air fryers', 'A side-by-side of basket area and folded footprint; a recommendation only if the arithmetic supports it.', 'design decision'),
    ('T-05', 'Questions to ask before buying a multi-function kitchen appliance', 'Air fryers', 'A checklist grounded in what a listing can and cannot tell you; the limits stated, not hidden.', HELPFUL),
    ('T-06', 'Holiday hosting with an air fryer: what actually scales', 'Air fryers', 'A timing plan for a known number of servings, tied to a specific model’s stated capacity.', 'design decision'),
    ('T-07', 'Which thermometer for an air fryer?', 'Thermometers', 'A pairing guide from the USDA FSIS safe-temperature chart to the two probe styles on the shelf.', FTC),
    ('T-08', 'Instant-read or leave-in: how to choose a meat thermometer', 'Thermometers', 'A use-case split (thin cuts vs. roasts) with the official safe-temperature basis for each.', 'design decision'),
    ('T-09', 'Why your air fryer needs a probe, and which one', 'Both', 'The doneness gap a probe closes, with the official temperature basis and no invented test result.', FTC),
    ('T-10', 'Small-kitchen air fryer: the space audit before you buy', 'Air fryers', 'A measure-your-counter worksheet tied to the folded dimensions of the models listed.', 'design decision'),
    ('T-11', 'Air fryer for two: what size actually fits a two-person dinner?', 'Air fryers', 'A worked conversion from quart volume to a cooking surface for a two-person batch, checked against a published model manual.', 'design decision'),
    ('T-12', 'Air fryer or toaster oven: which one earns the counter space?', 'Air fryers', 'A format-level footprint and clearance comparison; no model claims beyond the listing titles on the shelf.', 'design decision'),
    ('T-13', 'Cooking from frozen in an air fryer: what to check before you trust the packet', 'Both', 'A pre-flight checklist with the official USDA FSIS temperature basis for doneness; no invented test result.', FTC),
    ('T-14', 'Meal prep with an air fryer: one cook, four lunches', 'Air fryers', 'A batch plan tied to the stated basket sizes on the shelf, with the arithmetic shown.', 'design decision'),
    ('T-15', 'Replacing a microwave: what an air fryer can and cannot do', 'Air fryers', 'A capability comparison at format level, from stated features only; the limits stated, not hidden.', HELPFUL),
    ('T-16', 'Air fryer noise, smell and smoke: what a listing never tells you', 'Air fryers', 'Observations from a named, dated first-person log — or nothing. Do not commission without hands-on evidence.', FTC),
)

# Rows whose guide already ships are marked published, by title match against
# the build's own guide list — one definition of "written", not a second copy.
try:
    from content import GUIDES as _GUIDES  # noqa: E402
    _PUBLISHED = {g["title"]: g["slug"] for g in _GUIDES}
except Exception:  # pragma: no cover - the bank still renders without the build
    _PUBLISHED = {}


def _state(topic):
    slug = _PUBLISHED.get(topic)
    if not slug:
        return {'html': '<span class="blank">Suggestion &mdash; awaiting evidence</span>'}
    return {'html': f'Published &middot; <a href="../guides/{esc(slug)}.html">{esc(slug)}</a>'}


def _basis(d, basis):
    """Render a Basis cell: an official link where one exists, else a flag."""
    if isinstance(basis, tuple):
        return {"html": outbound(d, basis[1], esc(basis[0]))}
    return {"html": f'<span class="blank" title="No official source; a design proposal, not a verified fact">{esc(basis)}</span>'}


def _topics():
    with open(ROOT / '_src' / 'data' / 'topics.json', encoding='utf-8') as fh:
        return json.load(fh)


def build(d):
    bank = _topics()
    rows = [[name, change, evidence, {"html": outbound(d, source[1], esc(source[0]))}]
            for name, change, evidence, source in OPTIONS]

    token_rows = [[name, meaning, _basis(d, basis)] for name, meaning, basis in TOKENS]

    style_rows = [[f"<strong>{esc(r['id'])}</strong>", esc(r['rule']), esc(r['basis'])]
                  for r in bank['style_rules']]
    style_table = table(['Ref', 'Rule', 'Basis'], [[{"html": a}, {"html": b}, {"html": c}]
                      for a, b, c in style_rows], caption='The register a page must pass before it ships')

    brief_rows = [[tid, topic, cluster, _state(topic), before, _basis(d, basis)]
                  for tid, topic, cluster, before, basis in TOPICS]

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
                        topic_rows, cls='register', caption='T-17 to T-30 · session additions · none is a popularity claim')

    done_list = "".join(f"<li>{esc(x)}</li>" for x in bank['traffic_plan']['already_done'])
    gated_list = "".join(f"<li>{esc(x)}</li>" for x in bank['traffic_plan']['missing_and_gated'])
    reading = " · ".join(outbound(d, r['url'], esc(r['name'])) for r in bank['traffic_plan']['official_reading'])

    body = pagehead('Suggestions / design brief', 'What should the next version do?',
                    'Four paths, the copy-ready prompt, the design tokens, the house-style register and a thirty-title topic bank — everything a designer or writer needs, and nothing they must guess.',
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
<h2>Design pack — the tokens that feed the prompt</h2>
<p>The prompt above is the sentence a designer starts from. These are the concrete tokens behind it, so the next pass is a decision about values rather than a fresh interpretation. The Basis column cites official guidance where one exists; a design decision with no official source is flagged as such rather than presented as a fact.</p>
{table(['Token', 'What it means on the page', 'Basis'], token_rows, caption='Design tokens for the next pass')}''', cls='section-tint')
    body += section(f'''
<div class="sec-head"><div><p class="eyebrow"><i></i> THE GATE</p>
<h2>House-style register</h2></div>
<p>Ten rules, each with its basis. Three of them are Amazon or FTC rules the build already enforces; the rest are the difference between a publication and a generated feed.</p></div>
{style_table}
<p class="table-note">Approving this register is S-32 on the <a href="{esc(rel(d, 'suggestions/index.html'))}">suggestions board</a>. It constrains only future pages; nothing published changes retroactively.</p>''')
    body += section(f'''
<h2>Topic bank — catchy, question-shaped, not invented</h2>
<p>These are working hypotheses for articles, mapped to the two clusters on the shelf. None is a claim that a topic is trending, that it has search volume, or that any product is best. The <em>before you write it</em> column is the gate: a topic is commissioned only when the named evidence exists, and until then it stays a suggestion. Rows whose guide already ships say so and link to it. This is the surface to review and pick from before any of it is written.</p>
{table(['Ref', 'Working topic', 'Cluster', 'State', 'Evidence required before writing it', 'Basis'], brief_rows, caption='T-01 to T-16 · the brief’s hypotheses, operationalized — proposals, not a publishing order')}
<div class="callout"><h2>What this bank is not</h2>
<p>None of these titles is a claim about search volume, popularity or trend data — no keyword tool was consulted. They are shaped like the questions buyers ask because that is the only defensible way to guess before measurement exists. The gate is S-33: Search Console (S-03) confirms which questions are real, then those topics get written. T-23 (the first-use smell question) is on hold until a citable source exists; a guessed safety answer is the one thing this site cannot ship.</p></div>''')
    body += section(f'''
<div class="sec-head"><div><p class="eyebrow"><i></i> THE NEXT WAVE</p>
<h2>Session additions to the bank</h2></div>
<p>Fourteen further working titles in five clusters, six mapping to published guides. Clustered so internal links are deliberate, seasonal where the calendar helps.</p></div>
{topic_table}''', cls='section-tint')
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
    return page(d, title='Design decision brief — Crisp & Counter', description='The copy-ready design prompt, design tokens, ten house-style rules and a thirty-title topic bank for the next affiliate publication design pass, with evidence and release gates.',
                body=body, active='suggestions/index.html', canonical='suggestions/design.html')
