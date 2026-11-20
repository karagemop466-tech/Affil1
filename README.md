# Affil1

Amazon affiliate site built to read like a shop, not an audit. Buyer-first guides for air fryers and multi-function kitchen appliances.

**Tracking ID:** `shopnow047c-20`
**Branch:** `arena/f10ea853-affil1` (base `cca8c2a`)
**Prepared:** 2026-11-20

## What’s in the repo

- `/` — publication front page: product picks, buyer-question guides, how it works
- `/categories/air-fryers.html` — findings table (one row per submitted link, source link per row)
- `/dashboard.html` — entries/findings table, empty campaign ledger, measurement status
- `/guides/` — four question-shaped buying guides (working titles)
- `/suggestions.html` — decision suggestions; review before implementing
- `/reviews/flagged.html` — Flagged for Review page (irregularities and unverified items)
- `/disclosure.html` — Associates statement (tracking ID `shopnow047c-20`)
- `/privacy.html` — privacy notice for self-hosted analytics
- `/assets/css/main.css` — design system
- `/assets/js/common.js` — shared masthead, navigation group, disclosure strip (above the fold), footer
- `/assets/js/analytics.js` — privacy-preserving client; five defined events; outbound click counter
- `/server/collect.js` — self-hosted analytics endpoint (Node.js, run outside GitHub Pages)
- `/data/confirmations.json` — product-intent confirmation records
- `/data/campaign-ledger.json` — empty campaign ledger with provenance trail
- `/sitemap.xml`, `/rss.xml`, `/robots.txt`

## Verification standard

Every table row carries a source link to an official source (Amazon.com). Values not confirmed from an official source are left blank and flagged — never inferred. Full records: `data/confirmations.json`.

## Publishing the site

1. Push to `main`.
2. Enable GitHub Pages for the repository: source = `main` branch, `/ (root)`.
3. Site publishes at `https://karagemop466-tech.github.io/Affil1/`.

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
