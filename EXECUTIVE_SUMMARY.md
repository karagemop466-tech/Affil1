# Executive summary

**Publication:** [Crisp & Counter](https://karagemop466-tech.github.io/Affil1/) · **Tracking ID supplied:** `shopnow047c-20` · **Checked:** 20 November 2026

The buyer-facing publication presents three air fryers and two meat thermometers, with product records, comparisons and question-shaped guides. The [suggestions queue](https://karagemop466-tech.github.io/Affil1/suggestions/) and [open questions](https://karagemop466-tech.github.io/Affil1/questions/) separate proposals from missing evidence; [Flagged for Review](https://karagemop466-tech.github.io/Affil1/review/) records unresolved issues.

## Observed destinations, not confirmed intent

All five submitted short links reached Amazon listings in a page-fetch check on 20 November 2026. P-04 first returned a checkpoint and resolved on a later attempt; the reason for the checkpoint is unknown. A parallel session reported the P-04 and P-05 destinations reversed, so their mapping is disputed (FLG-016); a repeated fetch in this session produced the mapping below. Observed destinations are not proof of the product originally intended. No intended ASIN, intended listing URL, intent-confirmation date or source has been confirmed.

| Ref | Submitted official link | Observed official listing | Intended ASIN |
|---|---|---|---|
| P-01 | https://link.amazon/B04G1MEwY | https://www.amazon.com/dp/B0CDY277D3 | |
| P-02 | https://link.amazon/B02NbDxp3 | https://www.amazon.com/dp/B09B7SB46R | |
| P-03 | https://link.amazon/B00hJ57DV | https://www.amazon.com/dp/B08DKYBTPH | |
| P-04 | https://link.amazon/B0c8moW59 | https://www.amazon.com/dp/B0DHZTCNR5 | |
| P-05 | https://link.amazon/B0f3GKalj | https://www.amazon.com/dp/B0DZFD6R9Z | |

No product has been tested; illustrations are not product photographs. Prices, ratings and commission rates are not published. Check the [Amazon policies](https://affiliate-program.amazon.com/help/operating/policies) before adding product data.

## What remains unverified

- Attribution and Special Link status are **unconfirmed**. The supplied short links are not declared invalid. One test per product in the enrolled Associates workflow, followed by a report check, is needed before scaling.
- Analytics events are specified, but the maintained publication's collector is **not deployed or enabled**. GitHub Pages is static hosting; a separate properly configured service and a privacy/consent decision are needed. No traffic, conversion or revenue figures are claimed.
- Search Console ownership verification and sitemap submission have not been confirmed. The sitemap and feed exist, but do not guarantee indexing or rankings.
- An author identity, permitted live data access and genuine product testing remain open. The empty campaign ledger must only be populated from dated, authorized first-party reports.

## Compliance and publication

The publication places the Associates disclosure beneath the masthead and in the footer and marks product links sponsored. Review [Amazon's Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement), [Program Policies](https://affiliate-program.amazon.com/help/operating/policies), and [FTC guidance](https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) before publishing changes. Automated checks do not substitute for account verification or legal review.

## Session addendum — arena/ac649871-affil1 (2026-11-20)

### Independent verification pass (live fetches, this session)
Re-fetched all five submitted short links independently:

| Ref | Submitted link | This session's observation | Status here |
|---|---|---|---|
| P-01 | https://link.amazon/B04G1MEwY | dp/B0CDY277D3 — CHEFMAN 6 Quart Dual Basket Air Fryer Oven (Black) | Verified |
| P-02 | https://link.amazon/B02NbDxp3 | dp/B09B7SB46R — Emeril Lagasse 26QT French Door Air Fryer Toaster Oven | Verified |
| P-03 | https://link.amazon/B00hJ57DV | dp/B08DKYBTPH — Chefman Air Fryer 8 Qt TurboFry 4-in-1 (Stainless Steel) | Verified (earlier homepage observation preserved as transient) |
| P-04 | https://link.amazon/B0c8moW59 | Checkpoint-gated twice; candidate destination dp/B0DHZTCNR5 (ThermoMaven 1 Sec Digital Meat Thermometer, observed by the PR #27 session) confirmed live by direct page check | Unverified — identity disputed (FLG-016) |
| P-05 | https://link.amazon/B0f3GKalj | dp/B0DZFD6R9Z — CHEF iQ Sense Smart Wireless Meat Thermometer (Gen3) | Verified (earlier homepage observation preserved as transient) |

New objective check: every submitted slug is 9 characters while Amazon ASINs are 10-character
identifiers (SP-API Catalog Items reference) — slugs are recorded as opaque tokens, never as
ASINs (FLG-001). The full machine-readable register (schema v2, with per-record history and
disputed-observation preservation) is `data/confirmations.json`.

### The notes edition (`/notes/`)
This session ships a self-contained, hand-authored reader-facing publication at `notes/`:
shop-style front page leading with the verified shortlist, seven question-first buyer guides
(including a seasonal holiday-counter-math guide), the decision desk (`notes/suggestions.html`
suggestions queue with decision gates; `notes/questions.html` pre-decision questions), and the
transparency desk (`notes/notes/flagged-for-review.html`). It carries the Associates disclosure
above the fold, marks every outbound product link `rel="nofollow sponsored"` with the
`shopnow047c-20` tag, and includes its own sitemap and feed. It is deliberately foreign to the
root build so parallel rebuilds cannot wipe it; see `notes/README.md`.

### Requests to the integration owner (logged, not edited cross-scope)
1. Link the notes edition from the generated root navigation (`notes/`) and append its URLs
   (`notes/…`) to the generated root sitemap/feed — `notes/sitemap.xml` and `notes/feed.xml`
   exist meanwhile.
2. Settle the FLG-016 mapping dispute for P-04 in the enrolled Associates workflow, then unify
   the root and notes registers.
