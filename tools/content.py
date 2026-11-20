"""Reader-facing prose. Kept separate from layout so the words can be edited
without touching the templates.

Editorial rule for every guide here: the only product facts that may appear are
the ones transcribed in src/data/products.json from a listing title the site
actually reached. No price, no rating, no review count, no test result, no
superlative, no winner. If a sentence needs a fact that is not in that file, the
sentence does not ship.
"""

GUIDES = [
    {
        "slug": "basket-or-oven-air-fryer",
        "kicker": "Choosing a shape",
        "title": "Basket or oven-style air fryer: what should you compare?",
        "dek": "Two appliances share a name and almost nothing else. Here is the list of differences that actually change how a weeknight goes \u2014 and the ones that only look like they do.",
        "read_minutes": 7,
        "photo": "assets/img/format-basket",
        "photo_alt": "Golden potato wedges being lifted out of the drawer of an unbranded basket-style air fryer",
        "photo_caption": "Illustration of a basket-style drawer, not a photograph of a product on this site.",
        "updated": "2026-11-20",
        "sections": [
            {
                "h": "The difference is the shape of the space, not the badge",
                "p": [
                    "A basket fryer gives you one deep container. Food goes in, the drawer closes, a fan moves hot air over it. An oven-style fryer gives you a shallow cavity with racks, and often a door on the front or two doors that open outward.",
                    "That is the whole of it. Everything a shopper cares about afterwards \u2014 how much fits, how often you have to intervene, where it lives on the counter, what needs washing \u2014 follows from those two shapes rather than from the brand or the badge on the front."
                ]
            },
            {
                "h": "What actually changes between them",
                "items": [
                    ("Batch shape", "A basket holds one pile. An oven holds layers. If you cook for four, the difference is whether one round of food is enough or whether you are running the machine twice."),
                    ("Intervention", "Basket cooking usually means pulling the drawer and shaking. Rack cooking usually means turning pieces and sometimes swapping shelf positions. Neither is better; one of them is more tolerable to you."),
                    ("Front clearance", "A door that opens outward needs space in front of the machine, and that space is usually the part of the counter you stand in."),
                    ("Vertical clearance", "A basket needs room above it to lift the drawer out. An oven needs room above the door swing if the door lifts rather than folds."),
                    ("What you can put in it", "A shallow oven cavity accepts a pan, a small mould or a plate. A deep basket mostly accepts loose food. If you intend to bake or reheat plated food, this is the deciding difference."),
                    ("Washing", "Baskets are usually one or two pieces. Ovens often ship with a rack, a tray, and sometimes a basket accessory, and each of those is a separate thing to wash and to store.")
                ]
            },
            {
                "h": "The three measurements to take before you choose",
                "p": [
                    "Do this with a tape, not with a feeling. It takes four minutes and it rules out most of the wrong answers.",
                    "Width and depth of the spot on the counter, including the space the door or drawer needs while open. Height from counter to the underside of the cabinet above, which is the measurement people forget and then regret. And the distance to the nearest socket, because a short cord quietly decides the layout for you.",
                    "If a number you need is not published on the official listing or in the manual, write 'unknown' next to it and move on. A blank is more useful than a guess, and it is a reminder to check before you buy."
                ]
            },
            {
                "h": "Where the seller's own wording is the only thing we have",
                "p": [
                    "Two products in this site's register illustrate the split honestly, using nothing but the words on their listings.",
                    "P-01 is described by its seller as a 6-quart dual-basket fryer with two independent 3-quart baskets and a sync-finish function. P-02 is described as a 26-quart French-door unit with 24 one-touch presets. Read those two descriptions side by side and you can see the shape of the trade: one is two small deep containers, the other is one large shallow cavity.",
                    "What this site cannot tell you is whether either is any good. Neither was tested, and no star rating or price appears here because the data has a permitted source and this build does not have access to it."
                ]
            },
            {
                "h": "A short way to decide",
                "p": [
                    "Write down the meal you cook most often and how many people eat it. Then answer one question: does that meal fit in one deep container, or does it need to lie flat on a shelf?",
                    "If it fits in a container, a basket fryer will probably feel simpler \u2014 fewer parts, fewer decisions, less door space needed. If it needs to lie flat, or if you want to put a pan in it, an oven shape is doing something a basket cannot do.",
                    "Then check the two numbers you measured against the two products you are considering, and stop. The rest of the specification sheet is not going to change the answer."
                ]
            }
        ],
        "closing": "No product on this site was tested, ranked or scored. The descriptions of P-01 and P-02 above are the sellers' own wording, transcribed from the listing titles reached on 2026-11-20."
    },
    {
        "slug": "air-fryer-capacity-checklist",
        "kicker": "Sizing",
        "title": "A no-hype checklist for comparing air-fryer capacity",
        "dek": "The quart figure on the box answers a question you did not ask. This is the version of the question you did ask.",
        "read_minutes": 6,
        "photo": "assets/img/capacity",
        "photo_alt": "Food laid out in a single layer on a counter next to a tape measure",
        "photo_caption": "Illustration. The food and the tape are props, not a measurement of any product.",
        "updated": "2026-11-20",
        "sections": [
            {
                "h": "A quart is a volume. You cook with a surface.",
                "p": [
                    "Capacity is quoted as a volume because a volume is one number and numbers fit on boxes. But hot air needs to reach the food, and food that is piled up does not get air on the parts that are touching.",
                    "So the useful question is not 'how many quarts' but 'how much food can sit in a layer that still lets air around it'. Those two questions have different answers, and the second one is not printed anywhere."
                ]
            },
            {
                "h": "What to do instead, in order",
                "items": [
                    ("1. Pick the actual meal", "Not 'food' in general. The specific thing you will cook on a Tuesday: six chicken thighs, a bag of frozen chips, two salmon fillets."),
                    ("2. Count the pieces", "Write the number down. This converts a vague intention into something you can compare against a drawing."),
                    ("3. Look for the usable area", "Some manuals show the basket or rack dimensions, or a diagram with food laid out. That drawing is worth more than the quart figure."),
                    ("4. Check whether it needs a single layer", "Most air-frying guidance assumes space around each piece. If your meal needs a single layer, the layer is your real capacity."),
                    ("5. Multiply by batches", "If your meal does not fit in one layer, the honest capacity is 'two batches', and you should decide now whether you mind waiting."),
                    ("6. Take the measurements off the listing", "External width, depth and height, so you know it fits the gap. If they are not published, that is a reason to look at a different listing, not a reason to guess.")
                ]
            },
            {
                "h": "The trap in the number",
                "p": [
                    "A larger quoted capacity usually means a physically larger machine, which needs more counter and, in the oven shape, more door clearance. There is no configuration where you get more cooking space for the same footprint.",
                    "The other trap is the opposite one: buying small to save counter space and then discovering that the meal you cook most often needs two batches. Two batches is not a disaster, but it is a daily tax, and it is worth noticing before you pay it rather than after."
                ]
            },
            {
                "h": "What the sellers in this register actually state",
                "p": [
                    "All five submitted links resolved to live listings in the session of 20 November 2026, and one of them needed a retry after three failures in an earlier session. Three are air fryers; the other two are probe thermometers, which have no capacity to compare and are handled in their own guide. The three air-fryer titles state 6 quarts across two 3-quart baskets (P-01), 8 quarts in a single basket (P-03), and 26 quarts in a French-door oven (P-02).",
                    "Those are the sellers' figures, repeated as figures. They have not been measured. A quart quoted for a two-basket machine is also counting two separate containers, which is exactly the kind of detail a single capacity number hides \u2014 so if you are comparing P-01 against P-03, compare the 3-quart basket against the 8-quart basket, not the 6 against the 8."
                ]
            },
            {
                "h": "When the number is genuinely enough",
                "p": [
                    "If you cook for one or two, mostly loose food, mostly from frozen, and you do not mind a second batch occasionally, then almost any capacity will work and this checklist is more caution than you need.",
                    "The checklist earns its keep when three things are true at once: you cook for more than two, the food needs to lie flat, and counter space is tight. That combination is where the quart figure misleads the most."
                ]
            }
        ],
        "closing": "Capacity figures quoted above are transcribed from listing titles reached on 2026-11-20. No product was measured or tested."
    },
    {
        "slug": "cleanup-and-counter-space",
        "kicker": "Everyday cost",
        "title": "How to assess cleanup and counter-space trade-offs",
        "dek": "The appliance that gets used is the one that is easy to put away and easy to wash. Both of those are checkable before you buy.",
        "read_minutes": 5,
        "photo": "assets/img/cleanup",
        "photo_alt": "An unbranded air-fryer basket and tray in a sink with a brush and a cloth",
        "photo_caption": "Illustration of the washing-up step, not a photograph of any product here.",
        "updated": "2026-11-20",
        "sections": [
            {
                "h": "Count the parts before you count the features",
                "p": [
                    "An air fryer's real cost is paid every time you use it, in washing and in putting it away. That cost is set by how many separate pieces come out and how big they are.",
                    "A single basket is usually a basket and a crisper plate. A dual-basket machine doubles that. An oven typically adds a rack, a tray, and sometimes a rotisserie or a basket accessory. None of those are bad \u2014 but you wash them, and you store them, and one of them is always slightly too big for the sink."
                ]
            },
            {
                "h": "The four questions that predict whether you will keep using it",
                "items": [
                    ("Does it fit in your sink?", "Take the internal width and depth of the appliance's largest removable part and compare it with your sink. A tray that does not lie flat gets washed at an angle and gets washed badly."),
                    ("Where does it live when it is not in use?", "If the answer is 'on the counter', it needs to earn that space permanently. If the answer is 'in a cupboard', check the weight and whether the cupboard is above shoulder height."),
                    ("What has to move to make room?", "The honest test is not whether it fits, but what leaves the counter to let it in. If you cannot name the thing that moves, you have not made room, you have just added."),
                    ("How long is the cord, and where is the socket?", "A cord that does not reach means an extension lead across a work surface, which is both a nuisance and something the manufacturer's own instructions may warn against.")
                ]
            },
            {
                "h": "Dishwasher-safe is a claim, not a fact you own",
                "p": [
                    "Listings often say a basket is dishwasher-safe. Whether that applies to your machine, your detergent and your cycle is a question for the manufacturer's own instructions for the exact model \u2014 and it is worth checking, because a non-stick coating that is ruined by a hot cycle is an expensive way to learn this.",
                    "Where this site cannot confirm a care instruction from an official manual, it says nothing rather than saying something plausible."
                ]
            },
            {
                "h": "A five-minute layout test",
                "p": [
                    "Before ordering, cut a rectangle of paper to the appliance's published width and depth, put it where the machine would go, and then try to use the kitchen around it for a day. Open the cupboard the paper is blocking. Stand where you normally stand.",
                    "It sounds excessive. It is also the cheapest way to discover that the thing you were about to buy makes the most-used part of your counter unusable, and it costs one sheet of paper."
                ]
            },
            {
                "h": "What the register can and cannot tell you here",
                "p": [
                    "Two of the three air-fryer listings state in their titles that the basket is dishwasher-safe, in the sellers' wording (P-01 and P-03). P-02's title instead lists six cooking accessories as included, which is a count, not a care instruction. Those are seller statements, and this site has not checked any of them against a manual.",
                    "No dimensions are published for any of these products on this site, because dimensions were not confirmed from an official specification sheet in this build. That is a gap, and it is on the review page rather than buried."
                ]
            }
        ],
        "closing": "No product on this site was tested. Seller-stated attributes are labelled as such wherever they appear."
    },
    {
        "slug": "multi-function-kitchen-appliance-questions",
        "kicker": "Before you buy",
        "title": "Questions to ask before buying a multi-function kitchen appliance",
        "dek": "Multi-function usually means one thing done well and several things done acceptably. The trick is finding out which is which before it takes up a shelf.",
        "read_minutes": 6,
        "photo": "assets/img/multifunction",
        "photo_alt": "An unbranded basket air fryer, countertop oven and probe thermometer on one counter",
        "photo_caption": "Illustration of three appliance shapes, none of them a product sold here.",
        "updated": "2026-11-20",
        "sections": [
            {
                "h": "Start by naming the one job",
                "p": [
                    "Every multi-function appliance has a job it was designed around and a list of jobs it will also attempt. The list is what the marketing talks about. The job is what you will actually use it for.",
                    "Before comparing anything, write one sentence: 'I want this to make ___ easier.' If you cannot finish that sentence without listing three equally weighted things, you are looking at a category where one good single-purpose appliance and one good pan will serve you better."
                ]
            },
            {
                "h": "Nine questions, in the order that saves time",
                "items": [
                    ("What is the primary job, in the seller's own words?", "The first clause of a listing title is usually the job. Everything after the first pipe or comma is the ambition."),
                    ("How many of the functions need a separate accessory?", "If three of the advertised functions need parts that live in a cupboard, you have bought a machine and a drawer."),
                    ("What does the manual say about each function?", "Presets are not the same as capability. A preset is a button that sets a time and a temperature; it does not tell you the result is good."),
                    ("How large is it, and where does it go?", "An appliance that does four things but lives in a cupboard does one thing: take up space."),
                    ("How many pieces come out to wash?", "Count them for the function you will use daily, not the one you will use at Christmas."),
                    ("Does it need clearance above or in front?", "Doors that open out and lids that lift both consume the space you stand in."),
                    ("What is excluded from the warranty, and for how long?", "Read the actual document, not the badge on the box. If the document is not published, that is information."),
                    ("What happens when one part breaks?", "Accessory availability is the difference between a five-year appliance and an eighteen-month one."),
                    ("Would two simpler things do the job better?", "The correct answer is sometimes yes, and a multi-function appliance is often the wrong purchase for someone who already owns a good oven.")
                ]
            },
            {
                "h": "The preset trap",
                "p": [
                    "A count of presets is the easiest number to put on a box and the least informative. Twenty-four presets can be twenty-four combinations of the same two settings on the same heating element.",
                    "When a listing leads with a preset count, read the rest of the title for the things that constrain the experience: the size of the cavity, the number of racks, whether the door opens flat, how many accessories are included. Those are the parts you cannot change later."
                ]
            },
            {
                "h": "Where the thermometer fits, and where it does not",
                "p": [
                    "One of the products submitted for this site (P-05) is not an air fryer. It is a wireless meat thermometer whose listing states three probes and a 1000\u00b0F heat rating, and which names air fryers among its intended uses.",
                    "That is a useful illustration of the multi-function question rather than an exception to it. A probe does one job \u2014 it tells you the internal temperature of something \u2014 and it does that job in an oven, a pan, a smoker or an air fryer. It is a single-purpose tool that travels between appliances, which is often a better purchase than an appliance that claims to do the thermometer's job as one of nine features.",
                    "This site has not tested it, and its accuracy is not stated here."
                ]
            },
            {
                "h": "A decision rule that holds up",
                "p": [
                    "Buy for the job you do weekly. Rent, borrow or use a pan for the job you do twice a year.",
                    "If a multi-function appliance is the only way to get the weekly job done in the space you have, it is the right purchase. If it is a way to avoid choosing, it will end up in the cupboard by March."
                ]
            }
        ],
        "closing": "No product on this site was tested, ranked or scored. P-05's attributes above are transcribed from its listing title."
    },
    {
        "slug": "thermometer-instant-or-wireless",
        "kicker": "Thermometers",
        "title": "Instant-read or wireless probe? What a kitchen thermometer has to do",
        "dek": "Two of the five products here are thermometers, and they are not competing answers to the same question. One is for the moment you open the oven; the other is for the twenty minutes before it.",
        "read_minutes": 6,
        "photo": "assets/img/thermometer",
        "photo_alt": "A thin probe thermometer inserted into a roasted chicken on a wooden board",
        "photo_caption": "Illustration. It is not a photograph of either thermometer on this site.",
        "updated": "2026-11-20",
        "sections": [
            {
                "h": "The question is not accuracy. It is where you are standing.",
                "p": [
                    "Both products here are sold on accuracy, and accuracy is the least useful thing to compare them on, because neither seller's accuracy claim can be checked from a listing. What differs, and what you can actually feel in a kitchen, is where the reading appears and how long you have to stand there to get it.",
                    "An instant-read probe is a hand tool. You open the oven or lift the lid, push the probe in, read a number, and take it out. A wireless probe set stays in the food while it cooks and sends the number somewhere else \u2014 a base unit, a phone \u2014 so you can be in another room when the target is reached."
                ]
            },
            {
                "h": "What each listing actually states",
                "p": [
                    "These are the sellers' own claims, transcribed from the listing titles on 2026-11-20. They are not measurements, and no product here was used."
                ],
                "items": [
                    ("P-04, ThermoMaven instant-read", "The title claims a one-second reading, an accuracy of plus or minus 0.5\u00b0F, NIST and NSF certification, IP67 waterproofing and an auto-rotating backlit screen."),
                    ("P-05, CHEF iQ Sense", "The title claims three ultra-thin probes, a wireless connection with unlimited range over WiFi, a 1000\u00b0F heat rating, five sensors, and lists BBQ, grill, oven, smoker and air fryer among its intended uses.")
                ]
            },
            {
                "h": "Where the two claims diverge, and why it matters",
                "items": [
                    ("Probes", "One probe against three. Three probes means three pieces of food monitored at once, which matters if you cook two joints and a bird, and is dead weight if you cook one steak."),
                    ("Heat rating", "The wireless set states 1000\u00b0F. That is a rating for the probe sitting inside a hot cavity, not a cooking instruction, and it is the number that decides whether a probe survives a pizza oven."),
                    ("Range", "\u201cUnlimited range\u201d is a claim about a network connection, not about physics. If your WiFi does not reach the garden, the range is your WiFi's range."),
                    ("Reading time", "One second stated for the instant-read. That is the difference between checking a pan on the hob without lifting it off and having to wait."),
                    ("Water", "IP67 is stated for P-04 only. That is a rating for the probe, and it is the sort of claim a manual should confirm before you put it anywhere near a dishwasher."),
                    ("Batteries and pairing", "A wireless set has two things to keep charged and one thing to pair. Neither listing title states battery life, and this site does not fill that gap.")
                ]
            },
            {
                "h": "What this guide will not tell you",
                "p": [
                    "It will not tell you a safe internal temperature. The United States Department of Agriculture publishes that guidance, and the page could not be reached from the environment this site was built in; a temperature figure copied from a blog would be worse than no figure, so none appears here.",
                    "It will not tell you which of the two is more accurate, because accuracy claims are made by sellers and this site has tested nothing. And it will not tell you which one to buy: that depends on whether you cook one thing at a time or several, and whether you want to walk away."
                ]
            },
            {
                "h": "A short way to decide",
                "p": [
                    "If you mostly need to know when a pan, a breast or a loaf is done while you are standing next to it, a fast hand-held probe is the simpler tool: one object, one reading, nothing to charge but the device itself.",
                    "If you roast, smoke or air-fry large pieces and want to know the moment the centre reaches temperature without opening the door, a probe that stays in the food is doing something the hand-held one cannot do. That is a different job, not a better one.",
                    "Write down which of those two sentences describes your week. The specification sheet will not change the answer."
                ]
            }
        ],
        "closing": "No product on this site was tested, ranked or scored. Every attribute above is quoted from a listing title reached on 2026-11-20. No temperature or food-safety figure appears because the official source could not be reached."
    }
]

# Rows for the comparison table. Every cell is either transcribed from a listing
# title reached on 2026-11-20 or explicitly blank. Blank is a valid value.
COMPARE_COLUMNS = [
    ("Product", "The register reference and the brand as stated on the listing"),
    ("Shape", "Basket, oven or other \u2014 read from the listing title and category path"),
    ("Stated capacity", "Exactly as the seller words it. Not measured"),
    ("Stated attributes", "Only what the listing title itself claims"),
    ("Listing", "The destination the submitted link actually reached"),
    ("Not stated here", "Values with no permitted source, left blank on purpose")
]

# COMPARE_ROWS deliberately does not exist. The comparison table is built from
# src/data/products.json so that a fact can never exist in two places and drift.
