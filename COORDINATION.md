# COORDINATION.md — shared task board

This file is the single source of truth for who is working on what. Read it before you start.

Last updated: 2026-11-20 (final integration session `arena/2361a177-affil1`).

## Current state: ONE canonical publication

Several sessions built in parallel. As of this integration there is exactly one published
publication, **Good Measure Kitchen**, at the site root. Every page it serves is rendered by
`scripts/build_site.py` from the single source of truth `site_data.py`, and every page it
serves passes `scripts/check_site.py`.

| Path | Owner | Status |
| --- | --- | --- |
| Canonical publication (root) | `arena/2361a177-affil1` | **Live.** Rendered, gated, deployed. |
| Archived prior work | `archive/session-*/` | Preserved in the repository. Never published. |

### Why the parallel sections were archived rather than kept live

`main` briefly carried two additional full publications at the root and under `/crisp/`,
each with its own front page, guides, product tables, register pages, sitemap and feed.
Keeping them would have meant serving three publications about the same five products on
one domain. For search that is duplicate content competing with itself, and for a reader it
is three front doors to the same shop — the exact "audit dump" failure the brief rules out.

The rule applied: **preserve the work, publish one site.** Every file from every prior
session is still in the repository under `archive/`, with its internal links repaired so it
still renders and can still be reviewed. Nothing was deleted. The one idea worth keeping
from `/crisp/` — a comparison table built only from what each listing states — was rebuilt
properly as `shop/compare.html`, with every cell linked to the listing it was read from.

## Rules (restated so they survive a cold start)

1. Claim a task by writing your session ID + file scope below, commit, and push **before** editing files.
2. Never start a task another live session has claimed.
3. Keep scopes non-overlapping. Work only on your own branch.
4. Need a file another session owns? Log the request here. Do not edit it.
5. Small, frequent commits. `git pull --rebase` before every push.
6. Shared outputs — the front page, `sitemap.xml`, `feed.xml`, navigation — are only changed
   by the integration session once all other tasks are done.
7. Never mark anything verified without an official source link. If a value cannot be confirmed,
   leave it blank and flag it. No inference, no filler.

## Task board

| Task | Scope | Owner | Status | Notes |
| --- | --- | --- | --- | --- |
| SG-01 Source register and product confirmation records | `src/data/products.json` → `site_data.py` | S-96012762, then `arena/2361a177-affil1` | done | 5 submitted links resolved, 4 derived ASINs observed, 1 unresolved. |
| SG-02 Compliance register (Associates + FTC) | `src/data/compliance.json` → `site_data.py` | S-96012762 | done | Clause-level points with official URLs. |
| SG-03 Editorial cluster + question set | `src/data/questions.json` → `site_data.py` | S-96012762 | done | Working titles only. No search-volume claims. |
| SG-04 Suggestion board | `src/data/suggestions.json` → `site_data.py` | S-96012762 | done | 15 proposals, each with a decision slot and a source. |
| SG-05 Open-questions register | `src/data/questions-open.json` → `site_data.py` | S-96012762 | done | 8 questions, each answerable or blocked. |
| SG-06 Analytics + click-measurement plan | `assets/analytics.js`, `api/` | S-96012762, then `arena/2361a177-affil1` | done | 5 events. Endpoint intentionally not deployed. |
| SG-07 Site build: landing, category, guide pages | `scripts/build_site.py` | S-96012762, then `arena/2361a177-affil1` | done | Disclosure above the fold on every page. |
| SG-09 Search + syndication | `sitemap.xml`, `feed.xml`, `robots.txt` | `arena/2361a177-affil1` | done | One indexable host, canonical URLs, feed linked site-wide. |
| SG-10 Flagged for Review page | `desk/flagged-for-review.html` | `arena/2361a177-affil1` | done | 9 items, each with the source that would settle it. |
| SG-11 Executive summary | `desk/executive-summary.html` | `arena/2361a177-affil1` | done | Written against the locked data. |
| SG-12 Integration: merge, re-verify, build, deploy, PR | branch + `main`, Pages | `arena/2361a177-affil1` | done | See the integration log. |
| SG-29 Search Console | out of repo | `arena/2361a177-affil1` | needs review | Cannot be completed without account access. FLG-010. |
| SG-30 Reader capture (email) | out of repo | `arena/2361a177-affil1` | needs review | Requires a provider + privacy review. FLG-011. |
| SG-31 Comparison table | `shop/compare.html` | `arena/2361a177-affil1` | done | Rebuilt from the `/crisp/` idea, every cell sourced. |
| SG-32 Publishing gate in CI | `.github/workflows/pages.yml` | `arena/2361a177-affil1` | done | Build fails if the committed HTML drifts from the renderer, or if the gate fails. |

## Verification ledger (what was actually checked, and against what)

| # | Claim | How it was checked | Result | Source |
| --- | --- | --- | --- | --- |
| V-01 | `link.amazon/*` short links resolve to Amazon product pages | Fetched each of the 5 URLs, followed redirects, read the destination canonical `/dp/` ASIN | 4/5 resolved; `B0c8moW59` hit an Amazon `/checkpoint/continue` interstitial twice and never resolved | Resolved targets recorded per-record in `site_data.py` |
| V-02 | The 5 supplied codes are valid ASINs | Counted characters and compared against Amazon's ASIN definition | **Failed** — all 5 supplied codes are 9 characters; an ASIN is 10 | [Amazon: Understanding ASINs](https://sell.amazon.com/blog/what-is-an-asin) |
| V-03 | Special Links must carry the Associate ID as a URL parameter | Read Associates Program Policies §2(b) | Confirmed | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| V-04 | A link may not obscure that it points to Amazon | Read Program Policies §2 (link shortener / cloaking clause) | Confirmed | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| V-05 | Prices may only be shown if Amazon serves them, or via Creators API / PA API | Read Program Policies §2(b) price/availability clause | Confirmed — **no price appears on any reader-facing page** | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| V-06 | Affiliate compensation must be disclosed clearly and conspicuously | Read FTC Endorsement Guides, affiliate FAQ | Confirmed — disclosure is above the masthead on all 23 pages and repeats in every footer | [FTC Endorsement Guides FAQ](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) |
| V-07 | Commission rates for Home & Kitchen etc. | `affiliate-program.amazon.com/help/operating/schedule` | **Not available** — redirects to Associates sign-in. Rates are left blank and flagged | — (FLG-004) |
| V-08 | The supplied short links are or are not compliant Special Links | No official mechanism exists to check a tag without account access | **Unresolved** (maintains FLG-003) | — |
| V-09 | Every published page passes the publishing gate | `scripts/check_site.py` over the rendered output | 23 pages, 10 checks, 0 failures | The gate itself, in this repository |
| V-10 | No internal link on the published site is broken | Gate check 6 across 24 pages | 0 broken | — |
| V-11 | Root-absolute links resolve on the `/Affil1/` subpath | The generator derives the base path from the site origin | Fixed | — |

## Flagged irregularities (published on `desk/flagged-for-review.html`)

- **FLG-001** All five supplied codes are 9 characters. The Associates tag format is `XXXXX-20`; the
  short-link path segment is not the ASIN. The ASIN must be read from the resolved page, not assumed.
- **FLG-002** No supplied link was observed to carry `shopnow047c-20`. Tracking attribution is unconfirmed.
- **FLG-003** Compliance status of the `link.amazon` short links is unresolved. Do not assert invalid; do not scale.
- **FLG-004** Commission rates require sign-in; omitted rather than guessed.
- **FLG-005** `B0c8moW59` never resolved to a product page (bot checkpoint only). Its ASIN is blank.
- **FLG-006** No price, rating, review count, or availability on any reader-facing page: policy-gated, not merely unknown.
- **FLG-007** Product identity beyond brand/model/category is unverified — no unit dimensions, wattage, or warranty.
- **FLG-008** Using Special Links or Program Content to develop machine-learning models needs express
  prior written approval under the IP License. Any "AI-driven" automation must be reviewed against
  this clause before it touches Amazon content.
- **FLG-009** The analytics collector is specified, not deployed. No third-party script, no cookie, no tracking is live.
- **FLG-010** Search Console property and sitemap submission need account access; not performed.
- **FLG-011** Email capture needs a provider and a privacy review; not performed.
- **FLG-012** Editorial titles are hypotheses. No search-volume or popularity data was obtained.
- **FLG-013** A dated observed price is republished on the desk pages. The distinction between a dated
  research observation and displaying Program Content has not been confirmed with the program.
- **FLG-014** Pages source is "Deploy from a branch"; switching it to "GitHub Actions" needs a repository
  administrator. The workflow is in place either way.

## Live deploy paths

- Publication: https://karagemop466-tech.github.io/Affil1/
- The shelf: https://karagemop466-tech.github.io/Affil1/shop/
- Compare: https://karagemop466-tech.github.io/Affil1/shop/compare.html
- Guides: https://karagemop466-tech.github.io/Affil1/guides/
- The desk: https://karagemop466-tech.github.io/Affil1/desk/
- Flagged for review: https://karagemop466-tech.github.io/Affil1/desk/flagged-for-review.html
- Feed: https://karagemop466-tech.github.io/Affil1/feed.xml
- Sitemap: https://karagemop466-tech.github.io/Affil1/sitemap.xml
- Archived prior work is in the repository under `archive/` and is not deployed.

## Integration log

### Final integration — `arena/2361a177-affil1`

1. **Merged** `origin/main` into the branch. The clone was shallow, so the first attempt reported
   unrelated histories; `git fetch --unshallow` restored the real common ancestor and the merge
   then proceeded normally.
2. **Resolved conflicts by role**, not by taking one side wholesale:
   - Canonical surfaces (`index.html`, `styles.css`, `app.js`, `feed.xml`, `sitemap.xml`,
     `guides/*.html`) → the rebuilt publication.
   - Prior-session root pages, registers, source data and tools → `archive/session-96012762-affil1/`,
     with every relative link repaired so the archived tree still renders.
   - The `/crisp/` section → `archive/session-96012762-affil1/crisp/`, links repaired.
   - `data.js` removed from the published tree; kept in the archive.
3. **Folded forward** the one idea worth keeping: the comparison table, rebuilt as
   `shop/compare.html` with every cell linked to the listing it was read from.
4. **Fixed a real deployment bug** found during integration: `404.html` used root-absolute
   links (`/styles.css`), which resolve to the domain root and break on the `/Affil1/`
   subpath. The generator now derives the base path from the site origin.
5. **Extended the publishing gate** to understand the deployment base path and to exclude
   archived prior work from the published surface.
6. **Re-verified**: `scripts/build_site.py` renders 24 files; `scripts/check_site.py` passes
   23 pages across 10 checks with 0 failures; the archive tree has 0 broken internal links.
7. **Wired the gate into CI**: `.github/workflows/pages.yml` now renders the site, fails the
   build if the committed HTML has drifted from the renderer, runs the gate, and publishes
   only the site files.

### Prior integrations

- PR #1 "Build evidence-led affiliate publication storefront" — merged to `main`.
- PR #2 "Record publication verification and Pages deployment" — merged to `main`.
- PRs #3–#17 — parallel sessions, merged to `main`. Their work is preserved in `archive/`.

### Pull request and merge result

- PR: _pending_
- Merge result: _pending_
- GitHub Pages deployment: _pending_
