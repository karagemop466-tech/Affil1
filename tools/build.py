#!/usr/bin/env python3
"""Build the Crisp & Counter static site.

Every page goes through layout.page(), which is the only function that emits a
document shell. That is what guarantees the disclosure strip, the masthead, the
navigation and the footer on all of them, including 404.html.

Internal links are relative because GitHub Pages serves this repository from
/Affil1/ and a root-absolute href such as "/about/" would 404.
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import layout  # noqa: E402
from layout import page, rel, esc, eyebrow, SITE_NAME, SITE_URL, BUILD_DATE  # noqa: E402
import page_home  # noqa: E402
import page_products  # noqa: E402
import page_guides  # noqa: E402
import page_compare  # noqa: E402
import page_questions  # noqa: E402
import page_suggestions  # noqa: E402
import page_review  # noqa: E402
import page_desk  # noqa: E402
from content import GUIDES  # noqa: E402

DATA = ROOT / "src" / "data"

# Files this build generates. Anything in an owned directory that is NOT in this
# list belongs to another session/edition, so clean() must not delete it.
GENERATED = {
    "index.html", "404.html", "sitemap.xml", "feed.xml", "robots.txt",
    "guides/index.html",
    "guides/basket-or-oven-air-fryer.html",
    "guides/instant-read-vs-wireless-meat-thermometer.html",
    "guides/air-fryer-capacity-checklist.html",
    "guides/cleanup-and-counter-space.html",
    "guides/batch-cooking-air-fryer-formats.html",
    "guides/holiday-roast-and-air-fryer-playbook.html",
    "guides/multi-function-kitchen-appliance-questions.html",
    "products/index.html",
    "products/air-fryers.html",
    "products/thermometers.html",
    "products/p-01.html", "products/p-02.html", "products/p-03.html",
    "products/p-04.html", "products/p-05.html",
    "compare/index.html",
    "questions/index.html",
    "suggestions/index.html",
    "review/index.html", "review/images.html", "review/measurement.html",
    "about/index.html",
    "operations/ledger.html",
    "brief/index.html",
}

# Only files THIS build emitted in an earlier version and retired. Never
# contains files from parallel sessions.
RETIRED = [
    "guides/cleanup-counterspace.html",
]


def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return json.load(fh)


def write(rel_path, content):
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return rel_path


def clean():
    """Remove only this build's own outputs."""
    for rel_path in sorted(GENERATED) + RETIRED:
        path = ROOT / rel_path
        if path.is_file():
            path.unlink()


def favicon():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect width="32" height="32" rx="7" fill="#1f3a30"/>
<path d="M9 21c1.8-6.5 5.6-10 12-10-1.8 6.5-5.6 10-12 10z" fill="#e9b44c"/>
<circle cx="21.5" cy="10.5" r="1.7" fill="#f5efe2"/>
</svg>"""
    path = ROOT / "assets/img/favicon.svg"
    path.write_text(svg, encoding="utf-8")


def sitemap(pages):
    """Canonical URLs. A directory index is listed as its directory, because
    that is the URL the canonical tag on that page names."""
    urls = []
    for p in pages:
        if p == "404.html":
            continue
        loc = SITE_URL + "/" + (p[:-len("index.html")] if p.endswith("index.html") else p)
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{BUILD_DATE}</lastmod></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def feed(latest_guides):
    items = []
    for g in latest_guides:
        link = f"{SITE_URL}/guides/{g['slug']}.html"
        items.append(f"""  <item>
    <title>{esc(g['title'])}</title>
    <link>{link}</link>
    <guid isPermaLink="true">{link}</guid>
    <pubDate>Fri, 20 Nov 2026 00:00:00 GMT</pubDate>
    <description>{esc(g['dek'])}</description>
  </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{esc(SITE_NAME)} \u2014 buying guides</title>
  <link>{SITE_URL}/</link>
  <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
  <description>Air-fryer and meat-thermometer buying guides that verify every link and source before describing a product.</description>
  <language>en-us</language>
  <lastBuildDate>Fri, 20 Nov 2026 00:00:00 GMT</lastBuildDate>
  <copyright>2026 {esc(SITE_NAME)}</copyright>
{chr(10).join(items)}
</channel>
</rss>
"""


ROBOTS = """User-agent: *
Allow: /

Sitemap: https://karagemop466-tech.github.io/Affil1/sitemap.xml
"""


def main():
    products_doc = load("products.json")
    products = products_doc["products"]
    sources = load("sources.json")
    questions = load("questions.json")
    suggestions = load("suggestions.json")
    flags = load("flags.json")
    images = load("images.json")

    html_count = sum(1 for p in GENERATED if p.endswith(".html"))
    meta = {
        "tracking": products_doc["meta"].get("tracking_id_supplied"),
        "page_count": html_count,
    }

    clean()
    favicon()

    pages = []

    # root
    pages.append(write("index.html", page_home.build("", products, meta)))
    pages.append(write("404.html", page_desk.build_404("", meta)))

    # guides
    pages.append(write("guides/index.html", page_guides.build_index("guides", meta)))
    for g in GUIDES:
        pages.append(write(f"guides/{g['slug']}.html", page_guides.build_guide("guides", g, products, meta)))

    # products & category subpages
    pages.append(write("products/index.html", page_products.build_register("products", products, meta)))
    pages.append(write("products/air-fryers.html", page_products.build_category(
        "products", products,
        slug="air-fryers",
        label="Air Fryers",
        kicker="Category 01 · Air Fryers",
        headline="Three air-fryer shapes,<br>verified on Amazon",
        dek="Dual-basket 6-quart drawer (P-01), French-door 26-quart countertop oven (P-02), and single 8-quart basket (P-03) — every listing verified on 20 November 2026 with zero invented prices or ratings.",
        note_html='<p class="table-note">All three listings sit under Amazon&rsquo;s <em>Home &amp; Kitchen &gt; Kitchen &amp; Dining &gt; Small Appliances &gt; Fryers &gt; Air Fryers</em> breadcrumb.</p>',
        meta=meta,
    )))
    pages.append(write("products/thermometers.html", page_products.build_category(
        "products", products,
        slug="thermometers",
        label="Meat Thermometers",
        kicker="Category 02 · Meat Thermometers",
        headline="Two meat thermometers:<br>instant-read &amp; wireless",
        dek="A handheld 1-second digital probe (P-04) and a 3-probe wireless smart kit (P-05) — both verified under Amazon&rsquo;s Thermometers &amp; Timers &gt; Meat category and paired with official USDA FSIS safe temperature guidance.",
        note_html='<p class="table-note">Both listings sit under Amazon&rsquo;s <em>Home &amp; Kitchen &gt; Kitchen &amp; Dining &gt; Kitchen Utensils &amp; Gadgets &gt; Thermometers &amp; Timers &gt; Meat</em> breadcrumb. Safe minimum internal temperatures are sourced from USDA FSIS (<a href="../about/index.html#sources">SRC-06, SRC-07</a>).</p>',
        meta=meta,
    )))
    for p in products:
        pages.append(write(f"products/{p['ref'].lower()}.html", page_products.build_product("products", p, meta)))

    # compare / questions / suggestions
    pages.append(write("compare/index.html", page_compare.build("compare", products, meta)))
    pages.append(write("questions/index.html", page_questions.build("questions", questions, meta)))
    pages.append(write("suggestions/index.html", page_suggestions.build("suggestions", suggestions, meta)))

    # review
    pages.append(write("review/index.html", page_review.build_index("review", flags, meta)))
    pages.append(write("review/images.html", page_review.build_images("review", images, products, meta)))
    pages.append(write("review/measurement.html", page_review.build_measurement("review", meta)))

    # desk
    pages.append(write("about/index.html", page_desk.build_about("about", sources, products, meta)))
    pages.append(write("operations/ledger.html", page_desk.build_ledger("operations", meta)))
    pages.append(write("brief/index.html", page_desk.build_brief("brief", products, questions, flags, meta)))

    pages.append(write("sitemap.xml", sitemap(pages)))
    pages.append(write("feed.xml", feed(GUIDES)))
    pages.append(write("robots.txt", ROBOTS))

    built = {p for p in pages}
    missing = GENERATED - built - {"robots.txt"}
    extra = built - GENERATED
    if missing:
        raise SystemExit(f"GENERATED lists files the build never wrote: {sorted(missing)}")
    if extra:
        raise SystemExit(f"Build wrote files not listed in GENERATED: {sorted(extra)}")
    print(f"built {len([p for p in pages if p.endswith('.html')])} pages")
    for p in pages:
        print("  " + p)


if __name__ == "__main__":
    main()
