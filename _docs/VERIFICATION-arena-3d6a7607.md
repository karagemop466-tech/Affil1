# Verification record — arena/3d6a7607-affil1 · 2026-11-20 UTC

Line-by-line record of what this session fetched, what it changed, what it
checked, and what it refused to infer. Companion to the board entry in
`COORDINATION.md`.

## Scope actually touched

| File | Change |
|---|---|
| `_tools/content.py` | One guide appended (`GUIDES.append`): `reheating-thanksgiving-leftovers`. No existing guide edited. |
| `assets/img/leftovers.jpg`, `-w560.jpg`, `-w900.jpg` | New illustration + resized variants (base regenerated at 1200px/quality 82 to pass the asset-weight check). |
| `_src/data/images.json` | One register entry appended for `leftovers`. |
| `_tools/page_guides.py` | Two lines: render the `sources` field that guides already carried but the template ignored; correct the side-card sentence "every one carries the site's Amazon tag" (false — see PR #106's flag on untagged cart CTAs) to "point to the official Amazon listing". |
| `_tools/build.py` | `ROBOTS`: `Disallow: /archive/` → `Disallow: /_archive/` (path has not existed since the underscore rename). |
| `_src/data/flags.json` | FLG-029 (high) and FLG-030 (low) appended; FLG-029 wording tightened to separate observation from mechanism. |
| Generated HTML, `sitemap.xml`, `feed.xml`, `robots.txt` | Via `_tools/build.py` only. |
| `README.md`, `EXECUTIVE_SUMMARY.md` | Counts only: 11 guides, 35 pages, 30 flags. |
| `_docs/VERIFICATION-arena-3d6a7607.md`, `COORDINATION.md` | This record and the board entry. |

Not touched: `_src/data/products.json`, `product-intent.json`, `offers`/`now`
surfaces (PR #104 scope), the untagged-cart flag (PR #106 scope), `arm_links.py`,
`_decision-support/`, `_platform/`, any other session's guide.

## Official sources fetched this session (2026-11-20)

Every figure published in the new guide was transcribed from one of these two
fetches. Nothing was inferred, and no other page was quoted.

| Source | Status on fetch | Used for |
|---|---|---|
| [USDA FSIS · Leftovers and Food Safety](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety) (page states Last Updated Jul 31, 2020) | Reached in full, both chunks | 40–140°F danger zone; refrigerate within 2 hours (1 hour over 90°F); shallow containers / slice turkey cooling advice; fridge 3–4 days; freezer 3–4 months quality note; 165°F reheat rule; rolling boil for sauces/soups/gravies; cover-to-reheat; microwave cold-spot caution; reheat-from-frozen and refreeze-after-165°F answers |
| [FoodSafety.gov · Cold Food Storage Chart](https://www.foodsafety.gov/food-safety-charts/cold-food-storage-charts) (page states Date Last Reviewed September 19, 2023) | Reached in full | Leftovers / cooked meat or poultry: fridge 3–4 days, freezer 2–6 months; freezer-guidelines-are-quality-only footnote (0°F indefinite safety) |
| [GitHub Pages · About GitHub Pages and Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll) | Reached in full, both chunks | The default rule that Jekyll does not build files/folders starting with `_` — the rule the underscore rename relies on |
| [GitHub Pages · Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) | Reached in full, chunk 0 | Branch-vs-workflow publishing modes; the warning that Pages sites are publicly available even when the repository is private |
| [Troubleshooting Jekyll build errors](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/troubleshooting-jekyll-build-errors-for-github-pages-sites) | Reached in full, both chunks | Checked for the `.nojekyll` bypass wording; **not found on the page** — so FLG-029 states the `.nojekyll` mechanism as the standard explanation and rests its claim on direct live observation instead |
| Live host, three fetches | Full content returned | `/_data/confirmations.json`, `/_platform/collector.py`, `/_tools/build.py` all serve as-is on the legacy Pages host (evidence for FLG-029) |

## Serving-scope finding (FLG-029), stated precisely

What was observed: three underscore-prefixed repo paths returned their full
content over the public host on 2026-11-20. What is documented: Jekyll's default
exclusion of `_`-prefixed paths, and the public availability of Pages sites.
What is standard knowledge but was not found verbatim in a fetched official page
this session: that `.nojekyll` disables the Jekyll build. The flag separates the
three. The finding does not depend on the mechanism: the paths are public, whatever
explains it.

The owner-level repair is unchanged from the previous sessions' handoff: switch
Pages publishing to the GitHub Actions workflow so the staged `_site` — not the
branch root — is served. `pages.yml` already supports it. This session cannot
change the repository setting and did not try.

## Guide-content rules respected

- No price, rating, review count, stock figure, or `$` anywhere in the new page
  (enforced by `check.py`; confirmed by its clean run).
- Product descriptions limited to listing-title wording already transcribed in
  `_src/data/products.json`; the only product-adjacent sentence ("An instant-read
  like the one in the shortlist answers the only question the appliance cannot")
  states no specification and names no brand.
- No claim that any product was tested, ranked or scored; the closing line says
  so explicitly and points the reader to the manual of their own model.
- The appliance-vs-guidance tension (official guidance says cover to reheat; a
  fan appliance crisps by dry air) is published as an editorial observation
  clearly separated from the official rule, and the "official guidance does not
  say" section names the gap rather than filling it — the anti-AI-slop rule the
  brief asks for.
- Illustration recorded in the images register with `depicts_a_real_product:
  false`; the page caption says it is not a photograph of any product sold here.

## Gates run on this branch (2026-11-20)

```
python3 _tools/build.py            → 35 HTML pages; second run byte-identical (md5 on index.html)
python3 _tools/check.py            → 35 pages, 0 errors, 0 warnings
python3 _tools/validate.py         → 1882 checks, all pass, 0 warnings
python3 _tools/check_local_links.py→ 69 pages, 0 broken relative references
cd _tools && python3 -m unittest test_paid_link_gate → OK
```

Spot-checks on the generated guide page:

- All official figures present and attributed: `165°F` (3 placements), `3 to 4
  days`, `2 to 6 months`, `rolling boil`, 2-hour / 1-hour rules.
- 8 outbound official-source links render (5 table-row links + 2 source-list
  links; the FoodSafety.gov chart URL appears on both the row and the list).
- `rel="sponsored nofollow noopener"` present on both product CTAs.
- In-guide table of contents anchors resolve (built by `_anchor()`, not hand-written).
- `sitemap.xml` carries the new URL exactly once; `feed.xml` carries it with dek
  and cluster; `robots.txt` now reads `Disallow: /_archive/`.

## Irregularities and refusals

- **FLG-029 (high, new)** — see above. Not fixed by this session; the durable fix
  is a repository setting only the owner can flip. Recorded, not papered over.
- **FLG-030 (low, new, fixed)** — stale `Disallow: /archive/` corrected to
  `/_archive/` in the generator.
- **Side-card overclaim, fixed** — the guide template asserted every product link
  carries the Amazon tag; the current build deliberately ships listing links
  without a tag until an account-validated Special Link exists (FLG-025 reading,
  PR #106's flag). Wording corrected to what is true of every build.
- **Sources field was dead** — guides carried `sources` data the template never
  rendered. Now rendered. The pre-existing `holiday-side-dish-capacity` guide's
  source (USDA FSIS Food thermometers) becomes visible as a side effect; that URL
  was already in `sources.json` from earlier sessions and was not re-fetched here.
- **Not verified this session, on purpose:** the five submitted links (FLG-028's
  homepage result not reproduced — one data point does not settle instability;
  left to the register); Associates enrolment, attribution, Special Links,
  Search Console, analytics hosting — all owner gates, all `needs review`.
- Renumbering note: if a concurrent PR had taken FLG-029/030 before this merged,
  the IDs here would have been renumbered before merge. PR #104/#106 do not touch
  those IDs (checked 2026-11-20 ~06:5x UTC, before commit).
