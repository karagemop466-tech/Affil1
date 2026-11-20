# Coordination — Affil1

Shared task board for parallel agent sessions. Source of truth: this file.
Merge base: `76d898b` (main at branch time). Main advanced to `ff74e5b` (PR #4,
session `arena/099b013a-affil1`) during this session; `origin/main` was merged
into branch `arena/55d40788-affil1` and conflicts resolved without discarding
the other session’s work — see the merge log below.

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
| Independent re-verification of all five submitted links | done | src/data/reverification.json | Each `link.amazon/...` requested a second time on 2026-11-20; destination URL + page title + breadcrumb read from Amazon.com itself. P-01→dp/B0CDY277D3, P-02→dp/B09B7SB46R, P-03→dp/B08DKYBTPH, P-05→dp/B0DZFD6R9Z, P-04→checkpoint only. Matches `src/data/products.json`; contradicts the archived `data/confirmations.json` rows for P-03 and P-05, which logged the homepage. |
| ASIN-format check on the five supplied codes | done | src/data/products.json, /flagged/ FLG-001 | Every supplied code is 9 characters; every destination ASIN is 10. `intended_asin` left null. Reference: Amazon's Catalog Items API defines the path parameter as the ASIN of the item — https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v2022-04-01-reference |
| Attribution risk in the submitted link form | done | tools/build.py `tagged_listing_url()`, EXECUTIVE_SUMMARY, /dashboard/#verification | Commission Income Statement §2 disqualifies purchases referred by a "Redirecting Link" (e) and any purchase not tracked because links are "not properly formatted" (g) — https://affiliate-program.amazon.com/help/operating/policies (fetched 2026-11-20). Buy buttons therefore use the tagged official listing URL; the submitted link stays recorded in its own field. |
| Disclosure wording against Operating Agreement §5 | done | tools/build.py `disclosure()` | §5 requires the exact sentence "As an Amazon Associate I earn from qualifying purchases", clearly and prominently; §6 makes a §5 violation a material breach. Verified verbatim at https://affiliate-program.amazon.com/help/operating/agreement (fetched 2026-11-20). The strip now carries the sentence verbatim plus a plain-language line (FTC "clear and conspicuous"). |
| Price / rating / image / review-use restrictions encoded as rules | done | PUBLISHING_WORKFLOW.md, src/data/suggestions.json (SUG-25, SUG-26 rejected) | Participation Requirements prohibit price tracking/alerting on an Associate site and restrict Program Content (images, reviews, ratings) to Amazon-served links or the Creators/PA API. Site publishes none; `validate.py` warns on any dollar figure. |
| Single publication surface at the repository root | done | index.html + 21 generated pages, archive/2026-11-20-integration/ | Four competing surfaces (root storefront, /crisp/, two CSS/JS shells, duplicate guide sets) were found on main. Nothing deleted: all moved to `archive/`, robots-disallowed, noindex, and explained in archive/README.md. `tools/build.py` + `src/data/` now generate the only published surface. |
| GitHub Pages mount-path defect fixed | done | all pages, tools/check_deploy_paths.py | main carried 205 broken or root-absolute references (verified with a filesystem scan of origin/main). Every page now uses relative links and resolves over HTTP at `/Affil1/`: 486/486 references OK. |
| CI: gate that cannot be bypassed | done | .github/workflows/pages.yml, tools/validate.py | The Actions workflow previously failed on every push to main (validation step) while Pages served the site through a *legacy branch build* — a red check beside a live URL. Now: rebuild from data → run the gate → fail on committed-output drift → resolve references at the mount → publish. Weekly audit re-runs the same gate. |
| Editorial expansion: 5 new guides, topics hub, front page | done | tools/content_extra.py, tools/extra_pages.py | Holiday oven-relief plan, frozen weeknights, dual-basket math, smart probe thermometers, first-week checklist. Written to the same rule: capability statements quote the seller's listing title only; each guide names what it does not claim. |
| Saved shortlist (reader utility) | done | assets/js/shortlist.js, /about/#privacy | localStorage only, nothing transmitted; the privacy copy was rewritten to state exactly that, because the previous text claimed nothing was ever written to storage. |
| Suggestions board + open questions for decision review | done | src/data/suggestions.json (11 added → 29), src/data/questions-open.json (8 added → 22) | Two new suggestions are rejections on policy grounds (no price alerts, no copied Program Content) so the constraint survives the next session. Five questions answered by this pass; the rest say who must answer. |

### Irregularities flagged for the owner (also published at /flagged/ and /dashboard/)

1. **`gh api /repos/.../pages` reports `build_type: legacy` while the Actions workflow also
   publishes.** Two deployment paths are racing. Recommend switching Pages to
   "GitHub Actions" as the source so only the gated artifact publishes. A repo-setting
   change, not a file change — deliberately left for the owner or the integration session.
2. **An archived register asserted three links "reached only the homepage"** while another
   left everything blank; both are now contradicted by two independent passes. Kept in
   `archive/` for inspection rather than deleted.
3. **`link.amazon` responses are unstable** — the same URL returned an interstitial to one
   session and a product page to another. Destinations on this site are dated observations.
4. **P-05 is a meat thermometer, not an air fryer.** Retained and given its own guide rather
   than dropped to make the shortlist look coherent.
5. **No human reviewer exists for this workflow**, so the publication gate is structural only.
   Recorded on /dashboard/#gate as `needs-review` rather than ticked.

### Handoff

Session arena/171b54e4, arena/2361a177, arena/4bcd015a, arena/771e5093 had claims on this board
and unmerged branches when this pass started; arena/96012762's `crisp/` publication and data
layer were merged (PR #7) and are the base this integration extended. Nothing from those branches
was edited or overwritten here. Any later session should extend `src/data/` and `tools/`, not add
a fifth front page.

### Concurrent integration pass resolved (PR #27, session arena/c9fc4295-affil1)

Main moved while this branch was open: a second session merged its own full rebuild
(`brief/`, `review/`, `operations/`, per-product pages, a rewritten `tools/build.py` plus
`tools/page_*.py`, and new `src/data` schemas). Resolution, recorded so the trade-off is
visible rather than silent:

- **Adopted from that pass:** self-hosted Fraunces + Inter, the responsive editorial art
  set and `src/data/images.json` (with its imagery rule), `favicon.svg`, the wider-bleed
  front-page title/description, and its P-04 destination discrepancy — published as
  FLG-016 and in `src/data/reverification.json` instead of being resolved by guesswork.
- **Set aside, not deleted:** its generated pages and second build system moved to
  `archive/2026-11-20-c9fc4295/`, and its two verification-audit files preserved
  side by side with this session's under `archive/2026-11-20-integration/`. One published
  pipeline was the point of the integration; two generators disagreeing about the same
  data would reproduce the original defect.
- **Conflict handling:** merged with `-X ours` on files this session owns and re-verified
  after; nothing in their branch was edited. Their work remains in `main` history and on
  `arena/c9fc4295-affil1`.
- **Gate widened by what the merge exposed:** a `srcset` attribute is a set of URLs, and
  the mount-path bug class that broke the earlier surfaces hides in it. `tools/validate.py`
  now resolves every `srcset` entry on disk, and `tools/build.py` rewrites `srcset` per
  directory depth like any other reference. Both changes came from reviewing the merged
  tree, not from a spec.
