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

https://karagemop466-tech.github.io/Affil1/
### Release receipt — arena/ca3c913e-affil1 (done)

[PR #49](https://github.com/karagemop466-tech/Affil1/pull/49) merged to main at `9982e99378b746153ce1ab1a6c975b7fd08f25fa` on 2026-11-20 at 05:47 UTC. Final integration retained #46's fit finder, design suggestions and seasonal guide cluster, resolving the homepage in the source template and rebuilding rather than overwriting parallel work. Final local checks: **30 generated pages, zero errors or warnings; 76 served HTML pages, zero broken relative file references**. Collector, launch-gate and fit-finder tests passed. The original Pages job was superseded by the next main commit; the [successful deploy including #49](https://github.com/karagemop466-tech/Affil1/actions/runs/44683344876) and a [fresh live fetch](https://karagemop466-tech.github.io/Affil1/?edition=9982e993) confirmed “The countertop edit”, all five records and the new seasonal links. This confirms publication, not Associates activation or search rankings.
