# Executive summary — Affil1 / Crisp & Counter

**Site:** Crisp & Counter — https://karagemop466-tech.github.io/Affil1/
**Tracking ID:** shopnow047c-20
**Date:** 20 November 2026

## What was asked for

An Amazon affiliate publication covering five supplied links: product research,
comparison content, buying guides, click measurement, compliant disclosure, a
suggestions section the owner can decide from, a clear list of questions that
must be answered before decisions, and a live site — built and merged without
further input.

## What exists now

One canonical site, 27 pages, rebuilt from `src/data` on every deploy:

- a product-led front page with five picks in two categories and a buy button on
  every card;
- a product page for each of the five, with stated facts, who it suits, who
  should skip it, and a one-block provenance record;
- a side-by-side comparison table;
- nine question-shaped guides across six clusters;
- a decision register of 22 questions, 10 answered with evidence;
- a suggestion queue with three coherent paths and 18 proposals, of which 8 have
  already been implemented and are shown with evidence;
- 19 review flags, an image policy, an inert analytics client and an empty
  campaign ledger with a provenance rule;
- a build-time checker that fails on a broken link, a missing disclosure, an
  untagged Amazon link, a reintroduced price, or a second competing edition.

## What was verified, and how

Each of the five supplied links was opened on 2026-11-20 and **all five
resolved**. The ASIN, page title and category breadcrumb were transcribed:

| Ref | Landed on | Product |
|---|---|---|
| P-01 | B0CDY277D3 | CHEFMAN 6 qt dual-basket air fryer |
| P-02 | B09B7SB46R | Emeril Lagasse 26 qt French-door air fryer oven |
| P-03 | B08DKYBTPH | Chefman 8 qt TurboFry air fryer |
| P-04 | B0DHZTCNR5 | ThermoMaven digital meat thermometer |
| P-05 | B0DZFD6R9Z | CHEF iQ Sense wireless meat thermometer |

Amazon's Operating Agreement §5, Program Policies §2(a)/(b), the FTC's
endorsement FAQ and Google's outbound-link documentation were each read in this
session and are quoted with links on the sources page.

## The three findings that change the plan

1. **The previous build's buy links had no tracking tag at all.** Program
   Policies §2(b) requires the Associates ID as a URL parameter, and a bare
   `/dp/` URL cannot be attributed to any account. Every destination is now built
   in one function with `?tag=shopnow047c-20`, and the build fails on an untagged
   link. This was a live defect and it is published on the review page.
2. **The site was two sites.** A generated edition and a hand-written one served
   the same five products from different URLs, competing for the same searches.
   They are consolidated; the other edition is archived with `noindex` on every
   page, not deleted.
3. **The fourth link resolves** — to a thermometer, not a fourth air fryer. The
   catalogue is three air fryers and two thermometers, and the site now says so.

## What still cannot be confirmed

- **Attribution.** No resolved URL showed the tag, and no Associates report has
  been read. One click from the owner's device plus the Orders report settles it.
- **Intended ASINs.** The supplied codes are nine-character short-link slugs, not
  identifiers. Only the account can supply what was intended.
- **Price, rating, availability.** Not shown anywhere, by rule: Amazon permits
  them only from Amazon-served data or its APIs, and neither is connected.
- **Author, traffic, rates, email list.** None exist. All are published as gaps.

No conversion score, revenue forecast or traffic estimate appears anywhere.

## The next decision

In order:

1. Click one product link, then read the Associates report.
2. Verify Search Console and submit the sitemap.
3. Choose one path on the suggestions page — shop first, publication first, or
   measure first — and commit to it before adding anything else.

Writing more guides before either measurement exists is the option that looks
like progress and is not.
