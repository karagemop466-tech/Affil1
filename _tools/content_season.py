"""Three guides added by session arena/ddb6772b-affil1, 2026-11-20.

A fourth, "Reheating leftovers so the outside is not the only hot part", was dropped
in the rebase that merged this branch with main, because arena/3d6a7607-affil1 had
already published "reheating-thanksgiving-leftovers" on the same FSIS pages. Two
guides answering one question is the duplication this project spent a consolidation
pass removing, so the newer copy yields rather than the register growing a twin.


Editorial rule, inherited from content.py and unchanged here:

  * no product fact appears unless it is already transcribed in
    _src/data/products.json from a listing this project reached. The wording is
    attributed to the listing and never restated as our finding;
  * no price, rating, review count, availability, test result, score or
    superlative appears anywhere;
  * every food-safety number is transcribed on 2026-11-20 from a US government
    page, and each guide carries a table whose rows link to that page, so the
    claim and its document sit in the same row;
  * nothing here is medical or regulatory advice. It is the published public
    guidance, quoted with its source, for people deciding what to cook in what.

Voice rule, also inherited: write to the person deciding, in the second person.
Keep the machinery of verification out of the reading path; the provenance lives
one click away on the product page.
"""

FSIS_TEMP_CHART = "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart"
FSIS_THERMOMETERS = "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers"
FSIS_LEFTOVERS = "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety"
FSIS_TURKEY = "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/poultry/turkey-farm-table"
FSIS_THANKSGIVING = "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/poultry/your-safe-thanksgiving-guide"
FDA_TEMPERATURES = "https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures"

RETRIEVED = "Each government page below was opened on 2026-11-20 and read from that page. Publication dates are the pages' own."

GUIDES = [
    {
        "slug": "thanksgiving-air-fryer-timing",
        "cluster": "Seasonal",
        "kicker": "Holiday timing",
        "title": "Thanksgiving without the oven traffic jam: what to move, and what never leaves",
        "dek": "A countertop fryer will not save the bird. It can take four sides, the rolls and the reheating off an oven that is already busy for hours. Here is the plan, in the order you actually make it.",
        "read_minutes": 8,
        "photo": "assets/img/holiday-table",
        "photo_alt": "A holiday table with serving dishes and a countertop air fryer at the edge of the frame",
        "photo_caption": "An editorial illustration for holiday timing. It is not a photograph of any model sold on this site.",
        "updated": "2026-11-20",
        "related": ["P-02", "P-01", "P-05"],
        "sections": [
            {
                "h": "Plan backward from the bird, not forward from the appliance",
                "p": [
                    "The fixed point on Thanksgiving is the turkey, and the government guidance around it is not negotiable by schedule: a whole turkey is safe when it reaches a minimum internal temperature of 165°F measured with a food thermometer, checked in the innermost part of the thigh, the innermost part of the wing and the thickest part of the breast. The cooking timetable published with that advice assumes a 325°F oven, and it is written to be used alongside a thermometer rather than instead of one.",
                    "So the useful question is not \u201ccan the air fryer cook dinner\u201d. It is \u201cwhich dishes do not need to be under 325°F dry heat for an hour, and can therefore leave the big oven entirely?\u201d Write the menu in two columns before you touch a specification sheet.",
                ],
            },
            {
                "h": "Two columns: under 165\u00b0F or near it",
                "p": [
                    "Column one is everything that has to hold one temperature for a long time: the bird, a gratin that needs to set, a pie that cannot be rushed. That column stays in the main oven. There is no clever workaround, and a countertop cavity does not change the arithmetic.",
                    "Column two is anything already cooked that only needs to be crisped, browned or driven back up to temperature: roasted vegetables that went soft, rolls, potatoes with a crust on top, frozen appetisers, bacon, leftover mash with something browned on it. That column is where a second heat source earns its counter space.",
                    "One line belongs in column two even if it surprises you: reheated leftovers. The federal guidance for leftovers is to reheat them to 165°F, covered, and to bring sauces, soups and gravies to a rolling boil. A small hot cavity reaching that temperature quickly is doing exactly the job the guidance asks for.",
                ],
                "items": [
                    ("What the appliance cannot take over", "Anything whose doneness you cannot verify with a probe, and anything bigger than the cooking surface you measured before you bought it."),
                    ("What it can genuinely take over", "Dishes whose finish is the point: browning, crisping, and reheating a single portion at a time."),
                    ("What it changes about the day", "One less thing competing for a rack and one temperature. That is the whole pitch, and it is enough."),
                ],
            },
            {
                "h": "The numbers that anchor the schedule",
                "p": [
                    "None of these come from a listing or from us. They are the published figures, transcribed from the page named in the last column on 2026-11-20. If your copy of a manual disagrees with a number here, the manual is about your appliance and this table is about food \u2014 check both.",
                ],
                "table": {
                    "caption": "Safe minimum internal temperatures used in this plan, as published on 2026-11-20",
                    "headers": ["Situation", "Published figure", "Official source"],
                    "rows": [
                        ["All poultry, including whole bird and breasts", "165°F, measured with a food thermometer",
                         {"url": FSIS_TEMP_CHART, "label": "USDA FSIS \u2014 Safe Minimum Internal Temperature Chart"}],
                        ["Stuffing cooked inside a bird", "165°F at the centre of the stuffing; FSIS advises not stuffing whole poultry for optimum safety",
                         {"url": FSIS_TURKEY, "label": "USDA FSIS \u2014 Turkey from Farm to Table"}],
                        ["Leftovers, reheated", "165°F, covered; sauces and gravies to a rolling boil",
                         {"url": FSIS_LEFTOVERS, "label": "USDA FSIS \u2014 Leftovers and Food Safety"}],
                        ["Hot food held before eating", "140°F or above, and no longer than 2 hours out",
                         {"url": FSIS_LEFTOVERS, "label": "USDA FSIS \u2014 Leftovers and Food Safety"}],
                        ["Thawed turkey, held before cooking", "1 to 2 days in the refrigerator; allow about 1 day per 4\u20135 pounds to thaw",
                         {"url": FSIS_TURKEY, "label": "USDA FSIS \u2014 Turkey from Farm to Table"}],
                        ["Cooked turkey, stored", "3 to 4 days refrigerated; 4 months frozen (quality guidance)",
                         {"url": FSIS_TURKEY, "label": "USDA FSIS \u2014 Turkey from Farm to Table"}],
                    ],
                },
            },
            {
                "h": "Read a listing for the three things that matter on the day",
                "p": [
                    "Preset counts are noise; a preset is a saved time and temperature you can set by hand. Ignore them and look for three properties, each of which only matters if the listing states it for the model you are reading.",
                    "First, whether the cavity takes a flat tray at all. The 26-quart figure on the French-door machine in this edit is a cavity volume in the seller's own words \u2014 it is not a promise that your sheet pan fits, and it never will be. Second, whether the baskets or racks can run independently and finish together: the dual-basket listing here states two independent 3-quart baskets and a sync-finish function, in the seller's wording, which is the feature that matters when you are landing four dishes in one window. Third, whether you can see the food without opening it \u2014 the same listing words that as viewing windows.",
                    "If a property is not stated on the listing you have open, treat it as unknown. Do not import it from a review, a comment, or another model with a similar name.",
                ],
            },
            {
                "h": "A timing sheet you can fill in in five minutes",
                "items": [
                    ("Sit-down time", "Write the hour people eat. Everything else is derived from it."),
                    ("Bird out and resting", "The turkey guidance is to let the bird stand before carving. That window is free oven space \u2014 and the busiest twenty minutes for the second appliance."),
                    ("The two hottest sides", "Pick the two dishes that are ruined by going soft. Those are the ones that go in the countertop fryer last, not first."),
                    ("The reheat run", "Anything that was made ahead and needs to hit 165°F gets the final batch. Cover it, check it with a probe, and do not guess."),
                    ("The queue check", "Count your batches against your dishes. If the plan needs three sequential loads for four side dishes, you are not saving time. Move a dish back to the oven or change the menu."),
                ],
            },
            {
                "h": "Where this becomes a thermometer question",
                "p": [
                    "Every load-bearing number in this guide is measured with a probe, in the middle of food, at a moment when you are tired and the kitchen is full. That is the honest case for buying a thermometer alongside \u2014 or instead of \u2014 a second appliance. An instant-read answers \u201cis this safe yet\u201d; a leave-in probe answers \u201chow close am I\u201d, which is the one you want when the oven is blocked by a roasting pan.",
                    "The two products in this edit that address that are P-04, described by its listing as a digital meat thermometer, and P-05, described as a wireless meat thermometer whose stated uses include air frying. Neither is an air fryer, and this site has not cooked with either.",
                ],
            },
        ],
        "closing": "Nothing on this site was tested, ranked or scored. Product descriptions are sellers' wording from listings reached on 2026-11-20; the food-safety figures are transcribed from the USDA pages linked in the table. For cooking a turkey, the FSIS pages named above are the authority, not this guide.",
    },
    {
        "slug": "where-to-put-the-probe",
        "cluster": "Tools",
        "kicker": "Technique",
        "title": "Where to put the thermometer probe, and why colour is not doneness",
        "dek": "The most common thermometer error is not the thermometer. It is the placement, the assumption that a brown exterior means a safe interior, and a probe left somewhere it was never designed to stay.",
        "read_minutes": 7,
        "photo": "assets/img/instant-read",
        "photo_alt": "A digital instant-read thermometer held over a cooked chicken breast on a board",
        "photo_caption": "An editorial illustration of a handheld thermometer. It is not a photograph of a model sold on this site.",
        "updated": "2026-11-20",
        "related": ["P-04", "P-05"],
        "sections": [
            {
                "h": "Placement is the part that gets the reading wrong",
                "p": [
                    "A thermometer is only right if it is in the right place. The published guidance is specific: put the probe in the thickest part of the food, away from bone, fat and gristle. For thin food \u2014 a burger patty, a thin chicken breast, a pork chop \u2014 insert it sideways through the side until the sensing area reaches the centre, which for a typical instant-read is roughly 2 to 3 inches.",
                    "For a whole bird, one spot is not enough: check the innermost part of the thigh, the innermost part of the wing, and the thickest part of the breast. For anything large or irregularly shaped, check in several places. And check each piece, because size and how food is distributed in the appliance means pieces reach a safe temperature at different times.",
                ],
            },
            {
                "h": "Why a brown exterior proves nothing",
                "p": [
                    "Colour and firmness are the signals people actually use, and they are the ones the guidance warns against. Some ground meat turns brown on the outside well before the inside is safe. In a USDA study of consumers grilling, 21% of participants relied on visual cues such as colour and grill marks to judge whether patties were done. The published position is that the only way to know food has reached a safe internal temperature is a food thermometer \u2014 a patty cooked to 160°F is safe regardless of colour.",
                    "There is a related trap for anyone reading appliance marketing: an air fryer's browning is a surface reaction. It tells you about the surface.",
                ],
            },
            {
                "h": "Instant-read or leave-in: two different questions",
                "p": [
                    "This is the decision most buyers get wrong, and the official thermometer guidance sorts it by design rather than by price. A leave-in probe is built to stay in the food while it cooks and reports temperature while you are doing something else. A handheld instant-read is used at the end, at the plate, and \u2014 importantly \u2014 most of them should not be left in food during cooking unless the manufacturer says it can withstand the heat and was designed for it.",
                    "That single line is worth more than any feature list. If you are considering one of the two thermometers in this edit: P-04's listing describes a digital meat thermometer and P-05's describes a wireless model with three probes and states among its uses air frying. Whether either is rated to remain in a running appliance at the temperature you plan to use is a manufacturer-instruction question, not a listing-title question, and this site does not answer it.",
                ],
                "table": {
                    "caption": "Thermometer types, as classified by USDA FSIS \u2014 Food Thermometers (retrieved 2026-11-20)",
                    "headers": ["Type", "Speed", "Placement", "Usage note in the source"],
                    "rows": [
                        ["Wireless / smart thermometer", "Left in the food while cooking", "At least 1 inch deep in the thickest part", "Provides live status on internal temperature"],
                        ["Thermometer fork combination", "2\u201310 seconds", "At least a quarter of an inch in the thickest part", "Not designed to remain in food while cooking"],
                        ["Thermocouple", "2\u20135 seconds", "A quarter of an inch or deeper as needed", "Fastest reading; works in thick and thin food"],
                        ["Thermistor", "10 seconds", "At least a half inch deep", "Measures thin and thick food; not designed to remain in food"],
                        ["Oven cord thermometer", "10 seconds", "At least a half inch deep", "Designed to remain in food in an oven or covered pot; base unit sits on the counter"],
                        ["Oven-safe bimetal (dial)", "1\u20132 minutes", "2 to 2.5 inches deep in the thickest part", "For roasts, casseroles and soups; not appropriate for thin food"],
                    ],
                },
            },
            {
                "h": "Accuracy is a range, not a number",
                "p": [
                    "Most food thermometers will read accurately within 2 to 4°F, according to the same guidance \u2014 which is why \u201cit said 164\u201d is not a reason to keep cooking a patty, and why \u201cit said 172\u201d is not a reason to panic. If you want to know whether yours is telling the truth, the two published checks are ice water, which should read 32°F with the stem at least 2 inches deep and not touching the glass, and boiling water, which should read 212°F at sea level after at least 30 seconds. Altitude changes the second number.",
                    "One more line from the same source, aimed squarely at connected-kitchen marketing: some models have plastic faces that can melt if placed too close to heat. Read the manufacturer's instructions before you leave anything in a closed, running appliance.",
                ],
            },
        ],
        "closing": "Every figure and classification in this guide comes from the USDA FSIS pages linked in the table, read on 2026-11-20. The two sentences about products describe what their listings state, and nothing about how they perform.",
    },
    {
        "slug": "leftovers-and-the-two-hour-rule",
        "cluster": "Food safety",
        "kicker": "Food safety",
        "title": "The two-hour rule, and what it really says",
        "dek": "Everyone has heard it. Almost nobody can recite it accurately, and the difference between the version in your head and the version on the page is the difference between a good plan and a guess.",
        "read_minutes": 5,
        "photo": "assets/img/cleanup",
        "photo_alt": "Cooked food in containers on a kitchen counter beside a washing-up area",
        "photo_caption": "An editorial illustration for leftover handling. It is not a photograph of any model sold on this site.",
        "updated": "2026-11-20",
        "related": ["P-04", "P-03"],
        "sections": [
            {
                "h": "The rule, as published",
                "p": [
                    "Bacteria grow rapidly between 40°F and 140°F. Once food has been cooked, hot food must be kept at 140°F or warmer to prevent bacterial growth, and within 2 hours of cooking \u2014 or of coming out of whatever was keeping it warm \u2014 leftovers must be refrigerated. Perishable food left out more than 2 hours at room temperature should be thrown away. If the room or the day is above 90°F, that window is 1 hour.",
                    "Two things are worth noticing. The clock starts when the food stops being held hot, not when you sat down to eat. And the same source lists the two main causes of foodborne illness as not cooking to a safe temperature and leaving food out at an unsafe temperature, which is a good reminder that the appliance you are shopping for is downstream of the habit.",
                ],
            },
            {
                "h": "Cooling is faster than most people plan for",
                "items": [
                    ("Divide it", "Shallow containers, not the pot. A big pot of soup cools slowly, which is precisely the condition the guidance is warning about."),
                    ("Cut the large items", "Slice a whole roast or a turkey breast; legs and wings can stay whole. Smaller pieces reach 40°F sooner."),
                    ("Hot food may go in the fridge", "The published guidance allows hot food to be placed directly in the refrigerator, or chilled rapidly in an ice or cold-water bath first. You do not have to cool it to room temperature on the counter, which is the misremembered version of the rule."),
                    ("Wrap it for the fridge", "Cover, seal or wrap airtight to keep bacteria out, hold moisture in and stop it picking up other smells \u2014 then refrigerate or freeze immediately."),
                ],
            },
            {
                "h": "How long is \u201cstill fine\u201d",
                "p": [
                    "Leftovers keep 3 to 4 days in the refrigerator, or 3 to 4 months in the freezer \u2014 the freezer figure is a quality limit rather than a safety one, since frozen food held continuously stays safe but loses moisture and flavour over time. The cooked-turkey storage figures in the same guidance set are 3 to 4 days refrigerated and 4 months frozen.",
                    "Reheat to 165°F with a thermometer, covered. If you have reheated something that was previously frozen and there is still too much of it, refreezing after it has reached 165°F is described as safe.",
                ],
                "table": {
                    "caption": "Leftover figures, transcribed from the linked pages on 2026-11-20",
                    "headers": ["Question", "Published answer", "Official source"],
                    "rows": [
                        ["Temperature range where bacteria grow rapidly", "Between 40°F and 140°F",
                         {"url": FSIS_LEFTOVERS, "label": "USDA FSIS \u2014 Leftovers and Food Safety"}],
                        ["Time out of refrigeration before discarding", "2 hours at room temperature, 1 hour above 90°F",
                         {"url": FSIS_LEFTOVERS, "label": "USDA FSIS \u2014 Leftovers and Food Safety"}],
                        ["Refrigerator life of leftovers", "3 to 4 days",
                         {"url": FSIS_LEFTOVERS, "label": "USDA FSIS \u2014 Leftovers and Food Safety"}],
                        ["Freezer life of leftovers", "3 to 4 months, for quality",
                         {"url": FSIS_LEFTOVERS, "label": "USDA FSIS \u2014 Leftovers and Food Safety"}],
                        ["Reheat target", "165°F, measured with a food thermometer",
                         {"url": FDA_TEMPERATURES, "label": "FoodSafety.gov \u2014 Cook to a Safe Minimum Internal Temperature"}],
                        ["Temperature for the reheat of poultry, casseroles and stuffing", "165°F for all poultry and casseroles",
                         {"url": FSIS_TEMP_CHART, "label": "USDA FSIS \u2014 Safe Minimum Internal Temperature Chart"}],
                    ],
                },
            },
            {
                "h": "What this has to do with the appliance you are shopping for",
                "p": [
                    "Only this: the countertop fryer is a reheating tool for some households, and the households it suits are the ones that already portion, cool and label things. If you buy it because it makes reheating easier, the honest feature list is short \u2014 one layer of food, a basket you can wash without a fight, and enough floor for the portion you actually eat. P-03's listing describes a single 8-quart basket; P-01's describes two independent 3-quart baskets and dishwasher-safe nonstick baskets, in the seller's wording. Which of those is the right shape for your leftovers is your kitchen's answer, not the specification's.",
                ],
            },
        ],
        "closing": "The numbers here are quoted from USDA and FoodSafety.gov pages retrieved 2026-11-20; where a page carries its own last-updated date, this site records it in the source register. Product sentences restate listing wording and nothing else. This is not medical advice \u2014 for anything unusual, the federal pages linked above are the place to look.",
    },
]
