# Affil1 — executive summary

**Project:** Amazon affiliate publication (static site, GitHub Pages)
**Branch:** `arena/2ed69be3-affil1` (integration pass, base `54b2b45` on `main`)
**Tracking ID:** `shopnow047c-20`
**Prepared:** 2026-11-20
**Live site:** https://karagemop466-tech.github.io/Affil1/
**Full version with tables:** `brief/index.html`

## What this is

A buyer-facing publication for three air fryers and two thermometers. It reads like a
shop, not an audit: the front page leads with the products, each product page says what
the thing is for and what to check before buying, and the verification machinery lives
behind the cards instead of in front of them.

## The five products, as verified on 2026-11-20

| # | Submitted link | Intended ASIN | Observed listing | Product | Status |
|---|---|---|---|---|---|
| P-01 | link.amazon/B04G1MEwY | — (not supplied) | [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) | CHEFMAN 6 qt dual-basket air fryer | Verified |
| P-02 | link.amazon/B02NbDxp3 | — | [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R) | Emeril Lagasse 26 qt French-door air fryer oven | Verified |
| P-03 | link.amazon/B00hJ57DV | — | [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH) | Chefman 8 qt TurboFry basket air fryer | Verified |
| P-04 | link.amazon/B0c8moW59 | — | [B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5) | ThermoMaven instant-read meat thermometer | Verified on the third attempt |
| P-05 | link.amazon/B0f3GKalj | — | [B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z) | CHEF iQ Sense wireless meat thermometer | Verified |

Intended ASIN and observed ASIN are separate fields and are never merged. Prices,
ratings, review counts and availability are blank everywhere: Amazon permits them only
from data Amazon serves or via its API, and neither is connected.

## What changed in this pass

1. **Tagged Special Links.** Policy §2(b) requires the Associates ID as a URL parameter.
   The previous build linked to bare `/dp/` addresses; every product link is now
   `/dp/ASIN?tag=shopnow047c-20` (FLG-016).
2. **P-04 corrected.** A third request resolved it. The stale "unresolved" copy is gone
   from the product record and the history is kept in FLG-004.
3. **Front page rebuilt** as a publication front page: hero, four decision paths, the
   five products, a feature guide, a season band, and three checkable claims.
4. **Guides clustered** into shape, size, upkeep and thermometers, with a fifth guide
   added for thermometers because two of five products are thermometers.
5. **One site to index.** The superseded parallel edition is marked `noindex` and kept
   out of the sitemap rather than deleted (FLG-018).
6. **Suggestion board rebuilt** as a decision tool: 15 proposals, 7 implemented, each
   with effort, risk, evidence, dependencies and accept/hold/reject.
7. **Question register rebuilt**: 16 questions, 6 answered with a source, 6 blocking,
   plus five concrete ways to discover the missing information.

## Measurement

Five events are defined in `assets/js/analytics.js`: `page_view`, `guide_open`,
`outbound_click`, `search_query_referral`, `report_import`. The client is inert until a
first-party endpoint is configured; none is deployed, because GitHub Pages cannot run a
collector. No cookie, no storage, no identifier, no third party. The campaign ledger is
empty with a defined schema and a provenance rule (FLG-017).

## Compliance gate

- Disclosure strip under the masthead on every page, repeated in the footer, worded as
  the Operating Agreement §5 requires.
- Every Amazon product link: `rel="sponsored nofollow noopener"`, new tab, tagged.
- `tools/check.py` fails the build on a missing disclosure, an unmarked product link, a
  price or rating phrase, a test claim, a broken link, a root-absolute link, or a commerce
  link without `?tag=shopnow047c-20`. That last rule caught twelve untagged evidence links
  on the day it was added.

## Still unknown (published, not hidden)

Six blocking questions: is the tracking ID active; does a click register; what was the
intended ASIN for each link; is the account in the right marketplace; is API/image access
available; what search demand exists. Twenty-one items are flagged on `review/index.html`,
including the unresolved compliance status of `link.amazon` short links — which this site
does **not** claim are invalid (FLG-003) — and a new one, FLG-021: a parallel session recorded
the opposite destinations for the two thermometer links, so this page shows both claims and
says the conflict is unresolved rather than picking the tidier one.

## Decisions waiting for you

`suggestions/index.html` — approve, hold or reject each of the 8 open proposals. The two
cheapest: click one link and find it in the report (S-02); ask Amazon support three
questions in writing (S-15).
