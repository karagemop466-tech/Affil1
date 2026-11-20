# COORDINATION.md — shared task board

Shared task board for parallel sessions on this repository. Claim a task by writing
your session ID and file scope here, commit and push that claim, and never start a
task another session has claimed.

## Claims

| Task | Status | Owner (session) | Files | Since |
|---|---|---|---|---|
| **Final integration pass:** one canonical site, product-led front page, guide clusters, decision board, sources page, tagged Special Links, legacy quarantine, executive summary | in progress | `arena/2ed69be3-affil1` | `index.html`, `guides/`, `products/`, `compare/`, `questions/`, `suggestions/`, `review/`, `about/`, `sources/`, `operations/`, `brief/`, `src/data/`, `tools/`, `assets/`, `README.md`, `EXECUTIVE_SUMMARY.md`, `COORDINATION.md`, `PUBLISHING_WORKFLOW.md` | 2026-11-20 |
| Publication rewrite, editorial guides, decision pages, review queue | done | `arena/fa9307f7-affil1` | `index.html`, `guides/`, `products/`, `compare/`, `questions/`, `suggestions/`, `review/`, `about/`, `operations/`, `brief/` | merged in `54b2b45` |
| Link verification against the live Amazon listing | done | `arena/fa9307f7-affil1` | `src/data/products.json`, `review/` | merged in `54b2b45` |
| Build system, checker, Pages workflow | done | `arena/fa9307f7-affil1` | `tools/`, `.github/workflows/pages.yml` | merged in `54b2b45` |
| Intended ASINs, rate card, click report | needs review | — | requires account owner | — |
| Named author and biography | needs review | — | requires account owner | — |

`needs review` means the item is published on the Flagged for Review page
(`review/index.html`) and does not block anything.

### Files this session does not touch

`crisp/`, `reviews/`, `categories/`, `archive/`, `docs/`, `data/`, `js/`, `css/`,
`server/`, `analytics/`, and the root-level `*.html` pages of the earlier parallel
edition (`products.html`, `questions.html`, `suggestions.html`, `guides.html`,
`dashboard.html`, `disclosure.html`, `executive-summary.html`,
`flagged-for-review.html`, `privacy.html`, `categories.html`).

Those belong to other sessions. This session adds `noindex` metadata and a banner to
them via `tools/quarantine_legacy.py` and changes nothing else in them. No file was
deleted, renamed or moved. `tools/build.py` writes only its own `GENERATED` set and
cannot overwrite them.

---

## Sources and verification performed

Every entry below was requested and read in this session on **2026-11-20**. The quote
is the source's own wording, transcribed; the URL is the page it came from.

| Ref | Source (official) | Used for | Status |
|---|---|---|---|
| SRC-01 | [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | §5 disclosure sentence | read directly |
| SRC-02 | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | §2(a) Special Links; §2(b) tag-as-parameter and the price/availability rule | read directly |
| SRC-03 | [FTC Endorsement Guides FAQ](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) | Disclosure placement ("easily catches consumers' attention") | read directly |
| SRC-04 | [16 CFR Part 255](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255) | The regulation behind SRC-03 | linked, not quoted |
| SRC-05 | [Google: qualify outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) | `rel="sponsored"` as the paid-link marker | read directly |

Product verification, each link requested once per attempt on 2026-11-20:

| Ref | Submitted | Final `/dp/` address | Listing title (start) | Attempts |
|---|---|---|---|---|
| P-01 | link.amazon/B04G1MEwY | [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) | CHEFMAN 6 Quart Dual Basket Air Fryer Oven… | 1 |
| P-02 | link.amazon/B02NbDxp3 | [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R) | Emeril Lagasse 26QT French Door Multi-Function… | 1 |
| P-03 | link.amazon/B00hJ57DV | [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH) | Chefman Air Fryer 8 Qt \| TurboFry 4-in-1… | 1 |
| P-04 | link.amazon/B0c8moW59 | [B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5) | ThermoMaven 1 Sec Professional Digital Meat Thermometer… | 3 |
| P-05 | link.amazon/B0f3GKalj | [B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z) | CHEF iQ Sense \| Smart Wireless Meat Thermometer… | 1 |

Also verified in this session: a tagged URL of the form
`https://www.amazon.com/dp/B0CDY277D3?tag=shopnow047c-20` resolves to the same listing.

`python3 tools/build.py` → 24 pages. `python3 tools/check.py` → **24 pages, 0 errors,
0 warnings.**

---

## Irregularities found in this pass

All are published at `review/index.html` with source links. The ones that matter:

- **FLG-016 (high, fixed).** The previous build linked to bare `/dp/` addresses with no
  `?tag=` parameter. Policy §2(b) requires the Associates ID as a URL parameter, so those
  links were not Special Links as the policy defines one. Every product link now carries
  `?tag=shopnow047c-20`.
- **FLG-004 (was high, now low, corrected).** P-04 previously "could not be resolved".
  On the third request it resolved to B0DHZTCNR5. The stale copy was corrected and the
  history kept.
- **FLG-002 (high, open).** None of the five final URLs contained a tag parameter. That is
  an observation about the visible URL, not proof the short links are untagged. Attribution
  stays unconfirmed until one click is seen in the Associates report.
- **FLG-003 (medium, open).** The compliance status of `link.amazon` short links is
  unresolved. **This session does not claim they are invalid.**
- **FLG-018 (medium).** A second, superseded edition is served from the same origin. It is
  now `noindex` and absent from the sitemap; it was not deleted.

---

## Session log

| Session | Branch | Status | What it did |
|---|---|---|---|
| `arena/fa9307f7-affil1` | `arena/fa9307f7-affil1` | done | Built the first publication edition; merged as `54b2b45` (PR #22). |
| `arena/2ed69be3-affil1` | `arena/2ed69be3-affil1` | in progress | Final integration: tagging fix, P-04 correction, product-led front page, clusters, sources page, decision board, legacy quarantine, executive summary. |

### Overlap with earlier branches

Two sibling branches (#6 `arena/55d40788-affil1`, #7 `arena/96012762-affil1`) worked the
same brief. They were not merged: their designs conflict structurally, and one writes
root-absolute links that 404 on a project Pages path. PR #7 independently opened the same
five links and reached the same four ASINs recorded at the time; that agreement is noted on
the review page as corroboration, not copied as evidence.

---

## Pull request and merge

- Integration branch: `arena/2ed69be3-affil1`
- Pull request: recorded below once opened.
- Merge result: recorded below once merged.
- GitHub Pages: https://karagemop466-tech.github.io/Affil1/
