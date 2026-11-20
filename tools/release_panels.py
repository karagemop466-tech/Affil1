"""Publication-ready decision and source panels, kept out of buyer navigation."""
REPORTS = 'https://affiliate-program.amazon.com/home/reports'
FTC = 'https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking'
GSC = 'https://support.google.com/webmasters/answer/9008080'
GOOGLE = 'https://developers.google.com/search/docs/fundamentals/creating-helpful-content'
PAGES = 'https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages'
PAGES_LIMITS = 'https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits'


def render(d, canonical):
    from layout import esc, outbound, rel, section, table
    def cite(url, label):
        return {'html': outbound(d, url, label)}
    if canonical == 'suggestions/':
        decision = table(['Decision', 'What we know', 'What we still need', 'How to find out', 'Review source'], [
            ['Release one product first', 'Five public listing observations; no confirmed intent or credited clicks.', 'Correct item, attributed link and review evidence.', 'Use the enrolled link generator for one confirmed ASIN; verify destination and review the permitted reporting workflow before promoting it.', cite(REPORTS, 'Associates reports')],
            ['Make a useful seasonal guide', 'Capacity and cleanup are already covered; no measured search demand.', 'Which real queries reach the site, and where buyers still need help.', 'Verify the URL-prefix property, submit the sitemap, then review weekly impressions and clicks. Choose one specific question per cycle.', cite(GSC, 'Search Console verification')],
            ['Launch first-party measurement', 'Five counters are implemented; Pages cannot run the collector.', 'Approved same-origin runtime, retention and notice.', 'Test the endpoint and all five counters in staging, including opt-out and disabled mode. Keep reported orders separate.', cite(PAGES, 'GitHub Pages documentation')],
            ['Choose production hosting before monetizing', 'Pages currently serves the editorial preview; its usage limits restrict sites primarily facilitating commercial transactions.', 'A suitable runtime and a hosting decision before activating revenue features.', 'Review hosting terms and plan a first-party deployment before enabling purchase links and production counters.', cite(PAGES_LIMITS, 'GitHub Pages usage limits')],
            ['Use AI for drafts, not proof', 'Listing claims are not hands-on findings; no priced or ranked products.', 'Official product material, measurable user need, editorial owner.', 'Generate outlines only. Have an editor check every claim against its source, byline and disclosure before scheduling.', cite(GOOGLE, 'Google Search Central')],
        ], cls='register')
        return section(f'''<div class="lede-prose"><p class="eyebrow">Decision brief</p><h2>What to approve, and what to find out first</h2></div>{decision}
<div class="callout"><h3>Design brief for the next iteration</h3><p>Design a warm, magazine-style kitchen shortlist. Lead with one cooking decision, then show the three appliance formats using consistent cards. Pair every card with a specific thing to measure or check. Reuse a cover, a shortlist, a seasonal story and a single RSS invitation. Use only labeled editorial illustrations and attributable bylines. Do not use “best”, fake reviews, discount badges or star ratings without substantiation.</p><p><strong>Cadence:</strong> Review evidence every week; plan one question-shaped guide per fortnight once collection and Search Console are live. Publish only after the fact, image and disclosure checks pass, then verify its canonical URL in both sitemap and RSS. Review the prior guide on the same date window each cycle.</p></div>''', sid='launch-decisions')
    if canonical == 'review/':
        return section(f'''<div class="lede-prose"><p class="eyebrow">Flagged for Review</p><h2>Production hosting</h2><p>Do not treat the editorial Pages deployment as approval for a commercial launch. GitHub Pages is static and its usage rules restrict sites primarily directed at facilitating commercial transactions. Review the intended use and select a supported first-party host before scaling monetization or telemetry. {outbound(d, PAGES_LIMITS, 'Official GitHub Pages usage limits')}.</p></div>''', sid='hosting-review')
    if canonical == 'brief/':
        return section(f'''<div class="callout"><p class="eyebrow">Executive launch decision</p><h2>Publish the guides. Hold purchase links until they’re verified.</h2><p>The buyer edition can help readers compare formats now. Public redirects support listing identification only; affiliate attribution, orders, pricing inputs and organic demand are unverified. Do not rank by conversion or commission and do not auto-publish AI output.</p><p><a href="{esc(rel(d, 'products/index.html'))}">Product records and intent</a> &middot; <a href="{esc(rel(d, 'suggestions/index.html'))}#launch-decisions">Decision brief and design prompt</a> &middot; {outbound(d, FTC, 'FTC endorsement guidance')}</p></div>''', sid='launch-decision')
    return ''
