// Product content. Buyer-facing copy, written from the observable listing facts
// (title, capacity, features stated on the listing). No price, no star rating,
// no review quote, no hands-on testing claim. See S04, S05, S19.
//
// No product images are used. Every image URL on an Amazon listing is Program
// Content with its own licensing rules, and none of them was supplied by the
// owner, so the design carries typographic cards instead.

import { site as siteCfg } from "../lib/site.mjs";

export const products = [
  {
    id: "P1",
    slug: "chefman-6-quart-dual-basket",
    name: "CHEFMAN 6 Quart Dual Basket Air Fryer",
    brand: "Chefman",
    category: "air-fryers",
    style: "Dual-basket",
    // Observed ASIN. NOT a confirmed intended ASIN. See data/product-intent.json.
    asin: "B0CDY277D3",
    asinStatus: "observed",
    listingTitle:
      "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black",
    hook: "Two baskets that finish at the same time, for the household that argues about fries.",
    oneLine:
      "A 6-quart air fryer split into two independent 3-quart baskets, with a sync-finish mode and viewing windows.",
    specs: [
      { label: "Stated capacity", value: "6 quarts total (two 3-quart baskets)" },
      { label: "Stated temperature range", value: "200–450°F" },
      { label: "Stated dimensions", value: "13.38\"D x 11.81\"W x 10.63\"H" },
      { label: "Basket coating", value: "Nonstick, dishwasher safe (per listing)" },
      { label: "Listed features", value: "Dual zone, sync finish, Hi-Fry, auto shut-off, viewing windows, mute" },
    ],
    bestFor: [
      "Two people eating different things at the same time",
      "Anyone who wants to look at the food without opening a basket",
      "Kitchens where a second appliance is not an option",
    ],
    thinkTwice: [
      "Each basket is 3 quarts. A whole chicken will not fit in one basket.",
      "It is a countertop footprint of roughly 13 by 12 inches, permanently.",
      "Two baskets means two things to wash, not one.",
    ],
    criteria: [
      {
        heading: "Sync finish, and why it is the whole point",
        body: "Dual-basket machines are not two air fryers in a trench coat; the useful feature is that the two baskets can be told to land at the same moment. Without sync, you are timing two cooks by hand. Check that the model you are looking at has it, because some dual-basket units do not.",
      },
      {
        heading: "Independent 3-quart zones versus one 6-quart basket",
        body: "Six quarts in one basket is better for a single large item. Six quarts split in two is better for two foods that need different temperatures or different times. These are different appliances that happen to share a number on the box, and the number is the least useful way to compare them.",
      },
      {
        heading: "The window matters more than it sounds",
        body: "Every time you open a basket to check, you drop the temperature and add time. A viewing window is a small feature that quietly changes how often you get the timing right.",
      },
    ],
    pairingGuide: "basket-vs-oven-air-fryer",
  },
  {
    id: "P2",
    slug: "emeril-lagasse-26qt-french-door",
    name: "Emeril Lagasse 26QT French Door Air Fryer Toaster Oven",
    brand: "Emeril Lagasse",
    category: "air-fryers",
    style: "Oven-style",
    asin: "B09B7SB46R",
    asinStatus: "observed",
    listingTitle:
      "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included",
    hook: "The one that replaces the toaster oven, if you have the counter for it.",
    oneLine:
      "A 26-quart French-door countertop oven with air-fry and convection modes, 24 presets, and six accessories in the box.",
    specs: [
      { label: "Stated capacity", value: "26 quarts (extra-large interior)" },
      { label: "Stated presets", value: "24 one-touch preset options" },
      { label: "Door style", value: "French door (two doors, opens outward)" },
      { label: "Stated modes", value: "Air fry, convection, toaster-oven functions" },
      { label: "Included accessories", value: "Six cooking accessories (per listing)" },
    ],
    bestFor: [
      "Replacing a toaster oven rather than adding to it",
      "Cooking a whole meal in one cavity, including a sheet-pan dinner",
      "Anyone who wants to see the food through a door without pulling a basket out",
    ],
    thinkTwice: [
      "26 quarts is a large permanent footprint. Measure the counter before you fall in love with it.",
      "French doors open outward, so it needs clear space in front and to the sides.",
      "More presets is not the same as more capability. You will use four of them.",
    ],
    criteria: [
      {
        heading: "Oven-style means you can see the food",
        body: "A door and a light let you watch without disturbing the cook. That is the single biggest day-to-day difference from a basket machine, and it is the reason oven-style units suit people who bake and roast more than they fry.",
      },
      {
        heading: "Capacity you can actually fill",
        body: "Twenty-six quarts is enough for a sheet pan, a small roast, or several racks at once. But large capacity only pays off if your recipes use it. A single person cooking one portion will heat a big cavity to cook a small amount.",
      },
      {
        heading: "Accessories are part of the purchase",
        body: "Six accessories included changes the real cost comparison against a bare oven. Check what is in the box before comparing against a unit that charges extra for the same racks.",
      },
    ],
    pairingGuide: "air-fryer-capacity-checklist",
  },
  {
    id: "P3",
    slug: "chefman-turbofry-8-quart",
    name: "Chefman TurboFry 8 Quart Air Fryer",
    brand: "Chefman",
    category: "air-fryers",
    style: "Single-basket",
    asin: "B08DKYBTPH",
    asinStatus: "observed",
    listingTitle:
      "Chefman Air Fryer 8 Qt | TurboFry 4-in-1 with 450°F Hi-Fry Option for Crispier Results | Bake, Dehydrate, Frozen | XL Nonstick Dishwasher-Safe Basket | Stainless Steel",
    hook: "One big basket, one decision, for the family that cooks the same thing for everyone.",
    oneLine:
      "An 8-quart single-basket air fryer with four presets and a nonstick basket that goes in the dishwasher.",
    specs: [
      { label: "Stated capacity", value: "8 quarts" },
      { label: "Stated temperature range", value: "200–400°F" },
      { label: "Stated presets", value: "Four (fries, chicken, meat, fish)" },
      { label: "Stated dimensions", value: "12.75\"D x 13.5\"W x 10\"H" },
      { label: "Cleaning", value: "Basket and tray top-rack dishwasher safe (per listing)" },
    ],
    bestFor: [
      "Cooking one large batch for several people",
      "Anyone who wants a single thing to wash",
      "A first air fryer where simplicity beats features",
    ],
    thinkTwice: [
      "One basket means one temperature at a time. Two foods needing different heats finish at different times.",
      "Eight quarts is genuinely big; it will not tuck into a cupboard.",
      "The listing notes a newer model exists in the same line, so check which generation you are buying.",
    ],
    criteria: [
      {
        heading: "Big single basket versus two small ones",
        body: "If everyone at the table eats the same thing, a big single basket is faster and simpler. If two people want different dinners, a split basket wins. This is a household question, not a spec question.",
      },
      {
        heading: "Dishwasher-safe is a real feature",
        body: "Nonstick degrades fastest when it is scrubbed. A basket and tray rated for the top rack removes the most common way people shorten an air fryer's life.",
      },
      {
        heading: "Watch the generation",
        body: "Air fryer lines get quietly revised. The listing for this model notes a newer model in the same family, so confirm which one the link lands on before you buy.",
      },
    ],
    pairingGuide: "air-fryer-capacity-checklist",
  },
  {
    id: "P5",
    slug: "chef-iq-sense-3-probe-thermometer",
    name: "CHEF iQ Sense Wireless Meat Thermometer (3 Probes)",
    brand: "CHEF iQ",
    category: "thermometers",
    style: "Wireless probe",
    asin: "B0DZFD6R9Z",
    asinStatus: "observed",
    listingTitle:
      "CHEF iQ Sense | Smart Wireless Meat Thermometer | 3 Ultra-Thin Probes | WiFi Unlimited Range | 1000°F Heat Safe | 5 Sensors | BBQ, Grill, Oven, Smoker, Air Fryer | Gen3",
    hook: "The thermometer that makes an air fryer safe for a whole chicken.",
    oneLine:
      "A Wi-Fi connected meat thermometer with three ultra-thin probes, wet-bulb and ambient sensing, and app-guided cooking.",
    specs: [
      { label: "Stated probes included", value: "Three (this variant)" },
      { label: "Stated sensors", value: "Five, including an ambient sensor" },
      { label: "Stated heat tolerance", value: "1000°F" },
      { label: "Connectivity", value: "Wi-Fi and Bluetooth, app display" },
      { label: "Stated battery life", value: "Up to 50 hours on a full charge" },
      { label: "Cleaning", value: "Probes stated waterproof and dishwasher safe" },
    ],
    bestFor: [
      "Anyone cooking whole birds or large cuts in an air fryer or oven",
      "Cooking three proteins to different doneness at once",
      "People who leave the room while something roasts",
    ],
    thinkTwice: [
      "It needs an app. A thermometer that depends on a phone is only as reliable as the app.",
      "This listing offers several probe counts at different variants; confirm the count before ordering.",
      "It is a precision tool, not a safety device. It reads temperature; it does not decide anything for you.",
    ],
    criteria: [
      {
        heading: "Why a thermometer belongs next to an air fryer",
        body: "Air fryers cook fast on the outside and can lag in the middle, especially with bone-in poultry. A probe in the thickest part turns a guess into a reading, which is the difference between juicy and safe-but-dry.",
      },
      {
        heading: "Ambient sensing changes what you can infer",
        body: "An ambient sensor reads the cooking environment alongside the food. It lets the app estimate cooking time rather than just reporting a current temperature, which is the feature that separates a smart thermometer from a display on a wire.",
      },
      {
        heading: "Probe count is the variant question",
        body: "One, two, three and four-probe versions appear on the same listing. The count changes the price and what you can cook at once, so pick the variant deliberately rather than accepting whichever the link opens.",
      },
    ],
    pairingGuide: "questions-before-buying-multifunction-appliance",
  },
];

// The unresolved link. Deliberately not attached to a product page.
export const heldProduct = {
  id: "P4",
  submitted_link: "https://link.amazon/B0c8moW59",
  submitted_code: "B0c8moW59",
  reason:
    "This link did not resolve to a product listing when checked on 2026-11-20. It returned a bot-check interstitial, then the Amazon homepage, and a direct lookup of the likely ASIN found no product.",
  effect:
    "Nothing is published for it. No product page, no guide mention, no shelf placement. Publishing a guess would put a link on the site that we cannot describe honestly.",
  next_step:
    "Regenerate the link from Associates Central, or send the product name, and the page will be built the same day.",
};

export const categories = [
  {
    id: "air-fryers",
    label: "Air fryers",
    blurb: "Basket, dual-basket and oven-style. Three of the four stocked products live here.",
  },
  {
    id: "thermometers",
    label: "Thermometers",
    blurb: "One probe set, chosen because it makes the air fryer safe for whole cuts.",
  },
];

export function productUrl(p) {
  return `${siteCfg.baseUrl}/shop/${p.slug}/`;
}

// Every outbound product link carries the Associates tag and is marked sponsored
// at the anchor level (rel="sponsored nofollow noopener"). S02 + S03.
export function sponsoredHref(asin) {
  return `https://www.amazon.com/dp/${asin}?tag=${siteCfg.tag}`;
}
