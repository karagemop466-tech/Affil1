"""Source-backed kitchen cluster. Listing observations are not product tests."""
FOOD_SAFETY = 'https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures'
FSIS_THERMOMETERS = 'https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers'


def guide(slug, title, dek, kicker, image, alt, sections, sources, related, closing):
    return dict(slug=slug, title=title, dek=dek, kicker=kicker, photo=f'assets/img/{image}',
                photo_alt=alt, photo_caption='A format illustration, not a photograph of a listed product.',
                updated='2026-11-20', read_minutes=3, sections=[dict(h=h, p=p) for h, p in sections],
                sources=sources, related=related, closing=closing)


BUYER_GUIDES = [
    guide('holiday-hosting', 'Is a countertop oven worth it for holiday sides?',
          'Work backward from serving time, the pans you already own, and what actually needs the main oven.',
          'Holiday kitchen', 'format-oven', 'An illustrated countertop oven with a tray of vegetables', [
              ('Write the menu as a schedule', ['List the dishes you need hot at the same time. Put the largest pan on the list first, then write down the dish that always ends up waiting for oven space. That second dish is what you’re shopping for.']),
              ('Use the pan, not the quart number', ['Measure your sheet pan rim to rim. If you’re comparing the listed Emeril Lagasse French-door model, the seller’s 26-quart figure describes cavity volume. It isn’t a promise that your pan fits. Check usable width and depth and the clearance in front of both doors.']),
              ('Plan how you’ll check doneness', ['FoodSafety.gov lists 165°F for poultry and leftovers. Use a food thermometer to check the food itself. Oven presets and the appliance display don’t tell you its internal temperature.']),
          ], [('Amazon listing: Emeril Lagasse French-door oven', 'https://www.amazon.com/dp/B09B7SB46R'), ('FoodSafety.gov: safe internal temperatures', FOOD_SAFETY)],
          ['products/p-02.html', 'guides/thermometer-pairing.html'], 'If your second dish already fits the oven you own, save the counter space.'),
    guide('meal-prep-sunday', 'One basket or two for Sunday meal prep?',
          'Sketch one batch of the lunch you actually pack before buying a bigger air fryer.',
          'Weeknight cooking', 'format-basket', 'Illustrated potato wedges in an unbranded air fryer basket', [
              ('Pick a batch you already cook', ['Write down one main and one side you usually pack. Lay them out in your usual pan or on a board and measure the area they take in one layer. Use that as a question to take to the appliance manual, not a capacity claim.']),
              ('Compare one big space with two small ones', ['The Chefman 6-quart dual-basket listing describes two separate 3-quart baskets. Its TurboFry listing describes a single 8-quart basket. Don’t treat both labels as usable floor area. If you cook the same food in every batch, compare the usable space of the single basket first. If two foods need independent settings, check the controls on the dual-basket model.']),
              ('Read the cleanup instructions for the exact model', ['The two Amazon titles describe dishwasher-safe baskets. Check the manual for the removable inserts and the parts you’ll wash between batches. A line about the basket doesn’t automatically cover every part.']),
          ], [('Amazon listing: Chefman dual-basket', 'https://www.amazon.com/dp/B0CDY277D3'), ('Amazon listing: Chefman TurboFry', 'https://www.amazon.com/dp/B08DKYBTPH')],
          ['products/p-01.html', 'products/p-03.html'], 'If the main won’t fit one side, two baskets may not solve the problem you have.'),
    guide('small-kitchen-counter', 'Will that air fryer fit a small kitchen?',
          'Measure the space the appliance uses in motion, not just where it sits.',
          'Small kitchens', 'decision-tools', 'Illustrated kitchen counter with a measuring tape', [
              ('Tape out the footprint', ['Put removable tape on the counter where the appliance would go. Measure the available width, depth and height. When you have an exact model in mind, compare with its manual for heat and ventilation clearances.']),
              ('Try the opening motion', ['The Emeril Lagasse listing calls out French doors; the Chefman TurboFry listing describes a basket. Mark where each would open. If either crosses a narrow walking route or crowds a kettle, check another spot.']),
              ('Find a landing spot for hot parts', ['Pick a heat-safe surface nearby for the basket or tray. Check how you’d carry it there without reaching across the sink or a cooktop.']),
          ], [('Amazon listing: Emeril Lagasse French-door oven', 'https://www.amazon.com/dp/B09B7SB46R'), ('Amazon listing: Chefman TurboFry', 'https://www.amazon.com/dp/B08DKYBTPH')],
          ['fit/index.html', 'guides/cleanup-and-counter-space.html'], 'If you have to move the appliance each time you open it, consider a different spot or a different shape.'),
    guide('thermometer-pairing', 'Instant-read or wireless: which thermometer do you need?',
          'Pick for the way you cook: a quick spot check at the end or monitoring during a longer cook.',
          'Cooking tools', 'thermometer', 'Illustrated probe thermometer beside roasted chicken', [
              ('Decide when you need a reading', ['For occasional spot checks, compare the ThermoMaven digital listing as an instant-read example. If you want to monitor during a long cook, compare the CHEF iQ Sense listing as a wireless example. These are two different tasks, so start with the one you do most.']),
              ('Look up limits before you leave a probe in', ['Check the exact manufacturer’s instructions for temperature limits, approved appliances, insertion depth, and how the probe should be secured. For a wireless model also check the app, phone, and connection requirements. Don’t assume a handheld thermometer can stay in a closed, running appliance.']),
              ('Use the food safety target, not the preset', ['FoodSafety.gov gives different temperature targets for different foods, and some cuts need a rest time. Look up what you’re cooking in the official chart. A longer feature list isn’t a substitute for using the thermometer as directed.', 'The USDA’s own thermometer factsheet adds two numbers worth knowing before you buy: readings are expected to be accurate within 2 to 4 degrees F, and the probe has to sit in the thickest part of the food, away from bone, fat and gristle. It also tells you to read the manufacturer’s instructions for insertion depth, which is the part a listing rarely states.']),
          ], [('Amazon listing: ThermoMaven digital', 'https://www.amazon.com/dp/B0DHZTCNR5'), ('Amazon listing: CHEF iQ Sense', 'https://www.amazon.com/dp/B0DZFD6R9Z'), ('FoodSafety.gov: safe internal temperatures', FOOD_SAFETY), ('USDA FSIS: food thermometers', FSIS_THERMOMETERS)],
          ['products/p-04.html', 'products/p-05.html'], 'Start with a spot-check model if that’s the only job you need it to do.'),
]
