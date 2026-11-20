# Executive summary — Affil1 / Crisp & Counter

**What:** a live Amazon affiliate publication for air fryers and countertop cooking
appliances, tracking ID `shopnow047c-20` (supplied by the owner; enrolment unverified).
**Where:** https://karagemop466-tech.github.io/Affil1/
**When:** 2026-11-20, integration pass by session `arena/359baa16-affil1`.
**Repo:** `karagemop466-tech/Affil1`, published from `main` by GitHub Actions.

## Read this first: the three facts that matter

An Amazon affiliate publication covering five supplied links: product research,
comparison content, buying guides, click measurement, compliant disclosure, a
suggestions section the owner can decide from, a clear list of questions that
must be answered before decisions, and a live site — built and merged without
further input.

## What exists now

One canonical site, 29 pages, rebuilt from `src/data` on every deploy:

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

Each submitted link was fetched, redirects followed, and the destination's own title and
breadcrumb read. No value was inferred; nothing that could not be read from the official
page is populated. Sources: Amazon's own listing pages (URLs below),
[Associates Program Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement)
§1 and §5, [Associates Program Policies / Commission Income
Statement](https://affiliate-program.amazon.com/help/operating/policies) §2, and the
[FTC Endorsement Guides](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking).

| Entry | Submitted link | Destination reached 2026-11-20 | Product, as the listing names it |
|---|---|---|---|
| P-01 | `link.amazon/B04G1MEwY` | `amazon.com/dp/B0CDY277D3` | CHEFMAN 6 Quart Dual Basket Air Fryer Oven |
| P-02 | `link.amazon/B02NbDxp3` | `amazon.com/dp/B09B7SB46R` | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven |
| P-03 | `link.amazon/B00hJ57DV` | `amazon.com/dp/B08DKYBTPH` | Chefman Air Fryer 8 Qt TurboFry 4-in-1 |
| P-04 | `link.amazon/B0c8moW59` | `amazon.com/dp/B0DHZTCNR5` — ThermoMaven 1 Sec instant-read thermometer | resolved on the third attempt (05:52 UTC); arrival carried `plpRedirect=mhFallback` |
| P-05 | `link.amazon/B0f3GKalj` | `amazon.com/dp/B0DZFD6R9Z` | CHEF iQ Sense Smart Wireless Meat Thermometer |

Notes that belong with that table, not under it:

- **All five submitted codes are 9 characters.** Every destination ASIN is 10. A 9-character
  code cannot be matched to a catalog ASIN as written, so `intended_asin` stays null and
  the observed destination is stored separately. That is a data-integrity finding, not an
  accusation that the links are invalid — their compliance status is unresolved
  (FLG-003) and the site says so.
- **P-05 is not an air fryer.** It is a probe thermometer, in a different Amazon category.
  Rather than dropping the awkward row, the publication has a guide for it.
- **Amazon's answers are not stable.** Two links returned a bot interstitial on the first
  request and a product page on a later one. Destinations on this site are dated
  observations, not assertions, and a weekly audit exists to notice when one changes.

## What the site is now

- **9 buyer guides**, question-shaped and seasonal (holiday oven relief, frozen weeknights,
  dual-basket math, probe thermometers, the first-week checklist, capacity, cleanup,
  shape, multi-function claims), each closing by naming what it does not claim.
- **A shortlist of all five rows**, described only in the seller's own words, with a
  save-to-browser list (localStorage, nothing transmitted) and no button at all for the
  row that never resolved.
- **Topics/cluster pages** so the internal link graph is deliberate, and an editorial
  **queue** published in the open with the reason each candidate is there.
- **Registers, demoted to the footer where a buyer will not trip over them:** source
  register, flagged register (15 items, each with its source), suggestion board
  (29 proposals), open questions (22, 5 answered by this pass), operations dashboard.
- **No prices, ratings, review counts or stock anywhere** — enforced by a build-time
  check, not by a promise. Publishing them without a PA/Creators feed is prohibited, and
  a stale price is a false claim. Price tracking and price alerts are recorded on the board
  as things this site must *never* build (the Participation Requirements prohibit them).

## Measurement, and what it will not pretend

Five events are defined and instrumented in a client that ships inert — nothing is sent
until a first-party collector is deployed, because static GitHub Pages cannot receive a
POST. No cookies, no IP capture, no third-party script. The campaign ledger is published
empty with its schema and a dated provenance trail; sessions, clicks and reported orders
are entered only from the account's own authorized reports. Click counts are never
presented as conversions: attribution lives in Amazon's numbers, not ours. Search
Console is **not** connected — no agent verified a property it does not own — so the
topic queue is labelled reasoning, and the first measured queries are what should
re-order it.

## Flagged for review (all published on the site, none hidden)

| ID | Item | Why it is flagged |
|---|---|---|
| FLG-001 | Five 9-character codes, not ASINs | The intended product identity cannot be read from any official source |
| FLG-002 | Tracking-ID attribution unconfirmed | Only the enrolled account's click report can confirm it |
| FLG-003 | Compliance status of `link.amazon` destinations unresolved | Redirect + no tag: cannot be attributed as published; not declared invalid |
| FLG-004 | P-04 resolved only on a third attempt | Two interstitials, then a fallback-flagged listing |
| FLG-018 | Three arrivals carry `plpRedirect=mhFallback` | The published destination may be a fallback, not the intended product |
| FLG-007 | Wattage, dimensions, warranty, noise blank | Not confirmable from an official source with this access |
| FLG-014 | Contradiction between archived registers on P-03/P-05 | Recorded as a correction with both observations dated |
| new | Two Pages deployments racing | Pages is set to a legacy branch build while Actions also publishes; owner decision on which is canonical |

## Decisions waiting for you, in the order that pays

1. Generate Special Links in Associates Central; test one; confirm the click; then
   `tools/arm_links.py` to arm it. Until then the site publishes reference links and earns nothing.
2. Verify Search Console (and Bing) on the live host. Nothing editorial should be
   decided before four weeks of real queries exist.
3. Name an author, or accept that desk-level bylines are the honest state. This is the
   one credibility item that cannot be generated.
4. Decide the production host (github.io project path vs a custom domain). Canonical URLs,
   sitemap and feed all rebuild from one constant in `tools/build.py`.
5. Then, and only then, the volume items: two guides a month, imagery per guide, hub pages
   for situations ("small kitchen, two people"), a downloadable capacity worksheet as the
   linkable asset.

Full scoring, cost and blockers: **/suggestions/**. What is unknown and who can supply
it: **/questions/**.

## No claim is made here that

any product was tested; any product is the best; any price, rating or stock level is
current; the Associates account is enrolled, in good standing, or attributing; any
traffic, conversion or revenue figure exists; or that Search Console / analytics are
running. Every one of those would need a source this project does not have, so each is
either blank with a reason, or a question on a page.

## Integration + verification pass (2026-11-20, arena/982fea5a-affil1)

This pass merged `origin/main` (3193be2) into branch `arena/982fea5a-affil1`
(branched from `main` at 8961b9a) to finish the integration. Conflict
resolution: the newer-edition files take main's versions — the maintained root
edition (generated pages, the paid-link gate, the canonical-five analytics
client, 21 flags). This pass's reconciliation is retained where main's version
was stale: `tools/validate.py` was reconciled to the canonical
`src/data/products.json` schema (`ref`/`submitted_code`/`submitted_code_length`/
`intended_asin`/`observed_asin`; the retired `crisp/`-era rules removed) and now
passes. `docs/EXECUTIVE_SUMMARY.md` was deleted by main (the root
`EXECUTIVE_SUMMARY.md` supersedes it).

### Line-by-line verification of the five submitted links

Fetched through the redirect via fetch_page against official Amazon pages; the
final URL read, the 10-character ASIN extracted from the `/dp/` segment, and the
page title transcribed and compared with the register (`src/data/products.json`):

| Submitted link | Resolved to | Title matches register |
|---|---|---|
| https://link.amazon/B04G1MEwY | https://www.amazon.com/dp/B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer — yes |
| https://link.amazon/B02NbDxp3 | https://www.amazon.com/dp/B09B7SB46R | Emeril Lagasse 26QT French Door — yes |
| https://link.amazon/B00hJ57DV | https://www.amazon.com/dp/B08DKYBTPH | Chefman Air Fryer 8 Qt TurboFry — yes |
| https://link.amazon/B0c8moW59 | https://www.amazon.com/dp/B0DHZTCNR5 | ThermoMaven 1 Sec — yes (resolved on re-verification 2026-11-20; was checkpoint-only) |
| https://link.amazon/B0f3GKalj | https://www.amazon.com/dp/B0DZFD6R9Z | CHEF iQ Sense — yes |

No arrival URL carried the tracking tag; attribution unconfirmed (FLG-002).
Sources: the five listing pages; https://affiliate-program.amazon.com/help/operating/policies;
https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v2022-04-01-reference (ASIN definition).

### Toolchain on the merged tree (2026-11-20)

- `python3 tools/build.py` — 29 pages.
- `python3 tools/check.py` — 0 errors, 0 warnings.
- `python3 tools/check_local_links.py` — 0 broken relative references.
- `python3 tools/validate.py` — 1441 checks, 0 warnings.
