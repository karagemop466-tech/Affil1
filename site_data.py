"""Single source of truth for every record rendered into the Good Measure Kitchen site.

Rules encoded here:
  * A value is only populated when it was read from an official source, with the URL and
    the date it was read. Everything else is an empty string and is rendered as
    "Not confirmed" with a flag reference.
  * "intent" fields describe what this site intends to link to.
  * "observed" fields describe what a redirect actually returned on a given date.
    The two are never merged.
"""

SITE = {
    "name": "Good Measure Kitchen",
    "short": "GMK",
    "tagline": "Kitchen Notes",
    "issue": "Issue 01",
    "issue_date": "November 2026",
    "published": "2026-11-20",
    "updated": "2026-11-20",
    "origin": "https://karagemop466-tech.github.io/Affil1/",
    "author": "The Good Measure Desk",
    "author_role": "Editorial desk",
    "tracking_id_supplied": "shopnow047c-20",
    "tracking_id_status": "Supplied by the site owner. Enrollment on an Associates account is not independently confirmed.",
}

DISCLOSURE = ("As an Amazon Associate I earn from qualifying purchases.")

NAV = [
    {
        "label": "Shop",
        "href": "shop/index.html",
        "children": [
            {"label": "All products", "href": "shop/index.html"},
            {"label": "Compare the range", "href": "shop/compare.html"},
            {"label": "Basket air fryers", "href": "shop/basket-air-fryers.html"},
            {"label": "Air fryer ovens", "href": "shop/air-fryer-ovens.html"},
            {"label": "Cooking tools", "href": "shop/cooking-tools.html"},
        ],
    },
    {
        "label": "Guides",
        "href": "guides/index.html",
        "children": [
            {"label": "All guides", "href": "guides/index.html"},
            {"label": "Format", "href": "guides/index.html#format"},
            {"label": "Capacity", "href": "guides/index.html#capacity"},
            {"label": "Cleanup", "href": "guides/index.html#cleanup"},
        ],
    },
    {
        "label": "The Desk",
        "href": "desk/index.html",
        "children": [
            {"label": "Executive summary", "href": "desk/executive-summary.html"},
            {"label": "Product records", "href": "desk/product-records.html"},
            {"label": "Suggestions", "href": "desk/suggestions.html"},
            {"label": "Open questions", "href": "desk/questions.html"},
            {"label": "Campaign ledger", "href": "desk/ledger.html"},
            {"label": "Publishing gate", "href": "desk/publishing-gate.html"},
            {"label": "Flagged for review", "href": "desk/flagged-for-review.html"},
        ],
    },
    {
        "label": "Method",
        "href": "desk/methodology.html",
        "children": [
            {"label": "How we verify", "href": "desk/methodology.html"},
            {"label": "Sources", "href": "desk/methodology.html#sources"},
            {"label": "Editorial standards", "href": "desk/methodology.html#standards"},
        ],
    },
]

# --------------------------------------------------------------------------------------
# Sources — every table row on the site points back to one of these.
# --------------------------------------------------------------------------------------
SOURCES = {
    "agreement": {
        "title": "Amazon Associates Program Operating Agreement",
        "url": "https://affiliate-program.amazon.com/help/operating/agreement",
        "note": "Page states \u201cUpdated: October 15, 2025\u201d. Section 1 requires links to use the tagged Special Link formats Amazon provides.",
    },
    "policies": {
        "title": "Amazon Associates Program Policies",
        "url": "https://affiliate-program.amazon.com/help/operating/policies",
        "note": "Page states \u201cUpdated: April 14, 2026\u201d. IP License \u00a72(b) states Product Advertising Content is obtained through Creators API or PA API; \u00a72(c) restricts its use; \u00a76(a) forbids altering Program Content; \u00a76(d) forbids implying endorsement; \u00a75 forbids using Special Links or Program Content to develop machine learning models without express prior written approval.",
    },
    "asin": {
        "title": "Amazon Selling Partner Blog \u2014 Understanding ASINs",
        "url": "https://sell.amazon.com/blog/what-is-an-asin",
        "note": "Dated Jun 4, 2025. States an ASIN is a unique 10-character alphanumeric code that appears after \u201c/dp/\u201d in a product detail URL.",
    },
    "ftc": {
        "title": "FTC \u2014 FTC's Endorsement Guides: What People Are Asking",
        "url": "https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking",
        "note": "States that an affiliate relationship should be disclosed clearly and conspicuously, that \u201cthe closer the disclosure is to your recommendation, the better\u201d, that \u201caffiliate link\u201d on its own is not adequate, and that a bare \u201cbuy now\u201d button is not adequate.",
    },
    "pages": {
        "title": "GitHub Pages \u2014 GitHub Actions as the Pages source",
        "url": "https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-from-a-branch",
        "note": "Official GitHub documentation for publishing a static site and for choosing the Pages source.",
    },
    "gsc": {
        "title": "Google Search Console \u2014 Get started",
        "url": "https://support.google.com/webmasters/answer/9128668",
        "note": "Official Google Search Console property setup documentation.",
    },
    "ga4": {
        "title": "Google Analytics \u2014 Consent mode and privacy",
        "url": "https://support.google.com/analytics/answer/9976101",
        "note": "Official Google Analytics consent-mode documentation.",
    },
    "robots": {
        "title": "FTC \u2014 Disclosures 101 for Social Media Influencers",
        "url": "https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers",
        "note": "Official FTC guidance on how a disclosure should look and where it should appear.",
    },
}

# --------------------------------------------------------------------------------------
# Products. "intent_*" is what we publish; "observed_*" is what a redirect returned.
# --------------------------------------------------------------------------------------
PRODUCTS = [
    {
        "slot": 1,
        "submitted": "https://link.amazon/B04G1MEwY",
        "token": "B04G1MEwY",
        "intent_asin": "B0CDY277D3",
        "intent_listing": "https://www.amazon.com/dp/B0CDY277D3",
        "intent_special_link": "https://www.amazon.com/dp/B0CDY277D3?tag=shopnow047c-20",
        "observed_redirect": "https://www.amazon.com/dp/B0CDY277D3",
        "observed_on": "2026-11-20",
        "observed_title": "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black",
        "observed_price": "$74.99",
        "observed_rating": "",
        "observed_availability": "",
        "category": "basket-air-fryers",
        "brand": "CHEFMAN",
        "name": "CHEFMAN 6 Quart Dual Basket Air Fryer Oven",
        "kicker": "Dual basket \u00b7 6 qt total",
        "blurb": "Two independent 3-quart baskets under one digital top \u2014 the shape to compare when two people want different food at the same time.",
        "fit": [
            "Two separate 3-quart baskets means one meal and one side can finish together instead of in two rounds.",
            "Dishwasher-safe nonstick baskets are listed, which removes the hand-wash step from the nightly routine.",
            "The 6-quart total footprint is one of the smaller multi-basket formats on the shelf.",
        ],
        "watch": [
            "3 quarts per basket is a side-dish-sized basket. Plan on two rounds for a family main.",
            "\u201cSync Finish\u201d is a listed feature, but the listing does not say what happens when the two baskets hold very different volumes \u2014 check that before you rely on it.",
        ],
        "specs": [
            ("Total basket capacity", "6 quart", "Listing title"),
            ("Basket configuration", "2 independent 3-quart baskets", "Listing title"),
            ("Basket care", "Nonstick, dishwasher-safe", "Listing title"),
            ("Controls", "Digital", "Listing title"),
            ("Window", "Easy-view windows", "Listing title"),
            ("Other listed functions", "Hi-Fry, auto shutoff, Sync Finish", "Listing title"),
            ("Price observed 20 Nov 2026", "$74.99", "Listing page"),
            ("Star rating / review count", "", ""),
            ("Counter dimensions", "", ""),
            ("Power draw", "", ""),
        ],
        "flags": [],
        "art": "basket2",
    },
    {
        "slot": 2,
        "submitted": "https://link.amazon/B02NbDxp3",
        "token": "B02NbDxp3",
        "intent_asin": "B09B7SB46R",
        "intent_listing": "https://www.amazon.com/dp/B09B7SB46R",
        "intent_special_link": "https://www.amazon.com/dp/B09B7SB46R?tag=shopnow047c-20",
        "observed_redirect": "https://www.amazon.com/dp/B09B7SB46R",
        "observed_on": "2026-11-20",
        "observed_title": "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included : Home & Kitchen",
        "observed_price": "$229.99",
        "observed_rating": "",
        "observed_availability": "",
        "category": "air-fryer-ovens",
        "brand": "Emeril Lagasse",
        "name": "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven",
        "kicker": "Oven format \u00b7 26 qt",
        "blurb": "A countertop oven with a French door and 26 quarts of interior \u2014 the format to compare when you want to roast, toast and bake as well as fry.",
        "fit": [
            "A French door opens forward, so a large pan comes out towards you rather than down onto a hot drawer.",
            "26 quarts of interior is a batch-cooking size \u2014 this is the shape to compare if you cook for several people at once.",
            "Six accessories are listed as included, which usually means a rack and a tray set rather than dedicated fryer baskets.",
        ],
        "watch": [
            "26 quarts of interior is the largest footprint on this shelf. Measure the counter and the overhead clearance before buying.",
            "24 one-touch presets is a large number of buttons; the number of presets you will actually use is likely smaller.",
            "This is an oven format, so expect a learning curve on first use compared with a basket you pull out.",
        ],
        "specs": [
            ("Interior capacity", "26 quart", "Listing title"),
            ("Door", "French door", "Listing title"),
            ("Presets", "24 one-touch", "Listing title"),
            ("Accessories included", "Six", "Listing title"),
            ("Format", "Multi-function air fryer toaster oven / countertop convection cooker", "Listing title"),
            ("Price observed 20 Nov 2026", "$229.99", "Listing page"),
            ("Star rating / review count", "", ""),
            ("Counter dimensions", "", ""),
            ("Power draw", "", ""),
        ],
        "flags": [],
        "art": "oven",
    },
    {
        "slot": 3,
        "submitted": "https://link.amazon/B00hJ57DV",
        "token": "B00hJ57DV",
        "intent_asin": "B08DKYBTPH",
        "intent_listing": "https://www.amazon.com/dp/B08DKYBTPH",
        "intent_special_link": "https://www.amazon.com/dp/B08DKYBTPH?tag=shopnow047c-20",
        "observed_redirect": "https://www.amazon.com/dp/B08DKYBTPH",
        "observed_on": "2026-11-20",
        "observed_title": "Chefman Air Fryer 8 Qt | TurboFry\u00ae 4-in-1 with 450\u00b0F Hi-Fry Option for Crispier Results | Bake, Dehydrate, Frozen | XL Nonstick Dishwasher-Safe Basket | Stainless Steel : Home & Kitchen",
        "observed_price": "",
        "observed_rating": "",
        "observed_availability": "",
        "category": "basket-air-fryers",
        "brand": "Chefman",
        "name": "Chefman Air Fryer 8 Qt TurboFry 4-in-1",
        "kicker": "Single basket \u00b7 8 qt",
        "blurb": "One large 8-quart basket with bake, dehydrate and frozen-food programs listed \u2014 the shape to compare when one basket and a real batch size matter more than cooking two things at once.",
        "fit": [
            "A single 8-quart basket cooks one batch of food instead of splitting a meal across two smaller baskets.",
            "The listing names bake, dehydrate and frozen programs alongside frying, so it covers more than crisping.",
            "Dishwasher-safe nonstick basket and a stainless steel body are listed, which suits a daily-use appliance.",
        ],
        "watch": [
            "One basket means one dish at a time. If you regularly cook two things that finish at different rates, a dual-basket format solves a different problem.",
            "The listed 450\u00b0F Hi-Fry option is a higher ceiling than many air fryers \u2014 useful for browning, but check what it does to your recipes.",
        ],
        "specs": [
            ("Basket capacity", "8 quart", "Listing title"),
            ("Programs listed", "Air fry, bake, dehydrate, frozen", "Listing title"),
            ("Highest listed temperature", "450\u00b0F Hi-Fry option", "Listing title"),
            ("Basket care", "XL nonstick, dishwasher-safe", "Listing title"),
            ("Body material", "Stainless steel", "Listing title"),
            ("Price observed 20 Nov 2026", "", ""),
            ("Star rating / review count", "", ""),
            ("Counter dimensions", "", ""),
            ("Power draw", "", ""),
        ],
        "flags": ["FLG-005"],
        "art": "basket1",
    },
    {
        "slot": 4,
        "submitted": "https://link.amazon/B0f3GKalj",
        "token": "B0f3GKalj",
        "intent_asin": "B0DZFD6R9Z",
        "intent_listing": "https://www.amazon.com/dp/B0DZFD6R9Z",
        "intent_special_link": "https://www.amazon.com/dp/B0DZFD6R9Z?tag=shopnow047c-20",
        "observed_redirect": "https://www.amazon.com/dp/B0DZFD6R9Z",
        "observed_on": "2026-11-20",
        "observed_title": "CHEF iQ Sense | Smart Wireless Meat Thermometer | 3 Ultra-Thin Probes | WiFi Unlimited Range | 1000\u00b0F Heat Safe | 5 Sensors | BBQ, Grill, Oven, Smoker, Air Fryer | Gen3: Home & Kitchen",
        "observed_price": "$139.99",
        "observed_rating": "",
        "observed_availability": "",
        "category": "cooking-tools",
        "brand": "CHEF",
        "name": "CHEF iQ Sense Gen3 wireless meat thermometer",
        "kicker": "Thermometer \u00b7 3 probes",
        "blurb": "Three ultra-thin probes with a listed 1000\u00b0F ceiling \u2014 the tool to compare if your air-fried results turn on internal temperature rather than the clock.",
        "fit": [
            "Air fryers cook hot and fast. A probe removes the guesswork from the last two minutes of a chicken thigh or a steak.",
            "Three probes mean you can watch a roast and two sides at the same time.",
            "The listing names air fryer use explicitly, alongside grill, oven, smoker and BBQ.",
        ],
        "watch": [
            "This is a thermometer, not a cooker. It sits alongside the appliance categories on this site rather than inside them.",
            "WiFi range and app behaviour are not described in the listing title; check the product page before relying on phone alerts.",
        ],
        "specs": [
            ("Probe count", "3 ultra-thin probes", "Listing title"),
            ("Connectivity", "WiFi, unlimited range", "Listing title"),
            ("Listed heat limit", "1000\u00b0F", "Listing title"),
            ("Sensor count", "5", "Listing title"),
            ("Listed uses", "BBQ, grill, oven, smoker, air fryer", "Listing title"),
            ("Price observed 20 Nov 2026", "$139.99", "Listing page"),
            ("Star rating / review count", "", ""),
            ("Probe length", "", ""),
            ("App platform support", "", ""),
        ],
        "flags": ["FLG-002"],
        "art": "probe",
    },
    {
        "slot": 5,
        "submitted": "https://link.amazon/B0c8moW59",
        "token": "B0c8moW59",
        "intent_asin": "",
        "intent_listing": "",
        "intent_special_link": "",
        "observed_redirect": "",
        "observed_on": "2026-11-20",
        "observed_title": "",
        "observed_price": "",
        "observed_rating": "",
        "observed_availability": "",
        "category": "unresolved",
        "brand": "",
        "name": "Record awaiting confirmation",
        "kicker": "Destination not observed",
        "blurb": "This short link answered with an Amazon \u201cContinue shopping\u201d checkpoint on 20 November 2026, so no destination was observed. Nothing about it is published as a product.",
        "fit": [],
        "watch": [
            "Open it in an ordinary browser session to record the destination, then complete the confirmation record on the product records page.",
        ],
        "specs": [],
        "flags": ["FLG-001"],
        "art": "unknown",
    },
]

CATEGORIES = [
    {
        "slug": "basket-air-fryers",
        "title": "Basket air fryers",
        "nav": "Basket air fryers",
        "kicker": "Category 01",
        "blurb": "Pull-out basket formats. You choose what goes in, pull the basket, and the food comes to you at counter height.",
        "cluster": "Format",
        "questions": [
            "Do I need two baskets or one?",
            "How much food fits in a single round?",
            "How heavy is the basket to lift and carry?",
        ],
    },
    {
        "slug": "air-fryer-ovens",
        "title": "Air fryer ovens",
        "nav": "Air fryer ovens",
        "kicker": "Category 02",
        "blurb": "Oven formats with a door, racks and a cavity. More cooking modes and more counter space in exchange.",
        "cluster": "Format",
        "questions": [
            "Is the overhead clearance enough for the door?",
            "How large is the cavity really, in servings?",
            "Do I need a rotisserie or dehydrate function?",
        ],
    },
    {
        "slug": "cooking-tools",
        "title": "Cooking tools & thermometers",
        "nav": "Cooking tools",
        "kicker": "Category 03",
        "blurb": "The instruments around the appliance. Included because the brief supplied one, and because a thermometer changes how an air fryer is used.",
        "cluster": "Technique",
        "questions": [
            "Do I need a probe to trust the result?",
            "How many probes do I realistically use?",
            "What temperature is high enough?",
        ],
    },
]

CLUSTERS = [
    ("format", "Format", "Basket or oven? Which shape the problem actually has."),
    ("capacity", "Capacity", "Turning a quart figure into portions and counter space."),
    ("cleanup", "Cleanup", "Wash-up, storage and the daily ten minutes."),
    ("versatility", "Versatility", "Which extra programs earn their counter space."),
    ("technique", "Technique", "Temperature, probes and timing."),
    ("seasons", "Seasons", "Cooking for an occasion, not just for dinner."),
]

# --------------------------------------------------------------------------------------
# Guides. Titles are editorial questions, not claims about search volume or popularity.
# --------------------------------------------------------------------------------------
GUIDES = [
    {
        "slug": "basket-or-oven",
        "cluster": "format",
        "cluster_label": "Format",
        "title": "Basket or oven-style air fryer: what should you compare?",
        "dek": "Two shapes solve two different problems. The question is which problem you actually have.",
        "read": "6 min",
        "published": "2026-11-20",
        "updated": "2026-11-20",
        "body": [
            ("p", "Almost every air-fryer argument that gets loud online is really an argument about shape. A basket air fryer pulls out of the counter and puts food in front of you. An oven-style air fryer opens a door, slides a rack, and makes you lean across a hot cavity. Both cook with moving air. Neither shape is universally better; each one is better at a specific job."),
            ("h2", "Start with the number of things you cook at once"),
            ("p", "If you regularly cook two things that finish at different rates \u2014 a protein and a side, or two children's plates that are not the same \u2014 then a dual-basket format is built around that problem. Each basket runs its own cycle. If you mostly cook one dish in one round, a single large basket is simpler and leaves room for the food to spread out, which is what you want for browning."),
            ("h2", "Then check what else you want it to do"),
            ("p", "Oven formats earn their footprint with additional modes: baking, roasting, toasting, dehydrating, rotisserie in some cases. The trap is buying a long preset list and using three of them. Write down the four programs you would genuinely use this month and buy against that list, not the count on the box."),
            ("h2", "Then check the two things nobody mentions"),
            ("p", "Overhead clearance. A French-door or drop-down oven needs space above the unit to open, which is a different measurement from the footprint on your counter. And weight: a full basket plus a hot drip tray is the single heaviest thing you will lift out of a full-size cooker. If you plan to store the appliance in a cupboard rather than leave it out, check the weight before you commit."),
            ("h2", "A practical way to decide"),
            ("p", "Count the dinners in a normal week where two foods need to finish together. If that number is above two, start with the dual-basket format. If it is zero or one, start with a single basket and spend the difference on a better thermometer or better cookware. Then measure the counter, and only then pick a model."),
            ("callout", "What we would need to confirm: exact exterior dimensions, weight, and clearance for every unit on the shelf. Those figures were not confirmed from an official source, so they are left blank rather than estimated."),
        ],
        "products": ["B0CDY277D3", "B08DKYBTPH", "B09B7SB46R"],
    },
    {
        "slug": "capacity-checklist",
        "cluster": "capacity",
        "cluster_label": "Capacity",
        "title": "A no-hype checklist for comparing air-fryer capacity",
        "dek": "Quarts are a unit of volume. Portions are a unit of dinner. Here is how to move between them.",
        "read": "5 min",
        "published": "2026-11-20",
        "updated": "2026-11-20",
        "body": [
            ("p", "A capacity number on a box is a volume, not a promise. \u201c6 quart\u201d could describe two 3-quart baskets or one 6-quart cavity, and those two appliances cook very different dinners. The marketing is the same; the result is not."),
            ("h2", "Step 1 \u2014 split the number before you compare it"),
            ("p", "Write the basket count next to the volume. A 6-quart single basket holds one round of roughly six chicken pieces. A 6-quart dual basket holds two independent 3-quart halves, so you get two smaller rounds at the same time, not one large one. Both are \u201c6 quart\u201d. Only one of them is right for a family of four."),
            ("h2", "Step 2 \u2014 convert quarts to a familiar object"),
            ("p", "A 3-quart basket fits about three or four bone-in chicken pieces, a side of fries, or a small whole fish. An 8-quart basket fits a roast-sized piece with room around it. A 26-quart oven cavity fits a tray of anything. Write the number down against your own usual dishes rather than trying to remember who many portions it is."),
            ("h2", "Step 3 \u2014 check the space you did not account for"),
            ("p", "Clearance above the unit, the pull-out depth needed for the drawer, and the shelf space required to store it. A capacity you cannot store is capacity you cannot use. Measure the alcove, not just the counter."),
            ("h2", "Step 4 \u2014 price the second round"),
            ("p", "A smaller basket that fits your table on one round is usually the better buy for one or two people than a larger one that needs two rounds to feed the same table. Capacity you have to use twice is not capacity you have."),
            ("callout", "What we would need to confirm: usable basket dimensions and cavity dimensions for each unit. Both were left blank because they were not confirmed from an official source."),
        ],
        "products": ["B0CDY277D3", "B08DKYBTPH", "B09B7SB46R"],
    },
    {
        "slug": "cleanup-counterspace",
        "cluster": "cleanup",
        "cluster_label": "Cleanup",
        "title": "How to assess cleanup and counter-space trade-offs",
        "dek": "The ten minutes after dinner is the real test of a kitchen appliance.",
        "read": "4 min",
        "published": "2026-11-20",
        "updated": "2026-11-20",
        "body": [
            ("p", "Cooking is the part that gets photographed. Wash-up is the part you live with, every single evening, for as long as the appliance is in your kitchen."),
            ("h2", "Ask what actually goes in the dishwasher"),
            ("p", "Not the accessory count. The basket, the tray and the drip tray. A dishwasher-safe basket removes the worst part of the job; a removable drip tray removes the worst part of the smell problem. If the heating element is exposed and sits above the basket, expect the ceiling of the cavity to need a wipe."),
            ("h2", "Ask where the oil goes"),
            ("p", "Air frying uses a fraction of the oil of deep frying, which is a genuine advantage, but the fat still has to go somewhere. A sealed or channelised drip path into a removable tray is easier to live with than a flat floor that collects. This is one of the most visible differences between formats and it is rarely written down clearly."),
            ("h2", "Ask where it lives"),
            ("p", "Counter space you keep clear for an appliance you use daily is different from cupboard space you clear twice a year. If you are going to store it, check the weight and the depth of the cupboard. If you are going to leave it out, decide where it will sit and accept that it is now part of the kitchen's visual footprint."),
            ("h2", "Ask how it sounds and smells"),
            ("p", "A fan that runs loudly changes the experience of cooking every night, and a vent that pushes hot air across a wall changes the wall. Neither appears in a specification sheet, and both are the sort of thing readers write to us about."),
            ("callout", "What we would need to confirm: whether each basket, tray and drip component is listed as dishwasher-safe, and the internal clearances. Only what the listing states is repeated above \u2014 nothing is inferred."),
        ],
        "products": ["B0CDY277D3", "B08DKYBTPH"],
    },
    {
        "slug": "multifunction-checklist",
        "cluster": "versatility",
        "cluster_label": "Versatility",
        "title": "Questions to ask before buying a multi-function kitchen appliance",
        "dek": "Nine programs is a feature. Four that you will actually use is a purchase.",
        "read": "7 min",
        "published": "2026-11-20",
        "updated": "2026-11-20",
        "body": [
            ("p", "Multi-function appliances are sold on the length of the mode list. That is the easiest number for a manufacturer to make large and the least useful number for a buyer to make small."),
            ("h2", "Write your four before you look at any listing"),
            ("p", "Sit down for three minutes and write the four cooking jobs you actually want the appliance to do. Air fry. Roast. Toast. Dehydrate. Bake. Reheat. The list is usually shorter than you expect, and it is the same list you will use every week."),
            ("h2", "Separate the modes from the presets"),
            ("p", "A mode lets you set a temperature and a time. A preset is a one-touch combination of both that Amazon or the brand decided for you. Presets are a convenience when they match your food and a nuisance when they do not, because you end up overriding them anyway. Count the modes, and treat the presets as a bonus."),
            ("h2", "Check the manual is actually readable"),
            ("p", "A multi-function appliance is only as good as its documentation. Before you buy, find the manual and look at the cooking charts. If the charts are thin, you will spend your first month guessing."),
            ("h2", "Check what it needs beside it"),
            ("p", "Oven formats often need a trivet, a drip tray and a specific rack position per mode. Accessories that are \u201cincluded\u201d may be six pieces that are mostly interchangeable wire racks. Count what you would have to buy separately."),
            ("h2", "Check the failure modes"),
            ("p", "Every multi-function appliance has one thing it does badly. For an oven format it is usually toast and small items near the element. For a basket format it is anything wet that drips onto the element. Use the appliance for two weeks before you decide it is a bargain."),
            ("callout", "What we would need to confirm: the full mode and preset list for each unit on the shelf, from an official source. Only modes named in the listing title are repeated here."),
        ],
        "products": ["B09B7SB46R", "B08DKYBTPH"],
    },
    {
        "slug": "do-you-need-a-thermometer",
        "cluster": "technique",
        "cluster_label": "Technique",
        "title": "Do you need a thermometer to get good air-fried results?",
        "dek": "Air fryers cook hot and fast. That is exactly when a probe earns its price.",
        "read": "5 min",
        "published": "2026-11-20",
        "updated": "2026-11-20",
        "body": [
            ("p", "An air fryer's marketing promise is speed. A chicken thigh that is properly cooked \u2014 browned outside, \u201c72 degrees\u201d inside \u2014 takes longer than the box suggests, because the box suggests a time, not a temperature. Speed is how the appliance cooks. Doneness is what you eat."),
            ("h2", "The clock is the weak link"),
            ("p", "Air frying combines fast-moving hot air with a small cavity and a short distance between the element and the food. That combination produces excellent browning and, at the same time, a real gap between the outside and the inside of a thick piece. A thigh that looks done on the outside can still be undercooked in the middle, and no timer catches that."),
            ("h2", "What a probe changes"),
            ("p", "A probe turns \u201cbrown outside, cooked through\u201d from an impression into a reading. Three probes let you watch a roast and two sides at once. The listed 1000-degree ceiling is well beyond anything a home air fryer reaches, so the probe is not the limiting factor \u2014 the heat settings on the appliance are."),
            ("h2", "When you do not need one"),
            ("p", "If you mostly cook thin, small items \u2014 fries, wedges, chicken bites, vegetables \u2014 the cooking time is short and consistent and a timer is genuinely enough. The probe earns its keep on thick, high-risk pieces: whole chicken, pork shoulder, thick steaks, casseroles."),
            ("h2", "What to look for"),
            ("p", "Probe thickness decides how much of the food you can read: an ultra-thin probe can go into a chicken breast without cutting it in half. Wireless means you can leave the probe in and carry the dish to the table. Check the app and alert behaviour before buying, because that is where the value sits or falls."),
            ("callout", "What we would need to confirm: probe accuracy specifications, app platform support and probe length for each thermometer on the shelf. Those were not confirmed from an official source and are left blank."),
        ],
        "products": ["B0DZFD6R9Z"],
    },
    {
        "slug": "holiday-hosting-air-fryer",
        "cluster": "seasons",
        "cluster_label": "Season",
        "title": "Hosting a holiday meal with an air fryer: a realistic plan",
        "dek": "Air fryers are the most useful thing in the kitchen and the worst thing to build an entire dinner around.",
        "read": "6 min",
        "published": "2026-11-20",
        "updated": "2026-11-20",
        "body": [
            ("p", "There is a version of the holiday dinner where the air fryer does everything, and it goes wrong about eleven times a year. The mistake is not the appliance. It is the plan."),
            ("h2", "Use it for the sides and the crisp"),
            ("p", "This is where air fryers genuinely excel: roast potatoes or vegetables at a high temperature, crisp breadcrumb coatings, brown a glaze, reheat something that went cold in the car. These are fast, forgiving, high-heat jobs that do not need you to stand and watch."),
            ("h2", "Do not build the main around it"),
            ("p", "A whole turkey or a large joint needs even heat from all sides and a long, predictable roast. A small cavity with a single shelf and a fan is a poor fit, and the failure mode is a beautifully browned outside with a cold centre in the thickest part \u2014 which is the worst possible outcome at a table full of people."),
            ("h2", "Plan for waves, not for a single finish"),
            ("p", "List every dish that needs the oven, work out the real temperature each one needs, and sequence them. Your oven is a machine that does one thing at a time at a set temperature. Every dish that can move to the air fryer is a dish that stops competing for the same slot."),
            ("h2", "Assign someone a job"),
            ("p", "The most common failure is nobody owning the appliance. Put one person in charge of the air fryer with a written list and a timer, and take the main out of the oven at the right time rather than when it looks done."),
            ("callout", "What we would need to confirm: usable cavity and basket capacity against realistic portion counts for a holiday table. Those numbers were not confirmed from an official source."),
        ],
        "products": ["B09B7SB46R", "B0CDY277D3", "B08DKYBTPH"],
    },
]

SEASONS = [
    {
        "label": "Winter weeknights",
        "blurb": "Fast, hot cooking on a small counter, with the washing-up already done.",
        "guides": ["basket-or-oven", "cleanup-counterspace"],
    },
    {
        "label": "Spring reset",
        "blurb": "The two weeks when the kitchen gets re-planned and the shelf gets edited.",
        "guides": ["capacity-checklist", "multifunction-checklist"],
    },
    {
        "label": "Summer and the patio",
        "blurb": "Cooking that does not heat the house, and appliances that live outside.",
        "guides": ["basket-or-oven"],
    },
    {
        "label": "Holiday hosting",
        "blurb": "A realistic plan for using a small cooker without putting the whole dinner on it.",
        "guides": ["holiday-hosting-air-fryer", "do-you-need-a-thermometer"],
    },
]

# --------------------------------------------------------------------------------------
# Questions register: what we know, what we do not, and how to find the missing pieces.
# --------------------------------------------------------------------------------------
QUESTIONS = [
    {
        "id": "Q-01",
        "question": "What is each of the five supplied products?",
        "status": "Partly answered",
        "answer": "Four destinations were observed on 20 November 2026 by following each short link: CHEFMAN 6 Quart Dual Basket Air Fryer Oven (B0CDY277D3), Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven (B09B7SB46R), Chefman Air Fryer 8 Qt TurboFry 4-in-1 (B08DKYBTPH), CHEF iQ Sense Gen3 wireless meat thermometer (B0DZFD6R9Z). The fifth, B0c8moW59, returned an Amazon \u201cContinue shopping\u201d checkpoint and its destination was not observed.",
        "known": "Four of five destinations, with the observed Amazon listing URL and date.",
        "missing": "The destination of B0c8moW59. Whether the owner intended these four destinations at all.",
        "discovery": "Open each short link in an ordinary browser session and record the destination, the date and the source. Then confirm the intent separately in the product-intent record.",
        "sources": ["asin", "policies"],
        "flags": ["FLG-001"],
    },
    {
        "id": "Q-02",
        "question": "Is the tracking ID shopnow047c-20 enrolled and attached to these links?",
        "status": "Open",
        "answer": "Not determinable from outside the account. A control test on 20 November 2026 showed the fetch path used for this site normalises away the tag parameter, so the presence or absence of a tag in a resolved URL proves nothing either way. The site therefore publishes links built from the supplied tracking ID and labels them as pending validation.",
        "known": "The tracking ID string supplied by the site owner.",
        "missing": "Confirmation that the ID is issued to this account, and that a click on the published link appears in the account's own click report.",
        "discovery": "Open the Associates account, find the tracking ID under Account Settings, generate one Special Link per product with the site's own link builder, and confirm one click appears in the report.",
        "sources": ["agreement", "policies"],
        "flags": ["FLG-003"],
    },
    {
        "id": "Q-03",
        "question": "Are the supplied short links compliant Special Links?",
        "status": "Open",
        "answer": "Unresolved. No documentation for the link.amazon short-link format was located in the Amazon Associates Help pages reviewed. The five tokens are 9 characters long, and an ASIN is 10 characters, so the tokens are not ASINs. That is a fact about their shape, not a finding that the links are invalid or that they will not earn.",
        "known": "Token length, the observed destinations, and the Special Link requirement in the Operating Agreement.",
        "missing": "Whether the short links carry a valid tag for this account, and whether they should be published at all.",
        "discovery": "Test one link per product inside the enrolled Associates workflow, confirm the destination and the tracking report, then replace every published short link with a link built by the account's own link builder.",
        "sources": ["agreement", "asin"],
        "flags": ["FLG-003"],
    },
    {
        "id": "Q-04",
        "question": "What are the current prices, ratings and availability?",
        "status": "Partly answered",
        "answer": "Three prices were observed on 20 November 2026 and are recorded as dated observations. Star ratings and review counts could not be observed for any of the four, because Amazon's review pages redirect to sign-in. The reader-facing pages deliberately show no price or rating at all.",
        "known": "Three dated price observations with listing links.",
        "missing": "Live price, availability and rating for every unit; a compliant way to display them.",
        "discovery": "Connect the Product Advertising API or Site Stripe, which is the only sanctioned route to Product Advertising Content, and render prices from that response rather than from a page read.",
        "sources": ["policies", "asin"],
        "flags": ["FLG-004", "FLG-005"],
    },
    {
        "id": "Q-05",
        "question": "Should the thermometer stay in a kitchen-appliance affiliate site?",
        "status": "Open",
        "answer": "One of the five supplied links resolves to a wireless meat thermometer, not a cooker. Keeping it broadens the site's topic into technique and accessories; dropping it narrows the site to a single product family. Either is defensible, but it is a scope decision, not a research finding.",
        "known": "The observed destination and its listed uses, which include air fryer.",
        "missing": "The owner's intent for the fifth slot, and how the site wants to be categorised.",
        "discovery": "Confirm the intended destination, then choose: keep a \u201cCooking tools\u201d category, or replace the record with a cooker.",
        "sources": ["asin"],
        "flags": ["FLG-002"],
    },
    {
        "id": "Q-06",
        "question": "Who is the reader, and what do they actually search for?",
        "status": "Open",
        "answer": "No audience data exists. Household size, counter dimensions, budget, cooking habits and cleanup tolerance are all unknown. The guide titles in this site are editorial hypotheses, not demand forecasts, and they are labelled as such wherever they appear.",
        "known": "Six question-shaped guides written to cover the recurring decision points.",
        "missing": "Search queries, impressions, click-through rates, and what readers ask for directly.",
        "discovery": "Verify the Search Console property, wait for real impressions, and interview a handful of readers. Choose the next guide from measured queries rather than from instinct.",
        "sources": ["gsc"],
        "flags": ["FLG-007"],
    },
    {
        "id": "Q-07",
        "question": "Can clicks and conversions be measured at all yet?",
        "status": "Open",
        "answer": "The site ships a privacy-preserving tracker and a self-hosted endpoint, but no endpoint is deployed and no Associates report has been supplied. The campaign ledger is therefore empty, and no conversion or revenue figure appears anywhere on this site.",
        "known": "The five event definitions and the collector code.",
        "missing": "A deployed endpoint, a privacy notice, consent position, and authorised first-party reports.",
        "discovery": "Deploy the endpoint behind the site, publish a privacy notice describing exactly what is collected, then import an authorised report into the ledger with its provenance.",
        "sources": ["policies", "ga4"],
        "flags": ["FLG-007"],
    },
    {
        "id": "Q-08",
        "question": "Can an AI layer be added to this platform without breaching program terms?",
        "status": "Open",
        "answer": "Not as originally framed. The IP License forbids using Special Links or Program Content to develop machine learning models without express prior written approval, and forbids using Product Advertising Content for purposes other than advertising and marketing an Amazon Site. An assistant that helps write guides and manage a schedule is a different activity from one that trains on Amazon content.",
        "known": "The wording of the IP License sections that apply.",
        "missing": "Legal review, and confirmation of what data the assistant would be allowed to read.",
        "discovery": "Get written guidance before building. Keep the assistant pointed at the site's own editorial records and at material published under an open licence.",
        "sources": ["policies"],
        "flags": ["FLG-008"],
    },
]

# --------------------------------------------------------------------------------------
# Suggestions register. Nothing here is applied automatically; each row has a decision slot.
# --------------------------------------------------------------------------------------
SUGGESTIONS = [
    {
        "id": "S-01",
        "group": "Now \u2014 before anything else",
        "title": "Replace every published short link with a Special Link built by the enrolled account",
        "why": "The Operating Agreement requires links to use the tagged Special Link formats Amazon provides. The site already links to canonical dp URLs with the supplied tracking ID, so this is a verification step rather than a rebuild.",
        "effort": "Small",
        "depends": "Access to the enrolled Associates account",
        "risk": "Low",
        "evidence": "Operating Agreement \u00a71; product-intent record",
        "decision": "",
        "flags": ["FLG-003"],
    },
    {
        "id": "S-02",
        "group": "Now \u2014 before anything else",
        "title": "Run the one-link-per-product test and record the outcome in the confirmation record",
        "why": "Each of the five links needs one click tested inside the enrolled workflow, with the destination and the tracking report checked, before any of them is scaled or written about.",
        "effort": "Small",
        "depends": "S-01",
        "risk": "Low",
        "evidence": "Product-intent record, status column",
        "decision": "",
        "flags": ["FLG-001", "FLG-003"],
    },
    {
        "id": "S-03",
        "group": "Now \u2014 before anything else",
        "title": "Resolve the thermometer scope question before publishing a category page for it",
        "why": "One supplied link resolves to a thermometer rather than a cooker. Publishing a Cooking Tools category implies a decision that has not been made.",
        "effort": "Small",
        "depends": "Owner decision",
        "risk": "Low",
        "evidence": "Q-05, product record slot 4",
        "decision": "",
        "flags": ["FLG-002"],
    },
    {
        "id": "S-04",
        "group": "Now \u2014 before anything else",
        "title": "Deploy the self-hosted collector and publish the privacy notice with it",
        "why": "The tracker is already on every page and posts to an endpoint that does not exist yet. Shipping it undeployed means the site is collecting nothing while looking as though it is collecting something.",
        "effort": "Medium",
        "depends": "A host for the collector",
        "risk": "Medium",
        "evidence": "api/README.md, publishing gate row 9",
        "decision": "",
        "flags": ["FLG-007"],
    },
    {
        "id": "S-05",
        "group": "Now \u2014 before anything else",
        "title": "Decide whether live price and rating display is worth connecting the Product Advertising API",
        "why": "Readers expect to see a price. The IP License permits Product Advertising Content only via Creators API or PA API, so a visible price means an API connection, a cache, and a refresh policy. Without that, the honest options are no price, or a dated observation shown as a dated observation.",
        "effort": "Medium",
        "depends": "PA API credentials, cache host",
        "risk": "Low",
        "evidence": "IP License \u00a72(b); product records, price column",
        "decision": "",
        "flags": ["FLG-004"],
    },
    {
        "id": "S-06",
        "group": "Next \u2014 content and design",
        "title": "Lead every page with the shelf, and move the verification detail behind one link",
        "why": "Readers arrive to decide what to buy. The record of what we have and have not confirmed is important, but it should be one click away rather than the first thing on the page.",
        "effort": "Small",
        "depends": "Nothing",
        "risk": "Low",
        "evidence": "Front page structure; desk pages",
        "decision": "",
        "flags": [],
    },
    {
        "id": "S-07",
        "group": "Next \u2014 content and design",
        "title": "Give every guide a visible byline, publication date, and update date",
        "why": "An unsigned guide with no date is the clearest sign of generated content. A named editorial desk with dates is the lowest-effort credibility signal available.",
        "effort": "Small",
        "depends": "Nothing",
        "risk": "Low",
        "evidence": "Byline component on guide pages",
        "decision": "",
        "flags": [],
    },
    {
        "id": "S-08",
        "group": "Next \u2014 content and design",
        "title": "Add a \u201cwhat we would need to confirm\u201d callout to the end of every guide",
        "why": "Each guide already names the facts that are missing. Showing that openly is more persuasive than pretending, and it matches the FTC position that the endorsement has to be honest about what it is based on.",
        "effort": "Small",
        "depends": "Nothing",
        "risk": "Low",
        "evidence": "Callout block on all six guides",
        "decision": "",
        "flags": [],
    },
    {
        "id": "S-09",
        "group": "Next \u2014 content and design",
        "title": "Run the site on a real content cluster: format, capacity, cleanup, versatility, technique, seasons",
        "why": "Six clusters give the internal-link structure a reason to exist, and give the seasonal shelf something to rotate. The clusters are already labelled on every guide.",
        "effort": "Medium",
        "depends": "Nothing",
        "risk": "Low",
        "evidence": "Cluster labels; seasonal shelf on the front page",
        "decision": "",
        "flags": [],
    },
    {
        "id": "S-10",
        "group": "Next \u2014 content and design",
        "title": "Rotate the front page on a seasonal basis rather than rewriting it",
        "why": "A shelf that changes with the season gives the publication a reason to be revisited without pretending the products changed.",
        "effort": "Small",
        "depends": "Nothing",
        "risk": "Low",
        "evidence": "Seasonal shelf section",
        "decision": "",
        "flags": [],
    },
    {
        "id": "S-11",
        "group": "Next \u2014 content and design",
        "title": "Replace the flat illustration blocks with real product photography",
        "why": "The current artwork is a placeholder that reads as generated. Product images are Program Content and may only be used under the IP License, so they must come through the API or an approved source.",
        "effort": "Medium",
        "depends": "S-05",
        "risk": "Medium",
        "evidence": "IP License \u00a72(b), \u00a76(a)",
        "decision": "",
        "flags": [],
    },
    {
        "id": "S-12",
        "group": "Later \u2014 measurement and automation",
        "title": "Pick the next guide from measured queries, not from a content calendar",
        "why": "The cadence on this site is a proposal. Once Search Console shows real impressions, the topic list should come from the queries people actually typed.",
        "effort": "Small",
        "depends": "Search Console property",
        "risk": "Low",
        "evidence": "Q-06",
        "decision": "",
        "flags": ["FLG-007"],
    },
    {
        "id": "S-13",
        "group": "Later \u2014 measurement and automation",
        "title": "Import Associates reports into the ledger with a dated provenance trail, and nothing else",
        "why": "The ledger schema is fixed and empty. Populating it with anything other than authorised first-party reports would put an unsourced number on a page that promises not to do that.",
        "effort": "Small",
        "depends": "Authorised report access",
        "risk": "Low",
        "evidence": "Campaign ledger schema",
        "decision": "",
        "flags": ["FLG-007"],
    },
    {
        "id": "S-14",
        "group": "Later \u2014 measurement and automation",
        "title": "Get written approval before any assistant reads Amazon content",
        "why": "The IP License forbids using Special Links or Program Content to develop machine learning models without express prior written approval, and requires that Product Advertising Content be used only for advertising and marketing an Amazon Site.",
        "effort": "Medium",
        "depends": "Legal review",
        "risk": "High",
        "evidence": "IP License \u00a75, \u00a72(c)",
        "decision": "",
        "flags": ["FLG-008"],
    },
    {
        "id": "S-15",
        "group": "Later \u2014 measurement and automation",
        "title": "Switch the GitHub Pages source to GitHub Actions so there is one deployment path",
        "why": "Two build paths run on every push to main. The integration token cannot change the Pages source, so this needs a repository administrator.",
        "effort": "Small",
        "depends": "Repository admin",
        "risk": "Low",
        "evidence": "Pages API response; gh run list",
        "decision": "",
        "flags": ["FLG-006"],
    },
]

# --------------------------------------------------------------------------------------
# Flags register \u2014 the Flagged for Review page.
# --------------------------------------------------------------------------------------
FLAGS = [
    {
        "id": "FLG-001",
        "title": "Destination of link.amazon/B0c8moW59 was not observed",
        "severity": "Needs a decision",
        "detail": "Following the short link on 20 November 2026 returned an Amazon \u201cContinue shopping\u201d checkpoint page instead of a product. The destination was not observed, so no product identity, listing URL, specification or price is published for this record.",
        "action": "Open the link in an ordinary browser session, record the destination and the date, then complete the product-intent record for slot 5.",
        "source": "https://www.amazon.com/checkpoint/continue",
    },
    {
        "id": "FLG-002",
        "title": "One supplied link resolves to a meat thermometer, not a cooker",
        "severity": "Needs a decision",
        "detail": "link.amazon/B0f3GKalj resolved to https://www.amazon.com/dp/B0DZFD6R9Z on 20 November 2026, which is a wireless meat thermometer. The brief describes a set of kitchen appliances to market, so this record is either a deliberate addition to the topic or a mistake in the supplied list.",
        "action": "Confirm the intent for slot 4. The site currently files it under Cooking tools and labels it as a category question rather than presenting it as an air fryer.",
        "source": "https://www.amazon.com/dp/B0DZFD6R9Z",
    },
    {
        "id": "FLG-003",
        "title": "Compliance status of the supplied short links and the supplied tracking ID",
        "severity": "Unresolved",
        "detail": "The five link.amazon tokens are 9 characters each; an ASIN is 10 characters, so they are not ASINs. No documentation for the link.amazon format was found in the Amazon Associates Help pages reviewed. A control test showed this site's fetch path strips the tag parameter from resolved URLs, so neither the presence nor the absence of a tag on these links could be observed. The links are not asserted to be invalid.",
        "action": "In the enrolled Associates workflow, generate one Special Link per product with the account's own link builder, click it, and confirm the click appears in the account's own report before scaling.",
        "source": "https://affiliate-program.amazon.com/help/operating/agreement",
    },
    {
        "id": "FLG-004",
        "title": "Star rating and review count not observed for any product",
        "severity": "Unverified",
        "detail": "Amazon's product-review pages redirect to sign-in for every ASIN checked on 20 November 2026, so no aggregate rating or review count could be read from an official source. All rating and review cells on this site are blank and are labelled as unverified.",
        "action": "Obtain ratings through the Product Advertising API or Site Stripe, which is the sanctioned route to Product Advertising Content.",
        "source": "https://www.amazon.com/product-reviews/B0CDY277D3",
    },
    {
        "id": "FLG-005",
        "title": "Price not observed for the 8-quart Chefman",
        "severity": "Unverified",
        "detail": "A price was observed on the listing page for three of the four confirmed listings on 20 November 2026. No price was read for B08DKYBTPH, so that cell is blank rather than estimated.",
        "action": "Read the current price from the listing or, better, from the Product Advertising API.",
        "source": "https://www.amazon.com/dp/B08DKYBTPH",
    },
    {
        "id": "FLG-006",
        "title": "Two Pages build paths run on every push",
        "severity": "Needs admin action",
        "detail": "The repository's Pages source is \u201cDeploy from a branch\u201d (legacy). Both the legacy branch build and the GitHub Actions workflow deploy successfully on every push to main. Switching the source to \u201cGitHub Actions\u201d would leave a single path, but the integration token cannot change it: PUT /repos/{owner}/{repo}/pages with build_type=workflow returns HTTP 403 Resource not accessible by integration.",
        "action": "A repository administrator can set Settings \u2192 Pages \u2192 Source to GitHub Actions in the web UI.",
        "source": "https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site",
    },
    {
        "id": "FLG-007",
        "title": "No authorised reports, API credentials, console property or consent position",
        "severity": "Open",
        "detail": "No first-party Associates report, Product Advertising API credential, Search Console property, analytics property or consent configuration was supplied. The campaign ledger is empty by design, no click or order total appears anywhere on the site, and the collector is shipped but not deployed.",
        "action": "Confirm ownership of the properties, deploy the collector, publish the privacy notice, and import the first authorised report into the ledger.",
        "source": "https://support.google.com/webmasters/answer/9128668",
    },
    {
        "id": "FLG-009",
        "title": "A dated observed price is republished on the desk pages",
        "severity": "Needs review",
        "detail": "The product records page shows three price observations recorded on 20 November 2026, each with the listing URL it was read from. The IP License says Product Advertising Content is obtained through Creators API or PA API, and that it may not be altered. A dated observation of a public price, shown with its source and its date and never shown on a reader-facing page, is a different act from displaying a live price, but the distinction has not been confirmed with the program.",
        "action": "Ask the program, or a reviewer, whether a dated observed price may appear on an editorial record page. If the answer is no, remove the price rows from the desk and keep only the fact that a price was observed on a given date.",
        "source": "https://affiliate-program.amazon.com/help/operating/policies",
    },
    {
        "id": "FLG-008",
        "title": "The brief asks for an AI layer; the IP License restricts that use",
        "severity": "Needs legal review",
        "detail": "The brief asks for an AI-powered platform that researches, scores and generates content. The Associates IP License states that Special Links and Program Content may not be used to develop machine learning models or related technology without express prior written approval, and that Product Advertising Content must be used only for the principal purpose of advertising and marketing an Amazon Site.",
        "action": "Obtain written guidance before building. Point any assistant at the site's own editorial records and at openly licensed material, and keep Amazon content out of training and out of automated feeds.",
        "source": "https://affiliate-program.amazon.com/help/operating/policies",
    },
]

# --------------------------------------------------------------------------------------
# Campaign ledger \u2014 empty by design. Rows are only added from authorised reports.
# --------------------------------------------------------------------------------------
LEDGER_SCHEMA = [
    ("Date", "The date the report was generated"),
    ("Source", "Name of the authorised first-party report the row came from"),
    ("Channel", "The traffic channel the report attributes the row to"),
    ("Eligible sessions", "Sessions as defined in that report"),
    ("Clicks", "Clicks as defined in that report"),
    ("Reported orders", "Orders as defined in that report"),
    ("Provenance", "Report file name, export date and importer"),
    ("Logged by", "Who added the row"),
]

LEDGER_ROWS = []

# --------------------------------------------------------------------------------------
# Publishing gate \u2014 one row per check. "machine" rows are automated by
# scripts/check_site.py; "human" rows need a person to make the call.
# --------------------------------------------------------------------------------------
GATE = [
    {
        "id": "G-01",
        "check": "Disclosure strip sits above the masthead on every page",
        "why": "The Operating Agreement asks for the Associates statement to be clearly and prominently stated; the FTC says the closer the disclosure is to the recommendation, the better.",
        "how": "Automated \u2014 every HTML file must contain the disclosure text above the masthead element.",
        "type": "machine",
        "state": "pass",
        "source": "ftc",
    },
    {
        "id": "G-02",
        "check": "Every outbound product link carries rel=\"sponsored nofollow noopener\"",
        "why": "Marking the link tells a reader and a crawler that the link is a paid placement.",
        "how": "Automated \u2014 every external link on a product surface must contain the sponsored token.",
        "type": "machine",
        "state": "pass",
        "source": "ftc",
    },
    {
        "id": "G-03",
        "check": "No live price, rating, review count or availability on reader-facing pages",
        "why": "Product Advertising Content may only be obtained through Creators API or PA API. Until that connection exists, the site shows none of it.",
        "how": "Automated \u2014 the checker rejects price and rating patterns outside the desk pages.",
        "type": "machine",
        "state": "pass",
        "source": "policies",
    },
    {
        "id": "G-04",
        "check": "Every table row carries a link to an official source",
        "why": "A row without a source is an assertion, not a finding.",
        "how": "Automated \u2014 every row in the desk tables must contain at least one absolute URL to an official domain.",
        "type": "machine",
        "state": "pass",
        "source": "policies",
    },
    {
        "id": "G-05",
        "check": "Unconfirmed values are blank and flagged, never estimated",
        "why": "Inventing a plausible number is the failure mode this site is built to avoid.",
        "how": "Automated \u2014 blank cells render as \u201cNot confirmed\u201d with a flag reference; no interpolation is performed.",
        "type": "machine",
        "state": "pass",
        "source": "policies",
    },
    {
        "id": "G-06",
        "check": "Intent fields and observed fields are stored separately",
        "why": "Merging them would let an observation become a claim without evidence.",
        "how": "Automated \u2014 the product record schema keeps intent_* and observed_* in disjoint columns.",
        "type": "machine",
        "state": "pass",
        "source": "agreement",
    },
    {
        "id": "G-07",
        "check": "Every page has a title, a description, a canonical and an RSS link",
        "why": "One canonical site with consistent metadata is what makes it indexable.",
        "how": "Automated \u2014 the checker verifies the head tags on every page.",
        "type": "machine",
        "state": "pass",
        "source": "pages",
    },
    {
        "id": "G-08",
        "check": "The sitemap and the feed contain every published page and guide",
        "why": "A guide that is not in the feed or the sitemap is a guide nobody finds.",
        "how": "Automated \u2014 the checker diffs the page list against sitemap.xml and feed.xml.",
        "type": "machine",
        "state": "pass",
        "source": "pages",
    },
    {
        "id": "G-09",
        "check": "The analytics collector is deployed, or it is not loaded at all",
        "why": "A tracker that posts to an endpoint that does not exist is worse than no tracker: it implies measurement that is not happening.",
        "how": "Human \u2014 confirm the endpoint responds before enabling the tracker site-wide.",
        "type": "human",
        "state": "pending",
        "source": "policies",
    },
    {
        "id": "G-10",
        "check": "Privacy notice published, describing what is actually collected",
        "why": "The IP License requires accurate and adequate disclosure of the use of cookies, pixels and other technologies and of how visitor data is collected, used, stored and disclosed.",
        "how": "Human \u2014 write the notice against the deployed collector's real behaviour, not the intended behaviour.",
        "type": "human",
        "state": "pending",
        "source": "policies",
    },
    {
        "id": "G-11",
        "check": "Endorsement context reviewed: the copy does not imply we used the product",
        "why": "The IP License forbids using Program Content in a way that implies a person's or company's endorsement. We have not handled these appliances, and the copy must not suggest that we have.",
        "how": "Human \u2014 read each product card as if you were the reader, and check the endorsement context.",
        "type": "human",
        "state": "pending",
        "source": "policies",
    },
    {
        "id": "G-12",
        "check": "One link per product tested inside the enrolled Associates workflow",
        "why": "Destination and tracking report must be confirmed before scaling.",
        "how": "Human \u2014 click, then check the account's own report, then record the date in the product-intent record.",
        "type": "human",
        "state": "pending",
        "source": "agreement",
    },
]

# --------------------------------------------------------------------------------------
# Executive summary
# --------------------------------------------------------------------------------------
EXEC_SUMMARY = {
    "situation": (
        "Five Amazon short links were supplied to market. Following each of them over HTTPS on "
        "20 November 2026 resolved four of them to specific Amazon product detail pages and sent the "
        "fifth to an Amazon checkpoint page. The five link tokens are nine characters long, and an "
        "Amazon Standard Identification Number is ten characters, so none of the supplied tokens is "
        "an ASIN. The site publishes canonical product links carrying the supplied tracking ID, and "
        "records the intent and the observation in separate fields."
    ),
    "findings": [
        (
            "Four destinations confirmed, one blocked",
            "CHEFMAN 6 Quart Dual Basket Air Fryer Oven (B0CDY277D3), Emeril Lagasse 26QT French Door "
            "Multi-Function Air Fryer Toaster Oven (B09B7SB46R), Chefman Air Fryer 8 Qt TurboFry 4-in-1 "
            "(B08DKYBTPH) and CHEF iQ Sense Gen3 wireless meat thermometer (B0DZFD6R9Z). The fifth "
            "short link returned an Amazon \u201cContinue shopping\u201d checkpoint and was not observed.",
            "https://www.amazon.com/dp/B0CDY277D3",
        ),
        (
            "One link is not an air fryer",
            "The link in slot 5 resolves to a wireless meat thermometer whose listing names air fryer "
            "among its uses. It is filed under Cooking tools and flagged as a scope question rather "
            "than presented as a cooker.",
            "https://www.amazon.com/dp/B0DZFD6R9Z",
        ),
        (
            "Tracking could not be confirmed, and that is a finding",
            "A control fetch of a URL that carried the supplied tracking ID returned a resolved URL "
            "with no tag parameter, which proves the fetch path used for this site normalises the tag "
            "away. So neither the presence nor the absence of a tag on the supplied links can be "
            "observed this way. The links are not called invalid; the question is open.",
            "https://affiliate-program.amazon.com/help/operating/agreement",
        ),
        (
            "Prices and ratings are deliberately absent from the shop",
            "Three prices were observed on 20 November 2026 and are recorded on the product records "
            "page as dated observations. Ratings could not be read at all, because Amazon's review "
            "pages redirect to sign-in. The reader-facing pages show no price and no rating, because "
            "the Associates IP License permits Product Advertising Content only through Creators API "
            "or PA API.",
            "https://affiliate-program.amazon.com/help/operating/policies",
        ),
        (
            "The measurement layer ships, deployed, honest",
            "A privacy-preserving tracker and a zero-dependency collector are in the repository. No "
            "endpoint is deployed, no report has been supplied, and the campaign ledger is empty. No "
            "click count, order count, conversion rate or revenue figure appears anywhere on this site.",
            "https://support.google.com/webmasters/answer/9128668",
        ),
    ],
    "decisions": [
        ("Confirm or replace the five destinations", "One click test per product inside the enrolled Associates workflow, with the destination and the tracking report recorded.", "S-01, S-02", "agreement"),
        ("Decide the scope of the thermometer record", "Keep a Cooking Tools category, or replace the record with a cooker.", "S-03", "asin"),
        ("Choose whether to connect the Product Advertising API", "A visible price is worth a real API connection; without one, the site shows none.", "S-05", "policies"),
        ("Deploy the collector and publish the privacy notice", "The tracker posts to /api/collect. Until that endpoint exists, it collects nothing and says so.", "S-04", "policies"),
        ("Get written approval before any assistant touches Amazon content", "The IP License restricts using Special Links and Program Content for machine learning without express prior written approval.", "S-14", "policies"),
    ],
    "done": [
        "Every published product link is a canonical Amazon product link carrying the supplied tracking ID, and is marked as a sponsored placement.",
        "The Associates disclosure sits above the masthead on every page and is repeated in the footer.",
        "Six question-shaped guides are published, each with a byline, dates, a cluster label and a note naming what is still unconfirmed.",
        "A product-intent confirmation record keeps the intended listing, the intended ASIN, the confirmation date and the source separate from the observed redirect target.",
        "A suggestions register, an open-questions register, a publishing gate and a flagged-for-review page are published for review.",
        "The build is automated: site pages are rendered from one data file, and scripts/check_site.py gates the result before deployment.",
    ],
}

# --------------------------------------------------------------------------------------
# Official reference for every suggestion row, so that every table row on the site
# carries a link to an official source.
# --------------------------------------------------------------------------------------
SUGGESTION_SOURCES = {
    "S-01": ["agreement"],
    "S-02": ["agreement", "policies"],
    "S-03": ["asin"],
    "S-04": ["policies"],
    "S-05": ["policies"],
    "S-06": ["ftc"],
    "S-07": ["ftc"],
    "S-08": ["ftc"],
    "S-09": ["gsc"],
    "S-10": ["gsc"],
    "S-11": ["policies"],
    "S-12": ["gsc"],
    "S-13": ["policies"],
    "S-14": ["policies"],
    "S-15": ["pages"],
}

# Reader-facing pages must never display a price, a rating, a review count or an
# availability claim. These are the patterns the publishing gate rejects.
FORBIDDEN_ON_READER_PAGES = [
    r"\$\s?\d",
    r"\d(?:\.\d)?\s*out of 5",
    r"\d[\d,]*\s*(?:global\s+)?ratings?\b",
    r"\b\d[\d,]*\s*(?:customer\s+)?reviews?\b",
    r"\bin stock\b",
    r"\bout of stock\b",
    r"\bcurrently available\b",
]

# Unsupportable claim language. Each entry is a pattern the reader-facing and desk
# pages are both checked against.
FORBIDDEN_CLAIMS = [
    r"\bbest overall\b",
    r"\bbest (?:air fryer|appliance|choice|pick|buy|value)\b",
    r"\bcheapest\b",
    r"\bmost popular\b",
    r"#1 (?:seller|pick|choice)",
    r"\bguaranteed to\b",
    r"\bgame[- ]changer\b",
    r"\byou need this\b",
    r"\bnumber one\b",
    r"\btrending\b",
    r"\blimited time\b",
]


# --------------------------------------------------------------------------------------
# Design direction. These are the instructions a designer or a design model should
# follow, written so they can be pasted straight into a prompt.
# --------------------------------------------------------------------------------------
DESIGN_DIRECTION = [
    ("Page archetype",
     "An editorial front page, not a dashboard. One lead story, three product cards, one "
     "comparison table, one seasonal band, one desk strip. A reader should know what to buy "
     "before they know what we have not verified."),
    ("Palette",
     "Warm paper (#faf8f3), deep sage-green ink (#22362d), a single terracotta accent "
     "(#c9603d), cream section bands (#f0eee4). No gradients beyond one soft hero wash, no "
     "neon, no glassmorphism."),
    ("Type",
     "A high-contrast serif for headlines and card titles, a neutral humanist sans for "
     "everything else. Headlines are sentence case. Never uppercase a whole sentence."),
    ("Card anatomy",
     "Every product card carries: brand, name, one-line format, a two-column body headed "
     "\u201cWhy it is on the shelf\u201d and \u201cWhere it might not suit you\u201d, a "
     "verification chip, and one outbound button. No badge walls, no star ratings, no "
     "\u201cbest overall\u201d ribbon."),
    ("Photography",
     "No stock photos of smiling families. Either a clean product silhouette or nothing. "
     "Amazon product imagery is Program Content and may only be used under the IP License, so "
     "it must arrive through the API, not through a page read."),
    ("Voice",
     "Second person, short sentences, concrete nouns. Explain the trade-off rather than "
     "declaring a winner. No exclamation marks, no \u201camazing\u201d, no \u201cgame-changer\u201d, "
     "no \u201cguaranteed\u201d."),
    ("Navigation",
     "One visible navigation group. Everything else lives in the footer. A single search "
     "affordance over the shelf table, not a site-wide search box."),
    ("Disclosure",
     "A full-width dark strip above the masthead on every page, always the same sentence, "
     "plus a repeat in the footer. It is part of the design, not a legal afterthought."),
    ("Tables",
     "One table per reader-facing page. Monospace for identifiers. Blank cells render as "
     "\u201cNot confirmed\u201d in italic, never as a dash and never with a guess."),
    ("Motion",
     "Under 200ms, opacity and transform only. Nothing that moves on scroll. Respect "
     "prefers-reduced-motion."),
    ("Imagery and rhythm",
     "Alternate dense and open sections. Use the seasonal band as a visual reset roughly "
     "every third screen so the page has a breathing rhythm."),
    ("What to avoid",
     "Stock-photo grids, fake urgency, countdown timers, rating stars the reader cannot "
     "verify, \u201ctop 10\u201d lists, comparison tables with an unearned winner column, and "
     "any layout that reads as machine-generated filler."),
]


# --------------------------------------------------------------------------------------
# Comparison dimensions. One row per dimension, one cell per product. Every value is
# taken from the listing the product record cites, and the row carries the source
# used. Dimensions we cannot source are deliberately absent rather than guessed.
# --------------------------------------------------------------------------------------
COMPARE = [
    ("Shape",
     {"B0CDY277D3": "Two pull-out baskets", "B09B7SB46R": "Front-door oven cabinet",
      "B08DKYBTPH": "One pull-out basket", "B0DZFD6R9Z": "Probe and base, no cooking cavity"},
     "Listing title"),
    ("What cooks at once",
     {"B0CDY277D3": "Two baskets, if the listed sync feature is used as described",
      "B09B7SB46R": "One cavity; racks may allow levels", "B08DKYBTPH": "One basket",
      "B0DZFD6R9Z": "Not applicable"},
     "Listing title"),
    ("Listed capacity",
     {"B0CDY277D3": "6 quart across two 3-quart baskets", "B09B7SB46R": "26 quart",
      "B08DKYBTPH": "8 quart", "B0DZFD6R9Z": "Not applicable"},
     "Listing title"),
    ("Listed programs",
     {"B0CDY277D3": "Air fry, Hi-Fry, auto shutoff", "B09B7SB46R": "24 one-touch presets",
      "B08DKYBTPH": "Air fry, bake, dehydrate, frozen", "B0DZFD6R9Z": "Not applicable"},
     "Listing title"),
    ("Cleaning as listed",
     {"B0CDY277D3": "Nonstick, dishwasher-safe baskets", "B09B7SB46R": "Not confirmed",
      "B08DKYBTPH": "Nonstick, dishwasher-safe basket", "B0DZFD6R9Z": "Not confirmed"},
     "Listing title"),
    ("Who it suits",
     {"B0CDY277D3": "Two people cooking different food at the same time",
      "B09B7SB46R": "One household cooking several things at once",
      "B08DKYBTPH": "One person cooking one dish, simply",
      "B0DZFD6R9Z": "Anyone cooking outdoors or wanting a reading in the kitchen"},
     "Editorial, from the listing facts above"),
    ("Counter footprint to check",
     {"B0CDY277D3": "Wide and shallow; the drawer pulls toward you",
      "B09B7SB46R": "Deep; the front door needs clearance in front of it",
      "B08DKYBTPH": "Standard single-drawer footprint",
      "B0DZFD6R9Z": "Small base, plus a receiver that stays in view"},
     "Editorial, from the shape of each format"),
]

COMPARE_NOTES = [
    "Deliberately not compared: which one cooks better. We have not used them.",
    "Deliberately not compared: which one is worth the money. We do not publish prices.",
    "Deliberately not compared: which one is more popular. No review or sales data was obtained.",
]
