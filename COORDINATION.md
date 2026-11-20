# Coordination — Affil1

Shared task board for parallel agent sessions. Source of truth: this file.
Session IDs are free-form; this session's ID is `session-arena-f10ea853`.

## Claims (task | status | owner | files touched | sources verified)

| # | Task | Status | Owner | Files touched | Sources verified |
|---|------|--------|-------|---------------|------------------|
| 1 | Repo review + COORDINATION.md setup | done | session-arena-f10ea853 | COORDINATION.md, README.md | n/a |
| 2 | Verify 5 submitted Amazon links against official Amazon sources | done | session-arena-f10ea853 | data/confirmations.json | Amazon.com official site: https://link.amazon/B04G1MEwY -> https://www.amazon.com/dp/B0CDY277D3; https://link.amazon/B02NbDxp3 -> https://www.amazon.com/dp/B09B7SB46R; https://link.amazon/B00hJ57DV -> https://www.amazon.com/ (homepage); https://link.amazon/B0c8moW59 -> Amazon checkpoint; https://link.amazon/B0f3GKalj -> https://www.amazon.com/ (homepage). Fetched 2026-11-20. |
| 3 | Build publication front page (index.html) + CSS/brand | done | session-arena-f10ea853 | index.html, assets/css/main.css | n/a |
| 4 | Build category subpages + product tables with per-row source links | done | session-arena-f10ea853 | categories/air-fryers.html | official Amazon links per row |
| 5 | Build dashboard page (entries/findings table + analysis) | done | session-arena-f10ea853 | dashboard.html | official Amazon links per row |
| 6 | Self-hosted analytics endpoint + outbound click counter (5 events) | done | session-arena-f10ea853 | assets/js/analytics.js, server/collect.js | n/a |
| 7 | Disclosure strip above the fold on every page + footer repeat | done | session-arena-f10ea853 | assets/js/common.js, all pages | Amazon Associates Operating Agreement, FTC |
| 8 | Sponsored marking on all outbound product links | done | session-arena-f10ea853 | all product links | Amazon Associates program policies |
| 9 | Product-intent confirmation records (ASIN, listing URL, date, source; redirect separate) | done | session-arena-f10ea853 | data/confirmations.json | Amazon ASIN definition |
| 10| RSS feed + sitemap.xml + Search Console readiness | done | session-arena-f10ea853 | rss.xml, sitemap.xml, robots.txt | n/a |
| 11| Question-shaped buying guides (editorial hypotheses) | done | session-arena-f10ea853 | guides/*.html | n/a (working titles only) |
| 12| Suggestions section for decision review (no implementation without review) | done | session-arena-f10ea853 | suggestions.html | n/a |
| 13| Campaign ledger (empty, dated provenance trail) | done | session-arena-f10ea853 | data/campaign-ledger.json | n/a |
| 14| Compliance gate: disclosure + API policy checks in publishing workflow | done | session-arena-f10ea853 | PUBLISHING_WORKFLOW.md | Amazon Associates Operating Agreement, FTC |
| 15| Executive summary | done | session-arena-f10ea853 | EXECUTIVE_SUMMARY.md | n/a |
| 16| Flagged for Review page (irregularities + unverified items) | done | session-arena-f10ea853 | reviews/flagged.html | n/a |
| 17| Integration: merge branches, re-verify line by line, build check, broken-link check | done | session-arena-f10ea853 | all | official Amazon sources per row; internal links root-relative |
| 18| PR to main, merge, enable GitHub Pages, confirm deploy | in progress | session-arena-f10ea853 | main branch, repo settings | n/a |

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
