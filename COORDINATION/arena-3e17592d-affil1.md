# arena/3e17592d-affil1 — measurement machinery, the owner switch, one indexable site, three sourced guides

**Session start:** 2026-11-20. **Branch:** `arena/3e17592d-affil1`, cut from `2934ed0`.
**Status:** complete; PR opened against `main`.

## Claim

| Task | Status | Owner | Files |
|---|---|---|---|
| Repair `_analytics/endpoint.py`: `from build import GENERATED` resolved against a `tools/` directory that has been `_tools/` since the Pages hide, so the collector and its suite could not import while CI's `py_compile` kept the pipeline green | merged here | arena/3e17592d-affil1 | `_analytics/endpoint.py` |
| Make the CI steps that only appeared to test the machinery test it: `unittest discover -s platform` imported CPython's stdlib package (45 stdlib tests, 0 platform tests) | merged here | arena/3e17592d-affil1 | `.github/workflows/edition-verify.yml`, `.github/workflows/kitchen-check.yml` |
| Repair `arm_links.py` — the owner's arming switch read `_src/_data/product-intent.json` and died with `FileNotFoundError` on `--status` | merged here | arena/3e17592d-affil1 | `_tools/arm_links.py` |
| Remove a false reader-facing claim from every guide ("every one carries the site's Amazon tag") and from the annex disclosure | merged here | arena/3e17592d-affil1 | `_tools/page_guides.py`, `_platform/build_edition.py`, generated pages |
| Make `edition/` a non-competing annex and *enforce* it: per-page `noindex, follow`, a visible reader note, no second advertised sitemap, three new assertions in the edition verifier | merged here | arena/3e17592d-affil1 | `_platform/build_edition.py`, `_platform/verify_edition.py`, `_tools/build.py` (robots), generated `edition/**` |
| Three question-shaped guides sourced to USDA FSIS, three commissioned illustrations, guide sources rendered on the page, product↔guide cross-links, front-page feature derived from the record instead of `GUIDES[7]` | merged here | arena/3e17592d-affil1 | `_tools/content.py`, `_tools/page_guides.py`, `_tools/page_products.py`, `_tools/page_home.py`, `assets/img/guide-*`, `_src/data/images.json` |
| Register every finding and owner decision; add two gates that turn this session's own failures into machine checks | merged here | arena/3e17592d-affil1 | `_src/data/{flags,questions,suggestions,sources,events,images}.json`, `_tools/check_image_register.py` (new), `_tools/check_register_refs.py` (new), `_tools/check.py`, `_tools/cta.py`, `_tools/test_cta_gate.py` |
| Executive summary section for this pass | merged here | arena/3e17592d-affil1 | `EXECUTIVE_SUMMARY.md` |

## What this session deliberately did not do

- **No link was armed and no tag was published.** `_tools/arm_links.py` is repaired so the
  owner *can* arm a link; nothing here was run with `--i-am-the-owner`, and
  `_src/data/product-intent.json` is untouched (still five `null` approvals, three `null`
  confirmations). The refusal path was re-verified by running it: exit 3, no write.
- **No invented numbers.** Every figure in the new guides is quoted from a page fetched and
  read in this session (USDA FSIS *Food Thermometers* and *Leftovers and Food Safety*), and
  every product sentence is the seller's listing wording already transcribed in
  `_src/data/products.json`. No traffic, order, conversion or revenue claim anywhere.
- **No competing claim against `edition/`.** Another session had already recorded the
  noindex decision (FLG-030). This session did not relitigate it; it closed the gap that
  decision left (nothing enforced it, the annex advertised a second sitemap) and resolved the
  contradiction its fix created with a robots.txt `Disallow` line — see FLG-039.

## Two deviations from the claim, recorded because they changed the outcome

1. **The `data-affiliate-ref` decoupling was implemented, then reverted.** The intent was to
   let `outbound_product_click` fire on the untagged links the site actually publishes. While
   this branch was open, `main` gained `check_link_copy_state` in `_tools/check.py`, whose
   stated policy is the opposite: publishing that attribute beside an un-armed link means the
   counter would report unattributable clicks as evidence. That is a defensible policy and it
   belongs to the gate, so `layout.py` was restored to main's version, `cta.py` was brought
   into line with it, and the owner's choice — count untagged clicks as explicitly
   unattributed observations, or run no click counter until the account is armed — is now a
   row on the reviewable queue (S-30), with both paths' cost and risk stated.
2. **A one-page sample was widened to the whole surface, which found live breakage.** The new
   site-wide scan showed four published pages emitting the forbidden attribute through
   `cta.py` while the gate sampled only `products/p-01.html`. Fixed at the emitter, covered by
   a unit test, and the gate now fails on any page; negative-tested by re-injecting a value
   into `index.html`.

## Verification

All commands run in this sandbox on the merged tree (rebased onto `main` at `b77e66c`):

| Command | Result |
|---|---|
| `python3 _tools/build.py` | 44 pages, sitemap, feed, robots |
| `python3 _tools/check.py` | 41 pages checked, **0 errors, 0 warnings** |
| `python3 _tools/validate.py` | 2,351 checks, 0 warnings |
| `python3 _tools/check_local_links.py` | 75 pages, 0 broken |
| `python3 _tools/check_image_register.py` | 0 errors, 2 warnings (registered-but-unused) |
| `python3 _tools/check_register_refs.py` | 102 cross-citations + 7 guide sources, 0 errors |
| `python3 -m unittest discover -s _tools -p 'test_*.py'` | 11 tests OK |
| `python3 -m unittest discover -s _platform -p 'test_*.py'` | 6 tests OK (was: 45 stdlib tests, 0 real) |
| `python3 -m unittest discover -s _analytics -p 'test_*.py'` | 1 test OK (was: import error) |
| `python3 _decision-support/validate.py` | PASS, all six check families |
| `python3 _platform/verify_edition.py` | 2,047 checks, 0 errors (was 1,965) |
| `python3 _tools/sweep_surfaces.py --dry-run` | `would move: 0` |
| reproducibility | second build over a copy → no diff |
| `python3 _tools/arm_links.py --status` | prints state (was `FileNotFoundError`) |
| `python3 _tools/arm_links.py --link …` without `--i-am-the-owner` | `REFUSED`, exit 3, no write |

Negative tests, so the new gates are not decoration:

- strip `noindex` + the reader note from `edition/index.html` → `verify_edition.py` fails with 2 errors;
- delete an image register row for a published asset → `check_image_register.py` fails with 1 error;
- re-inject a `data-affiliate-ref` value into `index.html` → `check.py` fails with 1 error;
- point a food-safety row at a dangling `SRC-99` → `check_register_refs.py` fails with 2 errors;
- run the CI discovery guard against an empty directory → it rejects.

## Notes for the integration session

- `-X theirs` merges during this branch silently dropped three source rows (`SRC-18..20` had
  been renumbered by `main`), which left rows citing the wrong *documents* rather than
  missing ids. My rows are now `SRC-21..23` and the citations were re-pointed; the new
  reference gate exists because of it. **Renumbering a register on merge is not safe** — an id
  that resolves to the wrong document passes every check that only looks for dangling ids.
- `_measurement/collector.py` reads `src/data/product-intent.json` (no such path since the
  underscore rename), so its allowlist is permanently empty and it fails closed for the wrong
  reason; `_platform/collector.py` belongs to the annex. Both were left alone as other
  sessions' scopes and recorded in FLG-035 / Q-25 rather than rewritten here.
- `assets/js/events.js` and `assets/js/shortlist.js` are orphaned (loaded by no page) yet are
  the only two files `kitchen-check.yml` syntax-checks, while all 17+ pages load
  `analytics.js` + `site.js`. Left as-is — the files still parse and the collector's tests now
  run — but the mismatch is a one-line change for whoever owns `assets/js/`.
- `feed.xml` still emits a fixed pubDate, and `robots.txt` remains one path below the host
  root, so it is advisory at best (FLG-027, unchanged, owner-blocked).
