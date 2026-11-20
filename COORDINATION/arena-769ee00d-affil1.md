# Session record — arena/769ee00d-affil1 · 2026-11-20

Long form of a second-session pass whose short version is on the board. Kept out of
`COORDINATION.md` because every parallel session appends to that file.

Branch `arena/769ee00d-affil1`, rebased onto `origin/main` (`feb3cfd`, PR #127) before
the work landed. Claim pushed first.

## What this pass was for

Read every published row again in a session that did not write it; publish the misses as
loudly as the matches; leave one site for search engines to index; take the audit voice
off the shop surfaces without touching the compliance gate behind it; help a reviewer
choose a path before anything is implemented; and record what is missing well enough
that the next session does not guess at it.

## Verified

* 5 of 5 official listings re-read; published ASIN, served title and category breadcrumb
  matched row for row. Evidence and raw strings:
  `_docs/VERIFICATION-arena-769ee00d-affil1.md`, machine-readable in
  `_src/data/recheck.json`, published at `verification/recheck.html`.
* Submitted short links re-followed: `B0f3GKalj` reached its recorded listing;
  `B04G1MEwY` and `B02NbDxp3` returned `https://www.amazon.com/`; `B00hJ57DV` and
  `B0c8moW59` failed to fetch. Three sessions now disagree about the same five slugs, so
  this is filed as route instability (FLG-055) and no stored field was edited. The site
  publishes the listing URL, not the short form.
* Re-read directly, this session: 16 CFR Part 233 (eCFR, up to date as of 11/18/2026) and
  USDA FSIS *Leftovers and Food Safety* → appended as SRC-18 and SRC-19 with verbatim
  quotes; OPM's 2026 federal-holiday table for the seasonal framing; `gh api
  repos/karagemop466-tech/Affil1/pages` → `build_type: legacy`, source branch `main`, path
  `/`, which is why a second served tree matters at all.

## Four defects found and repaired here

1. `FLG-052` — the deploy workflow's reproducibility step diffed build output against
   build output, after its own build step had already rewritten the tree: it could never
   catch a hand-edited or stale committed page, which on a legacy Pages site is the page
   readers get. Now diffs against `HEAD`, then rebuilds and diffs again to keep the
   determinism half. Found by testing reproducibility on a clean checkout.
2. Same finding's cause — `page_guides.py` emitted a guide's `sources` twice (an in-body
   aside and the article Sources block). Five guides shipped the duplicate and one had
   been trimmed by hand in the committed HTML. Fixed in the generator; pages regenerated;
   no hand edit preserved.
3. `FLG-053` / `Q-32` — `assets/img/meal-prep.jpg` (1408×768 photorealistic render) was
   served on a guide and the guides index while the image policy on the same site states
   one visual language and forbids photographic imagery. The register had documented the
   violation as a "generated editorial photograph". Replaced with a registered engraving
   (`assets/img/meal-prep-engraved` + `w560`/`w900`), the register row rewritten to
   describe what is served, and the render left in the tree unserved as the record.
4. `FLG-054` — `_tools/preview.py` imported the collector from `ROOT/'analytics'`, dead
   since the underscore rename, so the command `_analytics/README.md` documents raised
   ImportError and the five-event path could not be exercised at all. Corrected; the
   analytics test and both collector suites now run. (`_analytics/endpoint.py` had the
   same class of stale path and had been fixed by another session the same morning.)

Also corrected, small and cumulative: the verification page linked "The 22 pre-existing
flags" against a register of 51 and now counts from the data; the suggestions page
asserted three paths in prose and now counts; `EXECUTIVE_SUMMARY.md` and `README.md` had
drifted counts, synced once, with the standing fix filed as `S-52` rather than re-typed
again at the next merge.

## Shop-side changes

* Front-page trust band rewritten so it claims only what two sessions can support, and
  linked to the log (this was the overstatement in FLG-055).
* Reader nav keeps Shop / Categories / Guides / Compare / Find your fit; the
  second-read log joins the desk group in the footer, where every dashboard surface
  lives. Disclosure stays in the strip above `<main>` and again in the footer on all 50
  pages, enforced by the build.
* The `/edition/` preview is noindex with a pointer to the canonical root, so one site is
  offered to search — that half was landed independently by another session while this
  pass was in flight; the board records it once, not twice.
* `Q-33`: each product page still prints the submitted short link as code. It cannot be
  stood behind as a destination and it does not help a buyer decide, so the decision to
  move it into the registers only is filed for the owner rather than taken.

## Deliberately not done

* No new guides. This pass drafted a deal-week checklist, a reheat guide and a small-kitchen
  gift note; by the time they were ready, `main` carried `black-friday-air-fryer-checklist`,
  `reheating-thanksgiving-leftovers` and `air-fryer-gift-guide`. Three near-duplicates on a
  five-product shop is the slop pattern the brief asks to avoid, so the drafts were dropped
  and the existing guides were left as the canonical ones. The one durable piece — the
  former-price rule from 16 CFR 233.1 — is now SRC-18 for whoever edits that guide next.
* No image generated for a *product*. Every asset stays an illustration of a format, in the
  house style, registered in the same commit.
* `_src/data/products.json`, `links.json`, `paid_link_gate.py`, `cta.py`, `check.py`,
  `layout.py` beyond one footer line: cited, not edited. The gate that keeps a public
  observation from becoming an Associates tag is untouched and its tests pass.

## Requests to other owners (none blocking)

* `_platform/README.md` still documents `python3 platform/…`; the tree is `_platform/`.
  One-line fix for whoever touches that directory next.
* If the owner wants the `/edition/` preview off the host entirely rather than noindex'd,
  the move is `edition/` → `_edition/` plus `INTERNAL_SECTIONS` in `_tools/check.py` and
  `_tools/sweep_surfaces.py`, the `PUBLIC_DIRS` set, and the two links from `verification/`
  and `offers/`. Deliberately not done here.

## Gates on the merged tree, at commit time

`_tools/build.py` 50 pages, zero rebuild drift · `_tools/check.py` 0 errors 0 warnings ·
`_tools/validate.py` 3,285 checks 0 warnings · `_tools/check_local_links.py` 84 pages 0
broken · `_tools/check_image_register.py` 0 errors (2 pre-existing "registered but
unreferenced" warnings for `holiday-table` and `feature-holiday`) · `_tools` unit tests
OK · `_analytics` OK · `_measurement` OK · `_decision-support/validate.py` PASS ·
`_platform/verify_edition.py` 2,230 checks 0 errors.
