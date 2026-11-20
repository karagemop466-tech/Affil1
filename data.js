/* ============================================================
   Product register — Good Measure Kitchen (Affil1)
   Session arena/ac649871-affil1, verification pass 2026-11-20.

   Rules encoded here:
   - `submitted` is the operator-supplied short link, preserved byte-for-byte.
   - The short-link slug is an opaque token, NOT assumed to be an ASIN
     (each slug is 9 characters; Amazon ASINs are 10-character identifiers —
     see https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v2022-04-01-reference).
   - `officialListingUrl` is the verified official Amazon listing reached via
     the submitted link (live fetch, 2026-11-20). Kept separate from
     `observedRedirect`, which records the exact final URL observed. The two
     fields are never merged.
   - `title` is the listing title exactly as served by amazon.com on the
     confirmed date. No prices, ratings, review counts or availability are
     stored: Associates policy requires Amazon-served or API-served data for
     display, and none is available to this build.
   - Tracking ID shopnow047c-20 is appended to outbound links per the
     Associates Special Link format; per-link tracking confirmation inside the
     enrolled Associates workflow is still pending and flagged for review.
   ============================================================ */

window.SITE = {
  brand: 'Good Measure Kitchen',
  trackingId: 'shopnow047c-20',
  verificationDate: '2026-11-20',
  disclosure: 'As an Amazon Associate I earn from qualifying purchases.'
};

window.PRODUCTS = [
  {
    id: 1,
    submitted: 'https://link.amazon/B04G1MEwY',
    status: 'verified',
    title: 'CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black',
    shortTitle: 'CHEFMAN 6 Quart Dual Basket Air Fryer Oven',
    category: 'Dual-basket format',
    img: 'assets/img/p1.jpg',
    alt: 'Illustration of a dual-basket air fryer with two pull-out baskets',
    blurb: 'Two independent 3-quart baskets and a digital control panel. The first question this format asks of you: do you regularly cook two things at once?',
    officialListingUrl: 'https://www.amazon.com/dp/B0CDY277D3',
    observedRedirect: 'https://www.amazon.com/dp/B0CDY277D3 (final URL as served after the submitted link resolved, 2026-11-20)',
    confirmedDate: '2026-11-20',
    source: 'https://www.amazon.com/dp/B0CDY277D3 (Amazon.com official listing page, title confirmed on fetch)',
    note: 'Destination confirmed live. Short-link slug B04G1MEwY is 9 characters and is treated as an opaque token, not an ASIN.'
  },
  {
    id: 2,
    submitted: 'https://link.amazon/B02NbDxp3',
    status: 'verified',
    title: 'Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included',
    shortTitle: 'Emeril Lagasse 26QT French Door Air Fryer Toaster Oven',
    category: 'Oven-style multi-function',
    img: 'assets/img/p2.jpg',
    alt: 'Illustration of a french-door countertop oven with glass doors',
    blurb: 'A large oven-style countertop cooker with french doors and a multi-function control set. The question to hold onto: could one appliance do the work of two on your counter?',
    officialListingUrl: 'https://www.amazon.com/dp/B09B7SB46R',
    observedRedirect: 'https://www.amazon.com/dp/B09B7SB46R (final URL as served after the submitted link resolved, 2026-11-20)',
    confirmedDate: '2026-11-20',
    source: 'https://www.amazon.com/dp/B09B7SB46R (Amazon.com official listing page, title confirmed on fetch)',
    note: 'Destination confirmed live. Short-link slug B02NbDxp3 is 9 characters and is treated as an opaque token, not an ASIN.'
  },
  {
    id: 3,
    submitted: 'https://link.amazon/B00hJ57DV',
    status: 'verified',
    title: 'Chefman Air Fryer 8 Qt | TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results | Bake, Dehydrate, Frozen | XL Nonstick Dishwasher-Safe Basket | Stainless Steel',
    shortTitle: 'Chefman TurboFry 8 Qt Air Fryer (4-in-1)',
    category: 'XL single basket',
    img: 'assets/img/p3.jpg',
    alt: 'Illustration of a single-basket stainless steel air fryer',
    blurb: 'A single extra-large basket with a compact control set. The useful check: measure your most common batch, then compare it to the basket geometry — not the headline number.',
    officialListingUrl: 'https://www.amazon.com/dp/B08DKYBTPH',
    observedRedirect: 'https://www.amazon.com/dp/B08DKYBTPH (final URL as served after the submitted link resolved, 2026-11-20)',
    confirmedDate: '2026-11-20',
    source: 'https://www.amazon.com/dp/B08DKYBTPH (Amazon.com official listing page, title confirmed on fetch)',
    note: 'Destination confirmed live on 2026-11-20. An earlier verification attempt on the same date reached the Amazon homepage instead; recorded as a transient redirect in the confirmation register. Short-link slug B00hJ57DV is 9 characters and is treated as an opaque token, not an ASIN.'
  },
  {
    id: 4,
    submitted: 'https://link.amazon/B0c8moW59',
    status: 'pending',
    title: '',
    shortTitle: 'Listing pending confirmation',
    category: 'Unconfirmed',
    img: 'assets/img/p4.jpg',
    alt: 'Illustration of an unopened parcel with a blank tag',
    blurb: 'This short link currently lands on Amazon\u2019s automated checkpoint page, so no listing could be confirmed. It stays in the review queue — not on the shelf.',
    officialListingUrl: '',
    observedRedirect: 'https://www.amazon.com/checkpoint/continue (bot-checkpoint interstitial; destination not reachable without an interactive click; observed on two fetches, 2026-11-20)',
    confirmedDate: '',
    source: '',
    note: 'Unverified, not invalid. Confirm in the enrolled Associates workflow (SiteStripe test-link step) before any promotion.'
  },
  {
    id: 5,
    submitted: 'https://link.amazon/B0f3GKalj',
    status: 'verified',
    title: 'CHEF iQ Sense | Smart Wireless Meat Thermometer | 3 Ultra-Thin Probes | WiFi Unlimited Range | 1000°F Heat Safe | 5 Sensors | BBQ, Grill, Oven, Smoker, Air Fryer | Gen3',
    shortTitle: 'CHEF iQ Sense Smart Wireless Meat Thermometer',
    category: 'Kitchen companion tool',
    img: 'assets/img/p5.jpg',
    alt: 'Illustration of a wireless meat thermometer with a charging base',
    blurb: 'A companion tool rather than a cooker: a wireless thermometer with multiple probes. The fitting question: does it slot into the setup you already have?',
    officialListingUrl: 'https://www.amazon.com/dp/B0DZFD6R9Z',
    observedRedirect: 'https://www.amazon.com/dp/B0DZFD6R9Z (final URL as served after the submitted link resolved, 2026-11-20)',
    confirmedDate: '2026-11-20',
    source: 'https://www.amazon.com/dp/B0DZFD6R9Z (Amazon.com official listing page, title confirmed on fetch)',
    note: 'Destination confirmed live. An earlier verification attempt on the same date reached the Amazon homepage instead; recorded as a transient redirect in the confirmation register. Short-link slug B0f3GKalj is 9 characters and is treated as an opaque token, not an ASIN.'
  }
];

/* Campaign ledger — empty by design. Populate only from authorized first-party
   reports with a dated provenance trail. Fields: timestamp, source, channel,
   eligible sessions, clicks, reported orders. No conversion score or revenue
   forecast is computed or displayed anywhere on this site. */
window.LEDGER = [];
