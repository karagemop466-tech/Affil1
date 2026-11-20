# COORDINATION.md — shared task board

Shared task board for parallel sessions on this repository.

## Session log

| Session | Branch | Claimed scope | Status |
|---|---|---|---|
| `arena/fa9307f7-affil1` | `arena/fa9307f7-affil1` | Full rewrite: site root, guides, register, review queue, build system | done |
| `arena/47a393a2-affil1` | `arena/47a393a2-affil1` | Re-verification pass, tagged Special Links, `questions/decisions.html`, `review/verification.html`, suggestions rebuild, thermometer guide, `src/data/`, `tools/` | done — merged in PR #23 |

## Claims

| Task | Status | Owner | Files |
|---|---|---|---|
| Session claim: re-verify every supplied link and every policy source, fix the tracking defect, build the decision dossier | done | `arena/47a393a2-affil1` | `src/data/*.json`, `tools/*.py`, `questions/`, `review/`, `suggestions/`, `guides/`, `index.html`, `README.md`, `EXECUTIVE_SUMMARY.md`, `PUBLISHING_WORKFLOW.md` |
| Product facts beyond the listing title (dimensions, wattage, warranty) | needs review | — | `src/data/products.json` |
| Associates account data (intended ASINs, account status, rate card, click report) | needs review | — | requires account owner; see `questions/decisions.html` |
| Search Console verification and sitemap submission | unclaimed | — | requires owner's Google account |
| Analytics endpoint decision | unclaimed | — | `assets/js/analytics.js` is inert |

No other session had an open claim on these files when this work started. PR #19
(`arena/e56bd6f7-affil1`, an audit log in `COORDINATION.md` only) was open and
untouched; this file merges rather than overwrites its content.

## What this session changed, and why

Two things were defects rather than proposals, so they were fixed rather than
queued:

1. **The buy links were not Special Links.** All five arrival URLs were bare
   `/dp/<ASIN>` addresses with no tag, and the site was offering them as click
   targets. Program Policies §2(b) requires the Associates ID as a URL parameter,
   and Amazon's application-review page lists untagged links among its rejection
   reasons. The build now emits `/dp/<ASIN>/?tag=shopnow047c-20`, keeps the
   submitted code as history, and fails if an untagged retail link appears.
2. **P-04 resolved.** Three failures were recorded in the previous session; in this
   one it resolved on both attempts to `B0DHZTCNR5`, a ThermoMaven instant-read
   thermometer. The catalogue is therefore three air fryers and two thermometers,
   and every page that said otherwise was corrected.

Three further rows from the suggestion queue were implemented because they are
structural rather than editorial: the thermometer cluster guide, the noindex on the
parallel edition, and the shortlist-first front page. They stay in the queue marked
`implemented` so the record shows what changed.

## Sources and verification performed

Every source below was requested and its wording read **in this session** on
2026-11-20. Quotes are copied, not paraphrased, and are published with the date
read at `about/index.html#sources`; the pass itself is logged at
`review/verification.html`.

| Ref | Source | Used for |
|---|---|---|
| SRC-01 | https://affiliate-program.amazon.com/help/operating/agreement | §5 disclosure sentence, quoted verbatim |
| SRC-02 | https://affiliate-program.amazon.com/help/operating/policies | §2(a)(b): tag as a URL parameter; price/availability rule (page dated 2026-04-14) |
| SRC-03 | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255 | 16 CFR 255.0(f) definition of clear and conspicuous |
| SRC-04 | https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | Placement guidance; linked, not quoted |
| SRC-05 | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | `rel="sponsored"` for paid links (page updated 2025-12-10) |
| SRC-06 | https://sell.amazon.com/blog/what-is-an-asin | ASIN is a 10-character code, found after `/dp/` — closes FLG-011 |
| SRC-07 | https://affiliate-program.amazon.com/help/node/topic/G8TW5AE9XL2VX9VM | 3 sales / 180 days, 10-post originality bar, untagged links as a rejection reason |

Link verification, performed in this session, twice for P-04:

| Ref | Submitted | Resolved to | Product | Tag in final URL |
|---|---|---|---|---|
| P-01 | link.amazon/B04G1MEwY | ASIN B0CDY277D3 | CHEFMAN 6 qt dual basket | no |
| P-02 | link.amazon/B02NbDxp3 | ASIN B09B7SB46R | Emeril Lagasse 26 qt French-door oven | no |
| P-03 | link.amazon/B00hJ57DV | ASIN B08DKYBTPH | Chefman 8 qt TurboFry | no |
| P-04 | link.amazon/B0c8moW59 | ASIN B0DHZTCNR5 | ThermoMaven instant-read thermometer | no |
| P-05 | link.amazon/B0f3GKalj | ASIN B0DZFD6R9Z | CHEF iQ Sense wireless thermometer | no |

`python3 tools/build.py` → **25 pages**; `python3 tools/check.py` → **0 errors, 0 warnings**.

## Irregularities

All 17 are published at `review/index.html` with source links. The ones that matter
most:

- **FLG-002 (high)** — the buy links carried no tag until this build; fixed in the
  build, still unconfirmed until one click appears in the Associates report.
- **FLG-001** — all five submitted codes are nine characters; every ASIN on arrival
  is ten. They are short-link slugs, not identifiers, so `intended_asin` stays null.
- **FLG-004** — P-04 failed three times, then resolved twice. Both outcomes kept.
- **FLG-011** — closed: Amazon's own ASIN definition was found on sell.amazon.com.
- **FLG-017** — the parallel edition is still served, now `noindex, follow`.

## Merge log

| PR | Branch | Result |
|---|---|---|
| #22 | `arena/fa9307f7-affil1` | merged before this session; the root build became canonical |
| #23 | `arena/47a393a2-affil1` | this session — see the PR body for the change list, sources and flags |

GitHub Pages: https://karagemop466-tech.github.io/Affil1/

Nothing was deleted from another session's work. Their pages (`crisp/`,
`guides.html`, `products.html`, `dashboard.html`, `flagged-for-review.html`,
`reviews/`, `categories/`, `archive/`, `data/`, `js/`, `css/`, `server/`,
`analytics/`, `docs/`) are all still present and still served, now with
`noindex, follow` so that search engines index one edition. `tools/build.py` still
writes only the files in its own `GENERATED` set, and `tools/legacy.py` only adds a
meta tag — it never removes a page.

Handoff note: if a session finds a page here that contradicts `src/data/`, the data
is canonical and the page is the bug. Rebuild rather than hand-edit; CI diffs the
tree and fails on a hand-edited output.
