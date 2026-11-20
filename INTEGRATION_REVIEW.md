# Integration review — 2026-11-20

## Scope and status

This is a read-only review of the published `main` tree and the competing publication proposals. It does not choose or merge another session's work. No site implementation was changed in this branch; findings for the active publication PR were posted there for its owner.

- Fixed branch: `arena/487e4183-affil1`.
- Latest inspected `origin/main`: `7b236c2` (PR #26 merge).
- Open PRs at latest check: #9 (older publication proposal), #12 (older guide-link repair), #19 (cross-scope audit), and #24 (guide navigation/audit surface). PRs #22, #23, #25, and #26 have merged; PRs #15 and #11 closed without merging.
- GitHub Pages API reports `build_type=legacy`, source branch `main`, path `/`.
- Latest observed runs for PR #26: custom workflow `44682252872` successfully built/staged but skipped Actions artifact upload/deploy because Pages is legacy; the legacy Pages build/deployment `44682251402` succeeded. The current root, `/crisp/`, and an archived storefront were fetched after deployment. This confirms the current main deployment, not a single curated artifact.

## Official references

| Topic | Official reference | Use in this review |
|---|---|---|
| Associates Special Links and disclosure | [Amazon Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | A tagged link and the required Associates disclosure are program obligations; the page itself does not prove a particular submitted link's enrollment or attribution. |
| Current Program Content / participation requirements | [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | Check current policy before publishing Program Content or automating data collection. |
| ASIN format | [Amazon ASIN article](https://sell.amazon.com/blog/fba-new-selection-program) | An ASIN is a unique 10-character alphanumeric identifier. The submitted path tokens are 9 characters and cannot be treated as confirmed ASINs. |
| Endorsement disclosures | [FTC Endorsement Guides FAQ](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) | Supports clear, conspicuous disclosure near endorsements/links. |
| Search measurement | [Google Search Console start guide](https://developers.google.com/search/docs/monitor-debug/search-console-start) | Verification, sitemap submission, and query reporting require property/account setup. |
| Static hosting | [GitHub Pages overview](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) | Pages is static hosting; it does not run a custom analytics server. |

## Product-link observations

These are fetch observations recorded on 2026-11-20, not confirmations of intended products, account enrollment, compliant Special Links, or attribution:

| Submitted token | Observed destination | Important limitation |
|---|---|---|
| `B04G1MEwY` | `/dp/B0CDY277D3` | Observed destination only. |
| `B02NbDxp3` | `/dp/B09B7SB46R` | Observed destination only. |
| `B00hJ57DV` | Conflicting observations: Amazon homepage in an earlier fetch; `/dp/B08DKYBTPH` in a later fetch. | Preserve the conflict; do not set intended ASIN from either observation. |
| `B0c8moW59` | Amazon `/checkpoint/continue` interstitial in the latest recorded fetch. | No product listing observed; status unresolved. |
| `B0f3GKalj` | Conflicting observations: Amazon homepage in an earlier fetch; `/dp/B0DZFD6R9Z` in a later fetch. | Preserve the conflict; do not set intended ASIN from either observation. |

The short-link status remains unresolved. No claim is made that any submitted URL is invalid. An Associates account workflow/report was not available in this review, so the tracking ID and attribution remain unverified. Keep intended listing fields separate from redirect observations.

## Existing `main` publication

1. The repository is currently published from the `main` branch root. The root storefront links to a second publication under `/crisp/`; the unioned sitemap contains URLs from both.
2. Archived storefronts are still reachable under `/archive/session-099b013a-affil1/` and `/archive/session-c58c5996-affil1/`. Both paths were fetched successfully from the live Pages host. Test-gate exclusions do not make these files private or unpublished. A single canonical publication must be selected, and the publishing mechanism must exclude or otherwise safely retire alternate HTML surfaces.
3. The current Pages API source is `main:/`, not an Actions-only artifact configuration. PR #26's workflow stages `_site` but detects the legacy source and skips artifact upload/deployment; the Jekyll branch-root build publishes the repository tree.
4. On a fresh archive of `origin/main` `7b236c2`, `python3 tools/build.py && python3 tools/check.py` passed for 22 generated pages. `tools/stage.py _site` produced a 22-page staged directory, but the Pages setting does not deploy it. The repository tree still contains 73 HTML pages. An independent local-reference/fragment crawl found 1,766 local references and 53 broken references (32 root-level, 21 archived; 0 in `/crisp/`). Examples include old guide pages with missing local files/fragments and broken archived storefront navigation. The legacy `python3 tools/validate.py` fails immediately with `KeyError: 'supplied_path_code_length'` because PR #23 changed the product fields to `submitted_code` / `submitted_code_length` and `observed_asin`. A passing generated-page gate is not a whole-tree or deployment check; PR #19 separately records related findings.

## Open publication proposal: PR #9

The branch was fetched without checking it out, archived under `/tmp`, and tested in isolation:

```text
python3 tools/check_site.py --build
OK: checked 12 HTML pages, local navigation, above-fold/footer disclosures,
sourced product/decision rows, outbound-link attributes, five event names,
sitemap, and feed.
Built 12 pages into _site/
```

The register is cautious: it preserves all five submitted links, leaves intended and observed identity fields blank, marks them unverified, and does not call them invalid. Its current product controls carry `rel="sponsored nofollow noopener"`. The main unresolved review points are:

- **Publishing-source mismatch:** the checked GitHub Pages setting is legacy branch-root (`main:/`), while PR #9's workflow builds `_site/` and uses `upload-pages-artifact` / `deploy-pages`. A workflow file and a passing local artifact build do not establish that Pages is serving that artifact. With branch-root publishing, the existing `/crisp/` and `/archive/` content remains reachable outside the generated 12-page artifact. Align the Pages setting and workflow (if authorized), or otherwise reconcile publication, then check the actual public tree and deployment run.
- **Event contract mismatch:** the requested events are `page_view`, `outbound_click`, `guide_open`, `search_query_referral`, and `report_import`. PR #9's client/server/checker define `page_view`, `guide_open`, `outbound_product_click`, `comparison_tool_use`, and `suggestion_choice`. The search-referral and report-import events are not implemented, and the names differ. The endpoint is configured off; keep it that way until the event contract, privacy notice, retention, and separate host are complete.
- **Category coverage:** the proposal has a shortlist/product register and four guides, but no dedicated category landing page or category navigation. The request explicitly includes category pages.
- **Build-gate coverage:** actual disclosure placement looks correct in the pages inspected, but the gate only counts the disclosure sentence twice; it does not assert placement before `<main>` and inside `<footer>`. The product-row source check accepts any Amazon policy URL rather than tying a source to each nonblank fact. Current product identity cells are blank, which is safer, but the checks should enforce the stated rules rather than imply they already do.
- **Account-dependent link verification:** the links are visibly unverified, which is appropriate. Keep the status unresolved, do not infer intent from redirects, and do not claim enrollment or tracking compliance without the Associates workflow.

These findings were posted on [PR #9](https://github.com/karagemop466-tech/Affil1/pull/9#issuecomment-7031344781). The independent current-main crawl results were shared on [PR #19](https://github.com/karagemop466-tech/Affil1/pull/19#issuecomment-7031369267). These are integration requirements and evidence gaps, not a claim that the PR #9 local build fails.

## Closed integration proposal: PR #15

The isolated candidate passed its own `npm run verify`: 24 generated pages, zero gate violations, and 7/7 deliberate gate violations caught by its negative self-test. It was closed without merging. The review identified a publish-scope issue: it retained tracked archive HTML while its gate excluded `archive/`; the repository's legacy branch-root Pages setting means gate exclusion alone does not prevent those files from being served. Additional candidate-level concerns were recorded in the PR discussion, including confirming product-link/account attribution, checking product-specific narrative claims against sources, matching the required analytics event contract, and running its gate on pull requests if it is described as a PR gate.

## Merged publication and follow-ups: PRs #22, #23, #25, and #26

PR #22 was merged as `54b2b45`; PR #23 added the new P-04 observation and homepage changes (merge `0691fa7`); PR #25 corrected the summary page count; PR #26 moved the homepage toward buyer decisions and added a staging script (merge `7b236c2`). The current root page was fetched with a cache-busting query after deployment. It is a polished, reader-first Crisp & Counter front page with a disclosure above the fold, three air-fryer product cards, question-led guides, a separate thermometer section, and no prices or ratings.

The PR #26 custom workflow (`44682252872`) successfully built and staged 22 pages. It then detected `build_type=legacy` and skipped Actions artifact upload/deployment. The separate legacy Pages build/deployment (`44682251402`) succeeded. GitHub Pages API still reports `main:/`, status `built`.

Current checks and unresolved integration issues:

- **The deployed tree is broader than the generated edition.** `tools/build.py && tools/check.py` passes 22 generated pages; `tools/stage.py _site` stages those 22 pages. But the legacy branch-root build still exposes the repository tree: 73 HTML files after the build, including the older `/crisp/` site, `/archive/` snapshots, and legacy root pages. A whole-tree crawl found 1,766 local references and 53 broken references (32 root-level, 21 archived; 0 in `/crisp/`). The configured Pages source prevents the staged edition from being the only published tree. PR #24 is open on link repair/audit surfacing but currently conflicts with main; its exclusion of `archive/` from a checker would not itself unpublish those paths. Findings were posted on [PR #24](https://github.com/karagemop466-tech/Affil1/pull/24#issuecomment-7031517164) and [PR #19](https://github.com/karagemop466-tech/Affil1/pull/19#issuecomment-7031517473).
- **The product links are sponsored-marked but not tagged.** A scan of the 22 staged pages found 19 direct Amazon `/dp/<observed ASIN>` anchors and none with `tag=shopnow047c-20`. `rel="sponsored nofollow noopener"` does not establish a Special Link or attribution. The enrollment and click report remain unavailable, so keep status unresolved; do not claim any submitted short link is invalid. The current site disclosure refers to Amazon links as affiliate links even while link tracking is unconfirmed.
- **P-04’s latest observation changed.** PR #23 records a new fetch of `B0c8moW59` reaching observed listing `B0DHZTCNR5` (ThermoMaven); earlier attempts reached `/checkpoint/continue`. The product record keeps `intended_asin` null and records the earlier outcome, which is appropriate. It is an observed destination only, not intended identity or account-level verification. P-04 and P-05 are both thermometers, so any category copy should reflect both.
- **Analytics remains inactive and partly unwired.** The client is inert and declares the five requested event names, but it has no `guide_open` or `report_import` call sites. The current tracker emits `page_view`, `outbound_click`, and `search_query_referral`. The endpoint is not deployed; the inherited `analytics/endpoint.py` binds to loopback and accepts unvalidated event rows. Do not claim live measurement until the endpoint, schema/allowlist, privacy notice, retention, and authorized report-import path are ready.
- **The old validator is now broken.** On current `origin/main` `7b236c2`, `python3 tools/validate.py` raises `KeyError: 'supplied_path_code_length'`; current product records use `submitted_code` / `submitted_code_length` and `observed_asin`. This is a schema-drift regression not caught by the 22-page `tools/check.py` gate. A focused fix is being added on this branch because PR #24 does not modify `tools/validate.py`.

The official Amazon ASIN article [What is an ASIN?](https://sell.amazon.com/blog/fba-new-selection-program) was fetched in this review and describes ASINs as unique 10-character alphanumeric codes. It is suitable for format checking only; it cannot confirm intent for any submitted short link.

## Recommended integration sequence

1. Select and name one canonical publication; preserve alternate source/history without making duplicate live HTML pages.
2. Resolve the Pages source/workflow mismatch with available repository permissions, then verify the deployed public paths after the merge.
3. Keep supplied link intent blank until confirmed through the enrolled Associates workflow. Retain dated redirect observations separately and publish the unresolved status in the review queue.
4. Align analytics event names to the five requested events; do not enable collection until the self-hosted endpoint, privacy notice, retention, and reporting/import permissions are ready.
5. Make the build gate test disclosure placement, per-value source provenance, sponsored marking, link integrity, feed/sitemap coverage, and relevant policy requirements. Keep unsupported fields blank and visibly flagged.
6. Run a clean build and the complete gate, merge only after the site is not broken, then confirm the newest Actions/Pages run and fetch the live canonical site.

## Local verification performed

- On a fresh archive of `origin/main` `7b236c2`, `python3 tools/build.py && python3 tools/check.py`: **22 generated pages, 0 errors/warnings**; `python3 tools/stage.py _site`: **22 staged HTML pages**.
- `python3 tools/validate.py` on `7b236c2`: **fails** with `KeyError: 'supplied_path_code_length'` at line 176 after the P-04 schema update.
- Whole-tree local-reference/fragment crawl on `7b236c2`: **73 HTML pages, 1,766 local references, 53 broken** (32 root-level; 21 archived; 0 in `/crisp/`).
- Direct Amazon listing links in the 22 staged HTML pages: **19, zero with the supplied tracking ID**; all are sponsored-marked.
- `npm run verify` on the isolated PR #15 branch: **24 pages, 0 gate violations; 7/7 negative tests caught**.
- `python3 tools/check_site.py --build` on isolated PR #9 branch: **12 pages checked; build succeeded**.
- XML parsing on the reviewed branch's feeds/sitemaps: `sitemap.xml`, `feed.xml`, `rss.xml`, `crisp/sitemap.xml`, and `crisp/feed.xml` parsed successfully.
