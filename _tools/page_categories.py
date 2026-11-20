"""Category subpages: one index and one page per category in the register.

Why these exist. A buyer arrives with a shape in mind, not a product code. The
catalogue at products/ is organised by reference (P-01 to P-05), which is how the
verification register is keyed and how this project audits itself; it is not how a
person shops. The category pages are the reader-facing grouping: air fryers here,
thermometers there, and nothing in between.

Rules carried over from the rest of the build, deliberately:
  * every factual cell is transcribed from _src/data/products.json, which holds
    only what a listing this project reached actually said;
  * every register row carries a link to its official source, so the table can be
    checked without asking anyone to trust it;
  * where the register has no value, the cell says so in words. A blank with a
    reason is information; a blank that might be a zero is not.

Style note for anyone editing this file: the build runs on Python 3.11, where an
f-string may not contain a backslash escape or another triple-quoted f-string in a
replacement field. Blocks are therefore computed into names before the page body.
"""

from layout import (approved_amazon_urls, breadcrumb_schema, breadcrumbs, buy_url, esc,
                    eyebrow, note, page, pagehead, product_link, rel, section, table)
from page_home import guide_card, img
from content import GUIDES

MIDDLE = "\u00b7"
DASH = "\u2014"

CATEGORIES = [
    {
        "slug": "air-fryers",
        "name": "Air fryers",
        "kicker": "The countertop heat",
        "lead": "Three machines, three shapes, one question: does your dinner lie flat or sit in a drawer?",
        "dek": ("A basket is a deep container you fill and close. An oven is a shallow cavity with racks and a door. "
                "Capacity means nothing until you know which of those two things you are buying, which is why this "
                "page starts with shape and ends with the measurements you have to take yourself."),
        "filter": "air-fryers",
        # The shelf is the guides that answer a shopper's question about this shape,
        # in reading order: choose, size, live with, then the season. Slugs are listed
        # rather than filtered by cluster so the order is editorial and not alphabetical;
        # build_category skips any slug the site no longer publishes.
        "guides": ["basket-or-oven-air-fryer", "air-fryer-or-toaster-oven", "dual-zone-two-baskets",
                   "air-fryer-for-two", "air-fryer-capacity-checklist", "cooking-from-frozen",
                   "cleanup-and-counter-space", "reheating-thanksgiving-leftovers",
                   "holiday-hosting-air-fryer"],
        "honest": ("What this page cannot tell you: how any of these cooks, how loud it is, how long it lasts, or "
                   "what it costs. Those are not omissions we can fix by writing harder. A listing page does not "
                   "carry them in a form this site is allowed to republish, and nothing here has been measured."),
        "method": ("Each product block is transcribed from the listing this project reached, and links to it. "
                   "A product's identity is recorded as observed, not confirmed: the register keeps the ASIN the "
                   "operator intended and the ASIN the link actually opened in separate fields, because no account "
                   "owner has matched them. That gap is published on the review page rather than papered over."),
    },
    {
        "slug": "thermometers",
        "name": "Thermometers",
        "kicker": "The part that settles the argument",
        "lead": "An air fryer browns the outside. Only a probe tells you what the middle is doing.",
        "dek": ("Two thermometers, chosen because they answer two different questions: a handheld reading at the "
                "plate, and a leave-in reading while the food is still cooking. The federal guidance on placement "
                "and safe minimum temperatures is quoted with its source, because that is the part worth getting "
                "right."),
        "filter": "thermometers",
        "guides": ["thermometer-pairing", "where-to-put-the-probe",
                   "multi-function-kitchen-appliance-questions", "reheating-thanksgiving-leftovers"],
        "honest": ("What this page cannot tell you: whether either probe is rated to stay inside a running air "
                   "fryer at the temperature you plan to use. That is in the manufacturer's instructions for the "
                   "exact model, and no listing title here says it. Check before you leave a probe in anything."),
        "method": ("Temperature figures and thermometer classes come from the USDA FSIS pages linked in the guides "
                   "below, retrieved 2026-11-20. Product sentences restate listing wording and nothing else."),
    },
]


def _products():
    import json
    import pathlib
    root = pathlib.Path(__file__).resolve().parent.parent
    doc = json.loads((root / "_src/data/products.json").read_text(encoding="utf-8"))
    return doc["products"]


def _in(category):
    return [p for p in _products() if p.get("category") == category]


def _cat_name(slug):
    for c in CATEGORIES:
        if c["slug"] == slug:
            return c["name"]
    return slug


def _verified_cell(p):
    """Say what the record actually holds, in words, instead of implying a score."""
    checked = p.get("checked_on") or "not re-checked"
    confidence = p.get("identity_confidence") or "unrecorded"
    return f"Listing reached {checked} {MIDDLE} identity {confidence}"


def _stated(p):
    return p.get("stated_capacity") or f"Not published in the wording we recorded {DASH} check the manual"


def _features(p):
    """stated_attributes is a sentence in the register; title_stated is a list.

    Both shapes appear across the registers this build reads, and joining a string
    produces one character per cell -- which is how this function first shipped.
    The type test is the fix, and the checker catches the symptom rather than the
    cause, so it is written out here.
    """
    stated = p.get("stated_attributes") or p.get("title_stated") or []
    if isinstance(stated, str):
        return stated or "Nothing was transcribed from this listing"
    return "; ".join(stated) if stated else "Nothing was transcribed from this listing"


def _cta(p, d):
    return product_link(
        d, buy_url(p["observed_asin"]),
        'See it on Amazon <span aria-hidden="true">&#8599;</span>', cls="btn",
        aria=f"Open the Amazon listing for {p['brand']} {p['format_label']} (opens in a new tab)",
    )


def build_index(page_dir):
    d = page_dir
    cards = []
    for c in CATEGORIES:
        items = _in(c["filter"])
        count = f"{len(items)} {'pick' if len(items) == 1 else 'picks'} in this edit {MIDDLE} every one checked against its listing"
        href = rel(d, "categories/" + c["slug"] + "/index.html")
        cards.append(
            '<article class="cat-card">'
            f'<span class="cat-media">{img(d, items[0]["photo"], items[0]["photo_alt"], sizes="(max-width:820px) 100vw, 480px")}</span>'
            '<div class="cat-copy">'
            f'{eyebrow(c["kicker"])}'
            f'<h2><a href="{esc(href)}">{esc(c["name"])}</a></h2>'
            f'<p>{esc(c["lead"])}</p>'
            f'<p class="cat-count">{esc(count)}</p>'
            f'<a class="btn btn-small" href="{esc(href)}">Browse {esc(c["name"])} <span aria-hidden="true">&rarr;</span></a>'
            '</div></article>'
        )

    register_rows, register_sources = [], []
    # The evidence for a row is the listing it was read from, so the Listing column is
    # the source column. It is built by layout.product_link, which is the only place
    # an Amazon destination is emitted, so the sponsored marking cannot be forgotten.
    register_rows = []
    for p in _products():
        note_link = rel(d, "products/" + p["ref"].lower() + ".html")
        cat_link = rel(d, "categories/" + p["category"] + "/index.html")
        register_rows.append([
            {"html": f'<a href="{esc(note_link)}">{esc(p["name"])}</a>'
                      f'<span class="row-kicker">{esc(p["brand"])}</span>'},
            {"html": f'<a href="{esc(cat_link)}">{esc(_cat_name(p["category"]))}</a>'},
            _stated(p),
            p.get("format_label") or DASH,
            _verified_cell(p),
            {"html": product_link(d, buy_url(p["observed_asin"]),
                                  'Listing <span aria-hidden="true">&#8599;</span>', cls="tlink",
                                  aria=f"Open the Amazon listing for {p['ref']} (opens in a new tab)")},
        ])
    table_note = ("Listing column: the official Amazon page this register was transcribed from on "
                  "2026-11-20, and the only evidence a row here rests on. Price and rating are absent "
                  "by rule, not by accident \u2014 Amazon serves that data and this site holds no feed "
                  "that would let it republish it.")
    register = table(["Product", "Category", "Size as stated", "Shape", "Verification", "Listing"],
                     register_rows, cls="register", note=table_note)

    picks = [g for g in GUIDES if g["slug"] in ("basket-or-oven-air-fryer", "where-to-put-the-probe",
                                                "air-fryer-capacity-checklist")]
    guide_grid = "".join(guide_card(d, g) for g in picks)
    head = pagehead(
        "Browse",
        "Shop by category,<br>not by catalogue number",
        ("Two groups, because that is how the question arrives: a machine that cooks with hot air, and a "
         "probe that tells you when it is done. Everything on this page is transcribed from a listing this "
         "project opened, and every row links to it."),
        meta=f"Five products {MIDDLE} two categories {MIDDLE} last checked 20 November 2026",
    )
    lead_section = section("".join(cards), cls="cat-grid")
    table_section = section(
        '<div class="sec-head"><div>' + eyebrow("The whole edit") +
        "<h2>Every product, with the row it came from</h2></div>"
        "<p>A dashboard view for anyone checking the shop rather than shopping it. The last column is what "
        "our records say about how each product's identity was established.</p></div>" + register,
        cls="section-tint",
    )
    guide_section = section(
        '<div class="sec-head"><div>' + eyebrow("Reading further") +
        "<h2>The guides that go with these two categories</h2></div>"
        "<p>The category pages carry the comparison. The guides carry the questions a listing cannot answer.</p></div>"
        '<div class="gcard-grid three">' + guide_grid + "</div>",
        cls="",
    )
    body = head + lead_section + table_section + guide_section
    return page(
        d,
        title="Categories \u2014 air fryers and thermometers | Crisp & Counter",
        description=("Browse the edit by category: three air fryers (dual-basket, single-basket and French-door "
                     "oven) and two thermometers, each row linked to the official listing it was transcribed from."),
        body=body,
        active="products/index.html",
        canonical="categories/",
        structured=breadcrumb_schema([], "Categories", "categories/"),
    )


def _product_block(p, d, approved, index):
    rows = [
        ["Stated size", _stated(p)],
        ["What the listing claims", _features(p)],
        ["Buy it for", (p.get("suits") or ["Not assessed"])[0] or "Not assessed"],
        ["Skip it if", p.get("skip_if") or "No exclusion was recorded for this product"],
        ["Our note", p.get("edit_note") or "No editorial note recorded"],
        ["How this row was checked", _verified_cell(p)],
    ]
    listing = {"html": product_link(d, buy_url(p["observed_asin"]),
                                    'Listing <span aria-hidden="true">&#8599;</span>', cls="tlink",
                                    aria=f"Open the {p['ref']} listing on Amazon (opens in a new tab)")}
    rows = [r + [listing] for r in rows]
    facts = table(["For this pick", "What our records hold", "Evidence"], rows, cls="facts")
    media = (img(d, p["photo"], p["photo_alt"], sizes="(max-width:900px) 100vw, 460px",
                 loading="eager" if index == 0 else "lazy")
             + f'<p class="fig-note">{esc(p.get("photo_note") or "Editorial illustration, not a photograph of this product.")}</p>')
    tagged = ("Links through a Special Link this account validated."
              if p["observed_asin"] in approved else
              f"Untagged listing link {DASH} see the paid-links note for what that means for this site.")
    fine = f"{tagged} Price, rating and delivery are shown on Amazon, where they are always current."
    note_href = esc(rel(d, "products/" + p["ref"].lower() + ".html"))
    return (
        f'<article class="cat-product{"" if index % 2 == 0 else " flip"}" id="{esc(p["ref"].lower())}">'
        f'<div class="cat-product-media">{media}</div>'
        '<div class="cat-product-copy">'
        f'{eyebrow(p["brand"] + " " + MIDDLE + " " + p["format_label"])}'
        f'<h3>{esc(p["name"])}</h3>'
        f'<p class="dek">{esc(p["why"])}</p>'
        f'{facts}'
        f'<p class="cat-cta">{_cta(p, d)} <a class="tlink" href="{note_href}">Read the full note &rarr;</a></p>'
        f'<p class="cat-fine">{esc(fine)}</p>'
        '</div></article>'
    )


def build_category(page_dir, cat):
    d = page_dir
    items = _in(cat["filter"])
    # Resolve by slug, then restore the editorial order named above; a slug that no
    # longer exists is skipped instead of crashing the build.
    wanted = {s: i for i, s in enumerate(cat["guides"])}
    guides = sorted((g for g in GUIDES if g["slug"] in wanted), key=lambda g: wanted[g["slug"]])
    approved = approved_amazon_urls()

    blocks = "".join(_product_block(p, d, approved, i) for i, p in enumerate(items))
    head = pagehead(
        cat["kicker"],
        esc(cat["name"]) + "<br>worth the counter space?",
        cat["dek"],
        meta=(f"{len(items)} products in this category {MIDDLE} {len(guides)} guides "
              f"{MIDDLE} last checked 20 November 2026"),
    )
    products = section(blocks, cls="cat-products")
    method = section(
        '<div class="sec-head"><div>' + eyebrow("Before you buy") +
        "<h2>What to work out here, not on the listing</h2></div>"
        f"<p>{esc(cat['honest'])}</p></div>"
        + note("How this page is built", f"<p>{esc(cat['method'])}</p>"),
        cls="section-tint",
    )
    guide_cards = "".join(guide_card(d, g) for g in guides)
    guide_section = section(
        '<div class="sec-head"><div>' + eyebrow("Read next") +
        f"<h2>Guides for {esc(cat['name'].lower())}</h2></div>"
        "<p>Question-shaped, answer-first, and honest about what a listing can and cannot tell you.</p></div>"
        f'<div class="gcard-grid {"two" if len(guides) < 3 else "three"}">{guide_cards}</div>',
        cls="",
    )
    crumbs = breadcrumbs(d, [("categories/index.html", "Categories")])
    body = crumbs + head + products + method + guide_section
    href = f"categories/{cat['slug']}/"
    schema = {
        "@context": "https://schema.org", "@type": "CollectionPage", "name": cat["name"],
        "description": cat["dek"], "url": "https://karagemop466-tech.github.io/Affil1/" + href,
        "isPartOf": {"@type": "WebSite", "name": "Crisp & Counter"},
    }
    return page(
        d,
        title=f"{cat['name']}: what to compare before you buy | Crisp & Counter",
        description=cat["lead"] + " Every product row links to the official listing it was transcribed from.",
        body=body,
        active="products/index.html",
        canonical=href,
        structured=[
            breadcrumb_schema([("categories/index.html", "Categories")], cat["name"], href),
            schema,
        ],
    )
