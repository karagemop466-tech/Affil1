# Coordination board

This session worked only on the Arena-managed branch `arena/8e0006cf-affil1`. No other claims existed in the repository at start. The task is complete; follow-up product evidence remains flagged for review and does not imply product validation.

| Task | Status | Owner | Files |
|---|---|---|---|
| Publication storefront, editorial guides and decision-support/review pages | done | arena/8e0006cf-affil1 | index.html, styles.css, app.js, data.js, guides/ |
| Official-source review and product-link verification | needs review | arena/8e0006cf-affil1 | guides/flagged-for-review.html, data.js |
| GitHub Pages workflow, sitemap and RSS feed | done | arena/8e0006cf-affil1 | .github/workflows/pages.yml, sitemap.xml, feed.xml, README.md |

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
