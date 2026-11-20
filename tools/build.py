#!/usr/bin/env python3
"""Build the Crisp & Counter static site.

Every page goes through layout.page(), which is the only function that emits a
document shell. That is what guarantees the disclosure strip, the masthead, the
navigation and the footer on all of them, including 404.html.

Internal links are relative because GitHub Pages serves this repository from
/Affil1/ and a root-absolute href such as "/about/" would 404.
"""

import json
from datetime import date
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import layout  # noqa: E402
from layout import page, rel, esc, eyebrow, SITE_NAME, SITE_URL, BUILD_DATE  # noqa: E402
import page_sources
import page_home  # noqa: E402
import page_fit  # noqa: E402
import page_design  # noqa: E402
import page_products  # noqa: E402
import page_guides  # noqa: E402
import page_compare  # noqa: E402
import page_questions  # noqa: E402
import page_suggestions  # noqa: E402
import page_review  # noqa: E402
import page_desk  # noqa: E402
from content import GUIDES  # noqa: E402

sys.path.insert(0, str(ROOT / "kitchen-build"))
import readiness  # noqa: E402

DATA = ROOT / "src" / "data"

# The build writes these and nothing else. Anything not listed is another
# session's or another edition's file and is never touched.
OWNED = [
    "index.html", "404.html",
    "guides", "products", "compare", "questions", "suggestions",
    "review", "about", "operations", "brief", "fit",
    "sitemap.xml", "feed.xml", "robots.txt",
]

# Files this build generates. Anything in an owned directory that is NOT in this
# list belongs to someone else, so clean() must not delete it. This is the
# difference between a rebuild and a wipe.
GENERATED = {
    "index.html", "404.html", "sitemap.xml", "feed.xml", "robots.txt",
    "guides/index.html",
    "products/index.html",
    "products/p-01.html", "products/p-02.html", "products/p-03.html",
    "products/p-04.html", "products/p-05.html",
    "compare/index.html",
    "questions/index.html",
    "suggestions/index.html", "suggestions/design.html", "fit/index.html",
    "review/index.html", "review/images.html", "review/measurement.html",
    "about/index.html",
    "operations/ledger.html", "operations/launch-readiness.html",
    "brief/index.html",
} | {f"guides/{guide['slug']}.html" for guide in GUIDES}

GENERATED.add("sources/index.html")
GENERATED.update(f"guides/{g['slug']}.html" for g in GUIDES)

# Files THIS build emitted in an earlier version, now renamed, which must be
# removed when the slug list changes. It contains nothing that predates this
# build: guides/basket-or-oven.html and guides/capacity-checklist.html belong to
# a parallel edition on main and are still served, so deleting them here would
# destroy another session's work. Verified by rebuilding and diffing the tree.
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
    """Remove only this build's own outputs.

    The first version of this function wiped every owned directory. On a branch
    that also carries other sessions' pages, a rebuild would have deleted their
    work. Clean is now derived from GENERATED, so adding a foreign file to an
    owned directory is safe and the build still cannot leave a stale page of its
    own behind."""
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
        if p in ("404.html", "operations/launch-readiness.html"):
            continue
        loc = SITE_URL + "/" + (p[:-len("index.html")] if p.endswith("index.html") else p)
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{BUILD_DATE}</lastmod></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def feed(latest_guides):
    items = []
    for g in sorted(latest_guides, key=lambda item: item['updated'], reverse=True):
        published = date.fromisoformat(g.get('published', g['updated'])).strftime('%a, %d %b %Y 00:00:00 GMT')
        link = f"{SITE_URL}/guides/{g['slug']}.html"
        items.append(f"""  <item>
    <title>{esc(g['title'])}</title>
    <link>{link}</link>
    <guid isPermaLink="true">{link}</guid>
    <pubDate>{published}</pubDate>
    <description>{esc(g['dek'])}</description>
  </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{esc(SITE_NAME)} \u2014 buying guides</title>
  <link>{SITE_URL}/</link>
  <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
  <description>Practical guides to air fryers, countertop ovens, and cooking thermometers.</description>
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
    meta = {"tracking": products_doc["meta"].get("tracking_id_supplied")}
    sources = load("sources.json")
    questions = load("questions.json")
    suggestions = load("suggestions.json")
    flags = load("flags.json")
    images = load("images.json")

    intent = json.loads(readiness.INTENT.read_text(encoding="utf-8"))
    readiness.validate(intent)
    if {p['ref']: (p['submitted_link'], p['listing_url']) for p in products} != {
        p['ref']: (p['submitted_link'], p['observed_redirect_target']) for p in intent['records']
    }:
        raise SystemExit("Root register and affiliate evidence records disagree")
    meta["approved_links"] = {
        p["ref"]: p["approved_special_link"] for p in intent["records"]
        if readiness.eligible(p, intent["tracking_id_supplied"])
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
        pages.append(write(f"guides/{g['slug']}.html", page_guides.build_guide("guides", g, meta)))

    # products
    pages.append(write("products/index.html", page_products.build_register("products", products, meta)))
    for p in products:
        pages.append(write(f"products/{p['ref'].lower()}.html", page_products.build_product("products", p, meta)))

    pages.append(write("fit/index.html", page_fit.build("fit")))
    pages.append(write("suggestions/design.html", page_design.build("suggestions")))

    # compare / questions / suggestions
    pages.append(write("compare/index.html", page_compare.build("compare", products, meta)))
    pages.append(write("questions/index.html", page_questions.build("questions", questions, meta)))
    pages.append(write("suggestions/index.html", page_suggestions.build("suggestions", suggestions, meta)))

    # review
    pages.append(write("review/index.html", page_review.build_index("review", flags, meta)))
    pages.append(write("review/images.html", page_review.build_images("review", images, products, meta)))
    pages.append(write("review/measurement.html", page_review.build_measurement("review", meta, load("events.json"))))

    # desk
    pages.append(write("about/index.html", page_desk.build_about("about", sources, meta)))
    pages.append(write("sources/index.html", page_sources.build("sources",sources,products)))
    pages.append(write("operations/ledger.html", page_desk.build_ledger("operations", meta)))
    pages.append(write("operations/launch-readiness.html", readiness.render(intent)))
    pages.append(write("brief/index.html", page_desk.build_brief("brief", products, questions, flags, meta)))

    pages.append(write("sitemap.xml", sitemap(pages)))
    pages.append(write("feed.xml", feed(GUIDES)))
    pages.append(write("robots.txt", ROBOTS))

    built = {p for p in pages}
    if GENERATED != built:
        raise SystemExit(f"Page manifest mismatch: missing={sorted(GENERATED - built)}, extra={sorted(built - GENERATED)}")
    print(f"built {len([p for p in pages if p.endswith('.html')])} pages")
    for p in pages:
        print("  " + p)


if __name__ == "__main__":
    main()
