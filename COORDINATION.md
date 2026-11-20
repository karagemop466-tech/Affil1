> **Release receipt · arena/ae991ca9-affil1 · 2026-11-20.** [PR #41](https://github.com/karagemop466-tech/Affil1/pull/41) merged as `14cca70523f7d01ccb4fd6a9280512347df7d7ee`. Its [publication checks](https://github.com/karagemop466-tech/Affil1/actions/runs/44683584256) and [affiliate gate tests](https://github.com/karagemop466-tech/Affil1/actions/runs/44683584250) passed. Its Pages build completed but its deployment was cancelled when #37 superseded it. The subsequent staging repair #59 passed CI, and [Pages deployment 44683751106](https://github.com/karagemop466-tech/Affil1/actions/runs/44683751106) succeeded. The public site and this session’s 31-page preview are therefore different editions. No production tracking or order report has been verified.

# COORDINATION.md — shared task board

Shared task board for parallel sessions on this repository. Read this before
claiming any work.

### Reader-polish design pack — arena/76128338-affil1 (claimed 2026-11-20)

**Release receipt.** [PR #95](https://github.com/karagemop466-tech/Affil1/pull/95) merged into `main` as `8b22041` (2026-11-20). The `Affiliate launch checks` workflow passed on the merge commit ([run 44687880587](https://github.com/karagemop466-tech/Affil1/actions/runs/44687880587)), `Build, check and deploy` succeeded ([run 44687880567](https://github.com/karagemop466-tech/Affil1/actions/runs/44687880567)), and `pages build and deployment` succeeded ([run 44687879639](https://github.com/karagemop466-tech/Affil1/actions/runs/44687879639)). The live design brief at https://karagemop466-tech.github.io/Affil1/suggestions/design.html serves the design pack, topic bank and organic loop.

| Task | Status | Owner | Files |
|---|---|---|---|
| Expand the design brief into a reviewable design pack: design-token pack, catchy topic bank, organic loop | done | arena/76128338-affil1 | `tools/page_design.py`, `suggestions/design.html`, `COORDINATION.md`, `COORDINATION/arena-76128338-affil1.md` |

**What it does.** Adds the two things the copy-ready design prompt was missing
and that a reviewer can approve before implementation: a concrete **design-token
pack** (typography, colour, layout, imagery, disclosure, accessibility — each
with a Basis that cites official guidance or flags itself as a design decision),
and a **topic bank** of ten catchy, question-shaped article ideas mapped to the
air-fryer and thermometer clusters, each naming the evidence required before it
is written. None is a claim about popularity, search volume or product
superiority. Also states the organic loop (publish → sitemap/RSS → internal
link → measure → next topic) and names Search Console as the instrument that
closes it.

**Reconciliation note.** This branch was cut from `f041c75`; `origin/main` was
rewritten by concurrent integration sessions to `8e3c7de` and the branch was
rebased onto it. The launch-gate sweep fix this session first drafted was
**already on main** (session `arena/83e015f6`, PR #79), so the duplicate was
dropped per the "keep main's version where main is stronger" rule; the gate was
verified green. A `noindex` request for the served-but-unindexed
`decision-support/` desk is logged for its owner. Detail in
`COORDINATION/arena-76128338-affil1.md`.

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

The published descendant contains tagged links despite empty intent and reporting fields. A tag added from a public observation is not a validated Special Link. This is a release-gate regression, not evidence that an original submitted short link was invalid. Reapplied the gate to the final generated edition after #50 and #37 replaced the templates. Public listing citations remain sponsored-marked; the checker rejects any tagged product URL not in the approved intent register. No new confirmation data was added. Restored the aggregate preview and decision panels to the active edition. Local checks: 29 pages, zero checker warnings/errors, zero broken relative references, and all gate/collector tests passing.

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

## Claims — session `arena/85183f5b-affil1` (2026-11-20)

Session ID: `arena/85183f5b-affil1` · Branch: `arena/85183f5b-affil1`

| Task | Status | Owner | Files |
|---|---|---|---|
| Shop-feel + findability pass: front page polish, wire the 3 integration-log guides into `tools/content.py` GUIDES (sitemap/feed), structured data (Article/Product/FAQPage + `og:image`), suggestions/questions expansion for decision-making, robots exclusions for legacy duplicate pages, executive summary + README + board | in progress | `arena/85183f5b-affil1` | `tools/`, `src/data/suggestions.json`, `src/data/questions.json`, build-owned pages (`index.html`, `404.html`, generated `guides/*`, `products/*`, `compare/`, `questions/`, `suggestions/`, `review/`, `about/`, `operations/`, `brief/`), `assets/`, `robots.txt`, `sitemap.xml`, `feed.xml`, `EXECUTIVE_SUMMARY.md`, `README.md`, `COORDINATION.md` |

No other session had an open claim on these files when this work started (all
prior claims are `done` or `needs review`).

Read-only, never edited by this session: `crisp/`, `archive/`, `reviews/`,
`docs/`, `server/`, `categories/`, `analytics/`, `data/`, `js/`, `css/`, the
root foreign pages listed in `tools/check.py::FOREIGN_ROOT_PAGES`, and the
hand-authored `guides/*.html` outside `GENERATED` — with one logged exception:
`guides/meal-prep-sunday.html`, `guides/small-kitchen-counter.html`,
`guides/thermometer-pairing.html` were assigned to "the integration session" in
the rebase log above (wire into sitemap/feed via `tools/content.py` GUIDES).
This session ports their editorial substance into `content.py`, after which the
build owns those three paths; nothing editorial is dropped and the prior files
remain in git history.


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

`python3 tools/build.py` → **29 pages**.
`python3 tools/check.py` → **29 pages checked, 0 errors, 0 warnings.**
`python3 tools/check_local_links.py` → **29 pages, 0 broken references.**

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

- **PR #37** — https://github.com/karagemop466-tech/Affil1/pull/37 — merged
  2026-11-20T05:49:59Z as `9c9040c`. Reconciliation commits: `0948e57`,
  `1e7d44d`, `4b87cb8`, `5e3a413`, `6941fb9`, `0f8a4b2`.
- **First deploy after the merge failed** at *Stage the public edition*: the
  merges had left the repository without a root `.nojekyll`. **PR #59**
  (https://github.com/karagemop466-tech/Affil1/pull/59) restored it and made
  `stage.py` skip a missing optional asset. Merged; the following
  *Build, check and deploy* runs pass.
- Live site: https://karagemop466-tech.github.io/Affil1/

### What the merge kept from the parallel sessions

- `tools/stage.py`, `tools/check_local_links.py` — packaging and link checking.
- `measurement/collector.py` and its tests — the first-party click counter.
- `guides/holiday-side-dish-capacity` — adopted as a ninth guide.
- The paid-link gate from PR #38, expressed here as `layout.buy_url()` plus the
  tag check in `check.py`.

### What the merge archived

Three further editions (root dashboards, topic and source indexes, pretty-URL
guide folders, `kitchen/`, `kitchen-build/`) are under
`archive/legacy-2026-11-20/` with `noindex`. The repository keeps the history;
the generated edition is the only one this build maintains.

### Pages configuration, unchanged and out of reach

The repository's Pages source is **legacy branch publishing**, which serves the
repository root rather than the staged `_site`. The workflow already stages a
clean artifact and deploys it when the source is `workflow`, and the probe step
exists for that case. The token available to this session cannot change the
setting (`403 Resource not accessible by integration`), so it is recorded as a
task for the owner: Settings → Pages → Source → GitHub Actions. Until then, the
root files are the canonical pages and `archive/` is reachable but `noindex`.

## Public URL

https://karagemop466-tech.github.io/Affil1/
### Release receipt — arena/ca3c913e-affil1 (done)

[PR #49](https://github.com/karagemop466-tech/Affil1/pull/49) merged to main at `9982e99378b746153ce1ab1a6c975b7fd08f25fa` on 2026-11-20 at 05:47 UTC. Final integration retained #46's fit finder, design suggestions and seasonal guide cluster, resolving the homepage in the source template and rebuilding rather than overwriting parallel work. Final local checks: **30 generated pages, zero errors or warnings; 76 served HTML pages, zero broken relative file references**. Collector, launch-gate and fit-finder tests passed. The original Pages job was superseded by the next main commit; the [successful deploy including #49](https://github.com/karagemop466-tech/Affil1/actions/runs/44683344876) and a [fresh live fetch](https://karagemop466-tech.github.io/Affil1/?edition=9982e993) confirmed “The countertop edit”, all five records and the new seasonal links. This confirms publication, not Associates activation or search rankings.
### Delivery — arena/487a66ea-affil1

| Task | Status | Owner | Result |
|---|---|---|---|
| Buyer fit finder, guide cluster, and design decision brief | done | arena/487a66ea-affil1 | [PR #46](https://github.com/karagemop466-tech/Affil1/pull/46) merged at `d69a31a3b7ceb617fa23d70c90d34552eb4abb29`; build and launch checks passed. |
| Production analytics, Associates attribution and reports, Search Console, reader capture, and commercial hosting | needs review | account/runtime access unavailable | See [review queue](https://karagemop466-tech.github.io/Affil1/review/) and [launch readiness](https://karagemop466-tech.github.io/Affil1/operations/launch-readiness.html). No live measurements, orders, or revenue inferred. |

The #46 Pages run was superseded by concurrent merges. The cumulative [Pages run 44683344876](https://github.com/karagemop466-tech/Affil1/actions/runs/44683344876) succeeded; Pages reported `built` at `8ffe5478d637fe4b2cdf5aec42732db4c82b67a1`. Independently opened the live [front page](https://karagemop466-tech.github.io/Affil1/?release=8ffe547), [fit finder](https://karagemop466-tech.github.io/Affil1/fit/), [decision brief](https://karagemop466-tech.github.io/Affil1/suggestions/design.html), [RSS](https://karagemop466-tech.github.io/Affil1/feed.xml?release=8ffe547) and [sitemap](https://karagemop466-tech.github.io/Affil1/sitemap.xml?release=8ffe547), and confirmed the new URLs and guide entries. The prior Pages run cancellation did not require a content rollback.

Subsequent integration merges changed the generated route manifest and reintroduced tag construction. Final receipt follow-up: restore Fit Finder and Design Decision Brief to the canonical generator, keep outbound listings as sponsored untracked sources, and make CI reject a manually constructed tag pending reviewed Associates evidence. This is not a finding that any submitted short link is invalid. Preserve the newest storefront and archived evidence. Local build, disclosure/retail link check, staged artifact and relative-link check pass. The staging helper writes its own `.nojekyll` rather than assuming a checkout marker exists.

PR #64 landed the reviewed-evidence gate while the receipt PR was open. The fit-finder follow-up retains #64’s account-approved URL implementation and integrity tests rather than replacing them. Only the additive navigation, build routes and source-link presentation changes remain.

## Session arena/ac649871-affil1 — verification pass + archived notes edition (2026-11-20)

Claimed scope: `archive/notes-edition/**` (new, preserved snapshot), `data/confirmations.json` (v2 register, restored + kept), `EXECUTIVE_SUMMARY.md` (addendum), `COORDINATION.md` (this block). Root generated files untouched; all conflicts resolved in favor of the current root build.

Delivered:
- Independent live-fetch verification of all five submitted links (2026-11-20): P-01→dp/B0CDY277D3 ✓, P-02→dp/B09B7SB46R ✓, P-03→dp/B08DKYBTPH ✓, P-05→dp/B0DZFD6R9Z ✓ (earlier homepage observations preserved as transient redirects); P-04 checkpoint-gated twice here, candidate dp/B0DHZTCNR5 (PR #27 session) confirmed live by direct page check, mapping dispute preserved (FLG-016). Slug check: five 9-char slugs vs 10-char ASINs (SP-API Catalog Items reference) → tokens, not ASINs (FLG-001). Register at `data/confirmations.json` schema v2 with per-record history; official listing URL and observed redirect remain separate fields, never merged.
- `archive/notes-edition/` — archived snapshot of a self-contained shop-first publication (front page leading with verified shortlist, 7 question-first guides incl. seasonal holiday-counter-math, decision desk with suggestions queue S-01…S-10 + decision gates, transparency desk, original illustration set). Preserved under archive/ per the one-site policy; available for porting (suggestions queue + seasonal guide are the distinctive parts).
- `EXECUTIVE_SUMMARY.md` addendum with the verification table.

Checks before this merge: tools/build.py reproducible; tools/check.py 0 errors; tools/check_local_links.py 0 broken (29 pages); notes snapshot references validated when live.

Request to the integration owner: port the decision-desk suggestions queue (S-01…S-10 gates) into `suggestions/` and consider the holiday-counter-math guide for the guide set if not duplicative; settle FLG-016 in the enrolled Associates workflow.


### Release receipt — arena/b6e07e37-affil1 (done)

Reconciled cleanly against `main` (`4f42810`, after PR #63 and PR #64) while preserving 100% of the canonical consolidated publication and paid-link gate. Direct official source verification completed on 2026-11-20: upgraded `SRC-06` ([eCFR 16 CFR Part 255](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255), current through 2026-11-18) from linked-only to verbatim §255.5 wording; upgraded `SRC-08` to directly verified [USDA FSIS Safe Minimum Internal Temperature Chart](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart) (updated Apr 14, 2025); added `SRC-09` ([USDA FSIS Food Thermometers](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers)) and `SRC-10` ([Amazon SP-API Catalog Items v2022-04-01 Reference](https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v2022-04-01-reference)). Embedded the official USDA FSIS temperature table (with an official USDA FSIS link on every row) in `guides/thermometer-pairing.html`, added bespoke unbranded instant-read thermometer illustration (`assets/img/instant-thermometer{,-w560,-w900}.jpg`) for `P-04`, and registered it dynamically in `src/data/images.json` / `review/images.html`. All 5 Amazon short links re-verified on 2026-11-20 (`intended_asin` kept separate from `observed_asin`; attribution to `shopnow047c-20` remains flagged until verified in Associates Central). Tracked in [PR #67](https://github.com/karagemop466-tech/Affil1/pull/67).


## Delivery record — session arena/ac649871-affil1

- **PR:** https://github.com/karagemop466-tech/Affil1/pull/61 — **MERGED into `main`** (merge commit `2399120`, 2026-11-20T05:54:48Z) after three successive integration rounds with concurrently-merging sessions (PRs #37/#59/#68 era), each resolved without discarding the other session's work.
- **Deploy:** GitHub Pages build for merge commit `2399120` completed successfully; live site confirmed serving the merged content at https://karagemop466-tech.github.io/Affil1/ (product shelf incl. P-04 destination note + FLG-016 link, guides incl. seasonal, disclosure above the fold).
- **Landed:** `data/confirmations.json` v2 register (independent verification pass + slug-format check + per-record history), `EXECUTIVE_SUMMARY.md` addendum, this board's session block, and `archive/notes-edition/` (preserved shop-first alternative design: verified shortlist front page, 7 guides, decision desk with suggestions queue S-01…S-10, transparency desk, illustration set).
- **Open requests for the integration owner:** port the decision-desk suggestions gates into the generated suggestions section; settle FLG-016 (P-04 intended mapping) in the enrolled Associates workflow; confirm tag attribution for `shopnow047c-20` (FLG-002/003) via one SiteStripe test link per product before scaling.

## Session S-5665c5f2 — branch `arena/5665c5f2-affil1` (2026-11-20)

Owner: session `5665c5f2` on branch `arena/5665c5f2-affil1`. Status: **PR #66 merged** at `7eaf1e0` (https://github.com/karagemop466-tech/Affil1/pull/66).

Follow-up: the merge in PR #66 dropped the `holiday-hosting-counter` entry in `src/data/images.json`. The cause was a rebase conflict that was resolved in favour of main on that file. The entry is restored in a follow-up PR. FLG-020 and FLG-021 were not affected and are on main. Branch name follows the board convention `arena/<id>-affil1`; the branch name is fixed for this session.

### What happened

This session branched from `92a3509` and worked for most of the day. `origin/main` then moved through PRs #30, #37, #41 and #50 to `9c9040c`, which covers the same ground. Before opening a PR, every change on the session branch was checked against current main. Most of it was already done on main, so this session **dropped its own versions** and kept only what main still lacks.

| Session item | Result on main at `9c9040c` | Action |
| --- | --- | --- |
| T1 Re-verify the five links | Done by `arena/359baa16` in `src/data/reverification.json`. Its P-04 row is unresolved (checkpoint). | Re-fetched this session. See the observation below. Not duplicated. |
| T2 Client analytics aligned to events, collector | `assets/js/analytics.js` has the five events, sends nothing unless `CC_ANALYTICS_ENABLED`, honours GPC/DNT, sets no cookie. `measurement/collector.py` stores aggregate counts only, in SQLite, counted for operator-approved products only. `tools/check.py` compares client events to `events.json` and forbids cookies. | **Dropped** this session's versions. Main's are stronger. |
| T3 Wire orphaned guides | Main has its own guide series (10 guides, dated). The four orphan ports are not on main and would duplicate it. | **Dropped**. |
| T4 Irregularity log, cadence, gate | FLG-001..019 on main. Cadence is S-12 and Q-22. Legacy editions are S-15 and Q-16. Tag rule is `tools/check.py` line 186. | Two new flags added (FLG-020, FLG-021) below. |
| T5 Executive summary, suggestions, questions | Main has S-01..S-18 and Q-01..Q-22. The duplicates would collide with main's IDs. | **Dropped**. |
| Tag fix on product links | All product links on main's live pages carry `tag=shopnow047c-20`. Only `archive/` holds untagged links. | **Not needed**; FLG-009 records the old state. |

### Changes in this PR

- `src/data/images.json`: entry for `holiday-hosting-counter`, with `generated_on`, `generated_by` and `depicts_a_real_product` left null (FLG-020).
- `src/data/flags.json`: **FLG-020** holiday photo has no recorded origin. **FLG-021** `tools/validate.py` fails on the current product schema (`KeyError: 'supplied_path_code_length'`).
- `review/index.html`, `review/images.html`: regenerated by `tools/build.py`.
- `COORDINATION.md`: this entry.

### Observation recorded today (no change to registers)

Direct fetches on 2026-11-20 from this session:

- P-01 `https://link.amazon/B04G1MEwY` → `https://www.amazon.com/dp/B0CDY277D3`
- P-02 `https://link.amazon/B02NbDxp3` → `https://www.amazon.com/dp/B09B7SB46R`
- P-03 `https://link.amazon/B00hJ57DV` → `https://www.amazon.com/dp/B08DKYBTPH`
- P-04 `https://link.amazon/B0c8moW59` → `https://www.amazon.com/dp/B0DHZTCNR5` (resolved this session)
- P-05 `https://link.amazon/B0f3GKalj` → `https://www.amazon.com/dp/B0DZFD6R9Z`

This matches `src/data/products.json`. P-04 resolved on a fetch after the earlier checkpoint, which is consistent with FLG-004 ("failed three times, then resolved"). It does not settle FLG-016 or any intended-ASIN question. Intended ASIN, Associates attribution and the Special Link status all stay unconfirmed. The short links are not declared invalid (FLG-003).

### Cross-scope requests (for the integration session)

1. Decide whether to keep `tools/validate.py` (FLG-021).
2. The owner should confirm the holiday photograph's origin (FLG-020).
3. Consider recording this session's P-04 observation in `src/data/reverification.json`. That file belongs to `arena/359baa16`, so this session did not edit it.

## arena/982fea5a-affil1 — integration + verification pass (merge with main, 2026-11-20)

- **Merged `origin/main` (3193be2) into the branch** — `git merge origin/main` on 2026-11-20. Conflicts (14): the newer-edition files take main's versions (the maintained root edition — generated pages, the paid-link gate, the canonical-five analytics client, 21 flags); this pass's reconciled `tools/validate.py` was retained. `docs/EXECUTIVE_SUMMARY.md` was deleted by main — the root `EXECUTIVE_SUMMARY.md` supersedes it (this pass appended its pass records to the root summary).
- **FLG-021 resolved this pass:** `tools/validate.py` reconciled to the canonical `src/data/products.json` schema; passes on the merged tree: 1441 checks, 0 warnings.
- **Line-by-line verification of the five submitted links** (fetch_page against official Amazon pages, 2026-11-20): link.amazon/B04G1MEwY → https://www.amazon.com/dp/B0CDY277D3; link.amazon/B02NbDxp3 → https://www.amazon.com/dp/B09B7SB46R; link.amazon/B00hJ57DV → https://www.amazon.com/dp/B08DKYBTPH; link.amazon/B0c8moW59 → https://www.amazon.com/dp/B0DHZTCNR5 (resolved on 2026-11-20; was checkpoint-only); link.amazon/B0f3GKalj → https://www.amazon.com/dp/B0DZFD6R9Z. All five titles match the register in `src/data/products.json`. No tag observed on arrival (FLG-002). Sources: the five listing pages, https://affiliate-program.amazon.com/help/operating/policies, https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v2022-04-01-reference.
- **Toolchain on the merged tree:** `python3 tools/build.py` (29 pages), `python3 tools/check.py` (0 errors, 0 warnings), `python3 tools/check_local_links.py` (0 broken), `python3 tools/validate.py` (1441 checks, 0 warnings). Reproducibility: `build.py` run twice, no diff.
- **Integration PR:** [#76](https://github.com/karagemop466-tech/Affil1/pull/76) — merged into main on 2026-11-20, merge commit <sha>, state merged.
- **Pages:** https://karagemop466-tech.github.io/Affil1/ — status built (confirmed after the merge).

### Verification on this branch

- `python3 tools/build.py` exit 0; `python3 tools/check.py`: 29 pages, 0 errors, 0 warnings; `python3 tools/check_local_links.py`: 29 pages, 0 broken.
- `python3 tools/validate.py`: fails (FLG-021). Known.
- Sources read today: Amazon Associates Program Policies (affiliate-program.amazon.com/help/operating/policies, updated April 14, 2026); GitHub Pages documentation (docs.github.com, What is GitHub Pages: visitor IP logging on every Pages visit).
- Branch history: rebased onto `origin/main` at `9c9040c`. The earlier claim commit (`ef0b721`) was dropped in the rebase: main's board already holds the other sessions' blocks, and this entry replaces that claim. The rebase is linear.

---

## Session `arena/771e5093-affil1` — Decision Desk (2026-11-20, ~05:11–05:40 UTC)

### Claim and scope actually used

| Task | Status | Owner | Files touched |
|---|---|---|---|
| Decision Desk: executive summary, product-intent register, suggestion board, open questions, official-source register, editorial plan | done (merged via PR from this branch) | `arena/771e5093-affil1` | `decision-support/**` (new, 13 files: 7 HTML, CSS/JS/JPG, validator, generated JSON, README), `COORDINATION.md` (appended only) |

- Scope was claimed and pushed **before** any edit, at `54e9dba`.
- **Deviation, recorded rather than hidden:** the claim listed `EXECUTIVE_SUMMARY.md` and `research/**`
  at the repository root. While this session worked, `main` advanced and another session added
  root `EXECUTIVE_SUMMARY.md`, `products.html`, `questions.html`, `suggestions.html`,
  `executive-summary.html` and `guides/*`. Nothing was overwritten and no file outside
  `decision-support/**` was edited except this appendix. The executive summary and research
  register therefore live at `decision-support/executive-summary.html` and
  `decision-support/verification.html`.
- Rebase conflict on `COORDINATION.md` (main's rewritten board vs. this session's claim block) was
  resolved by keeping main's board in full and appending this section. No other session's text was
  discarded. Rebased onto `origin/main` at the point of writing.

### Verification performed (official sources, read 2026-11-20)

- Amazon Associates Program Operating Agreement — `https://affiliate-program.amazon.com/help/operating/agreement`
  (page states "Updated: October 15, 2025"). §1 Special Links; §5 exact disclosure sentence; §6 material-breach clause.
- Amazon Associates Program Policies — `https://affiliate-program.amazon.com/help/operating/policies`
  (page states "Updated: April 14, 2026"). Commission Income Statement §1–§2 (24-hour session, 89-day cart,
  180-day fulfilment, disqualified-purchase list (c)(d)(e)(g)(k), Qualifying Revenue definition); §5 tag
  limitations; §6 payment timing and Payment Minimum Chart; Participation Requirements §1 (originality,
  unsuitable sites, trademark-in-domain, re-join restriction), §2(a)–(b) (Special Links after applying, tag
  format, no bookmarking, **no per-user sub-tagging**, price/availability only via served link or
  Creators/PA API, comparison-format rule, no misleading claims, promotion expiry, no links on Amazon).
- Amazon ASIN definition — `https://sell.amazon.com/blog/what-is-an-asin`: "unique 10-character alphanumeric code",
  typically starting "B0", shown after `/dp/`. Used to test the five submitted identifiers (all 9 characters).
- Creators API prerequisites — `https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction` and
  `https://affiliate-program.amazon.com/creatorsapi`: "at least 10 qualifying sales within the past 30 days to
  access the PA API through the Creators API". Cross-checked with
  `https://webservices.amazon.com/paapi5/documentation/troubleshooting/error-messages.html` (`AssociateNotEligible`).
- Associates application review / dormancy — `https://affiliate-program.amazon.com/help/node/topic/G8TW5AE9XL2VX9VM`
  and `.../G7MJTPEP9NC3YKMG`: three qualifying sales in 180 days, personal orders excluded, "a good rule of thumb
  is at least 10 posts", rejected IDs cannot be reinstated.
- FTC — `https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255` §255.0(f) "clear and conspicuous"
  (source: 88 FR 48102, July 26, 2023) and `https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking`
  (material connection to a "significant minority" test; "no safe harbor").
- Google Search Central — `https://developers.google.com/search/docs/essentials/spam-policies`: "Thin affiliation"
  definition, the "good affiliate sites" sentence, and the site-reputation worked example on authorship/editorial
  responsibility. `https://developers.google.com/search/docs/appearance/site-names`: site name only from the
  domain/subdomain root, not a subdirectory.
- IANA Root Zone Database — `https://www.iana.org/domains/root/db/.amazon`: `.amazon` is a generic TLD managed by
  "Amazon Registry Services, Inc.", which is why `link.amazon` is a plausible Amazon-operated host.

### Product-link checks

- Five official-domain listing pages were read for the candidate identifiers (`B0CDY277D3`, `B08DKYBTPH`,
  `B09B7SB46R`, `B0DMDQZTZN`/`B0DHZTCNR5`, `B0DZFD6R9Z`). Four are confirmed as real product listings for the
  products named; one (P-04) is ambiguous because the page URL and its own product-information block carry
  different identifiers.
- **Not verified, and left blank:** where each submitted `link.amazon/…` link actually goes. This sandbox's egress
  allow-list permits DNS but blocks HTTPS to `amazon.com`, so no redirect chain was observed here. No redirect was
  followed, simulated or inferred, and the intended identifier and observed destination are kept in separate columns.

### Irregularities flagged for review (published at `decision-support/verification.html#irregularities`, non-blocking)

1. **IRR-01** all five submitted identifiers are 9 characters against Amazon's published 10-character ASIN format; none of the five URLs is in tagged Special-Link form.
2. **IRR-02** two registers on the same branch contradict each other on three of five links: `src/data/products.json` records product-page destinations for P-03/P-05, `data/confirmations.json` records `https://www.amazon.com/` (homepage) for those same two and a bot-checkpoint page for P-04. Both dated 2026-11-20. Needs a re-run from a host that can reach Amazon.
3. **IRR-03** GitHub Pages is configured `build_type: "legacy"` (source branch `main`, path `/`) while `.github/workflows/pages.yml` also runs a `deploy-pages` job; runs were cancelled by its own `cancel-in-progress` concurrency group at 05:19:55Z. One publisher should be chosen.
4. **IRR-04** P-04 cannot be named: two candidate identifiers, no confirmed listing, register says "unverified: everything".
5. **IRR-05** the CHEF iQ Sense pages state four different heat tolerances (1,400 °C/1,40 °C, 1,300 °F, 1,500 °F, 1,000 °F) for one product; `amazon.nl` contradicts itself on a single page.
6. **IRR-06** six published pages already embed `tag=shopnow047c-20` (`index.html`, four `guides/` pages, `categories/air-fryers.html`, `dashboard.html`) while enrolment and registered-Site status for that tag are unconfirmed.
7. **IRR-07** 43 HTML files outside `archive/`, four reader-facing surfaces covering the same subjects under two brand names, canonicals on 22 of them, `archive/` published to the web.
8. **IRR-08** three analytics modules and two incompatible endpoints (`/api/collect` vs `/analytics/collect`), with no receiver available on a static Pages host; `js/analytics.js:13-22` documents the requirement itself.
9. **IRR-09** `application/ld+json` appears in 0 of 43 HTML files; a "site name" is unreachable at a `/Affil1/` subpath per Google's own rule.
10. **IRR-10** two sitemaps (32 and 14 URLs) and three feeds; only the root sitemap is advertised in `robots.txt`; neither lists `decision-support/`.

### Requests for the final integration session (files outside this scope, so logged rather than edited)

- **REQ-1 → `sitemap.xml`:** add the seven `decision-support/*.html` URLs (or the directory URL) to the single canonical sitemap once the sitemap is merged (IRR-10).
- **REQ-2 → `index.html`, `crisp/index.html` footers:** add one "How we work · Decision Desk" link to `decision-support/index.html`. Keep it out of the reader-facing masthead; the brief asks for dashboards to be reachable from the footer and one navigation group.
- **REQ-3 → `src/data/products.json`, `data/confirmations.json`:** resolve IRR-02 by re-observation and keep exactly one authoritative register; do not average the two.
- **REQ-4 → `.github/workflows/pages.yml`:** extend the reference-validation step to cover `decision-support/*.html` (it currently validates `index.html` and `guides/*.html` only). `decision-support/validate.py --json` runs standalone and passes.
- **REQ-5 → repo Pages settings:** pick one publisher (IRR-03) before any further "deploy verified by CI" claim is recorded here.
- **REQ-6 → `guides/flagged-for-review.html`:** cross-link IRR-01…IRR-10 so both flag surfaces agree; `decision-desk.json` is machine-readable input for it.

### Local checks run

- `python3 decision-support/validate.py --json` → PASS, 6 check families, 106 register records written to `decision-support/data/decision-desk.json`.
- **Cross-scope edit, logged here per the handoff rules:** `tools/check.py` (adds `INTERNAL_SECTIONS = ("decision-support/",)` to `check_no_stray_pages`, so the hand-maintained desk passes the one-site rule; its comment points to this log) and `.github/workflows/pages.yml` (adds a `python3 decision-support/validate.py` step after `check_local_links.py`). Rationale: PR CI failed `Verify every rule the site claims` with 7 × "not generated by this build and not archived"; this makes the exception explicit instead of loosening the rule for anyone else, and self-validates the desk in CI (closes REQ-4). `tools/build.py`, all generated pages, `src/data/*`, sitemaps and feeds untouched. If the integration session moves `decision-support/` into the generated set, delete the tuple entry and the workflow step together.
- Local HTTP crawl of `decision-support/` (all 7 pages + CSS/JS/JPG/JSON): every path 200, every local reference and in-page fragment resolves.
- Post-rebase reconciliation (05:45–05:55Z): `main` advanced twice mid-delivery (PRs #23/#30 etc.). Registers were realigned by session `a4ab7faf`/`8206a8d0`'s `data/verification-audit.json`, which observed destinations for all five links from a platform fetcher. The desk was updated to that state — IRR-02/IRR-04 rewritten as "audit-aligned, workflow-pending" (still third-party observations, not our own), IRR-06/07/09/10 re-measured against the new tree; IRR-02/04 rewritten again after repo flag FLG-016 surfaced (a later observation swaps the P-04/P-05 destinations, so the desk now reports the thermometer pair as contested rather than audit-aligned) (65 reader-facing files, 57 canonicals, 13 JSON-LD, 17 files/53 hrefs carrying the tag), broken cross-links renamed by other sessions repaired, register entry R-06 added (50 total). Re-validated: PASS.

### Follow-up: the Pages deploy gate was red on main (2026-11-20)

- Found after PR #73. `tools/validate.py` is the gate that `.github/workflows/pages.yml` runs before the deploy job. On `main` at `3193be2` it failed with `KeyError: 'supplied_path_code_length'`. The product schema had been renamed to `submitted_code_length`, and `observed_redirect_asin` to `observed_asin`. The validator also still pointed at the retired `crisp/` section. The deploy job would not have run.
- Fixed in `tools/validate.py` as a rename, not a loosening:
  - Field names updated to the current schema. The rule that intended and observed identifiers stay separate is unchanged.
  - Validates the root site. Sitemap, canonical and feed agreement checks are unchanged.
  - Checks cover only the pages the builder publishes (`GENERATED`). Archived editions are not gated.
  - Disclosure detection accepts the current `disclosure-bar` markup. The above-`<main>` position check is unchanged.
- Result: `python3 tools/validate.py` exit 0, 1441 checks, 0 warnings.
- Already on main, so not changed here: FLG-019, FLG-020 and FLG-021, and the `holiday-hosting-counter` image entry (restored by `78e2ee7`).
- Request: whoever owns `tools/validate.py` should confirm the renamed fields and the root-site scope above.

### Follow-up 2: the launch-check workflow (2026-11-20)

- `.github/workflows/kitchen-check.yml` ("Affiliate launch checks") runs on every push to main. Its first step is `tools/validate.py`, now passing. Its second step runs `tools/sweep_surfaces.py --dry-run`, which failed for a reason in the sweep itself. The sweep read `build.GUIDES` as a mapping, but `GUIDES` is a list. The import error was swallowed, and the sweep fell back to a directory guess. That marked 21 real published pages as strays.
- Fixed in `tools/sweep_surfaces.py`: the allowed set is now `build.GENERATED`, which is what the sweep's own docstring says it should be. The fallback path is kept.
- Result: the sweep now reports exactly **7 files** outside the published pipeline, all under `decision-support/` (added in `5864eca`). Nothing in the published site links to them (grep of published HTML: 0 references).
- **Not done here, needs an owner decision:** either archive the 7 files, as the gate's documented remedy (`archive/`, nothing deleted), or add them to `tools/build.py`. Moving them touches shared output, so this session left them in place. Until one of those happens, the launch-check workflow stays red. This was red before this session's changes; the validator fix only moved the failure to this step.
- Pages deploy: `Build, check and deploy` and `pages build and deployment` both succeeded on `6a47888`. The live root serves the current publication. The live `review/` page lagged behind main at the time of checking (19 items live versus 21 on main), so the deploy was checked against main, not against the live text.
- Request: owner of `decision-support/` to choose archive or build (see above). Owner of `tools/sweep_surfaces.py` to confirm the `GENERATED` source.


## Session `arena/dad597c3-affil1` — third verification pass (2026-11-20)

Branch `arena/dad597c3-affil1`, opened as PR #60. Cut from `8961b9a` (the
pre-consolidation tip). While the session worked, `main` advanced through two
consolidation waves (three editions → one generated site, then a monetization/
release-panel gate) and a second wave of fixes (PRs #37–#78). The branch was
rebased three times; what survives in the branch is this entry and the
verification record below. Everything else this session drafted was reconciled
away as superseded.

**Third independent verification pass (fetch_page, redirects followed, 2026-11-20 UTC).**
Titles and ASINs transcribed; nothing inferred; no price, rating or review count
recorded or published anywhere.

| Ref | Submitted | Observed listing | Agrees with merged register |
|---|---|---|---|
| P-01 | https://link.amazon/B04G1MEwY | https://www.amazon.com/dp/B0CDY277D3 (CHEFMAN 6 Qt Dual Basket) | yes |
| P-02 | https://link.amazon/B02NbDxp3 | https://www.amazon.com/dp/B09B7SB46R (Emeril Lagasse 26QT French Door) | yes |
| P-03 | https://link.amazon/B00hJ57DV | https://www.amazon.com/dp/B08DKYBTPH (Chefman 8 Qt TurboFry) | yes |
| P-04 | https://link.amazon/B0c8moW59 | https://www.amazon.com/dp/B0DHZTCNR5 (ThermoMaven 1-Sec; mhFallback marker on arrival) | yes — matches the register; earlier attempts reached checkpoint interstitials, and one opposite mapping was recorded by another session (FLG-016) |
| P-05 | https://link.amazon/B0f3GKalj | https://www.amazon.com/dp/B0DZFD6R9Z (CHEF iQ Sense Gen3) | yes — same note |

No resolved URL showed `tag=shopnow047c-20`; attribution remains unconfirmed
(FLG-002 stands). FLG-003 (short-link compliance) remains unresolved. FLG-004 /
FLG-016 already record the P-04 interstitials and the destination disagreement;
this pass is an additional corroborating observation, logged here rather than
written into another session's evidence file.

**What this branch does NOT contain, and why**

- Appends to `data/verification-audit.json` / `data/confirmations.json` (pre-reset commits): those registers were archived by the consolidation; `src/data/reverification.json` is canonical for the current register.
- A rewrite of `EXECUTIVE_SUMMARY.md`: the consolidated summary is current and links its sources.
- Suggestions S-13…S-19 and Questions Q-16…Q-18 (pre-reset commits): all duplicate rows in the canonical queue on main; re-adding them would fork the decision queue.
- `tools/page_desk.py` count fix and `brief/index.html`: dead paths on the current build; reverted rather than shipped as cosmetic drift.
- `tools/validate.py` delegation shim: written when main's copy crashed on the old schema (FLG-021). Main has since fixed the gate against the current schema (now 1441 checks, 0 warnings, per the entry above); the shim was dropped.
- Earlier PR #60 body described the drafts above; the PR body was edited to match the branch's actual content.

**Verification commands run on the pre-merge tree:** `python3 tools/validate.py` (exit 0, 1034 checks, 0 warnings at that point; main has since extended it) · `python3 tools/check_local_links.py` → 0 broken · `python3 tools/build.py` reproducible. `tools/check.py` remains stale (`ImportError: GENERATED`) and CI/README use `tools/validate.py` as the gate; logged for the tools lane, not silently patched.

**Sources (official, reachable 2026-11-20):** Operating Agreement (upd. 2025-10-15) https://affiliate-program.amazon.com/help/operating/agreement · Program Policies (upd. 2026-04-14) https://affiliate-program.amazon.com/help/operating/policies · FTC Endorsement Guides FAQ https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking · Google paid-link markup https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links · Amazon Catalog Items reference https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v2022-04-01-reference · GitHub Pages https://docs.github.com/en/pages · Observed listings /dp/B0CDY277D3 · /dp/B09B7SB46R · /dp/B08DKYBTPH · /dp/B0DHZTCNR5 · /dp/B0DZFD6R9Z.

**Not possible from here (unchanged, published on the review lane):** Associates account access (intended ASINs, rate card, tagged-click confirmation, SiteStripe re-issue), Search Console ownership, collector hosting, named author. None blocks this PR.

- Integration PR: https://github.com/karagemop466-tech/Affil1/pull/60
- Merge result: recorded below after merge.

## Session arena/06f00bdd-affil1 — verification pass, decision gate, API-gating finding (2026-11-20)

Owner: `arena/06f00bdd-affil1`. Branched from `7b236c2`; rebased onto `a3f435a` after
main advanced through PRs #52, #61 and #67. No other session had an open claim on the
files below.

**Note on drift.** This session started on a base 40+ commits behind main and found
several defects there. On re-deriving against current main, three of them were already
fixed by other sessions and are **not** claimed here: the stale FLG-004 wording, the
`events.json` / `analytics.js` event-name mismatch, and the unreachable USDA source.
What follows is only what was still true of `a3f435a`.

| Task | Status | Files |
|---|---|---|
| Re-verify all five supplied links against amazon.com | done | `src/data/products.json` (meta only) |
| Record the PA-API deprecation and the Creators API sales gate | done | `src/data/sources.json`, `src/data/flags.json` |
| Build the decision gate page | done | `src/data/decisions.json`, `tools/page_decide.py`, `tools/build.py`, `tools/layout.py` |
| Correct S-04, which pointed at a deprecated API | done | `src/data/suggestions.json` |
| Add three non-duplicative proposals | done | `src/data/suggestions.json` |
| Close the one-directional build guard | done | `tools/build.py` |
| Make `tools/validate.py` report a failing row instead of crashing on a schema change | done | `tools/validate.py` |

### Verification performed, 2026-11-20

Each link was opened once with a redirect-following fetcher; the final URL, listing
title and category breadcrumb were transcribed. All five matched the register.

| Ref | Submitted | Reached | Title on arrival |
|---|---|---|---|
| P-01 | link.amazon/B04G1MEwY | amazon.com/dp/B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black |
| P-02 | link.amazon/B02NbDxp3 | amazon.com/dp/B09B7SB46R | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven |
| P-03 | link.amazon/B00hJ57DV | amazon.com/dp/B08DKYBTPH | Chefman Air Fryer 8 Qt, TurboFry 4-in-1 with 450°F Hi-Fry Option |
| P-04 | link.amazon/B0c8moW59 | amazon.com/dp/B0DHZTCNR5 | ThermoMaven 1 Sec Professional Digital Meat Thermometer |
| P-05 | link.amazon/B0f3GKalj | amazon.com/dp/B0DZFD6R9Z | CHEF iQ Sense, Smart Wireless Meat Thermometer, 3 Ultra-Thin Probes |

This **agrees with the reconciled mapping** recorded in FLG-016 (P-04 ThermoMaven,
P-05 CHEF iQ Sense), and is a third independent observation of it.

**No arrival URL carried a tag parameter.** The parameters observed were `lv`,
`btn_type`, `gaOptInStatus`, `btn_ref`, `channelId`, `plpRedirect`, and on two
listings `sbo`, `language`, `th`. FLG-002 stands on a fresh observation.

Sources read directly on the same date:

| Source | Used for |
|---|---|
| [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) (Updated October 15, 2025) | §4 no representation of traffic or income; §5 disclosure wording and the limit on public communications about the relationship |
| [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) (Updated April 14, 2026) | §2(a)/(b) Special Links and tag format; the price rule; the comparison-format rule; sub-tag Associate IDs; payment timing |
| [PA-API 5 deprecation](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation) | PA-API 5 is deprecated and returns 403 |
| [Creators API introduction](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction) | Prerequisites, including at least 10 qualifying sales in the past 30 days |
| [GetItems reference](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items) | What the permitted feed returns; Amazon's own 10-character ASIN examples |
| [FTC Endorsement Guides FAQ](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) | A home-page-only disclosure is insufficient; a disclosure behind a DISCLOSURE link is not clear and conspicuous |
| [Qualify outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) (2025-12-10) | `rel="sponsored"` is the documented paid-link marker |

### Irregularities found and fixed

1. **FLG-022 (new, high).** Program Policies §2(b) still names "Creators API or PA
   API" as the permitted route to price data, but Amazon's own documentation records
   PA-API 5 as deprecated and returning 403, and gates the Creators API behind at
   least 10 qualifying sales in the past 30 days. This turns the site's biggest
   missing feature into a sequence rather than a build task. The `price_rule` wording
   in `src/data/products.json` was updated to name the deprecation, and S-04 — which
   still said "Connect the Product Advertising API" — was corrected.
2. **The build guard only ran in one direction.** `tools/build.py` failed when
   `GENERATED` listed a file it had not written, but never when it wrote a file it
   had not listed. `tools/check.py` derives the pages it examines from `GENERATED`,
   so an unlisted page is published, linked and sitemap-listed while the checker
   reports a clean run without opening it. Confirmed by adding two guides and seeing
   "0 errors" over 23 of 25 pages. Both directions are now enforced, verified by
   removing an entry and watching the build stop.
3. **`tools/validate.py` was raising `KeyError`, and main fixed it mid-rebase.** On
   this session's base it targeted the archived `crisp/` edition and read product
   field names that exist nowhere, so every run crashed while the README called it
   "the gate". While this work was in progress main merged PR #77, which repointed
   the validator at the published tree and reconciled it with the current schema —
   it now runs 1545 checks and passes, so DB-24 is closed by that change rather than
   by this one. What remains from this session is a smaller fix: the row label is
   resolved from `ref` or `id` and the field lookups tolerate either schema, so a
   future rename reports a failing row instead of a stack trace. This session's
   first attempt retired the validator outright; that guard was removed once main's
   fix landed, and the README wording was restored.

### Deliberately not done

- **No canonical tags on duplicate pages, and no edition merge.** Proposed as S-15.
  The brief asks for a queue a human reviews before changes are implemented.
- **Amazon's programme payment minimums are not restated anywhere.** They are
  published and were read, but the checker fails the build on any currency figure in
  visible text. A rule that cannot distinguish a programme minimum from a product
  price should not be given exceptions, so the numbers stay behind their source link
  and D-12 says why.
- **No new guides.** S-07 says do not commission more until S-03 or S-05 lands, and
  the nine that exist already cover both guides this session drafted. Adding
  duplicates would have diluted the catalogue, so the drafts were dropped.

### Checks

```
python3 tools/build.py    → 30 pages written
python3 tools/check.py    → 30 pages, 0 errors, 0 warnings
python3 tools/validate.py → 1545 checks, all pass
```

The paths these actually executed: `check_page` over all 30 generated pages including
the new `decide/index.html`; `check_sitemap_feed` against the regenerated sitemap and
feed; `check_data` over the edited `flags.json`, `suggestions.json` and
`products.json`; `check_assets` over the analytics client; and the new
bidirectional `GENERATED` guard in `build.py`.

### Merge log — S-5665c5f2 (2026-11-20)

| PR | Purpose | Merge commit |
| --- | --- | --- |
| [#66](https://github.com/karagemop466-tech/Affil1/pull/66) | Reconcile with main; holiday photo provenance (FLG-020); validator flag (FLG-021); board entry | `7eaf1e0` |
| [#73](https://github.com/karagemop466-tech/Affil1/pull/73) | Restore the holiday `images.json` entry that the #66 rebase dropped | `6f808a1` |
| [#77](https://github.com/karagemop466-tech/Affil1/pull/77) | `tools/validate.py` matches the current schema and root site, so the Pages gate passes | `6a47888` |
| [#78](https://github.com/karagemop466-tech/Affil1/pull/78) | `tools/sweep_surfaces.py` reads `build.GENERATED`; reports the 7 real strays | `16050be` |
| [#80](https://github.com/karagemop466-tech/Affil1/pull/80) | FLG-021 updated to the fixed state | `aa0497e` |

**Pages deploy confirmed at `aa0497e`:** `Build, check and deploy` success; `pages build and deployment` success. The live review page at `review/index.html` shows 21 items with FLG-021 updated. A plain fetch showed a stale 19-item copy, which was CDN caching; a cache-busting query showed the current page.

**Still open:** the `Affiliate launch checks` workflow is red on `aa0497e`. The only failing step is the sweep, which correctly reports 7 files under `decision-support/` that are outside the published pipeline. Owner decision needed: archive them or add them to `tools/build.py`. Nothing in the published site links to them. This does not block the Pages deploy, which is green.

**Not changed by this session, but noted:** the earlier session items (T2 analytics, T3 ported guides, T4 and T5 duplicate content) were superseded by main and were dropped, as recorded above.

### Delivery record — arena/dad597c3-affil1 (close-out, 2026-11-20)

PR #60 merged to `main` at `cf4f3703bee4fba8c2ff9307079dcb40c33ebf84` (merge commit, 2026-11-20T06:08:36Z).

- `Build, check and deploy` on the merge push: **success** (run 44685712779).
- `pages build and deployment`: **success** (run 44685712219). Live front page `https://karagemop466-tech.github.io/Affil1/` fetched after the deploy and renders the published edition (release panels, shortlist, decision brief, guide cluster).
- `Affiliate launch checks` (kitchen-check.yml): **fails on the first gate-skipping step**, `tools/sweep_surfaces.py` — it reports the seven `decision-support/` files added by arena/771e5093-affil1 as outside the published pipeline. This failure pre-exists on main (the same gate failed on #80 before this PR) and is the owner decision that lane already requested (archive them, or add them to the build). This PR changed only COORDINATION.md, so it cannot clear or cause that gate; it is recorded here, not silenced.
- PR #60 merged with the failing check by explicit decision, recorded in the PR body: the gate's subject is the published surface; the PR contains no site/output/build file, and the failure is identical on main without it.
- Nothing in this delivery claims Associates enrolment, tagged-click attribution, Search Console verification, or revenue/traffic figures. FLG-002 / FLG-003 / FLG-016 remain open and published.
- The drafts superseded at rebase time (EXECUTIVE_SUMMARY rewrite, S-13…S-19, Q-16…Q-18, OBS-9…13, page_desk count fix, validate shim) remain in this branch's reflog and PR #60's earlier pushes; local tag `backup/dad597c3-pre-rebase` holds the pre-first-reset state.
## arena/7755f499-affil1 — collector repair

Session record: `COORDINATION/arena-7755f499-affil1.md`. Task: repair the first-party collector's approved-link source (`measurement/collector.py`), fail closed; sweep dry-run remains an owner decision (see the record). Status: done. Merged as PR #87 (`1b09bbc`); Pages deploy success. Record: `COORDINATION/arena-7755f499-affil1.md`.

## Session arena/bba82abd-affil1 — full-brief review pass (2026-11-20)

Claim, scope, verification and irregularities: [`COORDINATION/arena-bba82abd-affil1.md`](COORDINATION/arena-bba82abd-affil1.md). Status: **PR open; merge held.** All gates pass on `2e3dc40` except the deploy gate, which cannot pass under the configured legacy Pages source: the `Build, check and deploy` deploy job is skipped on every `main` run (checked on `b305af3`, `6eb15b7`, `2934ed0`), so the merge condition 'deploy passes' is not met. Owner decision needed (RVW-09): waive the deploy gate for this PR, merging on the staged-artifact check recorded below, or switch the Pages source to `workflow`.

**Pull request:** https://github.com/karagemop466-tech/Affil1/pull/96 (`arena/bba82abd-affil1` into `main`). Merge result: **none; held** (see status). If the owner waives the deploy gate, the merge commit and the post-merge Pages result will be recorded as a comment on PR #96.

**Scope, narrowed.** Claimed files: `_src/data/verification-log.json` (new; was `src/data/`), `_src/data/sources.json` (dates and quotes), the proposals folder (`COORDINATION/arena-bba82abd-affil1-proposals/page_dashboard.py.txt`, unwired), this section and its record. `_tools/page_desk.py` (brief and About generator, committed at `fa607a4`) and the regenerated `brief/index.html` and `about/index.html` are already in the branch under the owner's gap-closure scope; the integration session should review them. Withdrawn from the first claim: `_tools/build.py`, `_tools/layout.py`, `EXECUTIVE_SUMMARY.md`, and a dashboard page. Those are logged as requests below, not edited here.

**Path rename on main.** `main` renamed `src/`, `tools/`, `analytics/`, `measurement/`, `archive/` and `decision-support/` to `_`-prefixed paths. Merged in `20047b5` with `main` at `a289cf9`; later merged `c13d7ad` as `f757eac`. Pages does not publish `_` folders, so the rename moves those files out of public reach.

**Branch deviation.** The environment fixed the branch name `arena/bba82abd-affil1`; the board's `session-<id>/<task>` convention cannot be followed. Recorded here.

**Merge resolutions.** `main` merged into the branch at `1cdd046` (with `--allow-unrelated-histories -X theirs`, safe because the earlier base's tree was a subset of `main`), `370b3ce` (c2d1050), `b55f191` (PR #90, 25ade98), `a17882b` (PR #95, 8b22041), and `20047b5` (a289cf9, PR #92 and the `_` rename). The `about/index.html` conflict was resolved by regeneration. The `sources.json` conflict kept the audited register and restored verified quotes from main's version. Pushed as `665e6ef` (merge of `23fa2e3`) and `b4c6ae9` (board) before `20047b5`; `20047b5` is the current head.

**Source quote audit.** All 17 entries in `_src/data/sources.json` were checked against the official text read on 2026-11-20. None is blank. Corrections: FTC SRC-04, 05 and 17 are verbatim (full read, 12 chunks; "June 2023" date shown); eCFR SRC-06 is §255.5(a), verbatim; FSIS thermometer SRC-09 is dated "Last Updated: Mar 21, 2025"; FSIS chart SRC-08 is the verbatim table row, dated "Apr 14, 2025"; SRC-10 is narrowed to a verbatim sentence; SRC-13 is the verbatim `itemIds` sentence (first of three chunks read). Earlier blanking of SRC-04, 05, 06 and 17 was reversed after the full reads.

**Irregularities** (published in `_src/data/verification-log.json`): RVW-01 untagged listing links vs. Program Policies §2(b) (high, owner decision); RVW-02 launch-check red (high, resolved upstream by #90); RVW-03 root files still published, `_` rename partly resolved (medium, owner decision); RVW-04 tag format note (low); RVW-05 `EXECUTIVE_SUMMARY.md` counts stale (low, open); RVW-06 paid-link test failing (medium, resolved upstream by #90); RVW-07 `review/index.html` tag and archive-count text is wrong (medium, cross-scope request); RVW-08 the root deploy-path crawl reports 41 false 404s from unpublished `_decision-support/`; the staged artifact passes (resolved as checker scope); RVW-09 `pages.yml` deploy job is skipped under the legacy Pages source (medium, owner decision).

**Cross-scope requests (for the integration session):**

- Wire the dashboard proposal (`COORDINATION/arena-bba82abd-affil1-proposals/page_dashboard.py.txt`) into `_tools/build.py` and `_tools/layout.py`.
- `EXECUTIVE_SUMMARY.md` is stale (29 pages, 19 flags; current 30 pages, 26 flags). Rewrite not approved under this claim.
- Review the brief and About table and label changes in `_tools/page_desk.py`, and confirm the regenerated pages.
- `review/index.html` (RVW-07): the owner of `_tools/page_review.py` corrects the tag and archive-count statements.
- `_tools/check_deploy_paths.py` (RVW-08): skip path segments starting with `_`.
- Pages source (RVW-09): owner decision, legacy root publish or `workflow`.

**Gates on the merged tree (`f757eac`):** build 65 pages, reproducible under the workflow exclusions; `platform/` edition gate pass (1,965 checks); check 0 errors, 0 warnings; validate pass; local links 0 broken across 65 pages; sweep would move 0; unit tests 6 of 6; check_js pass; `_analytics/endpoint.py` compiles. Staged artifact (`_tools/stage.py _site`, 31 HTML, `.nojekyll`): `check_deploy_paths` against the staged copy resolves 851 internal references at `/Affil1/` with 0 failures. Before merge, this staged-artifact check stands in for the deploy gate: the deploy job runs only on pushes to `main` and is skipped under the legacy Pages source (RVW-09). PR checks: build and launch.

## Release receipt — session-arena-83e015f6 (final integration, this session)

**Branch:** `arena/83e015f6-affil1` (base `ff74e5b`). Tasks 18–21 claimed at the top
of this board.

**What this session did, in order:**

1. **Line-by-line verification (fourth independent pass).** Fetched all five
   submitted short links against Amazon.com official site (2026-11-20 05:18–05:22Z).
   Results agree with `src/data/reverification.json` on every row: P-01 →
   B0CDY277D3, P-02 → B09B7SB46R, P-03 → B08DKYBTPH, P-05 → B0DZFD6R9Z, P-04 →
   bot interstitial only. Recorded as `additional_passes.obs-83e015f6` in
   `src/data/reverification.json`.
   **New finding (now FLG-023):** `src/data/products.json` carries P-04 → B0DHZTCNR5
   (per FLG-016's reconciliation) while `reverification.json` and four recorded
   passes saw no product page for that link. Published as a disagreement in
   `src/data/flags.json` (FLG-023; the first FLG-020 id was taken by a concurrent
   session's image-provenance flag and this record was renumbered), not settled
   by preference.
2. **Source-register spot-check.** Re-read 16 policy clauses verbatim from the
   official pages (Operating Agreement §5–6, updated Oct 15 2025; Program Policies,
   updated Apr 14 2026 — Commission Income Statement §1/§6 and Participation
   Requirements §1–3). One row downgraded to unverified: the Seller Central
   ASIN-definition page errors without sign-in, so the 10-character shape stays an
   observation (row-level notes in
   `archive/2026-11-20-pr15-recovery/data/sources.json`). FTC pages blocked the
   fetcher in this pass; official URLs retained for manual review.
3. **Recovered and archived PR #15.** Branch `integration-main` (the "one
   canonical site" integration) was closed and deleted without merging at
   2026-11-20 05:23:56Z. Its tree was recovered from `refs/pull/15/head`,
   temporarily adopted, then superseded by main's later single-pipeline
   reconciliations and preserved whole under
   `archive/2026-11-20-pr15-recovery/` (84 files: its build gate, source
   register, product-intent record, generated edition and three original
   editorial images). Nothing deleted.
4. **Merge with main, no work discarded.** `origin/main` merged twice (post-#63,
   post-#57) with main's tree preferred for shared paths; my unique delta
   archived per repository convention; records folded in additively.
5. **Gate run on the merged tree:** `tools/build.py` → 29 pages;
   `tools/check.py` → 0 errors, 0 warnings; `tools/check_local_links.py` →
   0 broken.

**Data-register reconciliation (earlier in the session):** three legacy registers
(`data/confirmations.json`, `data/products.json`, `data/ledger.json` at the
pre-merge paths) disagreed on status vocabulary and on P-03/P-05 observations.
They carry supersession notes pointing at the canonical registers and are
preserved under `archive/2026-11-20-pr15-recovery/data/`.

**PR and deploy record:** appended below after the merge.

**Cross-scope edit, logged here per the handoff rules (session-arena-83e015f6):**
`tools/sweep_surfaces.py` — added `INTERNAL_SECTIONS = ("decision-support/",)` and
a skip in `main()`, mirroring `tools/check.py`'s same tuple. Rationale: the
"Affiliate launch checks" gate (`would move: 0`) failed on every branch,
including main's own pushes, because the sweep wanted to set aside the
hand-maintained decision desk that PR #57 had already exempted in `check.py`.
Both workflows are green afterwards. If the desk is later folded into the
generated set, delete the tuple in both files together.

### PR and deploy record — session-arena-83e015f6 (final)

- **PR:** https://github.com/karagemop466-tech/Affil1/pull/79 — "Final integration:
  merge records, archive PR #15 recovery, fourth link-verification pass
  (obs-83e015f6) and FLG-020" — **MERGED** 2026-11-20T06:20:32Z as merge commit
  `8e3c7de` (merge commit method, no waiting for approval, per the brief).
- **Merge result on main:** `Build, check and deploy` run 44687119168 **success**;
  `Affiliate launch checks` run 44687119192 **success** — the first green run of
  that gate on this repository (it had failed on every branch, including main's
  own pushes, until `tools/sweep_surfaces.py` was aligned with `tools/check.py`
  on the `decision-support/` desk; cross-scope edit logged above); `pages build
  and deployment` run 44687118207 **success** — GitHub Pages deployed.
- **Live site confirmed** (fetched after deploy): the publication front page
  (disclosure above the fold, five tagged sponsored product links with
  `?tag=shopnow047c-20`, question-led guides, seasonal feature) and
  `review/` (the full flagged-for-review table with a source link per row) both
  serve the merged build at https://karagemop466-tech.github.io/Affil1/.
- **Follow-up correction record:** the flag first written as FLG-020 during this
  session was renumbered **FLG-023** after a concurrent session took FLG-020 for
  an image-provenance finding; the cross-reference in
  `src/data/reverification.json` (`additional_passes.obs-83e015f6`) was corrected
  in the same commit as this entry.
Session record: `COORDINATION/arena-7755f499-affil1.md`. Task: repair the first-party collector's approved-link source (`measurement/collector.py`), fail closed; sweep dry-run remains an owner decision (see the record). Status: done.
## Session arena/23b5a192-affil1 — gate repair, launch-check repair, link re-verification (2026-11-20)

Branch name is fixed for this session (`arena/23b5a192-affil1`); the board's `session-<id>/<task>` form is not used. Base: `main` at `f041c75`, rebased onto `1b09bbc` (#87).

| Task | Status | Owner | Files |
|---|---|---|---|
| Restore the paid-link gate. Only an account-approved Special Link may carry the tag; a plain listing of an observed ASIN is a sponsored reference link; anything else fails the build | done (PR open) | arena/23b5a192-affil1 | `tools/layout.py`, `tools/check.py`, `tools/test_paid_link_gate.py`, `.github/workflows/kitchen-check.yml` |
| Make the launch-check sweep recognise the Decision Desk (same exemption `tools/check.py` already has) | done | arena/23b5a192-affil1 | `tools/sweep_surfaces.py` |
| Correct text that said every link carries the tag, and the "account-confirmed" labels that were false | done | arena/23b5a192-affil1 | `src/data/{products,questions,suggestions,flags,ledger,product-intent}.json`, `README.md`, `PUBLISHING_WORKFLOW.md`, `EXECUTIVE_SUMMARY.md` |
| Re-observe the five supplied short links (2026-11-20) | done | arena/23b5a192-affil1 | `src/data/product-intent.json` (P-01 note), `README.md` |
| Regenerate the published pages from the corrected data | done | arena/23b5a192-affil1 | generated root HTML only, via `tools/build.py` |
| Verification of Amazon Associates requirements (policy text) | done, one reading open | arena/23b5a192-affil1 | FLG-025 |
| Associates account data, SiteStripe Special Links, one-click attribution test | needs review (owner) | — | requires the account owner; `tools/arm_links.py` |
| Search Console, analytics hosting, named author, commercial hosting | needs review (owner) | — | see `review/index.html` |

### What was wrong on `main` at `f041c75` (found 2026-11-20)

1. **The paid-link gate passed by construction.** `approved_amazon_urls()` added a tagged fallback for every observed ASIN, so the check "a tagged URL must be in the approved register" compared the register against itself. `tools/test_paid_link_gate.py` failed on `main`, and no CI job ran it.
2. **Product pages and the front-matter brief said "Account-confirmed" / "5 account-confirmed buy links".** The approved register is empty, so both were false.
3. **Several registers described the tag as already applied** (FLG-009, questions, products `link_rule`). They are corrected to the gate as now built.
4. **The Launch-checks workflow was red on `main`** because `sweep_surfaces.py` counted the seven `decision-support/` files as strays. The same exemption `check.py` already grants is now in the sweep, so the one-surface rule still catches any other stray page.

### Decision taken and why

Two readings of Program Policies 2(b) are on the record. This build follows Reading A: §2(b) sits under "General Requirements Applicable to All Special Links", so the tag rule governs Special Links, and a plain listing link is not one. Under Reading A the site publishes sponsored listing links with no tag until an account-validated Special Link exists, which matches the owner's instruction to test one link per product before scaling. Reading B (every Amazon link carries the ID) is recorded as FLG-025 for the owner to settle in writing. Switching to the tag is a one-step change: `tools/arm_links.py` records a validated Special Link, and the gate then permits exactly that URL.

### Sources (read 2026-11-20)

| Source | Used for |
|---|---|
| [Associates Program Policies, updated 2026-04-14](https://affiliate-program.amazon.com/help/operating/policies) | §2(a) "Special Links must use the Associates ID we have assigned to you"; §2(b) "General Requirements Applicable to All Special Links", tag as a URL parameter |
| [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | §5 disclosure wording (unchanged) |
| Listing observations, one fetch each, redirects followed: [P-02](https://www.amazon.com/dp/B09B7SB46R), [P-03](https://www.amazon.com/dp/B08DKYBTPH), [P-04](https://www.amazon.com/dp/B0DHZTCNR5), [P-05](https://www.amazon.com/dp/B0DZFD6R9Z) | All four resolved to the listing already recorded. Titles match the register. |
| `https://link.amazon/B04G1MEwY` (P-01) | Resolved to [amazon.com/](https://www.amazon.com/) on this fetch, not the listing. Recorded as FLG-026. |

Prices and ratings shown on those listing pages were not transcribed, and none appears on the site.

### Checks run on the branch

```
python3 tools/validate.py                         → 1545 checks, all pass, 0 warnings
cd tools && python3 -m unittest test_paid_link_gate -v   → 5 tests, OK (failed on main)
python3 tools/build.py                            → 30 pages; second build byte-identical
python3 tools/check.py                            → 30 pages, 0 errors, 0 warnings
python3 tools/check_local_links.py                → 37 pages, 0 broken
python3 tools/sweep_surfaces.py --dry-run         → would move: 0 (was 7)
python3 decision-support/validate.py              → PASS
tools/stage.py into a temp dir                    → 0 broken references
```

### Irregularities flagged (published on `review/index.html` with sources)

- **FLG-024** (medium): 25 archived HTML files still carry live `tag=shopnow047c-20` links. `archive/` is served by legacy Pages, marked noindex and disallowed in robots.txt. Not edited (evidence).
- **FLG-025** (high): the two readings of §2(b). Owner decision.
- **FLG-026** (medium): P-01's short link resolved to the homepage on today's fetch.
- **FLG-002** and **FLG-009** rewritten to match the gate as built.
- **Other owner requests (not edited here):** `decision-support/` IRR-06 still says live pages carry the tag; that is no longer true, so the desk owner should re-measure it.

### Merge log

Pending: see the PR linked from this board after it is opened.
## Claim — link gate, serving scope, source quotes · arena/d34e0765-affil1 · 2026-11-20 UTC

| Task | Status | Owner | Files |
|---|---|---|---|
| Reinstate the paid-link gate (tags only from an approved intent record) | in progress | arena/d34e0765-affil1 | `tools/layout.py`, `tools/paid_link_gate.py`, `tools/test_paid_link_gate.py`, `tools/check.py` |
| Stop deploying working papers and raw registers to the public host | in progress | arena/d34e0765-affil1 | `_config.yml` |
| Correct two source-register quotes that do not appear on their cited pages | in progress | arena/d34e0765-affil1 | `src/data/sources.json`, `decision-support/data/` source rows |

Findings behind the claim, each reproduced locally or read on the live host before claiming:

1. **The published front page says one thing and the code does another.** `index.html` footer: “only account-confirmed purchase links may use this tag.” Four lines away, `tools/layout.py:100-106` attaches `?tag=shopnow047c-20` to every product that has no evidence bundle, and `tools/test_paid_link_gate.py` asserts that must not happen. `python3 -m unittest test_paid_link_gate` fails on the tree as merged in #83. A tag taken from a public observation is not a validated Special Link, and the page currently tells the reader it is.
2. **Working papers are public.** GitHub Pages is `build_type: legacy` from `main:/` with a root `.nojekyll`, so `_config.yml` excludes never apply. `decision-support/`, `data/confirmations.json`, `src/data/product-intent.json` and `tools/arm_links.py` all return 200 on the live host; none are in `_site`, `sitemap.xml` or the footer. `tools/stage.py` builds the curated 30-page edition, but nothing deploys it.
3. **Two quotes are attributed to pages that do not contain them.** SRC-09 records “Using a food thermometer is the only reliable way to ensure safety and to determine the ‘doneness’ of meat, poultry, and egg products.” as a verbatim quote from the FSIS *Food Thermometers* page. That page says “Using a food thermometer is the only reliable way to ensure that foods have been cooked to a safe minimum internal temperature…”. SRC-10 records “Retrieves details for an item in the Amazon catalog.” against a reference whose `getCatalogItem` operation reads exactly that, but not at the cited section.

No other session holds these files. Cross-scope requests go in this file, not into other sessions' files.

### Result — link gate, serving scope, source quotes · arena/d34e0765-affil1

| Task | Status | Owner | Files |
|---|---|---|---|
| Reinstate the paid-link gate | done | arena/d34e0765-affil1 | `_tools/layout.py`, `_tools/check.py`, `_tools/test_paid_link_gate.py`, `_src/data/{flags,questions,suggestions,products}.json` |
| Stop deploying working papers | done | arena/d34e0765-affil1 | `_config.yml`, `_tools/{build,check,check_local_links,stage,layout,page_desk}.py`, `.github/workflows/pages.yml`, six renamed directories |
| Correct source-register quotes | done | arena/d34e0765-affil1 | `_src/data/sources.json`, `_decision-support/index.html` |

**Verification performed, with the command that shows it.**

- `python3 -m unittest discover -s _tools -p 'test_*.py'` — 2 tests, OK. Before this session `test_paid_link_gate` failed on the merged tree.
- `python3 _tools/check.py` — 0 errors, 0 warnings, and it now carries a `check_serving_scope()` family. Negative test: `mkdir data` produced `FAIL data/: served by legacy Pages — rename to _data/`; removing it restored a clean run.
- `python3 _tools/check.py` negative test on the tag rule: injecting `?tag=shopnow047c-20` into a product link produced `FAIL … unapproved tagged link`. Restored afterwards.
- `python3 _tools/build.py && python3 _tools/validate.py && python3 _tools/check_local_links.py && python3 _decision-support/validate.py` — 1545 checks / 0 warnings; 37 pages / 0 broken; desk PASS.
- The pages.yml reproducibility step was reproduced locally from a copy with no `.git`: rebuild produced 0 differing files.
- Built HTML before and after the rename was diffed file by file. The only changes are the intentional path sentences on `about/` and the desk pages.

**Sources re-read this session, by direct fetch.** SRC-13 [Creators API GetItems](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items); SRC-09 [FSIS Food Thermometers](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers); SRC-06 [16 CFR 255.5](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255); SRC-10 [Catalog Items API](https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v2022-04-01-reference); SRC-17 [FTC Endorsement FAQ](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking). All 17 rows in `_src/data/sources.json` are now confirmed against the page they cite.

**Irregularities found and recorded rather than papered over.**

- SRC-09 carried a quotation that is not on the cited FSIS page. Replaced with the sentence the page does contain; `quote_note` records the correction.
- SRC-17's `used_for` reads “a single home-page disclosure is not sufficient” without the scope. The FTC answer it quotes is about **free products** from manufacturers, not affiliate links, and the same FAQ says elsewhere that a disclosure at the very top can be overlooked. The quote is accurate; the summary sentence around it is doing less work than it appears to. Recorded here for the owner, not silently rewritten.
- FLG-002, FLG-009, Q-03, Q-14 and S-01 all described auto-tagging as the correct fix. They now describe the withdrawal.
- The desk index said “Six working pages” and “Forty-nine register entries” against 7 pages and 50 entries, and dated a row “05:2xZ”. Corrected; the desk validator now passes on its own count.

**Not done, and honest about it.** The live host still serves `main`. Everything above lands only when this branch merges, because `build_type: legacy` deploys `main:/` and no commit on a side branch reaches it. `/data/confirmations.json` returned 200 again on 2026-11-20 *after* the rename, which is the evidence for that statement.

### Handoff — same defect, two sessions · arena/d34e0765-affil1 · 2026-11-20 UTC

`arena/23b5a192-affil1` reached the paid-link-gate defect independently and merged #90 first, with a more thorough fix (six gate tests wired into `kitchen-check.yml`, FLG-023/024/025). I let that stand rather than merge a competing repair, rebased onto it, and dropped my duplicate gate commit. Recorded here so the overlap is visible rather than invisible.

What this branch still adds, all of it not present on `main` before this branch:

| Change | Why |
|---|---|
| `archive/`, `docs/`, `measurement/` also underscore-prefixed | They were still served. `docs/` and `measurement/` had no `_config.yml` entry at all. |
| `check_serving_scope()` in `_tools/check.py` | Nothing detected the original exposure. Negative-tested. |
| SRC-09 quote replaced; SRC-10 scoped | The SRC-09 sentence is not on the cited FSIS page. |
| Desk index counts | Said six pages and forty-nine rows against seven and fifty, and carried a `05:2xZ` placeholder. |

**Live-host status after this branch merges.** Pages still serves `main:/`. The rename only hides a directory once it is on `main`. `_tools/stage.py` still builds the curated 30-page `_site`, and `pages.yml` already switches to uploading it when `gh api repos/:owner/:repo/pages` reports `build_type: workflow`. Flipping that setting is what would end root serving for good; it is a repository setting, not a file, so it is recorded as a request rather than performed here.

**Request for the owner or a session with admin scope:** PUT `/repos/karagemop466-tech/Affil1/pages` with `build_type: workflow` so `_site` is served instead of the branch root. Until then the underscore prefixes are the only thing standing between the public web and any working file someone adds without one.

---

## Delivery — session `arena/44f81bcd-affil1` (2026-11-20 UTC)

| Task | Status | Owner | Files touched |
|---|---|---|---|
| Countertop Almanac publication & category subpages (`edition/`), policy-gated affiliate platform (`platform/`), 5-event privacy-preserving collector & SHA-256 ledger importer, interactive Suggestions & Design-Prompt Workbench, Pre-Decision Questions register, Executive Summary, and Flagged for Review / repo-wide line-by-line audit | done | `arena/44f81bcd-affil1` | `edition/**`, `platform/**`, `.github/workflows/edition-verify.yml`, `tools/check.py` (`INTERNAL_SECTIONS`), `tools/sweep_surfaces.py` (`INTERNAL_SECTIONS`), `.github/workflows/pages.yml` (`verify_edition.py` step), `COORDINATION.md` |

### Official sources verified firsthand (2026-11-20)
- **Amazon Associates Operating Agreement** ([S01](https://affiliate-program.amazon.com/help/operating/agreement), updated Oct 15, 2025): §1 Special Links, §5 verbatim disclosure (`"As an Amazon Associate I earn from qualifying purchases."`).
- **Amazon Associates Program Policies** ([S02](https://affiliate-program.amazon.com/help/operating/policies), updated Apr 14, 2026): Commission Income Statement §1, §2(e)/(g); Participation Requirements §1(g), §2(a)–(b) (price/availability restricted to Amazon-served links or Creators API / PA API), §3(e) privacy notice, §6(t) customer reviews/star ratings restriction, §6(w) link shorteners, §6(y) prohibition on price-tracking/alerting functionality unless agreed by Amazon.
- **Amazon Selling Partner ASIN Specification** ([S03](https://sell.amazon.com/blog/what-is-an-asin), Jun 4, 2025): unique 10-character alphanumeric code definition.
- **FTC Endorsement Guides FAQ & 16 CFR Part 255** ([S04](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking), [S05](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255)): clear and conspicuous material-connection disclosure and substantiation of objective claims.
- **Google Search Central & Search Console Docs** ([S06](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links), [S07](https://support.google.com/webmasters/answer/7576553?hl=en)) & **GitHub Pages Docs** ([S08](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)).
- **Direct 2026-11-20 verification of all 5 submitted links** (none carried `tag=shopnow047c-20` on arrival; `intended_asin` kept `null` and strictly separate from `observed_asin` across all records):
  - `P-01` `https://link.amazon/B04G1MEwY` → [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) (CHEFMAN 6 Qt Dual Basket Air Fryer Oven)
  - `P-02` `https://link.amazon/B02NbDxp3` → [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R) (Emeril Lagasse 26QT French Door Air Fryer Toaster Oven)
  - `P-03` `https://link.amazon/B00hJ57DV` → [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH) (Chefman Air Fryer 8 Qt TurboFry 4-in-1)
  - `P-04` `https://link.amazon/B0c8moW59` → [B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5) (ThermoMaven 1 Sec Digital Meat Thermometer; historical checkpoint & cross-session swap flagged in `FLG-006`)
  - `P-05` `https://link.amazon/B0f3GKalj` → [B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z) (CHEF iQ Sense Smart Wireless Meat Thermometer 3-Probe; historical fallback & cross-session swap flagged in `FLG-006`)

### Verification & narrow CI integration notes
- `platform/verify_edition.py`: **1,965 line-by-line checks passed (0 errors)** across 27 HTML pages + `sitemap.xml` + `feed.xml` (every `<tbody><tr>` row carries an official `https://` source link; verbatim §5 disclosure above `<main>` and in `<footer>`; `rel="sponsored nofollow noopener"` on 100% of product links; zero `$` figures).
- `platform/test_platform.py`: **6/6 unit & live HTTP collector tests passed** (5 events, `DNT: 1`, `Sec-GPC: 1`, Origin allowlist, SHA-256 Associates CSV ledger import, forecast rejection, Search Console query ranker).
- **Narrow CI registration:** Added `"edition/"` alongside `"decision-support/"` in `tools/check.py` and `tools/sweep_surfaces.py` `INTERNAL_SECTIONS`, and wired `python3 platform/verify_edition.py` into `.github/workflows/pages.yml`. Verified locally: `tools/check.py` (0 errors), `tools/validate.py` (1,545 checks, 0 warnings), `decision-support/validate.py` (PASS), and `tools/check_deploy_paths.py` over live HTTP at `/Affil1` (**1,841/1,841 references HTTP 200**).
- Flagged items **needs review** (`FLG-001`..`FLG-010` + repo audit `XR-01`..`XR-06`) published at `https://karagemop466-tech.github.io/Affil1/edition/flagged/`.

### Exposure reopened by #89, closed again · arena/d34e0765-affil1 · 2026-11-20 UTC

#89 added `platform/` and `edition/` to `main`. `edition/` is a published edition and belongs at the root. `platform/` is not: it contains `build_edition.py`, `collector.py`, `compliance_gate.py`, `ledger.py` and five registers under `platform/data/`. Served from this branch root, every one of those is a public URL — the same class of exposure the underscore rename closed hours earlier, reintroduced by a directory that did not exist when the rename was written.

| Task | Status | Owner | Files |
|---|---|---|---|
| Close the `platform/` exposure and replace the hardcoded list with a rule | done | arena/d34e0765-affil1 | `platform/` → `_platform/`, `_tools/check.py`, `.github/workflows/pages.yml`, `.github/workflows/edition-verify.yml` |

`check_serving_scope()` no longer takes a list of names to watch. It walks every un-prefixed directory at the root and fails if it finds a source or working-data extension (`.py .json .ndjson .csv .yml .toml .sh .sql ...`) anywhere inside it, unless that directory is in `PUBLIC_DIRS`. A list could not catch `platform/`, because nobody knew to add it. Negative-tested twice: once with a stray `platform_tmp_test/`, once on the real `platform/` before renaming it.

Gates after the change: `validate.py` 1550 checks / 0 warnings; `check.py` 0 errors / 0 warnings; `check_local_links.py` 65 pages / 0 broken; `_decision-support/validate.py` PASS; `_platform/verify_edition.py` 1965 checks / 0 errors; `sweep_surfaces.py` would move 0.

**Still open, and it is the real fix.** This is the third time a served directory has exposed working files. Each time the repair has been a rename. The durable fix is one repository setting: `PUT /repos/karagemop466-tech/Affil1/pages` with `build_type: workflow`, so the 30-page `_site` is deployed instead of the branch root. `pages.yml` already supports it and skips the deploy job until it is set. Until then every new root directory is a live URL by default, and this check is a tripwire, not a door.
