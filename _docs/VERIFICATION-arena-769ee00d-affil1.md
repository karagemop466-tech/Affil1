# Verification pass — arena/769ee00d-affil1 · 2026-11-20

A second, independent read of every row this shop publishes about a product, plus the
official documents its rules rest on, plus the four things the pass found broken and
fixed rather than wrote around.

Read-only page fetches that follow redirects, issued from the agent environment between
06:52 and 07:10 UTC on 2026-11-20. Two things were read off each official page: the
document title, which carries the listing title, and the category breadcrumb. Nothing
here was copied from a search snippet, from another session's note, or from prior
knowledge of a product. The machine-readable copy is `_src/data/recheck.json`, rendered
at `verification/recheck.html`; this file keeps the raw strings an auditor would want
and the reasoning that stayed off a public page.

## 1. The five official listings — all five matched

| Ref | URL opened | Title served | Breadcrumb served |
|---|---|---|---|
| P-01 | https://www.amazon.com/dp/B0CDY277D3 | "Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen" | Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers |
| P-02 | https://www.amazon.com/dp/B09B7SB46R | "Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included : Home & Kitchen" | same Air Fryers path |
| P-03 | https://www.amazon.com/dp/B08DKYBTPH | "Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel : Home & Kitchen" | same Air Fryers path |
| P-04 | https://www.amazon.com/dp/B0DHZTCNR5 | "Amazon.com: ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified, Auto-Rotate Bright LED Screen, IP67 Waterproof for Grill BBQ, Stocking Stuffers Gifts for Men, Black : Home & Kitchen" | Home & Kitchen › Kitchen & Dining › Kitchen Utensils & Gadgets › Thermometers & Timers › Meat |
| P-05 | https://www.amazon.com/dp/B0DZFD6R9Z | "Amazon.com: CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors \| BBQ, Grill, Oven, Smoker, Air Fryer \| Gen3: Home & Kitchen" | same Meat thermometers path |

Consequence: the five published `observed_asin` values, the five transcribed titles and
both category paths are confirmed by a second session. No register row needed editing.

Not established by this, and not claimed anywhere on the site: the intended ASIN (still
null for all five), price, rating, review count, stock, dimensions, wattage, warranty,
or whether any of the five is any good. Program Policies §2(b) allows price and
availability only from Amazon-served data or the Creators/PA API, and this build has
neither, which is why those columns are empty by design rather than by omission.

## 2. The submitted short links — the part that did not reproduce

The operator supplied five links of the form `https://link.amazon/<9-character slug>`.

| Submitted link | Result in this session | Verdict recorded |
|---|---|---|
| `link.amazon/B04G1MEwY` (P-01) | `https://www.amazon.com/`, title "Amazon.com. Spend less. Smile more." | fell back to the marketplace home page |
| `link.amazon/B02NbDxp3` (P-02) | `https://www.amazon.com/`, same title, a Black Friday promotion rail in place of a product | fell back to the marketplace home page |
| `link.amazon/B0f3GKalj` (P-05) | `https://www.amazon.com/dp/B0DZFD6R9Z` carrying `plpRedirect=mhFallback` and a session token, with the CHEF iQ Sense title | reached the recorded listing |
| `link.amazon/B00hJ57DV` (P-03) | request failed | no observation |
| `link.amazon/B0c8moW59` (P-04) | request failed (two further attempts also failed) | no observation |

Three sessions now hold three accounts of the same five slugs: one recorded all five as
resolving, a second recorded all five returning the home page, and this pass reached the
home page for two, the listing for one, and got nothing for two. That is reported as
instability of the route, never as proof that a link is dead, invalid or non-compliant —
FLG-003 keeps that question open, and it can only be settled inside the enrolled account.

What the site does about it, and what was changed here:

* no buy button forwards a short link; every destination is built from the observed ASIN
  as a plain official listing URL, and `paid_link_gate.py` refuses a tag the account has
  not issued;
* the front-page trust band used to read that each of the five links "was opened,
  followed to the Amazon listing it lands on". That sentence is not reproducible from the
  submitted URL, so it now says what two sessions can support and links the log (FLG-055);
* the matching row on `verification/` moved from *holds* to *holds, with a caveat* rather
  than being quietly deleted.

## 3. Official documents re-read in this session

| Document | URL | What it was checked against |
|---|---|---|
| 16 CFR Part 233 — Guides Against Deceptive Pricing | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-233 | §233.1(a) verbatim: "If the former price is the actual, bona fide price at which the article was offered to the public on a regular basis for a reasonably substantial period of time, it provides a legitimate basis for the advertising of a price comparison." eCFR footer: "Displaying title 16, up to date as of 11/18/2026", source 32 FR 15534. Quoted in the deal-week guide, added as SRC-18. |
| USDA FSIS — Leftovers and Food Safety | https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety | "Leftovers can be kept in the refrigerator for 3 to 4 days or frozen for 3 to 4 months"; the two-hour rule; microwave reheating "until it reaches 165° F as measured with a food thermometer". Added as SRC-19. |
| Amazon Associates Program Policies | https://affiliate-program.amazon.com/help/operating/policies | the price/availability permission and the tag requirement, as quoted in `_src/data/sources.json` (SRC-02/03/14/15, read directly by session arena/62b049f0-affil1 the same day) |
| Associates Operating Agreement | https://affiliate-program.amazon.com/help/operating/agreement | the §5 sentence every page must carry; verified here as *applied*: the strip precedes `<main>` and the sentence appears twice per page, which `check.py` enforces |
| Google — qualify outbound links | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | sponsored marking on every product destination |
| OPM federal holidays | https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/ | Thanksgiving Day, Thursday 26 November 2026. Used only as calendar framing: "Black Friday" and "Cyber Monday" have no official date, so the guides are written to stay true without naming them as events (Q-27) |
| GitHub Pages limits / configuration | https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits | and `gh api repos/karagemop466-tech/Affil1/pages` → `build_type: "legacy"`, `source: {branch: main, path: "/"}`: the repository root **is** the public host |

## 4. What this pass found broken, and what it did

1. **A deploy gate that could not fail.** `.github/workflows/pages.yml` copied the tree,
   rebuilt and diffed — after its own build step had already written the generated pages
   into that tree. It compared build output with build output, so it could only catch a
   non-deterministic generator, never a hand-edited or stale committed page. On a legacy
   Pages site the committed file is what readers get. Found by testing reproducibility on
   a clean checkout, which changed `guides/where-to-put-the-probe.html`. Repaired: the step
   now diffs against `HEAD`, then rebuilds and diffs again. FLG-052, Q-31.
2. **A generator emitting the same source list twice.** `page_guides.py` rendered a guide's
   `sources` both as an in-body aside and as the article's Sources block; five guides shipped
   with the duplicate, and one had been trimmed by hand in the committed HTML — which is how
   (1) was found. Fixed in the generator, and the five pages regenerated. No hand edit was
   kept or copied.
3. **A photograph where the site's own rule forbids one.** `assets/img/meal-prep.jpg`, a
   1408×768 photorealistic render, was loaded by a guide and the guides index, while
   `review/images.html` states that every image is an engraved two-colour illustration and
   that photographic imagery is barred. The register had recorded it honestly as a
   photograph, which documented the contradiction instead of ending it. Replaced with a
   registered engraving; the render stays in the tree, unserved, as the record. FLG-053,
   Q-32.
4. **A measurement path that could not start.** `_tools/preview.py` inserted `ROOT/'analytics'`
   on the import path, dead since the underscore rename, so the command the README documents
   raised ImportError. (`_analytics/endpoint.py` had the same class of stale path and had
   already been fixed by another session the same morning.) Corrected; the analytics test and
   both collector tests now run. FLG-054.
5. **Counts retyped into prose.** The verification page linked "The 22 pre-existing flags"
   against a register of 51; the suggestions page asserted a guide count and a path count in
   fixed text; `EXECUTIVE_SUMMARY.md` and `README.md` restate register sizes by hand. The
   generated pages were made to count from the data; the markdown was corrected once and the
   standing fix filed as S-52 rather than re-typed again next merge.

Logged, not touched, because the files belong to another owner: `_platform/README.md` still
documents its commands as `python3 platform/…`, which has not been the path since the rename.

## 5. Gates, run on the merged tree at commit time

| Gate | Result |
|---|---|
| `_tools/build.py` | 50 pages, zero rebuild drift |
| `_tools/check.py` | 0 errors, 0 warnings |
| `_tools/validate.py` | 3,285 checks, 0 warnings |
| `_tools/check_image_register.py` | 0 errors |
| `_tools/check_local_links.py` | 0 broken references |
| `_tools` unit tests (paid-link gate) | OK |
| `_analytics`, `_measurement` tests | OK |
| `_decision-support/validate.py` | PASS |
| `_platform/verify_edition.py` | 0 errors |

## 6. Links for manual review

* Second-read log, one dated source link per row:
  https://karagemop466-tech.github.io/Affil1/verification/recheck.html
* Page-by-page audit: https://karagemop466-tech.github.io/Affil1/verification/
* Everything flagged: https://karagemop466-tech.github.io/Affil1/review/
* Decision register and paths: https://karagemop466-tech.github.io/Affil1/questions/ ·
  https://karagemop466-tech.github.io/Affil1/suggestions/
* The five listings as published: [P-01](https://www.amazon.com/dp/B0CDY277D3) ·
  [P-02](https://www.amazon.com/dp/B09B7SB46R) · [P-03](https://www.amazon.com/dp/B08DKYBTPH) ·
  [P-04](https://www.amazon.com/dp/B0DHZTCNR5) · [P-05](https://www.amazon.com/dp/B0DZFD6R9Z)
