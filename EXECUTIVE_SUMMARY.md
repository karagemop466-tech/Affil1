# Executive summary — Affil1 / Crisp & Counter

**What:** a live Amazon affiliate publication for air fryers and countertop cooking
appliances, tracking ID `shopnow047c-20` (supplied by the owner; enrolment unverified).
**Where:** https://karagemop466-tech.github.io/Affil1/
**When:** 2026-11-20, integration pass by session `arena/359baa16-affil1`.
**Repo:** `karagemop466-tech/Affil1`, published from `main` by GitHub Actions.

## Read this first: the three facts that matter

1. **The traffic surface was broken in five different ways at once, and now it is one
   site.** `main` had accumulated four competing front pages plus an archive: a
   storefront at the root, a second publication under `/crisp/`, two more CSS/JS
   shells, and duplicated guide/suggestion/flag pages under both `/` and `/guides/`.
   Every root page also linked with root-absolute paths, which 404 under a GitHub
   Pages project mount. A buyer would have seen a half-styled page and a search
   engine would have seen two sites claiming the same content. One publication now
   publishes at the root; the rest is preserved, untouched, in `archive/`.
2. **As supplied, none of the five links could have earned anything.** Each is
   `link.amazon/<code>`: no `tag` parameter, and it reaches Amazon through an
   intermediate redirect. Amazon's Commission Income Statement disqualifies purchases
   arriving via a "Redirecting Link", and separately disqualifies any purchase "not
   correctly tracked or reported because the links from your site … are not properly
   formatted". The published buy buttons therefore point at the official listing URL
   with the tracking tag appended, and the register keeps the submitted link in its
   own field. **The remaining step is human:** generate the real Special Links in
   Associates Central, test one link, confirm one click in the account's report, then
   scale. Until then this site is a well-built shop with the door handle unbolted.
3. **Two registers in the repo contradicted each other about the same links, and both
   were partly wrong.** An archived file logged three links as "reached only the
   Amazon homepage"; a second file, written from a sandbox with no network, logged all
   five as unverifiable. A fresh double pass (two sessions, same day) resolves it: four
   reach product pages, one never leaves Amazon's bot interstitial. The correction is
   published on the site — at `/dashboard/#verification` and `/about/#corrections` —
   rather than quietly overwritten, and the contradictory file is left in `archive/`.

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
| P-04 | `link.amazon/B0c8moW59` | none — continue-shopping interstitial | unresolved; no buy button published |
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
| FLG-004 | P-04 never resolved | No product page reached; no button published |
| FLG-007 | Wattage, dimensions, warranty, noise blank | Not confirmable from an official source with this access |
| FLG-014 | Contradiction between archived registers on P-03/P-05 | Recorded as a correction with both observations dated |
| new | Two Pages deployments racing | Pages is set to a legacy branch build while Actions also publishes; owner decision on which is canonical |

## Decisions waiting for you, in the order that pays

1. Generate Special Links in Associates Central; test one; confirm the click. Then scale.
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
