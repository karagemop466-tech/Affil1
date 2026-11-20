# Coordination — Affil1

Shared task board for parallel sessions on this repository. Read this before
claiming any work.

## Sessions

- `arena/8e0006cf-affil1` (PRs #1, #2; merged into main before this session):
  Good Measure Kitchen storefront — `index.html`, `styles.css`, `app.js`,
  `data.js`, `guides/`, `feed.xml`, `sitemap.xml`, `.github/workflows/pages.yml`,
  `README.md`, `COORDINATION.md`. GitHub Pages deploy previously reported
  successful (run 44679102768).
- `arena/099b013a-affil1` (PR #3, merged into main as ff74e5b during this
  session): Affil1 shop surface — `categories/`, `dashboard.html`,
  `products.html`, `executive-summary.html`, `disclosure.html`, `privacy.html`,
  `data/`, `assets/`, `css/`, `js/`, `server/`, `rss.xml`, `EXECUTIVE_SUMMARY.md`,
  `PUBLISHING_WORKFLOW.md`, `reviews/flagged.html`, plus root-level
  `questions.html`, `suggestions.html`, `sitemap.xml`, `robots.txt`.
- `arena/55d40788-affil1` (this session, PR #6): publication front page rebuild,
  product-intent confirmation records, five-event privacy-preserving analytics
  with self-hostable endpoint, decision-support pages (suggestions, questions),
  merged sitemap/feed, this board.
- `arena/c58c5996-affil1` (PR #5, merged into main as ed46d41 during this
  session): integrated front page + CSS/JS/data/feed variants, plus unique pages
  `guides/air-fryer-category.html`, `guides/executive-summary.html`,
  `guides/pre-decision-questions.html`, `guides/suggestions.html`.

## Merge log (2026-11-20)

Merging `origin/main` into `arena/55d40788-affil1` produced conflicts on:
`COORDINATION.md`, `index.html`, `guides/basket-or-oven.html`,
`guides/capacity-checklist.html`, `questions.html`, `suggestions.html`,
`sitemap.xml`. Resolution: this session’s verified versions kept at those paths;
the parallel session’s conflicting versions preserved under
`archive/session-099b013a-affil1/` (content retained, not discarded). `sitemap.xml`
is the URL-set union of both sessions. No work was discarded.

Second merge: origin/main (ed46d41, session arena/c58c5996-affil1) into
arena/55d40788-affil1 produced conflicts on COORDINATION.md, analytics.js,
app.js, data.js, feed.xml, index.html, sitemap.xml, styles.css.
Resolution: this session's verified versions kept at those paths; the parallel
session's conflicting versions preserved under
archive/session-c58c5996-affil1/; their unique guide pages under guides/
were retained. sitemap.xml re-computed as the URL-set union of both sessions.
No work was discarded.

## Claims (task | status | owner | files touched | sources verified)

| # | Task | Status | Owner | Files touched | Sources verified |
|---|------|--------|-------|---------------|------------------|
| 1 | Repo review + coordination setup | done | session-arena-f10ea853 | COORDINATION.md, README.md | n/a |
| 2 | Verify 5 submitted Amazon links against official Amazon sources | done (claimed) | session-arena-f10ea853 | data/confirmations.json | Amazon.com official site claimed: B04G1MEwY->dp/B0CDY277D3; B02NbDxp3->dp/B09B7SB46R; B00hJ57DV->homepage; B0c8moW59->checkpoint; B0f3GKalj->homepage. Fetched 2026-11-20. **Irregularity: this session could not independently re-verify these mappings (no direct amazon.com access from sandbox); they are flagged, not treated as confirmed.** |
| 3 | Publication front page + CSS/brand | done | session-arena-f10ea853 | index.html, assets/css/main.css | n/a |
| 4 | Category subpages + product tables with per-row source links | done | session-arena-f10ea853 | categories/air-fryers.html | official Amazon links per row |
| 5 | Dashboard page (entries/findings table + analysis) | done | session-arena-f10ea853 | dashboard.html | official Amazon links per row |
| 6 | Publication front page leading with products (this session) | done | arena/55d40788-affil1 | index.html, styles.css, app.js | Local link check; live smoke test 200 |
| 7 | Product-intent confirmation records (intended ASIN; official listing URL, confirmation date, source; observed redirect separate; all blank/unverified) | done | arena/55d40788-affil1 | data.js, guides/flagged-for-review.html | User-supplied URLs preserved exactly; no values inferred |
| 8 | Self-hosted analytics endpoint + outbound click counter (5 events) | done | both sessions | assets/js/analytics.js, server/collect.js; analytics.js, analytics/endpoint.py | n/a |
| 9 | Disclosure strip above the fold on every page + footer repeat | done | both sessions | assets/js/common.js, all pages; index.html, guides/*.html, suggestions.html, questions.html | Amazon Associates Operating Agreement §5; FTC Endorsement Guides FAQ |
| 10 | Sponsored marking on all outbound product links | done | both sessions | all product links | Amazon Associates program policies |
| 11 | RSS feed + sitemap.xml + Search Console readiness | done | both sessions | rss.xml, sitemap.xml, robots.txt, feed.xml | n/a |
| 12 | Question-shaped buying guides (editorial hypotheses) | done | both sessions | guides/*.html | n/a (working titles only) |
| 13 | Suggestions section for decision review | done | both sessions | suggestions.html (both versions retained) | n/a |
| 14 | Campaign ledger (empty, dated provenance trail) | done | both sessions | data/campaign-ledger.json; index.html ledger | n/a |
| 15 | Compliance gate: disclosure + API policy checks in publishing workflow | done | session-arena-f10ea853 | PUBLISHING_WORKFLOW.md | Amazon Associates Operating Agreement, FTC |
| 16 | Executive summary | done | session-arena-f10ea853 | EXECUTIVE_SUMMARY.md | n/a |
| 17 | Flagged for Review page(s) | done | both sessions | reviews/flagged.html, guides/flagged-for-review.html | n/a |
| 18 | Integration: merge with main, re-verify line by line, build check, broken-link check | done | arena/55d40788-affil1 | all | Local reference check passed on 9 pages; sitemap/feed XML parse; smoke test 200 |
| 19 | PR to main, merge, enable GitHub Pages, confirm deploy | in progress | arena/55d40788-affil1 | PR #6, main branch, repo settings | n/a |

## Rules

- Claim a task by writing your session ID and file scope, commit and push the claim immediately.
- Never start a task another session has claimed. Keep scopes non-overlapping.
- Small, frequent commits; `git pull --rebase` before every push.
- On merge conflict: stop, resolve without discarding the other session’s work, log what happened here.
- `needs review` = published on a Flagged for Review page; does not block other work.
- Nothing is marked verified without checking against an official source; link that source.
- Shared outputs (table data, index, navigation) change only in the final integration session.

## Sources and verification log (this session)

- Amazon Associates Program Operating Agreement, section 5:
  https://affiliate-program.amazon.com/help/operating/agreement — disclosure:
  “As an Amazon Associate I earn from qualifying purchases.” Appears above the
  masthead and in the footer on all 9 site pages.
- Amazon Associates Program Policies:
  https://affiliate-program.amazon.com/help/operating/policies
- FTC Endorsement Guides FAQ:
  https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
- User-supplied links preserved exactly: https://link.amazon/B04G1MEwY,
  https://link.amazon/B02NbDxp3, https://link.amazon/B00hJ57DV,
  https://link.amazon/B0c8moW59, https://link.amazon/B0f3GKalj. No redirects
  followed; intended ASIN and observed redirect are separate fields; both
  unverified/blank.

## Irregularities / unresolved decisions

- All five `link.amazon/...` destinations and intended ASINs are unverified;
  enrolled Associates workflow confirmation pending. The parallel session’s
  claimed Amazon mappings (claim #2 above) could not be independently re-verified
  and are flagged for review — not claimed valid, not claimed invalid.
- Selected tracking ID `shopnow047c-20` is user-supplied; enrollment and site
  association unverified.
- No analytics endpoint credentials; beacon disabled until the operator
  self-hosts `analytics/endpoint.py`. Campaign ledger empty by design; no
  conversion score or revenue forecast.

## Delivery

- PR: https://github.com/karagemop466-tech/Affil1/pull/6 — pending merge to
  `main`, then GitHub Pages deploy confirmation.

## Claims — session arena/359baa16-affil1 (integration + publication rebuild, started 2026-11-20 05:12 UTC)

| Task | Status | Owner | Files touched | Notes |
|---|---|---|---|---|
| Independent line-by-line re-verification of all 5 submitted links (contradictions in data/confirmations.json vs data/products.json vs guides) | in progress | arena/359baa16-affil1 | data/verification.json | Each link fetched this session; prior session claims re-checked |
| Final integration: one coherent published surface, single design system, relative links for the /Affil1/ Pages base path | in progress | arena/359baa16-affil1 | index.html, guides/, categories/, assets/, .github/workflows/pages.yml, sitemap.xml, rss.xml, robots.txt | Superseded prior pages moved to archive/, never deleted |
| Suggestions + pre-decision questions + flagged-for-review pages (decision support) | in progress | arena/359baa16-affil1 | suggestions.html, questions.html, flagged.html | |
| Publishing machinery + compliance gate in CI (build, broken-link check, sponsored/disclosure lint) | in progress | arena/359baa16-affil1 | tools/build.py, tools/check_site.py, tools/verify_links.py | |
| Executive summary refresh | pending | arena/359baa16-affil1 | EXECUTIVE_SUMMARY.md, README.md | |

Concurrent claims noted (not touched by this session): arena/171b54e4 (publication rebuild), arena/2361a177 (publication rebuild scope), arena/4bcd015a (sourced publication + tools/check_site.py), arena/771e5093 (decision-support hub), arena/96012762 (Crisp & Counter + tools/build.py). Those branches were not merged into main by 05:18 UTC; this session works on its own branch and does not edit their files. Anything of theirs already on `main` is preserved in `archive/` and, where it is the better page, kept in place.

Handoff/takeover note: sessions arena/f10ea853, arena/c58c5996 and arena/55d40788 marked tasks done and merged via PRs #3, #5, #6, #8 — their claims are closed, so this session may integrate their outputs.

## Integration record — session arena/359baa16-affil1 (2026-11-20, 05:12–05:45 UTC)

### Tasks completed (replaces the in-progress table above)

| Task | Status | Files touched | What was verified |
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
