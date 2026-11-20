# Session log — `arena/ddb6772b-affil1` · 2026-11-20 UTC

Branch: `arena/ddb6772b-affil1`, rebased onto `origin/main` at `d345cf0`, then through
`3d2a453` (PR #108) mid-work. Claim committed before any site file was touched.

## Scope delivered

1. `/categories/` index + `air-fryers` + `thermometers` subpages, wired into nav,
   footer, sitemap and feed.
2. One new guide with per-row official sourcing (`where-to-put-the-probe`); three
   others drafted here were retired on rebase against main's `holiday-hosting-air-fryer`
   and `reheating-thanksgiving-leftovers`, and the module records why.
3. One false compliance sentence on every guide page, repaired and made computed.
4. Register updates: 4 sources (SRC-21…SRC-24), 3 questions (Q-25…Q-27), 3 suggestions
   (S-32…S-34), 2 flags (FLG-036, FLG-037), a third corroboration appended to main's
   FLG-028, and 6 observation rows in `_data/verification-observations.ndjson`.
5. Executive summary counts corrected and an addendum added.
6. `FLG-036`: the guides loop in `_tools/check.py` requires the literal sentence "No link
   currently carries the tracking tag"; the sidebar now generates it from the register, and
   the rule itself carries an expiry date, which is flagged rather than silently edited.
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
| FLG-034 | All five submitted `link.amazon/<code>` links resolved to the Amazon homepage when this session followed them, in five separate fetches. Direct fetch of `amazon.com/dp/B0CDY277D3` in the same session matched the register title. | Open. No published destination uses a short link, so readers are unaffected; the intended-ASIN chain is not established. |
| FLG-035 | Nine modules in `_tools/` are unreachable from `_tools/build.py` and from every workflow (`buyer_guides`, `content_extra`, `extra_pages`, `page_sources`, `preview`, `quarantine_legacy`, `shop_build`, `shop_check`, `verify_links`). `research_brief.py` is wired into `editorial.yml` and `arm_links.py` is an owner CLI, so neither is counted. `extra_pages.py` also links to `/_src/data/reverification.json` with a root-absolute URL that would 404 on a project-pages host. | Open. Nothing published changes; the risk is a future session editing a file that publishes nothing. |
| (main's FLG-031) | The same guide-page sentence — that every product link "carries the site's Amazon tag" — was found and fixed independently by `arena/b990bce7-affil1`, which rewrote the sentence and added a `check.py` rule requiring the literal phrase "No link currently carries the tracking tag". | Same defect, two sessions. Their flag and their fix stand as the record. This pass adds the durability: the sentence is generated from `approved_amazon_urls()`, so it cannot outlive the register state, and it still emits the exact phrase their checker looks for. |

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

- [PR #118](https://github.com/karagemop466-tech/Affil1/pull/118) merged into `main` as `d63b2f6`; all four workflows green on the merge commit; `pages build and deployment` run 44694702258 succeeded; the live category pages and the new guide were then fetched from the Pages host and read back.
- Four rebases/merges onto a `main` that moved under the branch. Resolution rule used every time, and written into `/tmp/merge_main.py` so it is mechanical: build outputs are never hand-merged (main's copy, then regenerate), registers keep main's row at the id and re-file this session's rows at the end of the range, append-only markdown keeps both texts. Rows re-filed this way: SRC-21…24, S-39…41, FLG-039…040. Findings dropped as already published: the short-link flag (main's FLG-028, appended as a third corroboration), the guide tag-sentence flag (main's FLG-031), three board duplicates (S-01, S-12, S-24), two policy sources (SRC-18/19).
- Follow-up after the merge: the probe guide's classification table now carries a linked source per row, which is what this session claimed in its own editorial rule and had not enforced.

## Rebase reconciliation (recorded because it removed work, not because it added it)

Two rebases onto a moving `origin/main` (through `bcef8b6`, PR #121). Everything that
collided was resolved by keeping main's row and renumbering or dropping mine:

| Drafted here | State on main | Resolution |
|---|---|---|
| 4 guides | 4 more guides published by other sessions | 1 kept, 3 retired as duplicate coverage |
| short-link instability flag | already FLG-028, corroborated by two sessions | no new flag; third corroboration appended |
| false tag-sentence flag + fix | already FLG-031 + S-22, wording fixed | no new flag; fix made *computed*, which theirs is not |
| fortnightly cadence proposal | already S-12 | dropped |
| masthead/nav trimming proposal | already S-24, implemented | dropped |
| SiteStripe arming proposal | already S-14/S-26 | dropped |
| 2 Amazon-policy sources | already SRC-18/SRC-19 | dropped; 4 USDA rows renumbered to SRC-21…SRC-24 |
| front-page `GUIDES[-4:]` and seasonal-by-newest | main fixed the same defect by slug | main's version kept; my only addition is suppressing standing copy whose article is no longer selected |
| `check.py` literal-sentence rule (mine) | rule exists on main | kept as FLG-037, because the rule can outlive the fact it asserts |

`_data/verification-observations.ndjson`, `_src/data/*.json` id renumbering, and the
retired-guide note in `_tools/content_season.py` are the audit trail for all of it.
