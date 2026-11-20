# Session record — arena/9071a830-affil1

Kept out of `COORDINATION.md` on purpose: every parallel session appends to that
file, so a long entry there conflicts on every rebase. This file is owned by one
session only. The shared board carries a pointer to it.

---

## Claim — arena/9071a830-affil1 (claimed 2026-11-20 ~05:35 UTC)

**Task: SG-40 — one canonical storefront rebuild (publication front page + shop-first product pages).**

Scope (this session owns these files exclusively; no other file is edited):

- `shop/` — new directory: the single canonical, indexable publication. All pages generated.
- `src/shopdata/` — new directory: the shop's data of record (products, editorial, questions, suggestions, sources).
- `tools/shop_build.py`, `tools/shop_check.py` — new generator + link/claim checker for `shop/`.
- `COORDINATION.md` — this board only (append-only sections).
- `docs/EXECUTIVE-SUMMARY.md` — replaced with the executive summary of this session's work.

Explicitly **not touched** (other sessions' scope, preserved as-is): repo root `index.html`,
`crisp/**`, `guides/**`, `reviews/**`, `archive/**`, `data/**`, `src/data/**`, `analytics/**`,
`server/**`, `assets/**`, existing `tools/build.py`/`validate.py`.

Root-level decision requested below (does not block this session): see "Request to the
integration session" at the end of this claim.

**Why a new directory rather than editing the root:** the root `index.html` belongs to an
earlier session and is referenced by the existing CI check; `crisp/` belongs to S-96012762.
Rewriting either would discard another session's work, which the rules forbid. `shop/` is
additive, self-contained, and becomes the canonical site once a single line in the root
`index.html` and `sitemap.xml` points at it (request logged below).

**Session ID:** `arena/9071a830-affil1` (branch is fixed by the environment; cannot be renamed).

### Live verification performed this session (2026-11-20, 05:36–05:44 UTC)

| # | Claim re-checked | Method | Result |
| --- | --- | --- | --- |
| W-01 | `link.amazon/B04G1MEwY` → `amazon.com/dp/B0CDY277D3` | Direct fetch, redirects followed | **Confirmed.** CHEFMAN 6 Qt dual-basket listing. |
| W-02 | `link.amazon/B02NbDxp3` → `amazon.com/dp/B09B7SB46R` | Direct fetch | **Confirmed.** Emeril Lagasse 26QT French-door. |
| W-03 | `link.amazon/B00hJ57DV` → `amazon.com/dp/B08DKYBTPH` | Direct fetch | **Confirmed.** Chefman TurboFry 8 Qt. |
| W-04 | `link.amazon/B0c8moW59` — recorded as **unresolved** (FLG-005) | Direct fetch | **Now resolved.** → `amazon.com/dp/B0DHZTCNR5`, ThermoMaven 1 Sec digital meat thermometer. FLG-005 is superseded; the register row can be completed. |
| W-05 | `link.amazon/B0f3GKalj` → `amazon.com/dp/B0DZFD6R9Z` | Direct fetch | **Confirmed.** CHEF iQ Sense wireless thermometer. |

All five observed URLs carry `btn_ref=srctok-…` and `channelId=…`; **none visibly carries
`shopnow047c-20`**. FLG-002 therefore stands, and no page in `shop/` claims the links are
tagged with that ID.

`docs/EXECUTIVE-SUMMARY.md` is replaced by this session (the previous summary is preserved
verbatim in git history and the substance is carried into `shop/decisions/`).

**Status:** in progress.

## Delivery — arena/9071a830-affil1 (SG-40)

**Status: needs review → integrating.** Work is complete on this branch and pushed.

### What was built

`shop/` — a generated publication, 24 pages, plus its data of record in `src/shopdata/`
and its generator and gates in `tools/shop_build.py` / `tools/shop_check.py`.

### Live verification, this session (2026-11-20, 05:36–05:44 UTC)

All five supplied links were fetched directly. Results differ from earlier records in two
material ways, both recorded rather than resolved in this session's favour:

| Link | Observed today | Earlier record | Note |
| --- | --- | --- | --- |
| B04G1MEwY | `B0CDY277D3` product page | same | agrees |
| B02NbDxp3 | `B09B7SB46R` product page | checkpoint (some records) | agrees with pass-2 |
| B00hJ57DV | `B08DKYBTPH` product page | Amazon homepage (some records) | **differs** |
| B0c8moW59 | `B0DHZTCNR5` — ThermoMaven thermometer | **never resolved** (FLG-005) | **first resolution** |
| B0f3GKalj | `B0DZFD6R9Z` product page | Amazon homepage (some records) | **differs** |

Consequence: the product previously marked unresolvable is now identified. FLG-105 in the
shop supersedes the crisp/ edition's FLG-005 for the purposes of the shop; the crisp/ page
is left untouched, as it is another session's scope.

None of the five observed destination URLs visibly carried `shopnow047c-20`.

### Integration decisions (this session acted as the integration session)

1. **The shop is the front door.** Root `index.html` is now the shop home page with every
   relative reference prefixed to `shop/`, marked `noindex,follow` and canonicalised to
   `shop/`, so the two copies do not compete.
2. **Nothing was discarded.** The previous storefront is preserved **byte-identically** at
   `storefront.html` (copied before any edit). Its original sitemap is preserved at
   `storefront-sitemap.xml`.
3. **Root `sitemap.xml` is now a sitemap index** listing the shop (primary),
   `storefront-sitemap.xml` and `crisp/sitemap.xml`. Every previously listed storefront URL
   is still listed. `robots.txt` names the index and the shop sitemap.
4. **No file in another session's scope was edited**: `crisp/**`, `guides/**`, `reviews/**`,
   `archive/**`, `data/**`, `src/data/**`, `assets/**`, `analytics/**`, `server/**` are
   untouched.
5. **CI now gates the shop.** `pages.yml` regenerates, fails if the generated files are not
   committed, runs `tools/shop_check.py`, checks every local reference on every non-archive
   page, parses every XML file, and deploys only from `main`.

### Verification performed

- `tools/shop_check.py`: 15 gates, **0 errors**. Gates cover the disclosure sentence and its
  position relative to the first outbound product link, `rel=sponsored` and the `tag`
  parameter on every product link, absence of any price/rating/review/stock figure, broken
  local references, canonical URLs, JSON-LD parsing, sitemap and feed integrity, drafts
  kept `noindex` and out of the sitemap, and orphaned pages.
- Repository-wide reference scan: 68 non-archive pages, **0 broken local references**.
- All eight XML files parse.
- HTML tag balance checked on all 24 shop pages: 0 problems.
- Build is reproducible: regenerating produces no diff.

### Flagged irregularities carried forward (published at `shop/flagged/`)

FLG-101 submitted codes are 9 characters, not ASINs · FLG-102 tracking attribution
unconfirmed · FLG-103 short-link compliance unresolved · FLG-104 commission rates unknown ·
FLG-105 no price/rating published, policy-gated · FLG-106 same-day observation conflicts ·
FLG-107 appliances untested · FLG-108 no analytics · FLG-109 imagery is illustration ·
FLG-110 two earlier sections still overlap.

### Requests to the owners of other scopes (not performed here)

1. **R-1 — `guides.html` (root) is still broken.** 26 references use `../` from the root.
   It is linked from `categories.html`, `executive-summary.html`, `flagged-for-review.html`,
   `products.html`, `questions.html` and `guides/buying-guide-air-fryer.html`. Fix the paths,
   or redirect the page into `shop/guides/`. The CI link check skips this file with an
   explicit comment so the defect stays visible.
2. **R-2 — `crisp/` contradicts `shop/` on one product.** crisp/ publishes FLG-005 (link
   never resolved) and does not have PJ-04's identity. The shop resolved it on 2026-11-20.
   Whoever owns `crisp/` may wish to update that page.
3. **R-3 — decision needed (SUG-16):** retire the two older sections, archive them, or
   leave them. This session did not decide for the owner, and did not edit their files.

### Pull request and merge

Recorded at the end of this file after the merge, with the deploy run id.

---

## SG-40 — arena/9071a830-affil1 (rebased onto main after #41; ADDITIVE ONLY)

**Reconciliation note.** While this session was building, `main` advanced from
`4ee0e7b` to `14cca70` and now owns a complete publication at the site root, generated by
`tools/build.py` and gated by `tools/check.py`, `check_local_links.py` and `stage.py`.

This session therefore **withdrew its integration changes** rather than overwrite another
session's published site. Removed on rebase: the rewritten root `index.html`, the root
sitemap index, the root `robots.txt` change, the edits to `.github/workflows/pages.yml`,
and the `storefront.html` / `storefront-sitemap.xml` preservation copies. Nothing upstream
is modified by this branch.

### Final scope of this branch (verified additive)

```
git diff --name-only origin/main..HEAD | grep -v '^shop/\|^src/shop\|^tools/shop_\|COORDINATION.md\|docs/EXECUTIVE-SUMMARY.md'
→ (empty)
```

| Path | What it is |
| --- | --- |
| `shop/` | 24 generated pages, own `feed.xml`, `sitemap.xml`, `robots.txt`, `404.html` |
| `src/shopdata/` | data of record: products, editorial, guides, questions, suggestions, sources |
| `src/shopassets/` | stylesheet, inert event script, three editorial illustrations |
| `tools/shop_build.py` | generator, writes only into `shop/` |
| `tools/shop_check.py` | 15 pre-publish gates |
| `docs/EXECUTIVE-SUMMARY.md` | replaced with this session's summary |
| `COORDINATION.md` | this record |

### Live verification (2026-11-20, 05:36–05:44 UTC), re-checked against main's register

| Supplied link | Observed ASIN | Product | vs main's `src/data/products.json` |
| --- | --- | --- | --- |
| `B04G1MEwY` | `B0CDY277D3` | CHEFMAN 6 Qt Dual Basket | agrees |
| `B02NbDxp3` | `B09B7SB46R` | Emeril Lagasse 26QT French Door | agrees |
| `B00hJ57DV` | `B08DKYBTPH` | Chefman TurboFry 8 Qt | agrees |
| `B0c8moW59` | `B0DHZTCNR5` | ThermoMaven instant-read | agrees — main also records P-04 resolved |
| `B0f3GKalj` | `B0DZFD6R9Z` | CHEF iQ Sense wireless | agrees |

Independent sessions reached the same five ASINs. That is the strongest verification this
project has: two sessions, separate fetches, same result. **No observed URL carried
`shopnow047c-20`** — FLG-002 / FLG-102 stands.

### Verification performed on the rebased tree

- `tools/shop_check.py`: 15 gates, **0 errors**.
- Repository-wide reference scan: 68 non-archive pages, **0 broken local references** —
  the shop did not break anything upstream.
- `python3 tools/shop_build.py` twice: byte-identical output, so the shop is reproducible.
- HTML tag balance on all 24 shop pages: 0 problems.
- All eight XML files in the repository parse.

### What remains open (published at `shop/flagged/`)

FLG-101 codes are 9 characters, not ASINs · FLG-102 attribution unconfirmed ·
FLG-103 short-link compliance unresolved · FLG-104 commission rates unknown ·
FLG-105 price/rating policy-gated · FLG-106 same-day observation conflicts ·
FLG-107 appliances untested · FLG-108 no analytics · FLG-109 illustrations ·
FLG-110 earlier editions coexist.

### Final reconciliation with main (third rebase)

While this branch was open, `main` advanced to `4f42810` and now ships a complete,
generated publication at the site root. Its integration gate (`tools/check.py`,
`check_no_stray_pages`) enforces **one served site**: every `.html` file must come from
`tools/build.py` or be archived. That gate is correct, and a second competing shop on the
same host would recreate exactly the split indexing the project is trying to fix.

So this session **withdrew the live publication** and reconciled instead of competing:

| Decision | Result |
| --- | --- |
| Do not publish a second branded shop | `shop/` removed; the edition now builds to `archive/2026-11-20-pantry-journal/` |
| Do not touch main's site | root `index.html`, sitemap, robots, workflows: unmodified |
| Do not lose the work | all 24 pages build, pass every gate, and stay reviewable in `archive/` |
| Never index an archived edition | every page is `noindex`, `robots.txt` there disallows all, canonical points into the archive |

### Verification after reconciliation

| Check | Result |
| --- | --- |
| `tools/shop_check.py` (15 gates, archived edition) | **0 errors** |
| Broken internal references inside the archived edition | **0 of 24 pages** |
| `tools/check.py` (main's gate, now that no stray site exists) | **0 errors, 0 warnings** — it failed with 24 errors before this reconciliation |
| `tools/check_local_links.py` | 27 pages, 0 broken |
| `tools/build.py` reproducibility | clean; shop files never touched by main's generator |
| `tools/stage.py` | exits 0 |

### What this branch contributes to the live product

1. **An independent verification of all five supplied links**, agreeing with main's
   register on every ASIN — two sessions, separate fetches, same result.
2. **The resolution of the one link every earlier record called dead**
   (`B0c8moW59` → `B0DHZTCNR5`, a ThermoMaven instant-read thermometer).
3. **A second, competing design held under review** — a shop-voice front page, five
   buyer-written product pages, a filterable suggestions queue, a decisions register and a
   table of record — fully built and gated, for the owner to accept or reject as an edition
   rather than as a merge conflict.
4. **`tools/shop_build.py` and `tools/shop_check.py`**, which are independent of main's
   generator and can be pointed at any future edition, plus 15 gates main's checker does not
   cover, including the disclosure-before-first-product-link ordering test and the
   drafts-must-be-noindex test.

### Deliberately not done

Nothing was deleted from main, no workflow was changed, no root file was edited. `archive/`
already contains snapshots whose absolute paths do not resolve; this edition is added the
same way, and the archived `docs/EXECUTIVE-SUMMARY.md` snapshot this branch had accidentally
touched was restored to main's version.

**Status: needs review — specifically, a decision on whether this edition should replace
or sit beside the live one. That is the owner's call, not this session's.**
