# Affil1 — Executive summary

**Project:** Amazon affiliate marketing site (GitHub Pages)
**Live URL:** https://karagemop466-tech.github.io/Affil1/
**Session:** `arena/ac649871-affil1` (base `ff74e5b`; rebased onto current `main`)
**Tracking ID:** `shopnow047c-20`
**Prepared:** 2026-11-20

## What this is
A buyer-facing affiliate publication and shop for countertop kitchen gear (air fryers, oven-style cookers, companion tools). It reads like a shop, not an audit: the verified shortlist leads the front page, question-first guides carry the editorial voice, and every compliance surface (disclosure, sponsored marking, flagged items, decision desk) stays one click away without ever being the headline.

## Products submitted (5) — verification pass of 2026-11-20
| # | Submitted link | Short-link slug | Verified official listing | Listing title (as served by amazon.com) | Status |
|---|---|---|---|---|---|
| 1 | https://link.amazon/B04G1MEwY | B04G1MEwY (9 chars — token, not an ASIN) | https://www.amazon.com/dp/B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven (Black) | Verified |
| 2 | https://link.amazon/B02NbDxp3 | B02NbDxp3 (token) | https://www.amazon.com/dp/B09B7SB46R | Emeril Lagasse 26QT French Door Air Fryer Toaster Oven | Verified |
| 3 | https://link.amazon/B00hJ57DV | B00hJ57DV (token) | https://www.amazon.com/dp/B08DKYBTPH | Chefman Air Fryer 8 Qt TurboFry 4-in-1 (Stainless Steel) | Verified |
| 4 | https://link.amazon/B0c8moW59 | B0c8moW59 (token) | — | — | Unverified — Amazon bot-checkpoint interstitial on repeated fetches |
| 5 | https://link.amazon/B0f3GKalj | B0f3GKalj (token) | https://www.amazon.com/dp/B0DZFD6R9Z | CHEF iQ Sense Smart Wireless Meat Thermometer (Gen3) | Verified |

Key facts, each checked against an official source:
- **Four of five links resolve live to official Amazon product pages** (independent fetches, 2026-11-20). Titles above are the exact listing titles served by amazon.com; source link for every row is on the storefront and in `data/confirmations.json`.
- **The submitted slugs are 9 characters; Amazon ASINs are 10-character identifiers** (SP-API Catalog Items reference). Slugs are recorded as opaque tokens — never treated as ASINs. Earlier sessions' "intended ASIN" labels are retained verbatim in the register with the format check beside them.
- **Observed redirect targets and official listing URLs are stored in separate fields and never merged.** Earlier observations that differ (homepage instead of product page) are preserved as history, not overwritten.
- **No prices, ratings, review counts or commission rates appear anywhere on the site**: Associates policy conditions price display on Amazon-served or API-served data, which this static build does not have. Nothing was inferred.

## Site structure (reader path → machinery path)
- `/` — shop front: hero, the shortlist (5 product cards with verification stamps), guide cluster, seasonal cluster (holiday counter math), "how we verify", decision-desk teaser
- `/guides/` — the notebook: seven question-shaped guides (format, capacity, cleanup, multi-function, accessories, running costs, holiday counter math) + this season's cluster
- `/suggestions.html` — the suggestions queue: 10 proposed changes with rationale, effort, dependencies, status and decision gates; nothing ships without a recorded decision
- `/questions.html` — the pre-decision list: seven questions with have/missing/answer/discovery for each
- `/executive-summary.html` and this file — the short version
- `/guides/flagged-for-review.html` — Flagged for Review: full verification register, FLG-001…012, official references
- `/dashboard.html`, `/categories/air-fryers.html`, `/reviews/flagged.html` — machinery pages (audit tables, ledger, findings)
- `/disclosure.html`, `/privacy.html` — compliance pages
- `/crisp/` — parallel session's publication section (untouched by this redesign)
- `/sitemap.xml`, `/rss.xml`, `/feed.xml`, `/robots.txt` — findability

## Measurement (machinery, gated)
Five defined events: `page_view`, `outbound_click`, `guide_read`, `suggestion_review`, `session_start`. Client collector: `assets/js/analytics.js` (localStorage-backed, silent-fail); endpoint code: `server/collect.js` and `analytics/endpoint.py` — **not deployed** (FLG-009). The outbound-click counter is wired to every sponsored product link. Ledger stays empty until authorized first-party reports exist.

## Campaign ledger
Empty and intentionally so. Columns: timestamp, source, channel, eligible sessions, clicks, reported orders, provenance report, notes. Entries are added only from authorized first-party reports with a dated provenance trail. No conversion score or revenue forecast is presented anywhere.

## Compliance gate
- Disclosure "As an Amazon Associate I earn from qualifying purchases." above the fold on every page + footer repeat (Operating Agreement §5; FTC Endorsement Guides).
- `rel="nofollow sponsored"` on every outbound product link; Associates tag `shopnow047c-20` appended per the Special Link format.
- Per-link tracking confirmation in the enrolled Associates workflow is **pending** (account access unavailable to this build) — flagged FLG-002/003, not asserted valid or invalid.
- Publishing gate checklist lives in `PUBLISHING_WORKFLOW.md`.

## Flagged items (published on `/guides/flagged-for-review.html`, none block launch)
FLG-001 slug-vs-ASIN format check · FLG-002 tag attribution unconfirmed · FLG-003 Special-Link status of `link.amazon` unresolved · FLG-004 commission rates behind sign-in · FLG-005 one checkpoint-gated link · FLG-006 no price/rating display without Amazon-served data · FLG-007 attributes beyond titles unverified · FLG-008 editorial titles are hypotheses · FLG-009 analytics endpoint not deployed · FLG-010 ledger empty by design · FLG-011 Search Console submission needs account access · FLG-012 email capture needs provider + privacy review.

## Next decisions awaiting review (`/suggestions.html`)
S-01 enrolled-workflow link test (blocked: account access) · S-02 scheduled re-verification · S-03 Search Console + sitemap submission (blocked: account access) · S-04 publishing cadence (two weeks per guide) · S-05 deploy self-hosted collector (blocked: privacy review) · S-06 ledger population from authorized reports · S-07 Amazon-served price data via SiteStripe/PA API · S-08 author bylines · S-09 pre-publish compliance checklist as blocking step · S-10 monthly query review → topic selection.

## Design notes (why it no longer reads like generated filler)
- One design system (`styles.css`), warm editorial palette, serif display type, consistent masthead/footer/disclosure on the whole reader path.
- Original illustration set (`assets/img/`) in a single style — clearly labeled as illustrations, never passed off as product photography.
- The front page leads with the shelf, the guides and the season — the verification machinery is reachable but never the headline.
- Catchy-but-honest article set: each guide targets a real buyer question; seasonal cluster (holiday counter math) gives the publication a calendar.
