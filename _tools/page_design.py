"""Decision brief for the next design pass; alternatives are not work orders.

This page is the review surface for the design of Crisp & Counter as a polished
marketing affiliate publication. It carries three things a reviewer can approve
before any implementation: the four direction options, a concrete design-token
pack, and a topic bank of catchy, question-shaped article ideas. Every topic row
states what must be true before it is written, so approving a row is a decision
rather than a blank cheque. Nothing here is a claim about popularity, search
volume or product superiority.
"""
from layout import esc, outbound, page, pagehead, rel, section, table

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

# Design-token pack. These are proposals for the design prompt, not verified
# facts, so the Basis column cites official guidance where one exists and says
# "design decision" where none does. Nothing is presented as a verified claim
# without a source.
TOKENS = (
    ('Typography', 'Serif display headlines (Fraunces), a plain sans body, a tight type scale, and one voice for cards and guides.', 'design decision'),
    ('Colour', 'Warm paper background, a dark green accent, one warm highlight for the buy action; no more than three colours in view.', 'design decision'),
    ('Layout', 'One useful choice first on mobile (single basket, dual basket, or oven), then detail; a persistent shortlist rail on desktop.', 'design decision'),
    ('Imagery', 'Food photography or visibly labelled illustrations only. No invented test result, star rating, sale or ranking.', FTC),
    ('Disclosure', 'The Associates statement under the masthead on every page and repeated in the footer; never behind a link or a hover.', FTC),
    ('Accessibility', 'Keyboard-reachable cards and tables, real alt text, sufficient contrast, and no motion that cannot be reduced.', 'design decision'),
)

# Topic bank. Working hypotheses for catchy, question-shaped articles, mapped to
# the two product clusters. Each row names the evidence required before it is
# written; none is a claim that the topic is popular or that any product is best.
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
    ('T-16', 'Air fryer noise, smell and smoke: what a listing never tells you', 'Air fryers', 'Observations from a named, dated first-person log \u2014 or nothing. Do not commission without hands-on evidence.', FTC),
)

# Rows whose guide already ships are marked published, by title match against
# the build's own guide list \u2014 one definition of "written", not a second copy.
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


def build(d):
    rows = [[name, change, evidence, {"html": outbound(d, source[1], esc(source[0]))}]
            for name, change, evidence, source in OPTIONS]
    body = pagehead('Suggestions / design brief', 'What should the next version do?',
                    'Four paths, with the evidence worth gathering before committing to any of them.',
                    meta='Decision brief &middot; November 2026')
    body += section(f'''
<h2>Pick one direction to test</h2>
{table(['Direction', 'What changes', 'Question and how to answer it', 'Official reference'], rows, caption='Options for the next design pass')}
<div class="callout"><h2>Copy-ready design prompt</h2>
<p>Design Crisp &amp; Counter as an independent kitchen buying publication. Use warm paper, dark green accents, legible serif headlines, and clear food photography or visibly labelled illustrations. On mobile, start with one useful choice: single basket, dual basket, or oven. On each card, write a cooking scenario, one trade-off, and one thing to check next. Make the comparison readable by keyboard and on small screens. Give guides a consistent editorial byline, sources, and related reading. Put the Associates disclosure under the masthead and in the footer; keep the source register and decision tools one click away. Never show an invented test result, star rating, sale, or ranking. Do not show a tracked shopping CTA until the destination and attribution are verified.</p></div>''')

    token_rows = [[name, meaning, _basis(d, basis)] for name, meaning, basis in TOKENS]
    body += section(f'''
<h2>Design pack — the tokens that feed the prompt</h2>
<p>The prompt above is the sentence a designer starts from. These are the concrete tokens behind it, so the next pass is a decision about values rather than a fresh interpretation. The Basis column cites official guidance where one exists; a design decision with no official source is flagged as such rather than presented as a fact.</p>
{table(['Token', 'What it means on the page', 'Basis'], token_rows, caption='Design tokens for the next pass')}''', cls='section-tint')

    topic_rows = [[tid, topic, cluster, _state(topic), before, _basis(d, basis)]
                  for tid, topic, cluster, before, basis in TOPICS]
    body += section(f'''
<h2>Topic bank — catchy, question-shaped, not invented</h2>
<p>These are working hypotheses for articles, mapped to the two clusters on the shelf. None is a claim that a topic is trending, that it has search volume, or that any product is best. The <em>before you write it</em> column is the gate: a topic is commissioned only when the named evidence exists, and until then it stays a suggestion. Rows whose guide already ships say so and link to it. This is the surface to review and pick from before any of it is written.</p>
{table(['Ref', 'Working topic', 'Cluster', 'State', 'Evidence required before writing it', 'Basis'], topic_rows, caption='Editorial topic bank — proposals, not a publishing order')}''')

    body += section(f'''
<h2>A cadence that can respond to results</h2>
<ol class="tight">
<li><strong>Weekly:</strong> Check indexing and query/page patterns in the verified Search Console property. Log the date range and missing data. The first themes are small kitchens, meal prep, holiday sides, and food thermometers, not proven search trends.</li>
<li><strong>Every other week:</strong> Publish one distinct question or improve an existing guide. Update an existing page rather than creating a near-duplicate. The build adds each accepted guide to the sitemap and RSS feed.</li>
<li><strong>Every 28 days:</strong> Review query and landing-page data against the previous comparable window. Keep on-site outbound counts separate from Associates orders. If the data are sparse, improve the guide or keep collecting; don’t estimate demand, commissions, or conversion.</li></ol>
<h2>The organic loop, in one line</h2>
<p>Publish one question-shaped guide &rarr; the build adds it to the sitemap and RSS feed &rarr; link it from the shortlist and related guides &rarr; read the query and landing-page data &rarr; choose the next topic from what arrived, not from instinct. Search Console is the only instrument that closes that loop; without it the site publishes into the dark.</p>
<p><strong>Hosting gate:</strong> {outbound(d, PAGES[1], esc(PAGES[0]))} restricts using Pages for sites primarily intended to facilitate commercial transactions. Treat this Pages release as editorial and move the monetized operation to appropriate hosting if it becomes primarily commercial.</p>
<p><a href="{esc(rel(d, 'suggestions/index.html'))}">All suggestions</a> &middot;
<a href="{esc(rel(d, 'questions/index.html'))}">Open questions</a> &middot;
<a href="{esc(rel(d, 'review/measurement.html'))}">Measurement status</a></p>''')
    return page(d, title='Design decision brief — Crisp & Counter', description='Practical alternatives for the next affiliate publication design, with evidence and release gates.',
                body=body, active='suggestions/index.html', canonical='suggestions/design.html')
