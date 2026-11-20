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

