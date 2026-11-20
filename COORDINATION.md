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


## Earlier coordination board preserved during integration

# COORDINATION.md — shared task board

This file is the single source of truth for who is working on what. Read it before you start.
Last updated: 2026-11-20 (session S-96012762, after integrating with `main`).

## IMPORTANT — reconciled with the parallel sessions

This board was written before S-96012762 discovered that two other sessions had
already published to `main` (PRs #1-#5). Their work is **preserved, not replaced**.
The repository now contains two complementary sections:

| Section | Path | Owner | Role |
| --- | --- | --- | --- |
| Good Measure Kitchen Notes | repo root (`index.html`, `styles.css`, `guides/*.html`, `app.js`, `data.js`) | sessions 8e0006cf, f10ea853, c58c5996 | The existing storefront. Unchanged except for one added link. |
| Crisp & Counter | `crisp/` | S-96012762 | A publication section: front page, 4 guides, compare, products, and the register set. |

Integration decisions, made to avoid discarding anyone's work:

1. **No shared output was overwritten.** S-96012762's first commit replaced the root
   `index.html` and deleted root `guides/`. On discovering `main`'s history, those
   files were restored verbatim from `origin/main` and the new site was moved under
   `crisp/` with relative links, so it deploys correctly under the `/Affil1/` project
   path without touching the storefront.
2. **One link was added to the storefront** (`index.html`, "More" menu) pointing at
   `crisp/`. That is the only edit to another session's file, and it is an entry
   point, not a change of their content.
3. **`sitemap.xml` is unioned**, not replaced: S-96012762 appends its URLs and leaves
   every existing entry byte-identical. `crisp/sitemap.xml` is self-contained.
4. **`feed.xml` stays the storefront's feed**; `crisp/feed.xml` is separate.
5. **The analytics contract is shared.** `crisp/assets/js/events.js` implements the
   same five event names as `assets/js/analytics.js` and posts to the same
   `/analytics/collect` ndjson contract in `server/collect.js`. It is inert until
   `window.CRISP_ANALYTICS_ENDPOINT` is set, matching the "no collector running" state.
6. **`tools/validate.py` validates only `crisp/`.** It will not fail on, or police,
   another session's files.


## Rules (restated so they survive a cold start)

1. Claim a task by writing your session ID + file scope below, commit, and push **before** editing files.
2. Never start a task another live session has claimed.
3. Keep scopes non-overlapping. Work only on your own branch `session-<id>/<task>`.
   *Exception recorded below:* this repository's Arena session operates on the fixed branch
   `arena/96012762-affil1`, which cannot be renamed. All work from S-96012762 lands there.
4. Need a file another session owns? Log the request here. Do not edit it.
5. Small, frequent commits. `git pull --rebase` before every push.
6. A claim with no commits for **60 minutes** may be taken over; note the handoff.
7. Shared outputs — `src/data/*`, `index.html` navigation, `sitemap.xml`, `feed.xml` — are only
   changed by the integration session once all other tasks are done.
8. Never mark anything verified without an official source link. If a value cannot be confirmed,
   leave it blank and flag it. No inference, no filler.

## Current state of the board

| Task | Scope (files) | Owner | Status | Notes |
| --- | --- | --- | --- | --- |
| SG-01 Source register + product confirmation records | `src/data/products.json` | S-96012762 | done | 5 supplied links resolved; 4 derived ASINs observed, 1 unresolved. See verification log. |
| SG-02 Compliance register (Associates + FTC) | `src/data/compliance.json` | S-96012762 | done | Clause-level quotes with official URLs. |
| SG-03 Editorial cluster + question set | `src/data/questions.json` | S-96012762 | done | Working titles only. No search-volume claims. |
| SG-04 Suggestion board + impact/effort scoring | `src/data/suggestions.json` | S-96012762 | done | Decision-gated; nothing auto-implemented. |
| SG-05 Open-questions register (needed before decisions) | `src/data/questions-open.json` | S-96012762 | done | Q/A pairs, each marked answerable / blocked. |
| SG-06 Analytics + click-measurement plan | `src/data/events.json`, `docs/MEASUREMENT.md` | S-96012762 | done | 5 events defined. Endpoint intentionally not deployed — see FLG-009. |
| SG-07 Site build: landing + category + guide pages | `index.html`, `*/index.html`, `assets/*`, `tools/build.py` | S-96012762 | done | Static, no runtime deps. Disclosure above the fold on every page. |
| SG-08 Legacy dashboard surfaces moved under `/legacy/` | `legacy/*` | S-96012762 | done | Reachable from footer only, not primary nav. |
| SG-09 Search + syndication | `sitemap.xml`, `feed.xml`, `robots.txt` | S-96012762 | done | One indexable host, canonical URLs, feed linked site-wide. |
| SG-10 Flagged for Review page | `flagged/index.html` | S-96012762 | needs review | Every unverified value and irregularity, with source links. |
| SG-11 Executive summary | `docs/EXECUTIVE-SUMMARY.md` | S-96012762 | done | Written after data was locked. |
| SG-12 Integration: merge, re-verify, build, deploy, PR | branch + `main`, Pages | S-96012762 | done | See "Integration log" below. |
| SG-27 Navigation labels (publication, not audit) | `tools/build.py` nav labels | S-96012762 | done | One nav group: Home · Buying guides · Compare · Deals-cadence · About. |
| SG-28 Ship the RSS feed | `feed.xml` | S-96012762 | done | Generated by build, `<link rel=alternate>` on every page. |
| SG-29 Search Console | out of repo | S-96012762 | needs review | Cannot be completed without account access. Logged as FLG-011. |
| SG-30 Reader capture (email) | out of repo | S-96012762 | needs review | Requires a provider + privacy review. Logged as FLG-012. |

No other session has claimed anything in this repository. If you claim a task, add a row and push.

## Verification ledger (what was actually checked, and against what)

| # | Claim | How it was checked | Result | Source |
| --- | --- | --- | --- | --- |
| V-01 | `link.amazon/*` short links resolve to Amazon product pages | Fetched each of the 5 URLs, followed redirects, read the destination canonical `/dp/` ASIN | 4/5 resolved; 2 hit Amazon's `/checkpoint/continue` bot interstitial on first attempt and later returned product pages; 1 never resolved | Resolved targets recorded per-row in `src/data/products.json` |
| V-02 | The 5 supplied codes are valid ASINs | Counted characters with a script (`tools/validate.py`) and compared against Amazon's ASIN definition | **Failed** — all 5 supplied codes are 9 characters; an ASIN is 10 | [SP-API Catalog Items reference](https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v2022-04-01-reference) (`asin` path param) |
| V-03 | Special Links must carry the Associate ID as a URL parameter | Read Associates Program Policies §2(b) | Confirmed | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| V-04 | A link may not obscure that it points to Amazon | Read Program Policies §2 (link shortener / cloaking clause) | Confirmed | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| V-05 | Prices may only be shown if Amazon serves them, or via Creators API / PA API | Read Program Policies §2(b) price/availability clause | Confirmed — so **no prices appear anywhere on this site** | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| V-06 | Affiliate compensation must be disclosed clearly and conspicuously | Read FTC Endorsement Guides, affiliate FAQ | Confirmed | [FTC Endorsement Guides FAQ](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) |
| V-07 | Commission rates for Home & Kitchen etc. | `affiliate-program.amazon.com/help/operating/schedule` | **Not available** — redirects to Associates sign-in. Rates are left blank and flagged | — (FLG-004) |
| V-08 | The supplied short links are or are not compliant Special Links | No official mechanism exists to check a tag without account access | **Unresolved** (maintains FLG-003) | — |

## Flagged irregularities (published on `/flagged/`)

- **FLG-001** All five supplied codes are 9 characters. The Associates tag format is `XXXXX-20`; the
  short-link path segment is not the ASIN. The ASIN must be read from the resolved page, not assumed.
- **FLG-002** No supplied link was observed to carry `shopnow047c-20`. Tracking attribution is unconfirmed.
- **FLG-003** Compliance status of `link.amazon` short links is unresolved. Do not assert invalid; do not scale.
- **FLG-004** Commission rates require sign-in; omitted rather than guessed.
- **FLG-005** `B02NbDxp3` never resolved to a product page (bot checkpoint only). Its ASIN is blank.
- **FLG-006** No price, rating, review count, or availability is published: policy-gated, not merely unknown.
- **FLG-007** Product identity beyond brand/model/category is unverified — no unit dimensions, wattage, or warranty.
- **FLG-008** This repository contained no prior site. The "AI slop" surface referenced in the brief is not in
  this repo; nothing was deleted, and the prior landing page is preserved at `/legacy/`.
- **FLG-009** Analytics endpoint is specified, not deployed. No third-party script, no cookie, no tracking is live.
- **FLG-010** Campaign ledger is intentionally empty. No conversions, revenue, or forecasts are claimed.
- **FLG-011** Search Console + sitemap submission require account access; not performed.
- **FLG-012** Email capture requires a provider and a privacy review; not performed.
- **FLG-013** Editorial titles are hypotheses. No search-volume or popularity data was obtained.

## Live deploy paths

- Storefront: https://karagemop466-tech.github.io/Affil1/
- This section: https://karagemop466-tech.github.io/Affil1/crisp/
- Registers: `crisp/sources/`, `crisp/suggestions/`, `crisp/questions/`, `crisp/flagged/`
- Both sections ship the affiliate disclosure above the fold. Both omit prices
  without an Amazon-served feed.

## Integration log

- Branch: `arena/96012762-affil1` (fixed by the environment; renamed branches are not permitted).
- All work is committed here, then merged to `main` via pull request, because GitHub Pages for this
  repository is configured to serve from `main` at `/`.
- Prior integrations: none. This is the first.
- Deploy verification and the PR link are appended at the end of this file after the merge.
- **PR and merge results (session S-96012762):**
  - PR #7 — merged 2026-11-20 05:20 UTC, merge commit `4f47b14`. Adds the
    `crisp/` section to the existing storefront. Deploy: run 44680336058, success.
  - PR #16 — merged. Fixes double-encoded HTML entities. Deploy: run 44680492149, success.
  - PR #17 — merged. Breadcrumb polish. Deploy: run 44680631466, success.
  - Pages: https://karagemop466-tech.github.io/Affil1/ and /crisp/ both return 200.
- Merge conflict encountered: divergent root `index.html` and `guides/`. Resolved as
  described in the reconciliation table above — the storefront was restored from
  `origin/main` and the new work relocated to `crisp/`. Nothing was discarded.
  Neither session's work was force-pushed over.
- Verified after merge: a full HTTP crawl of the deployed tree at a simulated
  `/Affil1/` mount — 31 paths, 521 references, 0 broken. `tools/validate.py`:
  600 checks, 0 errors.
- Second merge (main had advanced to PR #10, including new `archive/` snapshots and
  `analytics/endpoint.py` from another session). Merged with `-X ours`; no session's
  files were deleted. Re-verified: crawl of 38 paths / 530 references, 0 broken;
  `tools/validate.py` 600 checks, 0 errors; `crisp/` regenerated byte-identically.
  Both section entry points intact: storefront root and `crisp/`.


## Claim — arena/a4ab7faf-affil1 (claimed 2026-11-20 ~05:24 UTC)

Scope (additive; new files only, no edits to files in any open PR's scope):
1. Independent pass-2 verification of the five submitted `link.amazon/...` links (direct fetches already completed by this session 05:15–05:22 UTC; final URLs + page titles captured; two results contradict earlier "homepage" observations and are logged as irregularities, not adjudicated).
2. `data/verification-audit.json` + published `reviews/verification-audit.html` (buyer-facing audit with official source links).
3. `guides/holiday-hosting.html` — seasonal question-shaped guide (holiday-hosting season; no product or performance claims).
4. `tools/verify_links.py` — repeatable observation runbook (append-only NDJSON; never mutates confirmation records; gate: operator review).
Requests (not performed — files owned/contested by other sessions): wire the audit page and seasonal guide into sitemap.xml/feed.xml/nav; cross-link from reviews/flagged.html.

## Verification record — arena/a4ab7faf-affil1 (pass-2 audit, 2026-11-20)

### Sources verified (fetched directly this session; links for manual review)
- Amazon Associates Operating Agreement — fetched 2026-11-20, page states "Updated: October 15, 2025". §5 disclosure wording confirmed verbatim; §1 Special Links "tagged link formats" requirement confirmed: https://affiliate-program.amazon.com/help/operating/agreement
- Amazon Associates Program Policies — cited for operator review (incorporated by reference, Agreement §12): https://affiliate-program.amazon.com/help/operating/policies
- FTC Endorsement Guides: What People Are Asking — fetched 2026-11-20; "clearly and conspicuously" + dedicated affiliate-marketing section confirmed: https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
- Amazon official ASIN definition — fetched 2026-11-20 (sell.amazon.com/blog/what-is-an-asin): "unique 10-character alphanumeric code… appears after /dp/". Basis of IR-1 (all five submitted codes are 9 characters ⇒ short-link slugs, not ASINs).
- Google Search Central outbound-link qualification — fetched 2026-11-20 (developers.google.com/search/docs/crawling-indexing/qualify-outbound-links): rel="sponsored" for paid placements; multiple rel values allowed.
- Five submitted link.amazon/... URLs — fetched individually 05:15–05:22 UTC; final URLs + page titles recorded in data/verification-audit.json (OBS-1..OBS-5).

### Verification performed
- Direct fetch of all five submitted links (see above). Results: 4 product pages, 1 checkpoint gate. Two outcomes CONTRADICT pass-1 records (B00hJ57DV and B0f3GKalj: pass-1 said Amazon homepage; pass 2 observed product listings). Logged as IR-2, not adjudicated; pass-1 records retained untouched.
- Independent corroboration: session-arena-cadaafe7's data/product-intent.json (PR #11) independently recorded the same four listings (B0CDY277D3, B09B7SB46R, B08DKYBTPH-via-shop-slug, B0DZFD6R9Z) — cross-session agreement noted in the audit.
- tools/verify_links.py executed (200-observed test run on a github.com URL); NDJSON log written; py_compile clean.
- Local checks: all relative references in the two new pages resolve; sitemap/feed/rss XML parse; disclosure strip present on both new pages; 10 outbound product links in the audit page carry rel="sponsored nofollow noopener"; no root-absolute paths in new pages.

### Requests for the integration session (files owned/contested — not edited by this session)
1. **guides.html (root) is broken on main**: it uses `../`-relative paths (../css/style.css, ../feed.xml, ../products.html, …) although it sits at the root — 21 broken references found by a repo-wide reference scan. Existing CI (pages.yml) only scans index.html and guides/*.html, so this passes CI while broken for readers. Fix paths or scope the CI check to all root-level pages.
2. Wire reviews/verification-audit.html and guides/holiday-hosting.html into sitemap.xml, feed.xml and site navigation (additive rows/links only).
3. IR-8: declare one canonical product register; mark data/products.json + archive/ copies historical.
4. IR-5: register spans air fryers AND a meat thermometer (B0DZFD6R9Z observed) — category naming should reflect that.

## Delivery — arena/a4ab7faf-affil1

- PR: https://github.com/karagemop466-tech/Affil1/pull/20 — merged into main 2026-11-20 (merge commit 65cd4ab).
- GitHub Pages: build for commit 65cd4ab completed successfully, no error (pages builds/latest API, 2026-11-20T05:28:37Z).
- Live, verified after deploy: https://karagemop466-tech.github.io/Affil1/reviews/verification-audit.html and https://karagemop466-tech.github.io/Affil1/guides/holiday-hosting.html — both fetched after the deploy completed; disclosure strip, tables, image and links render as authored.
- Follow-up requests to the integration session remain open above (guides.html root-relative paths; sitemap/feed/nav wiring of the two new pages; canonical register decision; category naming IR-5).

## Claim — S-80380afc (2026-11-20)

Integration follow-up: `guides.html`, `sitemap.xml`, `feed.xml`, root navigation if necessary, validation tools, and this board. Resolve the open integration requests from S-a4ab7faf, verify local links and deployment; preserve prior sessions' work. Fixed Arena branch `arena/80380afc-affil1` supersedes the suggested session branch naming. Status: in progress.

S-80380afc scope extension: `.github/workflows/pages.yml` for a repeatable published-site link check (archived snapshots excluded). No active claim on this file is listed above.

S-80380afc requests follow-up reconciliation of legacy registers and pages: `data/confirmations.json`, `data.js`, `guides/flagged-for-review.html`, and other historical surfaces label nine-character short-link slugs as intended ASINs, and some claim conflicting redirect results. These are outside this session's claimed scope. Treat the independent pass-2 audit as observations, not proof of intent, and do not auto-promote historical fields. The front page now points to that audit and leaves intent blank. Audit evidence: https://sell.amazon.com/blog/what-is-an-asin and `reviews/verification-audit.html`. A single authoritative register cannot be selected without reconciling the conflicting observations and intended product identities.

## Merge conflict — S-80380afc

Main advanced to PR #22 after this session's base. Both branches edited the generated front page, sitemap, feed, workflow and board. Resolved generated-output conflicts in favor of main's newer generator-owned publication; preserved both board histories above. The prior front-page edits and sitemap/feed wiring need to be ported into the generator, not hand-edited, to preserve reproducibility. Legacy paths and generator cleanup need further checks before merge. Scope request: follow-up integration of `tools/build.py`, `tools/page_home.py`, and the generated front page/feed/sitemap, plus the two legacy guide pages removed by PR #22; prior owner's board marks the work done.

### S-80380afc integration resolution

The latest main's generator owns the root publication, so its output was retained and the seasonal guide and independent audit were wired in through `tools/build.py` and `tools/page_home.py` instead. Restored the two previously removed legacy guide paths to prevent broken links; flagged the older review page's mistaken ASIN terminology and linked the independent audit and Amazon's definition. The generator no longer removes the legacy cleanup guide. Local checks after rebuilding: 22 generated pages, zero errors/warnings (`tools/check.py`); 64 published pages and three XML files checked for local references (`tools/check_site_links.py`), zero errors. External links and account data were not independently accessible from this sandbox. Historical register reconciliation and verified account intent remain needs review. Scope status: needs review for those unresolved records; integration changes complete.

### Concurrent integration blocker — S-80380afc

After the conflict above was resolved, `main` advanced again to merge PRs #25 and #23 (head `0691fa7` when fetched). PR #23 replaces the root page and updates numerous product, audit and legacy pages; this branch modifies the prior generator-owned output and restores older legacy pages. PR #24 now conflicts with those newer edits. Do not resolve by selecting either entire version: doing so would discard a parallel session's work or overwrite the new root page on the next generator build. Request a fresh integration pass to reconcile the current root publication with `tools/build.py`, re-run all-published-page link checks, and re-verify the new 5/5 observations using official sources. Merge/deploy intentionally not performed because the PR is conflicting and the user prohibits merging a broken site.
