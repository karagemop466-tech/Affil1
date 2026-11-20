# Session log — `arena/1623419c-affil1`

Branch: `arena/1623419c-affil1` · cut from `main` @ `6eb15b7` · 2026-11-20 UTC

## Claimed task

**One-site indexing & final integration/verification.** De-index every non-canonical
HTML surface so search engines index exactly one site; fix the `robots.txt`
`/archive/` → `/_archive/` path bug; re-verify the five submitted links line by
line against official Amazon pages; correct the stale README build paths; run the
full gate set and publish.

Claimed scope: `_tools/build.py` (ROBOTS constant), `_platform/build_edition.py`
(head template + edition robots), `_decision-support/*.html`, `_archive/**/*.html`
(noindex meta only), `README.md`, `COORDINATION.md`, `COORDINATION/arena-1623419c-affil1.md`.

## Findings (audit, before any edit)

| Surface | Pages | Indexable | Evidence |
|---|---|---|---|
| Root canonical (guides/products/compare/about/suggestions/questions/review/operations/brief/fit/decide + `index.html`/`404.html`) | 31 | yes (intended) | root `sitemap.xml`, `feed.xml` |
| `edition/` (Countertop Almanac) | 27 | **yes — competing edition** | 0 `noindex`; own `robots.txt` advertising own sitemap |
| `_decision-support/` (internal desk) | 7 | **yes** | 0 `noindex` |
| `_archive/` | 126 (69 without noindex) | **yes, and block misses** | root `robots.txt` says `Disallow: /archive/`; real dir is `_archive/` |

Root `robots.txt` `Disallow: /archive/` does not match the served path `/_archive/`,
so the archive was never actually crawler-blocked.

## Work done

(filled in as the session progresses)
