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
import page_fit  # noqa: E402
import page_design  # noqa: E402
import page_start  # noqa: E402
import page_products  # noqa: E402
import page_guides  # noqa: E402
import page_compare  # noqa: E402
import page_questions  # noqa: E402
import page_suggestions  # noqa: E402
import page_decide  # noqa: E402
import page_review  # noqa: E402
import page_desk  # noqa: E402
from content import GUIDES  # noqa: E402

DATA = ROOT / "src" / "data"

# The build writes these and nothing else. Anything not listed is either a
# static asset or an archived edition, and is never touched.
OWNED = [
    "index.html", "404.html",
    "guides", "start", "products", "compare", "questions", "suggestions", "decide",
    "review", "about", "operations", "brief",
    "sitemap.xml", "feed.xml", "robots.txt",
]

GENERATED = {
    "index.html", "404.html", "sitemap.xml", "feed.xml", "robots.txt",
    "guides/index.html",
    "start/index.html",
    "products/index.html",
    "products/p-01.html", "products/p-02.html", "products/p-03.html",
    "products/p-04.html", "products/p-05.html",
    "compare/index.html",
    "questions/index.html",
    "suggestions/index.html", "suggestions/design.html", "fit/index.html",
    "decide/index.html",
    "review/index.html", "review/images.html", "review/measurement.html",
    "about/index.html",
    "operations/ledger.html",
    "brief/index.html",
}
GENERATED |= {f"guides/{g['slug']}.html" for g in GUIDES}


def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return json.load(fh)


def write(rel_path, content):
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return rel_path


def clean():
    """Remove only this build's own outputs, never a foreign or archived file."""
    for rel_path in sorted(GENERATED):
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


def as_url(p):
    return SITE_URL + "/" + (p[:-len("index.html")] if p.endswith("index.html") else p)


def sitemap(pages):
    """Canonical URLs a reader could want. A directory index is its directory.

    Which pages belong in a sitemap is decided once, in `publish.in_sitemap`,
    because three separate gates read the answer: this builder, tools/check.py
    and tools/validate.py. Duplicating the rule here is how the earlier edition
    ended up with a sitemap that listed the repository's audit trail.
    """
    from publish import in_sitemap
    urls = [f"  <url><loc>{as_url(p)}</loc><lastmod>{BUILD_DATE}</lastmod></url>"
            for p in pages if in_sitemap(p)]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def feed(guides):
    items = []
    for g in guides:
        link = f"{SITE_URL}/guides/{g['slug']}.html"
        items.append(f"""  <item>
    <title>{esc(g['title'])}</title>
    <link>{link}</link>
    <guid isPermaLink="true">{link}</guid>
    <pubDate>Fri, 20 Nov 2026 00:00:00 GMT</pubDate>
    <category>{esc(g['cluster'])}</category>
    <description>{esc(g['dek'])}</description>
  </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{esc(SITE_NAME)} \u2014 guides</title>
  <link>{SITE_URL}/</link>
  <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
  <description>Air-fryer and thermometer buying guides, with each product link checked against the live Amazon listing.</description>
  <language>en-us</language>
  <lastBuildDate>Fri, 20 Nov 2026 00:00:00 GMT</lastBuildDate>
  <copyright>2026 {esc(SITE_NAME)}</copyright>
{chr(10).join(items)}
</channel>
</rss>
"""


# One canonical site. The archived edition under archive/ carries noindex, and
# /archive/ is not listed in the sitemap. Nothing here blocks crawling of the
# canonical pages.
# `/archive/` holds superseded editions kept for review. They are deliberately
# excluded from the Pages build (tools/publish.py) so they are not served at all;
# the Disallow below is defence in depth for any route that serves them again.
#
# The earlier wording here said "/archive/ is not listed in the sitemap", which
# was true and insufficient: the files were still published and still parseable,
# and one archive page was a complete second storefront with tagged buy links.
# See FLG-026.
ROBOTS = """User-agent: *
Allow: /
Disallow: /archive/

Sitemap: https://karagemop466-tech.github.io/Affil1/sitemap.xml
"""


def main():
    products_doc = load("products.json")
    products = products_doc["products"]
    meta = {"tracking": products_doc["meta"].get("tracking_id_supplied")}
    sources = load("sources.json")
    questions = load("questions.json")
    suggestions = load("suggestions.json")
    decisions = load("decisions.json")
    flags = load("flags.json")
    images = load("images.json")

    clean()
    favicon()

    pages = []

    # root
    pages.append(write("index.html", page_home.build("", products, meta)))
    pages.append(write("404.html", page_desk.build_404("", meta)))

    # guides
    pages.append(write("guides/index.html", page_guides.build_index("guides")))
    for g in GUIDES:
        pages.append(write(f"guides/{g['slug']}.html", page_guides.build_guide("guides", g, meta)))

    # products
    pages.append(write("start/index.html", page_start.build("start", products_doc, GUIDES)))
    pages.append(write("products/index.html", page_products.build_register("products", products, meta)))
    for p in products:
        pages.append(write(f"products/{p['ref'].lower()}.html", page_products.build_product("products", p, meta)))

    pages.append(write("fit/index.html", page_fit.build("fit")))
    pages.append(write("suggestions/design.html", page_design.build("suggestions")))

    # compare / questions / suggestions
    pages.append(write("compare/index.html", page_compare.build("compare", products, meta)))
    pages.append(write("questions/index.html", page_questions.build("questions", questions, meta)))
    pages.append(write("decide/index.html", page_decide.build("decide", decisions, meta)))
    pages.append(write("suggestions/index.html", page_suggestions.build("suggestions", suggestions, meta)))

    # review
    pages.append(write("review/index.html", page_review.build_index("review", flags, meta)))
    pages.append(write("review/images.html", page_review.build_images("review", images, products, meta)))
    pages.append(write("review/measurement.html", page_review.build_measurement("review", meta)))

    # desk
    pages.append(write("about/index.html", page_desk.build_about("about", sources, meta)))
    pages.append(write("operations/ledger.html", page_desk.build_ledger("operations", meta)))
    pages.append(write("brief/index.html", page_desk.build_brief("brief", products, questions, flags, meta)))

    pages.append(write("sitemap.xml", sitemap(pages)))
    pages.append(write("feed.xml", feed(GUIDES)))
    pages.append(write("robots.txt", ROBOTS))

    built = set(pages)
    missing = GENERATED - built - {"robots.txt"}
    if missing:
        raise SystemExit(f"GENERATED lists files the build never wrote: {sorted(missing)}")
    # The other direction matters just as much, and until this guard existed only
    # the first was checked. tools/check.py derives the set of pages it examines
    # from GENERATED, so a page that is written but not listed is a page the
    # checker never opens -- while still reporting a clean run. Two guides were
    # published that way before this was caught.
    unlisted = built - GENERATED
    if unlisted:
        raise SystemExit("build wrote pages that GENERATED does not list, so the checker "
                         f"would skip them: {sorted(unlisted)}")
    print(f"built {len([p for p in pages if p.endswith('.html')])} pages")
    for p in pages:
        print("  " + p)


if __name__ == "__main__":
    main()
