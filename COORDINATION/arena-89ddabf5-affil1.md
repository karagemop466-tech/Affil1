# Session record — arena/89ddabf5-affil1

Kept in a session-owned file rather than appended to `COORDINATION.md`, which
every parallel session appends to and which conflicts on every rebase. The shared
board carries the claim and a pointer to this file.

---

## First pass (base `0691fa7`) — superseded

Claimed and completed a verification and consistency pass over `src/data/**`,
`data/**`, `tools/page_*.py`, `assets/js/analytics.js`, `EXECUTIVE_SUMMARY.md`
and `tools/validate.py`.

`origin/main` then advanced 94 commits through PRs #37, #41, #44, #45, #49, #50,
#51, #58, #59, #63, #64, #66, #67, #70 and #75, rewriting the pipeline in a final
integration pass. A rebase was attempted; the conflict set was ~27 files. **This
session dropped its own versions rather than forcing its pass into a
consolidated pipeline.** What happened to each item:

| First-pass item | State on `main` | Decision |
| --- | --- | --- |
| Re-verify the five listings | Done; five of five resolved, `intended_asin` null | Dropped as duplicate |
| `data/confirmations.json` v2 | Supplied by `arena/ac649871`, richer than this pass's | Dropped main's copy |
| Stale "four of five" copy | Gone | Dropped |
| One definition of the five events | `src/data/events.json` is the single list; `check.py` compares the client against it | Dropped main's client |
| Reader capture artefact | Answered as an open question: an RSS feed and a prominent link, no form | **Did not override.** Shipping a form would contradict the published decision record. |
| Publishing cadence | Answered as S-12 and Q-22, plus a weekly editorial research workflow | Dropped as duplicate |
| `tools/validate.py` crash | Fixed independently in `8ef437f` (PR #76) and `7a04031` | Dropped as duplicate |

## Second pass (base `3193be2`) — superseded

Repointed `validate.py` at `build.GENERATED` and fixed three assertions that
could not fail (a disclosure substring test that matched the `<title>` text, a
warn-only price rule, and acceptance of root-absolute hrefs). `main` independently
landed the same fixes. Dropped rather than duplicated.

## Third claim — harden the gate's soft rules (base `b5da998`)

Scope: `tools/validate.py`, `COORDINATION.md`, this file.

`validate.py` runs again, but two rules cannot stop a release:

1. a price figure only warns, although Program Policies §2(b) makes a published
   price unlawful here;
2. an unmarked affiliate link only warns, and only if it lacks `nofollow` — and
   only when the element's class contains `btn`, so a plain text link to a
   listing with no `sponsored` token passed.

Both are now errors. `noopener` warns. Result: 1545 checks, 0 errors,
0 warnings; each rule verified by deliberately breaking it.

## Verification performed (2026-11-20)

All five Amazon listings were opened again, one request each, and the returned
document title and category breadcrumb transcribed. They match
`src/data/products.json` for all five, including P-04 → `B0DHZTCNR5` (a fourth
independent observation that this link resolves).

| Source | Read as |
| --- | --- |
| https://affiliate-program.amazon.com/help/operating/agreement | Updated October 15, 2025. §1 Special Links; §5 the disclosure sentence. |
| https://affiliate-program.amazon.com/help/operating/policies | Updated April 14, 2026. §2(a)/(b) tag-as-URL-parameter; price/availability rule. |
| https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | "clearly and conspicuously"; disclosure near the recommendation. |
| https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255 | 16 CFR 255.5, current through 2026-11-18. |
| https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | Last updated 2025-12-10 UTC; `rel="sponsored"` marks paid links. |
| https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart | Updated April 14, 2025. |
| https://sell.amazon.com/blog/what-is-an-asin | "a unique 10-character alphanumeric code". |

Compliance sweep over every served HTML page with `archive/` excluded:
disclosure sentence present, disclosure strip before `<main>`, exactly one
`<h1>`, every affiliate link carrying `sponsored`, no broken relative reference,
no root-absolute reference, and no price, rating, review-count, stock,
best-seller or test-claim phrase. Zero violations.

No resolved URL carried `shopnow047c-20`; attribution remains unconfirmed
(FLG-002). No submitted short link is described as invalid (FLG-003).

## Irregularities

- **X-16** — `tools/sweep_surfaces.py` reads `build.GUIDES.keys()`, but
  `build.GUIDES` is a list of dicts. It therefore always falls back to
  "keeping guides by directory", allows only 16 paths, and would report 21
  legitimate generated pages as a second surface. The CI step that runs it
  compares against the string `^would move: 0 `, so the check fails on every run
  rather than silently passing. Outside this claim's scope; recorded for the
  integration owner.
- **X-17** — `check_deploy_paths.py` tries to fetch `../<page>` over HTTP from
  the sandbox and reports `Connection refused` for every page. It is a local
  diagnostic, not a published defect.
