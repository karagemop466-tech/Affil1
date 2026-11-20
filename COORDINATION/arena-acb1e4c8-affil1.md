# arena/acb1e4c8-affil1 — product page buying path, buyer-voice rewrite, decision registry

**Session start:** 2026-11-20. **Branch:** `arena/acb1e4c8-affil1`, cut from `2934ed0`.
**Status:** in progress.

## Claim

| Task | Status | Owner | Files |
|---|---|---|---|
| Give every product a defensible buying decision record: replace empty Price/Rating columns with listing-verified values, add a labelled official-listing CTA that stays inside the paid-link gate, and add a reviewable decision registry | in progress | arena/acb1e4c8-affil1 | `_src/data/products.json`, `_src/data/decisions-registry.json` (new), `_tools/layout.py`, `_tools/page_products.py`, `_tools/page_compare.py`, `_tools/page_home.py`, `_tools/page_decisions.py` (new), `_tools/build.py`, `_tools/check.py`, `assets/css/site.css`, `sitemap.xml`, `COORDINATION.md`, this file |

**Duplicate-work check.** PRs #47 ("Storefront rebuild: products-first front page"), #62 ("Wire 3
guides, lead with all 5 products, ship tagged Special Links") and #93 ("Reader-facing release")
each scope the same files (`_tools/page_home.py`, `_tools/page_products.py`, `_tools/layout.py`).
Those are **open, unmerged** proposals, not merged work, so this branch does not duplicate merged
work — but it does overlap three open proposals. Recorded rather than resolved unilaterally: if
one of them merges first, this session's generator edits will conflict, and the conflict must be
resolved in favour of **the paid-link gate**, which every competing proposal relaxes.

## What this session will not do

- It will not put the Associates tag on a link that the account has not confirmed. The gate in
  `_tools/paid_link_gate.py` stays closed. Tagging a URL built from a redirect observation is
  exactly what Amazon's Program Policies §2(a)–(b) forbid, and `test_paid_link_gate.py` asserts
  the register stays empty until an account-generated Special Link exists.
- It will not display price, rating, review count or stock. Program Policies §2(b) permits price
  display only when Amazon serves the link carrying that data, or via Creators API / PA API; the
  site has neither. So the columns become **honest, listing-verified specifics** instead of
  permanently blank ones, and the price question moves to the registry.
- It will not claim a test, a ranking or a best-seller status.
