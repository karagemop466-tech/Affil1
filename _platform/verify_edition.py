#!/usr/bin/env python3
"""Line-by-line compliance, link, anchor, and table-row source verifier for edition/."""

from __future__ import annotations

import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlsplit

PLATFORM_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = PLATFORM_DIR.parent
EDITION_DIR = ROOT_DIR / "edition"

sys.path.insert(0, str(PLATFORM_DIR))
from compliance_gate import DOLLAR_PRICE_RE, EXACT_ASSOCIATES_DISCLOSURE, validate_data_layer  # noqa: E402

OFFICIAL_DOMAINS = (
    "affiliate-program.amazon.com",
    "sell.amazon.com",
    "consumer.ftc.gov",
    "www.ecfr.gov",
    "developers.google.com",
    "support.google.com",
    "docs.github.com",
    "www.fsis.usda.gov",
    "www.amazon.com",
)


def is_product_url(url: str) -> bool:
    return "link.amazon/" in url or bool(re.search(r"amazon\.com/(dp|gp/product)/", url))


class PageAuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.h1_count = 0
        self.canonical: str | None = None
        self.meta_robots: str | None = None
        self.annex_note = False
        self.rss_link: str | None = None
        self.has_disclosure_before_main = False
        self.seen_main = False
        self.in_disclosure = False
        self.in_footer = False
        self.disclosure_text: list[str] = []
        self.footer_text: list[str] = []
        self.links: list[tuple[str, str, int]] = []
        self.short_link_hrefs: list[tuple[str, int]] = []
        self.assets: list[tuple[str, int]] = []
        self.imgs_missing_alt = 0

        self.in_tbody = False
        self.in_tr = False
        self.tr_line = 0
        self.current_tr_external_urls: list[str] = []
        self.tbody_rows: list[tuple[int, list[str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        amap = {k: (v or "") for k, v in attrs}
        line = self.getpos()[0]
        if amap.get("id"):
            self.ids.add(amap["id"])
        if tag == "main":
            self.seen_main = True
        if tag == "div" and amap.get("class") == "disclosure":
            self.in_disclosure = True
            if not self.seen_main:
                self.has_disclosure_before_main = True
        if tag == "footer":
            self.in_footer = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta" and amap.get("name") == "robots":
            self.meta_robots = amap.get("content")
        if tag == "div" and amap.get("class") == "annex-note":
            self.annex_note = True
        if tag == "link":
            if amap.get("rel") == "canonical":
                self.canonical = amap.get("href")
            elif amap.get("rel") == "alternate" and amap.get("type") == "application/rss+xml":
                self.rss_link = amap.get("href")
            elif amap.get("rel") in ("stylesheet", "icon") and amap.get("href"):
                self.assets.append((amap["href"], line))
        if tag == "script" and amap.get("src"):
            self.assets.append((amap["src"], line))
        if tag == "img":
            if "alt" not in dict(attrs) or not amap.get("alt").strip():
                self.imgs_missing_alt += 1
            if amap.get("src"):
                self.assets.append((amap["src"], line))
        if tag == "tbody":
            self.in_tbody = True
        if tag == "tr" and self.in_tbody:
            self.in_tr = True
            self.tr_line = line
            self.current_tr_external_urls = []
        if tag == "a" and amap.get("href"):
            href = amap["href"]
            rel = amap.get("rel", "")
            self.links.append((href, rel, line))
            if SHORT_LINK.search(href) and "amazon.com" not in href:
                self.short_link_hrefs.append((href, line))
            if self.in_tr and href.startswith("https://"):
                self.current_tr_external_urls.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self.in_disclosure:
            self.in_disclosure = False
        if tag == "footer":
            self.in_footer = False
        if tag == "tr" and self.in_tr:
            self.tbody_rows.append((self.tr_line, list(self.current_tr_external_urls)))
            self.in_tr = False
        if tag == "tbody":
            self.in_tbody = False

    def handle_data(self, data: str) -> None:
        if self.in_disclosure:
            self.disclosure_text.append(data)
        if self.in_footer:
            self.footer_text.append(data)


SHORT_LINK = re.compile(r"link\.amazon/")
AMAZON_LISTING = re.compile(r"amazon\.[a-z.]+/(?:dp|gp/product)/([A-Za-z0-9]+)")


def permitted_amazon_destinations() -> set[str]:
    """The only Amazon destinations the annex may send a reader to.

    Mirrors ``permitted_amazon_urls`` in _tools/layout.py, which governs the root site:
    an account-issued Special Link when one exists, otherwise the plain listing of the
    ASIN the submitted link was observed to reach. The short links themselves are
    evidence, not destinations - the register records several of them resolving to the
    Amazon homepage or a checkpoint page, so a buy button wired to one is a buy button
    that can land anywhere.
    """
    out: set[str] = set()
    data = ROOT_DIR / "_platform" / "data" / "products.json"
    if not data.is_file():
        return out
    for prod in json.loads(data.read_text(encoding="utf-8")).get("products", []):
        obs = prod.get("observed_redirect") or {}
        for url in (
            (prod.get("intent_confirmation") or {}).get("validated_special_link_url"),
            (prod.get("intent_confirmation") or {}).get("approved_special_link"),
            obs.get("observed_redirect_url"),
        ):
            if url:
                out.add(url.split("?")[0])
        if obs.get("observed_asin"):
            out.add(obs["observed_asin"])
    return out


def verify_edition(edition_dir: pathlib.Path = EDITION_DIR) -> tuple[list[str], int]:
    errors: list[str] = []
    checks = 0

    data_errs = validate_data_layer()
    errors.extend(data_errs)
    checks += 1

    html_files = sorted(edition_dir.rglob("*.html"))
    if len(html_files) < 20:
        errors.append(f"Expected >= 20 HTML pages in edition/, found {len(html_files)}")

    parsed_pages: dict[pathlib.Path, PageAuditParser] = {}
    for page_path in html_files:
        raw = page_path.read_text(encoding="utf-8")
        rel_name = str(page_path.relative_to(edition_dir))
        if raw.startswith("---"):
            errors.append(f"{rel_name}: must not begin with Jekyll YAML frontmatter.")
        if DOLLAR_PRICE_RE.search(raw):
            errors.append(f"{rel_name}: contains prohibited dollar price figure.")

        parser = PageAuditParser()
        parser.feed(raw)
        parsed_pages[page_path] = parser
        checks += 6

        if parser.h1_count != 1:
            errors.append(f"{rel_name}: expected 1 <h1>, found {parser.h1_count}")
        if not parser.has_disclosure_before_main:
            errors.append(f"{rel_name}: missing <div class='disclosure'> before <main>")
        if EXACT_ASSOCIATES_DISCLOSURE not in "".join(parser.disclosure_text):
            errors.append(f"{rel_name}: top disclosure missing verbatim Associates §5 sentence")
        if EXACT_ASSOCIATES_DISCLOSURE not in "".join(parser.footer_text):
            errors.append(f"{rel_name}: footer missing verbatim Associates §5 sentence")
        if parser.imgs_missing_alt:
            errors.append(f"{rel_name}: {parser.imgs_missing_alt} <img> missing descriptive alt")
        if rel_name != "404.html" and not parser.canonical:
            errors.append(f"{rel_name}: missing canonical link")
        if not parser.rss_link:
            errors.append(f"{rel_name}: missing RSS autodiscovery link")

        # One host, one site to index. This edition and the generated shop at the
        # repository root publish the same five listings, so every page of the
        # annex has to carry the two things that keep it from competing: a noindex
        # rule the crawler can read, and a visible pointer to the reader edition.
        # Checked here rather than trusted, because a template edit can drop it.
        checks += 2
        if "noindex" not in (parser.meta_robots or ""):
            errors.append(f"{rel_name}: missing <meta name=\"robots\" content=\"noindex, follow\"> "
                          f"— the annex would compete with the root publication for the index")
        if not parser.annex_note:
            errors.append(f"{rel_name}: missing the annex note that points readers to the shop")

        # Every <tbody><tr> row must carry at least one official https:// source link
        for row_line, ext_urls in parser.tbody_rows:
            checks += 1
            has_official = any(urlsplit(u).netloc in OFFICIAL_DOMAINS for u in ext_urls)
            if not has_official:
                errors.append(f"{rel_name}:{row_line}: table row lacks an official https:// source link")

        # Asset resolution
        for asset_ref, line in parser.assets:
            checks += 1
            if asset_ref.startswith(("http://", "https://", "data:")):
                continue
            if asset_ref.startswith("/"):
                errors.append(f"{rel_name}:{line}: root-absolute asset path forbidden -> {asset_ref}")
                continue
            resolved = (page_path.parent / asset_ref.split("#")[0]).resolve()
            if not resolved.is_file():
                errors.append(f"{rel_name}:{line}: missing asset -> {asset_ref}")

    # Link, anchor, and rel="sponsored" resolution across all pages
    for page_path, parser in parsed_pages.items():
        rel_name = str(page_path.relative_to(edition_dir))
        for href, rel_attr, line in parser.links:
            checks += 1
            rel_tokens = set(rel_attr.split())
            if href.startswith(("http://", "https://")):
                if is_product_url(href):
                    if "sponsored" not in rel_tokens:
                        errors.append(f"{rel_name}:{line}: product link missing rel='sponsored' -> {href}")
                else:
                    if "sponsored" in rel_tokens:
                        errors.append(f"{rel_name}:{line}: non-product citation wrongly marked sponsored -> {href}")
                continue
            if href.startswith(("mailto:", "tel:", "javascript:")):
                continue
            if href.startswith("/"):
                errors.append(f"{rel_name}:{line}: root-absolute link forbidden on GitHub Pages -> {href}")
                continue

            parts = urlsplit(href)
            if not parts.path:
                if parts.fragment and parts.fragment not in parser.ids:
                    errors.append(f"{rel_name}:{line}: missing in-page anchor #{parts.fragment}")
                continue

            target_path = (page_path.parent / parts.path).resolve()
            if target_path.is_dir():
                target_path = target_path / "index.html"
            if not target_path.is_file():
                errors.append(f"{rel_name}:{line}: broken relative link -> {href}")
                continue
            if parts.fragment and target_path in parsed_pages:
                if parts.fragment not in parsed_pages[target_path].ids:
                    errors.append(f"{rel_name}:{line}: missing target anchor {href}")

    # The annex must not advertise a second sitemap: a robots.txt only counts at the
    # host root (developers.google.com/crawling/docs/robots-txt/create-robots-txt), so
    # this line could only ever mislead a reader of the file into thinking the annex
    # has its own indexable sitemap.
    robots_txt = (edition_dir / "robots.txt").read_text(encoding="utf-8")
    checks += 1
    if "Sitemap:" in robots_txt:
        errors.append("edition/robots.txt: advertises a sitemap for a noindex annex")

    # --- buy-path integrity: the annex must not send readers to an unvalidated link
    permitted = permitted_amazon_destinations()
    for page_path, parser in parsed_pages.items():
        rel_name = str(page_path.relative_to(edition_dir))
        for href, line in parser.short_link_hrefs:
            checks += 1
            errors.append(f"{rel_name}:{line}: short link offered as a destination -> {href} "
                          f"- show it as <code> evidence and link the observed /dp/ listing")
        for href, rel_attr, line in parser.links:
            m = AMAZON_LISTING.search(href)
            if not m:
                continue
            checks += 1
            if "sponsored" not in set(rel_attr.split()):
                continue  # covered by the rel check above
            key = href.split("?")[0]
            if key not in permitted and m.group(1) not in permitted:
                errors.append(f"{rel_name}:{line}: paid link destination is not in the register "
                              f"of approved Special Links or observed listings -> {href}")

    # XML Sitemap & RSS Feed validation
    sitemap_xml = (edition_dir / "sitemap.xml").read_text(encoding="utf-8")
    feed_xml = (edition_dir / "feed.xml").read_text(encoding="utf-8")
    ET.fromstring(sitemap_xml)
    ET.fromstring(feed_xml)
    checks += 2

    for page_path, parser in parsed_pages.items():
        rel_name = str(page_path.relative_to(edition_dir))
        if rel_name == "404.html":
            continue
        checks += 1
        if parser.canonical and f"<loc>{parser.canonical}</loc>" not in sitemap_xml:
            errors.append(f"{rel_name}: canonical {parser.canonical} missing from edition/sitemap.xml")

    return errors, checks


if __name__ == "__main__":
    errs, count = verify_edition()
    if errs:
        print(f"platform/verify_edition.py FAILED ({len(errs)} errors across {count} checks):")
        for err in errs:
            print(f"  ERR  {err}")
        raise SystemExit(1)
    print(f"platform/verify_edition.py: {count} line-by-line checks passed (0 errors)")
