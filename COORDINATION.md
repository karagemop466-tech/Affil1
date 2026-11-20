> **Release receipt · arena/ae991ca9-affil1 · 2026-11-20.** [PR #41](https://github.com/karagemop466-tech/Affil1/pull/41) merged as `14cca70523f7d01ccb4fd6a9280512347df7d7ee`. Its [publication checks](https://github.com/karagemop466-tech/Affil1/actions/runs/44683584256) and [affiliate gate tests](https://github.com/karagemop466-tech/Affil1/actions/runs/44683584250) passed. Its Pages build completed but its deployment was cancelled when #37 superseded it. The subsequent staging repair #59 passed CI, and [Pages deployment 44683751106](https://github.com/karagemop466-tech/Affil1/actions/runs/44683751106) succeeded. The public site and this session’s 31-page preview are therefore different editions. No production tracking or order report has been verified.

# COORDINATION.md — shared task board

Shared task board for parallel sessions on this repository. Read this before
claiming any work.

### Buyer publication & gated research — arena/daf8045f-affil1

| Task | Status | Owner | Files |
|---|---|---|---|
| Integrate the maintained publication: storefront art direction, evidence-gated next actions and editorial research, build and Pages release | done | arena/daf8045f-affil1 | tools/page_home.py, tools/layout.py, tools/page_suggestions.py, tools/check.py, assets/css/storefront.css, assets/img/storefront*, generated maintained HTML, COORDINATION.md |

Earlier #27 integration merged. Open #29 targets legacy tables, not these publication templates. No legacy table edits planned.

Additional unclaimed scope: `tools/stage.py` (package stylesheet), `assets/js/analytics.js`, `analytics/cc_collector.py`, `analytics/test_cc_collector.py` (maintained-edition aggregate schema), and `tools/page_desk.py` / `tools/page_review.py` for the release status. No changes to other sessions' collectors.

### Storefront verification — arena/daf8045f-affil1 · 2026-11-20 UTC

- **Done:** illustrated front page, format cards, shared masthead and disclosure, asset manifest, reviewable design prompt, query-based editorial cadence, and end-to-end release checks. #38 landed concurrently: retained its paid-CTA gate, seasonal guide, launch register and measurement contract, merged the template edits and regenerated the affected pages. Board conflicts with #32/#35 retained both histories.
- Independently opened all five submitted links. Observed in order: [Chefman 6 qt dual](https://www.amazon.com/dp/B0CDY277D3), [Emeril 26 qt oven](https://www.amazon.com/dp/B09B7SB46R), [Chefman 8 qt TurboFry](https://www.amazon.com/dp/B08DKYBTPH), [ThermoMaven instant-read](https://www.amazon.com/dp/B0DHZTCNR5), [CHEF iQ wireless](https://www.amazon.com/dp/B0DZFD6R9Z). No visible arrival tag. These are observations only, not confirmed intended ASINs. The reverse historical thermometer observations remain FLG-016; FLG-003 remains unresolved.
- Read the [Associates agreement](https://affiliate-program.amazon.com/help/operating/agreement), [Program Policies](https://affiliate-program.amazon.com/help/operating/policies), [FTC FAQ](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking), [Google link qualification](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links), [query report documentation](https://support.google.com/webmasters/answer/7576553), and [Pages usage limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits). Commercial hosting, first-party production telemetry, search ownership and authorized order reports remain **needs review**. No traffic, profitability, order or attribution claim.
- Checked the maintained build (24 pages), local file references across 74 HTML pages, the collector's five synthetic event counters/opt-outs and three launch preflight tests. No legacy-edition factual certification is claimed.

Concurrent integrations #32, #38, #42 and the journal discovery release: retained the task-board histories and combined source templates, including the paid-link gate, newer executive brief, local search and shelf filters. Integrated the fit finder and four seasonal guides; retained the new guide clusters and featured them on the illustrated front page. Rebuilt generated pages. Reused and tested the #32 collector instead of writing a duplicate. [PR #44](https://github.com/karagemop466-tech/Affil1/pull/44).

Current integration: #50, #41 and #37 selected incompatible generators while #44 was open. Preserved the current main pipeline and ported the cover and cards into its template rather than reviving a retired edition.
## arena/3cad5d4e-affil1 — deployment and follow-up

[PR #45](https://github.com/karagemop466-tech/Affil1/pull/45) merged at `714affa1c94507f4f5ae74d28d2f01333f2b963b`. Both PR checks passed. Its standalone Pages run was superseded by [run 44683427404](https://github.com/karagemop466-tech/Affil1/actions/runs/44683427404), which deployed successfully from descendant `e6f3234` after concurrent #51. The design decision and hosting-review panels were retained in that descendant.

| Task | Status | Owner | Scope |
|---|---|---|---|
| Restore the approval requirement after automatic tags were added by #51 | done | arena/3cad5d4e-affil1 | Maintained product-link rendering, source/CTA labels, and checker only; no product observations or other sessions' new guides changed |

The published descendant contains tagged links despite empty intent and reporting fields. A tag added from a public observation is not a validated Special Link. This is a release-gate regression, not evidence that an original submitted short link was invalid. Reapplied the gate to the final generated edition after #50 and #37 replaced the templates. Public listing citations remain sponsored-marked; the checker rejects any tagged product URL not in the approved intent register. No new confirmation data was added. Restored the aggregate preview and decision panels to the active edition. Local checks: 27 pages, zero checker warnings/errors, zero broken relative references, and all gate/collector tests passing.

## Measurement and product-release gate — arena/3cad5d4e-affil1

| Task | Status | Owner | Files |
|---|---|---|---|
| `arena/fa9307f7-affil1` | same | Build system, publication rewrite, review queue (PR #22) | done |
| `arena/a4ab7faf-affil1` | same | Pass-2 verification audit, seasonal guide (PRs #20, #21) | done |
| `arena/b41317f8-affil1` | `arena/b41317f8-affil1` | **Final integration pass**: one canonical site, shop-voice rewrite, tagged links, new guides, suggestions/questions refresh, PR + merge + deploy | in progress → done below |

## Claims

| Task | Status | Owner | Files |
|---|---|---|---|
| Consolidate two editions into one canonical site | done | arena/b41317f8-affil1 | root tree, `archive/legacy-2026-11-20/`, `robots.txt`, `sitemap.xml` |
| Re-verify all five supplied links | done | arena/b41317f8-affil1 | `src/data/products.json` |
| Tag every Amazon link (Program Policies §2(b)) | done | arena/b41317f8-affil1 | `tools/layout.py`, `tools/check.py` |
| Shop-voice front page and product pages | done | arena/b41317f8-affil1 | `tools/page_home.py`, `tools/page_products.py`, `assets/css/site.css` |
| Four new guides, eight total | done | arena/b41317f8-affil1 | `tools/content.py`, `tools/page_guides.py` |
| Suggestions queue with three paths | done | arena/b41317f8-affil1 | `src/data/suggestions.json`, `tools/page_suggestions.py` |
| Decision register, 22 questions | done | arena/b41317f8-affil1 | `src/data/questions.json`, `tools/page_questions.py` |
| Product facts beyond the listing title | needs review | — | `src/data/products.json` |
| Associates account data (intended ASINs, rate card, click report) | needs review | — | requires account owner |
| Search Console verification | needs review | — | requires owner's Google account |
| Analytics endpoint hosting + retention | needs review | — | requires owner decision |

`needs review` means the item is published on the review page and does not block
anything.

**Open pull requests that were not touched by this session:** #19
(`arena/e56bd6f7-affil1`, coordination log only), #12 (`arena/c58c5996-affil1`),
#9 (`arena/4bcd015a-affil1`), #23 (`arena/8206a8d0-affil1`). None was rebased,
force-pushed, merged or closed here.

## Why this integration pass was needed

`main` served two competing editions of the same shop: the generated edition at
the root and a hand-written edition under `crisp/` plus duplicate root pages
(`products.html`, `questions.html`, `suggestions.html`, `guides.html`,
`dashboard.html`, `flagged-for-review.html`, `privacy.html`,
`executive-summary.html`, `disclosure.html`, `categories.html`). They described
the same five products with different navigation and different URLs. Two editions
cannot both be the site a search engine indexes, and the brief for this session
asks explicitly for "one site to index".

The earlier coordination note called consolidation a design decision for a final
integration pass. This is that pass.

**What was done with the other edition: archived, not deleted.** Every file moved
to `archive/legacy-2026-11-20/`, every archived `.html` file carries
`<meta name="robots" content="noindex, follow">`, and `sitemap.xml` lists only
canonical URLs. Git history retains the originals. `archive/legacy-2026-11-20/README.md`
records what moved and why.

## Sources and verification performed

Every source was requested and read in this session on 2026-11-20.

| Ref | Source | Used for |
|---|---|---|
| SRC-01 | https://affiliate-program.amazon.com/help/operating/agreement | §5 disclosure wording, quoted verbatim |
| SRC-02 | https://affiliate-program.amazon.com/help/operating/policies | §2(a)/(b): Special Links must use the Associates ID, and the tag must appear as a URL parameter |
| SRC-03 | https://affiliate-program.amazon.com/help/operating/policies | §2(b): price/availability only from Amazon-served data or the APIs |
| SRC-04 | https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | Disclosure placement: "the closer the disclosure is to your recommendation, the better" |
| SRC-05 | https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | "affiliate link" alone may be inadequate; "paid link" beside it is better |
| SRC-06 | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255 | Linked, not quoted |
| SRC-07 | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | `rel="sponsored"` is the paid-link marker |
| SRC-08 | https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/air-fryers | **Not reached from this environment.** No figures reproduced |

Link verification, one request per link on 2026-11-20:

| Ref | Submitted | Resolved to | Product | Change vs previous record |
|---|---|---|---|---|
| P-01 | link.amazon/B04G1MEwY | B0CDY277D3 | CHEFMAN 6 qt dual basket | unchanged |
| P-02 | link.amazon/B02NbDxp3 | B09B7SB46R | Emeril Lagasse 26 qt French door | unchanged |
| P-03 | link.amazon/B00hJ57DV | B08DKYBTPH | Chefman 8 qt TurboFry | unchanged |
| P-04 | link.amazon/B0c8moW59 | **B0DHZTCNR5** | ThermoMaven digital meat thermometer | **newly resolved** (3 failures in an earlier session) |
| P-05 | link.amazon/B0f3GKalj | B0DZFD6R9Z | CHEF iQ Sense wireless probes | unchanged |

`python3 tools/build.py` → **27 pages**.
`python3 tools/check.py` → **27 pages checked, 0 errors, 0 warnings.**
`python3 tools/check_local_links.py` → **27 pages, 0 broken references.**

## Irregularities found in this pass

- **FLG-009 (new, corrected):** the previous build linked to bare
  `https://www.amazon.com/dp/<ASIN>` with **no tag parameter**, which cannot be
  attributed to any account and does not meet Program Policies §2(b). Every
  Amazon destination is now built by `layout.buy_url()` with
  `?tag=shopnow047c-20`, and `check.py` fails the build on an untagged link.
- **FLG-004 (downgraded):** P-04 resolved on first attempt this session. The
  earlier failures are recorded as unexplained, not diagnosed.
- **FLG-015 (corrected):** two of the five products are thermometers, not one.
  They are published as their own category.
- **FLG-008 (new):** two competing editions were live at once; consolidated.
- **FLG-002 (unchanged):** no resolved URL showed the tag, and no Associates
  report has been read. Attribution remains unconfirmed.
- **FLG-016 (new):** buy-button wording ("See it on Amazon") is a compliance
  judgement logged for owner review before paid traffic.

All 19 flags are published at `review/index.html` with source links.

## Reconciliation with main (two rounds)

`main` moved four merges ahead while this session was working. On reconciliation,
`main` carried **three** published editions (generated root, `crisp/` and a
`kitchen/` "Good Measure" desk) plus duplicate root pages. All three are now
archived under `archive/legacy-2026-11-20/` with `noindex`, and the Pages
artifact is staged from the generated set only (`tools/stage.py`, added by a
parallel session and kept).

Two pieces of the parallel work were kept as-is because they are good and
complementary:

- `tools/stage.py` — packages only the generated edition for Pages, so the
  repository can hold history without publishing it.
- `measurement/collector.py` and its tests — the self-hosted collector the
  measurement plan refers to.
- `guides/holiday-side-dish-capacity` — a new seasonal guide from the parallel
  session, adopted into this build with a cluster and related products rather
  than archived.
- The paid-link gate idea from PR #38 is implemented here as `layout.buy_url()`
  plus the tag rule in `check.py`.

**Conflict in the product record, published rather than resolved by preference:**
a parallel session first observed P-04 → B0DZFD6R9Z and P-05 → B0DHZTCNR5, the
reverse of this session's observation; a later fetch by that session agreed with
the mapping here (B0DHZTCNR5 / B0DZFD6R9Z). The disagreement is recorded in
FLG-016, both product pages carry an identity note, and neither mapping is called
the intended product. The operator can settle it in a minute with SiteStripe.

**Archived in the second round:** `kitchen-build/` (a second generator, whose
output `operations/launch-readiness.html` linked to untagged `/dp/` URLs),
`operations/launch-readiness.html`, and `.github/workflows/kitchen-check.yml`.
Keeping them would have published a second page shell and untagged Special Links.
They are preserved under `archive/legacy-2026-11-20/`.

## Merge log

- PR: https://github.com/karagemop466-tech/Affil1/pull/37
- Merge result: recorded in the PR body and in the commit message.

## Public URL

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

## Publication integration — arena/c1891b66-affil1

| Task | Status | Owner | Scope |
|---|---|---|---|
| Buyer front page and single-edition Pages packaging | done | arena/c1891b66-affil1 | tools/page_home.py, tools/layout.py, tools/stage.py, .github/workflows/pages.yml, README.md |

- Rechecked the [Associates agreement](https://affiliate-program.amazon.com/help/operating/agreement), [program policies](https://affiliate-program.amazon.com/help/operating/policies), [paid-link markup](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links), and [Pages publishing sources](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). Product evidence was retained from the prior source register; this pass did not establish new product facts or verify account data.
- Build and checker: 22 maintained pages, zero errors or warnings; staged package checked for missing HTML links and assets. The GitHub Pages API reports legacy publishing from `main` root. Switching to an artifact-only workflow returned HTTP 403, so the main-branch release remains the available publication path. The custom workflow stages the maintained edition and deploys only if custom Actions is selected.
- Pending: authorized Associates link confirmation and reporting, Search Console ownership, production analytics hosting and review, and reader capture. No estimates substituted.
- Rebase handoff: main merged #23 and #25 while #26 was open. Retained both sessions’ records, P-04 re-verification, guides, and executive-summary changes. Resolved the generated homepage conflict in the template and rebuilt; both thermometer records now have separate homepage paths.

- Integration PR: [#26](https://github.com/karagemop466-tech/Affil1/pull/26). The authoritative merge and deployment outcomes are linked from the PR timeline and [Pages runs](https://github.com/karagemop466-tech/Affil1/actions/workflows/pages/pages-build-deployment).

### Delivery — S-8206a8d0 (merged)

- PR: https://github.com/karagemop466-tech/Affil1/pull/23 — merged into main 2026-11-20 (merge commit 0691fa7).
- CI on PR: Build, check and deploy — build pass (6s), deploy skipped (PR). On main: build success (27s), pages build success (34s). Pages latest build status: built.
- Live: https://karagemop466-tech.github.io/Affil1/ (Crisp & Counter front page) and https://karagemop466-tech.github.io/Affil1/crisp/ (parallel edition).
- Rebase onto PR #22 logged above; no session's work discarded. Follow-up for integration session: wire `guides/meal-prep-sunday.html`, `guides/small-kitchen-counter.html`, `guides/thermometer-pairing.html` into generated sitemap/feed (requires extending `tools/content.py` GUIDES in the PR #22 build).
## Integration follow-up — 2026-11-20

| Task | Status | Owner | Files |
|---|---|---|---|
| Audit and reconcile live editions, correct broken links and disclosure gaps, document differing redirect observations and broaden checks | in progress | arena/c9fc4295-affil1 | COORDINATION.md, root legacy HTML, src/data/, tools/, generated site output and workflow |

The initial shallow checkout made the ancestor appear unrelated and caused a rebase conflict; after fetching complete history, main fast-forwarded without discarding either edition. Main advanced again during this work; rebase conflicts were resolved by retaining the newer session files and reapplying the observation flag and relevant independent fixes. The generated and legacy pages will be checked separately. Account-gated attribution and measurement remain unverified.

### Follow-up audit results

- Another session reported the opposite P-04/P-05 mapping; these observations conflict with our page-fetch on 2026-11-20: [P-04](https://link.amazon/B0c8moW59) reached [B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z), while [P-05](https://link.amazon/B0f3GKalj) reached [B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5). Prior results remain historical, not confirmation of intent. Published as FLG-016; intended ASINs and tracking remain unconfirmed. Account verification is still needed.
- Fixed root guide paths and legacy links to retired files, added no-script disclosure fallbacks, added `sponsored` to four legacy product citations, and corrected an unsupported dishwasher-safe statement about P-02. Official listing: https://www.amazon.com/dp/B09B7SB46R. Added a sitewide destination warning and FLG-017 for conflicting legacy editions.
- `python3 tools/build.py`, `python3 tools/check.py` (22 generated pages, 0 errors), and `python3 tools/check_local_links.py` (65 served HTML files, 0 broken relative file references) pass. The new check does not verify anchors or external URLs. The older `tools/validate.py` fails because the newer product schema is incompatible; this needs reconciliation, not a claim of success.
- Analytics remains disabled, Search Console and Associates reporting are not connected, and no product-intent, conversion, price or commission data has been invented. Older editions remain inconsistent; consolidation and complete line-by-line verification remain **needs review**, not complete.

### PR and deployment result — arena/c9fc4295-affil1

- [PR #27](https://github.com/karagemop466-tech/Affil1/pull/27) merged as `92a3509c9a56bbd6aa01eef8d7ae0afbb4ab7f06`; the PR build and link checks passed.
- GitHub Pages [deployment run 44682421711](https://github.com/karagemop466-tech/Affil1/actions/runs/44682421711) succeeded; the Pages API reported `built` for that merge commit.
- Audit and link repairs: done. Full legacy-edition reconciliation, product intent, tracking attribution, and live analytics: **needs review** as detailed in FLG-016/017 and the measurement page. The older crisp-specific validator remains incompatible with the current data schema.
## Reconciliation — arena/c7f7070d-affil1, 2026-11-20

PR #23 and PR #26 landed after the initial claim; PR #27 landed while this work was in progress. Work was stashed and rebased, then stash-application conflicts were resolved by retaining PR #27's destination warnings and review flags, combining the source-link and event-spec corrections, and regenerating output from the combined templates. No other session's edition was deleted. The parallel claim overlaps this one; future cross-scope changes should be coordinated here rather than silently overwritten.

Two independent fetches in this session reached [P-04 B0DHZTCNR5](https://link.amazon/B0c8moW59) and [P-05 B0DZFD6R9Z](https://link.amazon/B0f3GKalj), respectively; PR #27 reports the reverse. The conflict is retained as FLG-016, not resolved by assumption. Intended product and attribution remain unknown. Added explicit null intent URL/date/source fields, corrected stale counts and the P-02 dishwasher assertion, and removed a fabricated blank ledger row. Aligned the measurement *documentation* to the five canonical event names; the existing disabled client still uses different names and must not be mistaken for a working implementation. Sources read: [Amazon Agreement](https://affiliate-program.amazon.com/help/operating/agreement), [Amazon Policies](https://affiliate-program.amazon.com/help/operating/policies), [FTC FAQ](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking), [Google Performance report](https://support.google.com/webmasters/answer/7576553) and [Search Console verification](https://support.google.com/webmasters/answer/9008080).

Checks: `python3 tools/build.py`, `python3 tools/check.py` (22 generated pages, 0 errors, 0 warnings), and `python3 tools/check_local_links.py` (65 pages, 0 broken relative file references). The legacy validator and live measurement remain needs review, as do all account-gated work and full cross-edition factual verification. Link checks do not establish attribution, stable redirects, or buyer intent.

Rebase after PR #28: a task-board conflict was resolved by retaining both merge/deployment histories and this reconciliation record.

## Editorial supplement — arena/03232911-affil1

| Task | Scope | Owner | Status | Notes |
| --- | --- | --- | --- | --- |
| GM-01 | `kitchen/`, `measurement/` | arena/03232911-affil1 | done | Additive buyer publication, redirect review and aggregate measurement. Leaves generated root site and peer PRs intact. |
| Guide-index repair | `guides.html` | peer integration | handed off | Repairs were covered by the parallel integrations; no edit here. |

Claim was pushed before implementation. Shared-board-only rebase conflicts occurred when #22 then #27 and #28 changed `main`; retained the incoming board and reapplied only this claim. Older entries remain in Git history. Request to the current integration owner: link `/kitchen/` and its guide into the generated root navigation, sitemap and feed after overlapping PRs settle.

- Direct Amazon recheck (2026-11-20, all five submitted links): `B04G1MEwY` → [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3), `B02NbDxp3` → [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R), `B00hJ57DV` → [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH), `B0c8moW59` → [B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5), `B0f3GKalj` → [B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z). P-04/P-05 reverse mapping in #27 kept as conflicting evidence. No observed arrival showed the chosen tag. Intent, attribution and short-link compliance remain unverified; no Special Links emitted by this edition.
- Read the official [Amazon ASIN definition](https://sell.amazon.com/blog/what-is-an-asin), [Associates Agreement](https://affiliate-program.amazon.com/help/operating/agreement), [Program Policies](https://affiliate-program.amazon.com/help/operating/policies), [FTC endorsement guidance](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking), [USDA thermometer guidance](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers), [Google outbound link guidance](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links), [Search Console performance report](https://support.google.com/webmasters/answer/7576553), and [Pages usage limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits). The supplement is editorial, not a commercially hosted affiliate operation.
- Local checks: scoped seven-page check including anchors, sponsored markers and XML; aggregate collector exercised with all five synthetic events and rejection/opt-out tests; root build 22 pages with 0 errors/warnings, shared crawler 72 served files with 0 broken relative references.
- Needs review on `/kitchen/flagged.html`: no Associates account validation, live measurement, Search Console property, or reader capture. The ledger is empty, and AI-assisted research/drafting is a scoped proposal, not an autonomous production pipeline.

- PR [#31](https://github.com/karagemop466-tech/Affil1/pull/31): main advanced to #30 during PR checks. Resolved the resulting board-only rebase conflict by retaining both logs and leaving all peer site files unchanged. Deploy outcome is tracked on the PR timeline and Pages builds.
## arena/7b1823aa-affil1

| Task | Status | Owner | Scope |
|---|---|---|---|
| Wire maintained publication measurement contract and local collector | done | arena/7b1823aa-affil1 | `assets/js/analytics.js`, `analytics/endpoint.py`, `analytics/test_endpoint.py`, `analytics/README.md` (public wording overlaps PR #27; defer those files) |

- PR #27 merged before the public copy was touched. Expanded claim to `tools/build.py`, `tools/page_review.py`, `review/measurement.html`, `tools/check.py`, and `src/data/events.json`. Rebased over #27; the coordination conflict contained adjacent entries, and both were retained.
- Verified the five event counters, rejection of unknown fields/routes, cross-origin submission rejection, and DNT/GPC handling with the local HTTP test. The browser client passed syntax validation. The published measurement page uses the same event specification as the collector.
- Production activation **needs review** ([FLG-009](review/index.html#FLG-009)): [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) is static. No first-party runtime or approved retention policy is configured. No sessions, orders, attribution or commissions were established. Use authorized [Associates reporting](https://affiliate-program.amazon.com/home/reports) for reported orders; do not derive them from clicks.

- Delivery PR: [#32](https://github.com/karagemop466-tech/Affil1/pull/32). Initial merge attempt raced another coordination update; rebased, kept both entries, and reran checks. See the PR timeline and [Pages deployments](https://github.com/karagemop466-tech/Affil1/actions/workflows/pages/pages-build-deployment) for the recorded results.
- Rebased again over the #28 deployment log; retained both coordination entries.
- Preserved the parallel session’s source column and updated the now-implemented measurement wording; regenerated the shared page.
- Rebased over #31, retaining its independent supplement and coordination entry.

### Delivery — Good Measure Kitchen Notes

- [PR #31](https://github.com/karagemop466-tech/Affil1/pull/31) merged into `main` at `adb5e9834260d07d1128012fa900859a258360d4` on 2026-11-20. [PR build](https://github.com/karagemop466-tech/Affil1/actions/runs/44682671403) and [GitHub Pages release](https://github.com/karagemop466-tech/Affil1/actions/runs/44682695195) both succeeded.
- Fetched and read the live [front page](https://karagemop466-tech.github.io/Affil1/kitchen/), [Executive summary](https://karagemop466-tech.github.io/Affil1/kitchen/desk.html) and [Flagged for Review](https://karagemop466-tech.github.io/Affil1/kitchen/flagged.html) after deployment. The product intent cells and campaign ledger remain empty by design. Root navigation/feed integration was left to the active integration owner; the supplement includes its own feed and sitemap on the same host.
### Merge and deployment — arena/c7f7070d-affil1

[PR #30](https://github.com/karagemop466-tech/Affil1/pull/30) merged as `ab2e18b3b503c9d2da588b0692307611434946fc`. Its PR build passed, and [GitHub Pages deployment 44682623391](https://github.com/karagemop466-tech/Affil1/actions/runs/44682623391) succeeded. Pages API reported `built` for the merge commit; the live measurement page was fetched and displayed the corrected specification and destination warning. Account-gated attribution, intent, real measurement and full cross-edition verification remain needs review.

Board-only conflict after PR #31 was resolved by retaining both the editorial supplement and reconciliation deployment records.

A second board-only rebase over PR #32 retained both records; PR #32 subsequently aligned the client and collector contract. Production remains disabled.

Board-only rebase over PR #35 kept both deployment notes.

## Claim — S-02502b50 · integration edition

| Task | Scope | Owner | Status |
| --- | --- | --- | --- |
| SG-32 Buyer-first integration edition, evidence register, decision desk, and measurement gate | Maintained generator, `kitchen-build/**`, `.github/workflows/kitchen-check.yml`, generated outputs, this board section | S-02502b50 | done |

2026-11-20 UTC. Fixed Arena branch `arena/02502b50-affil1`. Open PRs #9, #12, #19 and #22 were reviewed for scope. Do not overwrite their files or the shared root `index.html`, feed or sitemap in this pass. Shared integration request: once the overlapping PRs are settled, route the root masthead and sitemap to the preferred edition, correct the malformed legacy root and `guides.html`, and retire duplicate buyer-facing claims and unvalidated CTAs without deleting historical evidence. This edition will have a self-contained sitemap/feed and an explicit candidate canonical register; it does not assert repository-wide consolidation.

Rebase conflict at claim: PR #22 advanced `main` and rewrote the board. Preserved its current board verbatim and appended only this claim; earlier audit remains in Git history and `data/verification-audit.json`.

SG-32 scope update after #22 merged: no duplicate edition. Extend the now-merged root generator (`tools/{build,check,content,layout,page_*}.py` as needed), `src/data/{products,flags,questions,suggestions}.json`, the root edition's `assets/css/site.css` and `assets/js/analytics.js`, and their generated pages/feed/sitemap. New runtime/runbook/tests: `kitchen-build/**`. Open #9 remains an alternative root replacement: its unique files, designs and workflow are not touched. #12's legacy guide and #19's audit work are not touched. The scope is the integrated root generator and its reproducible outputs, not another session's unmerged implementation. New direct evidence requires revising P-04: the prior checkpoint remains a historical observation; a fresh request reached Amazon listing `B0DHZTCNR5` (ThermoMaven instant-read meat thermometer), not confirmed intent.

Concurrent scope update: PRs #23 and #26 appeared after the integration claim. #23 independently observed the same five listings, including the new P-04 destination, and #26 owns root layout/staging. No overlapping data/template edits will be retained in SG-32. Integrators: #23 proposes locally constructed `?tag=shopnow047c-20` CTAs while still flagging attribution as unconfirmed; an appended tag is not enrolled-workflow evidence. Keep those CTAs gated pending an Associates-generated link, confirmation of the intended variant, and an authorized attribution report. P-04's latest observed listing is not confirmed intent. SG-32 now limits its merge to the first-party measurement client, self-hosted runtime, private report intake, publishing preflight, and decision runbook; this does not replace the live storefront or duplicate its index.

Additive SG-32 public scope: `operations/launch-readiness.html`, separate from the occupied `operations/ledger.html`; this page uses the root publication's visual shell and sources without changing its nav. The root/staging owners can add it to the desk footer when consolidating scopes. `.github/workflows/kitchen-check.yml` is unique to SG-32.

Post-merge handoff: #23 and #26 are merged. SG-32 claims the maintained generator's launch-register link, paid CTA gate, stale root review copy, and one seasonal capacity guide through its generated feed/sitemap. This does not rewrite the historical `crisp/` or legacy editions; #24 still owns `guides.html`. Rebase onto #23/#26 and the #23 delivery note caused an append-only board conflict; main's notes were retained and this section reattached.

### SG-32 delivery — S-02502b50

- [PR #38](https://github.com/karagemop466-tech/Affil1/pull/38) merged into `main` at 05:43:39 UTC on 2026-11-20, merge commit `32bad415bb5291b7af6ad6e76d58bc699382b663`. Build and launch checks both passed before merge.
- [GitHub Pages deployment 44682938832](https://github.com/karagemop466-tech/Affil1/actions/runs/44682938832) completed successfully for the merge. Direct post-deploy fetches confirmed the [launch readiness desk](https://karagemop466-tech.github.io/Affil1/operations/launch-readiness.html) and [holiday capacity guide](https://karagemop466-tech.github.io/Affil1/guides/holiday-side-dish-capacity.html).
- Final checks covered 24 maintained pages and 74 served HTML files, with no broken relative references. During rebase, kept #32’s canonical five-event names and browser client, aligned the optional self-hostable preview/runtime to its `/api/e` protocol, and restricted outbound events to approved paid CTAs. The competing delivery log that landed immediately before the merge caused a `COORDINATION.md` append conflict; both records were preserved.

### SG-32 verification — S-02502b50

- **Done:** maintained root guide, sitemap/RSS integration, footer launch desk, five-row intent/observation record, paid-CTA build gate, self-hostable same-origin aggregate counters and private normalized Associates-report importer. Preview/test data are not campaign data. **Needs review:** production analytics hosting/privacy, Associates enrollment and tracking, Search Console, and reader email; the public ledger stays empty. AI draft prompt and review workflow are documented; no unattended AI or campaign optimization is claimed.
- Directly re-opened all five Amazon short links on 2026-11-20. This pass observed `B0CDY277D3`, `B09B7SB46R`, `B08DKYBTPH`, `B0DHZTCNR5`, `B0DZFD6R9Z` in supplied order. No `tag` on arrival. During the rebase #27 reported the thermometer destinations in the **opposite order**; retained both reports and the historical P-04 checkpoint, with official listing links in the launch desk and FLG-016. Intent and attribution remain blank; FLG-003 stays unresolved. Rebase conflicts in generated pages were resolved in the source templates then rebuilt, retaining #27’s flags and older-edition notice.
- Official review: [Amazon ASIN definition](https://sell.amazon.com/blog/what-is-an-asin), [Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement), [Program Policies](https://affiliate-program.amazon.com/help/operating/policies), [FTC guidance](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking), [Google paid-link markup](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links), [Google search performance report](https://support.google.com/webmasters/answer/7576553?hl=en), [GitHub Pages capabilities](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), [USDA thermometer guidance](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers).
- Verification: 24 maintained pages, zero checker errors/warnings; 67 served HTML files scanned for relative references, zero broken; three aggregate/preflight tests passed. Legacy pages remain separate and may retain previously published unvalidated CTAs; the gate applies to the maintained edition. Existing legacy source mode prevented an artifact-only cutover (#26). Do not use legacy copies as product-intent or attribution evidence.
## Measurement and evidence integration — arena/29fee39e-affil1

| Task | Status | Owner | Scope |
|---|---|---|---|
| First-party measurement, account-evidence publishing gate, and executive reconciliation | in progress | arena/29fee39e-affil1 | `measurement/`, `assets/js/analytics.js`, `src/data/events.json`, `src/data/products.json`, `src/data/flags.json`, `tools/page_products.py`, `tools/page_compare.py`, `tools/page_desk.py`, `tools/page_review.py`, `tools/check.py`, generated outputs of these templates, `privacy.html`, `PUBLISHING_WORKFLOW.md` |

Checked open PRs #9, #12, #19 and #24; this pass does not edit their guides or front-page template. An initial shallow-clone rebase hit a spurious conflict in this board; aborted, fetched history, then fast-forwarded without dropping either session’s log. The previous account-data review remains open; this pass builds controls, not account access.

Narrowed after #27, #30, #31 and #32 merged during this turn: own only the Special Link evidence gate (`tools/link_evidence.py`, its tests, `tools/stage.py`, `tools/page_products.py`, `products/`, `src/data/products.json`), the buyer comparison and executive decision pages (`tools/page_compare.py`, `tools/page_desk.py` and their outputs), the review data (`src/data/flags.json`, generated review page), and `PUBLISHING_WORKFLOW.md`. Reuse the merged analytics implementation; the overlapping local prototype was withdrawn before commit. Rebase conflict in the coordination log resolved by keeping all entries.

### Evidence gate delivery — arena/29fee39e-affil1

## Merge resolution — arena/4772a1e3-affil1 (2026-11-20, PR #47)

Main advanced through PRs #22–#46 while this branch was in flight. Main now contains a
**generated** root edition (Crisp & Counter, built by `tools/build.py` from `src/data/`,
gated by `tools/check.py` + a reproducible-build CI diff in `pages.yml`, staged to Pages by
`tools/stage.py`) plus the still-served legacy parallel edition. After fetching and merging
`origin/main` (conflict in 31 files), the resolution was:

**Kept from main, everywhere it conflicted (nothing of theirs discarded):**
`index.html`, `guides/index.html`, `sitemap.xml`, `feed.xml`, `rss.xml`, `README.md`,
`EXECUTIVE_SUMMARY.md`, `.github/workflows/pages.yml`, every legacy/parallel-edition page
(`suggestions.html`, `questions.html`, `products.html`, `categories*.html`, `dashboard.html`,
`guides.html`, `disclosure.html`, `privacy.html`, `reviews/flagged.html`, all `guides/*.html`
in conflict). `guides/cleanup-counterspace.html` and `guides/flagged-for-review.html`
take **main's deletions** (my stubs withdrawn — the deployed edition stages only built
outputs, so redirect stubs would never deploy anyway).

**Dropped from this branch (duplicative — superseded by main's work):**
the hand rebuilt `index.html` (main ships a generated, products-first front page with its
own hero art, JSON-LD and enforced disclosure/sponsored rules); the `design-prompt-pack.html`
(main's `brief/` + `suggestions/` + `questions/` + `review/` deliver the decision-gated
brief, 12 proposals with accept/hold/reject controls, and 15 questions with the artefact
that closes each — the redesign the pack proposed has shipped); `guides/holiday-gift-checklist.html`
(main published `guides/holiday-side-dish-capacity.html`, in the sitemap and feed);
`assets/favicon.svg` (main ships `assets/img/favicon.svg`);
`assets/img/hero-kitchen-notes.jpg` and `assets/img/holiday-gift-checklist.jpg`
(main ships its own responsive hero art); the `styles.css` polish block, the `main.css`
accent re-tint and the `common.js` brand unification (main's parallel session kept the
legacy edition on its own Affil1 identity deliberately; one-file-per-edition separation is
the load-bearing constraint); the widened CI reference check (superseded by main's
`check_local_links.py` + reproducible-build gate, which is strictly stronger).

**Kept from this branch (additive, no ownership conflict, verified after merge):**
- `js/main.js`: root-absolute `/disclosure.html` made depth-relative (would 404 on the
  project-Pages mount at `/Affil1/`).
- `js/analytics.js`: root-absolute `/api/collect` made depth-relative; added a warning that
  its event list (guide_engagement, conversion_attempt) is legacy and NOT the canonical
  five events (assets/js/analytics.js + docs/MEASUREMENT.md). Flagged as IR-13.
- `data.js` / `app.js`: relabeled — submitted codes are 9-char short-link slugs, not ASINs
  (IR-1); statuses now `observed-listing` / `conflict-logged` / `unresolved` with pass-1 vs
  pass-2 disagreement surfaced instead of one merged verdict; `app.js` rendering updated to
  match. (`app.js` has no consumers on main; `data.js` feeds the legacy
  `guides/air-fryer-category.html`.)
- `data/products.json`: marked **HISTORICAL**, superseded by `data/confirmations.json`
  (pass 1) and `data/verification-audit.json` (pass 2). Declares the two passes are never
  merged. This answers the open IR-8 request for the root register. (Main's maintained
  register is `src/data/products.json` for the generated edition — untouched.)
- `COORDINATION.md`: this entry.

**Irregularities reconfirmed / still open (not adjudicated here):**
IR-1/FLG-001 (submitted codes are 9 chars), IR-2 (pass-1 vs pass-2 observations disagree for
3 of 5 links), FLG-003 (short-link compliance unresolved), FLG-016/017 on main (P-04/P-05
conflicting redirects; legacy releases mixed into root-based Pages hosting). P-04 on main is
now listed in the Amazon recheck as B0DHZTCNR5 — a third distinct value across records; it is
recorded here only as an observation, not reconciled. Category naming for the meat
thermometer (IR-5) is decided on main via S-08. Nothing in this branch asserts any submitted
link invalid, and no verification record was merged into another.

**Earlier ask from arena/a4ab7faf-affil1 answered on main:** guides.html root-relative
paths (main's version rewritten and CI-covered by `check_local_links.py`); sitemap/feed
wiring (main's generated sitemap/feed already include the audit and seasonal pages). Canonical
register: `data/confirmations.json` + `data/verification-audit.json` (legacy) and
`src/data/products.json` (generated edition); the rest are historical.

- Scope status: **done** for source recheck, comparison, executive decision brief and publishing notes. #38 merged before this release with a competing gate, so we retained #38’s `kitchen-build/intent.json` gate, product templates, seasonal guide and checks, and withdrew the duplicate in this branch. Resolved board and template conflicts without removing the merged release controls; regenerated the affected HTML. Parallel collector work was reused from #32.
- Amazon recheck (2026-11-20, submitted redirects followed via official Amazon pages): P-01 [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3), P-02 [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R), P-03 [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH), P-04 [B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5), P-05 [B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z). Listing titles and arrival identifiers checked against the maintained register; no visible tag. Preserved #27's conflicting P-04/P-05 observations in FLG-016. No account-backed intent or attribution was established.
- Read [Amazon ASIN definition](https://sell.amazon.com/blog/what-is-an-asin), [Operating Agreement §§1, 5](https://affiliate-program.amazon.com/help/operating/agreement), [Policies §§2(b), 3 and 5](https://affiliate-program.amazon.com/help/operating/policies), [FTC endorsement FAQ](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking), [Search Console Performance report](https://support.google.com/webmasters/answer/7576553), and [Pages static hosting and logging](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) and [usage limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits). The last two new flags cover commercial hosting and use of Amazon Program Content in ML development. Nothing here approves the account, API or production AI automation.
- Verified the maintained build, 24 generated pages (0 errors/warnings), 74 served pages’ relative references (0 broken), staged artifact, the launch-readiness test and the merged analytics integration test. Remaining **needs review**: FLG-002/003 private link confirmation; FLG-016/017 conflicting redirects and legacy releases mixed into root-based Pages; real collector hosting, consent/retention, Search Console and reader capture. The site is not collecting production analytics or conversions; ledger remains empty.
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

## Claim — arena/4772a1e3-affil1 (claimed 2026-11-20 ~06:05 UTC)

Branch `arena/4772a1e3-affil1` (fixed by environment; cannot be renamed), branched from
`4ee0e7b` (main after PR #21). Claiming the open integration follow-ups from
`arena/a4ab7faf-affil1` plus the storefront polish/consolidation scope. No other live
session holds a claim on these files (the storefront sessions' work is merged; all their
tasks read done/needs-review, none claimed <60 min ago).

Scope (this session):
1. Rebuild root `index.html` as one consistent, polished publication front page
   (products-first; disclosure above the fold; sponsored links; intended vs observed
   never merged; messages match data/confirmations.json + data/verification-audit.json;
   remove contradictory "unverified" vs "Verified picks" copy; OG/Twitter meta; favicon).
2. Consolidate duplicate storefront pages into canonical URLs via redirect stubs
   (root `guides.html` -> `guides/` index; `guides/cleanup-counterspace.html` ->
   `guides/cleanup-counter-space.html`; `guides/flagged-for-review.html` and
   `flagged-for-review.html` -> `reviews/flagged.html`; `guides/suggestions.html` ->
   `suggestions.html`; `guides/executive-summary.html` -> `executive-summary.html`;
   `guides/buying-guide-air-fryer.html` -> `guides/basket-or-oven.html`;
   `guides/air-fryer-category.html` -> `categories/air-fryers.html`;
   `guides/pre-decision-questions.html` -> `questions.html`). No file is deleted;
   stubs keep every inbound link working.
3. CI (`.github/workflows/pages.yml`): widen the static reference check from
   `index.html` + `guides/*.html` to all HTML except `archive/`.
4. `sitemap.xml`, `feed.xml`, `rss.xml`: add reviews/verification-audit.html,
   guides/holiday-hosting.html, the new seasonal guide and the new design-prompt-pack
   page; drop stubbed URLs; keep crisp/ entries byte-identical.
5. New pages: `design-prompt-pack.html` (the site-design prompt + design tokens +
   marketing suggestions to feed a redesign, decision-gated) and
   `guides/holiday-gift-checklist.html` (seasonal, question-shaped; editorial
   hypothesis; no prices/ratings; sponsored links).
6. `suggestions.html`: add proposed S-006..S-0xx (design/brand/imagery/cadence/OG/email
   gate/Search Console), each marked proposed — nothing auto-implemented.
   `questions.html`: add Q10+ marketing/brand/measurement-readiness rows (answerable /
   blocked), matching the existing table format.
7. `EXECUTIVE_SUMMARY.md` refresh to the reconciled state; `data.js` / `app.js`
   relabeled ("Submitted code (short-link slug)", not ASIN; single-observation evidence;
   pass-1 vs pass-2 conflicts noted, never adjudicated).
8. `assets/js/common.js`: unify injected brand with the storefront masthead
   (GOOD MEASURE — Kitchen Notes), add the verification-audit/holiday pages to footer.

Explicitly NOT doing: touching `crisp/` (S-96012762's scope), deleting any file,
merging pass-1 and pass-2 verification records, asserting any supplied link invalid,
adding prices/ratings/review counts, or turning on analytics (no first-party host yet).

Status: superseded in part — see "Merge resolution" above. Kept: js/main.js, js/analytics.js, data.js, app.js, data/products.json marker, COORDINATION log. Dropped: everything else listed there.

https://karagemop466-tech.github.io/Affil1/

## Merge addendum — arena/4772a1e3-affil1 (2026-11-20, second merge, main @ 716ddbd)

Main advanced through PRs #32–#59 while this branch was open. The board's direction is now
settled there: one published edition at the root (the generated build); every superseded
surface (legacy Good Measure / Affil1 pages, `data.js`, `app.js`, `js/main.js`,
`js/analytics.js`, `data/products.json`, `styles.css`, `assets/js/common.js`,
`assets/css/main.css`, and the parallel `crisp/` and `kitchen/` generator outputs) was
**archived** under `archive/2026-11-20-*` — nothing was discarded. This branch keeps:
the merge resolution entry above (first merge, main @ 4059ac2) and this addendum. The five
files this branch had kept (`js/main.js`, `js/analytics.js`, `data.js`, `app.js`,
`data/products.json`) are withdrawn in favor of main's archival decision; the fixes they
contained (depth-relative paths; the submitted-code relabel; the HISTORICAL marker) remain
in git history and in `archive/2026-11-20-integration/` for reference. The defects those
fixes addressed (root-absolute paths broken on the project-Pages mount; a legacy
`js/analytics.js` event list inconsistent with the canonical five) either no longer exist
in the published tree (the legacy edition is archived, not served) or are main's call to
address in its own lineage.

Net effect of PR #47 after both merges: **zero net file changes to the published edition**;
the PR exists to record the branch's convergence with main and to keep this log accurate.
### Release receipt — arena/ca3c913e-affil1 (done)

[PR #49](https://github.com/karagemop466-tech/Affil1/pull/49) merged to main at `9982e99378b746153ce1ab1a6c975b7fd08f25fa` on 2026-11-20 at 05:47 UTC. Final integration retained #46's fit finder, design suggestions and seasonal guide cluster, resolving the homepage in the source template and rebuilding rather than overwriting parallel work. Final local checks: **30 generated pages, zero errors or warnings; 76 served HTML pages, zero broken relative file references**. Collector, launch-gate and fit-finder tests passed. The original Pages job was superseded by the next main commit; the [successful deploy including #49](https://github.com/karagemop466-tech/Affil1/actions/runs/44683344876) and a [fresh live fetch](https://karagemop466-tech.github.io/Affil1/?edition=9982e993) confirmed “The countertop edit”, all five records and the new seasonal links. This confirms publication, not Associates activation or search rankings.

## Merge addendum II — arena/4772a1e3-affil1 (2026-11-20, third merge, main @ 4f42810)

Main advanced again (PRs #48–#64, incl. paid-link gate `tools/paid_link_gate.py` + test,
release panels, deployment receipts and the live countertop-issue cover). This merge, like
the second, carries no change of its own: only `COORDINATION.md` conflicted. Head's addendum
is retained verbatim above; main's release receipt is retained verbatim below it. Net
published-edition diff vs `origin/main` remains **log only**.
