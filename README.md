# Affil1 — Amazon affiliate site

Buyer-first affiliate editorial site for air fryers and multi-function kitchen appliances. Built to read like a shop, not an audit: product picks lead the front page, every page carries an above-the-fold Associates disclosure, and every outbound product link is marked `sponsored`.

**Tracking ID:** `shopnow047c-20` (user-supplied; account enrollment and live attribution unverified)
**Branch:** `arena/f10ea853-affil1` (base `cca8c2a`, merged with parallel session `arena/8e0006cf-affil1`)
**Prepared:** 2026-11-20

## What’s in the repo

- `/` — Affil1 publication front page: product picks, buyer-question guides, how it works
- `/categories/air-fryers.html` — findings table (one row per submitted link, source link per row)
- `/dashboard.html` — entries/findings table, empty campaign ledger, measurement status
- `/guides/` — question-shaped buying guides (working titles)
- `/suggestions.html` — decision suggestions; review before implementing
- `/reviews/flagged.html` — Affil1 Flagged for Review page (irregularities and unverified items)
- `/guides/flagged-for-review.html` — parallel session’s review queue (Good Measure Kitchen)
- `/disclosure.html` — Associates statement (tracking ID `shopnow047c-20`)
- `/privacy.html` — privacy notice for self-hosted analytics
- `/assets/css/main.css` — design system
- `/assets/js/common.js` — shared masthead, navigation group, disclosure strip, footer
- `/assets/js/analytics.js` — privacy-preserving client; five defined events; outbound click counter
- `/server/collect.js` — self-hosted analytics endpoint (Node.js, run outside GitHub Pages)
- `/data/confirmations.json` — product-intent confirmation records
- `/data/campaign-ledger.json` — empty campaign ledger with provenance trail
- `/app.js`, `/data.js`, `/styles.css` — parallel session’s static storefront components (retained)
- `/feed.xml` — parallel session’s RSS feed (retained)
- `/sitemap.xml`, `/rss.xml`, `/robots.txt`

## Verification standard

Every table row carries a source link to an official source (Amazon.com). Values not confirmed from an official source are left blank and flagged — never inferred. Full records: `data/confirmations.json`.

Verified against Amazon.com (official site), fetched 2026-11-20:

| # | Submitted link | Intended ASIN | Verified listing | Status |
|---|---|---|---|---|
| 1 | https://link.amazon/B04G1MEwY | B04G1MEwY | https://www.amazon.com/dp/B0CDY277D3 | Verified |
| 2 | https://link.amazon/B02NbDxp3 | B02NbDxp3 | https://www.amazon.com/dp/B09B7SB46R | Verified |
| 3 | https://link.amazon/B00hJ57DV | B00hJ57DV | — | Unverified — homepage reached |
| 4 | https://link.amazon/B0c8moW59 | B0c8moW59 | — | Unverified — Amazon checkpoint |
| 5 | https://link.amazon/B0f3GKalj | B0f3GKalj | — | Unverified — homepage reached |

## Preview locally

Run `python3 -m http.server 8080 --bind 0.0.0.0` and open the preview. The site is plain HTML/CSS/JS and has no build dependencies.

## Deployment

`.github/workflows/pages.yml` deploys to GitHub Pages on pushes to `main` and on manual workflow dispatch. Enable GitHub Pages with **GitHub Actions** as the source in repository settings. Update `sitemap.xml` and `rss.xml` if the canonical Pages URL differs from `https://karagemop466-tech.github.io/Affil1/`. Search Console and analytics require account/property setup and are not falsely represented as connected.

## Self-hosted analytics

GitHub Pages is static, so the collector must run outside Pages:

```
node server/collect.js   # PORT=8080 by default; set $PORT to override
POST /analytics/collect  # newline-delimited JSON events -> data/events.jsonl
```

The client degrades silently if the collector is unreachable.

## Decision process

Suggestions live on `/suggestions.html`. Nothing is implemented until a suggestion is reviewed and a path is chosen. See `PUBLISHING_WORKFLOW.md` for the pre-publish compliance gate.

## Coordination

`COORDINATION.md` is the shared task board for parallel sessions. Claim tasks there before working.

## Editorial and compliance limits (both sessions)

- Top-of-page and footer Associates disclosure on each page.
- Submitted outbound product links use `rel="sponsored nofollow"`.
- No product features, price, reviews, rank, popularity, commission, conversion, or revenue claims are populated without evidence.
- Flagged pages list missing data, official source references, and next steps; unverified means unverified — not invalid.
