# Affil1 — Executive summary

**Project:** Amazon affiliate marketing site (GitHub Pages)
**Branch:** `arena/8206a8d0-affil1` (polish + re-verification pass, 2026-11-20)
**Tracking ID:** `shopnow047c-20`
**Prepared:** 2026-11-20

## What this is
A buyer-facing affiliate site for air fryers and multi-function kitchen appliances. It reads like a shop/publication, not an audit: product picks lead the front page, every page carries an above-the-fold disclosure, and every outbound product link is marked `sponsored`.

## Products submitted (5)
| # | Submitted link | Intended ASIN | Verified listing | Status |
|---|---|---|---|---|
| 1 | https://link.amazon/B04G1MEwY | B04G1MEwY | https://www.amazon.com/dp/B0CDY277D3 | Verified |
| 2 | https://link.amazon/B02NbDxp3 | B02NbDxp3 | https://www.amazon.com/dp/B09B7SB46R | Verified |
| 3 | https://link.amazon/B00hJ57DV | B00hJ57DV | https://www.amazon.com/dp/B08DKYBTPH | Listing checked 2026-11-20 (re-verified) |
| 4 | https://link.amazon/B0c8moW59 | B0c8moW59 | https://www.amazon.com/dp/B0DHZTCNR5 | Listing checked 2026-11-20 (resolved on re-verification; was checkpoint-only) |
| 5 | https://link.amazon/B0f3GKalj | B0f3GKalj | https://www.amazon.com/dp/B0DZFD6R9Z | Listing checked 2026-11-20 (re-verified) |

Verified against Amazon.com (official source) on 2026-11-20. Intended ASIN and observed redirect target are stored in separate fields and never merged. Prices, ratings and commissions are blank — not confirmed from an official source, never inferred.

## Site structure
- `/` — publication front page: hero, this week’s picks (product grid), buyer-question guides, how it works
- `/categories/air-fryers.html` — findings table, one row per product, source link per row
- `/dashboard.html` — entries/findings table + empty campaign ledger + measurement status
- `/guides/` — four question-shaped guides (working titles)
- `/suggestions.html` — decision suggestions; review before implementing
- `/reviews/flagged.html` — Flagged for Review page (irregularities + unverified items)
- `/disclosure.html` — full Associates statement
- `/privacy.html` — privacy notice for self-hosted analytics
- `/sitemap.xml`, `/rss.xml` — for search engines and feed readers

## Measurement (turned on before content)
Five defined events (canonical, src/data/events.json): `page_view`, `outbound_product_click`, `guide_read_75`, `compare_view`, `flag_page_view`. Self-hosted collector at `/analytics/collect` (code: `server/collect.js`); client degrades silently when unreachable. No cookies, no IP logging. Next guide topic chosen from measured queries.

## Campaign ledger
Empty and intentionally so. Entries (timestamp, source, channel, eligible sessions, clicks, reported orders, provenance report, notes) are added only from authorized first-party reports, with a dated provenance trail. No conversion score or revenue forecast is presented.

## Compliance gate
Disclosure above the fold on every page + footer repeat; `rel="nofollow sponsored"` on all outbound product links; review against Amazon Associates Operating Agreement and FTC endorsement guidance before publishing (see `PUBLISHING_WORKFLOW.md`).

## Flagged items
All five short links now resolve to product pages (re-verified 2026-11-20). Every observed ASIN differs from the 9-character short-link slug — intended and observed identifiers remain in separate fields and are never merged. Tracking attribution under shopnow047c-20 remains unconfirmed for all five (FLG-002). All flagged items are published on `/reviews/flagged.html` with source links; they do not block the launch.

## Next decisions awaiting review (`/suggestions.html`)
S-001 price/commission tracking · S-002 replace short links with validated Special Links · S-003 turn on real analytics · S-004 compliance gate in publishing workflow · S-005 brand imagery.
