# Coordination — Affil1

Shared task board for parallel agent sessions. Source of truth: this file.
Session IDs are free-form; this session's ID is `session-arena-f10ea853`.

## Claims (task | status | owner | files touched | sources verified)

| # | Task | Status | Owner | Files touched | Sources verified |
|---|------|--------|-------|---------------|------------------|
| 1 | Repo review + COORDINATION.md setup | in progress | session-arena-f10ea853 | COORDINATION.md, README.md | n/a |
| 2 | Verify 5 submitted Amazon links against official Amazon sources | unclaimed | — | data/confirmations.json | Amazon product pages (link.amazon short links) |
| 3 | Build publication front page (index.html) + CSS/brand | unclaimed | — | index.html, assets/css/*.css | n/a |
| 4 | Build category subpages + product tables with per-row source links | unclaimed | — | categories/*.html | official sources per row |
| 5 | Build dashboard page (entries/findings table + analysis) | unclaimed | — | dashboard.html | official sources per row |
| 6 | Self-hosted analytics endpoint + outbound click counter (5 events) | unclaimed | — | assets/js/analytics.js, server/collect.js | n/a |
| 7 | Disclosure strip above the fold on every page + footer repeat | unclaimed | — | all pages, assets/js/disclosure.js | Amazon Associates Operating Agreement, FTC |
| 8 | Sponsored marking on all outbound product links | unclaimed | — | all product links | Amazon Associates program policies |
| 9 | Product-intent confirmation records (ASIN, listing URL, date, source; redirect separate) | unclaimed | — | data/confirmations.json | Amazon ASIN definition |
| 10| RSS feed + sitemap.xml + Search Console readiness | unclaimed | — | rss.xml, sitemap.xml | n/a |
| 11| Question-shaped buying guides (editorial hypotheses) | unclaimed | — | guides/*.html | n/a (working titles only) |
| 12| Suggestions section for decision review (no implementation without review) | unclaimed | — | suggestions.html | n/a |
| 13| Campaign ledger (empty, dated provenance trail) | unclaimed | — | data/campaign-ledger.json | n/a |
| 14| Compliance gate: disclosure + API policy checks in publishing workflow | unclaimed | — | PUBLISHING_WORKFLOW.md | Amazon Associates Operating Agreement, FTC |
| 15| Executive summary | unclaimed | — | EXECUTIVE_SUMMARY.md | n/a |
| 16| Flagged for Review page (irregularities + unverified items) | unclaimed | — | reviews/flagged.html | n/a |
| 17| Integration: merge branches, re-verify line by line, build check, broken-link check | unclaimed | — | all | official sources per row |
| 18| PR to main, merge, enable GitHub Pages, confirm deploy | unclaimed | — | main branch, repo settings | n/a |

## Rules
- Claim a task by writing your session ID and file scope, commit and push the claim immediately.
- Never start a task another session has claimed. Keep scopes non-overlapping.
- Work on feature branch `session-<id>/<task>`; edit only claimed files.
- Small, frequent commits; `git pull --rebase` before every push.
- On merge conflict: stop, resolve without discarding other session's work, log the handoff.
- A task older than 60 minutes with no commits may be taken over; note the handoff here.
- `needs review` = published on Flagged for Review page; does not block other work.
- Nothing is marked verified without checking against an official source; link that source.
- Shared outputs (table data, index, navigation) change only in the final integration session.

Session this message belongs to: `session-arena-f10ea853` on branch `arena/f10ea853-affil1` (base `cca8c2a`).
