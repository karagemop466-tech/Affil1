/* Product-intent confirmation records.
   Intended ASIN is the identifier parsed from the user-submitted URL — it is kept
   separate from any observed redirect target. Verified entries are populated
   from official Amazon listing checks on 2026-11-20. Unverified entries remain
   blank and flagged. No values are inferred or filled in. */
window.PRODUCTS = [
  {
    id: 1,
    submitted: 'https://link.amazon/B04G1MEwY',
    intendedAsin: 'B04G1MEwY',
    officialListingUrl: 'https://www.amazon.com/dp/B0CDY277D3',
    confirmedDate: '2026-11-20',
    source: 'https://www.amazon.com/dp/B0CDY277D3',
    observedRedirect: 'B0CDY277D3',
    status: 'verified',
    note: 'Verified against Amazon.com official listing on 2026-11-20. Intended ASIN and observed redirect target are separate.'
  },
  {
    id: 2,
    submitted: 'https://link.amazon/B02NbDxp3',
    intendedAsin: 'B02NbDxp3',
    officialListingUrl: 'https://www.amazon.com/dp/B09B7SB46R',
    confirmedDate: '2026-11-20',
    source: 'https://www.amazon.com/dp/B09B7SB46R',
    observedRedirect: 'B09B7SB46R',
    status: 'verified',
    note: 'Verified against Amazon.com official listing on 2026-11-20. Intended ASIN and observed redirect target are separate.'
  },
  {
    id: 3,
    submitted: 'https://link.amazon/B00hJ57DV',
    intendedAsin: 'B00hJ57DV',
    officialListingUrl: '',
    confirmedDate: '',
    source: '',
    observedRedirect: '',
    status: 'unverified',
    note: 'Intended ASIN parsed from submitted URL path; destination, listing identity and tracking not confirmed. Homepage reached, no product page.'
  },
  {
    id: 4,
    submitted: 'https://link.amazon/B0c8moW59',
    intendedAsin: 'B0c8moW59',
    officialListingUrl: '',
    confirmedDate: '',
    source: '',
    observedRedirect: '',
    status: 'unverified',
    note: 'Intended ASIN parsed from submitted URL path; destination, listing identity and tracking not confirmed. Amazon checkpoint gate.'
  },
  {
    id: 5,
    submitted: 'https://link.amazon/B0f3GKalj',
    intendedAsin: 'B0f3GKalj',
    officialListingUrl: 'https://www.amazon.com/dp/B0DZFD6R9Z',
    confirmedDate: '2026-11-20',
    source: 'https://www.amazon.com/dp/B0DZFD6R9Z',
    observedRedirect: 'B0DZFD6R9Z',
    status: 'verified',
    note: 'Verified against Amazon.com official listing on 2026-11-20. Intended ASIN and observed redirect target are separate.'
  }
];

/* Campaign ledger — empty by design. Populate only from authorized first-party
   reports with a dated provenance trail. Fields: timestamp, source, channel,
   eligible sessions, clicks, reported orders. */
window.LEDGER = [];