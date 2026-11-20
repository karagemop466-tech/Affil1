# COORDINATION.md — shared task board

Shared task board for parallel sessions on this repository.

## Session log

| Session | Branch | Claimed scope | Status |
|---|---|---|---|
| `arena/fa9307f7-affil1` | `arena/fa9307f7-affil1` | Full rewrite: `index.html`, `guides/`, `products/`, `compare/`, `questions/`, `suggestions/`, `review/`, `about/`, `operations/`, `brief/`, `assets/`, `src/data/`, `tools/`, `README.md` | done |
| `arena/c7f7070d-affil1` | `arena/c7f7070d-affil1` | Shop-front reconciliation and re-verification | done; account and measurement gaps need review |

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
| Reconcile newly merged PR #23 with generated publication and correct summary; no new guides before measurement | done | arena/c7f7070d-affil1 | `src/data/*.json`, `tools/*.py`, generated HTML, `EXECUTIVE_SUMMARY.md`, `COORDINATION.md` |

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

## Publication desk — eaf80f48 (2026-11-20)

| Task | Status | Owner | Files |
|---|---|---|---|
| Front-page publication design, reader guide discovery, fresh source spot checks and integration | in progress | arena/eaf80f48-affil1 | tools/page_home.py, tools/layout.py, new assets/css/editorial.css, assets/js/discover.js, assets/img/edit-*, generated maintained HTML, COORDINATION.md |

Prior integration #27 is merged. This scope does not edit the legacy editions, their data or the other open PRs.
### PR and deployment result — arena/c9fc4295-affil1

- [PR #27](https://github.com/karagemop466-tech/Affil1/pull/27) merged as `92a3509c9a56bbd6aa01eef8d7ae0afbb4ab7f06`; the PR build and link checks passed.
- GitHub Pages [deployment run 44682421711](https://github.com/karagemop466-tech/Affil1/actions/runs/44682421711) succeeded; the Pages API reported `built` for that merge commit.
- Audit and link repairs: done. Full legacy-edition reconciliation, product intent, tracking attribution, and live analytics: **needs review** as detailed in FLG-016/017 and the measurement page. The older crisp-specific validator remains incompatible with the current data schema.
## Reconciliation — arena/c7f7070d-affil1, 2026-11-20

PR #23 and PR #26 landed after the initial claim; PR #27 landed while this work was in progress. Work was stashed and rebased, then stash-application conflicts were resolved by retaining PR #27's destination warnings and review flags, combining the source-link and event-spec corrections, and regenerating output from the combined templates. No other session's edition was deleted. The parallel claim overlaps this one; future cross-scope changes should be coordinated here rather than silently overwritten.

Two independent fetches in this session reached [P-04 B0DHZTCNR5](https://link.amazon/B0c8moW59) and [P-05 B0DZFD6R9Z](https://link.amazon/B0f3GKalj), respectively; PR #27 reports the reverse. The conflict is retained as FLG-016, not resolved by assumption. Intended product and attribution remain unknown. Added explicit null intent URL/date/source fields, corrected stale counts and the P-02 dishwasher assertion, and removed a fabricated blank ledger row. Aligned the measurement *documentation* to the five canonical event names; the existing disabled client still uses different names and must not be mistaken for a working implementation. Sources read: [Amazon Agreement](https://affiliate-program.amazon.com/help/operating/agreement), [Amazon Policies](https://affiliate-program.amazon.com/help/operating/policies), [FTC FAQ](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking), [Google Performance report](https://support.google.com/webmasters/answer/7576553) and [Search Console verification](https://support.google.com/webmasters/answer/9008080).

Checks: `python3 tools/build.py`, `python3 tools/check.py` (22 generated pages, 0 errors, 0 warnings), and `python3 tools/check_local_links.py` (65 pages, 0 broken relative file references). The legacy validator and live measurement remain needs review, as do all account-gated work and full cross-edition factual verification. Link checks do not establish attribution, stable redirects, or buyer intent.

Rebase after PR #28: a task-board conflict was resolved by retaining both merge/deployment histories and this reconciliation record.

Integration note (eaf80f48): preserved both board entries after the concurrent append conflict. PR #32 owns measurement; this session will not duplicate that work. Additional scope: tools/stage.py to include the new reader assets in Pages artifacts.

### Reader-facing release — eaf80f48

- Updated the maintained templates, not the legacy storefronts. A seasonal cover leads into a filterable five-product shelf, short reading paths and local search. No-JS readers can browse all five cards and follow ordinary links. Disclosures still appear under the masthead and in the footer.
- Checked the five submitted links against the arrived-at Amazon listing titles on 2026-11-20: [P-01](https://www.amazon.com/dp/B0CDY277D3), [P-02](https://www.amazon.com/dp/B09B7SB46R), [P-03](https://www.amazon.com/dp/B08DKYBTPH), [P-04](https://www.amazon.com/dp/B0DHZTCNR5), [P-05](https://www.amazon.com/dp/B0DZFD6R9Z). These are observations only. FLG-016 remains open because another observation reverses the thermometer pair. None of these landing URLs established the supplied tracking ID or the owner's intent. No price, rank, demand or conversion figures were imported.
- Checked the [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) for its tagged-link requirement. No new monetized link was constructed or labeled approved. Authorized Associates reports and a production host remain prerequisites, not inferred facts.
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
Integrated merged #31/#32; retained both task-board histories. Search Console, collector hosting and Associates reports remain unconfirmed.
