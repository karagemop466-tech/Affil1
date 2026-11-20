/* Product-intent confirmation records.
 *
 * One record per user-submitted link. Fields are deliberately kept separate:
 *   intendedAsin   - identifier parsed from the submitted short link (Amazon's ASIN
 *                    definition is the checkable identifier; it is NOT confirmed here)
 *   officialListingUrl - official Amazon listing URL, confirmed in the enrolled
 *                    Associates workflow. Left blank until confirmed.
 *   confirmationDate / confirmationSource - when and where the listing was confirmed.
 *   observedRedirectTarget - destination actually observed when the link was followed.
 *                    Kept in a separate field and never merged with officialListingUrl.
 *
 * Every record below is UNVERIFIED: the sandbox cannot reach amazon.com, so no ASIN,
 * listing, price, feature, review, commission, redirect destination or tracking
 * behavior has been independently confirmed. Blank values are left blank on purpose;
 * they are flagged for manual review against official Amazon sources.
 */
window.PRODUCTS = [
  {
    id: 1,
    submitted: 'https://link.amazon/B04G1MEwY',
    intendedAsin: 'B04G1MEwY',
    officialListingUrl: '',
    confirmationDate: '',
    confirmationSource: '',
    observedRedirectTarget: '',
    status: 'unverified',
    note: 'Intended identifier parsed from submitted short link. Confirm ASIN and official listing in the enrolled Associates workflow; test one link per product before scaling.'
  },
  {
    id: 2,
    submitted: 'https://link.amazon/B02NbDxp3',
    intendedAsin: 'B02NbDxp3',
    officialListingUrl: '',
    confirmationDate: '',
    confirmationSource: '',
    observedRedirectTarget: '',
    status: 'unverified',
    note: 'Intended identifier parsed from submitted short link. Confirm ASIN and official listing in the enrolled Associates workflow; test one link per product before scaling.'
  },
  {
    id: 3,
    submitted: 'https://link.amazon/B00hJ57DV',
    intendedAsin: 'B00hJ57DV',
    officialListingUrl: '',
    confirmationDate: '',
    confirmationSource: '',
    observedRedirectTarget: '',
    status: 'unverified',
    note: 'Intended identifier parsed from submitted short link. Confirm ASIN and official listing in the enrolled Associates workflow; test one link per product before scaling.'
  },
  {
    id: 4,
    submitted: 'https://link.amazon/B0c8moW59',
    intendedAsin: 'B0c8moW59',
    officialListingUrl: '',
    confirmationDate: '',
    confirmationSource: '',
    observedRedirectTarget: '',
    status: 'unverified',
    note: 'Intended identifier parsed from submitted short link. Confirm ASIN and official listing in the enrolled Associates workflow; test one link per product before scaling.'
  },
  {
    id: 5,
    submitted: 'https://link.amazon/B0f3GKalj',
    intendedAsin: 'B0f3GKalj',
    officialListingUrl: '',
    confirmationDate: '',
    confirmationSource: '',
    observedRedirectTarget: '',
    status: 'unverified',
    note: 'Intended identifier parsed from submitted short link. Confirm ASIN and official listing in the enrolled Associates workflow; test one link per product before scaling.'
  }
];
