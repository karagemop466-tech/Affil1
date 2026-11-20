"""Reader-facing prose. Kept separate from layout so the words can be edited
without touching the templates.

Editorial rule for every guide here: the only product facts that may appear are
the ones transcribed in src/data/products.json from a listing title the site
actually reached. No price, no rating, no review count, no test result, no
superlative, no winner. If a sentence needs a fact that is not in that file, the
sentence does not ship.

Voice rule: write to the person deciding, in the second person, and keep the
machinery of verification out of the reading path. A guide is a guide. The
provenance lives one click away, on the page for the product it describes.
"""

GUIDES = [
    {
        "slug": "basket-or-oven-air-fryer",
        "cluster": "Choosing",
        "kicker": "Choosing a shape",
        "title": "Basket or oven-style air fryer: what should you compare?",
        "dek": "Two appliances share a name and almost nothing else. These are the differences that change how a weeknight goes, and the ones that only look like they do.",
        "read_minutes": 7,
        "photo": "assets/img/format-oven",
        "photo_alt": "An unbranded countertop oven with French doors open on a tray of roasted vegetables",
        "photo_caption": "Illustration of an oven-style cavity, not a photograph of a product on this site.",
        "updated": "2026-11-20",
        "related": ["P-01", "P-03", "P-02"],
        "sections": [
            {
                "h": "The difference is the shape of the space",
                "p": [
                    "A basket fryer is one deep container. Food goes in, the drawer closes, a fan moves hot air over it. An oven-style fryer is a shallow cavity with racks, and a door on the front or two doors that open outward.",
                    "Everything else follows from that. How much fits, how often you intervene, where it lives on the counter, what needs washing \u2014 all of it is downstream of the shape. The brand on the front is not.",
                ],
            },
            {
                "h": "What actually changes",
                "items": [
                    ("Batch shape", "A basket holds one pile. An oven holds layers. Cooking for four is either one round or two, and this is where you find out which."),
                    ("Intervention", "Baskets mean pulling a drawer and shaking. Racks mean turning pieces and sometimes swapping shelf positions. Neither is better; one of them will annoy you more."),
                    ("Front clearance", "A door that opens outward eats the space in front of the machine \u2014 usually the space you stand in."),
                    ("Vertical clearance", "A drawer needs room above to lift out. A drop-down door needs room below to swing. Check both before you fall in love with a photograph."),
                    ("What fits inside", "A shallow cavity takes a tray, a pan, a small mould, a plate. A deep drawer mostly takes loose food. If you want to bake or reheat plated food, this decides it."),
                    ("Washing", "Baskets are one or two pieces. Ovens arrive with a rack, a tray, sometimes an accessory basket, and each one is a separate thing to wash and store."),
                ],
            },
            {
                "h": "Three measurements, four minutes",
                "p": [
                    "Do this with a tape rather than a feeling. Width and depth of the counter space, including whatever the door or drawer needs while open. Height from the counter to the underside of the cabinet above. And the distance to the nearest socket, because a short cord quietly decides the layout for you.",
                    "If a number is not published on the official listing or in the manual, write \u201cunknown\u201d next to it and move on. A blank sends you back to check; a guess sends you to the returns desk.",
                ],
            },
            {
                "h": "The two shapes in this edit",
                "p": [
                    "P-01 is a 6-quart machine with two independent 3-quart drawers and a sync-finish setting, in the seller's wording. P-03 is a single 8-quart basket. P-02 is a 26-quart French-door oven with 24 presets and six accessories, again per the seller.",
                    "Read those three descriptions side by side and the trade is visible: two small deep containers, one large deep container, or one big shallow cavity. That is the whole decision. Whether any of them cooks well is a different question, and this site does not answer it.",
                ],
            },
            {
                "h": "A short way to decide",
                "p": [
                    "Write down the meal you cook most often and how many people eat it. Then answer one question: does that meal fit in one deep container, or does it need to lie flat on a shelf?",
                    "If it fits in a container, a basket will feel simpler: fewer parts, fewer decisions, less door space. If it needs to lie flat, or you want to put a pan in it, an oven shape is doing something a basket cannot.",
                    "Then check your two measurements against the two machines you are considering, and stop. The rest of the specification sheet will not change the answer.",
                ],
            },
        ],
        "closing": "No product on this site was tested, ranked or scored. Descriptions of P-01, P-02 and P-03 are the sellers' own wording, transcribed from the listings reached on 2026-11-20.",
    },
    {
        "slug": "dual-zone-two-baskets",
        "cluster": "Choosing",
        "kicker": "Dual zone",
        "title": "Two baskets or one: is dual-zone worth the counter space?",
        "dek": "A second drawer is the most seductive feature in the category. It is also the one most often bought for a dinner you cook twice a month.",
        "read_minutes": 5,
        "photo": "assets/img/format-basket",
        "photo_alt": "Golden potato wedges being lifted from the basket of an unbranded air fryer",
        "photo_caption": "Illustration. Not a photograph of any product sold here.",
        "updated": "2026-11-20",
        "related": ["P-01", "P-03"],
        "sections": [
            {
                "h": "What the second basket actually buys you",
                "p": [
                    "Two independent drawers let you run two temperatures and two timers at once. That is a real advantage in exactly one situation: two foods, different cooking times, needed on the same plate.",
                    "The rest of the time it is two containers where one would do. Both get dirty, both get washed, and the machine is wider than the single-basket version of the same thing.",
                ],
            },
            {
                "h": "The split-capacity trap",
                "p": [
                    "A dual-basket machine quoted at 6 quarts might be two 3-quart drawers. A single-basket machine quoted at 8 quarts is one 8-quart basket. Comparing the headline numbers says the first is smaller; comparing what you can actually put in one place says it is a lot smaller.",
                    "So compare like with like. Drawer against drawer, or total against total, but never one against the other.",
                ],
            },
            {
                "h": "Questions that settle it quickly",
                "items": [
                    ("Do you cook two different foods at the same time more than once a week?", "If yes, dual-zone earns its footprint. If it is a weekend thing, a single basket and a tray in the oven does the same job."),
                    ("Would the second drawer replace something else on the counter?", "Two drawers can replace a second appliance. That is a genuine win in a small kitchen."),
                    ("Do you have the width?", "Dual-basket bodies are wider. Measure the gap, then add the clearance the drawers need to pull out."),
                    ("Would you rather have 8 quarts in one place or 6 in two?", "One big basket for a family portion; two small ones for a two-part dinner."),
                ],
            },
            {
                "h": "Where sync finish fits",
                "p": [
                    "P-01's listing describes a sync-finish function, which is the seller's term for coordinating the two drawers so they finish together. If you are buying two baskets, this is the feature that makes them a system rather than two machines in one box.",
                    "It is worth checking that the drawers genuinely run independently, because a machine with two compartments and one shared control is a different, cheaper design.",
                ],
            },
            {
                "h": "The honest summary",
                "p": [
                    "Buy the second drawer if your dinners genuinely come in two parts. Buy the single basket if they do not, and spend the saved counter space on something you will use every day.",
                ],
            },
        ],
        "closing": "P-01's dual-basket and sync-finish descriptions are the seller's wording from the listing reached on 2026-11-20. Nothing here was tested.",
    },
    {
        "slug": "air-fryer-capacity-checklist",
        "cluster": "Sizing",
        "kicker": "Sizing",
        "title": "A no-hype checklist for comparing air-fryer capacity",
        "dek": "The quart figure on the box answers a question you did not ask. This is the version you did ask.",
        "read_minutes": 6,
        "photo": "assets/img/capacity",
        "photo_alt": "Food laid out in a single layer on a counter next to a tape measure",
        "photo_caption": "Illustration. The food and the tape are props, not a measurement of any product.",
        "updated": "2026-11-20",
        "related": ["P-03", "P-01", "P-02"],
        "sections": [
            {
                "h": "A quart is a volume. You cook on a surface.",
                "p": [
                    "Capacity is quoted as a volume because a volume is one number and numbers fit on boxes. But hot air has to reach the food, and food that is piled up does not get air on the parts that are touching.",
                    "So the useful question is not how many quarts, but how much food can sit in a layer that still lets air around it. Those two questions have different answers, and the second one is not printed anywhere.",
                ],
            },
            {
                "h": "Do this instead, in order",
                "items": [
                    ("Pick the actual meal", "Not food in general. The specific thing you cook on a Tuesday: six chicken thighs, a bag of frozen chips, two salmon fillets."),
                    ("Count the pieces", "Write the number down. It converts a vague intention into something you can compare against a drawing."),
                    ("Look for the usable area", "Some manuals show basket or rack dimensions, or a diagram with food laid out. That drawing is worth more than the quart figure."),
                    ("Check whether it needs a single layer", "Most air-frying guidance assumes space around each piece. If your meal needs a single layer, the layer is your real capacity."),
                    ("Multiply by batches", "If it does not fit in one layer, the honest capacity is two batches. Decide now whether you mind waiting."),
                    ("Take the external measurements", "Width, depth and height, so you know it fits the gap. If they are not published, look at a different listing rather than guessing."),
                ],
            },
            {
                "h": "The trap in the number",
                "p": [
                    "A larger quoted capacity usually means a physically larger machine, which needs more counter and, in the oven shape, more door clearance. There is no configuration where more cooking space comes for the same footprint.",
                    "The opposite trap is buying small to save counter, then discovering that the meal you cook most often needs two batches. Two batches is not a disaster, but it is a daily tax. Better to notice it before you pay it.",
                ],
            },
            {
                "h": "What the listings in this edit state",
                "p": [
                    "P-03 states 8 quarts in a single basket. P-01 states 6 quarts across two 3-quart baskets. P-02 states a 26-quart French-door cavity. Those are sellers' figures, repeated as figures, and none of them was measured.",
                    "The comparison worth making is P-01's 3-quart drawer against P-03's 8-quart basket, not 6 against 8. One number describes a container you can fill; the other describes two you cannot fill at once.",
                ],
            },
            {
                "h": "The one-sentence version",
                "p": [
                    "Buy the smallest machine that fits your most common meal in one layer, and check the external dimensions before you buy it, not after.",
                ],
            },
        ],
        "closing": "Stated capacities are the sellers' own figures from the listings reached on 2026-11-20. No capacity was measured and no product was tested.",
    },
    {
        "slug": "cleanup-and-counter-space",
        "cluster": "Living with it",
        "kicker": "Living with it",
        "title": "How to assess cleanup and counter-space trade-offs",
        "dek": "The parts you wash and the space it occupies decide whether you keep using it. Both are checkable in about five minutes.",
        "read_minutes": 6,
        "photo": "assets/img/cleanup",
        "photo_alt": "A basket and crisper plate drying beside a sink on a kitchen counter",
        "photo_caption": "Illustration. Not a photograph of any product sold here.",
        "updated": "2026-11-20",
        "related": ["P-01", "P-02"],
        "sections": [
            {
                "h": "Count the parts before the features",
                "p": [
                    "An air fryer's real cost is paid every time you use it, in washing and putting away. That cost is set by how many separate pieces come out and how big they are.",
                    "A single basket is usually a basket and a crisper plate. A dual-basket machine doubles that. An oven typically adds a rack, a tray and sometimes a basket accessory. None of that is bad \u2014 but you wash it, you store it, and one piece is always slightly too big for the sink.",
                ],
            },
            {
                "h": "Four questions that predict whether you keep using it",
                "items": [
                    ("Does the largest part fit in your sink?", "Measure the removable part, not the machine. A tray that has to be washed at an angle gets washed badly."),
                    ("Where does it live when it is cold?", "On the counter means it must earn permanent space. In a cupboard means checking the weight and whether the shelf is above shoulder height."),
                    ("What moves out to let it in?", "The honest test is not whether it fits, but what leaves the counter. If you cannot name the thing, you have not made room, you have added."),
                    ("How long is the cord, and where is the socket?", "A cord that does not reach means an extension lead across a work surface, which the manufacturer's own instructions may warn against."),
                ],
            },
            {
                "h": "Dishwasher-safe is a claim, not a fact you own",
                "p": [
                    "Listings often say a basket is dishwasher-safe. Whether that applies to your machine, your detergent and your cycle is a question for the manufacturer's instructions for that exact model. A coating ruined by a hot cycle is an expensive way to learn this.",
                    "Where a care instruction could not be confirmed from an official manual, this site says nothing rather than something plausible.",
                ],
            },
            {
                "h": "The five-minute layout test",
                "p": [
                    "Before ordering, cut a rectangle of paper to the published width and depth, put it where the machine would go, and use the kitchen around it for a day. Open the cupboard the paper blocks. Stand where you normally stand.",
                    "It sounds excessive. It is also the cheapest way to find out that the thing you were about to buy makes the most-used part of the counter unusable \u2014 and it costs one sheet of paper.",
                ],
            },
            {
                "h": "The trade in one line",
                "p": [
                    "More capacity means more surface to wash and more counter to give up. The right answer is the smallest machine whose parts you will still be willing to wash in February.",
                ],
            },
        ],
        "closing": "Dishwasher-safe wording on P-01, P-02 and P-03 is the sellers' own claim. No care instruction was checked against a manufacturer's manual in this build.",
    },
    {
        "slug": "small-kitchen-space-audit",
        "cluster": "Living with it",
        "kicker": "Small kitchens",
        "title": "Small kitchen, big appliance: a five-minute space audit",
        "dek": "Before you compare capacities, find out what your kitchen will actually let you own. It is a shorter list than you think.",
        "read_minutes": 5,
        "photo": "assets/img/decision-tools",
        "photo_alt": "A tape measure and a notepad on a kitchen counter beside a kettle",
        "photo_caption": "Illustration. Not a photograph of any product sold here.",
        "updated": "2026-11-20",
        "related": ["P-03", "P-01", "P-04"],
        "sections": [
            {
                "h": "Measure the gap, not the appliance",
                "p": [
                    "Every counter has one gap wide enough for a small appliance and one socket within reach of it. Find both, write the numbers down, and shop inside those numbers. Most of the regret in this category comes from buying to the quart figure and hoping the counter agrees.",
                    "Include the open state: a drawer that pulls out, a door that drops down, a lid that lifts. The machine is at its largest when it is doing its job.",
                ],
            },
            {
                "h": "The audit, in five steps",
                "items": [
                    ("Photograph the counter as it is", "Not tidied. The photograph is the honest baseline."),
                    ("Name what leaves", "One thing has to go for something to arrive. If nothing can go, the answer may be a smaller appliance or none."),
                    ("Check the overhang", "Upper cabinets limit how tall the machine can be and how far a lid can lift."),
                    ("Check the socket", "Distance and whether the plug shares a circuit with a kettle and a toaster."),
                    ("Check the cupboard route", "If it will be stored, the path matters: weight, width, and whether you can lift it above shoulder height."),
                ],
            },
            {
                "h": "Small kitchen, which shape?",
                "p": [
                    "A single-basket fryer is the most compact way to air-fry and the easiest to put away. A dual-basket machine is wider but can replace a second appliance, which sometimes nets out smaller overall. A French-door oven is the largest of the three and asks for clear space in front of it.",
                    "In a genuinely small kitchen the ranking usually comes out single basket, then dual basket if it replaces something, then oven. That is a rule of thumb about footprint, not a judgement about quality.",
                ],
            },
            {
                "h": "The thermometer exception",
                "p": [
                    "A thermometer takes up a drawer and no counter at all, and it is the one item here that makes everything else more predictable. If your kitchen is too small for an appliance, it is not too small for a probe.",
                ],
            },
        ],
        "closing": "Footprint comparisons are general observations about appliance shape, not measurements of the products on this site. No dimensions were confirmed for any product here.",
    },
    {
        "slug": "multi-function-kitchen-appliance-questions",
        "cluster": "Before you buy",
        "kicker": "Before you buy",
        "title": "Questions to ask before buying a multi-function kitchen appliance",
        "dek": "Multi-function usually means one thing done well and several done acceptably. The trick is finding out which is which before it takes a shelf.",
        "read_minutes": 6,
        "photo": "assets/img/multifunction",
        "photo_alt": "An unbranded basket air fryer, countertop oven and probe thermometer on one counter",
        "photo_caption": "Illustration of three appliance shapes, none of them a product sold here.",
        "updated": "2026-11-20",
        "related": ["P-02", "P-05"],
        "sections": [
            {
                "h": "Start by naming the one job",
                "p": [
                    "Every multi-function appliance has a job it was designed around and a list of jobs it will also attempt. The list is what the marketing talks about; the job is what you will actually use it for.",
                    "Before comparing anything, finish this sentence: \u201cI want this to make ___ easier.\u201d If you cannot finish it without listing three equally weighted things, one good single-purpose appliance and one good pan will serve you better.",
                ],
            },
            {
                "h": "Nine questions, in the order that saves time",
                "items": [
                    ("What is the primary job, in the seller's own words?", "The first clause of a listing title is usually the job. Everything after the first pipe is the ambition."),
                    ("How many functions need a separate accessory?", "If three advertised functions need parts that live in a cupboard, you have bought a machine and a drawer."),
                    ("What does the manual say about each function?", "A preset is a button that sets a time and a temperature. It is not evidence that the result is good."),
                    ("How large is it, and where does it go?", "An appliance that does four things but lives in a cupboard does one thing: take up space."),
                    ("How many pieces come out to wash?", "Count them for the function you will use daily, not the one you will use at Christmas."),
                    ("Does it need clearance above or in front?", "Doors that open out and lids that lift both consume the space you stand in."),
                    ("What is excluded from the warranty, and for how long?", "Read the document, not the badge on the box. If it is not published, that is information too."),
                    ("What happens when one part breaks?", "Accessory availability is the difference between a five-year appliance and an eighteen-month one."),
                    ("Would two simpler things do it better?", "Sometimes yes. This is the question the listing will never ask you."),
                ],
            },
            {
                "h": "The preset trap",
                "p": [
                    "A count of presets is the easiest number to print on a box and the least informative. Twenty-four presets can be twenty-four combinations of the same two settings on the same heating element.",
                    "When a listing leads with a preset count, read the rest of the title for the things that constrain the experience: cavity size, rack count, whether the door opens flat, how many accessories are included. Those are the parts you cannot change later.",
                ],
            },
            {
                "h": "Where a thermometer fits, and where it does not",
                "p": [
                    "P-05 is not an air fryer. It is a wireless meat thermometer whose listing states three probes and a 1000\u00b0F heat rating, and which names air fryers among its intended uses. P-04 is the instant-read version of the same idea.",
                    "That is a useful illustration of the multi-function question rather than an exception to it. A probe does one job \u2014 it tells you the internal temperature of something \u2014 and it does that job in an oven, a pan, a smoker or an air fryer. A single-purpose tool that travels between appliances is often a better purchase than an appliance that claims to do the thermometer's job as one of nine features.",
                ],
            },
            {
                "h": "A decision rule that holds up",
                "p": [
                    "Buy for the job you do weekly. Borrow, or use a pan, for the job you do twice a year.",
                    "If a multi-function appliance is the only way to get the weekly job done in the space you have, it is the right purchase. If it is a way to avoid choosing, it will be in the cupboard by March.",
                ],
            },
        ],
        "closing": "No product on this site was tested, ranked or scored. P-04 and P-05 attributes are transcribed from their listing titles, reached on 2026-11-20.",
    },
    {
        "slug": "thermometer-pairing",
        "cluster": "Tools",
        "kicker": "Tools",
        "title": "Do you need a meat thermometer for an air fryer?",
        "dek": "An air fryer is very good at browning and completely blind to the middle. A probe is how you fix the second part.",
        "read_minutes": 6,
        "photo": "assets/img/thermometer",
        "photo_alt": "A thin probe thermometer inserted into a roasted chicken on a wooden board",
        "photo_caption": "Illustration. Not a photograph of any product sold here.",
        "updated": "2026-11-20",
        "related": ["P-04", "P-05"],
        "sections": [
            {
                "h": "The problem a probe solves",
                "p": [
                    "Air frying is fast and dry, and the window between cooked and overdone is short \u2014 especially for chicken pieces, pork and fish. Recipes give times, but times assume a size, a starting temperature and a machine. A probe replaces all three assumptions with one reading.",
                    "It also lets you stop opening the drawer. Every time you open it, heat leaves and the timer becomes a suggestion.",
                ],
            },
            {
                "h": "Two kinds of thermometer, two jobs",
                "items": [
                    ("Instant read", "You open the appliance, insert the probe, read the number, wipe it and put it away. P-04 states a one-second reading, \u00b10.5\u2109 accuracy, and an IP67 rating, in the seller's wording. Best for quick checks and thin pieces."),
                    ("Leave-in wireless", "The probe stays in the food while it cooks and reports to a base or a phone. P-05 states three probes, wireless operation, a 1000\u00b0F heat rating and names air fryers among its uses, per the seller. Best for roasts, whole birds and long cooks."),
                ],
            },
            {
                "h": "Which one for an air fryer?",
                "p": [
                    "If you mostly cook pieces \u2014 thighs, wings, fish, vegetables \u2014 an instant read is enough and lives in a drawer. If you cook whole birds or large roasts, a leave-in probe earns its keep because you cannot read the centre without opening the door.",
                    "Check the heat rating against how you cook. A probe rated well above your cooking temperature is one less thing to think about; one rated close to it is a thing to remember.",
                ],
            },
            {
                "h": "Where the numbers come from",
                "p": [
                    "Safe internal temperatures are published by food safety authorities, not by appliance sellers. USDA FSIS states that visual cues like color are unreliable and that using a food thermometer placed in the thickest part away from bone, fat or gristle is the only reliable way to verify safe internal temperature (SRC-09).",
                    "The figures below are transcribed directly from the USDA FSIS Safe Minimum Internal Temperature Chart (last updated April 14, 2025; SRC-08), with an official source link on every row:",
                ],
                "table": {
                    "caption": "USDA FSIS Safe Minimum Internal Temperatures (verified 2026-11-20, SRC-08)",
                    "headers": ["Food", "Safe minimum internal temperature & rest", "Official source"],
                    "rows": [
                        ["Beef, pork, veal and lamb steaks, chops and roasts", "145°F (62.8°C) and rest at least 3 minutes", {"url": "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart", "label": "USDA FSIS chart"}],
                        ["Ground meats (beef, pork, veal, lamb)", "160°F (71.1°C)", {"url": "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart", "label": "USDA FSIS chart"}],
                        ["All poultry (whole bird, breasts, thighs, wings, ground, stuffing)", "165°F (73.9°C)", {"url": "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart", "label": "USDA FSIS chart"}],
                        ["Eggs", "160°F (71.1°C)", {"url": "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart", "label": "USDA FSIS chart"}],
                        ["Fish and shellfish", "145°F (62.8°C)", {"url": "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart", "label": "USDA FSIS chart"}],
                        ["Leftovers and casseroles", "165°F (73.9°C)", {"url": "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart", "label": "USDA FSIS chart"}],
                        ["Ham, fresh or smoked (uncooked)", "145°F (62.8°C) and rest at least 3 minutes", {"url": "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart", "label": "USDA FSIS chart"}],
                    ],
                },
            },
            {
                "h": "The cheap upgrade",
                "p": [
                    "If you are choosing between a bigger air fryer and a thermometer, the thermometer is usually the better first purchase. Capacity changes how much you can cook; temperature changes whether it is any good.",
                ],
            },
        ],
        "closing": "P-04 and P-05 specifications are the sellers' claims from listings reached on 2026-11-20. No thermometer was tested and no accuracy was independently measured.",
    },
    {
        "slug": "holiday-hosting-air-fryer",
        "cluster": "Seasonal",
        "kicker": "Seasonal",
        "title": "Hosting with an air fryer: what actually scales",
        "dek": "The appliance that feeds two beautifully is not automatically the one that feeds eight. Here is where the arithmetic changes.",
        "read_minutes": 6,
        "photo": "assets/img/holiday-hosting-counter",
        "photo_alt": "A crowded holiday kitchen counter with serving dishes and an air fryer in the corner of the frame",
        "photo_caption": "Illustration. Not a photograph of any product sold here.",
        "updated": "2026-11-20",
        "related": ["P-02", "P-01", "P-05"],
        "sections": [
            {
                "h": "Capacity does not scale the way guests do",
                "p": [
                    "Doubling the number of people does not double the basket. It doubles the number of batches, and each batch is a separate ten to twenty minutes when the machine is unavailable for anything else.",
                    "That is fine if the air fryer is doing one component \u2014 the crisp thing, the roasted vegetables, the reheated leftovers. It is a problem if it is expected to be the oven.",
                ],
            },
            {
                "h": "The three jobs an air fryer does well at a gathering",
                "items": [
                    ("The crisp side dish", "Roast potatoes, sprouts, wedges, breaded things. Small volume, high impact, and better fresh than held."),
                    ("The reheat", "Leftovers and make-ahead items come back closer to fresh than a microwave manages."),
                    ("The overflow", "When the main oven is full, a countertop oven-style air fryer is a second cavity with its own temperature."),
                ],
            },
            {
                "h": "What it does badly at a gathering",
                "p": [
                    "Holding food warm. Air fryers are at their worst when asked to wait; the texture that makes them worth having goes soft under a lid. If timing matters, cook in waves and accept that the last wave is the good one.",
                    "Cooking a large single item. A whole bird needs a cavity, not a drawer \u2014 and even then, a 26-quart oven-style machine is not a substitute for a full-size oven on the day.",
                ],
            },
            {
                "h": "The setup that works",
                "p": [
                    "One oven-style machine for volume and a probe for the thing you cannot see into. P-02 states a 26-quart cavity and six accessories; P-05 states three leave-in probes. Together they cover the two failure modes of a hosted dinner: not enough space, and not knowing when the middle is done.",
                    "If you already own a full-size oven, the air fryer's job is the side dish and the overflow. Buy for that, not for the fantasy of replacing the oven.",
                ],
            },
            {
                "h": "A note on timing the table",
                "p": [
                    "Work backwards from the moment you sit down, and give the air fryer the last twenty minutes rather than the first two hours. Everything that can be made ahead should be, and everything that must be crisp should be last.",
                ],
            },
        ],
        "closing": "P-02 and P-05 descriptions are the sellers' wording from listings reached on 2026-11-20. Nothing here was tested.",
    },
]

# Rows for the comparison table. Every cell is either transcribed from a listing
# title reached on 2026-11-20 or explicitly blank. Blank is a valid value.
GUIDES.append({
    "slug": "holiday-side-dish-capacity",
    "cluster": "Seasonal",
    "related": ["P-02", "P-03", "P-05"],
    "title": "Will your air fryer fit the holiday sides without a queue?",
    "kicker": "Seasonal kitchen · holiday sides",
    "dek": "Plan backward from serving time: check the tray, count the batches, and give the meals you already cook more weight than the number on the box.",
    "updated": "2026-11-20",
    "read_minutes": 3,
    "photo": "assets/img/capacity",
    "photo_alt": "An editorial illustration for comparing air fryer capacity",
    "photo_caption": "Editorial illustration, not a photograph of any model on this site.",
    "sections": [
        {"h": "Start with the side that has to land last", "p": [
            "Imagine that you want crisp potatoes and roasted vegetables on the table at the same time. Pick the dish you want to cook last. Work backward from that tray, rather than assuming an appliance can take both at once. If you already make that dish in the oven, measure the area you actually use, not the size of the pan rim."
        ]},
        {"h": "Make a quick batch plan", "p": [
            "Sketch the usable rack or basket footprint from the manual for the exact model. Check the manual’s food load and spacing instructions. Split a mock shopping list into the number of loads that fit, allowing for any required preheat, unloading and reload time.",
            "Example worksheet, not a cooking recommendation: if a recipe you already use takes 18 minutes and your plan needs two sequential loads, that is 36 minutes of recipe time before any turnaround. That number is arithmetic, not a claim about a particular air fryer. If the timing doesn't work, move one side to the oven or choose a dish that doesn't need the fryer."
        ]},
        {"h": "Look for the thing that actually frees up the oven", "items": [
            ("Considering two baskets?", "Look at each basket’s dimensions and check whether each dish fits its own basket. Compare independent controls in the exact manual."),
            ("Considering a countertop oven?", "Measure the tray you mean to use, plus door travel and the clearances in the manual. Do not assume racks can be used together in every mode."),
            ("Cooking meat alongside the sides?", "Use a food thermometer and the official USDA guidance for placement and safe minimum internal temperatures. Don’t use colour or recipe timing alone."),
        ]},
    ],
    "sources": [("USDA Food Safety and Inspection Service · Food thermometers", "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers")],
    "closing": "Buy for the batches you cook on ordinary weeks. Solve the holiday bottleneck on paper before spending money on extra capacity.",
})


COMPARE_COLUMNS = [
    ("Product", "Brand and shape as stated on the listing"),
    ("Shape", "Basket, oven or thermometer, read from the title and category path"),
    ("Stated size", "Exactly as the seller words it. Not measured"),
    ("Stated features", "Only what the listing title itself claims"),
    ("Price", "Blank: Amazon serves it, this site does not hold it"),
    ("Rating", "Blank: Amazon serves it, this site does not hold it"),
]

# COMPARE_ROWS deliberately does not exist. The comparison table is built from
# src/data/products.json so that a fact can never exist in two places and drift.
