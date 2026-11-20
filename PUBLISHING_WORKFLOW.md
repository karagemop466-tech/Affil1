# Publishing workflow — evidence before promotion

This is a release checklist for the maintained **Crisp & Counter** edition. A flag can remain open while the editorial site ships. It cannot be used as evidence to enable a blocked feature.

## 1. Product identity and attribution

- Observe each supplied URL separately from any enrolled link. Record the listing, ASIN, date, and unusual outcomes; retain conflicting observations. The [Amazon ASIN definition](https://sell.amazon.com/blog/what-is-an-asin) explains why a short-link slug is not an ASIN.
- If authorized, record the intended ASIN, its official listing URL, date and public Associates Central reference in `kitchen-build/intent.json`. Leave confirmation fields null until the evidence bundle is complete. It is valid for separately sourced intended and observed ASINs to match.
- Generate one Special Link per product in the enrolled workflow. Check the exact destination and variant with Amazon's authorized tooling and reconcile credited, eligible activity with [Associates Central reports](https://affiliate-program.amazon.com/home/reports). Do not create artificial clicks or orders or commit private reports, account identifiers other than the chosen public tag, access tokens, or query-bearing report URLs.
- Only then populate `approved_special_link` and `tracking_report_reference` in the same evidence bundle. The build checks completeness, the intended listing and the selected tag. Resolve conflicting observed destinations before approval. This is a structural gate, **not** independent proof of the report. Public buttons use the direct listings until evidence exists. A short link is not declared invalid merely because attribution is unknown.

## 2. Copy, links and rights

- Recheck the [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement), [Program Policies](https://affiliate-program.amazon.com/help/operating/policies), and [FTC guidance](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking). Read the disclosure on mobile before the first recommendation and again in the footer. Check the adjacent link text and endorsement context, not just the HTML attribute.
- Mark outbound product links `sponsored`. Attribute listing statements, link the source, and leave missing information blank. Don't claim hands-on tests, rankings or trending status without supporting evidence.
- Before introducing Amazon data, review IP, cache/refresh, display, and API eligibility rules. Do not use Program Content or Special Links to develop machine learning models or related technology without the express prior written approval described in Participation Requirements §5. Use cleared inputs for AI-assisted outlines; a reviewer checks every claim and approves publication. No autonomous publishing, scraping or private reporting is enabled.

## 3. Measure, then plan the next guide

- Check [GitHub Pages usage limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) before any commercial rollout. Pages is static. The optional first-party counter is tested but off in production; review hosting, privacy, retention and opt-out before activation. Do not derive sessions or orders from raw events.
- Confirm Search Console ownership and submit the canonical sitemap. Every four weeks read the [Search performance report](https://support.google.com/webmasters/answer/7576553) by page and available query. Improve one guide or propose one distinct guide; if evidence is sparse, record the result and defer. Keep the canonical sitemap and RSS feed in sync with every published guide.
- Start with the empty campaign ledger. Add only authorized first-party report figures, with reporting period, timestamp, source, channel, and provenance. Unknown sessions, clicks or orders remain blank. No forecasts or conversion scores.

## 4. Release

Run `python3 tools/build.py`, `python3 tools/check.py`, `python3 tools/check_local_links.py`, `python3 -m unittest discover -s kitchen-build`, and `python3 -m unittest discover -s analytics`. Stage the maintained edition with `python3 tools/stage.py <empty-output-folder>`. Record reviewer, date, unresolved flags and official sources on the PR. Confirm the Pages run for the merge SHA, not just the most recent green run.
