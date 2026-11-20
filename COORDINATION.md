# Coordination board

Branch: `arena/55d40788-affil1` (session `arena/55d40788-affil1`). Base commit `76d898b` of `main`.

| Task | Status | Owner | Files |
|---|---|---|---|
| Rebuild landing page as publication front page leading with products | in progress | arena/55d40788-affil1 | index.html, styles.css, app.js |
| Product-intent confirmation records table (intended ASIN, official listing URL, confirmation date, source; observed redirect separate) | in progress | arena/55d40788-affil1 | data.js, guides/flagged-for-review.html |
| Privacy-preserving outbound click counter + self-hosted analytics endpoint (5 events) | in progress | arena/55d40788-affil1 | analytics.js, analytics/endpoint.py, app.js |
| Decision-support pages: suggestions queue + open questions/information | in progress | arena/55d40788-affil1 | suggestions.html, questions.html |
| Trendy question-shaped category guides + SEO (sitemap, feed, meta) | in progress | arena/55d40788-affil1 | guides/*.html, sitemap.xml, feed.xml, styles.css |
| Integration, broken-link check, GitHub Pages publish, PR to main | unclaimed | arena/55d40788-affil1 | all |

## Sources and verification log

- Amazon Associates Program Operating Agreement, section 5: https://affiliate-program.amazon.com/help/operating/agreement — official disclosure statement: “As an Amazon Associate I earn from qualifying purchases.”
- Amazon Associates Program Policies: https://affiliate-program.amazon.com/help/operating/policies
- FTC Endorsement Guides FAQ: https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
- User-supplied links are preserved exactly. No redirects followed; no ASIN/listing identity, price, availability, feature, review, commission or performance independently confirmed. Intended identifier and observed redirect are separate fields; observed redirect is blank everywhere.
- Selected tracking ID `shopnow047c-20` is user-supplied; enrollment/site association unverified.
- No authorized Associates reports, Search Console property, analytics credentials or API access supplied. Campaign ledger empty; five event names documented as proposed, instrumentation added client-side.

## Irregularities / unresolved decisions

- All five `link.amazon/...` URLs require enrolled Associates workflow destination and tracking verification. Unresolved status is not a claim they are invalid.
- Tracking ID `shopnow047c-20`: account enrollment and live attribution unverified.
- No analytics endpoint credentials; client-side collector implemented, beacon endpoint must be self-hosted by the operator (see analytics/endpoint.py).

## Delivery

- Not yet delivered. PR and GitHub Pages publish pending integration task.

## Sources and verification log

- Amazon Associates Program Operating Agreement, section 5: https://affiliate-program.amazon.com/help/operating/agreement — official search result confirms required statement: “As an Amazon Associate I earn from qualifying purchases.” Exact disclosure appears above the masthead and in the footer on all site pages. Also references Program Policies; check current rules before operating.
- Amazon Associates Program Policies: https://affiliate-program.amazon.com/help/operating/policies — linked for the operator to consult. No claim of line-by-line policy approval is made.
- FTC Endorsement Guides FAQ: https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking — official FTC guidance says affiliate relationships should be disclosed clearly and conspicuously, close to recommendation/link context.
- User-supplied links are preserved exactly. No redirects were followed and no ASIN/listing identity, current price, availability, feature, review, commissions or performance was independently confirmed. The intended identifier and observed redirect are separate fields; the latter is blank.
- Static checks performed locally and in GitHub Actions: all relative HTML references exist; each page has disclosure; listed submitted product links include `rel="sponsored nofollow noopener"`; sitemap/feed XML parse; GitHub Pages build/deploy workflow passed.

## Irregularities / unresolved decisions

- All five `link.amazon/...` URLs and intended IDs require enrolled Associates workflow destination and tracking verification. Unresolved status is not a claim they are invalid. Record intended ASIN, official listing URL, confirmation date, source and observed redirect separately.
- Selected tracking ID `shopnow047c-20` is user-supplied; account enrollment/site association and live attribution are unverified.
- No authorized Associates reports, campaign data, Amazon Product Advertising API access, Search Console property, Analytics setup, privacy/consent decisions, analytics endpoint or reporting credentials were supplied. Ledger is empty; no conversion score/revenue forecast shown. Five event names are documented as proposed, not deployed.
- RSS/sitemap canonical URL uses `https://karagemop466-tech.github.io/Affil1/`; recheck if repository Pages configuration/domain changes.
- GitHub Actions reported a Node.js 20 deprecation warning for upstream actions under Node 24; deployment succeeded. Refresh action versions when compatible releases are available.

## Delivery

- PR: https://github.com/karagemop466-tech/Affil1/pull/1 — merged 2026-11-20.
- GitHub Pages: https://karagemop466-tech.github.io/Affil1/ — Actions deployment run https://github.com/karagemop466-tech/Affil1/actions/runs/44679102768 completed successfully; workflow's build and deploy jobs passed.
- An initial `git pull --rebase origin arena/8e0006cf-affil1` could not find a remote-tracking branch because it had not been pushed yet; rebased against `origin/main`, then pushed the current Arena branch successfully. No work was discarded.
