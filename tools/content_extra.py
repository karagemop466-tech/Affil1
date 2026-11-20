"""Additional guides added by the integration pass (session arena/359baa16-affil1).

Same editorial rule as content.py: a product capability is stated only when it
appears in the seller's own listing title, and it is always attributed to the
listing rather than presented as our finding. No price, rating, review count,
wattage, dimension or warranty figure appears anywhere, because none of those
could be confirmed from an official source with the access available.
"""

GUIDES = {
    "air-fryer-thanksgiving-overflow": {
        "title": "Thanksgiving overflow: what an air fryer actually fixes on the biggest oven day",
        "deck": "It will not roast the turkey. What it can do is take four sides, the rolls and the reheating off an oven that is already holding a bird for four hours. Here is the plan, and the questions to ask a listing before you believe it.",
        "cluster": "Cook with it",
        "og_image": "feature-holiday.jpg",
        "minutes": 7,
        "products": ["P-01", "P-02"],
        "head": """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"Thanksgiving overflow: what an air fryer actually fixes on the biggest oven day","datePublished":"2026-11-20","dateModified":"2026-11-20","author":{"@type":"Organization","name":"Crisp & Counter"},"publisher":{"@type":"Organization","name":"Crisp & Counter"},"description":"A planning method for using a countertop air fryer as oven relief on a large holiday dinner, with the questions to ask a listing before you buy.","mainEntity":{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Can an air fryer cook a Thanksgiving turkey?","acceptedAnswer":{"@type":"Answer","text":"A single-basket machine will not hold a turkey. Some oven-style countertop fryers advertise a cavity large enough to attempt one, which is a listing claim to verify against the manufacturer's own guidance, not a result we have tested. The more reliable holiday use is oven relief: sides, rolls, reheating."}},{"@type":"Question","name":"What does a dual-basket machine add on a holiday?","acceptedAnswer":{"@type":"Answer","text":"Two independently controlled baskets, when a listing says it has them, mean two side dishes finishing at their own temperature. One listing in our register states '2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets' and 'Sync Finish'. Read the exact wording before you plan around it."}},{"@type":"Question","name":"How many people can an air fryer serve on Thanksgiving?","acceptedAnswer":{"@type":"Answer","text":"Nobody can answer that from a quart number. Convert it to your own dishes: how many grams of Brussels sprouts fit in one layer on your sheet pan, and how many layers you need. Then ask whether that fits the basket floor or the rack area the listing describes."}}]}}
</script>""",
        "body": """
<p class="lead">The honest pitch for buying a countertop fryer in November is not health, and it is not speed. It is <strong>oven geometry</strong>. On the day the oven is committed to a bird for hours, every side dish competes for one rack and one temperature. That is the problem a second heat source solves.</p>

<p>Everything below is a planning method, not a recipe set. We have not cooked in any of these machines, and we will not pretend otherwise. What we can do is read a listing closely with you and show which sentences are load-bearing.</p>

<h2>Start with the oven you are freeing, not the basket you are buying</h2>

<p>Write your menu in two columns. Left column: anything that must finish at a single temperature with a long, slow dry heat — the bird, the potato gratin under cheese. Right column: anything that is <em>done</em> and only needs to be crisped, browned or reheated — roasted vegetables that went soft, rolls, leftover mash with a crust on top, frozen appetisers, bacon, Brussels sprouts from raw.</p>

<p>The right column is the addressable load. If it is fewer than three dishes, a countertop fryer is a nice-to-have and you should not buy one for one holiday. If it is five or more, the question changes from “should I” to “which shape”.</p>

<h2>Capacity in the real world: floors, not volumes</h2>

<p>Quart numbers describe an enclosed cavity. What matters is the surface you can lay food on in a single layer, because an air fryer is a convection oven and crowded food steams. Two listings in our register show how differently the same problem gets described:</p>

<div class="product-inline" data-products="P-01,P-02"></div>

<ul class="tick">
  <li><strong>6 quarts, split into two 3-quart baskets.</strong> Two temperatures at once, and each basket is the size of one side dish — not half of a big one. Good for two dishes finishing independently. Bad for a single dish that needs one large floor.</li>
  <li><strong>26 quarts, one cavity, French door, six accessories.</strong> That is oven territory: racks, multiple levels, a tray of something at once. Two people can work it simultaneously; a family cannot cook three sides in parallel unless they rotate.</li>
</ul>

<div class="callout">
  <span class="callout-label">Do the arithmetic on your own pans</span>
  <p>Take the sheet pan you already use and physically place it on the counter. Compare that footprint to the basket or rack the listing describes. If your pan is bigger than the cooking floor, the advertised quart count will not translate into one-batch sides for your household, no matter how it is marketed.</p>
</div>

<h2>Which claimed features actually reduce holiday stress</h2>

<p>Ignore preset counts. A listing that says “24 one-touch presets” is telling you about a menu, not about cooking performance; a preset is a saved time and temperature, and you can set both by hand in about four seconds. The holiday-relevant claims are narrower:</p>

<ul class="tick">
  <li><strong>Independent zones with a shared finish.</strong> One listing in our register uses the phrase “Sync Finish”. If two baskets can be started at different times and still end together, that is a real coordination feature when you are trying to land four dishes in one ten-minute window. Verify the exact wording and the manufacturer's explanation before you build a timing plan on it.</li>
  <li><strong>A top temperature above the usual 400&nbsp;°F.</strong> One listing states a “450°F Hi-Fry” option. Higher dry heat is what browns reheated food instead of drying it out. Treat it as a claim about a mode, not a result.</li>
  <li><strong>Windows.</strong> “Easy view windows” sounds cosmetic. On a day when the appliance is behind you and you are not going to open it eight times to check, being able to see colour develop is a genuine workflow difference.</li>
  <li><strong>Dishwasher-safe baskets.</strong> Everything else on the counter at 7pm is a plate, a carving board and a sink. If the parts that touch the food can go in the dishwasher, that is worth more than any preset.</li>
</ul>

<h2>The part nobody wants to hear: the failure modes</h2>

<p>A countertop fryer on Thanksgiving creates two new problems. First, <strong>holding</strong>. Food cooked at 12:40 and served at 4:00 is not the same food. Plan to cook the crispiest things last, and treat the fryer as the “finish at service” appliance rather than the “cook ahead” appliance. Second, <strong>the cord</strong>. You now have a second high-wattage appliance on the same kitchen circuit as the oven, the microwave and the fridge. Which outlet you plug it into, and whether that trips a breaker, is a house-specific question that no listing can answer for you.</p>

<h2>Questions to ask before you buy for this one holiday</h2>

<ol>
  <li>Which three dishes move off my oven, and how many batches does each need?</li>
  <li>Does the cooking floor accept my actual sheet pan, or does food get transferred (an extra dirty thing) to fit?</li>
  <li>Does the listing claim independent zones, a shared finish, or a higher top temperature — and can I find that explained by the manufacturer?</li>
  <li>Where does it live between now and next November? A machine that must be lifted out of a cupboard every year is a machine that stays in the cupboard.</li>
  <li>Would the same money spent on a decent sheet pan and an instant-read probe change the dinner more? For a lot of households the honest answer is yes.</li>
</ol>

<div class="callout">
  <span class="callout-label">What this guide does not claim</span>
  <p>No performance, ranking, taste or “best for Thanksgiving” verdict — we have not cooked in these machines. Every capability sentence above is the seller's own listing wording, quoted and attributed. Prices, star ratings and review counts are deliberately absent: Amazon's program terms permit that data only when it serves the link or arrives through its API, and this site has no live feed. Read <a href="/about/#method">how we check</a> for the full method.</p>
</div>
""",
    },

    "frozen-food-nights": {
        "title": "Frozen food nights: four questions that decide whether a basket earns its counter",
        "deck": "Most air-fryer purchases are justified on weeknights, not weekends. Before you buy one for the freezer aisle, four questions are worth answering with your own kitchen in front of you.",
        "cluster": "Live with it",
        "og_image": "topic-frozen.jpg",
        "minutes": 5,
        "products": ["P-03"],
        "head": """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"Frozen food nights: four questions that decide whether a basket earns its counter","datePublished":"2026-11-20","dateModified":"2026-11-20","author":{"@type":"Organization","name":"Crisp & Counter"},"publisher":{"@type":"Organization","name":"Crisp & Counter"},"description":"Four practical questions for deciding whether a countertop fryer suits a household that leans on frozen and convenience food.","mainEntity":{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Do air fryer listings publish cooking times for frozen food?","acceptedAnswer":{"@type":"Answer","text":"A listing may name a frozen mode or preset, which is a statement that a mode exists. It is not a time or temperature table. The package you are cooking from and the manufacturer's manual are the sources for that."}},{"@type":"Question","name":"Does basket size matter for frozen food?","acceptedAnswer":{"@type":"Answer","text":"More than for most fresh food, because frozen items cook best in a single layer with air moving between them. Count how many pieces your household eats per sitting and compare that with the cooking floor, not the quart figure."}}]}}
</script>""",
        "body": """
<p class="lead">The appliance you use twice a week matters more than the one that impresses guests once. For a lot of households the twice-a-week job is simple: something frozen, something that should end up hot in the middle and crisp outside, in about the time it takes to set the table.</p>

<h2>Question 1: how many pieces, in one layer?</h2>

<p>Frozen food is the clearest case of the single-layer rule. Nuggets, fries, wings, patties and fish fingers all release surface moisture; stacked, they steam each other and come out pale and leathery. So the useful number is not quarts, it is <em>how many things fit on the floor</em>. Count what your household actually eats in one sitting. If that exceeds what one layer holds, you are buying a machine you will run in batches — which is fine, as long as you knew before paying.</p>

<div class="product-inline" data-products="P-03"></div>

<p>That listing describes an 8-quart basket and, unusually, puts “Frozen” in its own title as a named use. Note what that is and is not: it is a claim that a mode exists. It is not a time-and-temperature table, and it is not a promise about how your chicken tenders will turn out.</p>

<h2>Question 2: does anything in the box get in the way?</h2>

<p>Some baskets have a crisper plate that reduces usable floor. Some oven-style units have racks that let you run two levels for items that do not need contact — a real advantage for reheating pizza or roasted vegetables, a disadvantage for anything that needs a hot surface. Look at the accessory list, not the marketing line, and ask which shape your food is.</p>

<h2>Question 3: can you clean it without a ritual?</h2>

<p>On a weeknight, cleaning is the whole decision. A basket that goes in the dishwasher is a materially different object from one that needs soaking; nonstick that chips in a year is a different object from bare metal you can scrub. Where a listing says “Nonstick Dishwasher-Safe Basket”, that is the seller describing the parts; anything beyond that — how long the coating survives your sponge — is a question for owner reviews on the retailer's own page, which we deliberately do not reproduce here.</p>

<h2>Question 4: where does it sit, permanently?</h2>

<p>A frozen-food appliance that lives in a cupboard is not a frozen-food appliance. Measure the piece of counter you are genuinely willing to surrender, including the arc of a door that opens downward and the few centimetres of rear clearance a fan needs. Then check the listing's stated footprint, or ask the manufacturer for it — we leave that field blank rather than guessing, and we say why on the <a href="/flagged/">flagged register</a>.</p>

<div class="callout">
  <span class="callout-label">A cheap way to test the hypothesis this week</span>
  <p>Before buying anything, run one frozen-food dinner in a conventional oven at a high temperature on a preheated sheet pan and time it honestly, including cleaning. If that was already fine, an air fryer is a convenience upgrade, not a solution — and you should buy it on those terms, with expectations that match.</p>
</div>

<h2>What we are not telling you</h2>

<p>Nothing here is a cooked result. We have not measured browning, texture, noise, energy use or timing in any machine. Capability wording is quoted from listings and attributed as such. Prices and ratings are absent by policy, not by oversight.</p>
""",
    },

    "dual-basket-math": {
        "title": "Dual basket or two separate machines? The counter math nobody writes down",
        "deck": "Two baskets in one box looks obviously better than one. The comparison that matters is against two small single-basket machines — on outlets, on cleanup, on cooking floor, and on what happens when one half breaks.",
        "cluster": "Size it right",
        "og_image": "topic-frozen.jpg",
        "minutes": 6,
        "products": ["P-01", "P-03"],
        "body": """
<p class="lead">A dual-basket machine is marketed as two appliances in one. Judge it against the obvious alternative: two of the cheapest decent single-basket machines, on the same counter, for the same money or less.</p>

<h2>Where one box genuinely wins</h2>

<ul class="tick">
  <li><strong>A single cleaning session.</strong> Two baskets and two plates in one sink, one wipe-down of one exterior.</li>
  <li><strong>One cord, one outlet, one storage problem.</strong> Small but real, and it compounds weekly.</li>
  <li><strong>Coordinated finishing.</strong> The listing below claims “Sync Finish” — two zones that end together. That is the whole reason the format exists: chips and chicken take different times, and you want them on the table at once.</li>
  <li><strong>A shared control language.</strong> One manual, one set of buttons, no second appliance to learn.</li>
</ul>

<div class="product-inline" data-products="P-01"></div>

<h2>Where two machines win</h2>

<ul class="tick">
  <li><strong>Independent capacity.</strong> Two 3-quart baskets is not one 6-quart basket. If tonight's job is a single large tray of something, a split cavity can be worse than one big one — and one big one is what the second device in our comparison below is.</li>
  <li><strong>Failure isolation.</strong> When one half of a dual unit faults, dinner is cancelled. When one of two cheap units faults, you still have a working appliance.</li>
  <li><strong>Two cooks, two places.</strong> One on the counter by the stove, one on an island or in a summer kitchen. A single box can only be one place.</li>
  <li><strong>Repair and replacement cost.</strong> Replacing one small machine is a different sum from replacing an integrated dual one.</li>
</ul>

<h2>The questions no comparison table answers</h2>

<ol>
  <li><strong>Do both zones reach the same temperature, and does one run hotter out of the box?</strong> Only the manufacturer's specification, or your own thermometer, can tell you. Listings usually describe the control scheme, not the tolerance.</li>
  <li><strong>Can one basket run empty?</strong> If you often cook for one, a machine that insists on running both halves is a waste of electricity.</li>
  <li><strong>Is the shared housing a cleaning problem?</strong> Two removable baskets are easy; the fixed central divider, the top surface and the shared fan area are the parts people complain about.</li>
  <li><strong>What is the combined height against your cabinets?</strong> Dual units are wide; oven-style units are tall. Measure the space, then the box.</li>
</ol>

<div class="callout">
  <span class="callout-label">The 30-second version</span>
  <p>Buy the dual basket if your recurring problem is “two different things must finish at the same time”. Buy one larger single basket if your recurring problem is “there is too much of one thing”. Buy two cheap machines only if you have the counter space, two outlets on different circuits, and no appetite for a coordinated appliance.</p>
</div>

<div class="product-inline" data-products="P-03"></div>

<h2>What this page is not</h2>

<p>It is not a verdict. We have not run either machine, measured recovery time between zones, or compared energy use. Where a sentence describes a capability, it is quoting a seller's own listing title and saying so. Prices are not shown because Amazon's program terms restrict price display to data Amazon serves with the link or data obtained through its API; we have neither, so we publish neither. Every field we could not confirm is blank and listed on the <a href="/flagged/">flagged register</a> with the source that would settle it.</p>
""",
    },

    "smart-probe-thermometer": {
        "title": "Instant-read or leave-in probe? Two thermometers, one question",
        "deck": "Two of the five links in our register are not air fryers at all — one is a wired multi-probe set, one is a one-second handheld. Same treatment as the fryers: what each listing claims, which question decides it, and what neither can tell you.",
        "cluster": "Buy smart",
        "og_image": "topic-probe.jpg",
        "minutes": 7,
        "products": ["P-05", "P-04"],
        "body": """
<p class="lead">The cheapest way to ruin a good piece of meat is to guess. A thermometer turns “is it ready?” into a number — and there are two quite different products that produce that number, which is why the useful question comes before any brand comparison: <strong>do you want to hold it, or watch it?</strong></p>

<h2>First, the fork in the road</h2>

<ul class="tick">
  <li><strong>An instant-read</strong> is a hand tool. Open the door, poke the thickest part, wait a second, close the door. It answers <em>right now</em>, and it is not built to live in the food while it cooks.</li>
  <li><strong>A leave-in probe</strong> is a sensor on a wire, or on a wireless base, that stays in the meat and reports continuously, so you can leave the kitchen and be told when to come back.</li>
</ul>

<p>Two of the links in our register are one of each. If you mostly cook steaks, chops and chicken pieces, the handheld is the tool and a connected probe is a gadget you will forget to charge. If you roast a turkey or smoke a shoulder for four hours, the reverse is true — and buying the wrong one of the two is the most common thermometer regret, because on a listing page both simply read as “a thermometer”.</p>

<h2>Why these two are in an air-fryer register at all</h2>

<p>Because the person shopping for a countertop fryer in November is usually shopping for the same event: a big dinner, an oven that is occupied, and a protein that must not be overcooked. The five links we were given resolve to three fryers and two thermometers. We record that rather than quietly dropping the awkward rows, because a shortlist that hides its mismatches is not a shortlist. One of the two thermometer destinations arrived through a fallback redirect and is flagged as such — see <a href="/flagged/#FLG-018">FLG-018</a>.</p>

<div class="product-inline" data-products="P-05,P-04"></div>

<h2>Question 1: how many probes, and what do you do with the extra?</h2>

<p>This listing states three probes. Two is the practical minimum for anyone who cooks a bird and something else — breast and thigh, or brisket and a smoker. A third earns its keep only if you actually cook two proteins at once, or want a backup that never has to be washed mid-cook. Ask what you will measure, not how many sockets the box advertises.</p>

<h2>Question 2: what does “heat safe to 1000&nbsp;°F” cover?</h2>

<p>That wording matters because it decides whether the probe can live inside the cooking environment: a searing pan, a grill, a smoker, an oven running hot. Ambient tolerance and probe-tip tolerance are frequently different numbers on the same product, and the difference is the difference between “leave it in” and “take it out before you sear”. The listing title is not the specification sheet; get the manufacturer's figures before you rely on either.</p>

<h2>Question 3: what does “WiFi unlimited range” actually promise?</h2>

<p>Two different architectures hide behind that phrase, and they behave completely differently in a real house:</p>

<ul class="tick">
  <li><strong>Probe → base → your home network → phone.</strong> Range is roughly “anywhere the internet reaches”, which is what “unlimited” is gesturing at. It depends on the base sitting inside WiFi coverage and on an app being online.</li>
  <li><strong>Probe → phone directly over Bluetooth.</strong> Range is a wall or two. Some products do both, and switch when you walk away.</li>
</ul>

<p>Which one you have decides whether you can leave the house. That is a question for the manufacturer's documentation — and it is precisely the sort of field we leave blank on our product cards rather than fill in from a guess.</p>

<h2>Question 4: what do “1 Sec” and “±0.5&nbsp;°F” actually promise?</h2>

<p>The handheld in our register states a one-second read, a half-degree tolerance, NIST and NSF certification, an auto-rotating screen and IP67 waterproofing. Those are four different claims wearing one title:</p>

<ul class="tick">
  <li><strong>Speed</strong> is a convenience claim about standing at the stove, and it matters most when you are testing six pieces at once.</li>
  <li><strong>Accuracy</strong> is the number worth caring about — and a stated tolerance is a specification, not something you can verify at home without an ice bath and a reference instrument.</li>
  <li><strong>Certification wording</strong> points at a traceability or product-safety scheme. What exactly it covers — the sensor, the calibration, the materials — is answerable only from the manufacturer's own documentation.</li>
  <li><strong>An IP67 rating</strong> is an enclosure rating: the body survives immersion. It does not mean the instrument belongs in a pot.</li>
</ul>

<p>And the sentence most buyers skip: an instant-read is meant to be <em>out</em> of the food before heat is applied again. Check the manual for insertion depth and for whether the model tolerates oven ambient heat at all — many do not, and a probe cooked inside an oven is both destroyed and, for the minute before it dies, possibly wrong.</p>

<h2>Question 5: does a phone you keep glancing at help or hurt?</h2>

<p>Be honest about the interaction. A device that pushes an alert lets you stop checking. A device that only shows a number inside an app you have to open can be worse than a dial you glance at while walking past the oven. If your kitchen is next to the oven, spend the money on better insulation gloves and a simple instant-read instead; nobody should be buying a connected gadget to solve a distance problem they do not have.</p>

<div class="callout">
  <span class="callout-label">Food-safety note, stated plainly</span>
  <p>Doneness temperatures are a food-safety question, not a preference question, and they change with the cut, the carryover and the guidance you follow. Use the current published guidance from your national food-safety authority as the reference, and treat any app's presets — including on a device we have not used — as a starting point rather than an authority.</p>
</div>
""",
    },

    "first-week-checklist": {
        "title": "Your first week with a new air fryer: a checklist that is not recipes",
        "deck": "Everything you should do in the first seven days so the appliance is still on the counter in month six — seasoning the run, learning the hot spots, and setting up the cleanup you will actually keep.",
        "cluster": "Live with it",
        "og_image": "topic-firstweek.jpg",
        "minutes": 5,
        "products": [],
        "body": """
<p class="lead">Most countertop fryers are abandoned in week eight, not because they cook badly but because nobody set them up. This is the setup week: five small tasks, none of them recipes.</p>

<h2>Day 1 — burn it off, then learn its language</h2>

<p>Run the empty appliance hot for the time the manufacturer's manual specifies, in a room you can ventilate, with nothing in the basket. New coatings and insulation off-gas; doing it once, deliberately, on day one is better than discovering it on the night you have people over. Then read the manual's own cleaning section <em>before</em> the first meal, because it is the only document that describes your specific basket.</p>

<h2>Day 2 — find the hot spots with one cheap test</h2>

<p>Cook a single layer of something small and uniform — the cheapest frozen thing in your freezer is ideal — and stop it two minutes early. Look at where browning happened first: front, back, left, right, edges. Every fan has a personality. Knowing yours is worth more than any preset, and it is the one measurement you can take in your own kitchen in ten minutes.</p>

<h2>Day 3 — set up the cleanup loop</h2>

<ul class="tick">
  <li>Torn-out paper towel and a brush live <em>next to</em> the machine, not in a drawer. Wipe the rim while the basket is warm.</li>
  <li>Decide now whether the basket goes in the dishwasher or the sink, and only in the dishwasher if the listing and the manual both say so.</li>
  <li>Dry the basket fully before it goes back. Trapped water is how nonstick edges flake.</li>
</ul>

<h2>Day 4 — give it a fixed home</h2>

<p>Choose the spot with three constraints: an outlet you are willing to keep reserved, rear clearance for the exhaust, and a door swing that does not hit a cabinet handle. If the machine has to be lifted out of a cupboard each time, plan for the fact that it will stop happening in about six weeks.</p>

<h2>Day 5 to 7 — three tests that answer “was this worth it”</h2>

<ol>
  <li>One weeknight dinner, in one layer, timed from freezer to plate including cleanup. Write the number down.</li>
  <li>One reheat that would normally go in the microwave. Note texture, honestly.</li>
  <li>One thing you assumed it would fail at — a single thin cut of meat, a delicate fish, something wet-battered. Knowing its failure modes is the difference between owning an appliance and being surprised by one.</li>
</ol>

<div class="callout">
  <span class="callout-label">Why there are no times or temperatures on this page</span>
  <p>Any number we printed would be a guess about your machine, your load and your freezer. The manual you own and the package you are cooking from are the two sources that actually apply. Our product pages do the narrow, checkable job instead: recording what each listing states and what we could not confirm from an official source — see <a href="/about/#method">the method</a>.</p>
</div>
""",
    },
}

# Extra rows for the comparison table, drawn only from listing-title wording.
COMPARE_ROWS = [
    {
        "label": "Holiday oven relief (multiple dishes finishing together)",
        "P-01": "Listing claims two independent baskets and a shared finish",
        "P-02": "One large cavity; one temperature at a time",
        "P-03": "Single basket; batch by floor area",
        "verdict_kind": "shape",
    },
    {
        "label": "Frozen weeknight food in a single layer",
        "P-01": "Two small floors, both usable at once",
        "P-02": "Racks if the accessories listed support them",
        "P-03": "One XL basket; a frozen mode is named in the title",
        "verdict_kind": "shape",
    },
    {
        "label": "Big-protein cooking away from the main oven",
        "P-01": "Not this format",
        "P-02": "Oven-style cavity with a front door",
        "P-03": "Basket depth limits what fits",
        "verdict_kind": "shape",
    },
    {
        "label": "Reading one piece of meat at the stove",
        "P-01": "", "P-02": "", "P-03": "",
        "P-04": "This is that tool: the listing states a one-second read",
        "P-05": "Wrong shape — a probe wired to a base is not a handheld",
        "verdict_kind": "shape",
    },
    {
        "label": "Following a four-hour roast from another room",
        "P-01": "", "P-02": "", "P-03": "",
        "P-04": "Not what it is for; it is not a leave-in sensor",
        "P-05": "Listing states three probes and a WiFi base for continuous monitoring",
        "verdict_kind": "shape",
    },
]

TOPICS = [
    {
        "name": "Choose the shape",
        "blurb": "Basket, dual basket, or oven-style: the decision that decides everything else.",
    },
    {
        "name": "Size it right",
        "blurb": "Quarts, floors, batches and the counter you are actually surrendering.",
    },
    {
        "name": "Live with it",
        "blurb": "Cleanup, cords, storage and the six-month survival test.",
    },
    {
        "name": "Cook with it",
        "blurb": "What a second heat source is good for on the days that matter.",
    },
    {
        "name": "Buy smart",
        "blurb": "Adjacent gear, and how to read a listing without being sold to.",
    },
]
