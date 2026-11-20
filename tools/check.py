#!/usr/bin/env python3
"""Static checks. Fails the build on anything that would make the site wrong.

The point is not style. Each rule below encodes a claim the site makes, so the
claim is enforced rather than remembered:

  * no price, rating, review count or stock phrase  -> the site's compliance claim
  * sponsored on every Amazon link                  -> the FTC/Google marking claim
  * disclosure above <main> on every page           -> the Operating Agreement claim
  * no root-absolute internal href                  -> the project-Pages claim
  * every internal link and anchor resolves         -> the no-broken-links claim
  * no external resource loading                    -> the no-third-party claim
"""

import json
import pathlib
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent

# One canonical site. The superseded edition is preserved under archive/ with a
# noindex tag on every page, and is deliberately out of scope: it is a record,
# not a destination. Any OTHER .html file anywhere in the tree is a stray page
# that would compete with the canonical one, and it fails the build.
ARCHIVE = ROOT / "archive"

def owned(page):
    """True only for a file this build generates.

    Directory-based filtering was not enough: it still swept in other sessions'
    pages that live in guides/. The build's GENERATED set is the only honest
    definition of 'ours', and it is imported rather than duplicated."""
    from build import GENERATED
    return page.relative_to(ROOT).as_posix() in GENERATED

PAGES = sorted(p for p in ROOT.rglob("*.html") if owned(p))

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []          # (attr, value, line)
        self.anchors = []       # dicts of attrs
        self.ids = set()
        self.images = []
        self.inline_handlers = []
        self.scripts = []
        self.disclosure_index = None
        self.main_index = None
        self.h1 = 0
        self.order = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.order += 1
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a":
            self.anchors.append(a)
            if any(k.startswith("on") for k in a):
                self.inline_handlers.append(a)
        if tag in ("a", "link") and a.get("href"):
            self.refs.append(("href", a["href"], self.getpos()[0]))
        if tag == "script" and a.get("src"):
            self.refs.append(("src", a["src"], self.getpos()[0]))
            self.scripts.append(a["src"])
        if tag == "img":
            self.images.append(a)
            if a.get("src"):
                self.refs.append(("src", a["src"], self.getpos()[0]))
        if tag == "h1":
            self.h1 += 1
        if tag == "main" and self.main_index is None:
            self.main_index = self.order
        if tag == "div" and "disclosure-bar" in (a.get("class") or ""):
            if self.disclosure_index is None:
                self.disclosure_index = self.order

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


BANNED = [
    (re.compile(r"\$\s?\d[\d,.]*"), "currency figure"),
    (re.compile(r"£\s?\d|€\s?\d"), "currency figure"),
    (re.compile(r"\b\d+(\.\d+)?\s?(out of 5|/5)\b", re.I), "star rating"),
    (re.compile(r"\b[1-5](\.\d)?\s?stars?\b", re.I), "star rating"),
    (re.compile(r"\b\d[\d,]*\s+(customer\s+)?reviews?\b", re.I), "review count"),
    (re.compile(r"\bin stock\b|\bout of stock\b|\bonly \d+ left\b", re.I), "stock status"),
    (re.compile(r"\bbest[- ]?seller\b", re.I), "best-seller claim"),
    (re.compile(r"\b(we|I)\s+(tested|tried|used|bought)\b", re.I), "test claim"),
    (re.compile(r"\b(our|my)\s+(testing|hands-on)\b", re.I), "test claim"),
    (re.compile(r"#1\b|\bnumber one\b", re.I), "ranking claim"),
]

# Only retail destinations are affiliate links. A citation to Amazon's own
# policy pages is a source, not a Special Link, and marking it "sponsored"
# would misdescribe it. This distinction is enforced rather than described.
AFFILIATE = re.compile(
    r"^https?://(?:(?:[a-z0-9-]+\.)*amazon\.[a-z.]+/(?:dp|gp/product)/|link\.amazon/)", re.I)
AMAZON_ANY = re.compile(r"(^//|https?://)([a-z0-9.-]*amazon\.[a-z.]+|amzn\.to|link\.amazon)", re.I)
EXTERNAL_RESOURCE = re.compile(r"^(https?:)?//", re.I)

# Third-party hosts allowed to appear as *citations* (anchors), never as resources.
CITATION_OK = re.compile(
    r"https?://(www\.)?(amazon\.com|affiliate-program\.amazon\.com|consumer\.ftc\.gov|"
    r"ecfr\.gov|www\.ecfr\.gov|developers\.google\.com|docs\.github\.com|www\.fsis\.usda\.gov|"
    r"sellercentral\.amazon\.com|karagemop466-tech\.github\.io|link\.amazon|github\.com|"
    r"www\.ftc\.gov)",
    re.I,
)


def check_page(path):
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    page_dir = path.parent

    s = Scan()
    try:
        s.feed(text)
        s.close()
    except Exception as e:  # malformed HTML
        err(f"{rel}: could not parse HTML ({e})")
        return

    # --- disclosure must exist, and must come before <main> ---
    if s.disclosure_index is None:
        err(f"{rel}: no disclosure strip")
    elif s.main_index is not None and s.disclosure_index > s.main_index:
        err(f"{rel}: disclosure strip appears after <main>")
    if "As an Amazon Associate I earn from qualifying purchases." not in text:
        err(f"{rel}: required Associates sentence missing")
    if text.count("As an Amazon Associate I earn from qualifying purchases.") < 2:
        warn(f"{rel}: Associates sentence appears only once (strip + footer expected)")

    # --- one h1 ---
    if s.h1 != 1:
        err(f"{rel}: expected exactly one <h1>, found {s.h1}")

    # --- links resolve ---
    for attr, value, line in s.refs:
        if not value or value.startswith(("#", "mailto:", "data:", "javascript:")):
            continue
        if attr == "src" and EXTERNAL_RESOURCE.match(value):
            err(f"{rel}:{line}: external resource load {value!r}")
            continue
        if attr == "href" and EXTERNAL_RESOURCE.match(value):
            if not CITATION_OK.match(value):
                err(f"{rel}:{line}: uncited external link {value!r}")
            continue
        if value.startswith("/"):
            err(f"{rel}:{line}: root-absolute link {value!r} breaks on a project Pages path")
            continue
        target_part, _, frag = value.partition("#")
        target = (page_dir / target_part).resolve() if target_part else path
        if target_part and not target.exists():
            err(f"{rel}:{line}: broken local link {value!r}")
            continue
        if frag and target.suffix == ".html" and target.exists():
            ids = Scan()
            ids.feed(target.read_text(encoding="utf-8"))
            if frag not in ids.ids:
                err(f"{rel}:{line}: missing anchor #{frag} in {target.name}")

    # --- Amazon links must be sponsored AND carry the Associates tag ---
    from layout import TRACKING_ID
    for a in s.anchors:
        href = a.get("href") or ""
        rels = (a.get("rel") or "").split()
        if AFFILIATE.match(href):
            if f"tag={TRACKING_ID}" not in href:
                err(f"{rel}: product link without the Associates tag: {href}")
            if "sponsored" not in rels:
                err(f"{rel}: affiliate link not marked sponsored: {href}")
            if "nofollow" not in rels:
                err(f"{rel}: affiliate link missing nofollow: {href}")
            if "noopener" not in rels:
                err(f"{rel}: affiliate link missing noopener: {href}")
            if a.get("target") != "_blank":
                warn(f"{rel}: affiliate link without target=_blank: {href}")
        elif AMAZON_ANY.search(href):
            # A citation to Amazon's own policy or help page. It must NOT be
            # marked sponsored, because it is not a paid link.
            if "sponsored" in rels:
                err(f"{rel}: policy citation wrongly marked sponsored: {href}")
            if "noopener" not in rels:
                warn(f"{rel}: citation without rel=noopener: {href}")

    # --- images need alt ---
    for im in s.images:
        if "alt" not in im:
            err(f"{rel}: image without alt attribute: {im.get('src')}")
        elif len(im["alt"].strip()) < 12:
            warn(f"{rel}: thin alt text on {im.get('src')}")

    # --- banned claims in visible text ---
    visible = re.sub(r"<script.*?</script>", " ", text, flags=re.S)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"\s+", " ", visible)
    for pattern, label in BANNED:
        for m in pattern.finditer(visible):
            snippet = visible[max(0, m.start() - 55):m.end() + 55].strip()
            err(f"{rel}: {label} in text: ...{snippet}...")

    # --- no inline event handlers ---
    if re.search(r"\son(click|load|error|mouseover)\s*=", text, re.I):
        err(f"{rel}: inline event handler present")

    # --- every table cell must be a real cell, not one character per row ---
    for m in re.finditer(r"<tbody>(.*?)</tbody>", text, re.S):
        body = m.group(1)
        tds = len(re.findall(r"<td[ >]", body))
        trs = len(re.findall(r"<tr[ >]", body))
        if trs and tds > trs * 12:
            err(f"{rel}: table body has {tds} cells across {trs} rows - likely shredded markup")
        char_cells = len(re.findall(r"<td>.{1}</td>", body))
        if char_cells > 6:
            err(f"{rel}: {char_cells} single-character cells - table cells were iterated as strings")

    # --- head essentials ---
    for needle in ("<title>", 'name="description"', 'rel="canonical"'):
        if needle not in text:
            err(f"{rel}: missing {needle}")
    if 'lang="en"' not in text:
        err(f"{rel}: missing lang attribute")


def check_sitemap_feed():
    pages = sorted(
        p.relative_to(ROOT).as_posix() for p in PAGES
        if p.name != "404.html"
    )
    # A sitemap lists directories, not "index.html" file names.
    def as_url(rel_path):
        return rel_path[:-len("index.html")] if rel_path.endswith("index.html") else rel_path
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>(.*?)</loc>", sm)
    base = "https://karagemop466-tech.github.io/Affil1/"
    listed = {l.replace(base, "") for l in locs}
    urls = {as_url(p) for p in pages}
    # Only this build's own generated set. Other editions' pages live at their
    # own URLs and are not this sitemap's business.
    from build import GENERATED  # the build's own list, not a second copy
    generated = set()
    for g in GENERATED:
        if g == "404.html" or g in ("sitemap.xml", "feed.xml", "robots.txt"):
            continue
        generated.add(g[:-len("index.html")] if g.endswith("index.html") else g)
    for u in sorted(generated):
        if u not in listed:
            err(f"sitemap.xml: missing {u or '(root)'}")
    for l in listed:
        target = ROOT / (l or "index.html")
        if l.endswith("/"):
            target = ROOT / l / "index.html"
        if not target.exists():
            err(f"sitemap.xml: lists {l!r} but no such page exists")

    feed = (ROOT / "feed.xml").read_text(encoding="utf-8")
    for link in re.findall(r"<(?:link|guid[^>]*)>(.*?)</(?:link|guid)>", feed):
        item = link.replace(base, "").strip()
        if item and not item.startswith("http") and not (ROOT / item).exists():
            err(f"feed.xml: item link {item} does not exist")
    if "<rss" not in feed:
        err("feed.xml: not an RSS document")


def check_data():
    d = json.loads((ROOT / "src/data/products.json").read_text(encoding="utf-8"))
    refs = [p["ref"] for p in d["products"]]
    if len(refs) != len(set(refs)):
        err("products.json: duplicate refs")
    for p in d["products"]:
        if p["intended_asin"] is not None and len(p["intended_asin"]) != 10:
            err(f"products.json: {p['ref']} intended_asin is not 10 characters")
        if p["observed_asin"] is not None and len(p["observed_asin"]) != 10:
            err(f"products.json: {p['ref']} observed_asin is not 10 characters")
        if p["submitted_code"] != p["submitted_link"].rsplit("/", 1)[-1]:
            err(f"products.json: {p['ref']} submitted_code does not match the link")
        if p["intended_asin"] == p["observed_asin"] and p["intended_asin"] is not None:
            err(f"products.json: {p['ref']} intended and observed have been merged")

    for name in ("sources.json", "questions.json", "suggestions.json", "flags.json", "images.json"):
        json.loads((ROOT / "src/data" / name).read_text(encoding="utf-8"))

    flags = json.loads((ROOT / "src/data/flags.json").read_text(encoding="utf-8"))
    ids = [f["id"] for f in flags["flags"]]
    if len(ids) != len(set(ids)):
        err("flags.json: duplicate flag ids")

    qs = json.loads((ROOT / "src/data/questions.json").read_text(encoding="utf-8"))
    for q in qs["questions"]:
        if q.get("answered") and not q.get("answer"):
            err(f"questions.json: {q['id']} marked answered with no answer")
        if q.get("answered") and not q.get("evidence"):
            warn(f"questions.json: {q['id']} answered without a source reference")


def check_assets():
    for f in (ROOT / "assets/img").glob("*"):
        if f.suffix.lower() in (".jpg", ".png") and f.stat().st_size > 400_000:
            warn(f"assets/img/{f.name}: {f.stat().st_size // 1024} KB is heavy")
    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    if re.search(r"@import|https?://", css):
        err("site.css: imports or absolute URLs present")
    if "fonts.googleapis" in css:
        err("site.css: still references Google Fonts")
    for css_url in re.findall(r"url\(([^)]+)\)", css):
        target = (ROOT / "assets/css" / css_url.strip("'\"")).resolve()
        if not target.exists():
            err(f"site.css: missing font file {css_url}")

    js = (ROOT / "assets/js/analytics.js").read_text(encoding="utf-8")
    for ev in ("page_view", "outbound_click", "guide_open", "search_query_referral", "report_import"):
        if ev not in js:
            err(f"analytics.js: event {ev} is not defined")
    if "document.cookie" in js:
        err("analytics.js: sets a cookie")


def check_no_stray_pages():
    """Every served .html file is either generated by this build or archived."""
    from build import GENERATED
    for p in ROOT.rglob("*.html"):
        if p.is_relative_to(ARCHIVE):
            continue
        rel_path = p.relative_to(ROOT).as_posix()
        if rel_path not in GENERATED:
            err(f"{rel_path}: not generated by this build and not archived - one site only")


def main():
    for p in sorted(PAGES):
        check_page(p)
    check_sitemap_feed()
    check_no_stray_pages()
    check_data()
    check_assets()

    print(f"pages checked: {len(PAGES)} (this build's output only)")
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  FAIL  {e}")
    print(f"\n{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
