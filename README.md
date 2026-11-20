# Affil1

Reader-first Amazon affiliate marketing publication.

## Tracking ID
`shopnow047c-20`

## Site
- **Front page:** `index.html` — publication front page leading with products
- **Products:** `products.html` — product-intent confirmation record (all 5 submitted Amazon short links unverified)
- **Categories:** `categories.html` — category dashboard table
- **Guides:** `guides.html` + `guides/buying-guide-air-fryer.html` — question-shaped buying guides
- **Suggestions:** `suggestions.html` — review-before-implement suggestions
- **Open questions:** `questions.html` — questions, information, and answers to address before decisions
- **Executive summary:** `executive-summary.html`
- **Affiliate disclosure:** `disclosure.html` — above the fold on every page + repeated in footer
- **Flagged for Review:** `flagged-for-review.html` — flagged irregularities & unverified items

## Data
- `data/products.json` — product-intent confirmation record
- `data/ledger.json` — campaign ledger (empty by design)
- `sitemap.xml` — one canonical site for search engines
- `feed.xml` — RSS feed

## Assets
- `css/style.css` — design system
- `js/analytics.js` — self-hosted, privacy-preserving analytics (5 events)
- `js/main.js` — navigation, disclosure strip, outbound-click counter, sponsored link marking

## Verification
Per the project verification rule, every value that cannot be confirmed from an official source is left blank and flagged unverified. Nothing is inferred. The build environment cannot reach amazon.com or link.amazon.com, so all five submitted short links are unverified. See `flagged-for-review.html` and `questions.html`.

## Compliance
- Disclosure strip above the fold on every page, repeated in the footer
- All outbound product links marked `rel="sponsored nofollow"`
- Disclosure placement and endorsement context reviewed against the Amazon Associates Program Operating Agreement and FTC guidance (compliance gate)
- Amazon Associate tracking ID: `shopnow047c-20` (enrollment not yet confirmed)

## GitHub Pages
Enable GitHub Pages from the `main` branch (root) to publish. See `COORDINATION.md` for the task board and integration status.
