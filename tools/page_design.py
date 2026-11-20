"""Decision brief for the next design pass; alternatives are not work orders."""
from layout import esc, outbound, page, pagehead, rel, section, table

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
<p>Design Crisp &amp; Counter as an independent kitchen buying publication. Use warm paper, dark green accents, legible serif headlines, and clear food photography or visibly labelled illustrations. On mobile, start with one useful choice: single basket, dual basket, or oven. On each card, write a cooking scenario, one trade-off, and one thing to check next. Make the comparison readable by keyboard and on small screens. Give guides a consistent editorial byline, sources, and related reading. Put the Associates disclosure under the masthead and in the footer; keep the source register and decision tools one click away. Never show an invented test result, star rating, sale, or ranking. Do not show a tracked shopping CTA until the destination and attribution are verified.</p></div>
<h2>A cadence that can respond to results</h2>
<ol class="tight">
<li><strong>Weekly:</strong> Check indexing and query/page patterns in the verified Search Console property. Log the date range and missing data. The first themes are small kitchens, meal prep, holiday sides, and food thermometers, not proven search trends.</li>
<li><strong>Every other week:</strong> Publish one distinct question or improve an existing guide. Update an existing page rather than creating a near-duplicate. The build adds each accepted guide to the sitemap and RSS feed.</li>
<li><strong>Every 28 days:</strong> Review query and landing-page data against the previous comparable window. Keep on-site outbound counts separate from Associates orders. If the data are sparse, improve the guide or keep collecting; don’t estimate demand, commissions, or conversion.</li></ol>
<p><strong>Hosting gate:</strong> {outbound(d, PAGES[1], esc(PAGES[0]))} restricts using Pages for sites primarily intended to facilitate commercial transactions. Treat this Pages release as editorial and move the monetized operation to appropriate hosting if it becomes primarily commercial.</p>
<p><a href="{esc(rel(d, 'suggestions/index.html'))}">All suggestions</a> &middot;
<a href="{esc(rel(d, 'questions/index.html'))}">Open questions</a> &middot;
<a href="{esc(rel(d, 'review/measurement.html'))}">Measurement status</a></p>''')
    return page(d, title='Design decision brief — Crisp & Counter', description='Practical alternatives for the next affiliate publication design, with evidence and release gates.',
                body=body, active='suggestions/index.html', canonical='suggestions/design.html')
