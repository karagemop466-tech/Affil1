"""Generate the public launch register; operator preflight never publishes a CTA."""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from layout import DISCLOSURE, SITE_URL, esc, link, pagehead, section, table

INTENT = Path(__file__).with_name('intent.json')
OUTPUT = ROOT / 'operations/launch-readiness.html'
POLICY = 'https://affiliate-program.amazon.com/help/operating/policies'
AGREEMENT = 'https://affiliate-program.amazon.com/help/operating/agreement'
ASIN = 'https://sell.amazon.com/blog/what-is-an-asin'
GSC = 'https://support.google.com/webmasters/answer/7576553?hl=en'
PAGES_DOC = 'https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages'
FTC = 'https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking#affiliateornetwork'
GOOGLE_LINKS = 'https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links'
USDA = 'https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers'
CONFIRMATION = ('intended_asin', 'official_listing_url', 'confirmation_date', 'confirmation_source',
                'approved_special_link', 'tracking_report_reference')


def eligible(p, tag):
    """Mechanical checks for long-form Amazon.com links only. Evidence must still be reviewed."""
    if not all(isinstance(p.get(k), str) and p[k].strip() for k in CONFIRMATION):
        return False
    asin = p['intended_asin']
    if not re.fullmatch(r'[A-Z0-9]{10}', asin):
        return False
    if p['official_listing_url'] != f'https://www.amazon.com/dp/{asin}':
        return False
    try:
        day = date.fromisoformat(p['confirmation_date'])
        url = urlsplit(p['approved_special_link'])
        source = urlsplit(p['confirmation_source'])
    except ValueError:
        return False
    return (day.isoformat() == p['confirmation_date'] and day <= date.today()
            and source.scheme == 'https' and source.netloc == 'affiliate-program.amazon.com'
            and bool(source.path.strip('/')) and not source.query and not source.fragment
            and url.scheme == 'https' and url.netloc == 'www.amazon.com'
            and url.path == f'/dp/{asin}' and not url.fragment
            and parse_qs(url.query, keep_blank_values=True).get('tag') == [tag]
            and bool(re.fullmatch(r'[A-Za-z0-9._-]{1,80}', p['tracking_report_reference'])))


def validate(doc):
    records = doc['records']
    if [p['ref'] for p in records] != [f'P-0{i}' for i in range(1, 6)]:
        raise ValueError('expected five unique references in order')
    for p in records:
        if not re.fullmatch(r'https://link\.amazon/[A-Za-z0-9]{9}', p['submitted_link']):
            raise ValueError('unexpected submitted slug')
        if not re.fullmatch(r'https://www\.amazon\.com/dp/[A-Z0-9]{10}', p['observed_redirect_target']):
            raise ValueError('unexpected listing observation')
        if not isinstance(p['observed_label'], str) or not p['observed_label'].strip():
            raise ValueError('missing observed title label')
        if set(CONFIRMATION) - set(p):
            raise ValueError('missing confirmation fields')
        if any(p[k] is not None for k in CONFIRMATION) and not eligible(p, doc['tracking_id_supplied']):
            raise ValueError(f"{p['ref']}: incomplete confirmation or malformed Special Link")


def source(url, label, *, product=False):
    return {'html': link('operations', url, esc(label), external=True, sponsored=product)}


def render(doc):
    rows = []
    for p in doc['records']:
        observed = p['observed_redirect_target']
        row = [p['ref'], p['submitted_link'].rsplit('/', 1)[1],
               source(observed, f"{p['observed_label']} · {observed.rsplit('/', 1)[1]}", product=True)]
        row.extend(p[k] or '' for k in CONFIRMATION[:3])
        row.append(source(p['confirmation_source'], 'Associates evidence') if p['confirmation_source'] else '')
        row.append('Needs final editorial review' if eligible(p, doc['tracking_id_supplied']) else 'Unverified · CTA held')
        rows.append(row)
    findings = [
        ['Are the listing destinations confirmed intent?', 'No. Five listing pages observed in this pass. P-04 and P-05 also have contradictory redirect observations.', 'Validate one link per exact variant in the enrolled Associates workflow. Record the verified destination and tracking report before scaling.', source(AGREEMENT, 'Amazon Operating Agreement')],
        ['Are the short links invalid?', 'Unknown. Redirects and absent visible tag parameters do not establish compliance or attribution.', 'Use an Amazon-provided link from the enrolled account; do not append a tag and call it verified.', source(POLICY, 'Amazon Program Policies')],
        ['Can we show price, stock or reviews?', 'No approved feed is connected to this workflow. No commerce fields were transcribed from the fetched pages.', 'Check the current API license, access and display rules before publishing any dynamic data.', source(POLICY, 'Amazon Program Policies')],
        ['Are we collecting clicks or orders?', 'Not on GitHub Pages. The optional same-origin counter has no deployment there. Orders are not browser events.', 'Deploy after a privacy and retention review; import aggregate Associates reports privately, with dates and provenance.', source(PAGES_DOC, 'GitHub Pages hosting docs')],
        ['What should we publish next?', 'Capacity, cleanup and thermometer questions are editorial ideas. No search-demand or conversion evidence was obtained.', 'Verify Search Console and review the query/page report weekly. Draft one guide every two weeks at most; skip a cycle if evidence is absent.', source(GSC, 'Search Console Performance report')],
    ]
    proposals = [
        ['1 · First', 'Prove the purchase path', 'Start with one exact variant per product. Keep the buying CTA off until its destination and tracking evidence pass review.', source(AGREEMENT, 'Amazon Special Link terms')],
        ['2 · Next', 'Write for one real kitchen decision', 'Try “Would your usual dinner fit in one layer?” or “Instant-read or leave-in probe for a holiday roast?” State how to check in the manual; never imply hands-on testing.', source(USDA, 'USDA food thermometer guidance')],
        ['3 · After baseline', 'Improve one guide instead of launching another cluster', 'Use Search Console query/page pairs; choose one recurring buyer question. Compare the same date windows and change one thing at a time. No forecast.', source(GSC, 'Google report and caveats')],
        ['4 · Hold', 'Offer a reader digest', 'Keep RSS available. Defer email until there is a reviewed provider, consent record, unsubscribe flow and retention plan.', source(PAGES_DOC, 'GitHub Pages capabilities')],
    ]
    reg = table(['Ref', 'Submitted slug', 'Observed Amazon listing (source)', 'Intended ASIN', 'Confirmed listing URL', 'Confirmed date', 'Confirmation source', 'Gate'], rows,
                caption=f"Destination observations · {doc['checked_on']}",
                note='Blank confirmation fields are unverified. Observed listings are evidence links, not validated affiliate links.')
    flags = ''.join(f'<li><strong>{esc(p["ref"])}</strong> · {esc(p["prior_discrepancy"])}'
                    + (f' {source(p["alternate_observed_target"], "Alternate Amazon listing", product=True)["html"]}.'
                       if p.get("alternate_observed_target") else '') + '</li>'
                    for p in doc['records'] if p['prior_discrepancy'])
    content = pagehead('Operations desk', 'Affiliate launch readiness',
                       'What readers can use now, what the evidence supports, and what must be checked before monetizing.',
                       meta='Tracking ID supplied: <code>shopnow047c-20</code> · attribution not confirmed')
    content += section(f'''<h2>Executive summary</h2>
<p>Keep the buying guides live. The submitted links reached three air-fryer listings and two thermometer listings in this recheck. None has an independently confirmed intended ASIN or confirmed attribution. Product pages should help a reader choose a format first; keep verified purchasing links separate from the evidence register.</p>
<p>Start with existing guides on capacity and cleanup. Publish the next question only when it answers something the reader cannot get from a listing alone. Keep the scope narrow: no rankings, price quotes, popularity claims, commission estimates or revenue forecasts without admissible evidence.</p>
<h2>The five submitted links</h2>{reg}
<p>Amazon defines an <a rel="noopener" href="{ASIN}">ASIN</a> as a ten-character identifier; the submitted nine-character slugs are not ASINs.</p>
<h2 id="flagged">Flagged for review</h2><ul>{flags}</ul>
<p><a href="https://github.com/karagemop466-tech/Affil1/blob/main/data/verification-audit.json">Read the historical redirect audit</a> · <a href="../review/">Published review queue</a></p>
{table(['Decision question', 'What we know now', 'How to close the gap', 'Official source'], findings)}
<h2 id="suggestions">Suggestions for review</h2>
{table(['Order', 'Proposal', 'Decision or next test', 'Official source'], proposals)}
<p><a href="../suggestions/">Use the suggestions board to record accept, hold or reject</a>. A local decision does not publish links or change this site.</p>
<h2 id="prompt">Design and drafting brief</h2>
<p>Make the home page feel like the front of a kitchen publication: warm editorial photography, product formats before operations, one question per headline, and one useful next action per card. Illustrations must not pass as product photos. Use an honest editorial byline, not a fabricated tester. On mobile, keep disclosures visible before the content and put operations in a single menu and the footer.</p>
<p>Give the drafting agent only the approved source packet and a buyer question. Ask for the decision first, a practical example second, and a source beside each product claim. Return a separate evidence checklist and gaps; do not guess missing numbers. A draft is not a publish instruction. Check the <a rel="noopener" href="{AGREEMENT}">Associates Agreement</a>, <a href="{FTC}">FTC disclosure guidance</a> and <a href="{GOOGLE_LINKS}">Google paid-link markup</a> before shipping a new CTA.</p>''')
    canonical = SITE_URL + '/operations/launch-readiness.html'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Affiliate launch readiness — Crisp &amp; Counter</title>
<meta name="description" content="Dated product observations, the affiliate publishing gate, and suggested next decisions.">
<meta name="robots" content="noindex,follow"><link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="../assets/css/site.css"><link rel="alternate" type="application/rss+xml" href="../feed.xml" title="Crisp &amp; Counter">
</head><body><a class="skip" href="#main">Skip to content</a><header class="masthead"><div class="wrap masthead-inner">
<a class="brand" href="../"><span class="brand-name">Crisp <span class="brand-amp">&amp;</span> Counter</span><span class="brand-tag">Kitchen buying guides</span></a>
<nav class="nav" aria-label="Sections"><a href="../guides/">Buying guides</a><a href="../compare/">Compare</a><a href="../review/">Review desk</a></nav></div></header>
<div class="disclosure-bar" role="region" aria-label="Affiliate disclosure"><div class="wrap disclosure-inner"><p>{DISCLOSURE} <a href="../about/#disclosure">About the disclosure</a></p></div></div>
<main id="main">{content}</main>
<footer class="site-footer"><div class="wrap"><p class="foot-disclosure">{DISCLOSURE}</p><p><a href="../brief/">Executive summary</a> · <a href="../operations/ledger.html">Campaign ledger</a> · <a href="../questions/">Open questions</a> · <a href="../suggestions/">Suggestions</a> · <a href="../feed.xml">RSS</a></p></div></footer>
<script src="../assets/js/analytics.js" defer></script></body></html>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='check the generated public page is current')
    parser.add_argument('--intent', type=Path, default=INTENT)
    parser.add_argument('--require-approved', help='fail unless the reference has complete evidence and a matching URL')
    args = parser.parse_args()
    doc = json.loads(args.intent.read_text())
    validate(doc)
    if args.require_approved:
        if not any(p['ref'] == args.require_approved and eligible(p, doc['tracking_id_supplied']) for p in doc['records']):
            parser.exit(1, f'{args.require_approved}: paid CTA blocked; no approved evidence bundle.\n')
        return
    if args.intent != INTENT:
        parser.error('custom manifests are only supported for --require-approved')
    text = render(doc)
    if args.check:
        if OUTPUT.read_text() != text:
            parser.exit(1, 'Run python3 kitchen-build/readiness.py to refresh the launch register.\n')
    else:
        OUTPUT.write_text(text, encoding='utf-8')


if __name__ == '__main__':
    main()
