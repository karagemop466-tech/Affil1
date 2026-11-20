# Coordination board

This checkout is on the Arena-managed branch `arena/8e0006cf-affil1`. Per session constraints, work remains on this branch; no other agent claims are visible in this repository.

| Task | Status | Owner | Files |
|---|---|---|---|
| Publication storefront, decision-support and flagged-review pages | in progress | arena/8e0006cf-affil1 | index.html, styles.css, app.js, data.js, guides/, COORDINATION.md |
| Official-source verification of supplied product links and marketing claims | needs review | arena/8e0006cf-affil1 | guides/flagged-for-review.html, data.js |
| GitHub Pages deployment configuration | in progress | arena/8e0006cf-affil1 | .github/workflows/pages.yml |

## Sources and verification log

- No product attributes, prices, ratings, popularity, commissions, availability, reviews, or conversion performance are treated as verified. Supplied links/IDs are user-provided inputs, not confirmation of destination contents or Amazon Associates eligibility.
- Amazon Associates Program Operating Agreement: https://affiliate-program.amazon.com/help/operating/agreement
- Amazon Associates Program Policies: https://affiliate-program.amazon.com/help/operating/policies
- FTC Endorsement Guides: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking

## Irregularities / unresolved decisions

- All five supplied `link.amazon/...` URLs and apparent ASIN strings have unresolved destination/official listing, intended-ASIN, redirect, tracking-tag and enrolled-account status. Preserve intended URL/ASIN separately from any observed redirect; test one per product inside the enrolled Associates workflow before scaling.
- Selected tracking ID `shopnow047c-20` was supplied by the user; account ownership/enrollment and link behavior are not independently verifiable here.
- No authorized first-party Associates reports, campaign data, Amazon Product Advertising API access, analytics consent/legal setup, Search Console property, or publishing credentials were supplied. No order/revenue/conversion estimates are fabricated.
- GitHub Pages publication can be configured in-repository, but deployment success depends on repository settings and GitHub Actions permissions.

## Verification performed

Initial repository inspection: only an 8-byte README existed; no existing app, data register, or other claims to verify. Review each source in the site before any claim is labeled verified.
