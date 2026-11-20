# Affil1 — Executive summary

**Project:** Amazon affiliate marketing site (GitHub Pages)
**Branch:** `arena/982fea5a-affil1` (integration + verification pass, 2026-11-20)
**Tracking ID:** `shopnow047c-20`
**Prepared:** 2026-11-20

## What this is

A buyer-facing affiliate site for air fryers and multi-function kitchen
appliances. It reads like a shop/publication, not an audit: product picks lead
the front page, every page carries an above-the-fold disclosure, and every
outbound product link is marked `sponsored` (Special Link form:
`amazon.com/dp/<ASIN>?tag=shopnow047c-20`).

## Products submitted (5) — verified line by line against official Amazon pages

| # | Submitted link | Observed listing (official) | Status |
|---|---|---|---|
| 1 | https://link.amazon/B04G1MEwY | https://www.amazon.com/dp/B0CDY277D3 | Verified — title matches the register (P-01) |
| 2 | https://link.amazon/B02NbDxp3 | https://www.amazon.com/dp/B09B7SB46R | Verified — Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven (P-02) |
| 3 | https://link.amazon/B00hJ57DV | https://www.amazon.com/dp/B08DKYBTPH | Verified — Chefman Air Fryer 8 Qt TurboFry (P-03) |
| 4 | https://link.amazon/B0c8moW59 | https://www.amazon.com/dp/B0DHZTCNR5 | Verified — resolved on re-verification 2026-11-20; previously checkpoint-only (P-04) |
| 5 | https://link.amazon/B0f3GKalj | https://www.amazon.com/dp/B0DZFD6R9Z | Verified — CHEF iQ Sense wireless thermometer (P-05) |

Verification method: each submitted link was requested through the redirect, the
final URL read, the 10-character ASIN extracted from the `/dp/` segment, and the
page title transcribed and compared with the register (`src/data/products.json`).
All five match. No value was inferred or carried over from a search result. No
arrival URL carried the tracking tag — attribution remains unconfirmed (FLG-002).

**Intended ASIN vs observed.** `src/data/products.json` keeps
`intended_asin` (the owner's intent) and `observed_asin` (the 10-character ASIN
actually opened) as separate fields, never merged. All five `intended_asin`
values are null: the submitted codes are 9-character slugs, so the owner's intent
is not established beyond the observation; the 10-character `observed_asin` is
the checkable identifier. `data/confirmations.json` records, per submitted link:
the slug as `intended_asin`, the `official_listing_url`, `confirmation_date`,
`source`, and the `observed_redirect_target` in a separate field — the two are
never merged. (Interpretation question for the owner: is `intended_asin` as
stored — the slug — the right record of intent? See FLG-016 discussion in
COORDINATION.md and questions Q-01 on `/questions/`.)

## Site structure (root build — the live edition)

- `/` — publication front page: hero, this week's picks (product grid), buyer-question guides, how it works
- `/products/` — the product register: one row per product (P-01…P-05), source link per row
- `/products/p-01.html` … `/products/p-05.html` — per-product records
- `/compare/` — comparison table: five rows (four air fryers + the thermometer), seller-stated claims only
- `/guides/` — question-shaped buying guides (working hypotheses, not popularity claims)
- `/questions/` — open questions with the artefact that would close each one
- `/suggestions/` — decision suggestions; review before implementing
- `/review/` — Flagged for Review page (irregularities + unverified items), image policy, measurement plan
- `/operations/ledger.html` — campaign ledger (empty by design)
- `/about/`, `/brief/` — About this site, the brief
- `/sitemap.xml`, `/feed.xml`, `/rss.xml` — for search engines and feed readers

Root edition — not generated or validated by `tools/build.py` / `tools/check.py`
(foreign root-edition files served at the same paths; logged in COORDINATION.md):
`dashboard.html`, `categories/air-fryers.html`, `disclosure.html`, `privacy.html`.

## Products data rules

No price, star rating, review count or stock status appears anywhere on this
site: Amazon permits those only where Amazon serves the link carrying the data,
or via the Creators API / PA API (Program Policies §2(b), SRC-02). Neither path
is connected, and `tools/check.py` fails the build if a currency figure, a star
rating, a review count or a stock phrase is introduced.

## Compliance

Disclosure above the fold on every page (root build) and repeated in the footer;
the exact Associates sentence is enforced by `tools/check.py`. Every outbound
product link carries `rel="sponsored nofollow noopener"` and the tag
`shopnow047c-20`. Review against the Amazon Associates Operating Agreement and
FTC endorsement guidance before publishing (PUBLISHING_WORKFLOW.md).

## Toolchain (all run 2026-11-20)

- `python3 tools/build.py` — built 22 pages.
- `python3 tools/check.py` — **0 errors, 0 warnings** (disclosure on every page,
  sponsored on every outbound, no banned phrases, every link resolves).
- `python3 tools/validate.py` — **passes** (619 checks, 0 warnings).
  *Previously crashed with `KeyError: 'supplied_path_code_length'` — the
  validator expected the old schema while `src/data/products.json` uses the
  canonical register schema; aligned and re-run.*
- `python3 tools/stage.py _site` — staged.
- CI-style reproducibility diff (build twice, `diff -r` — clean).
- `python3 tools/verify_links.py` — appended 5 observations to
  `data/verification-observations.ndjson`; outcome `fetch_error` (bash `urllib`
  is blocked from this sandbox to amazon.com). The authoritative verification is
  the fetch_page table above.

## Analytics

The five canonical events from `src/data/events.json` are recorded by
`assets/js/analytics.js` (v2, rewritten this pass): `page_view`,
`outbound_product_click`, `guide_read_75`, `compare_view`, `flag_page_view`.
The client is inert until a page sets `window.CC_ANALYTICS_ENDPOINT` — nothing is
recorded or sent now (FLG-010). `tools/check.py` now enforces the canonical five
and fails on the legacy names.

## Flagged items

- **FLG-016 (new)** — two analytics systems named the five events differently;
  reconciled to the canonical five. Legacy duplicates: `analytics.js`,
  `js/analytics.js`, `js/events.js`, `assets/js/events.js`,
  `analytics/endpoint.py`, `server/collect.js`. The canonical collector design
  in `src/data/events.json` posts to endpoint `/api/e`; the rewritten client
  posts to `window.CC_ANALYTICS_ENDPOINT` (still inert: no endpoint deployed).
- All other fifteen flags (FLG-001…FLG-015) published on `/review/` with source
  links; none block the site from being live.

## Decisions the site is waiting on (questions and where the answers live)

1. **Intended ASIN semantics** (Q-01) — the register stores `intended_asin` = null; the slug lives in `data/confirmations.json`. Confirm intent reading.
2. **Tracking attribution** (Q-03, FLG-002) — no arrival page showed the tag. Only a click from the owner's device + the Associates click report confirms.
3. **P-04's identity** (Q-02, FLG-004) — the link never reached a product page; a browser session on the interstitial recovers it.
4. **The thermometer in the catalogue** (Q-06, FLG-015) — P-05 is a thermometer; routed to its own section.
5. **Prices / ratings / stock** (SRC-02) — not shown; would require the Creators API or PA API.
6. **Author identity** (Q-08, FLG-006) — not published; guides are questions only.
7. **Analytics collector hosting** (Q-07, FLG-009, FLG-010) — GitHub Pages cannot run the collector; needs a host.
8. **Search Console** (Q-11, FLG-011) — unverified.
9. **Commission rates** (Q-09, FLG-004, FLG-013) — behind an Associates sign-in.
10. **Buyer-intent/conversion tracking** (Q-14, FLG-014) — campaign ledger starts empty; no orders data exists.
11. **Topic choice from measured queries** (Q-07) — next guide topic needs Search Console + click data.

Full detail with source links: `/questions/` (15 questions + answers, some blocked on account access),
`/review/` (all flags with what-to-check links).

## Live

https://karagemop466-tech.github.io/Affil1/
