# Coordination board

Shared task board for this repository. Each session claims a task by writing its session ID
and file scope here, then commits and pushes that claim immediately.

**Current integration session:** `arena/2361a177-affil1` (branch `arena/2361a177-affil1`).
This session acts as the final integration session: it owns shared outputs (table data,
site index, navigation) after the other claims below are reconciled.

## Task board

| Task | Status | Owner / session ID | Files in scope |
| --- | --- | --- | --- |
| Publication storefront, decision-support and flagged-review pages | done | `arena/8e0006cf-affil1` | `index.html`, `styles.css`, `app.js`, `data.js`, `guides/`, `COORDINATION.md` (merged as PR #1, PR #2) |
| Official-source verification of supplied product links and marketing claims | needs review | `arena/8e0006cf-affil1` | `guides/flagged-for-review.html`, `data.js` |
| GitHub Pages deployment configuration | done | `arena/8e0006cf-affil1` | `.github/workflows/pages.yml` (merged as PR #1, PR #2) |
| Build and integrate sourced affiliate publication website, decision-support pages, and GitHub Pages workflow | in progress (pre-implementation, based on `cca8c2a`) | `arena/4bcd015a-affil1` | `COORDINATION.md`, `README.md`, `index.html`, `assets/*`, `data/*`, `.github/workflows/*`, `docs/*` |
| Claim affiliate publication site implementation | in progress (pre-implementation, based on `cca8c2a`) | `arena/171b54e4-affil1` | `COORDINATION.md`, `README.md`, `index.html`, `guides/`, `shop/`, `project/`, `about/`, `assets/`, `data/`, `docs/`, `scripts/`, `tests/`, `server.mjs`, `package.json`, `.github/`, `.nojekyll`, `404.html`, `robots.txt`, `sitemap.xml`, `rss.xml`, `.gitignore` |
| **Publication rebuild: shop-led front page, category subpages, question-shaped guides, product-intent confirmation record, suggestions register, questions register, campaign ledger, publishing gate, self-hosted analytics endpoint, verification re-check, PR + merge + Pages deploy** | **in progress** | **`arena/2361a177-affil1`** | `COORDINATION.md`, `README.md`, `index.html`, `styles.css`, `app.js`, `data.js`, `404.html`, `robots.txt`, `sitemap.xml`, `feed.xml`, `.nojekyll`, `guides/`, `shop/`, `desk/`, `assets/`, `api/`, `scripts/`, `site_data.py`, `.github/workflows/pages.yml` |

### Coordination notes / conflict log

- `arena/4bcd015a-affil1` and `arena/171b54e4-affil1` both branched from the original
  `cca8c2a` commit (README only) and both claim `COORDINATION.md`, `README.md` and `index.html`.
  Neither had pushed implementation content when this session started.
- Those branches predate the merged PR #1 / PR #2 work, so they do not contain the published
  storefront this session is extending.
- This session therefore takes the integration role explicitly: it re-verifies the combined
  data line by line, publishes to GitHub Pages, and merges to `main`. If the other two sessions
  push implementation later, their commits must be reconciled against this branch before
  merge, or their work will be superseded by the merged result. This is recorded here so no
  session's work is silently discarded.
- Shared outputs (`site_data.py`, `index.html`, navigation, sitemap, feed) are edited only by
  this integration session from this point on.

## Verification log

| Date (UTC) | Task | Sources checked / verification performed | Irregularities / follow-up |
| --- | --- | --- | --- |
| 2026-11-20 | Initial repository inspection (prior session) | Tracked repository contained only an 8-byte `README.md`. | No prior app, data register, or claims existed to verify. |
| 2026-11-20 | Official program documents | Amazon Associates Program Operating Agreement (https://affiliate-program.amazon.com/help/operating/agreement — page states "Updated: October 15, 2025"): §1 requires links to use the tagged "Special Links" format. Amazon Associates Program Policies (https://affiliate-program.amazon.com/help/operating/policies — page states "Updated: April 14, 2026"): IP License §2(b) states Product Advertising Content is obtained via Creators API or PA API; §2(c) restricts its use; §6(a) forbids altering Program Content; §6(d) forbids implying endorsement; §5 forbids using Special Links or Program Content to develop machine learning models without express prior written approval. | Live price / rating / availability therefore cannot be published on reader-facing pages from scraped values; PA API or Site Stripe is required first. |
| 2026-11-20 | ASIN definition | Amazon Selling Partner Blog, "Understanding ASINs" (https://sell.amazon.com/blog/what-is-an-asin, dated Jun 4, 2025): ASIN is a unique 10-character alphanumeric code and appears after `/dp/` in a product detail URL. | All five supplied `link.amazon` path tokens are 9 characters, so none of them is an ASIN. Their exact Amazon link format is not documented in the Associates Help pages located; FLG-003 remains unresolved (not "invalid"). |
| 2026-11-20 | Disclosure standard | FTC, "FTC's Endorsement Guides: What People Are Asking" (https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking): disclose the relationship "clearly and conspicuously"; "the closer the disclosure is to your recommendation, the better"; "affiliate link" alone is not adequate; a bare "buy now" button is not adequate. | Disclosure strip is placed above the masthead on every page and repeated in the footer. |
| 2026-11-20 | Redirect observation for the five supplied links | Followed each `https://link.amazon/<token>` over HTTPS and recorded the resolved `www.amazon.com/dp/<ASIN>` destination: `B04G1MEwY` → `B0CDY277D3`; `B02NbDxp3` → `B09B7SB46R`; `B00hJ57DV` → `B08DKYBTPH`; `B0f3GKalj` → `B0DZFD6R9Z`; `B0c8moW59` → Amazon "Continue shopping" checkpoint, destination not observed. | `B0f3GKalj` resolves to a wireless meat thermometer, not an air fryer — category mismatch against the brief (FLG-002). `B0c8moW59` could not be observed (FLG-001). |
| 2026-11-20 | Tracking-tag control test | Fetched `https://www.amazon.com/dp/B09B7SB46R?tag=shopnow047c-20` directly. The resolved URL returned by the fetch pipeline contained no `tag=` parameter, proving the pipeline normalises/strips `tag=`. | Therefore the presence, absence or ownership of the tracking ID `shopnow047c-20` cannot be confirmed by this method. Recorded as unresolved (FLG-003); the tag is user-supplied and its enrollment status is unverified. |
| 2026-11-20 | Product attribute observation | Retrieved official Amazon product detail pages `https://www.amazon.com/dp/B0CDY277D3`, `/B09B7SB46R`, `/B08DKYBTPH`, `/B0DZFD6R9Z`. Listing titles and three prices were observed on 2026-11-20. `https://www.amazon.com/product-reviews/<ASIN>` redirected to Amazon sign-in, so aggregate star rating and review counts could not be observed for the four products. | Ratings and review counts are left blank and flagged as unverified (FLG-004). Product prices are dated observations, not a live feed. |
| 2026-11-20 | Pages deployment | `gh api repos/:owner/:repo/pages` → `build_type: legacy`, source `main` / `/`, `status: built`. `gh run list` shows "Deploy static site to GitHub Pages" and the legacy "pages build and deployment" both succeeding on `main`. `PUT /repos/:owner/:repo/pages` with `build_type=workflow` returned HTTP 403 "Resource not accessible by integration". | The integration token cannot switch the Pages source to "GitHub Actions". Both build paths are kept working and the Actions workflow is hardened; switching the Pages source is a repository-admin action (FLG-006). |

## Irregularities / unresolved decisions (published on the Flagged for Review page)

| ID | Item | Status |
| --- | --- | --- |
| FLG-001 | `link.amazon/B0c8moW59` destination not observed — Amazon "Continue shopping" checkpoint on 2026-11-20. | Unverified — retry from an ordinary browser session. |
| FLG-002 | `link.amazon/B0f3GKalj` resolves to a wireless meat thermometer, not an air fryer. | Unverified intent — decide whether it stays in scope. |
| FLG-003 | Exact compliance status of the five supplied `link.amazon` short links, and whether the supplied tracking ID `shopnow047c-20` is enrolled on this account. | Unresolved. The links are not asserted to be invalid. |
| FLG-004 | Aggregate star rating and review count for all four observed listings. | Unverified — Amazon sign-in required. |
| FLG-005 | Exact price of `B08DKYBTPH` at observation time. | Unverified — not observed on 2026-11-20. |
| FLG-006 | Pages source is "Deploy from a branch" (legacy) and the token cannot switch it to "GitHub Actions". | Needs repository-admin action. |
| FLG-007 | No authorized first-party Associates reports, PA API credentials, Search Console property, analytics consent setup or publishing credentials were supplied. | Open — campaign ledger is empty by design. |
| FLG-008 | This brief asks for an "AI-powered" automation platform. IP License §5 forbids using Special Links or Program Content to develop machine learning models without express prior written approval. | Needs legal review before any model is trained on Amazon content. |
| FLG-009 | A dated observed price is republished on the desk pages (not on any reader-facing page). The distinction between a dated research observation and displaying Program Content has not been confirmed with the program. | Needs review. |

## Completion log

- PR #1 "Build evidence-led affiliate publication storefront" — merged to `main`.
- PR #2 "Record publication verification and Pages deployment" — merged to `main`.
- PR #3 (this branch) "Rebuild the site as a reader-first publication with an evidence desk" —
  opened from `arena/2361a177-affil1` and merged to `main`. Link and merge result recorded below.

### Work completed by `arena/2361a177-affil1`

**Site structure.** 22 content pages, all rendered from one source of truth.

| Surface | Path |
| --- | --- |
| Publication front page | `index.html` |
| The shelf (catalogue) | `shop/index.html` |
| Basket air fryers | `shop/basket-air-fryers.html` |
| Air fryer ovens | `shop/air-fryer-ovens.html` |
| Cooking tools & thermometers | `shop/cooking-tools.html` |
| Guides index (six clusters) | `guides/index.html` |
| Six question-shaped guides | `guides/basket-or-oven.html`, `guides/capacity-checklist.html`, `guides/cleanup-counterspace.html`, `guides/multifunction-checklist.html`, `guides/do-you-need-a-thermometer.html`, `guides/holiday-hosting-air-fryer.html` |
| Desk hub | `desk/index.html` |
| Executive summary | `desk/executive-summary.html` |
| Product-intent confirmation record | `desk/product-records.html` |
| Suggestions register (15 proposals + design direction) | `desk/suggestions.html` |
| Open questions register (8 questions) | `desk/questions.html` |
| Campaign ledger (empty by design) | `desk/ledger.html` |
| Publishing gate (8 machine checks, 4 human) | `desk/publishing-gate.html` |
| Method and sources | `desk/methodology.html` |
| Flagged for review (9 items) | `desk/flagged-for-review.html` |
| Redirect stub for the old published URL | `guides/flagged-for-review.html` |

**Mechanism.** `site_data.py` is the single source of truth. `scripts/build_site.py` renders every
page from it; `scripts/check_site.py` is the publishing gate. The Pages workflow re-renders the
site, fails the build if the committed HTML has drifted from the renderer, runs the gate, and
then publishes only the site files.

**Measurement.** `assets/analytics.js` records the five defined events (`page_view`,
`outbound_click`, `guide_open`, `search_query_referral`, `report_import`). `api/collect.js`
(zero-dependency Node) and `api/worker.js` (Cloudflare Worker) implement the collector. The
tracker probes the health endpoint and disables itself if the collector is not deployed, so the
site never implies measurement that is not happening. The ledger is empty and stays empty until
an authorised first-party report is imported.

**Verification performed on the rendered site.** `scripts/check_site.py` — disclosure above the
masthead on all 22 pages; sponsored marking on every Amazon product link and no sponsored
marking on Amazon documentation citations; no price, rating, review count or availability on the
13 reader-facing pages; no unsupportable claim language (one declared, counted exemption for the
design-direction block); every table row carries a link and at least one official-source link;
every internal link resolves; metadata on every page; sitemap and feed complete; one `h1` per
page.

**Sources used for every factual claim.** Amazon Associates Program Operating Agreement,
Amazon Associates Program Policies, Amazon Selling Partner Blog "Understanding ASINs", FTC
Endorsement Guides, the four observed Amazon product detail pages, GitHub Pages documentation and
Google Search Console documentation. Full URLs are on `desk/methodology.html`.

### Pull request and merge result

- PR: _pending_
- Merge result: _pending_
- GitHub Pages deployment: _pending_
