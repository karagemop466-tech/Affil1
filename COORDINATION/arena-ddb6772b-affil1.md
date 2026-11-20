# Session log — `arena/ddb6772b-affil1` · 2026-11-20 UTC

Branch: `arena/ddb6772b-affil1`, rebased onto `origin/main` at `d345cf0`, then through
`3d2a453` (PR #108) mid-work. Claim committed before any site file was touched.

## Scope delivered

1. `/categories/` index + `air-fryers` + `thermometers` subpages.
2. Four new reader-facing guides with per-row official sourcing.
3. One false compliance sentence on every guide page, repaired and made computed.
4. Register updates: 6 sources, 3 questions, 6 suggestions, 3 flags, 6 observation rows.
5. Executive summary counts corrected and an addendum added.
6. Front-page seasonal band and journal shelf derived from data instead of list indices.

## Method, and the limits of it

* Every factual figure in the new editorial copy is transcribed from a page this
  session opened on 2026-11-20, and each guide carries a table whose rows link to that
  page, so a claim and its document sit in the same row. Sources: FSIS Safe Minimum
  Internal Temperature Chart (dated Apr 14 2025), FSIS Food Thermometers (no date shown),
  FSIS Leftovers and Food Safety (dated Jul 31 2020), FSIS Turkey from Farm to Table (no
  date shown), FoodSafety.gov temperature chart (dated Nov 21 2024), Amazon Associates
  Operating Agreement §5 and Program Policies (Commission Income Statement §2(g),
  Participation Requirements §1).
* Product capability sentences use only wording already transcribed in
  `_src/data/products.json`, attributed to the listing. Nothing was inferred.
* No price, rating, review count, availability, test result or ranking. A listing page
  read during verification displayed prices and star figures; neither was transcribed.
* `_data/verification-observations.ndjson` rows record observations, not confirmations.

## Findings

| ID | Finding | State |
|---|---|---|
| FLG-029 | All five submitted `link.amazon/<code>` links resolved to the Amazon homepage when this session followed them, in five separate fetches. Direct fetch of `amazon.com/dp/B0CDY277D3` in the same session matched the register title. | Open. No published destination uses a short link, so readers are unaffected; the intended-ASIN chain is not established. |
| FLG-030 | Nine modules in `_tools/` are unreachable from `_tools/build.py` and from every workflow (`buyer_guides`, `content_extra`, `extra_pages`, `page_sources`, `preview`, `quarantine_legacy`, `shop_build`, `shop_check`, `verify_links`). `research_brief.py` is wired into `editorial.yml` and `arm_links.py` is an owner CLI, so neither is counted. `extra_pages.py` also links to `/_src/data/reverification.json` with a root-absolute URL that would 404 on a project-pages host. | Open. Nothing published changes; the risk is a future session editing a file that publishes nothing. |
| FLG-031 | Every guide page asserted that product links "carry the site's Amazon tag" while the approved Special-Link register is empty. Live on `main` at the base commit. | Fixed in this pass: the sentence is computed from `approved_amazon_urls()`. |

## Cross-scope notes and requests (not edited, per the handoff rules)

1. **`_tools/stage.py`**: its asset allowlist names specific css/js files. My category
   styles were appended to `assets/css/storefront.css`, which is already in the list, so
   staging is complete — verified: `stage.py` writes 94 files including `categories/`.
   No change requested, recorded so the next session follows the same route instead of
   adding a stylesheet that a workflow deploy would drop.
2. **`_tools/check.py::PUBLIC_DIRS`** already reserved `categories` and `compliance`.
   This pass used `categories`. `compliance` remains unwritten; whoever claims it should
   register the pages in `build.py` the same way, or `check_no_stray_pages()` will fail.
3. **`edition/`** is still served as a second, complete edition at `/Affil1/edition/`
   with its own sitemap and feed, which competes with the canonical site for the "one
   site to index" goal. Its owner (`arena/44f81bcd-affil1`) should either fold it into the
   root build or mark it `noindex`; this session did not touch it.
4. **Pages `build_type`** is still `legacy`, so the branch root is what is published.
   `pages.yml` already switches to uploading the curated `_site` when the repository
   setting says `workflow`. That is an owner or admin action, not a file change.
5. **`suggestions.json` S-23** proposes that `/products/` (the register view) or
   `/categories/` (the shopper view) be the one that is indexed. Both are in the sitemap
   now, which is the honest state until the owner decides.

## Reproduced checks, this branch

```
python3 _tools/build.py                    → 42 pages; second build byte-identical
python3 _tools/check.py                    → 42 pages, 0 errors, 0 warnings
python3 _tools/validate.py                 → 2,609 checks, 0 warnings
python3 _tools/check_local_links.py        → 76 pages, 0 broken
python3 _tools/sweep_surfaces.py --dry-run → would move: 0
cd _tools && python3 -m unittest discover  → 10 tests OK
python3 _decision-support/validate.py      → PASS, 6 check families
python3 _platform/verify_edition.py        → 1,965 checks, 0 errors
python3 _tools/stage.py /tmp/stage-test    → 94 files, no missing-asset lines
CI reproducibility diff (copy, rebuild, diff -r) → no drift
```

## Merge log

See the PR linked from COORDINATION.md. Updated below on merge.
