// Site configuration. One base URL, one brand, one navigation graph.
// Changing the canonical host is a one-line edit here (see Q-08).

export const site = {
  brand: "The Crisp Counter",
  shortBrand: "Crisp Counter",
  tagline: "Kitchen tools, chosen by what you actually cook.",
  desk: "the shopnow047c-20 desk",
  // Canonical base, no trailing slash.
  baseUrl: "https://karagemop466-tech.github.io/Affil1",
  tag: "shopnow047c-20",
  language: "en-US",
  season: {
    label: "Holiday season 2026",
    note: "Counter space gets tight and ovens get booked. The guides below are written for that week, not for a showroom.",
  },
  // S01 — exact wording, used verbatim, on every page.
  disclosure:
    "As an Amazon Associate I earn from qualifying purchases.",
  disclosureLong:
    "As an Amazon Associate I earn from qualifying purchases. Every outbound product link on this site is a sponsored affiliate link and is marked as such. Products are described from their Amazon listings; this site does not publish prices, star ratings, or review quotes, and does not claim hands-on testing.",
  affiliateNote:
    "We do not publish prices or star ratings. Amazon's Associates policies restrict both to data served by Amazon's own APIs, so each product page links straight to the live listing where the current price and rating are shown by Amazon.",
};

// Single navigation group in the masthead. Records live in the footer.
export const nav = [
  { label: "Shop", href: "/shop/", key: "shop" },
  { label: "Guides", href: "/guides/", key: "guides" },
  { label: "About", href: "/about/", key: "about" },
];

export const footerGroups = [
  {
    title: "Shop",
    links: [
      { label: "All products", href: "/shop/" },
      { label: "Air fryers", href: "/shop/#air-fryers" },
      { label: "Thermometers", href: "/shop/#thermometers" },
    ],
  },
  {
    title: "Guides",
    links: [
      { label: "All guides", href: "/guides/" },
      { label: "Basket vs. oven style", href: "/guides/basket-vs-oven-air-fryer/" },
      { label: "Capacity checklist", href: "/guides/air-fryer-capacity-checklist/" },
    ],
  },
  {
    title: "Records",
    links: [
      { label: "Record index", href: "/records/" },
      { label: "Source register", href: "/records/source-register/" },
      { label: "Product intent", href: "/records/product-intent/" },
      { label: "Compliance", href: "/records/compliance/" },
      { label: "Measurement", href: "/records/measurement/" },
      { label: "Campaign ledger", href: "/records/campaign-ledger/" },
      { label: "Open questions", href: "/records/questions/" },
      { label: "Suggestions", href: "/records/suggestions/" },
      { label: "Flagged for review", href: "/records/flagged/" },
    ],
  },
  {
    title: "About",
    links: [
      { label: "How this shop works", href: "/about/" },
      { label: "Executive summary", href: "/summary/" },
      { label: "RSS feed", href: "/feed.xml" },
    ],
  },
];
