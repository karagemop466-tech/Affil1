/* Product-intent confirmation records.
   Intended ASIN is the identifier parsed from the user-submitted URL — it is kept
   separate from any observed redirect target, and both remain blank/unverified
   until checked through the enrolled Amazon Associates workflow. No values are
   inferred or filled in. */
window.PRODUCTS = [
  {
    id: 1,
    submitted: 'https://link.amazon/B04G1MEwY',
    intendedAsin: 'B04G1MEwY',
    officialListingUrl: '',
    confirmedDate: '',
    source: '',
    observedRedirect: '',
    status: 'unverified',
    note: 'Intended ASIN parsed from submitted URL path; destination, listing identity and tracking not confirmed.'
  },
  {
    id: 2,
    submitted: 'https://link.amazon/B02NbDxp3',
    intendedAsin: 'B02NbDxp3',
    officialListingUrl: '',
    confirmedDate: '',
    source: '',
    observedRedirect: '',
    status: 'unverified',
    note: 'Intended ASIN parsed from submitted URL path; destination, listing identity and tracking not confirmed.'
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
    note: 'Intended ASIN parsed from submitted URL path; destination, listing identity and tracking not confirmed.'
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
    note: 'Intended ASIN parsed from submitted URL path; destination, listing identity and tracking not confirmed.'
  },
  {
    id: 5,
    submitted: 'https://link.amazon/B0f3GKalj',
    intendedAsin: 'B0f3GKalj',
    officialListingUrl: '',
    confirmedDate: '',
    source: '',
    observedRedirect: '',
    status: 'unverified',
    note: 'Intended ASIN parsed from submitted URL path; destination, listing identity and tracking not confirmed.'
  }
];

/* Campaign ledger — empty by design. Populate only from authorized first-party
   reports with a dated provenance trail. Fields: timestamp, source, channel,
   eligible sessions, clicks, reported orders. */
window.LEDGER = [];