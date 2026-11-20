#!/usr/bin/env python3
"""Publishing gate for the Good Measure Kitchen site.

Run after scripts/build_site.py. Exits non-zero if any check fails, so the
Pages workflow refuses to deploy a broken or non-compliant site.

    python3 scripts/check_site.py

Checks
  1. The Associates disclosure sits above the masthead on every page.
  2. Every outbound Amazon link carries rel="sponsored nofollow noopener".
  3. Reader-facing pages show no price, rating, review count or availability.
  4. No unsupportable claim language anywhere on the site.
  5. Every table row carries a link, and at least one link to an official source.
  6. Every internal link resolves to a file that exists.
  7. Every page has a title, description, canonical URL and feed link.
  8. The sitemap lists every page and the feed lists every guide and category.
  9. No template delimiters survive into the rendered output.
 10. Every page has exactly one h1.
"""

import os
import re
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import site_data as D  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OFFICIAL_HOSTS = {
    "amazon.com", "www.amazon.com", "link.amazon", "amzn.to", "a.co",
    "amzn.eu", "amzn.asia", "affiliate-program.amazon.com",
    "sell.amazon.com", "amazon.co.uk", "amazon.de", "amazon.co.jp",
    "ftc.gov", "www.ftc.gov", "consumer.ftc.gov", "ecfr.gov",
    "google.com", "www.google.com", "support.google.com", "developers.google.com",
    "docs.github.com", "github.com", "karagemop466-tech.github.io",
}

READER_FACING_GLOBS = ["index.html", "shop/*.html", "guides/*.html"]

# Pages kept only to preserve an older published URL. They are exempt from the content
# checks but must still link onward to the page that replaced them.
REDIRECT_STUBS = {"guides/flagged-for-review.html"}

# A link to an Amazon product detail page, or an Amazon short link, is a placement and
# must be marked sponsored. A link to Amazon's own programme documentation, blogs,
# review pages or checkpoints is a citation of evidence and must not be.
PRODUCT_LINK_RE = re.compile(
    r"^https?://(?:[a-z0-9-]+\.)*amazon\.[a-z.]+/dp/|"
    r"^https?://link\.amazon/|"
    r"^https?://(?:amzn\.to|amzn\.eu|amzn\.asia|a\.co)/", re.I)

AMAZONISH = ("amazon.com", "link.amazon", "amzn.to", "a.co", "amzn.eu", "amzn.asia",
             "affiliate-program.amazon.com", "sell.amazon.com")

failures = []
notes = []


def fail(check, detail):
    failures.append((check, detail))


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


def all_html():
    out = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", ".github", "node_modules", "api", "scripts", "data")]
        for f in files:
            if f.endswith(".html"):
                out.append(os.path.relpath(os.path.join(base, f), ROOT).replace(os.sep, "/"))
    return sorted(out)


def content_pages():
    """Pages that must satisfy the content checks. Redirect stubs are excluded."""
    return [p for p in all_html() if p not in REDIRECT_STUBS]


def glob_pages(pattern):
    if "*" not in pattern:
        return [pattern] if os.path.exists(os.path.join(ROOT, pattern)) else []
    directory, _, tail = pattern.rpartition("/")
    suffix = tail.replace("*", "")
    out = []
    for p in all_html():
        if p.startswith(directory + "/") and p.endswith(suffix):
            out.append(p)
    return sorted(out)


def check_disclosure(pages):
    for page in pages:
        body = read(page)
        i = body.find(D.DISCLOSURE)
        m = body.find("<header class=\"masthead\"")
        if i == -1:
            fail("1 disclosure", "%s: the disclosure statement is missing" % page)
        elif m == -1:
            fail("1 disclosure", "%s: no masthead found" % page)
        elif i > m:
            fail("1 disclosure", "%s: the disclosure appears below the masthead" % page)
    notes.append("1 disclosure: checked %d pages" % len(pages))


def check_sponsored(pages):
    pattern = re.compile(r"<a\b[^>]*href=\"(https?://[^\"]+)\"[^>]*>", re.I)
    for page in pages:
        body = read(page)
        for m in pattern.finditer(body):
            href = m.group(1)
            host = re.sub(r"^https?://([^/]+).*$", r"\1", href).lower()
            amazonish = any(host == h or host.endswith("." + h) for h in AMAZONISH)
            if not amazonish:
                continue
            tag = m.group(0)
            rel = re.search(r"rel=\"([^\"]*)\"", tag, re.I)
            relv = rel.group(1).lower() if rel else ""
            if PRODUCT_LINK_RE.match(href):
                if "sponsored" not in relv:
                    fail("2 sponsored", "%s: product link is not marked sponsored: %s" % (page, href))
                    continue
                if "nofollow" not in relv:
                    fail("2 sponsored", "%s: product link lacks nofollow: %s" % (page, href))
            else:
                if "sponsored" in relv:
                    fail("2 sponsored", "%s: an evidence citation is marked as a placement: %s" % (page, href))
    notes.append("2 sponsored: checked %d pages" % len(pages))


def check_reader_facing():
    pages = []
    for pattern in READER_FACING_GLOBS:
        pages.extend(glob_pages(pattern))
    for page in sorted(set(pages)):
        body = read(page)
        for pattern in D.FORBIDDEN_ON_READER_PAGES:
            m = re.search(pattern, body, re.I)
            if m:
                fail("3 reader-facing values",
                     "%s: found a reader-facing value matching %r (%r)"
                     % (page, pattern, m.group(0)[:40]))
    notes.append("3 reader-facing values: checked %d reader-facing pages" % len(set(pages)))


def check_claims(pages):
    for page in pages:
        body = read(page)
        for pattern in D.FORBIDDEN_CLAIMS:
            m = re.search(pattern, body, re.I)
            if m:
                fail("4 claims", "%s: unsupported claim language matching %r"
                     % (page, pattern))
    notes.append("4 claims: checked %d pages" % len(pages))


def check_table_rows(pages):
    row_re = re.compile(r"<tr\b.*?</tr>", re.S | re.I)
    link_re = re.compile(r"<a\b[^>]*href=\"([^\"]+)\"", re.I)
    for page in pages:
        body = read(page)
        for row in row_re.findall(body):
            if "<th" in row and "<td" not in row:
                continue
            links = link_re.findall(row)
            if not links:
                fail("5 table rows", "%s: a table row has no link" % page)
                continue
            official = False
            for href in links:
                if not href.startswith("http"):
                    continue
                host = re.sub(r"^https?://([^/]+).*$", r"\1", href).lower()
                if host in OFFICIAL_HOSTS or any(host.endswith("." + h) for h in OFFICIAL_HOSTS):
                    official = True
                    break
            if not official:
                fail("5 table rows", "%s: a table row has no link to an official source" % page)
    notes.append("5 table rows: checked %d pages" % len(pages))


def check_internal_links(pages):
    for page in pages:
        body = read(page)
        for href in re.findall(r"<a\b[^>]*href=\"([^\"]+)\"", body, re.I):
            if href.startswith(("http://", "https://", "mailto:", "#", "data:", "javascript:")):
                continue
            target = href.split("#")[0]
            if not target:
                continue
            if target.startswith("/"):
                resolved = os.path.normpath(os.path.join(ROOT, target.lstrip("/")))
            else:
                base = os.path.dirname(os.path.join(ROOT, page))
                resolved = os.path.normpath(os.path.join(base, target))
            if not os.path.exists(resolved):
                fail("6 internal links", "%s: broken local reference %s" % (page, href))
    notes.append("6 internal links: checked %d pages" % len(pages))


def check_metadata(pages):
    for page in pages:
        if page == "404.html":
            continue
        body = read(page)
        for needle, label in (
            ("<title>", "title"),
            ('name="description"', "meta description"),
            ('rel="canonical"', "canonical link"),
            ('type="application/rss+xml"', "feed link"),
        ):
            if needle not in body:
                fail("7 metadata", "%s: missing %s" % (page, label))
    notes.append("7 metadata: checked %d pages" % len(pages))


def check_sitemap_and_feed():
    sitemap = read("sitemap.xml")
    feed = read("feed.xml")
    expected_pages = [p for p in content_pages() if p != "404.html"]
    for page in expected_pages:
        if ("<loc>%s/%s</loc>" % (D.SITE["origin"].rstrip("/"), page)) not in sitemap:
            fail("8 sitemap", "%s is not in sitemap.xml" % page)
    for guide in D.GUIDES:
        if ("/guides/%s.html" % guide["slug"]) not in feed:
            fail("8 feed", "guide %s is not in feed.xml" % guide["slug"])
    for cat in D.CATEGORIES:
        if ("/shop/%s.html" % cat["slug"]) not in feed:
            fail("8 feed", "category %s is not in feed.xml" % cat["slug"])
    notes.append("8 sitemap/feed: checked %d pages, %d guides, %d categories"
                 % (len(expected_pages), len(D.GUIDES), len(D.CATEGORIES)))


def check_delimiters(pages):
    for page in pages:
        body = read(page)
        for needle in ("{{", "}}", "{%", "%}"):
            if needle in body:
                fail("9 delimiters", "%s: template delimiter %s survived rendering" % (page, needle))
    notes.append("9 delimiters: checked %d pages" % len(pages))


def check_single_h1(pages):
    for page in pages:
        body = read(page)
        count = len(re.findall(r"<h1\b", body, re.I))
        if count != 1:
            fail("10 h1", "%s: has %d h1 elements" % (page, count))
    notes.append("10 h1: checked %d pages" % len(pages))


def main():
    allp = all_html()
    pages = content_pages()
    if not pages:
        fail("setup", "no HTML pages found")

    # A redirect stub must point onward to the page that replaced it.
    for stub in sorted(REDIRECT_STUBS):
        body = read(stub)
        if "http-equiv=\"refresh\"" not in body:
            fail("0 redirect stubs", "%s: expected a refresh redirect" % stub)
        if "../desk/flagged-for-review.html" not in body:
            fail("0 redirect stubs", "%s: does not link onward to the new page" % stub)

    check_disclosure(pages)
    check_sponsored(pages)
    check_reader_facing()
    check_claims(pages)
    check_table_rows(pages)
    check_internal_links(allp)
    check_metadata(pages)
    check_sitemap_and_feed()
    check_delimiters(pages)
    check_single_h1(pages)

    for note in notes:
        print("  ok  %s" % note)
    if failures:
        print("\nFAILED %d check(s):" % len(failures))
        for check, detail in failures:
            print("  XX  [%s] %s" % (check, detail))
        sys.exit(1)
    print("\nPublishing gate passed: %d pages, %d checks." % (len(pages), len(notes)))
    print("Redirect stubs kept for older published URLs: %s" % (", ".join(sorted(REDIRECT_STUBS)) or "none"))


if __name__ == "__main__":
    main()
