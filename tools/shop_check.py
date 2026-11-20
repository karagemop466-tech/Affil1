#!/usr/bin/env python3
"""Pre-publish checks for shop/. Exits non-zero on any failure.

These are the gates that stop a page shipping without its obligations:

  C1  every page has the exact required disclosure sentence
  C2  the disclosure appears BEFORE the first outbound product link
  C3  every outbound Amazon link carries rel containing "sponsored"
  C4  every outbound Amazon link carries the Associates tag as a parameter
  C5  every outbound Amazon link is a direct amazon.com URL (no redirector)
  C6  no price, rating, review-count or availability figure is published
  C7  every local href/src resolves to a real file
  C8  every page declares a canonical URL and a title
  C9  every JSON-LD block parses
  C10 sitemap.xml and feed.xml parse; every sitemap URL has a file
  C11 every page links to the disclosure explanation
  C12 no root-absolute paths (the site is served under /Affil1/)
  C13 every product page links to its own ASIN and tag exactly once per CTA
  C14 no page is orphaned: every generated page is linked from somewhere
"""

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent.parent
SHOP = ROOT / "archive" / "2026-11-20-pantry-journal"
TAG = "shopnow047c-20"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."

errors = []
notes = []


def fail(check, msg):
    errors.append(f"[{check}] {msg}")


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []        # (href, rel, attrs_dict)
        self.refs = []         # (kind, value)
        self.has_canonical = False
        self.title = None
        self._in_title = False
        self.jsonld = []
        self._in_jsonld = False
        self.disclosure_pos = None
        self.serial = 0
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self.serial += 1
        if tag == "link" and d.get("rel") == "canonical":
            self.has_canonical = True
        if tag == "title":
            self._in_title = True
        if tag == "script" and d.get("type") == "application/ld+json":
            self._in_jsonld = True
            self.jsonld.append("")
        if tag == "a" and d.get("href"):
            self.links.append((d["href"], d.get("rel", ""), d, self.serial))
            self.refs.append(("href", d["href"]))
        if tag in ("img", "script", "source") and d.get("src"):
            self.refs.append(("src", d["src"]))

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_jsonld:
            self._in_jsonld = False

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data
        if self._in_jsonld:
            self.jsonld[-1] += data
        self.text_parts.append(data)
        if self.disclosure_pos is None and "As an Amazon Associate" in data:
            self.disclosure_pos = self.serial


def is_product_link(href):
    """True only for a link to an Amazon product detail page."""
    u = urlparse(href)
    host = u.netloc.lower()
    if not (host == "amazon.com" or host.endswith(".amazon.com")):
        return False
    return bool(re.search(r"/dp/[A-Za-z0-9]{10}", u.path))


def is_amazon_reference(href):
    """An Amazon-hosted policy or documentation page. Must NOT be tagged."""
    u = urlparse(href)
    host = u.netloc.lower()
    if not (host == "amazon.com" or host.endswith(".amazon.com")):
        return False
    return not is_product_link(href)


def resolve(page, ref):
    base = page.parent
    if ref.startswith("/"):
        return ("absolute", ref)
    target = (base / ref.split("#")[0].split("?")[0]).resolve()
    return ("local", target)


def main():
    pages = sorted(SHOP.rglob("*.html"))
    if not pages:
        fail("C0", "no pages built")
        report()
        return

    linked_targets = set()

    for page in pages:
        rel = str(page.relative_to(SHOP))
        raw = page.read_text(encoding="utf-8")
        s = Scan()
        s.feed(raw)

        # C15 - a draft must be noindex
        if 'content="noindex' not in raw:
            fail("C15", f"{rel}: archived edition page is not marked noindex")

        # C8
        if not s.has_canonical:
            fail("C8", f"{rel}: no canonical link")
        if not s.title or not s.title.strip():
            fail("C8", f"{rel}: no <title>")

        # C1
        if DISCLOSURE not in raw:
            fail("C1", f"{rel}: required disclosure sentence missing")

        # C11
        if "about/#disclosure" not in raw:
            fail("C11", f"{rel}: no link to the disclosure explanation")

        # C12
        if re.search(r'(?:href|src)="/[^/]', raw):
            fail("C12", f"{rel}: root-absolute path found")

        # C9
        for block in s.jsonld:
            try:
                json.loads(block)
            except Exception as exc:
                fail("C9", f"{rel}: JSON-LD does not parse ({exc})")

        # C2 / C3 / C4 / C5
        first_outbound = None
        for href, r, d, ser in s.links:
            if not href.startswith("http"):
                continue
            if is_product_link(href):
                if first_outbound is None:
                    first_outbound = ser
                if "sponsored" not in r:
                    fail("C3", f"{rel}: product link without rel=sponsored -> {href}")
                qs = parse_qs(urlparse(href).query)
                if TAG not in qs.get("tag", []):
                    fail("C4", f"{rel}: product link without tag={TAG} -> {href}")
                if "link.amazon" in urlparse(href).netloc:
                    fail("C5", f"{rel}: product link goes through a redirector -> {href}")
            elif is_amazon_reference(href):
                qs = parse_qs(urlparse(href).query)
                if "tag" in qs:
                    fail("C4", f"{rel}: policy/reference link must not carry an affiliate tag -> {href}")
            # no link on this site may point at the short-link redirector
            if "link.amazon" in urlparse(href).netloc:
                fail("C5", f"{rel}: link points at the unresolved short-link host -> {href}")

        if s.disclosure_pos is None:
            fail("C1", f"{rel}: disclosure text not found in body")
        elif first_outbound is not None and s.disclosure_pos > first_outbound:
            fail("C2", f"{rel}: disclosure appears after the first outbound product link")

        # C6 — a published price, rating or stock figure
        text = " ".join(s.text_parts)
        for pat, label in [
            (r"\$\s?\d", "a dollar amount"),
            (r"\bout of 5\b", "a star rating"),
            (r"\b\d[\d,]*\s+(?:ratings|reviews)\b", "a review count"),
            (r"\bin stock\b", "a stock status"),
            (r"\bbest ?seller\b", "a best-seller claim"),
        ]:
            for m in re.finditer(pat, text, re.I):
                ctx = text[max(0, m.start() - 70):m.end() + 70].replace("\n", " ")
                fail("C6", f"{rel}: found {label} -> …{ctx}…")

        # C7
        for kind, ref in s.refs:
            if not ref or ref.startswith(("http", "#", "mailto:", "data:", "javascript:")):
                continue
            mode, target = resolve(page, ref)
            if mode == "absolute":
                fail("C12", f"{rel}: root-absolute reference {ref}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                fail("C7", f"{rel}: broken {kind} -> {ref}")
            else:
                linked_targets.add(target.resolve())

    # C13 — each product page carries the tag on its own ASIN
    for prod_page in (SHOP / "products").glob("*/index.html"):
        raw = prod_page.read_text()
        slug = prod_page.parent.name
        rel = f"products/{slug}/"
        m = re.search(r'data-product="(PJ-\d\d)"', raw)
        if not m:
            fail("C13", f"{rel}: no product data attribute found")
            continue
        tagged = re.findall(r'href="(https://www\.amazon\.com/dp/[A-Z0-9]{10}\?tag=' + TAG + r')"', raw)
        if not tagged:
            fail("C13", f"{rel}: no tagged direct buy URL")

    # C10
    sm = SHOP / "sitemap.xml"
    if not sm.exists():
        fail("C10", "sitemap.xml missing")
    else:
        try:
            tree = ET.parse(sm)
            ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            locs = [el.text for el in tree.getroot().findall("s:url/s:loc", ns)]
        except Exception as exc:
            fail("C10", f"sitemap.xml does not parse: {exc}")
            locs = []
        base = "https://karagemop466-tech.github.io/Affil1/archive/2026-11-20-pantry-journal/"
        for loc in locs:
            if not loc.startswith(base):
                fail("C10", f"sitemap URL outside the shop base: {loc}")
                continue
            rest = loc[len(base):]
            target = SHOP / rest
            if rest == "" or rest.endswith("/"):
                target = SHOP / rest / "index.html"
            if not target.exists():
                fail("C10", f"sitemap URL has no file: {loc}")
        for loc in locs:
            if "the-dial-is-not-the-temperature" in loc or "multi-function-appliance-questions" in loc:
                fail("C10", f"draft guide must not be in the sitemap: {loc}")

    fd = SHOP / "feed.xml"
    if not fd.exists():
        fail("C10", "feed.xml missing")
    else:
        try:
            tree = ET.parse(fd)
            items = tree.getroot().findall("./channel/item")
            if len(items) < 3:
                fail("C10", f"feed.xml has only {len(items)} items")
            for it in items:
                link = it.find("link").text
                if link.startswith(base):
                    rest = link[len(base):]
                    tgt = SHOP / rest / "index.html" if rest.endswith("/") else SHOP / rest
                    if not tgt.exists():
                        fail("C10", f"feed item points at a missing page: {link}")
        except Exception as exc:
            fail("C10", f"feed.xml does not parse: {exc}")

    # C14 — orphans
    for page in pages:
        if page.name == "404.html":
            continue
        if page.resolve() not in linked_targets and page != SHOP / "index.html":
            pass
        if page.resolve() not in linked_targets and page != SHOP / "index.html":
            fail("C14", f"orphaned page, linked from nowhere: {page.relative_to(SHOP)}")

    report()


def report():
    print(f"shop_check: {len(errors)} error(s)")
    for e in errors:
        print("  ERROR", e)
    for n in notes:
        print("  note ", n)
    if errors:
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()
