# Affil1 — Executive summary

**Project:** Amazon affiliate publication (static site on GitHub Pages)
**Live:** <https://karagemop466-tech.github.io/Affil1/>
**Tracking ID:** `shopnow047c-20` (supplied; applied to every link; attribution not yet confirmed in the Associates account)
**Prepared:** 2026-11-20

## What this is

A buyer-facing shop and guide site for five kitchen products: two air fryers, one
French-door air-fryer oven and two meat thermometers. It is built to read like a
publication — a shop front, a shortlist, category pages, question-shaped guides —
and to be verifiable underneath: every product fact is either transcribed from
the live Amazon listing with the date it was checked, or quoted from an official
source, or absent.

## The five products, verified on 2026-11-20

Each supplied short link was opened, the arrival page read, and the destination
ASIN and listing title transcribed. Intended ASIN and observed ASIN are separate
fields and are never merged.

| # | Submitted link | Code in the link | Listing reached | Product | Status |
|---|---|---|---|---|---|
| 1 | <https://link.amazon/B04G1MEwY> | `B04G1MEwY` (9 chars) | <https://www.amazon.com/dp/B0CDY277D3> | CHEFMAN 6-quart dual-basket air fryer | resolved |
| 2 | <https://link.amazon/B02NbDxp3> | `B02NbDxp3` (9 chars) | <https://www.amazon.com/dp/B09B7SB46R> | Emeril Lagasse 26-quart French-door air fryer oven | resolved |
| 3 | <https://link.amazon/B00hJ57DV> | `B00hJ57DV` (9 chars) | <https://www.amazon.com/dp/B08DKYBTPH> | Chefman 8-quart TurboFry air fryer | resolved |
| 4 | <https://link.amazon/B0c8moW59> | `B0c8moW59` (9 chars) | <https://www.amazon.com/dp/B0DHZTCNR5> | ThermoMaven instant-read thermometer | resolved (see FLG-016) |
| 5 | <https://link.amazon/B0f3GKalj> | `B0f3GKalj` (9 chars) | <https://www.amazon.com/dp/B0DZFD6R9Z> | CHEF iQ Sense wireless thermometer | resolved (see FLG-016) |

Two irregularities are recorded rather than smoothed over:

- **FLG-001** — all five supplied codes are nine characters; all five ASINs on
  arrival are ten. The codes are short-link slugs, not product identifiers, so
  `intended_asin` is blank for every product rather than filled with a slug.
- **FLG-016** — a parallel session observed P-04 and P-05 reaching each other's
  destinations on the same date. Both observations are published with their date;
  neither is presented as the intended product.

## The defect that mattered most, and was fixed

Before this pass, **48 of the site's 101 Amazon product links carried no tracking
tag** — including every link on the front page, every product page and the whole
comparison table. They were correctly marked `rel="sponsored nofollow"` but, per
section 2 of Amazon's Program Policies, a Special Link must carry the Associates
ID as a URL parameter, and the Commission Income Statement excludes purchases
"not correctly tracked ... because the links ... are not properly formatted."

The cause was one line in the page templates: they passed the untagged listing
URL instead of a tagged one. Every product link now passes through a single
function that appends `?tag=shopnow047c-20`, and `tools/check.py` fails the build
if any Amazon product link on any generated page lacks a tag. Published as
FLG-018, including the part that is still unconfirmed: no click has yet been
seen in the Associates report.

## What exists on the site

| Surface | What it does |
|---|---|
| Shop front (`/`) | Five products led by the job each one does, shop-by-decision paths, guides, USDA temperatures, and four plainly stated rules |
| Product records (`/products/p-01..p-05`) | Seller's stated specs, the USDA targets for the thermometers, every field left blank and why |
| Categories (`/categories/air-fryers`, `/categories/thermometers`) | A browse layer generated from the same register |
| Guides (`/guides/`) | Six question-shaped buying guides, grouped by the decision they serve |
| Compare (`/compare/`) | Five products side by side, blanks left blank |
| Publishing calendar (`/calendar/`) | Dated slots, a status per slot, and one slot deliberately empty for a topic chosen from measured queries |
| Open questions (`/questions/`) | 16 questions, the answer where one exists, and five discovery routes for the ones that do not |
| Suggestions (`/suggestions/`) | 17 proposals in one decision table with an ordered path, plus a per-row accept/hold/reject control |
| Review queue (`/review/`) | 19 flags, each with the source to check it against |
| Measurement (`/review/measurement`) | Five events, a tested self-hosted collector, and the four steps to switch it on |
| Privacy (`/privacy.html`) | Generated from the collector's own field list so the two cannot disagree |
| Ledger (`/operations/ledger`) | Empty, with its provenance rule stated |

## Sources used, all read on 2026-11-20

| Ref | Source | Used for |
|---|---|---|
| SRC-01 | [Associates Program Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) (updated 15 Oct 2025) | §5 disclosure wording, quoted verbatim |
| SRC-02 | [Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) (updated 14 Apr 2026) | §2(a)(b) Special Links, the tag parameter, the price and availability rule |
| SRC-03 | [FTC Endorsement Guides FAQ](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) | Disclosure placement and conspicuousness |
| SRC-04 | [16 CFR Part 255](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255) | The regulation behind SRC-03 |
| SRC-05 | [Google: qualify outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) | `rel="sponsored"` as the paid-link marker |
| SRC-06 | [USDA FSIS safe-temperature chart](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart) (updated 14 Apr 2025) | The only numbers quoted as fact rather than as a seller's claim |
| SRC-07 | [Google Search Console](https://search.google.com/search-console/about) | What query data would be, and why it is not reconstructed locally |
| SRC-08 | [Bing Webmaster Tools](https://www.bing.com/webmasters/about) | The second, independent index |

## What is deliberately absent

- **Prices, star ratings, review counts, stock status.** Permitted only from
  Amazon-served data or the official API; neither is connected. Enforced by a
  build check that fails on a currency figure or a rating phrase.
- **Testing claims, rankings and winners.** Nothing was bought, used or measured.
- **Traffic, conversion and revenue figures.** No analytics are deployed, no
  Search Console property is verified, no commission rate has been read. The
  campaign ledger has zero rows.

## The next three decisions

1. **Confirm one click in the Associates report.** The links are tagged; the
   evidence that a click is credited does not yet exist. One click, then the
   report for that day.
2. **Put the site into two indexes.** Verify Search Console, submit the sitemap,
   then submit the same sitemap to Bing Webmaster Tools. Both accept a sitemap
   and report queries without any script on the page.
3. **Then choose between testing and waiting.** Buy one product and build a page
   from real measurements, or wait four weeks and write the next guide from query
   data. More guides written from instinct is the option that looks like progress
   and is not.

## Verdict

The site is live, internally consistent, machine-checked and honest about what it
does not know. It cannot yet be said to earn: attribution is unconfirmed and no
traffic data exists. Every place where that is true is published on the review
queue with a source and a date, rather than filled with a plausible number.
