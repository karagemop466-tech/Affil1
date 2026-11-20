# COORDINATION — shared task board

Repo: `karagemop466-tech/Affil1` · Tracking ID: `shopnow047c-20`
Last updated: 2026-11-20 (UTC)

This file is the shared task board for any agent session working in this repo.
Read it before starting. Claim a task by adding your session ID and file scope,
then commit and push the claim immediately.

## Session log

| Session ID | Branch | Started | Scope |
|---|---|---|---|
| `arena-cadaafe7` | `arena/cadaafe7-affil1` | 2026-11-20 | Whole-repo build (this session claimed all tasks below at once — no other sessions active at claim time) |

## Why one session claimed everything

At claim time (2026-11-20) the repository contained only `README.md` and a
single commit (`cca8c2a`). No other branch, worktree, or claim existed. With no
competing claim, splitting the build across sessions would have created
merge-conflict risk on shared outputs (navigation, table data, sitemap) for no
benefit. This session therefore claimed every task below and logged the
verification for each. **If a second session appears, it must claim a new row
before editing anything.**

## Task board

| ID | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T01 | Source register: official-source verification of all 5 submitted links | done | `arena-cadaafe7` | `data/sources.json`, `dashboard/source-register.html` (generated) |
| T02 | Product-intent confirmation record (intended vs. observed, kept separate) | done | `arena-cadaafe7` | `data/product-intent.json`, `dashboard/product-intent.html` |
| T03 | Policy + disclosure compliance surface | done | `arena-cadaafe7` | `data/policies.json`, `dashboard/compliance.html` |
| T04 | Decision-readiness question register | done | `arena-cadaafe7` | `data/questions.json`, `dashboard/questions.html` |
| T05 | Suggestion register with review controls | done | `arena-cadaafe7` | `data/suggestions.json`, `dashboard/suggestions.html` |
| T06 | Editorial guides (4 question-shaped pieces) + guide index | done | `arena-cadaafe7` | `content/guides.mjs`, `guides/*` |
| T07 | Shop surfaces (index + 4 product pages + 1 held page) | done | `arena-cadaafe7` | `content/products.mjs`, `shop/*` |
| T08 | Front page rebuilt as publication front page | done | `arena-cadaafe7` | `index.html` (generated) |
| T09 | Executive summary | done | `arena-cadaafe7` | `summary.html` |
| T10 | Campaign ledger (empty, well-defined) | done | `arena-cadaafe7` | `data/campaign-ledger.json`, `dashboard/campaign-ledger.html` |
| T11 | Privacy-preserving outbound-click counter + self-hosted endpoint contract | needs review | `arena-cadaafe7` | `assets/js/analytics.js`, `data/events.json`, `dashboard/measurement.html` |
| T12 | Findability: single canonical site, sitemap, feed, robots, canonicals | done | `arena-cadaafe7` | `sitemap.xml`, `feed.xml`, `robots.txt`, `<head>` |
| T13 | Flagged-for-review page | done | `arena-cadaafe7` | `dashboard/flagged.html` |
| T14 | Build + link check + Pages deploy | done | `arena-cadaafe7` | `scripts/build.mjs`, `scripts/check.mjs`, `.github/workflows/` |

**Status key:** `unclaimed` · `in progress` · `done` · `needs review`.
`needs review` means the item is published on the *Flagged for Review* page and
does not block anything.

## Hijack rule

If a session's claim is more than 60 minutes old with no commit, any other
session may take the task over. Record the handoff in the Session log above and
note which files you touched.

## Shared outputs

Shared outputs — `index.html`, the navigation block, `data/*.json` table data,
`sitemap.xml`, and `feed.xml` — are generated from `scripts/build.mjs`. Do not
hand-edit a generated file: edit the generator or the data it reads, then run
`npm run build`. That keeps two sessions from silently overwriting each other.
