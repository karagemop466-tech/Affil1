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
sys.path.insert(0, str(ROOT / "_tools"))

import layout  # noqa: E402
from layout import page, rel, esc, eyebrow, SITE_NAME, SITE_URL, BUILD_DATE  # noqa: E402
import page_home  # noqa: E402
import page_fit  # noqa: E402
import page_design  # noqa: E402
import page_products  # noqa: E402
import page_guides  # noqa: E402
import page_compare  # noqa: E402
import page_questions  # noqa: E402
import page_suggestions  # noqa: E402
import page_decisions  # noqa: E402
import page_decide  # noqa: E402
import page_now  # noqa: E402
import page_offers  # noqa: E402
import page_crosscheck  # noqa: E402
import page_review  # noqa: E402
import page_desk  # noqa: E402
from content import GUIDES  # noqa: E402

DATA = ROOT / "_src" / "data"

# The build writes these and nothing else. Anything not listed is either a
# static asset or an archived edition, and is never touched.
OWNED = [
    "index.html", "404.html",
    "guides", "products", "compare", "questions", "suggestions", "decide",
    "now", "offers", "verification", "decisions",
    "review", "about", "operations", "brief",
    "sitemap.xml", "feed.xml", "robots.txt",
]

GENERATED = {
    "index.html", "404.html", "sitemap.xml", "feed.xml", "robots.txt",
    "guides/index.html",
    "products/index.html",
    "products/p-01.html", "products/p-02.html", "products/p-03.html",
    "products/p-04.html", "products/p-05.html",
    "compare/index.html",
    "questions/index.html",
    "suggestions/index.html", "suggestions/design.html", "fit/index.html",
    "decisions/index.html",
    "decide/index.html",
    "now/index.html", "offers/index.html", "verification/index.html",
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
    """Canonical URLs only. A directory index is listed as its directory."""
    urls = [f"  <url><loc>{as_url(p)}</loc><lastmod>{BUILD_DATE}</lastmod></url>"
            for p in pages if p != "404.html"]
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


# One canonical site. The archived edition under _archive/, the internal
# decision desk under _decision-support/ and the parallel Countertop Almanac
# edition under edition/ are all reachable for human review but carry
# noindex, and none is listed in the sitemap. Disallow their served paths here
# as well, so a crawler that ignores the meta tag is still blocked. The path
# must be the served one (/_archive/, not /archive/) — an earlier revision
# disallowed /archive/, which never matched the real directory. Nothing here
# blocks crawling of the canonical pages.
# Why the published file above carries no "Disallow: /edition/" line.
#
# The annex at /Affil1/edition/ is a preserved review surface of the same five listings, and
# main's FLG-037 asks that it stop competing for the index. The mechanism it now uses is a
# per-page <meta name="robots" content="noindex, follow"> (asserted for all 27 pages by
# _platform/verify_edition.py). Blocking the crawl would defeat that: Google reads an indexing
# instruction "only if crawlers are allowed to access the pages that include these settings",
# while a URL disallowed in robots.txt "can still be indexed if linked to from other sites" -
# and the shop links to the annex from its review and question pages. A Disallow line here
# therefore produces indexed annex pages with no description, which is worse than the tag
# alone. Read 2026-11-20:
#   https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
#   https://developers.google.com/search/docs/crawling-indexing/robots/intro
# Two sessions' fixes for the same annex met in main and contradicted each other; FLG-044
# records the resolution rather than hiding it.
ROBOTS = """User-agent: *
Allow: /
Disallow: /_archive/

Disallow: /_decision-support/

# The /edition/ annex is held out of the index by a per-page noindex tag, not by a
# Disallow rule here: a blocked page cannot show you its tag, and its URLs can still be
# indexed from the links this site points at it. See _tools/build.py notes and FLG-044.
Sitemap: https://karagemop466-tech.github.io/Affil1/sitemap.xml
"""


# No "Disallow: /edition/". The annex at /Affil1/edition/ is kept out of the index by
# a noindex meta tag on each of its pages (FLG-030, FLG-036), and blocking the crawl
# defeats that: Google reads a indexing tag "only if crawlers are allowed to access the
# pages that include these settings", while a URL disallowed in robots.txt "can still be
# indexed if linked to from other sites" - so a Disallow line here produces indexed
# annex pages with no description, which is the worse outcome of the two. Sources:
#   https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
#   https://developers.google.com/search/docs/crawling-indexing/robots/intro
# A subdirectory robots.txt is not read at all, so edition/robots.txt cannot say this.


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
    pages.append(write("products/index.html", page_products.build_register("products", products, meta)))
    for p in products:
        pages.append(write(f"products/{p['ref'].lower()}.html", page_products.build_product("products", p, meta)))

    pages.append(write("fit/index.html", page_fit.build("fit")))
    pages.append(write("suggestions/design.html", page_design.build("suggestions")))

    # compare / questions / suggestions
    pages.append(write("compare/index.html", page_compare.build("compare", products, meta)))
    pages.append(write("questions/index.html", page_questions.build("questions", questions, meta)))
    pages.append(write("decide/index.html", page_decide.build("decide", decisions, meta)))

    # the choice surface: what is left, what to do first, what each page claims
    pages.append(write("now/index.html", page_now.build("now")))
    pages.append(write("offers/index.html", page_offers.build("offers")))
    pages.append(write("verification/index.html", page_crosscheck.build("verification")))
    pages.append(write("suggestions/index.html", page_suggestions.build("suggestions", suggestions, meta)))
    pages.append(write("decisions/index.html", page_decisions.build("decisions")))

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
    # the first was checked. _tools/check.py derives the set of pages it examines
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
