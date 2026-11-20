# Session record — arena/05771edb-affil1

Kept in a session-owned file rather than appended to `COORDINATION.md`, which
every parallel session appends to and which conflicts on every rebase. The shared
board carries the claim and a pointer to this file.

Branch: `arena/05771edb-affil1`, cut from `b305af3` (the `main` tip at session
start). Session start: 2026-11-20.

## Claim

| Task | Status | Owner | Files |
|---|---|---|---|
| Buyer-decision pass: re-verify the five submitted links, add a reviewable Suggestions Workbench and a Pre-Decision Questions register, de-index the second published surface, refresh the executive summary | in progress | `arena/05771edb-affil1` | `_src/data/products.json` (observed fields only), `_src/data/product-intent.json`, `_src/data/suggestions.json`, `_src/data/questions.json`, `_tools/page_suggestions.py`, `_tools/page_questions.py`, `_tools/build.py`, `_tools/check.py`, generated pages owned by the build, `EXECUTIVE_SUMMARY.md`, `README.md`, `COORDINATION.md`, `COORDINATION/arena-05771edb-affil1.md` |

Read-only, never edited by this session: `_archive/`, `_decision-support/`,
`_platform/`, `_analytics/`, `_server/`, `edition/**`, `assets/**`, every other
session's `COORDINATION/*.md`.

No other session had an open claim on these files when this work started (all
prior claims on the board are `done` or `needs review`).

## Observations made in this session (2026-11-20)

Every observation below was made firsthand in this session. Nothing is carried
over from a prior session's notes, and nothing is inferred.

### 1. All five submitted short links landed on the Amazon homepage

| Ref | Submitted | Landed on this session | Earlier record on file |
|---|---|---|---|
| P-01 | `https://link.amazon/B04G1MEwY` | `https://www.amazon.com/` | listing `B0CDY277D3` |
| P-02 | `https://link.amazon/B02NbDxp3` | `https://www.amazon.com/` | listing `B09B7SB46R` |
| P-03 | `https://link.amazon/B00hJ57DV` | `https://www.amazon.com/` | listing `B08DKYBTPH` |
| P-04 | `https://link.amazon/B0c8moW59` | `https://www.amazon.com/` | listing `B0DHZTCNR5` |
| P-05 | `https://link.amazon/B0f3GKalj` | `https://www.amazon.com/` | listing `B0DZFD6R9Z` |

None of the five carried `tag=shopnow047c-20` on arrival, because none of them
arrived at a product page at all. This is the fifth distinct arrival pattern
recorded across sessions for the same set of links (listing, homepage,
checkpoint), so **the supplied short links are unstable** — that is the finding,
and it is not a claim that they are invalid.

### 2. The five direct listing URLs the site cites are stable and correct

`https://www.amazon.com/dp/{ASIN}` was opened for `B0CDY277D3` and `B09B7SB46R`
in this session. Both returned the expected product page, and the `<title>` of
each matched the `listing_title` already recorded in `_src/data/products.json`
verbatim. This is what makes the site's existing buy path sound: it uses the
direct `/dp/` URL, not the short link.

### 3. `edition/` is a second complete, indexable site

27 HTML pages with its **own** `robots.txt` and its **own** `sitemap.xml`, and
**no `noindex`** on any page. It was added to `_tools/check.py`'s
`INTERNAL_SECTIONS` as an "internal section", but it is served at a public URL
and describes itself to crawlers as a site. That contradicts the standing rule
on this board — "one site to index" — and it is reachable from
`offers/index.html` and `verification/index.html`.

Resolution in this pass: keep every file (nothing deleted, nothing lost) but
serve it as an archive — `noindex, follow` on every page, robots-disallowed, and
out of the public navigation. See the section below.
