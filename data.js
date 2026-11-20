/* Product-intent confirmation records — reconciled 2026-11-20 by arena/4772a1e3-affil1.
   Intended ASIN is UNKNOWN for all five submitted links: the submitted codes are
   9-character short-link slugs, not ASINs (Amazon defines an ASIN as a 10-character
   alphanumeric code; source fetched 2026-11-20, sell.amazon.com/blog/what-is-an-asin).
   The submitter's intent is never inferred. Observed redirect targets (pass 2,
   2026-11-20T05:15–05:22Z) are stored separately from pass-1 records
   (data/confirmations.json) and the two passes are NEVER merged. Where they disagree,
   the disagreement is shown (see reviews/verification-audit.html).
   authoritative narrative: data/confirmations.json (pass 1) + data/verification-audit.json (pass 2). */
window.PRODUCTS = [
  {
    id: 1,
    submitted: 'https://link.amazon/B04G1MEwY',
    submittedCode: 'B04G1MEwY',
    intendedAsin: '',
    observedTarget: 'https://www.amazon.com/dp/B0CDY277D3',
    observedAsin: 'B0CDY277D3',
    observationDate: '2026-11-20',
    passesAgreed: true,
    status: 'observed-listing',
    note: 'Pass 1 (confirmations.json conf-001) and pass 2 (audit OBS-1) both reached the CHEFMAN 6 Quart Dual Basket Air Fryer Oven listing. Identity unconfirmed pending Associates-workflow test.'
  },
  {
    id: 2,
    submitted: 'https://link.amazon/B02NbDxp3',
    submittedCode: 'B02NbDxp3',
    intendedAsin: '',
    observedTarget: 'https://www.amazon.com/dp/B09B7SB46R',
    observedAsin: 'B09B7SB46R',
    observationDate: '2026-11-20',
    passesAgreed: false,
    status: 'conflict-logged',
    note: 'Pass 2 (audit OBS-2) reached the Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven listing; pass 1 / FLG-005 recorded an unresolved/checkpoint outcome. Both recorded, never merged.'
  },
  {
    id: 3,
    submitted: 'https://link.amazon/B00hJ57DV',
    submittedCode: 'B00hJ57DV',
    intendedAsin: '',
    observedTarget: 'https://www.amazon.com/dp/B08DKYBTPH',
    observedAsin: 'B08DKYBTPH',
    observationDate: '2026-11-20',
    passesAgreed: false,
    status: 'conflict-logged',
    note: 'Pass 2 (audit OBS-3) reached the Chefman Air Fryer 8 Qt TurboFry listing; pass 1 (conf-003) recorded the Amazon homepage. Conflict logged as IR-2; never adjudicated here.'
  },
  {
    id: 4,
    submitted: 'https://link.amazon/B0c8moW59',
    submittedCode: 'B0c8moW59',
    intendedAsin: '',
    observedTarget: '',
    observedAsin: '',
    observationDate: '2026-11-20',
    passesAgreed: true,
    status: 'unresolved',
    note: 'Both passes reached the Amazon bot-checkpoint (/checkpoint/continue). No product page observed; identity unknown. Not a claim that the link is invalid (FLG-003).'
  },
  {
    id: 5,
    submitted: 'https://link.amazon/B0f3GKalj',
    submittedCode: 'B0f3GKalj',
    intendedAsin: '',
    observedTarget: 'https://www.amazon.com/dp/B0DZFD6R9Z',
    observedAsin: 'B0DZFD6R9Z',
    observationDate: '2026-11-20',
    passesAgreed: false,
    status: 'conflict-logged',
    note: 'Pass 2 (audit OBS-5) reached the CHEF iQ Sense wireless meat thermometer listing — not an air fryer (IR-5). Pass 1 (conf-005) recorded the Amazon homepage. Conflict logged as IR-2.'
  }
];

/* Campaign ledger — empty by design. Populate only from authorized first-party
   reports with a dated provenance trail. Fields: timestamp, source, channel,
   eligible sessions, clicks, reported orders. */
window.LEDGER = [];
