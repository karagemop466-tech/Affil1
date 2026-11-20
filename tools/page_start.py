"""Where to start: the shop answering a question instead of listing stock.

Five products and ten guides are enough material to be useful and too much to
read in order. A shopper arrives with a situation, not a model number: a small
counter, a family of four, a bird to roast, a first air fryer. This page takes the
five situations the catalogue actually answers and, for each one, says which shape
to look at, which guide settles it, and what to measure before paying.

The rule the rest of the site lives by applies here too: nothing on this page is a
test result, a ranking or a price. Where a page would need a number this site
cannot source, it says what to measure instead.
"""

from layout import (AMAZON_NOTE, breadcrumb_schema, breadcrumbs, buy_url, esc,
                    eyebrow, outbound, page, pagehead, product_link, rel, section)

# Each situation is answered by pages that already exist. `refs` name products in
# the register; `guides` name real slugs; the build fails if either is missing, so
# this page cannot drift into describing content that was never written.
SITUATIONS = [
    {
        "id": "first-air-fryer",
        "label": "Your first air fryer",
        "title": "You have never owned one and do not want a cupboard ornament.",
        "look_at": "One basket, and nothing else.",
        "why": (
            "A single drawer has one part to wash, one control to learn and no second "
            "zone to fill. The usual first-owner mistake is buying the most complicated "
            "shape and discovering the cleaning, not the cooking, decides whether it "
            "gets used again."
        ),
        "measure": (
            "The footprint of the spot it will live in, the height under the cabinet "
            "above it, and the width of the biggest batch you actually cook. Then compare "
            "that batch with the basket dimensions in the manual, not with the quart figure."
        ),
        "refs": ["P-03"],
        "guides": ["basket-or-oven-air-fryer", "cleanup-and-counter-space"],
        "settles_it": "The cleanup guide, because it is the part that decides the answer.",
    },
    {
        "id": "cooking-two-things",
        "label": "Dinner and a side, at once",
        "title": "One appliance, two things, and you would rather they landed together.",
        "look_at": "Two independent baskets.",
        "why": (
            "Two drawers only help if they run independently and can be told to finish "
            "at the same time. If both drawers share one setting, you have bought one "
            "basket with a divider and a bigger washing-up bill."
        ),
        "measure": (
            "Each basket separately. Six quarts as two three-quart drawers is not the same "
            "as six quarts in one drawer, and it is certainly not comparable with an "
            "eight-quart single basket."
        ),
        "refs": ["P-01"],
        "guides": ["dual-zone-two-baskets", "air-fryer-capacity-checklist"],
        "settles_it": "The dual-zone guide, which asks how often you really cook two things.",
    },
    {
        "id": "small-counter",
        "label": "A small counter",
        "title": "The kitchen is fine. The worktop is the problem.",
        "look_at": "Whatever leaves you somewhere to chop.",
        "why": (
            "Counter space is a zero-sum budget. A machine that needs its drawer pulled "
            "out or its doors swung open also owns the space in front of it, which is "
            "usually the space you stand in."
        ),
        "measure": (
            "Clear depth with the drawer open or the doors down, plus the socket distance, "
            "because a short cord quietly relocates the appliance for you."
        ),
        "refs": ["P-03", "P-01"],
        "guides": ["small-kitchen-space-audit", "cleanup-and-counter-space"],
        "settles_it": "The space audit, which is a tape measure and ten minutes.",
    },
    {
        "id": "oven-replacement",
        "label": "Replacing a toaster oven",
        "title": "You want one box that toasts, bakes, reheats and air-fries.",
        "look_at": "An oven-style cavity with a door.",
        "why": (
            "A shallow cavity takes a tray, a rack, a pan or a plate. A deep drawer mostly "
            "takes loose food. If you want to put a pan in it, the shape decides before the "
            "brand does."
        ),
        "measure": (
            "The tray you already own, the usable rack dimensions from the manual, and the "
            "swing of the doors. Then count the accessories, because each one is a separate "
            "thing to wash and store."
        ),
        "refs": ["P-02"],
        "guides": ["basket-or-oven-air-fryer", "multi-function-kitchen-appliance-questions"],
        "settles_it": "The multi-function questions, written for exactly this decision.",
    },
    {
        "id": "stop-guessing",
        "label": "Stop guessing whether it is done",
        "title": "The outside looks right and you do not trust the middle.",
        "look_at": "A thermometer, and it is the cheapest thing on this page.",
        "why": (
            "An air fryer can brown the outside while the centre is under. The USDA's own "
            "guidance is blunt that colour and firmness are not indicators that food is safe, "
            "and that a food thermometer is the reliable check \u2014 at any price point."
        ),
        "measure": "Nothing. This one is decided by whether you want a reading or a leave-in probe.",
        "refs": ["P-04", "P-05"],
        "guides": ["thermometer-pairing", "turkey-timing-by-weight"],
        "settles_it": "The pairing guide, which explains when a leave-in probe beats a quick read.",
    },
]


def _product(page_dir, ref, products):
    p = products[ref]
    href = rel(page_dir, f"products/{ref.lower()}.html")
    return f"""<li class="start-pick">
  <div>
    <p class="start-pick-ref">{esc(p['brand'])} &middot; {esc(p['format_label'])}</p>
    <h4><a href="{esc(href)}">{esc(p['name'])}</a></h4>
    <p class="start-pick-why">{esc(p['why'])}</p>
    <p class="start-pick-links">
      {product_link(page_dir, buy_url(p['observed_asin']),
                    'See it on Amazon <span aria-hidden="true">&#8599;</span>',
                    cls='btn btn-small',
                    aria=f"Open the Amazon listing for {p['brand']} {p['format_label']} (paid link, opens in a new tab)")}
      <a class="tlink" href="{esc(href)}">Read the note <span aria-hidden="true">&rarr;</span></a>
    </p>
    <p class="pcard-fine">Listing source &middot; {esc(AMAZON_NOTE)}</p>
  </div>
</li>"""


def build(page_dir, products_doc, guides):
    d = page_dir
    products = {p["ref"]: p for p in products_doc["products"]}
    by_slug = {g["slug"]: g for g in guides}

    missing = []
    for s in SITUATIONS:
        missing += [r for r in s["refs"] if r not in products]
        missing += [g for g in s["guides"] if g not in by_slug]
    if missing:
        raise SystemExit(f"start page references content that does not exist: {sorted(set(missing))}")

    cards = []
    for s in SITUATIONS:
        guide_links = "".join(
            f'<li><a href="{esc(rel(d, "guides/" + g + ".html"))}">{esc(by_slug[g]["title"])}</a>'
            f'<span class="start-guide-meta"> &middot; {esc(by_slug[g]["cluster"])} &middot; '
            f'{by_slug[g]["read_minutes"]} min</span></li>'
            for g in s["guides"]
        )
        cards.append(f"""<article class="start-card" id="{esc(s['id'])}">
  <p class="start-label">{esc(s['label'])}</p>
  <h3>{esc(s['title'])}</h3>
  <p class="start-look">{esc(s['look_at'])}</p>
  <p>{esc(s['why'])}</p>
  <dl class="start-meta">
    <div><dt>Measure this</dt><dd>{esc(s['measure'])}</dd></div>
    <div><dt>What settles it</dt><dd>{esc(s['settles_it'])}</dd></div>
  </dl>
  <p class="start-picks-label">From the edit</p>
  <ul class="start-picks">{''.join(_product(d, r, products) for r in s['refs'])}</ul>
  <p class="start-picks-label">Read before you decide</p>
  <ul class="start-guides">{guide_links}</ul>
</article>""")

    body = f"""{breadcrumbs(d, [])}
{pagehead(
        'Where to start',
        'Five situations,<br>five starting points',
        'The shop is five products and ten guides, which is too much to read in order. '
        'Find your situation, take the one shape it points at, do the one measurement, '
        'and read the guide that settles it.',
        meta='No rankings &middot; no test results &middot; no prices copied from anywhere',
    )}
{section(f'''
<div class="start-intro">
  <p>Nothing below is a recommendation to buy a particular model. Each situation names a
  <em>shape</em> and then says what to measure before you choose between the models that
  share it. Where this site cannot verify a number &mdash; dimensions, wattage, warranty,
  current price &mdash; the page tells you to read it from the manual or the listing instead
  of guessing on the page.</p>
  <p>If two situations describe you, the one that changes your weeknight is the one to start
  with. Counter space is the exception: it overrides everything, because a machine with nowhere
  to live does not get used.</p>
</div>
<div class="start-grid">
{''.join(cards)}
</div>''')}
{section(f'''
<div class="start-close">
  <h2>Still deciding?</h2>
  <p>Three other pages exist for the moment before a purchase: the
  <a href="{esc(rel(d, 'compare/index.html'))}">side-by-side table</a> if you want every stated
  figure on one screen, the <a href="{esc(rel(d, 'fit/index.html'))}">fit finder</a> if the
  question is really about your counter, and the
  <a href="{esc(rel(d, 'guides/index.html'))}">guide index</a> if you would rather read for
  ten minutes than compare bullets.</p>
  <p class="tiny">Sources for the food-safety point above:
  {outbound(d, 'https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers', 'USDA FSIS &middot; Food Thermometers')},
  read 2026-11-20.</p>
</div>''', cls='section-tint')}"""

    return page(
        d,
        title="Where to start \u2014 five situations, five starting points | Crisp & Counter",
        description=("Find your kitchen situation and take one shape from the edit: first air fryer, "
                     "two things at once, a small counter, a toaster-oven replacement, or a thermometer. "
                     "Each one names what to measure and which guide settles it."),
        body=body,
        active="start/index.html",
        canonical="start/",
        structured=[
            breadcrumb_schema([], "Where to start", "start/"),
            {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "name": "Five buying situations",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i + 1,
                        "name": s["label"],
                        "description": s["title"],
                        "url": f"https://karagemop466-tech.github.io/Affil1/start/#{s['id']}",
                    }
                    for i, s in enumerate(SITUATIONS)
                ],
            },
        ],
    )
