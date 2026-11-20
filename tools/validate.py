#!/usr/bin/env python3
"""Pre-publish checks.

Fails loudly rather than quietly. Each check encodes a rule this project
committed to, so a regression breaks the build instead of shipping.
"""

import json
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT                   # the publication now publishes at the repository root
BASE = ""
SKIP_DIRS = {"archive", ".git", ".github", "node_modules"}
ERRORS = []
WARNINGS = []
CHECKS = 0


def is_product_link(href):
    """A link a reader could buy through: a listing, or the supplied short host.

    Policy documents and developer documentation on amazon.com are citations.
    Marking those rel=sponsored would misdescribe them, so they are excluded.
    """
    if "link.amazon/" in href:
        return True
    return bool(re.search(r"amazon\.com/(dp|gp/product)/", href))


def page_dir_of(rel):
    return (SITE / rel.lstrip('/')).parent


def err(msg):
    ERRORS.append(msg)


def warn(msg):
    WARNINGS.append(msg)


class RefCollector(HTMLParser):
    """Collect ids, links, and a few structural facts from one page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.canonical = None
        self.has_disclosure = False
        self.has_footer = False
        self.h1_count = 0
        self.imgs_without_alt = 0
        self.outbound = []
        self.imgs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
            rel = a.get("rel", "")
            href = a["href"]
            if href.startswith("http") and is_product_link(href):
                self.outbound.append((href, rel, a.get("class", "")))
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "h1":
            self.h1_count += 1
        if tag == "img":
            if "alt" not in a:
                self.imgs_without_alt += 1
            if a.get("src"):
                self.imgs.append(a["src"])
            # A srcset is a second set of URLs, and one that a link check misses.
            # Root-absolute entries here survive the filesystem check and 404 in
            # production, which is exactly the bug this gate exists to catch.
            for entry in (a.get("srcset") or "").split(","):
                url = entry.strip().split(" ")[0]
                if url:
                    self.imgs.append(url)
        if tag == "div" and a.get("class") == "disclosure":
            self.has_disclosure = True
        if tag == "footer":
            self.has_footer = True


def main():
    global CHECKS
    # Only validate pages this builder owns. The storefront at the repo root is
    # another session's scope; validate.py must never fail on their files.
    pages = sorted(p for p in SITE.rglob("*.html")
                   if not (set(p.relative_to(SITE).parts) & SKIP_DIRS))
    parsed = {}

    for p in pages:
        rel = "/" + str(p.relative_to(SITE))
        html = p.read_text(encoding="utf-8")
        c = RefCollector()
        c.feed(html)
        parsed[rel] = (c, html)

        is_shim = 'http-equiv="refresh"' in html
        is_404 = rel.endswith("/404.html")
        CHECKS += 1
        # Rule: exactly one H1 per page.
        if not is_shim and not is_404 and c.h1_count != 1:
            err(f"{rel}: expected 1 <h1>, found {c.h1_count}")

        CHECKS += 1
        # Rule: disclosure above the fold on every page. Shims are exempt (meta refresh only).
        if not is_shim and not is_404:
            if not c.has_disclosure:
                err(f"{rel}: missing the disclosure strip")
            else:
                pos_disc = html.find('class="disclosure"')
                pos_main = html.find("<main")
                if pos_main != -1 and pos_disc > pos_main:
                    err(f"{rel}: disclosure strip appears after <main>")

        CHECKS += 1
        # Rule: canonical present on real pages.
        if not is_shim and not is_404 and not c.canonical:
            err(f"{rel}: missing canonical")

        CHECKS += 1
        # Rule: every link a reader could buy through is marked sponsored.
        # A buy button must say sponsored. A citation in a register must not,
        # because it is evidence, not a recommendation - but it must be nofollowed.
        for href, rel_attr, cls in c.outbound:
            if "btn" in (cls or ""):
                if "sponsored" not in rel_attr:
                    err(f"{rel}: buy button without rel=sponsored -> {href[:70]}")
            else:
                if "nofollow" not in rel_attr:
                    warn(f"{rel}: citation link not nofollowed -> {href[:70]}")

        CHECKS += 1
        if c.imgs_without_alt:
            err(f"{rel}: {c.imgs_without_alt} <img> without alt")

        CHECKS += 1
        # Rule: every <img> must resolve on disk. A missing image is a broken
        # page as surely as a missing link, and it is invisible to a link check.
        for src in c.imgs:
            if src.startswith(("http://", "https://", "data:", "#")):
                continue
            target = (page_dir_of(rel) / src.split("#")[0].lstrip("/")).resolve()
            if not target.exists():
                err(f"{rel}: broken image src -> {src}")

        CHECKS += 1
        # Rule: no price-like strings anywhere. Catches an accidental reintroduction.
        for m in re.finditer(r"\$\s?\d", html):
            warn(f"{rel}: dollar figure near '{html[max(0,m.start()-40):m.start()+20].strip()[:70]}'")

    # ---- internal link resolution (filesystem-exact) ----
    for rel, (c, html) in parsed.items():
        page_file = SITE / rel.lstrip("/")
        for href in c.links:
            CHECKS += 1
            if href.startswith(("http://", "https://", "mailto:", "#", "data:", "javascript:")):
                continue
            target = href.split("#")[0]
            frag = href.split("#")[1] if "#" in href else None
            if not target:
                if frag and frag not in c.ids:
                    err(f"{rel}: dead in-page anchor #{frag}")
                continue
            # A leading "./" or "../" resolves relative to the page's directory.
            tp = (page_file.parent / target).resolve()
            if not tp.is_relative_to(SITE.resolve()):
                # escaping the section is allowed only to reach the storefront root
                if tp != SITE.parent.resolve():
                    err(f"{rel}: link escapes the site root -> {href}")
                continue
            if target.endswith("/"):
                tp = tp / "index.html"
            if not tp.exists():
                err(f"{rel}: broken internal link -> {href}")
                continue
            if frag:
                key = "/" + str(tp.relative_to(SITE)) if tp.is_relative_to(SITE) else None
                if key in parsed and frag not in parsed[key][0].ids:
                    err(f"{rel}: link {href} -> missing anchor #{frag}")

    # ---- monetization gate ----
    # Two directions, because both failure modes are live risks:
    # an unregistered site publishing a tracking tag, and a registered site
    # publishing affiliate links without the paid-link note.
    CHECKS += 1
    try:
        import build as _build
        live, intent = _build.LINKS_LIVE, _build.INTENT
    except Exception as exc:  # noqa: BLE001
        err(f"could not import the build gate to check it: {exc}")
        live, intent = None, None
    if live is not None:
        tagged = []
        for rel, (c, html) in parsed.items():
            for href, rel_attr, cls in c.outbound:
                if "tag=" in href:
                    tagged.append((rel, href))
            if "tag=" in html and "shopnow047c-20" in html:
                tagged.append((rel, "raw text mention"))
        CHECKS += 1
        if not live and tagged:
            for rel, href in tagged[:5]:
                err(f"{rel}: a tracking tag is published while product-intent.json says enrolment is unconfirmed -> {href[:70]}")
        if live:
            for rel, (c, html) in parsed.items():
                for href, rel_attr, cls in c.outbound:
                    CHECKS += 1
                    if "tag=" in href and "sponsored" not in rel_attr:
                        err(f"{rel}: tagged affiliate link without rel=sponsored -> {href[:70]}")
        approved = sum(1 for r in intent["records"] if r.get("approved_special_link"))
        CHECKS += 1
        if not live and approved:
            warn(f"{approved} approved_special_link value(s) exist while the three gate fields are false; "
                 "an approved link is published as an affiliate link regardless of those flags")

    # ---- data integrity ----
    CHECKS += 1
    data = json.loads((ROOT / "src/data/products.json").read_text())
    for prod in data["products"]:
        CHECKS += 1
        if prod["supplied_path_code_length"] != len(prod["supplied_path_code"]):
            err(f"{prod['id']}: supplied_path_code_length disagrees with the code")
        CHECKS += 1
        # Rule: intended and observed identifiers are separate fields and never merged.
        if prod.get("intended_asin") == prod.get("observed_redirect_asin") and prod.get("intended_asin"):
            err(f"{prod['id']}: intended_asin equals observed redirect; fields must stay distinct")
        CHECKS += 1
        # Rule: observed ASIN, when present, must be 10 characters.
        if prod.get("observed_redirect_asin") and len(prod["observed_redirect_asin"]) != 10:
            err(f"{prod['id']}: observed ASIN is not 10 characters")

    # ---- sitemap / feed agreement ----
    sitemap = (SITE / "sitemap.xml").read_text()
    feed = (SITE / "feed.xml").read_text()
    for rel, (c, html) in parsed.items():
        if rel == "/404.html":
            continue
        if not c.canonical:
            continue
        CHECKS += 1
        url = c.canonical
        if url and f"<loc>{url}</loc>" not in sitemap:
            err(f"{rel}: canonical {url} absent from sitemap.xml")
        if url and not url.startswith("https://karagemop466-tech.github.io/Affil1/"):
            err(f"{rel}: canonical outside the published base -> {url}")

    for slug in re.findall(r"<link>(https://[^<]+/guides/[^<]+)</link>", feed):
        CHECKS += 1
        if f"<loc>{slug}</loc>" not in sitemap:
            err(f"feed item not in sitemap: {slug}")

    print(f"checks run: {CHECKS}")
    for w in WARNINGS:
        print(f"  WARN {w}")
    if ERRORS:
        print(f"\nFAILED with {len(ERRORS)} error(s):")
        for e in ERRORS:
            print(f"  ERR  {e}")
        sys.exit(1)
    print(f"all checks passed ({len(WARNINGS)} warning(s))")


if __name__ == "__main__":
    main()
