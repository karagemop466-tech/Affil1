# Affil1 — Executive summary

**Project:** an Amazon Associates publication about countertop cooking appliances
**Live site:** https://karagemop466-tech.github.io/Affil1/
**Tracking ID supplied:** `shopnow047c-20`
**Session:** 2026-11-20
**Branch merged from:** `arena/47a393a2-affil1`

---

## 1. What this is, in one paragraph

A 25-page static publication built from `src/data/`, checked by a script that fails
the build on a broken link, an untagged Amazon link, a missing disclosure or a
reintroduced price. It leads with five products that were individually opened and
recorded, follows them with five question-shaped buying guides, and publishes its
own gaps rather than filling them: no prices, no ratings, no test results, no
named author and no revenue claim appear anywhere, because none of those could be
sourced.

## 2. The five supplied links, re-opened on 2026-11-20

| Ref | Submitted | Arrived at | What it is | Tag on arrival |
|---|---|---|---|---|
| P-01 | link.amazon/B04G1MEwY | `/dp/B0CDY277D3` | CHEFMAN 6 qt dual-basket air fryer | none |
| P-02 | link.amazon/B02NbDxp3 | `/dp/B09B7SB46R` | Emeril Lagasse 26 qt French-door air fryer oven | none |
| P-03 | link.amazon/B00hJ57DV | `/dp/B08DKYBTPH` | Chefman 8 qt TurboFry | none |
| P-04 | link.amazon/B0c8moW59 | `/dp/B0DHZTCNR5` | ThermoMaven instant-read thermometer | none |
| P-05 | link.amazon/B0f3GKalj | `/dp/B0DZFD6R9Z` | CHEF iQ Sense wireless thermometer | none |

All five resolved in this session. P-04 had failed three times in an earlier
session; it resolved on both attempts here, so its record keeps both outcomes.

## 3. The two findings that matter

**a. The buy links were not Special Links.** After the redirects were followed,
every arrival URL was a bare `/dp/<ASIN>` with no tag, and the site was offering
those addresses as click targets. Program Policies §2(b) requires the Associates
ID as a parameter in the URL of each link, and Amazon's own application-review page
lists untagged links among its reasons for rejection. The build now emits
`/dp/<ASIN>/?tag=shopnow047c-20`, keeps the submitted code as history, and fails if
an untagged retail link appears. **Attribution is still unproven** until one click
shows in the Associates report.

**b. Two of the five products are thermometers.** P-04 is an instant-read probe,
P-05 a wireless probe set. The catalogue is three air fryers and two thermometers,
in two different Amazon category paths. Every page that said otherwise was
corrected, and the pair got a guide of their own.

## 4. What was verified against an official source

| Source | What it settled |
|---|---|
| Associates Operating Agreement §5 | The exact required disclosure sentence, quoted verbatim |
| Associates Program Policies (updated 2026-04-14) §2(a)(b) | Special Links must carry the Associates ID as a URL parameter; price and availability only from Amazon-served data, Creators API or PA API |
| 16 CFR 255.0(f), via eCFR | "Clear and conspicuous" means difficult to miss; on the internet the disclosure should be unavoidable |
| Amazon Associates help, application review | Three qualifying sales within 180 days; robust original content, ten posts as a rule of thumb; untagged links are a stated rejection reason |
| Sell on Amazon, ASIN guide | An ASIN is a unique 10-character alphanumeric code, found after `/dp/` |
| Google Search Central, outbound links (updated 2025-12-10) | `rel="sponsored"` marks paid placements |

Full quotes, with the date each was read, are on `/about/#sources`; the pass itself
is logged row by row on `/review/verification.html`.

## 5. What the site now contains

| Surface | Status |
|---|---|
| Front page | Products first, method second; dated change log; two thermometers in their own band |
| Product register and five records | All five identified; intended ASIN, observed ASIN and tagged link are three separate fields |
| Guides | Five, including the new instant-read vs wireless thermometer guide |
| Compare | Every product side by side, with blanks left blank |
| Questions | 15 research questions, 6 answered with a source |
| Before you decide | **New.** 16 decisions in four ordered gates: what is known, what is missing, who can supply it, what artefact closes it |
| Suggestions | **Rebuilt.** 20 proposals inside three coherent paths, each with impact, effort, risk, reversibility and the decision it depends on |
| Review queue | 17 flags, severity-ordered, with closed flags kept rather than deleted |
| Verification log | **New.** 5 links, 7 sources, 9 findings from this pass |
| Image policy, measurement plan, ledger | Unchanged in substance: illustrations are labelled; analytics is inert; the ledger is empty and says why |

## 6. What is deliberately absent

- **Prices, ratings, review counts, stock.** No permitted data source is connected.
- **Test results and rankings.** Nothing was bought or used, so nothing is scored.
- **A named author.** No name would be true.
- **Traffic and revenue figures.** No analytics endpoint, no Search Console
  property, no commission rate read. No forecast is presented anywhere.
- **A sixth AI-written guide.** S-11 recommends against it until a test or real
  query data exists.

## 7. The next three actions, in order

1. **Click one tagged link and read the Associates click report.** Ten minutes.
   This closes the highest-severity flag and is the only thing between a finished
   publication and an earning one.
2. **Confirm the account state and the intended ASIN for each link** (D-02, D-03).
   Both need account access, which this session does not have.
3. **Pick a path, not a page.** Path A proves the click. Path B publishes to
   measured queries once Search Console is verified. Path C buys one appliance and
   tests it, which is the only route to a page a competitor cannot copy.

Everything a reviewer needs to disagree with is written down, with its source, on
`/questions/decisions.html` and `/review/verification.html`.
