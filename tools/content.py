"""Reader-facing prose. Kept separate from layout so the words can be edited
without touching the templates.

Editorial rule for every guide here: the only product facts that may appear are
the ones transcribed in src/data/products.json from a listing title the site
actually reached, and the only food-safety figures that may appear are quoted
from USDA FSIS (SRC-06, SRC-07). No price, no rating, no review count, no test
result, no superlative, no winner.
"""

GUIDES = [
    {
        "slug": "basket-or-oven-air-fryer",
        "kicker": "Air fryers · choosing a shape",
        "category": "air-fryers",
        "title": "Basket or oven-style air fryer: what should you compare?",
        "dek": "Two appliances share a name and almost nothing else. Here is the list of differences that actually change how a weeknight goes — and the ones that only look like they do.",
        "read_minutes": 7,
        "photo": "assets/img/format-basket",
        "photo_alt": "Golden potato wedges being lifted out of the drawer of an unbranded basket-style air fryer",
        "photo_caption": "Illustration of a basket-style drawer, not a photograph of a product on this site.",
        "updated": "2026-11-20",
        "related_refs": ["P-01", "P-02", "P-03"],
        "sections": [
            {
                "h": "The difference is the shape of the space, not the badge",
                "p": [
                    "A basket fryer gives you one deep container (or two side-by-side drawers). Food goes in, the drawer closes, and a fan moves hot air over it. An oven-style fryer gives you a shallow cavity with racks and a front door or pair of French doors that swing outward.",
                    "That is the whole of it. Everything a shopper cares about afterwards — how much fits, how often you intervene, where it lives on the counter, what needs washing — follows from those shapes rather than from the brand or the preset count on the front."
                ]
            },
            {
                "h": "What actually changes between them",
                "items": [
                    ("Batch shape", "A basket holds one pile; a dual-basket splits two foods at once; an oven holds flat layers. If you cook for four, the difference is whether one round of food is enough or whether you are running the machine twice."),
                    ("Intervention", "Basket cooking usually means pulling the drawer and shaking. Rack cooking usually means turning pieces and sometimes swapping shelf positions. Neither is universally simpler; pick the motion you actually tolerate."),
                    ("Front clearance", "A door that swings outward needs open space in front of the machine, which is usually the exact strip of counter where you prep."),
                    ("Vertical clearance", "A basket needs room above or beside it to lift the drawer out comfortably. An oven needs ventilation clearance above and behind, per its manual."),
                    ("What you can put in it", "A shallow oven cavity accepts a pan, a small baking dish or a plate. A deep basket mostly accepts loose food. If you plan to bake or reheat plated dishes, this is the deciding split."),
                    ("Washing", "A single basket is usually two pieces (drawer plus crisper plate). A dual-basket doubles that. An oven ships with trays, racks and accessories — each one a separate item to wash and store.")
                ]
            },
            {
                "h": "The three measurements to take before you choose",
                "p": [
                    "Do this with a tape measure, not with a guess. It takes four minutes and rules out most of the wrong answers.",
                    "Measure the width and depth of the counter spot including drawer pull-out or door swing, the vertical height from counter to the underside of the upper cabinet, and the distance to the nearest outlet so the cord never crosses a sink or burner.",
                    "If a dimension you need is missing from the official listing or manual, write 'unknown' beside it and check the manufacturer documentation before buying."
                ]
            },
            {
                "h": "How the three air fryers in this register illustrate the split",
                "p": [
                    "The three air fryers in this site's verified register span all three countertop shapes, using only the sellers' own title wording.",
                    "P-01 (CHEFMAN) is described as a 6-quart dual-basket air fryer with two independent 3-quart baskets, Easy View windows and Sync Finish. P-03 (Chefman TurboFry) is described as a single 8-quart basket with a 450°F Hi-Fry option. P-02 (Emeril Lagasse) is described as a 26-quart French-door multi-function air fryer toaster oven with 24 presets and six accessories.",
                    "Read those three descriptions together and the trade is plain: one single big basket, two smaller parallel baskets, or one wide shallow oven cavity. None of the three has been tested here, so no winner is declared."
                ]
            },
            {
                "h": "A short way to decide",
                "p": [
                    "Write down the meal you cook most often and how many people eat it. Then answer one question: does that meal fit in a deep container, need two separate temperatures at once, or need to lie flat on a tray?",
                    "Once you pick the shape, verify the external dimensions against your counter tape test and stop. Extra presets will not rescue the wrong geometry."
                ]
            }
        ],
        "closing": "No product on this site was tested, ranked or scored. Descriptions of P-01, P-02 and P-03 are the sellers' own wording, transcribed from the live listings verified on 2026-11-20."
    },
    {
        "slug": "instant-read-vs-wireless-meat-thermometer",
        "kicker": "Meat thermometers · choosing a probe",
        "category": "thermometers",
        "title": "Instant-read or wireless probe: which meat thermometer fits how you cook?",
        "dek": "An air fryer controls time and heat, not internal doneness. Here is how handheld instant-read probes differ from leave-in wireless probes — paired with the official USDA safe minimum internal temperature chart.",
        "read_minutes": 6,
        "photo": "assets/img/instant-thermometer",
        "photo_alt": "An unbranded folding digital instant-read meat thermometer resting beside a seared chicken breast on a wooden board",
        "photo_caption": "Illustration of an instant-read folding probe, not a photograph of P-04 or P-05.",
        "updated": "2026-11-20",
        "related_refs": ["P-04", "P-05"],
        "sections": [
            {
                "h": "Why visual cues fail — especially in an air fryer",
                "p": [
                    "High-velocity hot air browns the outside of chicken thighs, pork chops and burger patties quickly. Brown skin or firm edges feel finished long before the center reaches a safe internal temperature.",
                    "The USDA Food Safety and Inspection Service (FSIS) states plainly that color is not a reliable indicator of safety and that using a food thermometer is the only reliable way to verify food has reached a safe minimum internal temperature (SRC-07). The same principle prevents overcooking: stopping at the target number keeps lean cuts from drying out."
                ]
            },
            {
                "h": "Two tools built for two different habits",
                "items": [
                    ("Instant-read handheld probe (e.g., P-04)", "You open the drawer or oven, insert the probe into the thickest part away from bone, read the screen and pull it out. No app, no pairing, no charging dock to manage. Best for weeknight chicken breasts, fish, burgers and quick spot-checks across multiple pieces."),
                    ("Leave-in wireless multi-probe (e.g., P-05)", "Thin probes stay inside the food throughout the cook and send readings to a base or phone app. Best for thick roasts, whole poultry or multi-item cooks where opening the door repeatedly dumps heat and breaks your rhythm."),
                    ("Dependence trade-off", "A handheld probe works the instant you unfold it. A smart wireless kit adds charging, app updates and wireless range to your routine — worth it only if you actually cook cuts that stay in heat long enough to monitor continuously.")
                ]
            },
            {
                "h": "Official USDA safe minimum internal temperature chart",
                "p": [
                    "Every figure below is transcribed directly from the USDA FSIS Safe Minimum Internal Temperature Chart (last updated April 14, 2025; SRC-06). Insert the probe into the thickest part of the food, away from bone, fat or gristle (SRC-07)."
                ],
                "table": {
                    "caption": "USDA FSIS Safe Minimum Internal Temperatures (verified 2026-11-20, SRC-06)",
                    "headers": ["Food", "Minimum internal temperature & rest time"],
                    "rows": [
                        ["Beef, pork, veal and lamb steaks, chops and roasts", "145°F (62.8°C) and allow to rest for at least 3 minutes"],
                        ["Ground meats (beef, pork, veal, lamb)", "160°F (71.1°C)"],
                        ["All poultry (breasts, whole bird, legs, thighs, wings, ground poultry, stuffing)", "165°F (73.9°C)"],
                        ["Eggs", "160°F (71.1°C)"],
                        ["Fish and shellfish", "145°F (62.8°C)"],
                        ["Leftovers and casseroles", "165°F (73.9°C)"],
                        ["Ham, fresh or smoked (uncooked)", "145°F (62.8°C) and allow to rest for at least 3 minutes"]
                    ]
                }
            },
            {
                "h": "What the two thermometer listings in this register state",
                "p": [
                    "Two of the five submitted links in this catalogue are meat thermometers filed under Thermometers & Timers > Meat on Amazon.",
                    "P-04 (ThermoMaven, ASIN B0DHZTCNR5) is described by its seller as a 1-second digital meat thermometer with stated ±0.5°F accuracy, NIST and NSF certification, an auto-rotating LED display and IP67 waterproofing.",
                    "P-05 (CHEF iQ Sense, ASIN B0DZFD6R9Z) is described by its seller as a Gen3 smart wireless meat thermometer with three ultra-thin probes, WiFi unlimited range, five sensors, a 1000°F heat-safe rating and air fryers explicitly listed among intended uses.",
                    "Every specification above is the seller's listing language — neither thermometer has been calibrated, timed or tested by this site."
                ]
            },
            {
                "h": "Five questions to check before buying either format",
                "items": [
                    ("Which cuts do you cook weekly?", "If you cook thin cuts, chicken tenders or burgers in 10–15 minutes, a fast instant-read probe gets used daily. If you roast whole chickens or thick joints, a leave-in wireless probe earns its keep."),
                    ("Does a leave-in probe fit your air fryer safely?", "Check both the air fryer manual and the probe manual for maximum temperature limits and basket-clearance rules before shutting a drawer over a probe."),
                    ("Does the smart kit work without your phone?", "Check whether the dock shows live temperatures on its own or forces an app every time."),
                    ("How is the probe cleaned?", "Waterproof ratings vary between the probe tip, handle and charging dock. Read the manufacturer care instructions rather than assuming dishwasher safety."),
                    ("How will you verify accuracy?", "Manufacturer accuracy claims can be checked at home against an ice-water bath once you own the thermometer; this site has not verified either seller's claim.")
                ]
            }
        ],
        "closing": "Safe minimum internal temperatures are sourced directly from USDA FSIS (SRC-06, SRC-07). Product attributes for P-04 and P-05 are transcribed from their Amazon listing titles on 2026-11-20; neither unit was tested."
    },
    {
        "slug": "air-fryer-capacity-checklist",
        "kicker": "Air fryers · sizing",
        "category": "air-fryers",
        "title": "A no-hype checklist for comparing air-fryer capacity",
        "dek": "The quart figure on the box answers a question you did not ask. Here is how to translate volume into single-layer cooking surface before you buy.",
        "read_minutes": 6,
        "photo": "assets/img/capacity",
        "photo_alt": "Food laid out in a single layer on a counter next to a tape measure",
        "photo_caption": "Illustration. The food and the tape are props, not a measurement of any product.",
        "updated": "2026-11-20",
        "related_refs": ["P-01", "P-02", "P-03"],
        "sections": [
            {
                "h": "A quart is a volume. You cook with a surface.",
                "p": [
                    "Capacity is quoted as a volume because a volume is one number and numbers fit neatly on boxes. But hot air needs to circulate around the food, and food piled deep traps steam where pieces touch.",
                    "So the useful question is not 'how many quarts' but 'how much food sits in a single layer with space around it'. Those two questions have very different answers, and the second one is rarely printed on the front."
                ]
            },
            {
                "h": "Six steps to size it accurately",
                "items": [
                    ("1. Pick one real Tuesday meal", "Not 'dinner' in the abstract. Write down the exact meal: six chicken thighs, a pound of broccoli florets, two salmon fillets."),
                    ("2. Count the pieces", "Convert the meal into a concrete footprint you can compare against a basket or tray."),
                    ("3. Look for usable basket or tray dimensions", "Interior width and depth in the manufacturer manual matter more than the headline quart number."),
                    ("4. Decide if it must sit in a single layer", "Roasted vegetables and breaded cutlets need space; frozen fries tolerate shaking. Your single-layer meal sets your real minimum size."),
                    ("5. Count the batches honestly", "If your usual meal needs two rounds, write 'two batches' as the real cost — and decide whether you mind waiting."),
                    ("6. Check exterior footprint against your counter", "Bigger interior always means bigger exterior. Confirm the machine fits both your counter and your sink before ordering.")
                ]
            },
            {
                "h": "What the three air-fryer listings in this register state",
                "p": [
                    "All five submitted links in this register are now verified: three are air fryers (P-01, P-02, P-03) and two are meat thermometers (P-04, P-05, which have no cooking volume to compare).",
                    "The three air-fryer titles state: 6 quarts total split across two independent 3-quart baskets (P-01), 8 quarts in a single XL basket (P-03), and 26 quarts inside a French-door countertop oven (P-02).",
                    "Notice the hidden split: a 6-quart dual-basket machine does not hold a 6-quart roast — it holds two separate 3-quart portions. Compare each 3-quart drawer against an 8-quart single basket, not 6 against 8."
                ]
            },
            {
                "h": "When the quart number is enough",
                "p": [
                    "If you cook for one or two, mostly loose ingredients, and do not mind running a second batch once in a while, almost any standard basket capacity works.",
                    "This checklist earns its keep when three constraints collide: cooking for three or more, food that must lie flat, and tight counter space."
                ]
            }
        ],
        "closing": "Capacity figures quoted above are transcribed from listing titles verified on 2026-11-20. No basket or cavity was physically measured."
    },
    {
        "slug": "cleanup-and-counter-space",
        "kicker": "Air fryers · everyday cost",
        "category": "air-fryers",
        "title": "How to assess cleanup and counter-space trade-offs",
        "dek": "The appliance that gets used four nights a week is the one that fits your sink and stays out on the counter. Both are checkable in five minutes.",
        "read_minutes": 5,
        "photo": "assets/img/cleanup",
        "photo_alt": "An unbranded air-fryer basket and tray in a sink with a brush and a cloth",
        "photo_caption": "Illustration of the washing-up step, not a photograph of any product here.",
        "updated": "2026-11-20",
        "related_refs": ["P-01", "P-02", "P-03"],
        "sections": [
            {
                "h": "Count the washable parts before counting features",
                "p": [
                    "An air fryer's real price is paid after dinner in sink time and counter clutter. That cost is set by how many removable parts collect grease and how large they are.",
                    "A single-basket fryer usually has one basket and one crisper plate. A dual-basket doubles that to four pieces. A French-door oven adds wire racks, baking trays and drip pans — and a full-width tray can easily be wider than a compact sink basin."
                ]
            },
            {
                "h": "Four questions that predict whether it stays out or enters a cupboard",
                "items": [
                    ("Does the largest removable piece lie flat in your sink?", "A tray that has to be washed diagonally splashes water everywhere and discourages daily use."),
                    ("Does it live on the counter permanently?", "If it has to be lifted down from a high cupboard before every meal, check its weight in the manual before assuming you will reach for it."),
                    ("What leaves the counter to make room?", "If you cannot name the item that moves, you have not made space — you have just shrunk your prep area."),
                    ("Where is the outlet?", "Check cord length and keep cords away from wet sink zones and hot burners.")
                ]
            },
            {
                "h": "Dishwasher-safe is a seller phrase until you read the manual",
                "p": [
                    "Both P-01 (CHEFMAN 6 Qt dual basket) and P-03 (Chefman 8 Qt TurboFry) describe their nonstick baskets as dishwasher-safe in their listing titles, and P-02 states six included accessories. Treat any title claim as a starting point, then verify rack placement and detergent rules in the official manual so coatings last.",
                    "External dimensions are deliberately left blank on this site because they were not confirmed from official spec sheets in this build — check the manufacturer manual before cutting your layout test."
                ]
            },
            {
                "h": "The five-minute paper-rectangle test",
                "p": [
                    "Cut a piece of scrap paper or lay painter's tape on your counter to match the published footprint of the model you are considering, plus door swing or drawer pull-out. Leave it there for two days while cooking normally.",
                    "If you keep stepping around it or sliding a kettle out of the way, tape just saved you a return."
                ]
            }
        ],
        "closing": "No product on this site was tested. Seller-stated attributes are labelled as such wherever they appear."
    },
    {
        "slug": "batch-cooking-air-fryer-formats",
        "kicker": "Meal prep · workflow",
        "category": "air-fryers",
        "title": "Sunday meal prep: how basket, dual-zone and oven fryers change batch timing",
        "dek": "Batch cooking fails on sequencing, not recipes. Compare one 8-quart basket, two 3-quart drawers, and one 26-quart rack cavity against your actual weekly menu.",
        "read_minutes": 5,
        "photo": "assets/img/format-oven",
        "photo_alt": "An unbranded French-door countertop oven open on roasted vegetables",
        "photo_caption": "Illustration of an oven-style countertop cavity, not a photograph of P-02.",
        "updated": "2026-11-20",
        "related_refs": ["P-01", "P-02", "P-03"],
        "sections": [
            {
                "h": "Meal prep is a scheduling problem",
                "p": [
                    "Most Sunday prep plans stall when two components want different temperatures at the same time — say marinated chicken thighs and roasted broccoli. The right appliance shape depends on whether you batch one food in volume or cook two foods in parallel."
                ]
            },
            {
                "h": "Three countertop shapes, three Sunday routines",
                "items": [
                    ("Dual-basket (P-01 — seller-stated 6 Qt across two 3 Qt drawers)", "Built for parallelism: protein in one basket, vegetables in the other, using seller-stated Sync Finish so both end together. The trade-off is smaller individual drawer size (3 Qt each) and twice the basket surfaces to wash."),
                    ("French-door oven (P-02 — seller-stated 26 Qt cavity, 6 accessories)", "Built for flat sheet-pan volume: wide racks handle full trays of vegetables or multiple meal-prep proteins without splitting into tiny rounds. The trade-off is counter depth, door swing and rack cleanup."),
                    ("Single-basket (P-03 — seller-stated 8 Qt basket)", "Built for simplicity: one generous drawer for big batches of one ingredient at a time, then a fast wipe before the next round. The trade-off is sequential timing — dish two waits while dish one cools.")
                ]
            },
            {
                "h": "A five-minute rehearsal before you buy",
                "items": [
                    ("List your real weekly prep", "Write down the exact three components you cook most Sundays."),
                    ("Count simultaneous zones needed", "If two items need different temperatures right now, dual-zone shines. If one big tray is your bottleneck, oven racks win."),
                    ("Plan the cool-down counter space", "Hot baskets and racks need a trivet or cutting board immediately — include that staging spot in your counter measurement."),
                    ("Check doneness, not just timers", "Batch thickness varies from piece to piece; verify thick proteins with a food thermometer to the USDA safe minimum temperature (SRC-06) before boxing lunches.")
                ]
            }
        ],
        "closing": "Working title — not a claim about popularity, search volume or product superiority. No product on this site was tested; format attributes are quoted from live listings verified on 2026-11-20."
    },
    {
        "slug": "holiday-roast-and-air-fryer-playbook",
        "kicker": "Seasonal · hosting",
        "category": "thermometers",
        "title": "Hosting without oven gridlock: pairing a countertop fryer with a meat thermometer",
        "dek": "When the main oven is tied up by a roast, a countertop fryer handles crisp sides while a probe thermometer removes the guesswork from poultry and roasts.",
        "read_minutes": 5,
        "photo": "assets/img/holiday-hosting-counter",
        "photo_alt": "An unbranded matte-black air fryer beside roasted root vegetables and green beans on a wooden kitchen counter in winter light",
        "photo_caption": "Illustration of a holiday kitchen counter, not a photograph of any product sold here.",
        "updated": "2026-11-20",
        "related_refs": ["P-02", "P-04", "P-05"],
        "sections": [
            {
                "h": "Two bottlenecks ruin holiday timing — and neither is the recipe",
                "p": [
                    "Big dinners jam on two things: everything wants the main oven at a different temperature in the last 30 minutes, and nobody is sure whether the roast or bird is actually done without slicing it open.",
                    "That is why the five products in this catalogue pair naturally into two categories: three countertop air fryers that offload side dishes or reheating, and two meat thermometers that verify safe internal temperature without cutting into the meat."
                ]
            },
            {
                "h": "How to split the jobs cleanly",
                "items": [
                    ("Offload crisp sides to the countertop", "Brussels sprouts, root vegetables, dinner rolls or reheated appetizers can run in a countertop fryer while the main oven holds the centerpiece roast — or while the centerpiece rests."),
                    ("Use the rest window on purpose", "USDA FSIS specifies at least a 3-minute rest after whole cuts of beef, pork, veal or lamb reach 145°F (SRC-06), and larger roasts rest longer before carving. That rest window is free time for crisp sides."),
                    ("Check poultry to 165°F in the thickest spot", "USDA FSIS requires 165°F (73.9°C) for all poultry — whole birds, breasts, thighs, wings and stuffing — measured away from bone (SRC-06, SRC-07)."),
                    ("Pick your probe style for the dish", "A leave-in wireless multi-probe kit (like P-05, seller-stated 3 probes and WiFi range) lets you watch multiple spots in a large roast without opening the oven door; an instant-read probe (like P-04, seller-stated 1-second read) verifies side dishes, stuffing and pan cuts in seconds.")
                ]
            },
            {
                "h": "Pre-hosting electrical & space check",
                "p": [
                    "High-draw kitchen appliances can trip a shared breaker if a countertop oven, kettle and warming tray all run on the same circuit at once. Check your outlet circuits and counter landing zones a day before guests arrive — not ten minutes before dinner."
                ]
            }
        ],
        "closing": "Safe minimum internal temperatures and rest times are cited directly from USDA FSIS (SRC-06, SRC-07). Product capabilities are seller-stated from Amazon listings verified on 2026-11-20; no appliance or thermometer was tested."
    },
    {
        "slug": "multi-function-kitchen-appliance-questions",
        "kicker": "Before you buy · checklist",
        "category": "air-fryers",
        "title": "Questions to ask before buying a multi-function kitchen appliance",
        "dek": "Multi-function usually means one thing done well and several things done acceptably. The trick is finding out which is which before it claims a shelf.",
        "read_minutes": 6,
        "photo": "assets/img/multifunction",
        "photo_alt": "An unbranded basket air fryer, countertop oven and probe thermometer on one counter",
        "photo_caption": "Illustration of three appliance shapes, none of them a product sold here.",
        "updated": "2026-11-20",
        "related_refs": ["P-02", "P-03", "P-05"],
        "sections": [
            {
                "h": "Start by naming the one job",
                "p": [
                    "Every multi-function appliance has a job it was built around and a list of extra jobs it will attempt. The list is what the box advertises; the one job is what you will actually run on a Wednesday night.",
                    "Finish one sentence before shopping: 'I want this to make ___ easier.' If you cannot finish it without listing four unrelated dishes, two simpler tools often serve you better."
                ]
            },
            {
                "h": "Nine questions, in the order that saves time",
                "items": [
                    ("What is the primary job, in the seller's own words?", "The first clause of a listing title usually states the core machine. Everything after the pipe or comma is the ambition."),
                    ("How many functions need separate accessories?", "If three advertised modes require extra racks or pans stored in a drawer, you bought a machine plus a storage problem."),
                    ("What does the manual say about each mode?", "Presets are buttons that pick a default time and temperature; they do not guarantee results."),
                    ("How large is it, and where does it live?", "An appliance that does eight things from the back of a closet does zero things."),
                    ("How many pieces come out to wash?", "Count the cleanup for your weekly meal, not a once-a-year holiday dish."),
                    ("Does it need clearance above or in front?", "Swing doors and lift drawers consume active counter space."),
                    ("What does the actual warranty cover?", "Read the warranty terms before relying on a box claim."),
                    ("Can you replace worn baskets or trays?", "Spare-part availability decides whether a small appliance lasts years or months."),
                    ("Would a single-purpose tool pair better?", "Sometimes a straightforward air fryer paired with an independent meat thermometer beats an appliance claiming built-in smart modes.")
                ]
            },
            {
                "h": "The preset trap",
                "p": [
                    "A high preset count is the easiest number to print on a box and the least informative. Twenty-four presets can be twenty-four time-and-temperature combinations on the same heating element.",
                    "Look past the preset headline to the physical constraints you cannot change later: cavity size, rack positions, door swing and included pans."
                ]
            },
            {
                "h": "Why a standalone thermometer beats a built-in guess",
                "p": [
                    "Two of the five products in this catalogue (P-04 instant-read and P-05 wireless 3-probe) are dedicated meat thermometers. A standalone probe does one job — reading internal temperature — and travels cleanly between an air fryer, main oven, skillet and grill.",
                    "That single-purpose flexibility is often a smarter upgrade than chasing a more complex cooking appliance."
                ]
            }
        ],
        "closing": "No product on this site was tested, ranked or scored. Attributes referenced above are transcribed from live Amazon listings verified on 2026-11-20."
    }
]

# Column legend for the comparison page.
COMPARE_COLUMNS = [
    ("Product", "The register reference and the brand as stated on the listing"),
    ("Category", "Air Fryers or Meat Thermometers — read directly from Amazon's breadcrumb"),
    ("Shape", "Basket, oven, instant-read or wireless probe — read from the listing title"),
    ("Stated capacity", "Exactly as the seller words it. Not measured"),
    ("Stated attributes", "Only what the listing title itself claims"),
    ("Listing", "The destination the submitted link actually reached"),
]
