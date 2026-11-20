# Executive summary — Affil1 / Crisp & Counter

**What:** a live Amazon affiliate publication for air fryers and countertop cooking
appliances, tracking ID `shopnow047c-20` (supplied by the owner; enrolment unverified).
**Where:** https://karagemop466-tech.github.io/Affil1/
**When:** 2026-11-20. Integration passes by sessions `arena/359baa16-affil1`, `arena/62b049f0-affil1`
(counts and verification refresh) and `arena/10b5816b-affil1` (marketing & publication upgrade) —
both addenda at the end.
**Repo:** `karagemop466-tech/Affil1`, published from `main` by GitHub Actions.

## Read this first: the three facts that matter

An Amazon affiliate publication covering five supplied links: product research,
comparison content, buying guides, click measurement, compliant disclosure, a
suggestions section the owner can decide from, a clear list of questions that
must be answered before decisions, and a live site — built and merged without
further input.

## What exists now

One canonical site, 34 pages, rebuilt from `_src/data` on every deploy:

- a product-led front page with five picks in two categories and a buy button on
  every card;
- a product page for each of the five, with stated facts, who it suits, who
  should skip it, and a one-block provenance record;
- a side-by-side comparison table;
- ten question-shaped guides across six clusters;
- a decision register of 24 questions, 10 answered with evidence;
- a suggestion queue with three coherent paths and 21 proposals, of which 6 have
  already been implemented and are shown with evidence (15 open);
- an owner's "what is left" page (`/now/`), a ranked offers page (`/offers/`, 10
  weighted offers) and a per-page verification audit (`/verification/`);
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

- **10 buyer guides**, question-shaped and seasonal (holiday hosting, holiday sides,
  meal-prep Sunday, small-kitchen audit, dual-basket math, probe thermometers,
  capacity, cleanup, shape, multi-function claims), each closing by naming what it does not claim.
- **A shortlist of all five rows**, described only in the seller's own words, with a
  save-to-browser list (localStorage, nothing transmitted). Each row links only to the
  observed listing as a labelled reference link; P-04 is flagged (FLG-004, FLG-016) because
  its earlier attempts returned checkpoints and the thermometer pair was swapped in one record.
- **Topics/cluster pages** so the internal link graph is deliberate, and an editorial
  **queue** published in the open with the reason each candidate is there.
- **Registers, demoted to the footer where a buyer will not trip over them:** source
  register, flagged register (27 items, each with its source), suggestion board
  (21 proposals), open questions (24, 10 answered with evidence), operations ledger.
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

## Marketing & publication pass (2026-11-20, arena/10b5816b-affil1)

The brief for this pass: make the site read like a shop and a publication, not an
audit; lead with products; publish catchy, question-shaped seasonal content that
can earn organic traffic; and keep a reviewable decision board in front of any
change. What shipped:

- **Issue Nº 02, the holiday edit.** The front page now opens on a seasonal cover
  with a gift-edit feature and the Black Friday checklist, timed against the live
  shopping weekend (Amazon's own homepage was running its Black Friday Week event
  when this session fetched it — recorded as a dated observation, not a claim).
- **Four new question-shaped guides**, each built only from listing facts in the
  register: *Which air fryer gift fits which cook?*, *Black Friday air fryer
  deals: what should you check before you buy?*, *Is a wireless meat thermometer
  worth it?*, *Which air-fryer accessories will you actually use?*
- **Three new editorial illustrations** in the house engraving style, registered
  in the image register with prompts and alt text, labelled as illustrations.
- **Decision board extended**: S-22 (the seasonal issue, recorded as implemented
  with evidence), S-23..S-26 (editorial calendar from measured queries,
  comparison-page decision column, a single 'how we choose' page, and a
  fortnightly owner-question ritual). Every row stays unimplemented until the
  owner accepts it on /suggestions/.
- **Question register extended**: Q-23 (which queries actually arrive — blocked
  on Search Console), Q-24 (cadence and sign-off), Q-25 (do the seasonal modules
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
5. Answer Q-24 in one line: cadence, reviewer, and the sign-off rule.

Everything else — API access, custom domain, product photography, paid
acquisition — is sequenced behind those five and documented on /suggestions/.
