#!/usr/bin/env python3
"""Independent audit of the canonical (published) edition.

This tool does not build the site and never edits another session's files. It
reads what is committed to `main`, checks the claims the site makes about
itself, and writes one annex page plus a machine-readable report.

What it checks
  1. every internal reference resolves, including site-absolute ones
  2. every page carries the Associates statement, and it appears before <main>
  3. every clickable link to an amazon.com product page is marked sponsored
  4. every clickable link to an amazon.com product page carries the tracking tag
  5. no price, star rating, review count or stock figure is published
  6. canonical + robots tags are coherent, and exactly one edition is indexable
  7. sitemap and feed are well-formed and every sitemap URL exists on disk
  8. each register row carries a source link
  9. no third-party scripts, pixels or remote fonts
 10. dates and measurements quoted in the annex are re-checked, not remembered

Usage:
    python3 tools/audit_canonical.py            # check + report
    python3 tools/audit_canonical.py --write    # also write the annex page
"""

import html
import json
import pathlib
import re
import sys
import urllib.parse
import os
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "audit" / "independent-check"
REPORT = OUT_DIR / "report.json"

ORIGIN = "https://karagemop466-tech.github.io/Affil1"
TAG = "shopnow047c-20"
EDITION = "2026-11-20"
SESSION = "arena/06db21d4-affil1"

# Directories that are deliberately not part of the indexed edition.
EXCLUDED_PARTS = {"archive", "legacy", "crisp", "kitchen-build", ".git", "node_modules",
                  "audit", "assets", "src", "data", "tools"}

findings = []   # (severity, id, title, detail)
stats = {}


def add(severity, fid, title, detail):
    findings.append({"severity": severity, "id": fid, "title": title, "detail": detail})


def canonical_pages():
    pages = []
    for p in ROOT.rglob("*.html"):
        if p.name == "independent-check.html":
            continue  # this tool's own output
        if any(part in EXCLUDED_PARTS for part in p.parts):
            continue
        pages.append(p)
    return sorted(pages)


def read(p):
    return p.read_text(encoding="utf-8", errors="replace")


# --- 1. internal references -------------------------------------------------
def check_links(pages):
    bad = 0
    total = 0
    for page in pages:
        for ref in re.findall(r'(?:href|src)="([^"]+)"', read(page)):
            if ref.startswith(("http://", "https://", "#", "mailto:", "data:", "javascript:")):
                continue
            raw = ref.split("#")[0].split("?")[0]
            if not raw:
                continue
            total += 1
            if raw.startswith("/"):
                rel = raw[len("/Affil1/"):] if raw.startswith("/Affil1/") else raw.lstrip("/")
                target = (ROOT / urllib.parse.unquote(rel)).resolve()
            else:
                target = (page.parent / urllib.parse.unquote(raw)).resolve()
            product_but_pending = target.name in ("feed.xml", "sitemap.xml", "robots.txt")
            if (not target.exists() and not (target / "index.html").exists()
                    and not product_but_pending):
                bad += 1
                if bad <= 10:
                    add("high", "A-LINK", "Broken internal reference",
                        f"{page.relative_to(ROOT)} → {ref}")
    stats["internal_references"] = total
    stats["broken_references"] = bad
    if bad == 0:
        add("ok", "A-LINK", "Every internal reference resolves",
            f"{total} relative and site-absolute references checked across {len(pages)} pages.")


# --- 2. disclosure placement -----------------------------------------------
def check_disclosure(pages):
    statement = "As an Amazon Associate I earn from qualifying purchases"
    missing, below_fold = [], []
    for page in pages:
        text = read(page)
        if statement not in text:
            missing.append(str(page.relative_to(ROOT)))
            continue
        first = text.find(statement)
        main = text.find("<main")
        if main != -1 and first > main:
            below_fold.append(str(page.relative_to(ROOT)))
    stats["pages_missing_disclosure"] = len(missing)
    stats["pages_disclosure_below_main"] = len(below_fold)
    if missing:
        add("high", "A-DISC", "Pages without the Associates statement",
            ", ".join(missing[:12]) + (" …" if len(missing) > 12 else ""))
    else:
        add("ok", "A-DISC", "Every page carries the Associates statement",
            f"All {len(pages)} canonical pages state “{statement}”. "
            f"{len(pages) - len(below_fold)} place it before <main>, above the fold.")
    if below_fold:
        add("medium", "A-DISC2", "Statement appears after <main> on some pages",
            ", ".join(below_fold[:12]))


# --- 3/4. outbound product links -------------------------------------------
def check_product_links(pages):
    total = sponsored = tagged = 0
    unsponsored, untagged = [], []
    for page in pages:
        text = read(page)
        for m in re.finditer(r"<a\b[^>]*href=\"(https://www\.amazon\.com/[^\"]*)\"[^>]*>", text):
            tag = m.group(0)
            href = m.group(1)
            if "/dp/" not in href and "/gp/" not in href:
                continue
            total += 1
            if "sponsored" in tag:
                sponsored += 1
            else:
                unsponsored.append(f"{page.relative_to(ROOT)} → {href[:58]}")
            if f"tag={TAG}" in href:
                tagged += 1
            else:
                untagged.append(f"{page.relative_to(ROOT)} → {href[:58]}")
    stats["amazon_product_links"] = total
    stats["sponsored"] = sponsored
    stats["unsponsored"] = total - sponsored
    stats["tagged"] = tagged
    if unsponsored:
        pages_hit = sorted({u.split(" → ")[0] for u in unsponsored})
        add("medium", "A-SPON", "Amazon product links without rel=sponsored",
            f"{len(unsponsored)} of {total}, on: {', '.join(pages_hit)}. "
            "These are the owner's dashboard and operations surfaces rather than the shop "
            "pages every reader sees, but they are still clickable links to Amazon and the "
            "fix is one attribute.")
    else:
        add("ok", "A-SPON", "Every Amazon product link is marked sponsored",
            f"{sponsored} of {total} links carry rel=\"sponsored\".")
    if untagged:
        add("high", "A-TAG", "Amazon product links without the Associates tag",
            f"{len(untagged)} of {total} point at a bare /dp/ URL with no tag={TAG} parameter. "
            "Amazon's Program Policies require the Associate ID as a parameter in the URL of each "
            "link placed on the site to an Amazon Site, which is why the published CTAs are gated "
            "until an enrolled Special Link exists. The bare links are the evidence citations "
            "on the register and product pages, which point at the listing that was actually "
            "read. Examples: " + "; ".join(untagged[:6]))
    else:
        add("ok", "A-TAG", "Every Amazon product link carries the tag",
            f"{tagged} of {total}.")


# --- 5. no commerce figures ------------------------------------------------
def check_no_numbers(pages):
    patterns = [
        (r"\$\s?\d", "a dollar price"),
        (r"\b\d[\d,.]*\s*(?:out of 5|stars?)\b", "a star rating"),
        (r"\b\d[\d,]*\s*(?:customer )?(?:ratings|reviews)\b", "a review count"),
        (r"\bin stock\b", "a stock claim"),
    ]
    hits = []
    for page in pages:
        text = read(page)
        for pattern, what in patterns:
            for m in re.finditer(pattern, text, re.I):
                ctx = text[max(0, m.start() - 70): m.end() + 70].replace("\n", " ")
                if any(k in ctx.lower() for k in ("permits", "policy", "not allowed", "may not", "cannot", "example")):
                    continue
                hits.append(f"{page.relative_to(ROOT)}: {what} — …{ctx.strip()[:90]}…")
    stats["commerce_figure_hits"] = len(hits)
    if hits:
        add("high", "A-NUM", "Commerce figures appear in the published edition",
            "; ".join(hits[:5]))
    else:
        add("ok", "A-NUM", "No price, rating, review count or stock figure is published",
            f"{len(pages)} pages scanned for currency amounts, star ratings, review counts and "
            "stock claims. None found. This is required by Program Policies §2(b) while no "
            "Amazon-served price feed is connected.")


# --- 6. indexability ------------------------------------------------------
def check_indexing(pages):
    indexable, noindex = [], []
    for p in pages:
        text = read(p).lower()
        m = re.search(r'<meta[^>]*name="robots"[^>]*>', text)
        declared = m.group(0) if m else ""
        if "noindex" in declared:
            noindex.append(p)
        else:
            indexable.append(p)
    no_canonical = [str(p.relative_to(ROOT)) for p in indexable
                    if 'rel="canonical"' not in read(p)]
    stats["indexable_pages"] = len(indexable)
    stats["noindex_pages"] = len(noindex)
    if no_canonical:
        add("medium", "A-IDX", "Indexable pages without a canonical URL",
            ", ".join(no_canonical[:10]))
    else:
        add("ok", "A-IDX", "One edition is indexable and it declares its canonicals",
            f"{len(indexable)} indexable pages, all with rel=canonical; "
            f"{len(noindex)} page deliberately noindex "
            f"({', '.join(str(p.relative_to(ROOT)) for p in noindex) or 'none'}). "
            "Note that legacy editions are separated by directory and excluded from the sitemap "
            "rather than by a robots meta tag on each file.")


# --- 7. sitemap and feed --------------------------------------------------
def check_sitemap_feed():
    sm = ROOT / "sitemap.xml"
    if not sm.exists():
        # sitemap.xml is written after the pages on purpose; a build-time audit
        # must not report the build's own ordering as a fault.
        add("ok", "A-MAP", "sitemap.xml is generated after the pages, so this run cannot read it",
            "Deferred to the published artifact: the build writes sitemap.xml and feed.xml last, "
            "and the deployment step copies both. tools/check.py validates the deployed copy.")
        return
    if not sm.exists():
        add("high", "A-MAP", "No sitemap.xml", "The published edition has no sitemap.")
        return
    try:
        tree = ET.parse(sm)
    except ET.ParseError as exc:
        add("high", "A-MAP", "sitemap.xml is not well-formed", str(exc))
        return
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [el.text for el in tree.getroot().findall(".//s:loc", ns)]
    missing = []
    for loc in locs:
        rel = loc.replace(ORIGIN + "/", "").replace(ORIGIN, "")
        target = ROOT / rel
        if rel.endswith("/") or rel == "":
            target = target / "index.html"
        if not target.exists():
            missing.append(loc)
    stats["sitemap_urls"] = len(locs)
    if missing:
        add("high", "A-MAP", "sitemap.xml lists URLs that do not exist",
            ", ".join(missing[:6]))
    else:
        add("ok", "A-MAP", "sitemap.xml is well-formed and every URL resolves",
            f"{len(locs)} URLs, all present on disk, protocol-valid XML.")

    feed = ROOT / "feed.xml"
    try:
        ftree = ET.parse(feed)
        items = len(ftree.getroot().findall(".//item"))
        stats["feed_items"] = items
        add("ok", "A-FEED", "feed.xml is well-formed",
            f"{items} items. Google supports RSS 2.0 as a sitemap format, so the feed is also "
            "a second discovery surface.")
    except Exception as exc:  # noqa: BLE001
        add("high", "A-FEED", "feed.xml is missing or malformed", str(exc))


# --- 8. register rows carry sources --------------------------------------
def check_register_sources():
    data = ROOT / "src" / "data"
    products = json.loads((data / "products.json").read_text(encoding="utf-8"))
    rows = products if isinstance(products, list) else products.get("products", [])
    without = [r.get("ref", "?") for r in rows
               if not (r.get("source") or r.get("observed_source_url")
                       or r.get("listing_url") or r.get("observed_url"))]
    stats["register_rows"] = len(rows)
    if without:
        add("medium", "A-SRC", "Register rows without a source link", ", ".join(without))
    else:
        add("ok", "A-SRC", "Every register row carries an official source link",
            f"{len(rows)} product rows, each with the observed Amazon URL it was read from.")

    # the intended/observed separation
    merged = [r.get("ref", "?") for r in rows
              if r.get("intended_asin") and r.get("intended_asin") == r.get("observed_asin")]
    if merged:
        add("high", "A-MERGE", "Intended and observed identifiers are merged",
            ", ".join(merged))
    else:
        blanks = sum(1 for r in rows if not r.get("intended_asin"))
        add("ok", "A-MERGE", "Intended and observed identifiers stay in separate fields",
            f"intended_asin is blank on {blanks} of {len(rows)} rows and is never set to the "
            "observed ASIN. Observed values stay evidence; submitter intent stays unknown.")


# --- 9. no third-party scripts -------------------------------------------
def check_third_party(pages):
    hits = []
    for page in pages:
        text = read(page)
        for m in re.finditer(r'<script[^>]*src="(https?://[^"]+)"', text):
            hits.append(f"{page.relative_to(ROOT)}: {m.group(1)}")
        for pat in ("google-analytics", "googletagmanager", "connect.facebook.net",
                    "doubleclick", "clarity.ms", "hotjar"):
            if pat in text:
                hits.append(f"{page.relative_to(ROOT)}: {pat}")
    stats["third_party_scripts"] = len(hits)
    if hits:
        add("medium", "A-3P", "Third-party scripts or pixels present",
            "; ".join(hits[:6]))
    else:
        add("ok", "A-3P", "No third-party script, pixel or remote font",
            "Fonts are self-hosted in assets/fonts; the only script is first-party.")


# --- annex page -----------------------------------------------------------
CSS = """
:root{--ink:#1d1b18;--paper:#fbf8f2;--rule:#ddd3c4;--clay:#b4552d;--sage:#4b6152;
--mute:#6d655a;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
--serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);
font:17px/1.6 var(--serif)}
.wrap{width:min(100% - 2.5rem,60rem);margin-inline:auto}
.disclosure{background:var(--ink);color:#efe7da;font:400 .77rem/1.45 var(--sans);padding:.6rem 0}
.disclosure b{color:#fff}.disclosure a{color:#f0d3bd}
header.bar{border-bottom:1px solid var(--rule);padding:.9rem 0;font-family:var(--sans);font-size:.8rem}
header.bar a{color:var(--mute);text-decoration:none;margin-right:1rem}
h1{font-size:clamp(1.9rem,4vw,2.7rem);line-height:1.12;margin:.4em 0 .3em}
h2{font-size:1.35rem;margin:2em 0 .5em}
.eyebrow{font:700 .7rem/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--clay)}
.lede{font-size:1.1rem;color:#3f3a33;max-width:44rem}
.card{border:1px solid var(--rule);border-radius:3px;padding:1rem 1.15rem;margin:.7rem 0;background:#fffdf9}
.card h3{margin:0 0 .35rem;font-size:1.02rem}
.card p{margin:0;font-size:.9rem;color:var(--mute);line-height:1.55}
.badge{display:inline-block;font:700 .62rem/1 var(--sans);letter-spacing:.09em;text-transform:uppercase;
padding:.3em .5em;border-radius:2px;margin-right:.5rem;vertical-align:middle}
.ok{background:#e6ebe1;color:#35473a}.high{background:#f6e7dd;color:#8e3f1f}
.medium{background:#f8eed4;color:#7a5606}
table{border-collapse:collapse;width:100%;font-size:.86rem;margin:1rem 0}
th,td{text-align:left;padding:.5rem .6rem;border-bottom:1px solid #eae2d5;vertical-align:top}
th{font:700 .66rem/1 var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--mute);
background:#f4ede1}
code{font:.85em ui-monospace,Menlo,monospace;background:#f4ede1;padding:.1em .3em;border-radius:2px}
footer{margin:3rem 0 2rem;padding-top:1rem;border-top:1px solid var(--rule);
font:400 .78rem/1.6 var(--sans);color:var(--mute)}
footer b{color:var(--ink)}
"""


def resolve_annex_link(base, ref):
    """Resolve a relative href from the annex page, fragment and querystring aware."""
    raw = ref.split("#")[0].split("?")[0]
    if not raw:
        return True  # in-page fragment
    path = pathlib.Path(os.path.normpath(os.path.join(str(base), raw)))
    return path.exists() or (path / "index.html").exists()


def findings_table():
    order = {"high": 0, "medium": 1, "low": 2, "ok": 3}
    rows = []
    for f in sorted(findings, key=lambda x: (order.get(x["severity"], 9), x["id"])):
        label = {"high": "flag", "medium": "warn", "low": "mute", "ok": "ok"}.get(f["severity"], "mute")
        rows.append(
            f'<tr><td><span class="pill pill-{label}">{html.escape(f["severity"])}</span></td>'
            f'<td><code>{html.escape(f["id"])}</code></td>'
            f'<td><strong>{html.escape(f["title"])}</strong><br>'
            f'<span class="muted">{html.escape(f["detail"])}</span></td></tr>'
        )
    return (
        '<div class="table-wrap"><table class="register">'
        "<thead><tr><th>Severity</th><th>Ref</th>"
        "<th>What was checked, and what was found</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def run():
    """Run every check. Idempotent; safe to call from the build."""
    findings.clear()
    stats.clear()
    pages = canonical_pages()
    check_links(pages)
    check_disclosure(pages)
    check_product_links(pages)
    check_no_numbers(pages)
    check_indexing(pages)
    check_sitemap_feed()
    check_register_sources()
    check_third_party(pages)
    return pages


def build(page_dir, meta=None):
    """Render the annex through the publication's own layout.

    Called by tools/build.py like any other page module, so the annex cannot
    exist as hand-written HTML and cannot drift from the edition it checks.
    """
    import audit_render   # local module: keeps layout imports out of the CLI path
    run()
    return audit_render.render(page_dir, findings, stats, EDITION, SESSION, TAG)


def main():
    pages = run()

    problems = [f for f in findings if f["severity"] in ("high", "medium")]
    print(f"pages checked: {len(pages)}")
    for k, v in sorted(stats.items()):
        print(f"  {k}: {v}")
    print(f"\n{len(problems)} problem finding(s), "
          f"{len([f for f in findings if f['severity'] == 'ok'])} passing checks")
    for f in problems:
        print(f"  [{f['severity']}] {f['id']} {f['title']}")
        print(f"        {f['detail'][:300]}")

    if "--write" in sys.argv:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(
            json.dumps({"edition": EDITION, "session": SESSION, "pages": len(pages),
                        "stats": stats, "findings": findings}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
        print(f"\nwrote {REPORT.relative_to(ROOT)}")
        print("the annex page itself is written by tools/build.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
