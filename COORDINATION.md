# COORDINATION.md — shared task board

Shared task board for parallel sessions on this repository.

## Session log

| Session | Branch | Claimed scope | Status |
|---|---|---|---|
| `arena/fa9307f7-affil1` | `arena/fa9307f7-affil1` | Full rewrite: `index.html`, `guides/`, `products/`, `compare/`, `questions/`, `suggestions/`, `review/`, `about/`, `operations/`, `brief/`, `assets/`, `src/data/`, `tools/`, `README.md` | done |

No other session had an open claim on these files when this work started. Two
other branches have open pull requests (#6 `arena/55d40788-affil1`, #7
`arena/96012762-affil1`). Neither was modified, rebased or force-pushed.

## Claims

| Task | Status | Owner | Files |
|---|---|---|---|
| Publication rewrite, editorial guides, decision pages, review queue | done | arena/fa9307f7-affil1 | `index.html`, `guides/`, `products/`, `compare/`, `questions/`, `suggestions/`, `review/`, `about/`, `operations/`, `brief/` |
| Link verification against the live Amazon listing | done | arena/fa9307f7-affil1 | `src/data/products.json`, `review/` |
| Build system, checker, Pages workflow | done | arena/fa9307f7-affil1 | `tools/`, `.github/workflows/pages.yml` |
| Product facts beyond the listing title | needs review | — | `src/data/products.json` |
| Associates account data (intended ASINs, rate card, click report) | needs review | — | requires account owner |

`needs review` means the item is published on the review page and does not block
anything.

## Overlap with the other open branches

Two sibling branches worked the same brief at the same time. This session did not
merge them, because the three designs conflict structurally:

- `arena/96012762-affil1` (#7) writes **root-absolute** internal links
  (`href="/about/"`). On a project Pages path that resolves to
  `karagemop466-tech.github.io/about/` and 404s. It also publishes every page at
  both `/compare` and `/compare/index.html`.
- Both sibling branches use a different brand name and a different URL layout.

What was **reused as corroboration, not copied**: PR #7 independently opened the
same five links and reached the same four ASINs recorded here. That agreement is
noted in `review/index.html#FLG-008` because independent confirmation of the same
observation is worth something, while a shared assumption would not be.

Branch `arena/55d40788-affil1` (#6) ships an analytics client and a self-hosted
collector. The analogue in this tree (`assets/js/analytics.js`) was written for
this build; it is inert and documented at `review/measurement.html`.

## Sources and verification performed

Every source was requested and read in this session on 2026-11-20.

| Ref | Source | Used for |
|---|---|---|
| SRC-01 | https://affiliate-program.amazon.com/help/operating/agreement | §5 disclosure wording, quoted verbatim |
| SRC-02 | https://affiliate-program.amazon.com/help/operating/policies | §2(b) Special Links and the price/availability rule |
| SRC-03 | https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | Disclosure placement |
| SRC-04 | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255 | The regulation behind SRC-03; linked, not quoted |
| SRC-05 | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | `rel="sponsored"` is the documented paid-link marker |

Link verification, performed once per link on 2026-11-20:

| Ref | Submitted | Resolved to | Product |
|---|---|---|---|
| P-01 | link.amazon/B04G1MEwY | ASIN B0CDY277D3 | CHEFMAN 6 qt dual basket air fryer |
| P-02 | link.amazon/B02NbDxp3 | ASIN B09B7SB46R | Emeril Lagasse 26 qt French door air fryer oven |
| P-03 | link.amazon/B00hJ57DV | ASIN B08DKYBTPH | Chefman 8 qt TurboFry |
| P-04 | link.amazon/B0c8moW59 | **not resolved** | three attempts, continuity page each time |
| P-05 | link.amazon/B0f3GKalj | ASIN B0DZFD6R9Z | CHEF iQ wireless meat thermometer |

`python3 tools/check.py` → **22 pages, 0 errors, 0 warnings.**

## Irregularities

All 15 are published at `review/index.html` with source links. The three that
matter most:

- **FLG-001** — all five submitted codes are 9 characters; all four ASINs on
  arrival are 10. They are short-link slugs, not identifiers, so `intended_asin`
  is null rather than filled with the slug.
- **FLG-002** — no arrival page showed a tracking tag, so attribution to
  `shopnow047c-20` is unconfirmed. Not the same as untagged.
- **FLG-005** — no price, rating, review count or stock anywhere, by rule, with
  the policy quote on the sources page.


- Pull request and merge result: recorded in the PR body and below.
- GitHub Pages: https://karagemop466-tech.github.io/Affil1/

## Merge log

Rebased onto `main` after PRs #18, #20 and #21 merged a parallel edition that had
already adopted this branch's verified link table. Both editions agree on every
product fact:

| Ref | Observed ASIN | Both editions agree |
|---|---|---|
| P-01 | B0CDY277D3 | yes |
| P-02 | B09B7SB46R | yes |
| P-03 | B08DKYBTPH | yes |
| P-04 | unresolved | yes |
| P-05 | B0DZFD6R9Z | yes |

The conflict was structural, not factual: both trees write `index.html`,
`sitemap.xml`, `feed.xml`, `assets/css/` and `src/data/*.json`. This branch's
build owns those paths.

**Nothing was deleted from another session's work.** Their pages (`crisp/`,
`guides.html`, `products.html`, `dashboard.html`, `flagged-for-review.html`,
`reviews/`, `categories/`, `archive/`, `data/`, `js/`, `css/`, `server/`,
`analytics/`, `docs/`) are all still in the tree and still served.
`tools/build.py` now writes only the files in its own `GENERATED` set and will
not touch anything else; that was verified by dropping a foreign file into
`guides/` and rebuilding.

One file is retired: `guides/flagged-for-review.html` moves to `review/`. A
redirect stub could not be added because this build cannot hand-write HTML; the
front page and footer no longer link to the old path.

Duplicate root pages remain: this build serves `products/`, `questions/` and
`suggestions/` as directories while the parallel edition serves `products.html`
and siblings. The front page and footer link only to this build's set.
Consolidating the two editions is a design decision and is logged as the next
integration task rather than done here by deletion.

## Session S-8206a8d0 — polished shop front page + verification pass (2026-11-20)

Owner: S-8206a8d0 on branch `arena/8206a8d0-affil1`. Scope (non-overlapping with prior sessions' done work):
- `src/data/products.json` (P-04 re-verification), `data/confirmations.json`, `data/verification-audit.json` (append OBS-6..OBS-10)
- Root storefront polish: `index.html`, `assets/css/main.css`, `assets/js/analytics.js`, `assets/js/common.js`
- Broken-link + disclosure fixes: `guides.html`, `dashboard.html`, `categories/air-fryers.html`, `products.html`, `questions.html`, `suggestions.html`, `guides/*.html` (static disclosure + sponsored source links)
- New guides: `guides/meal-prep-sunday.html`, `guides/small-kitchen-counter.html`, `guides/thermometer-pairing.html`
- Findability: `sitemap.xml`, `rss.xml`, `feed.xml`, `robots.txt`, `EXECUTIVE_SUMMARY.md`, `executive-summary.html`
- Integration: rebuild `crisp/` via `tools/build.py`, run `tools/validate.py`, PR + merge + Pages verify

| Task | Status | Notes |
| --- | --- | --- |
| SG-31 Re-verify 5 links via official Amazon pages (fetch_page, 2026-11-20) | done | P-01..P-03,P-05 confirmed; P-04 now resolves to B0DHZTCNR5 (was checkpoint). Root dashboard (2 verified) is stale — canonical is src/data/products.json. |
| SG-32 Rebuild root landing as publication front page leading with products | done | Current index.html has duplicated/malformed sections (stray </div>, two product grids, two guide grids). |
| SG-33 Fix guides.html ../ paths (22 broken refs) + static disclosure everywhere | done | guides.html sits at root but uses ../ paths. |
| SG-34 Unify root tables to canonical 5-product register; outbound = dp+tag Special Links | done | No prices/ratings published (Program Policies 2(b)). |
| SG-35 Add 3 trendy seasonal guides + wire sitemap/feed/nav | done | Question-shaped, no popularity claims. |
| SG-36 Analytics: remove localStorage, align 5 events, SEO/canonical/OG/JSON-LD | done | Endpoint stays self-hosted, inert until deployed (FLG-009). |
| SG-37 Validate, build crisp, PR, merge, Pages deploy | in progress | Do not merge broken site. |

Verification (S-8206a8d0, 2026-11-20, via fetch_page against amazon.com official pages):
- https://link.amazon/B04G1MEwY -> https://www.amazon.com/dp/B0CDY277D3 CHEFMAN 6 Quart Dual Basket (title matches src/data P-01)
- https://link.amazon/B02NbDxp3 -> https://www.amazon.com/dp/B09B7SB46R Emeril Lagasse 26QT French Door (matches P-02)
- https://link.amazon/B00hJ57DV -> https://www.amazon.com/dp/B08DKYBTPH Chefman Air Fryer 8 Qt TurboFry (matches P-03; contradicts root dashboard homepage claim)
- https://link.amazon/B0f3GKalj -> https://www.amazon.com/dp/B0DZFD6R9Z CHEF iQ Sense thermometer (matches P-05; contradicts root dashboard homepage claim)
- https://link.amazon/B0c8moW59 -> https://www.amazon.com/dp/B0DHZTCNR5 ThermoMaven 1 Sec Professional Digital Meat Thermometer (NEW: previously checkpoint-only; now product page. Updates FLG-005/FLG-014 from unresolved to observed.)
- Policies re-checked: https://affiliate-program.amazon.com/help/operating/policies (Updated April 14, 2026) and FTC Endorsement Guides FAQ — both reachable, consistent with src/data/compliance.json S01-S13.
- Tracking tag shopnow047c-20 was NOT observed in any resolved URL; attribution remains unconfirmed (FLG-002 stands). Short-link compliance remains unresolved (FLG-003 stands); no link declared invalid.

### Delivery — S-8206a8d0 (2026-11-20)

- Re-verified all 5 links against amazon.com (fetch_page): P-01 B0CDY277D3, P-02 B09B7SB46R, P-03 B08DKYBTPH, P-04 B0DHZTCNR5 (newly resolved), P-05 B0DZFD6R9Z. Updated `src/data/products.json`, `src/data/flags.json` (FLG-005/014 resolution), `data/confirmations.json`, `data/verification-audit.json` (OBS-6..8).
- Rebuilt root landing as publication front page leading with products (5 cards, tagged Special Links `amazon.com/dp/<ASIN>?tag=shopnow047c-20`, `rel="sponsored nofollow noopener"`, no prices/ratings). Fixed malformed duplicate sections in old index.html.
- Fixed `guides.html` 22 broken `../` refs; added static disclosure strip to JS-only pages; added canonicals; fixed `disclosure.html#why-blank` anchor; unified dashboard/categories/products/questions/suggestions/flagged tables to canonical register.
- Added 3 trendy question-shaped guides: meal-prep-sunday, small-kitchen-counter, thermometer-pairing (+ holiday-hosting wired). Updated sitemap.xml, rss.xml, feed.xml, robots.txt, guides/index.
- Analytics: removed localStorage (now in-memory only, DNT/GPC honoured), aligned to canonical 5 events (page_view, outbound_product_click, guide_read_75, compare_view, flag_page_view). Endpoint remains self-hosted/inert (FLG-009).
- Crisp edition: updated `tools/build.py` outbound to tagged Special Links, products/compare to 5, rebuilt `crisp/` (619 validate checks pass).
- Checks: 0 broken internal refs (excl. archive), disclosure on every root page, 0 unsponsored dp links, 0 published prices, XML parses, `tools/validate.py` 619/619 pass.
- Remaining blocked (unchanged): FLG-002 tracking attribution, FLG-003 short-link compliance, FLG-004 rates, FLG-006 prices (rule), FLG-009 collector hosting, FLG-011 Search Console, FLG-012 email, FLG-013 author. All published on Flagged for Review; none block merge.

### Rebase log — S-8206a8d0 onto PR #22 (2026-11-20)

`origin/main` advanced to PR #22 (`arena/fa9307f7-affil1`, full Crisp & Counter rewrite owning root `index.html`, `tools/build.py`, `src/data/*`, `sitemap.xml`/`feed.xml`, `.github/workflows/pages.yml`). Rebased `arena/8206a8d0-affil1` onto it; 9 conflicts resolved without discarding either session's work:

- Kept PR #22 versions for: `index.html`, `tools/build.py`, `.github/workflows/pages.yml`, `assets/js/analytics.js`, `feed.xml`, `sitemap.xml`, `guides/index.html` (generated files; hand-edits would fail the reproducibility check). Our Good Measure landing (commit a90a8ea) is superseded at root by the Crisp & Counter front page, which satisfies the same brief (shop-like, products-led, disclosure above fold). Preserved in git history; parallel-edition pages (`dashboard.html`, `products.html`, `guides.html`, `crisp/`, `reviews/`, `categories/`) are untouched by that build and survive.
- Ported our P-04 re-verification (B0DHZTCNR5) into PR #22's `src/data/products.json` schema (ref/observed_asin), updated FLG-001/FLG-002 counts and `tools/content.py` copy (four→five), rebuilt: `tools/check.py` 22 pages, 0 errors.
- Kept our additive work: 3 new guides (`guides/meal-prep-sunday.html`, `small-kitchen-counter.html`, `thermometer-pairing.html` — not in GENERATED set, survive rebuild), `guides.html` path fixes, dashboard/categories/products/questions/suggestions/flagged unification, `data/*` audit appends, `crisp/` P-04 sync.
- Follow-up (not done by deletion): wiring the 3 new guides into the generated sitemap/feed requires extending PR #22's `tools/content.py` GUIDES; logged here for the integration session.

## Session `arena/b6e07e37-affil1` — 5/5 reconciliation, category subpages, USDA-sourced guides & final verification (2026-11-20)

Owner: `arena/b6e07e37-affil1` on branch `arena/b6e07e37-affil1` (rebased onto `main` at `0691fa7`).

Claimed scope (non-overlapping with prior done work; preserves all parallel-edition files untouched):
- `src/data/products.json`, `src/data/flags.json`, `src/data/questions.json`, `src/data/suggestions.json`, `src/data/sources.json`, `src/data/images.json`, `src/data/events.json`
- `tools/build.py`, `tools/content.py`, `tools/layout.py`, `tools/page_home.py`, `tools/page_products.py`, `tools/page_compare.py`, `tools/page_guides.py`, `tools/page_questions.py`, `tools/page_review.py`, `tools/page_suggestions.py`, `tools/page_desk.py`, `tools/check.py`
- `assets/css/site.css`, `assets/img/instant-thermometer*.jpg`
- Generated outputs in `GENERATED` (`index.html`, `404.html`, `guides/`, `products/`, `compare/`, `questions/`, `suggestions/`, `review/`, `about/`, `operations/`, `brief/`, `sitemap.xml`, `feed.xml`, `robots.txt`)
- `EXECUTIVE_SUMMARY.md`, `README.md`, `COORDINATION.md`

| Task | Status | Owner | Notes |
|---|---|---|---|
| INT-01 Re-verify all 5 Amazon links & official sources (Amazon Policies, FTC, eCFR, Google, USDA FSIS) | in progress | arena/b6e07e37-affil1 | All 5 links verified (3 Air Fryers + 2 Meat Thermometers); USDA FSIS now reachable and verified |
| INT-02 Reconcile Crisp & Counter templates & data with 5/5 two-category reality + render product-intent confirmation table | in progress | arena/b6e07e37-affil1 | Fixes stale 4/5 copy, adds `products/air-fryers.html` & `products/thermometers.html`, renders `FIELDS` table on product pages |
| INT-03 Add 3 new question-shaped guides (incl. USDA-verified thermometer/temp guide) wired into `tools/content.py`, `sitemap.xml`, `feed.xml` | in progress | arena/b6e07e37-affil1 | Uses fresh slugs; leaves S-8206a8d0 standalone guides untouched |
| INT-04 Generate P-04 instant-read illustration, update `EXECUTIVE_SUMMARY.md`, run `build.py` + `check.py` + live preview QA, PR + merge + verify Pages | in progress | arena/b6e07e37-affil1 | Reproducibility & 0-error check required before merge |

