# Crisp & Counter (Affil1) — Executive Summary

**Project:** Amazon affiliate kitchen buying publication (GitHub Pages)  
**Live site:** https://karagemop466-tech.github.io/Affil1/  
**Selected Tracking ID:** `shopnow047c-20` (supplied in brief; click attribution not independently confirmed — see `FLG-002`)  
**Verified & updated:** 2026-11-20

---

## 1. What was built
A 27-page static buyer-facing publication (**Crisp & Counter**) organized into two verified Amazon product categories — **Air Fryers (3)** and **Meat Thermometers (2)** — built from a single JSON source of truth (`src/data/`) and validated automatically on every build (`tools/check.py` + `.github/workflows/pages.yml`).

- **Front page (`index.html`)**: Leads immediately with products grouped by category (Air Fryers + Meat Thermometers), four buyer-decision paths, seven question-shaped buying guides, publishing rules, and a dated verification log.
- **Category subpages**: `products/air-fryers.html` (3 air fryers) and `products/thermometers.html` (2 meat thermometers), plus the complete **Product-Intent Confirmation Register** (`products/index.html`) and individual product records (`products/p-01.html`..`p-05.html`).
- **Side-by-side comparison (`compare/index.html`)**: All five verified listings compared strictly on seller-stated attributes and observed ASINs — zero invented prices, ratings, or winners.
- **Seven buying guides (`guides/`)**: Basket vs. oven, instant-read vs. wireless meat thermometer (with official **USDA FSIS** Safe Minimum Internal Temperature Chart), air-fryer capacity checklist, cleanup & counter space, Sunday meal-prep batch timing, holiday roast & air-fryer playbook, and multi-function appliance questions — all wired into `sitemap.xml` and `feed.xml`.
- **Decision & audit surfaces** (reachable from one navigation group and the footer):
  - **Open Questions (`questions/index.html`)**: 15 pre-decision questions (5 answered with evidence, 10 open with exact steps to close).
  - **Suggestions (`suggestions/index.html`)**: 14 reviewable proposals with local Accept / Hold / Reject decision controls and plain-text copy export.
  - **Flagged for Review (`review/index.html`)**: All 15 audit flags ordered by severity with official source links, plus Image Policy (`review/images.html`) and Measurement Plan (`review/measurement.html`).
  - **Campaign Ledger (`operations/ledger.html`)**: Empty by design with strict provenance columns; no conversion score or revenue forecast is shown.
  - **About & Sources (`about/index.html`)**: Full disclosure, linking rules, privacy posture, and 8 directly verified official sources with verbatim quotes.

---

## 2. Verified product register (5/5 observed on 2026-11-20)

Every submitted short link was requested directly against Amazon.com on 2026-11-20. **Intended ASIN** and **Observed ASIN** are stored in separate fields and never merged (`FLG-001`): all five submitted path codes are 9 characters with lowercase letters (short-link slugs), while every arrival ASIN is 10 uppercase characters.

| Ref | Category | Submitted link | Submitted code (9 chars) | Intended ASIN | Observed ASIN (10 chars) | Official Amazon listing | Status |
|---|---|---|---|---|---|---|---|
| P-01 | Air Fryers | `https://link.amazon/B04G1MEwY` | `B04G1MEwY` | — | `B0CDY277D3` | https://www.amazon.com/dp/B0CDY277D3 — CHEFMAN 6 Quart Dual Basket Air Fryer Oven (2×3 Qt) | Observed |
| P-02 | Air Fryers | `https://link.amazon/B02NbDxp3` | `B02NbDxp3` | — | `B09B7SB46R` | https://www.amazon.com/dp/B09B7SB46R — Emeril Lagasse 26QT French Door Air Fryer Toaster Oven | Observed |
| P-03 | Air Fryers | `https://link.amazon/B00hJ57DV` | `B00hJ57DV` | — | `B08DKYBTPH` | https://www.amazon.com/dp/B08DKYBTPH — Chefman Air Fryer 8 Qt TurboFry 4-in-1 | Observed |
| P-04 | Meat Thermometers | `https://link.amazon/B0c8moW59` | `B0c8moW59` | — | `B0DHZTCNR5` | https://www.amazon.com/dp/B0DHZTCNR5 — ThermoMaven 1 Sec Professional Digital Meat Thermometer | Observed (resolved after earlier `/checkpoint/continue` blocks; `FLG-004`) |
| P-05 | Meat Thermometers | `https://link.amazon/B0f3GKalj` | `B0f3GKalj` | — | `B0DZFD6R9Z` | https://www.amazon.com/dp/B0DZFD6R9Z — CHEF iQ Sense Smart Wireless Meat Thermometer (3 Probes) | Observed |

Prices, star ratings, review counts, availability, wattage, dimensions, warranties, and commission rates are **intentionally blank** because neither Amazon-served widgets nor Creators API / PA API nor Associates Central credentials are connected (`SRC-02`, `FLG-005`, `FLG-013`).

---

## 3. Official sources verified directly (2026-11-20)

| Ref | Official source | URL |
|---|---|---|
| SRC-01 | Amazon Associates Program Operating Agreement (§5) | https://affiliate-program.amazon.com/help/operating/agreement |
| SRC-02 | Amazon Associates Program Policies (§2(b) Special Links & Prices) | https://affiliate-program.amazon.com/help/operating/policies |
| SRC-03 | FTC Endorsement Guides: What People Are Asking | https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking |
| SRC-04 | 16 CFR Part 255 (eCFR, current through 2026-11-18) | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255 |
| SRC-05 | Google Search Central — Qualify Outbound Links (`rel="sponsored"`) | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links |
| SRC-06 | USDA FSIS — Safe Minimum Internal Temperature Chart | https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart |
| SRC-07 | USDA FSIS — Food Thermometers | https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers |
| SRC-08 | Amazon Selling Partner API — Catalog Items API v2022-04-01 Reference | https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v2022-04-01-reference |

---

## 4. Compliance & quality gates enforced automatically (`tools/check.py`)
1. Above-the-fold affiliate disclosure strip directly under the masthead on every page + footer repeat (`SRC-01`, `SRC-03`).
2. Every outbound Amazon product link carries `rel="sponsored nofollow noopener"` and `target="_blank"` (`SRC-05`); official policy citations are NOT marked `sponsored`.
3. Zero currency figures, star ratings, review counts, stock phrases, rankings, or test claims anywhere in visible text (`SRC-02`).
4. Zero root-absolute internal links (every path resolves cleanly under `/Affil1/`), zero external resource loads (self-hosted fonts), zero broken internal anchors, exact sitemap/feed parity, and CI build reproducibility check.

---

## 5. Key open risks & recommended next decisions (`suggestions/index.html`)
1. **Confirm tracking & intended ASINs (`S-01`, `S-02` — High Priority)**: None of the five resolved URLs showed a `tag=` parameter on arrival (`FLG-002`). Confirm intended ASINs inside Associates Central, generate validated Special Links for `shopnow047c-20`, test one live click, and confirm it appears in the Associates click report before scaling traffic.
2. **Search Console indexing (`S-07`)**: Verify the GitHub Pages property and submit `sitemap.xml` so future guides are chosen from measured queries rather than hypotheses.
3. **First-party measurement (`S-06`, `S-14`)**: Publish a formal privacy notice, deploy the self-hosted collector (`server/collect.js`) on a first-party host, and enable the five defined events (`page_view`, `outbound_click`, `guide_open`, `search_query_referral`, `report_import`) in `assets/js/analytics.js`.
4. **Editorial credibility (`S-03`, `S-04`, `S-12`)**: Name a real editor and consider hands-on testing with real photography before adding more guides (`S-11`).
