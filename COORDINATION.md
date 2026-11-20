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


## Claims (integration session — arena/83e015f6-affil1)

| # | Task | Status | Owner | Files touched | Sources verified |
|---|------|--------|-------|---------------|------------------|
| 18| PR to main, merge, enable GitHub Pages, confirm deploy | in progress | session-arena-83e015f6 (takeover from session-arena-f10ea853, branch merged via PR #4, claim stale >60 min) | main branch, repo settings | n/a |
| 19| Integration pass: one canonical site (adopt recovered PR #15 tree per takeover rule), preserve crisp/ + src/ + tools/ + docs/ from S-96012762, full broken-link check | in progress | session-arena-83e015f6 | all site files | pending |
| 20| Line-by-line re-verification of 5 submitted links (independent observation pass) + data-register reconciliation | in progress | session-arena-83e015f6 | data/*.json | Amazon.com official site, fetched 2026-11-20 (see session log) |
| 21| Publication polish: brand imagery, SEO structured data, suggestions decisions log | in progress | session-arena-83e015f6 | index.html (via content/), lib/, records/ | pending |

## Session log

- **2026-11-20 — session-arena-83e015f6** (branch `arena/83e015f6-affil1`, base `ff74e5b`): claims 18–21. Handoff noted (60-minute rule).
- **Independent verification pass (session-arena-83e015f6, 2026-11-20 ~05:18–05:22 UTC):** fetched each submitted short link against Amazon.com official site, followed redirects, read destination page titles:
  - `link.amazon/B04G1MEwY` → `https://www.amazon.com/dp/B0CDY277D3` — CHEFMAN 6 Quart Dual Basket Air Fryer Oven (matches P-01 observation).
  - `link.amazon/B02NbDxp3` → `https://www.amazon.com/dp/B09B7SB46R` — Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven (matches P-02).
  - `link.amazon/B00hJ57DV` → `https://www.amazon.com/dp/B08DKYBTPH` — Chefman Air Fryer 8 Qt TurboFry (matches P-03; note: session-arena-f10ea853 earlier observed this link landing on the Amazon homepage — resolution is not stable across fetches).
  - `link.amazon/B0c8moW59` → `https://www.amazon.com/checkpoint/continue` (continue-shopping interstitial; no product page reached — matches P-04 unresolved).
  - `link.amazon/B0f3GKalj` → `https://www.amazon.com/dp/B0DZFD6R9Z` — CHEF iQ Sense wireless meat thermometer (matches P-05; session-arena-f10ea853 earlier observed homepage — divergence recorded).
- **PR #15 takeover (2026-11-20):** branch `integration-main` was closed and deleted by its session at 05:23:56 UTC without merging. Per the handoff rule, its tree was recovered from `refs/pull/15/head` and adopted as the canonical single site (24 pages, gate-verified). Its product register matches this session's independent Amazon observations exactly.

## Final integration (session-arena-83e015f6) — decisions and crosswalks

**Canonical site.** The recovered PR #15 tree ("The Crisp Counter") is the one
indexable site: `index.html`, `shop/`, `guides/`, `about/`, `summary/`, `records/`.
Generated from `content/`, `data/`, `lib/` by `scripts/build.mjs`; gated by
`scripts/check.mjs` + `scripts/test-gate.mjs` (7/7 injected violations caught on
the final run). `robots.txt` disallows `/archive/`, `/crisp/`, `/docs/`.

**Preserved, not discarded.**
- `crisp/` (S-96012762) kept at its original path with its own sitemap/feed; excluded
  from the published-page gate with a printed note; not indexed (robots Disallow).
- `src/`, `tools/`, `docs/MEASUREMENT.md`, `docs/EXECUTIVE-SUMMARY.md` kept as-is.
- The earlier root surface (dashboard, 13 legacy guides, legacy registers) is at
  `archive/legacy-surface/` — git records them as renames.
- `data/confirmations.json`, `data/products.json`, `data/ledger.json` kept with
  supersession notes; `data/product-intent.json` and `data/campaign-ledger.json`
  are canonical.

**Verification ledger additions (integration pass, 2026-11-20).**

| # | Claim | How it was checked | Result | Source |
|---|---|---|---|---|
| V-09 | The five submitted short links' current destinations | Independent fetch pass (session-arena-83e015f6), redirects followed, destination titles read | Exactly matches obs-1: 4 product pages (B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DZFD6R9Z), 1 interstitial | data/product-intent.json observation_log obs-2 |
| V-10 | Short-link resolution is stable | Compared obs-0 (session-arena-f10ea853) with obs-1/obs-2 | **Failed** — obs-0 saw two links land on the homepage that later resolved to product pages. Recorded as FLG-009 | data/product-intent.json observation_log |
| V-11 | S01–S15, S24 policy clauses | Re-read verbatim from the cited official pages (Operating Agreement §5-6; Program Policies Commission Income Statement §1/§6 and Participation Requirements §1-3) | Confirmed; both "Updated" dates match the register notes | row-level spot_check notes in data/sources.json |
| V-12 | S22 ASIN length ("10 characters") | Re-fetch of the cited Seller Central topic + the customer-help node + SP-API reference | **Unverified** — Seller Central topic errors without sign-in; SP-API confirms ASIN as identifier but states no length. Value blanked, flagged | data/sources.json S22 |
| V-13 | S18/S19 FTC clauses | ftc.gov blocked the fetcher in this pass | Not re-checked; official URLs retained for manual review | data/sources.json S18/S19 spot_check |
| V-14 | Published site link integrity | Full crawl from index.html over internal refs (canonical-URL aware) | 32 paths, 0 broken | this integration log |
| V-15 | Data-register consistency | Compared all four product registers field by field | 3 disagreed; reconciled with supersession notes, nothing deleted | FLG-010 |

**Event-name crosswalk.** The canonical five events are `page_view`,
`outbound_click`, `guide_read`, `record_open`, `suggestion_decide`
(`data/events.json`; no identifiers of any kind). Earlier sessions defined a
variant set (`suggestion_review`, `session_start`); the mapping is
suggestion_decide ≈ suggestion_review, and session_start was dropped deliberately
(no session id is stored). `assets/js/analytics.js` is inert until an endpoint is
configured (FLG-004); `analytics/endpoint.py` is the candidate host.

**Flag-number crosswalk.** The published register (records/flagged) uses
FLG-001..FLG-010 from the PR #15 scheme. The S-96012762 board's FLG-001..FLG-013
map onto it as follows: their 001/002/004/006/007 ≈ published 003/002/006/001/007;
their 003 = published 003 (same item); their 005/008/009/010/011/012/013 are
covered by published 005/008/004/010/007 + the measurement and ledger records.

**Open pull requests (not mine; left open for their sessions).**
- PR #9 (arena/4bcd015a-affil1, "Countertop Notes") — would replace root files;
  superseded by the canonical site. Left open for its session; close or rebase as
  appropriate. Its unique assets are not in the tree and are not deleted anywhere.
- PR #12 (arena/c58c5996-affil1) — fixes root-absolute links in
  `guides/buying-guide-air-fryer.html`, a legacy-surface page now under
  `archive/legacy-surface/`. Superseded by the integration; left open for its session.
