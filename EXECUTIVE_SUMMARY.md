# Executive summary — Affil1 / Crisp & Counter

**What:** a live Amazon affiliate publication for air fryers and countertop cooking
appliances, tracking ID `shopnow047c-20` (supplied by the owner; enrolment unverified).
**Where:** https://karagemop466-tech.github.io/Affil1/
**When:** 2026-11-20, integration pass by session `arena/359baa16-affil1`; counts and
verification refreshed 2026-11-20 by session `arena/62b049f0-affil1` (see addendum at the end).
**Repo:** `karagemop466-tech/Affil1`, published from `main` by GitHub Actions.

## Read this first: the three facts that matter

An Amazon affiliate publication covering five supplied links: product research,
comparison content, buying guides, click measurement, compliant disclosure, a
suggestions section the owner can decide from, a clear list of questions that
must be answered before decisions, and a live site — built and merged without
further input.

## What exists now

One canonical site, rebuilt from `_src/data` on every deploy by `_tools/build.py`
and checked page by page by `_tools/check.py`:

- a product-led front page with five picks in two categories and a buy button on
  every card;
- a product page for each of the five, now leading with a **buying decision
  block** — choose it if / check before you buy / what it costs you / where the
  live price is — above the stated facts, who it suits, who should skip it, and a
  one-block provenance record;
- a comparison page with **two** tables: what the listings state, and what
  decision each product actually answers. The price and rating cells link to the
  live listing instead of sitting empty;
- ten question-shaped guides across six clusters, all in `sitemap.xml` and
  `feed.xml`;
- a decision register of 24 questions, 10 answered with evidence;
- a suggestion queue with three coherent paths and 21 proposals, of which some
  are already implemented and are shown with evidence;
- an owner's "what is left" page (`/now/`), a ranked offers page (`/offers/`, 10
  weighted offers) and a per-page verification audit (`/verification/`);
- a **decision registry** (`/decisions/`) of 7 open proposals, each carrying the
  official source and verbatim quote it is checked against, the single missing
  fact, the person who can close it, and an accept/hold/reject control recorded
  in the browser only;
- 27 review flags, an image policy, an inert analytics client and an empty
  campaign ledger with a provenance rule;
- a build-time checker that fails on a broken link, a missing disclosure, an
  Amazon product link outside the permitted set (an unapproved tag, a short link, or an unobserved ASIN), a reintroduced price, or a second competing edition.

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

- **10 buyer guides**, question-shaped and seasonal, across six clusters — basket or oven,
  dual-zone vs single basket, capacity, cleanup and counter space, meal-prep Sunday, the
  small-kitchen space audit, multi-function questions, thermometer pairing, holiday hosting
  and holiday side-dish capacity. Each closes by naming what it does not claim.
- **A shortlist of all five rows**, described only in the seller's own words, each linking
  only to its observed listing as a labelled reference link. P-04 is flagged (FLG-004,
  FLG-016) because earlier attempts returned checkpoints and the thermometer pair was
  swapped in one record; it is presented as a thermometer, not a fourth air fryer.
- **Topics/cluster pages** so the internal link graph is deliberate, and an editorial
  **queue** published in the open with the reason each candidate is there.
- **Registers, demoted to the footer where a buyer will not trip over them:** source
  register, flagged register (27 items, each with its source), suggestion board
  (21 proposals), open questions (24, 10 answered with evidence; 14 still blocked and
  published as such), decision registry (7 proposals), operations ledger.
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
   `_tools/arm_links.py` to arm it. Until then the site publishes reference links, and no click is attributable to the account.
2. Verify Search Console (and Bing) on the live host. Nothing editorial should be
   decided before four weeks of real queries exist.
3. Name an author, or accept that desk-level bylines are the honest state. This is the
   one credibility item that cannot be generated.
4. Decide the production host (github.io project path vs a custom domain). Canonical URLs,
   sitemap and feed all rebuild from one constant in `_tools/build.py`.
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

Ships the self-contained notes edition at `notes/`: shop-style front page leading with the verified shortlist, seven question-first guides, decision desk (suggestions queue with decision gates + pre-decision questions), transparency desk, own sitemap/feed. Disclosure above the fold; `rel="nofollow sponsored"` + `shopnow047c-20` on every outbound product link; no prices/ratings/commissions anywhere; ledger empty by design.

## Session addendum — arena/85183f5b-affil1 (2026-11-20)

Findability + line-by-line re-verification pass on the canonical edition:

- **Guide number ten.** `meal-prep-sunday` ported from the earlier integration log
  (question-shaped title, seller-transcribed facts only, `Living with it` cluster),
  with its own generated illustration registered in `src/data/images.json`. It flows
  into the sitemap (30 URLs) and the feed (10 items) through `GUIDES`.
- **Every published quote re-checked live on 2026-11-20** against SRC-01..SRC-10:
  Operating Agreement §1 and §5, Program Policies §2(b), the FTC endorsement FAQ
  (placement + affiliate sections), Google's outbound-link qualification, the
  eCFR current text of 16 CFR 255 (§255.5 Example 11, the affiliate-blogger case),
  USDA FSIS chart and thermometer pages, and Amazon's SP-API ASIN definition.
  One citation was corrected on the way: `src/data/compliance.json` S13 had a
  correct quote pointed at the 2009 Federal Register PDF that does not contain it
  (that PDF ends §255.5 at Example 9); it now cites the eCFR text where the
  sentence was re-fetched and matched verbatim. The FSIS host was retried and is
  still unreachable from this environment — no food-safety claim depends on it
  because the chart in the thermometer guide is transcribed from the chart page
  that did resolve (SRC-08).
- **Intent record.** `products.json` now stores `intended_listing_url`,
  `intended_confirmed_on` and `intent_source` as null fields beside
  `intended_asin`, with `meta.intent_rule`: they stay blank until the owner
  confirms each destination in the enrolled Associates account, and are never
  filled from the observed redirect.
- **Robots.** `robots.txt` now carries `Disallow: /archive/`; **FLG-027** records
  that a project-page robots.txt sits below the host root, so Search Console
  submission (Q-11 / S-03) is the required discovery step.
- **No number can drift.** The brief and about pages now count guides, questions,
  flags and image assets from the data at build time instead of hardcoding them.
- **Checks.** 31 pages, `check.py` 0 errors / 0 warnings, `check_local_links.py`
  0 broken references across 38 pages, `validate.py` 1603 checks / 0 warnings,
  build reproducible.
- **Duplicates dropped, not merged.** Earlier drafts of this pass carried their own
  cadence / consolidation / search / gate suggestions and question ids; main's
  S-12, S-15, Q-16 and Q-22 already hold those, so only genuinely new items were
  kept: Q-23 (market size), Q-24 (self-test budget) and FLG-027.

## Session addendum — arena/acb1e4c8-affil1 (2026-11-20)

This pass took the brief "lead with the products, not with the verification
process" literally and fixed the place where the site was failing it.

### What was wrong, precisely

The site was not short of care. It was short of a reason to click. Three
mechanical causes, each verified in the built HTML before being changed:

1. **The only call to action said "See listing source."** `_tools/layout.py`
   rewrote *every* untagged buy label beginning "See " or "Check " to that
   citation phrase. A citation verb on a buy button makes a shop read as an
   audit. Fixed at the source, so no template can reintroduce it.
2. **The comparison table carried two permanently empty columns.** Price and
   rating were blank by rule, and the page explained the rule at length. Correct,
   but a buyer cannot act on a blank cell. The columns now link to the live
   listing, and a second table sorts the five by *decision* instead of spec.
3. **The product page buried the decision.** It opened with an illustration
   caption ("not a photograph of P-01"), then a listing title. It now opens with
   the product, then a decision block: choose it if / check before you buy /
   what it costs you / where the price is.

### What was added

- `_src/data/decisions-registry.json` — one decision record per product, each
  naming the listing it rests on.
- `/decisions/` — the reviewable decision registry the brief asked for. Seven
  proposals, each with the official document and verbatim quote it is checked
  against, the single missing fact, its owner, and an accept/hold/reject control
  that writes to the browser only.

### What was deliberately not changed

The Associates tag. `_tools/paid_link_gate.py` and `test_paid_link_gate.py` still
assert that the approved register is **empty**, and every buy destination is
built by `buy_url()`, which returns a tagged URL only for an account-issued
Special Link. Putting `?tag=shopnow047c-20` on a URL rebuilt from a redirect
observation would be a link this project invented; Program Policies 2(a)–(b)
require Special Links to be the account's own. That stays blocked until the owner
generates them in Associates Central — it is row **D-01** on `/decisions/`.

### Merge with main, and the cart-link bypass this closed

While this branch worked, `origin/main` advanced 356 commits and then 4 more. Both
were merged in (never rebased, so no other session's history was rewritten). The
generated HTML conflicted in 30 files and was resolved by **rebuilding from the
merged sources**, not by hand-editing output.

The second merge mattered beyond bookkeeping. Main had added `_tools/cta.py`, which
rendered an "Add to basket" cart permalink for every product and appended the
Associates tag to a URL this project built itself. That bypasses `buy_url()`, the
single gate every other Amazon link goes through, and it is precisely what
`paid_link_gate.py` exists to prevent: Program Policies 2(a)–(b) require the
account's *own* Special Links, not a tag added to a redirect observation.

Main also logged it independently as **FLG-029**. The two changes are
complementary — main wrote the flag, this branch closed the defect — so the merge
was clean. `cta.pair()` now renders in three states:

1. **Cart door**, only when `paid_link_gate` holds an account-approved Special Link
   for that ASIN.
2. **Listing door** otherwise: the primary button becomes the official listing for
   the observed ASIN via `buy_url()` — permitted, still `rel="sponsored nofollow
   noopener"`, labelled "Live price and stock" — with one quiet line explaining why
   there is no one-click basket.
3. **Never** a synthesised tag.

No published page contains a `cart/add.html` URL. `_tools/test_cta_gate.py` asserts
all three states, including that a permitted listing never degrades to a dead
"withheld" notice. FLG-029 now carries a resolution and a "resolved in code" pill on
`/review/`, because a closed flag that still reads as open on the page a reviewer
trusts is its own defect.

### Verification run on this branch (all green, 2026-11-20)

| Gate | Command | Result |
|---|---|---|
| Build | `python3 _tools/build.py` | 35 pages, no errors |
| Static checks | `python3 _tools/check.py` | 35 pages, 0 errors, 0 warnings |
| Relative links | `python3 _tools/check_local_links.py` | 69 pages, 0 broken |
| Paid-link + cart gate | `python3 -m unittest discover -s _tools -p 'test_*.py'` | 10 tests, OK |
| Pre-publish | `python3 _tools/validate.py` | 1957 checks, 0 warnings |
| Decision Desk | `python3 _decision-support/validate.py` | PASS, 6 check families |
| Almanac edition | `python3 _platform/verify_edition.py` | 1965 line checks, 0 errors |
| Single surface | `python3 _tools/sweep_surfaces.py --dry-run` | 0 files moved |
| Reproducible | rebuild and `diff -r` | zero drift |
| Stage | `python3 _tools/stage.py _site` | 87 files, 35 pages |

Sources re-read for this pass: [Associates Program
Policies](https://affiliate-program.amazon.com/help/operating/policies) (Participation
Requirements 2(a)–(b): tag as a URL parameter; price and availability only when
Amazon serves the data or via Creators/PA API), [Google: qualify outbound
links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)
(`rel="sponsored"` for paid links).

The five `/dp/` listing pages were read directly on 2026-11-20 —
[B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3),
[B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R),
[B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH),
[B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5),
[B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z) — and each page title matched the
title already transcribed in `_src/data/products.json`. That is a title check, not a
redirect check: the supplied short links were not re-followed this pass, so it does
**not** establish where they redirect, confirm the operator's intended ASIN, or
confirm attribution. FLG-002, FLG-003 and FLG-018 remain open. The five observations
are appended to `_data/verification-observations.ndjson` with that limitation stated
in each row.

Nothing in the new copy states a price, rating, review count, stock level, test
result or ranking. The listing pages carried prices and ratings while being read
($74.99-tier figures, 4.4-star bands); none were copied, by rule and by check.

## Session addendum — arena/b990bce7-affil1 (2026-11-20, 06:40 UTC)

Reader-polish and accuracy pass, re-based onto `3d2a453` after four concurrent
merges. Five things were wrong, unreachable or missing.

**1. The site described its own links wrongly.** Every guide sidebar said the
product links carried "the site's Amazon tag", and every product page printed
"tag shopnow047c-20" under the buy button. No published URL carries a tag: the
paid-link gate holds no account-confirmed Special Link, so all five destinations
are the plain listing. Both now derive from the register and say the true thing —
plain listing, no tag, a click is not yet credited — and `_tools/check.py` fails
the build if copy and register disagree in either direction (FLG-031).

**2. A second complete edition was indexable.** `edition/` ships more than twenty
pages with self-referencing canonicals under `/Affil1/edition/` and carried no
robots instruction, so two copies of the same five products were both indexable.
Every edition page now carries `noindex, follow` (FLG-030); the maintained root is
the only indexable surface, which is what the About page already claimed.

**3. The masthead carried the desk.** The top bar included "What's left" and
"Decisions" — the project's to-do list and its decision register, both added by
concurrent merges during this pass. The masthead is now Shop · Guides · Compare ·
Find your fit, every desk page stays one click away in the footer, and a check
fails if a desk surface returns to the nav or a footer link loses its page.

**4. The supplied short links returned the Amazon home page, again.** Requested at
06:40 UTC with redirects followed, all five landed on `https://www.amazon.com/`
and none on a product. Main's FLG-028 records the same result from another
session; this pass appends its own timestamped record rather than renumbering.
All five destination listings were then requested directly and all five titles
matched the register (every arrival carried FLG-018's `plpRedirect=mhFallback`
marker, which is why no mapping is called confirmed).

**5. Counts had drifted.** Copy said eight and nine guides; there are ten.

**Added for the reader.** A printable counter-fit worksheet on `/fit/`: two empty
tables, one for the space you have against what the manual requires and one for
what you cook against what fits, with a print stylesheet and an explicit note that
nothing is pre-filled because no dimension on this site came from an official
specification sheet. The Guides index links to it. Article measure and body size
were raised, and a correction that contradicts an earlier record is now marked
where it appears rather than only in the register.

**Sources re-read:** Associates Operating Agreement §1 and §5 (2025-10-15),
Program Policies and the Commission Income Statement (2026-04-14), FTC
Endorsement Guides. SRC-18..SRC-20 added; the one carrying a verbatim quote has it
re-copied from the live page, and the two that do not are linked without one.

**Gates:** 35 pages, `check.py` 0/0, `validate.py` 1,909 checks 0 warnings,
`check_local_links.py` 0 broken, paid-link tests 6/6, `verify_edition.py` 1,965
checks, build reproducible.

**Still unverifiable, and still the whole story:** whether `shopnow047c-20` is
active and lists this site, which ASIN each product was meant to be, and whether a
click is credited. All three are read-only steps inside an Associates account.
