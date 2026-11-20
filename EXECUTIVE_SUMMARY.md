# Executive summary — Affil1 / Crisp & Counter

**What:** a live Amazon affiliate publication for air fryers and countertop cooking
appliances, tracking ID `shopnow047c-20` (supplied by the owner; enrolment unverified).
**Where:** https://karagemop466-tech.github.io/Affil1/
**Latest pass:** 2026-11-20, marketing & publication upgrade, session `arena/10b5816b-affil1` (addendum at the end).
**When:** 2026-11-20, integration pass by session `arena/359baa16-affil1`; counts and
verification refreshed 2026-11-20 by session `arena/62b049f0-affil1`; buyer-decision
pass by session `arena/05771edb-affil1` (each addendum at the end of this file).
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
- eleven question-shaped guides across six clusters, all in `sitemap.xml` and
  `feed.xml` (one added 2026-11-20: reheating Thanksgiving leftovers, built from
  USDA FSIS and FoodSafety.gov pages fetched that day);
- a decision register of 24 questions, 10 answered with evidence and 4 that block
  other work until they are answered;
- a suggestion queue with three coherent paths and 24 proposals (18 open, 6 already
  implemented and shown with evidence), each row carrying cost, risk and the question
  it depends on;

- nineteen question-shaped guides across six clusters, all in `sitemap.xml` and
  `feed.xml`, plus a category index and two category pages;
- a decision register of 27 questions, 10 answered with evidence, 17 open and each
   naming the document or dashboard that would close it;
- a suggestion queue with three coherent paths and 31 proposals, of which some
  are already implemented and are shown with evidence;
- an owner's "what is left" page (`/now/`), a ranked offers page (`/offers/`, 10
  weighted offers) and a per-page verification audit (`/verification/`);
- a **decision registry** (`/decisions/`) of 7 open proposals, each carrying the
  official source and verbatim quote it is checked against, the single missing
  fact, the person who can close it, and an accept/hold/reject control recorded
  in the browser only;
- 35 review flags, an image policy, an inert analytics client and an empty
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

- **14 buyer guides**, question-shaped and seasonal, across seven clusters — basket or oven,
  dual-zone vs single basket, capacity, cleanup and counter space, meal-prep Sunday, the
  small-kitchen space audit, multi-function questions, thermometer pairing, holiday hosting
  and holiday side-dish capacity, plus four added on 2026-11-20: Thanksgiving oven-traffic
  timing, reheating leftovers, thermometer probe placement and the two-hour rule. The four
  newest carry a table whose rows link to the federal page each figure was read from. Each
  guide closes by naming what it does not claim.
- **A shortlist of all five rows**, described only in the seller's own words, each linking
  only to its observed listing as a labelled reference link. P-04 is flagged (FLG-004,
  FLG-016) because earlier attempts returned checkpoints and the thermometer pair was
  swapped in one record; it is presented as a thermometer, not a fourth air fryer.
- **Topics/cluster pages** so the internal link graph is deliberate, and an editorial
  **queue** published in the open with the reason each candidate is there.
- **Registers, demoted to the footer where a buyer will not trip over them:** source
  register, flagged register (29 items, each with its source), suggestion board
  (24 proposals), open questions (24, 10 answered with evidence; 14 still blocked and

  register, flagged register (35 items, each with its source), suggestion board
  (31 proposals), open questions (27, 10 answered with evidence; 17 still blocked and
  published as such), decision registry (7 proposals), operations ledger.
- **Two category subpages** (`/categories/air-fryers/`, `/categories/thermometers/`) under a
  category index, so the URL a shopper lands on is organised by what they are buying rather
  than by the register's reference numbers.
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
| FLG-004 | P-04 failed three times, then resolved; later observations disagree on which product it is | The P-04 identity rests on one disputed observation |
| FLG-023 | Four recorded passes for P-04 saw only the bot interstitial | A single observation is not a settled identity |
| FLG-025 | Open reading: may plain listing links stay untagged before a Special Link is validated | A policy interpretation the site cannot make for itself |
| FLG-026 | P-01 short link returned the Amazon homepage on a 2026-11-20 fetch | Superseded by FLG-028, which found this for all five |
| **FLG-028** | **All five short links returned the Amazon homepage, found independently by two sessions** | **The link form is unstable; it is not used as any destination on the site** |
| FLG-029 | The 'Add to basket' links carry no tag and are not Special Links | Until an account-issued Special Link exists, no cart click can be attributed |

> **Correction made in this pass.** Three rows of this table previously carried the wrong
> flag IDs: a fallback-URL observation was attributed to FLG-018, a blank-specification
> observation to FLG-007, and an archived-register contradiction to FLG-014. Those IDs now
> belong to different findings (buy-button wording, AI illustrations and the empty ledger
> respectively). The rows above have been rewritten to match the flags they actually cite.
> The discrepancy was found by comparing each ID with its title in `_src/data/flags.json`.

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

## Latest pass — arena/05771edb-affil1 (2026-11-20)

This pass changed two things that were wrong and three that were missing. It did not
restyle the site and did not add a guide.

### 1. The five supplied short links reached no product — a second, independent confirmation

Each was requested once, in order, and followed. **All five returned
`https://www.amazon.com/`** — title *"Amazon.com. Spend less. Smile more."* — not a `/dp/`
listing. None carried `tag=shopnow047c-20`, because none arrived at a product page.

This duplicates, and so corroborates, **FLG-028**, which session `arena/bcd93318-affil1`
raised independently on the same day. Two sessions, two passes, same result. That flag is
the published record; this section adds the one thing it did not cover — all five direct
`/dp/` URLs were re-opened here and every title matched, including P-02 and P-03, which the
first pass did not re-check.

The finding is that the link form is **unstable**, which is the fifth distinct arrival
behaviour recorded for this same set of links across sessions: a product listing, the
Amazon homepage, and a `/checkpoint/continue` interstitial. It is *not* a claim that the
links are invalid or non-compliant; that question stays open in FLG-003 and is not decided
here, and no observed field was changed on the strength of any single fetch.

**Nothing on the site depended on them.** Every buy button already points at the direct
`/dp/` URL. All five direct URLs were re-opened in this pass and each returned a live
product page whose `<title>` matched the recorded `listing_title` verbatim:

| Ref | Direct destination re-verified 2026-11-20 | Capacity as stated in the data |
|---|---|---|
| P-01 | `amazon.com/dp/B0CDY277D3` — CHEFMAN 6 Quart Dual Basket Air Fryer Oven | 6 qt, as two 3-qt baskets |
| P-02 | `amazon.com/dp/B09B7SB46R` — Emeril Lagasse 26QT French Door Air Fryer Toaster Oven | 26 qt |
| P-03 | `amazon.com/dp/B08DKYBTPH` — Chefman Air Fryer 8 Qt TurboFry 4-in-1 | 8 qt |
| P-04 | `amazon.com/dp/B0DHZTCNR5` — ThermoMaven 1 Sec Professional Digital Meat Thermometer | n/a (thermometer) |
| P-05 | `amazon.com/dp/B0DZFD6R9Z` — CHEF iQ Sense Smart Wireless Meat Thermometer, 3 probes | n/a (thermometer) |

No price, rating, review count, stock level or availability figure was recorded, here or
on the site, because Program Policies §2(b) permits those only from an Amazon-served feed
and none is connected. `intended_asin`, `official_listing_url`, `confirmation_date`,
`confirmation_source`, `approved_special_link` and `tracking_report_reference` all remain
`null`: an observation of where a link lands cannot fill an intent field. A dated
`observation_trail` was added to `_src/data/products.json` so the passes are visible side
by side rather than averaged into one claim.

### 2. A second 27-page site was telling crawlers to index it

`edition/` (the "Countertop Almanac") is served from the same branch root. It shipped with
its own `robots.txt` saying `Allow: /`, its own `sitemap.xml`, and **no `noindex` on any of
its 27 pages** — a complete second publication competing with the canonical one for the
same five product pages. That is the exact condition the "one site to index" rule exists
to prevent, and it arrived after the earlier consolidation.

Fixed without deleting anything: every `edition/` page now carries `noindex, follow`, its
`robots.txt` is `Disallow: /`, and `_tools/check.py` gained `check_one_indexable_site()`.
The new rule is a rule, not a list of directory names: it finds any `robots.txt` below the
root and fails the build if that surface permits a crawl or if any of its pages lacks
`noindex`. Negative-tested by temporarily restoring `Allow: /`, confirming the build
fails, then restoring the fix.

### 3. What was missing, and is now on the site

- **Three new decision rows** on `/suggestions/`, each with cost, risk and dependency:
  S-22 (never publish a short link as a buy destination — current behaviour, made a
  standing rule), S-23 (give each product a five-minute check the reader can run in the
  shop, the cheapest genuinely useful content change left), S-24 (decide what `edition/`
  is for).
- **Two questions refreshed** rather than answered: Q-01 and Q-02 now state both arrival
  behaviours instead of the flattering one.
- **FLG-008 reopened** in a narrower, accurate form; **FLG-026 marked superseded** by
  FLG-028 because it described a one-link finding that is now a five-link one; and a
  `corroborated_by` note added to FLG-028 recording the second independent pass.

### 4. Gates after this pass

`_tools/build.py` 34 pages · `_tools/check.py` **0 errors, 0 warnings** ·
`_tools/validate.py` **1814 checks, 0 warnings** · `_tools/check_local_links.py` **0 broken
references across 68 pages** · `_decision-support/validate.py` PASS ·
`_platform/verify_edition.py` **1965 checks, 0 errors** · paid-link gate **6/6 tests pass**
· rebuild **reproducible, zero drift**.

### 5. What this pass could not do, and will not pretend to

No Associates report was read, so **no click, order or commission is attributed** to
`shopnow047c-20` and no revenue figure appears anywhere. Search Console is not connected,
so no traffic or query is claimed. No product was tested, so no page says one was. Those
three gaps need the account owner, and they sit at the top of the decision list above.

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

- `python3 _tools/build.py` — 29 pages at the time of that pass (34 after this one).
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
---

## Addendum — session `arena/d3f5a958-affil1`, 2026-11-20 (shop-polish & integration)

Current build after this session: **38 pages, 13 question-shaped guides, 32
review flags**. `_tools/check.py` 0 errors / 0 warnings; `_tools/validate.py`
2,158 checks pass; `_tools/sweep_surfaces.py` 0 stray surfaces;
`_platform/verify_edition.py` 1,965 checks pass; `_decision-support/validate.py`
PASS; the build is byte-identical on a second run.

1. **Three new question-shaped guides**, per the brief's cadence: *Air fryer for
   two: what size actually fits a two-person dinner?*, *Air fryer or toaster
   oven: which one earns the counter space?*, and *Cooking from frozen in an air
   fryer: what to check before you trust the packet* (two USDA FSIS source links
   rendered on the page). Facts limited to seller-stated listing wording; no
   product tested, nothing ranked. All three are in the sitemap and RSS feed.
2. **One site to index.** `edition/` (Countertop Almanac, added by PR #89 as a
   second publication for the same five products) is kept readable and gated
   but marked `noindex, follow`, and `robots.txt` disallows `/edition/`
   (FLG-032, with the written reversal path). The root publication — Crisp &
   Counter — is the single site in the root sitemap and feed.
3. **Recovered work:** the design-token pack and topic bank from session
   `76128338` were lost in the concurrent directory-rename merges and are
   restored, extended with topics T-11..T-16 and a State column that separates
   published guides from suggestions awaiting evidence.
4. **Findings ported:** FLG-030 (GitHub Pages has two configured publishers —
   verified first-hand via `gh api`) and FLG-031 (P-05 listing pages recorded
   as stating several different heat tolerances; carried forward with stated
   provenance, not re-verified; no figure published).

### What remains unverified (unchanged)

Attribution of clicks to `shopnow047c-20` (FLG-002), the intended ASINs behind
the five supplied short-link slugs (FLG-001, Q-01), price/rating availability
(FLG-022), a named author (FLG-006), Search Console and analytics hosting
(FLG-019), and the §2(b) tagging reading (FLG-025). All are published on the
review page with source links; none is inferred anywhere.

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

## Addendum — third-party pass, session `arena/d0594bc5-affil1` (2026-11-20)

An independent session re-ran the core verification rather than trusting the
board, and published its full receipt at
`_data/verification-observations/2026-11-20-arena-d0594bc5.md`. Results:

- **All five observed ASINs agree with the register.** Requesting
  `amazon.com/dp/{B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z}`
  directly returned product pages whose titles and breadcrumbs match
  `products.json` row for row (arrival under Amazon's `plpRedirect=mhFallback`
  fallback, recorded as the register requires). No price, rating or review count
  was recorded, per the site's standing rule.
- **All five submitted `link.amazon` URLs returned the Amazon homepage** in this
  pass — a third arrival class on the same date (earlier passes saw product
  pages and fetch errors). FLG-003 stays unresolved and nothing is claimed about
  the links' validity; the operational conclusion (only account-validated
  Special Links may carry the tag) is now proposal **S-30** on the decision queue.
- **Policy sources re-read firsthand:** Operating Agreement (updated 2026-10-15,
  §1 Special Links "tagged" formats) and Program Policies (Commission Income
  Statement §2(e) Redirecting Link, §2(g) properly formatted). FTC FAQ and the
  ASIN definition were verified firsthand earlier the same day by sessions
  recorded on the board; links for manual review are in the receipt.
- **Pages serving exposure confirmed, fix still owner-blocked.** This pass
  observed `PUBLISHING_WORKFLOW.md` serving HTTP 200 on the live host. The
  durable fix (flip Pages `build_type` to `workflow` so the staged 37-page
  edition is served) was pre-flighted clean — 86 files staged, 37 pages, every
  reference resolving — but the API call was refused to this environment
  (HTTP 403, no Pages write scope). Filed as proposal **S-29** with exact owner
  steps; ~20 stale open PRs are filed as proposal **S-31**.
- **Queue and gates.** The suggestions queue is now 28 rows (18 open, 10 implemented). In this pass (rebased onto main before merge): `check.py` 0 errors/0
  warnings, `validate.py` all checks pass, unit tests OK, local links 0 broken,
  edition verify 1965 checks pass.

## Marketing & publication pass (2026-11-20, arena/10b5816b-affil1)

The brief for this pass: make the site read like a shop and a publication, not an
audit; lead with products; publish catchy, question-shaped seasonal content that
can earn organic traffic; and keep a reviewable decision board in front of any
change. What shipped:

- **Issue Nº 02, the holiday edit.** The front page now opens on a seasonal cover
  with a gift-edit feature and the Black Friday checklist, timed against the live
  shopping weekend (Amazon's own homepage was running its Black Friday Week event
  when this session fetched it — recorded as a dated observation, not a claim).
- **Four new question-shaped guides** (the site now holds seventeen), each built only from listing facts in the
  register: *Which air fryer gift fits which cook?*, *Black Friday air fryer
  deals: what should you check before you buy?*, *Is a wireless meat thermometer
  worth it?*, *Which air-fryer accessories will you actually use?*
- **Three new editorial illustrations** in the house engraving style, registered
  in the image register with prompts and alt text, labelled as illustrations.
- **Decision board extended**: S-32 (the seasonal issue, recorded as implemented
  with evidence), S-33..S-36 (editorial calendar from measured queries,
  comparison-page decision column, a single 'how we choose' page, and a
  fortnightly owner-question ritual). Every row stays unimplemented until the
  owner accepts it on /suggestions/.
- **Question register extended**: Q-25 (which queries actually arrive — blocked
  on Search Console), Q-26 (cadence and sign-off), Q-27 (do the seasonal modules
  change clicks — blocked on measurement).
- **Third independent verification pass over the five supplied links**
  (obs-10b5816b). Result, recorded honestly: only P-05 reproduced its registered
  destination in this pass (B0DZFD6R9Z, CHEF iQ Sense); the other four landed on
  the Amazon homepage this time. That is consistent with the documented
  instability of these redirectors and with earlier archived observations; it
  does not refute the earlier successful arrivals, which remain dated
  observations. FLG-003 stance unchanged: the short links' compliance status is
  unresolved, not disproven.
- **Repository drift resolved, nothing discarded**: concurrent sessions renamed
  the working directories (`tools/` → `_tools/`, `src/` → `_src/`) and the
  observation log had ended up only in an archived copy. The two verification
  passes were restored to the active register verbatim and the incident logged on
  the coordination board.

### The owner checklist this pass leaves behind, in the order that pays

1. Click one buy link on the live site, then read Reports → Orders in Associates
   Central. That single check closes FLG-002 / Q-03 and is the only proof that
   the site can earn (S-01).
2. Verify Search Console and submit sitemap.xml. Every topic decision before
   that is instinct; after 28 days it is data (S-03, Q-23).
3. Choose a path on /suggestions/ (Shop first, Publication first, Measure first),
   then mark the rows. Nothing on that page has been implemented by anyone
   pressing a button.
4. Name an editor, or accept the honest desk-level byline (S-02).
5. Answer Q-26 in one line: cadence, reviewer, and the sign-off rule.

Everything else — API access, custom domain, product photography, paid
acquisition — is sequenced behind those five and documented on /suggestions/.

---

## Addendum — session `arena/ddb6772b-affil1`, 2026-11-20 UTC

Base `d345cf0`, rebased through `bcef8b6`. This pass changed the reader-facing
surface, the source registers, and one false sentence about attribution. It also
cut most of what it had drafted, because main had already published the better
version of it — that part is recorded here rather than quietly deleted.

**What shipped.** `/categories/` with an index and two subpages (Air fryers,
Thermometers): the same register regrouped by what a shopper is buying, every row
linked to the listing it was transcribed from, and an explicit statement of what the
page cannot tell you. `PUBLIC_DIRS` in `_tools/check.py` had already reserved
`categories`; nothing had ever written it. One guide was kept — probe placement, the
question no other page answered — with every figure transcribed from a US-government
page opened the same day and linked in the same table row. Three more drafted here
(reheating leftovers, the two-hour rule, Thanksgiving oven timing) were dropped on
rebase: main already publishes `reheating-thanksgiving-leftovers`, and
`holiday-hosting-air-fryer` already argues the last-twenty-minutes point. Two guides
making one argument is the duplication this project consolidated away at edition
scale, so the newer copy yielded. The front page's seasonal band and journal shelf are now derived from the
data rather than from fixed list indices, which every appending session invalidated.

**Registers.** Four new sources (SRC-21 FSIS Leftovers, SRC-22 FSIS Food
Thermometers, SRC-23 FSIS Turkey from Farm to Table, SRC-24 FoodSafety.gov chart,
each with the page's own date or an explicit "no date shown"), three new open
questions (Q-25, Q-26, Q-27), six new board proposals (S-26 to S-31) and two new
review flags (FLG-034, FLG-035).

**Not a new flag, a third corroboration.** Each of the five submitted
`link.amazon/<code>` links was fetched separately, redirects followed, by a fetcher
with no cookies and no region. All five returned the Amazon site homepage rather
than a listing; a direct fetch of the listing recorded for P-01 in the same session
matched the register title exactly. Four passes over the day, three different
answers. Nothing published uses a short link as a destination, so no reader is
affected; what is unproven is the hop from "the operator submitted this" to "this
page is about that product". This pass is recorded as a third corroboration inside
**FLG-028**, which already stated the finding, and as six dated rows in
`_data/verification-observations.ndjson`. It is not a finding that the links are
invalid: FLG-003 stays unresolved and the register still says so.

**Two sessions, one defect.** The guide sidebar sentence asserting that every
product link "carries the site's Amazon tag" was found and fixed here and,
independently, upstream (`FLG-031`, `S-22`). Upstream's flag and the `check.py` rule
that guards the sentence stand as the record. What this pass adds is that the
sentence is *computed* from `approved_amazon_urls()`
(`_tools/page_guides.py::_link_note`) rather than re-worded, so it cannot outlive the
register state; and **FLG-037** records that the guard is a literal-string test,
which will start demanding a false sentence the day a Special Link is validated.

**Gates after this pass, on the final tree:** 47 pages built twice, byte-identical ·
`check.py` 0 errors 0 warnings · `validate.py` 2,884 checks 0 warnings ·
`check_local_links.py` 81 pages 0 broken · paid-link tests OK · Decision Desk PASS ·
Almanac edition checks 0 errors · `sweep_surfaces.py` 0 to move · `stage.py` staging
complete · CI-style copy/rebuild/`diff -r` clean. No price,
rating, review count, stock level, test result or ranking was added; the listing page
read during verification displayed both, and neither was transcribed.
