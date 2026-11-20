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

FSIS_THERMOMETERS = "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers"

RETRIEVED = "The government page below was opened on 2026-11-20 and read from that page."

GUIDES = [

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
                    "headers": ["Type", "Speed", "Placement", "Usage note in the source", "Official source"],
                    "rows": [
                        ["Wireless / smart thermometer", "Left in the food while cooking", "At least 1 inch deep in the thickest part", "Provides live status on internal temperature", {"url": FSIS_THERMOMETERS, "label": "USDA FSIS \u2014 Food Thermometers"}],
                        ["Thermometer fork combination", "2\u201310 seconds", "At least a quarter of an inch in the thickest part", "Not designed to remain in food while cooking", {"url": FSIS_THERMOMETERS, "label": "USDA FSIS \u2014 Food Thermometers"}],
                        ["Thermocouple", "2\u20135 seconds", "A quarter of an inch or deeper as needed", "Fastest reading; works in thick and thin food", {"url": FSIS_THERMOMETERS, "label": "USDA FSIS \u2014 Food Thermometers"}],
                        ["Thermistor", "10 seconds", "At least a half inch deep", "Measures thin and thick food; not designed to remain in food", {"url": FSIS_THERMOMETERS, "label": "USDA FSIS \u2014 Food Thermometers"}],
                        ["Oven cord thermometer", "10 seconds", "At least a half inch deep", "Designed to remain in food in an oven or covered pot; base unit sits on the counter", {"url": FSIS_THERMOMETERS, "label": "USDA FSIS \u2014 Food Thermometers"}],
                        ["Oven-safe bimetal (dial)", "1\u20132 minutes", "2 to 2.5 inches deep in the thickest part", "For roasts, casseroles and soups; not appropriate for thin food", {"url": FSIS_THERMOMETERS, "label": "USDA FSIS \u2014 Food Thermometers"}],
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
        "sources": [("USDA FSIS \u2014 Food Thermometers: placement, accuracy, calibration and the type table", FSIS_THERMOMETERS),
                    ("USDA FSIS \u2014 Safe Minimum Internal Temperature Chart", "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart")],
        "closing": "Every figure and classification in this guide comes from the USDA FSIS pages linked in the table and listed under Sources, read on 2026-11-20. The two sentences about products describe what their listings state, and nothing about how they perform.",
    },

]
