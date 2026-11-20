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

# This build owns the site root. Other editions on main (crisp/ and the
# root-level *.html pages of a parallel session) are theirs, not this build's,
# and are deliberately out of scope. Claiming to verify them would be false.
OTHER_EDITIONS = {"crisp", "archive", "reviews", "docs", "server", "categories"}
FOREIGN_ROOT_PAGES = {
    "products.html", "questions.html", "suggestions.html", "guides.html",
    "dashboard.html", "disclosure.html", "executive-summary.html",
    "flagged-for-review.html", "privacy.html", "categories.html",
    "compare.html", "about.html", "legacy.html", "sources.html",
}

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
    r"https?://(www\.)?(amazon\.com|affiliate-program\.amazon\.com|sell\.amazon\.com|support\.google\.com|consumer\.ftc\.gov|"
    r"ecfr\.gov|www\.ecfr\.gov|developers\.google\.com|docs\.github\.com|www\.fsis\.usda\.gov|"
    r"sellercentral\.amazon\.com|sell\.amazon\.com|karagemop466-tech\.github\.io|link\.amazon|github\.com|"
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

    # --- every retail Amazon link must carry the Associates tag ---
    # Program Policies 2(b) requires the ID as a URL parameter. A /dp/ link
    # without it is not a Special Link, so it cannot be credited and Amazon
    # lists untagged links among its reasons for rejecting an application.
    for a in s.anchors:
        href = a.get("href") or ""
        if "link.amazon/" in href:
            err(f"{rel}: short link offered as a click target: {href}")
            continue
        if re.match(r"^https?://(?:[a-z0-9-]+\.)*amazon\.[a-z.]+/(?:dp|gp/product)/", href, re.I):
            if "tag=shopnow047c-20" not in href:
                err(f"{rel}: Amazon retail link without the Associates tag: {href}")

    # --- Amazon links must be sponsored, tagged, and any approval claim must hold ---
    # The kitchen-build preflight (a parallel session's tool) is the only thing
    # allowed to declare a link "approved". A link may not claim that approval
    # unless the intent record actually validates for it.
    sys.path.insert(0, str(ROOT / "kitchen-build"))
    try:
        import readiness
        intent = json.loads(readiness.INTENT.read_text())
    except Exception:
        readiness, intent = None, {"records": []}
    for a in s.anchors:
        href = a.get("href") or ""
        rels = (a.get("rel") or "").split()
        if AFFILIATE.match(href):
            paid = a.get("data-affiliate-ref")
            if paid:
                ok = readiness is not None and any(
                    p["ref"] == paid and p["approved_special_link"] == href
                    and readiness.eligible(p, intent["tracking_id_supplied"])
                    for p in intent["records"])
                if not ok:
                    err(f"{rel}: link claims an approval bundle that does not validate: {href}")
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
        if g in ("404.html", "operations/launch-readiness.html", "sitemap.xml", "feed.xml", "robots.txt"):
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

    for name in ("sources.json", "questions.json", "suggestions.json", "flags.json", "images.json",
                 "decisions.json", "verification.json"):
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


def check_legacy_and_index():
    """One site for search engines to index.

    The parallel edition is still served, so it must be noindexed rather than
    deleted; a page that becomes indexable by accident would put two copies of
    the same shop in front of a crawler.
    """
    from build import GENERATED
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(".git/") or rel in GENERATED:
            continue
        head = path.read_text(encoding="utf-8")[:2500]
        if 'content="noindex' not in head:
            err(f"{rel}: parallel-edition page is indexable (no noindex in <head>)")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap:" not in robots:
        err("robots.txt: no sitemap reference")
    if re.search(r"^Disallow:\s*/(\s*$|\s*\n)", robots, re.M):
        err("robots.txt: disallows the whole site")


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
    for spec in json.loads((ROOT / "src/data/events.json").read_text())["events"]:
        ev = spec["name"]
        if ev not in js:
            err(f"analytics.js: event {ev} is not defined")
    if "document.cookie" in js:
        err("analytics.js: sets a cookie")


def check_registers():
    """The decision register, the suggestion queue and the verification log.

    These three pages are the ones a reviewer acts on, so their internal
    consistency is a build rule rather than a matter of care: every suggestion
    points at a decision that exists, every path lists suggestions that exist,
    and every link in the verification log matches the product register.
    """
    d = json.loads((ROOT / "src/data/decisions.json").read_text(encoding="utf-8"))
    s = json.loads((ROOT / "src/data/suggestions.json").read_text(encoding="utf-8"))
    v = json.loads((ROOT / "src/data/verification.json").read_text(encoding="utf-8"))
    products = json.loads((ROOT / "src/data/products.json").read_text(encoding="utf-8"))["products"]
    by_ref = {p["ref"]: p for p in products}

    dec_ids = [x["id"] for x in d["decisions"]]
    if len(dec_ids) != len(set(dec_ids)):
        err("decisions.json: duplicate ids")
    for g in d["gates"]:
        for did in g["decisions"]:
            if did not in dec_ids:
                err(f"decisions.json: gate {g['id']} lists unknown {did}")
    for x in d["decisions"]:
        if x["answered"] and not x.get("evidence"):
            err(f"decisions.json: {x['id']} answered with no evidence")
        if not x["answered"] and not x.get("artefact"):
            err(f"decisions.json: {x['id']} open with no artefact that would close it")

    sug_ids = [x["id"] for x in s["suggestions"]]
    if len(sug_ids) != len(set(sug_ids)):
        err("suggestions.json: duplicate ids")
    path_ids = {p["id"] for p in s["paths"]}
    listed = [i for p in s["paths"] for i in p["items"]]
    for i in listed:
        if i not in sug_ids:
            err(f"suggestions.json: path lists unknown {i}")
    for x in s["suggestions"]:
        if x["path"] not in path_ids:
            err(f"suggestions.json: {x['id']} names unknown path {x['path']}")
        if x["id"] not in listed:
            err(f"suggestions.json: {x['id']} is in no path, so it can never be reviewed")
        for dep in re.findall(r"D-\d\d", x.get("depends_on", "")):
            if dep not in dec_ids:
                err(f"suggestions.json: {x['id']} depends on unknown decision {dep}")

    for r in v["links"]:
        p = by_ref.get(r["ref"])
        if not p:
            err(f"verification.json: unknown product {r['ref']}")
            continue
        if p.get("observed_asin") != r["asin"]:
            err(f"verification.json: {r['ref']} asin disagrees with products.json")
        if p.get("listing_url") and not p["listing_url"].endswith(r["asin"]):
            err(f"verification.json: {r['ref']} listing_url disagrees with the asin")
        if p.get("tagged_link") and "tag=shopnow047c-20" not in p["tagged_link"]:
            err(f"products.json: {r['ref']} tagged_link has no tag")
    if len(v["links"]) != len(products):
        err("verification.json: not every product has a link row")


def main():
    for p in sorted(PAGES):
        check_page(p)
    check_sitemap_feed()
    check_data()
    check_registers()
    check_legacy_and_index()
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
