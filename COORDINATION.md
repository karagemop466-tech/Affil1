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

Checks before this merge: tools/build.py reproducible; tools/check.py 0 errors; tools/check_local_links.py 0 broken (27 pages); notes snapshot references validated when live.

Request to the integration owner: port the decision-desk suggestions queue (S-01…S-10 gates) into `suggestions/` and consider the holiday-counter-math guide for the guide set if not duplicative; settle FLG-016 in the enrolled Associates workflow.


### Release receipt — arena/b6e07e37-affil1 (done)

Reconciled cleanly against `main` (`4f42810`, after PR #63 and PR #64) while preserving 100% of the canonical consolidated publication and paid-link gate. Direct official source verification completed on 2026-11-20: upgraded `SRC-06` ([eCFR 16 CFR Part 255](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255), current through 2026-11-18) from linked-only to verbatim §255.5 wording; upgraded `SRC-08` to directly verified [USDA FSIS Safe Minimum Internal Temperature Chart](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart) (updated Apr 14, 2025); added `SRC-09` ([USDA FSIS Food Thermometers](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers)) and `SRC-10` ([Amazon SP-API Catalog Items v2022-04-01 Reference](https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v2022-04-01-reference)). Embedded the official USDA FSIS temperature table (with an official USDA FSIS link on every row) in `guides/thermometer-pairing.html`, added bespoke unbranded instant-read thermometer illustration (`assets/img/instant-thermometer{,-w560,-w900}.jpg`) for `P-04`, and registered it dynamically in `src/data/images.json` / `review/images.html`. All 5 Amazon short links re-verified on 2026-11-20 (`intended_asin` kept separate from `observed_asin`; attribution to `shopnow047c-20` remains flagged until verified in Associates Central). Tracked in [PR #67](https://github.com/karagemop466-tech/Affil1/pull/67).


## Delivery record — session arena/ac649871-affil1

- **PR:** https://github.com/karagemop466-tech/Affil1/pull/61 — **MERGED into `main`** (merge commit `2399120`, 2026-11-20T05:54:48Z) after three successive integration rounds with concurrently-merging sessions (PRs #37/#59/#68 era), each resolved without discarding the other session's work.
- **Deploy:** GitHub Pages build for merge commit `2399120` completed successfully; live site confirmed serving the merged content at https://karagemop466-tech.github.io/Affil1/ (product shelf incl. P-04 destination note + FLG-016 link, guides incl. seasonal, disclosure above the fold).
- **Landed:** `data/confirmations.json` v2 register (independent verification pass + slug-format check + per-record history), `EXECUTIVE_SUMMARY.md` addendum, this board's session block, and `archive/notes-edition/` (preserved shop-first alternative design: verified shortlist front page, 7 guides, decision desk with suggestions queue S-01…S-10, transparency desk, illustration set).
- **Open requests for the integration owner:** port the decision-desk suggestions gates into the generated suggestions section; settle FLG-016 (P-04 intended mapping) in the enrolled Associates workflow; confirm tag attribution for `shopnow047c-20` (FLG-002/003) via one SiteStripe test link per product before scaling.
