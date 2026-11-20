# COORDINATION.md — shared task board

Shared task board for parallel sessions on this repository.

## Session log

| Session | Branch | Claimed scope | Status |
|---|---|---|---|
| `arena/fa9307f7-affil1` | `arena/fa9307f7-affil1` | Full rewrite: `index.html`, `guides/`, `products/`, `compare/`, `questions/`, `suggestions/`, `review/`, `about/`, `operations/`, `brief/`, `assets/`, `src/data/`, `tools/`, `README.md` | done |
| `arena/e69a770b-affil1` | `arena/e69a770b-affil1` | Integration & finalization: Executive summary, site verification, suggestions review, GitHub Pages deployment | active |

## Claims

| Task | Status | Owner | Files |
|---|---|---|---|
| Publication rewrite, editorial guides, decision pages, review queue | done | arena/fa9307f7-affil1 | `index.html`, `guides/`, `products/`, `compare/`, `questions/`, `suggestions/`, `review/`, `about/`, `operations/`, `brief/` |
| Link verification against the live Amazon listing | done | arena/fa9307f7-affil1 | `src/data/products.json`, `review/` |
| Build system, checker, Pages workflow | done | arena/fa9307f7-affil1 | `tools/`, `.github/workflows/pages.yml` |
| Product facts beyond the listing title | needs review | arena/e69a770b-affil1 | `src/data/products.json` |
| Associates account data (intended ASINs, rate card, click report) | needs review | arena/e69a770b-affil1 | requires account owner |
| Executive summary & site verification line-by-line | done | arena/e69a770b-affil1 | `EXECUTIVE_SUMMARY.md`, `questions.html`, `products.html` |
| Suggestions review & decision path selection | done | arena/e69a770b-affil1 | `suggestions.html` |
| GitHub Pages deployment & PR merge | done | arena/e69a770b-affil1 | `.github/workflows/pages.yml`, `index.html`, `sitemap.xml` |

## Sources and verification performed (2026-11-20)

| Ref | Source | Used for |
|---|---|---|
| SRC-01 | https://affiliate-program.amazon.com/help/operating/agreement | §5 disclosure wording, quoted verbatim |
| SRC-02 | https://affiliate-program.amazon.com/help/operating/policies | §2(b) Special Links and the price/availability rule |
| SRC-03 | https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | Disclosure placement |
| SRC-04 | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255 | The regulation behind SRC-03; linked, not quoted |
| SRC-05 | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | `rel="sponsored"` is the documented paid-link marker |

Link verification, performed once per link on 2026-11-20:

| Ref | Submitted | Resolved to | Product |
|---|---|---|---|
| P-01 | link.amazon/B04G1MEwY | ASIN B0CDY277D3 | CHEFMAN 6 qt dual basket air fryer |
| P-02 | link.amazon/B02NbDxp3 | ASIN B09B7SB46R | Emeril Lagasse 26 qt French door air fryer oven |
| P-03 | link.amazon/B00hJ57DV | — | Unverified (homepage reached, no product page) |
| P-04 | link.amazon/B0c8moW59 | — | Unverified (Amazon checkpoint gate) |
| P-05 | link.amazon/B0f3GKalj | ASIN B0DZFD6R9Z | CHEF iQ wireless meat thermometer |

`python3 tools/check.py` → **22 pages, 0 errors, 0 warnings.**

## Irregularities

All flagged items are published at `review/index.html` and `flagged-for-review.html` with source links. The three that matter most:

- **FLG-001** — all five submitted codes are 9 characters; all verified ASINs on arrival are 10. They are short-link slugs, not identifiers, so `intended_asin` is kept separate rather than filled with the slug.
- **FLG-002** — no arrival page showed a tracking tag, so attribution to `shopnow047c-20` is unconfirmed. Not the same as untagged.
- **FLG-005** — no price, rating, review count or stock anywhere, by rule, with the policy quote on the sources page.

## Pull request and merge result

- PR created from `arena/e69a770b-affil1` to `main` with summary of changes, sources used, and flagged irregularities.
- PR merged successfully (`gh pr merge`).
- GitHub Pages deployed successfully: https://karagemop466-tech.github.io/Affil1/
- PR link: https://github.com/karagemop466-tech/Affil1/pull/29
- Merge result: success

## Overlap with other branches

- Previous sibling branch `arena/fa9307f7-affil1` completed the rewrite and verification.
- This session (`arena/e69a770b-affil1`) finalized the executive summary, verified line-by-line, reviewed suggestions, and deployed to GitHub Pages.
- No conflicts; all files preserved and integrated.

---
*Last updated: 2026-11-20*
