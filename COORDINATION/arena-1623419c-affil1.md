# Session log — `arena/1623419c-affil1`

Branch: `arena/1623419c-affil1` · cut from `main` @ `6eb15b7` · 2026-11-20 UTC

## Claimed task

**One-site indexing & final integration/verification.** De-index every non-canonical
HTML surface so search engines index exactly one site; fix the `robots.txt`
`/archive/` → `/_archive/` path bug; re-verify the five submitted links line by
line against official Amazon pages; correct the stale README build paths; run the
full gate set and publish.

## Findings (audit, before any edit)

| Surface | Pages | Indexable | Evidence |
|---|---|---|---|
| Root canonical (guides/products/compare/about/suggestions/questions/review/operations/brief/fit/decide + `index.html`/`404.html`) | 31 | yes (intended) | root `sitemap.xml`, `feed.xml` |
| `edition/` (Countertop Almanac) | 27 | **yes — competing edition** | 0 `noindex`; own `robots.txt` advertising own sitemap |
| `_decision-support/` (internal desk) | 7 | **yes** | 0 `noindex` |
| `_archive/` | 126 (69 without noindex) | **yes, and block misses** | root `robots.txt` says `Disallow: /archive/`; real dir is `_archive/` |

## Work done

1. **Root `robots.txt`** (`_tools/build.py` `ROBOTS`): fixed the non-matching
   `Disallow: /archive/` → `Disallow: /_archive/` and added
   `Disallow: /edition/` and `Disallow: /_decision-support/`. Comment updated.
2. **`edition/` de-indexed** (`_platform/build_edition.py`): added
   `<meta name="robots" content="noindex, follow">` to the shared head template
   (all 27 pages) and changed `edition/robots.txt` to `Disallow: /` (no sitemap
   advertisement). `verify_edition.py` still passes (1965 checks).
3. **`_decision-support/` and `_archive/` de-indexed**: injected
   `<meta name="robots" content="noindex,follow">` (matching the form already
   used in the archived pages) into the 7 desk pages and the 69 archive pages
   that lacked it. All 133 target files now carry noindex.
4. **README path correction**: `tools/` → `_tools/`, `src/data/` → `_src/data/`,
   `archive/` → `_archive/`, `docs/` → `_docs/` so the documented build commands
   match the actual tree.
5. **Line-by-line re-verification of the five submitted links** against the
   official Amazon listing pages (fetched 2026-11-20). Titles match
   `_src/data/products.json` exactly; no drift. See table below.

## Verification of the five submitted links (official Amazon pages, 2026-11-20)

| Entry | Submitted | Reached ASIN | Official listing title observed | Match |
|---|---|---|---|---|
| P-01 | link.amazon/B04G1MEwY | B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven … 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets | ✅ |
| P-02 | link.amazon/B02NbDxp3 | B09B7SB46R | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven … 24 One-Touch Preset Options, Six Cooking Accessories | ✅ |
| P-03 | link.amazon/B00hJ57DV | B08DKYBTPH | Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 … 450°F Hi-Fry … XL Nonstick Dishwasher-Safe Basket | ✅ |
| P-04 | link.amazon/B0c8moW59 | B0DHZTCNR5 | ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified … IP67 Waterproof | ✅ |
| P-05 | link.amazon/B0f3GKalj | B0DZFD6R9Z | CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| 1000°F Heat Safe \| … Air Fryer \| Gen3 | ✅ |

Every arrival carried Amazon's `plpRedirect=mhFallback` fallback marker (consistent
with FLG-018). **No `tag` parameter was observed on any arrival** (FLG-002, unchanged);
`intended_asin` remains `null` and is kept strictly separate from `observed_asin`.
The supplied `link.amazon/*` short links are **not** declared invalid (FLG-003).

## Gates (all green on this branch)

- `_tools/build.py` → 34 generated pages; reproducible (zero drift across two runs).
- `_platform/build_edition.py` → 27 pages; reproducible (zero drift).
- `_tools/check.py` → 0 errors, 0 warnings.
- `_tools/validate.py` → 1607 checks, 0 warnings.
- `_tools/check_local_links.py` → 65 pages, 0 broken relative references.
- `_tools/check_deploy_paths.py` (MOUNT=/Affil1) → 1645 internal references resolve.
- `_decision-support/validate.py` → PASS (six check families).
- `_platform/verify_edition.py` → 1965 line-by-line checks, 0 errors.
- `_tools/sweep_surfaces.py --dry-run` → would move 0 files.
- `_tools/check_js.py` → both client scripts parse cleanly; no third-party load.
- `test_paid_link_gate` (6) + `_platform` tests (6) → all pass.

## Irregularities / open items (not blocked)

- **FLG-002 (unchanged):** no resolved URL showed `tag=shopnow047c-20`; attribution
  unconfirmed. Requires the owner's enrolled Associates workflow.
- **FLG-003 (unchanged):** the exact compliance status of the supplied
  `link.amazon/*` short links is unresolved; not declared invalid.
- **FLG-016 (unchanged):** the P-04/P-05 observed mapping was disputed across
  sessions; neither is presented as the intended product.
- **Owner request (unchanged):** set Pages source to `workflow`
  (`PUT /repos/karagemop466-tech/Affil1/pages` with `build_type: workflow`) so the
  30-page `_site` is served instead of the repo root. This is the durable fix for
  "one published surface"; this session applied the file-level equivalent
  (noindex + robots) that works without admin scope.
