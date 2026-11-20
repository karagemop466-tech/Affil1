# Countertop Notes

A static, publication-style affiliate buying guide and decision-support site for kitchen appliances. The editorial direction is reader-first: practical buyer questions, transparent sourcing, and unknowns left blank rather than guessed.

## Project contents

- `index.html` — publication front page with four buyer-question guides and the five submitted links.
- `guides/` — original comparison and buyer-decision articles.
- `product-register.html` — separate intended-product fields and unobserved redirect-target fields for each submitted link.
- `suggestions.html` — editorial paths, questions, evidence gaps, and discovery recommendations.
- `executive-summary.html` — project summary and launch gates.
- `decision-tool.html`, `campaign-ledger.html`, `flagged.html`, `about.html` — decision aid, empty measurement ledger, unresolved items, and sources/disclosures.
- `sitemap.xml`, `feed.xml`, `robots.txt` — crawl and feed discovery files.
- `analytics/server.mjs` — optional self-hosted event collector. GitHub Pages itself cannot run this server.
- `.github/workflows/pages.yml` — validates and deploys the static site to GitHub Pages from `main`.

## Important verification boundary

The five product URLs and tracking ID (`shopnow047c-20`) were supplied in the project brief. Product identity, intended ASIN, official listing URL, redirect destination, Associates enrollment, link/tag attribution, product details, prices, review data, commissions, and conversions have not been independently confirmed. The product register leaves those fields blank. The exact compliance status of the submitted short links is unresolved; this project does not claim they are invalid. See [Flagged for review](flagged.html).

## Local check/build

```sh
python3 tools/check_site.py --build
```

This validates local links, page disclosures, XML feeds, and the five product-record policy references, then creates `_site/` for the Pages artifact.

## Publishing and measurement

GitHub Pages must be enabled to use GitHub Actions as the publishing source. On merge to `main`, the workflow builds and deploys `_site/`; verify the workflow run and resulting URL in repository Actions/Pages settings. Search Console ownership, sitemap submission, and analytics endpoint hosting are separate setup steps and are not represented as complete here. See [deployment notes](docs/deployment-and-verification.md).
