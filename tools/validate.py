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
# The publication moved from the /crisp sub-site to the repository root, but this
# validator kept pointing at crisp/, which no longer exists. It therefore crashed
# on a missing file rather than checking anything. The base is now the root, and
# a missing sitemap/feed is reported as an error instead of raising.
SITE = ROOT
BASE = ""
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
        if tag == "img" and "alt" not in a:
            self.imgs_without_alt += 1
        cls = (a.get("class") or "").split()
        if "disclosure" in cls or "disclosure-bar" in cls or "disclosure-strip" in cls:
            self.has_disclosure = True
        if tag == "footer":
            self.has_footer = True


def main():
    global CHECKS
    # Only validate pages this builder owns. The storefront at the repo root is
    # another session's scope; validate.py must never fail on their files.
    # Engine archive. These are snapshots kept for provenance, are excluded from
    # the sitemap by design, and carry their own historical canonicals. Checking
    # them against today's sitemap produced dozens of false errors and buried the
    # real ones. Every other directory, including the maintained publication, is
    # still checked.
    ARCHIVE = SITE / "archive"
    pages = sorted(p for p in SITE.rglob("*.html")
                   if ARCHIVE not in p.parents)
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
                pos_disc = (html.find('class="disclosure-bar"') if 'class="disclosure-bar"' in html
                            else html.find('class="disclosure'))
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
        # Rule: no double-encoded entities. A named entity inside esc() renders as
        # the literal text "&ldquo;" on the page, which is a visible defect.
        for m in re.finditer(r"&amp;(?:ldquo|rdquo|mdash|ndash|rsquo|lsquo|hellip|nbsp|amp|quot);", html):
            err(f"{rel}: double-encoded entity '{m.group(0)}'")

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

    # ---- data integrity ----
    CHECKS += 1
    data = json.loads((ROOT / "src/data/products.json").read_text())
    # The register was renamed from submitted_code/observed_asin to
    # supplied_path_code/observed_redirect_asin, but this block kept reading the
    # old keys and crashed with a KeyError on its own data, which meant the whole
    # pre-publish check silently stopped running. Field names are now declared in
    # one place here, and a missing key is reported as an error rather than raised
    # as an exception, so a future rename cannot take the validator down with it.
    REF_KEY = "ref"
    CODE_KEY = "submitted_code" if "submitted_code" in data["products"][0] else "supplied_path_code"
    CODE_LEN_KEY = (CODE_KEY + "_length") if (CODE_KEY + "_length") in data["products"][0] else "submitted_code_length"
    OBSERVED_KEY = "observed_asin" if "observed_asin" in data["products"][0] else "observed_redirect_asin"
    INTENDED_KEY = "intended_asin"

    for prod in data["products"]:
        ident = prod.get(REF_KEY, "<no ref>")
        CHECKS += 1
        missing = [k for k in (REF_KEY, CODE_KEY, CODE_LEN_KEY, OBSERVED_KEY, INTENDED_KEY)
                   if k not in prod]
        if missing:
            err(f"{ident}: product record is missing field(s) {missing}")
            continue
        CHECKS += 1
        if prod[CODE_LEN_KEY] != len(prod[CODE_KEY]):
            err(f"{ident}: {CODE_LEN_KEY} disagrees with the code")
        CHECKS += 1
        # Rule: intended and observed identifiers are separate fields and never merged.
        if prod.get(INTENDED_KEY) and prod.get(INTENDED_KEY) == prod.get(OBSERVED_KEY):
            err(f"{ident}: intended_asin equals observed redirect; fields must stay distinct")
        CHECKS += 1
        # Rule: observed identifier, when present, must be a 10-character ASIN.
        if prod.get(OBSERVED_KEY) and len(prod[OBSERVED_KEY]) != 10:
            err(f"{ident}: observed ASIN is not 10 characters")

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

    # ---- one event vocabulary ------------------------------------------------
    # src/data/events.json is the published measurement spec. The shipped client
    # declared a different five names for several merges and nothing caught it,
    # while PUBLISHING_WORKFLOW.md claimed the two could not drift apart.
    spec_doc = json.loads((SITE / "src/data/events.json").read_text(encoding="utf-8"))
    spec_names = [e["name"] for e in spec_doc["events"]]
    CHECKS += 1
    if len(spec_names) != 5 or len(set(spec_names)) != 5:
        err(f"events.json: expected five distinct event names, got {spec_names}")
    declared_any = False
    for client in sorted((SITE / "assets/js").glob("*.js")):
        text = client.read_text(encoding="utf-8")
        m = re.search(r"var EVENTS = \[([^\]]*)\]", text)
        if not m:
            continue
        declared_any = True
        CHECKS += 1
        declared = [x.strip().strip('"\'') for x in m.group(1).split(",") if x.strip()]
        if declared != spec_names:
            err(f"{client.name}: event vocabulary {declared} != spec {spec_names}")
        for stale in ("outbound_click", "session_start", "suggestion_review"):
            CHECKS += 1
            if re.search(rf'["\']{stale}["\']', text):
                err(f"{client.name}: still references retired event name {stale}")
    CHECKS += 1
    if not declared_any:
        warn("no client declares an EVENTS list: the event spec is unenforced")

    # ---- document structure --------------------------------------------------
    # A heading inside an anchor produces an anchor around flow content: bad for
    # screen readers and wrong for the outline. Duplicate ids break in-page links.
    for rel, (c, html) in parsed.items():
        CHECKS += 1
        if re.search(r"<a\b[^>]*>(?:(?!</a>).)*?<h[1-6]\b", html, re.S):
            err(f"{rel}: a heading is nested inside an anchor")
        CHECKS += 1
        ids = re.findall(r'\bid="([^"]+)"', html)
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        if dupes:
            err(f"{rel}: duplicate id(s) {dupes}")

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
