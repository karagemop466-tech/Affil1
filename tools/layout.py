"""One place that decides what a page shell looks like.

The disclosure strip, the masthead, the navigation and the footer are generated
here and nowhere else. A page cannot be added without them because there is no
other way to produce a page.

Every internal link is relative and computed with posixpath.relpath, because
GitHub Pages serves this repository from /Affil1/ and a root-absolute href such
as "/about/" would 404.
"""

import html
import json
import pathlib
import posixpath
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE_NAME = "Crisp & Counter"
SITE_TAGLINE = "Kitchen buying guides"
SITE_URL = "https://karagemop466-tech.github.io/Affil1"
TRACKING_ID = "shopnow047c-20"
BUILD_DATE = "2026-11-20"

DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."

# A retail destination is an affiliate link; a policy page is a citation.
AFFILIATE_HINT = __import__("re").compile(
    r"^https?://(?:(?:[a-z0-9-]+\.)*amazon\.[a-z.]+/(?:dp|gp/product)/|link\.amazon/)", __import__("re").I)

# The only navigation group. Everything else lives in the footer.
NAV = [
    ("index.html", "The Edit"),
    ("products/index.html", "Product Shelf"),
    ("guides/index.html", "Buying Guides"),
    ("brief/index.html", "Site Desk"),
]

FOOTER_GROUPS = [
    ("Read", [
        ("guides/index.html", "All guides"),
        ("compare/index.html", "Comparison table"),
        ("feed.xml", "RSS feed"),
    ]),
    ("Catalogue", [
        ("products/index.html", "Product register"),
        ("products/p-05.html", "The thermometer"),
        ("about/index.html#how-we-link", "How we link"),
    ]),
    ("Review queue", [
        ("review/index.html", "Flagged for review"),
        ("review/images.html", "Image policy"),
        ("review/measurement.html", "Measurement plan"),
        ("operations/launch-readiness.html", "Affiliate launch readiness"),
        ("about/index.html#sources", "Sources"),
    ]),
    ("Desk", [
        ("questions/index.html", "Open questions"),
        ("suggestions/index.html", "Suggestions"),
        ("operations/ledger.html", "Campaign ledger"),
        ("brief/index.html", "Executive summary"),
        ("about/index.html", "About this site"),
    ]),
]


def esc(value):
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def rel(page_dir, target):
    """Relative URL from a page's directory to a target path at the repo root."""
    return posixpath.relpath(target, page_dir) if page_dir else target


def link(page_dir, target, label, *, cls=None, external=False, sponsored=False,
         aria=None, title=None, affiliate_ref=None):
    # An absolute URL is never passed through rel(): doing so would rewrite
    # "https://host/x" into "../https:/host/x" and produce a 404.
    absolute = target.startswith(("http://", "https://", "mailto:", "#"))
    href = target if (external or absolute) else rel(page_dir, target)
    attrs = [f'href="{esc(href)}"']
    if cls:
        attrs.append(f'class="{esc(cls)}"')
    if title:
        attrs.append(f'title="{esc(title)}"')
    if aria:
        attrs.append(f'aria-label="{esc(aria)}"')
    if affiliate_ref:
        attrs.append(f'data-affiliate-ref="{esc(affiliate_ref)}"')
    if sponsored:
        attrs.append('rel="sponsored nofollow noopener"')
        attrs.append('target="_blank"')
    elif external:
        attrs.append('rel="noopener"')
        attrs.append('target="_blank"')
    return f'<a {" ".join(attrs)}>{label}</a>'


def outbound(page_dir, url, label, **kw):
    """An official-source link. Never sponsored: these are citations."""
    return link(page_dir, url, label, external=True, **kw)


def product_link(page_dir, url, label, **kw):
    """Expose only bare observed listing URLs as product evidence."""
    if url.startswith("https://link.amazon/"):
        return f'<code class="code">{esc(url)}</code>'
    if not re.fullmatch(r"https://www\.amazon\.com/dp/[A-Z0-9]{10}", url):
        raise ValueError("Product evidence must be an untagged listing")
    return link(page_dir, url, label, sponsored=True, **kw)


def approved_cta(page_dir, record, meta):
    """Only the validated intent bundle, not a redirect observation, may supply a buy link."""
    url = meta.get("approved_links", {}).get(record["ref"])
    if not url:
        return ""
    return ('<p>Paid link: we may earn a commission if you buy through it.</p>'
            + link(page_dir, url, "Shop on Amazon ↗", cls="btn", sponsored=True,
                   affiliate_ref=record["ref"]))


def kindle(summary, body):
    """A small labelled aside. Used for honesty notes inside editorial prose."""
    return (
        '<aside class="note">'
        f'<p class="note-label">{esc(summary)}</p>'
        f"{body}"
        "</aside>"
    )


def disclosure_strip(page_dir):
    return f"""<div class="disclosure-bar" role="region" aria-label="Affiliate disclosure">
  <div class="wrap disclosure-inner">
    <span class="info-i" aria-hidden="true">i</span>
    <p>{DISCLOSURE} <a href="{esc(rel(page_dir, 'about/index.html'))}#disclosure">How our links work</a></p>
  </div>
</div>"""


def masthead(page_dir, active=None):
    # section-aware: every page under guides/ should light "Guides".
    def section_of(path):
        return path.split("/")[0] if "/" in path else path
    act = section_of(active) if active else None
    items = []
    for target, label in NAV:
        current = ' aria-current="page"' if act and section_of(target) == act else ""
        items.append(f'<a href="{esc(rel(page_dir, target))}"{current}>{esc(label)}</a>')
    from content import GUIDES
    catalog = NAV + [("compare/index.html", "Compare kitchen appliances"),
        ("review/index.html", "Flagged for review"), ("suggestions/index.html", "Suggestions"),
        ("questions/index.html", "Open questions"), ("operations/ledger.html", "Campaign ledger")]
    catalog += [(f"guides/{g['slug']}.html", g['title']) for g in GUIDES]
    products = json.loads((ROOT / 'src/data/products.json').read_text())['products']
    catalog += [(f"products/{p['ref'].lower()}.html", f"{p['brand']} {p['format_label']}") for p in products]
    results = ''.join(f'<li><a href="{esc(rel(page_dir, u))}">{esc(t)}</a></li>' for u,t in catalog)
    mark = '<svg viewBox="0 0 40 40" width="37" height="37" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="20" cy="20" r="18.3"/><path d="m10 10 6 6m-3-9 6 6m-12 0 6 6q3 3 6-1l11 12m-5-9c7-6 8-11 5-13L18 21m-1 3-7 8"/></svg>'
    return f"""<header class="masthead">
  <div class="editionline"><div class="wrap"><span>THE KITCHEN JOURNAL</span><span>VOL. 01 &nbsp; / &nbsp; NOVEMBER 2026</span></div></div>
  <div class="wrap masthead-inner">
    <a class="brand" href="{esc(rel(page_dir, 'index.html'))}">{mark}<span class="brand-name">Crisp <i>&amp;</i> Counter</span></a>
    <nav class="nav" aria-label="Sections">{"".join(items)}</nav>
    <button class="find" type="button" hidden data-find aria-label="Search the journal"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="10" cy="10" r="6.5"/><path d="m15 15 6 6"/></svg><span>Search</span></button>
  </div>
  <dialog class="searchdesk" aria-labelledby="search-title"><form method="dialog"><button aria-label="Close search">×</button></form><h2 id="search-title">Search the journal</h2><input type="search" placeholder="Try capacity, thermometer, cleanup…" aria-label="Search guides and products"><p role="status"></p><ul>{results}</ul></dialog>
</header>"""


def footer(page_dir):
    groups = []
    for heading, links in FOOTER_GROUPS:
        rows = "".join(
            f'<li><a href="{esc(rel(page_dir, t))}">{esc(l)}</a></li>' for t, l in links
        )
        groups.append(f'<div class="foot-col"><h2>{esc(heading)}</h2><ul>{rows}</ul></div>')
    return f"""<footer class="site-footer">
  <div class="wrap">
    <p class="foot-disclosure"><a href="{esc(rel(page_dir, 'review/index.html'))}#FLG-016">Thermometer link update: two checks found different destinations. Read the source notes &rarr;</a></p>
    <p class="foot-disclosure">{DISCLOSURE}</p>
    <div class="foot-grid">{"".join(groups)}</div>
    <div class="foot-bottom">
      <p>Submitted tracking ID: <code>{esc(TRACKING_ID)}</code> &mdash; supplied by the operator, attribution not independently confirmed.</p>
      <p class="foot-meta">{esc(SITE_NAME)} &middot; static site &middot; last built {esc(BUILD_DATE)} &middot; no cookies, no trackers, no third-party requests</p>
    </div>
  </div>
</footer>"""


def page(page_dir, *, title, description, body, active=None, canonical=None,
         body_class="", structured=None, og_type="website"):
    css = rel(page_dir, "assets/css/site.css")
    js = rel(page_dir, "assets/js/site.js")
    feed = rel(page_dir, "feed.xml")
    home = rel(page_dir, "index.html")
    canon = canonical or ""
    structured_block = ""
    if structured:
        structured_block = (
            '<script type="application/ld+json">'
            + json.dumps(structured, ensure_ascii=False)
            + "</script>\n"
        )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(SITE_URL + '/' + canon)}">
<link rel="icon" href="{esc(rel(page_dir, 'assets/img/favicon.svg'))}" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="{esc(SITE_NAME)} notes" href="{esc(feed)}">
<meta property="og:type" content="{esc(og_type)}">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(SITE_URL + '/' + canon)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{esc(rel(page_dir, 'assets/fonts/fraunces-latin-400-normal.woff2'))}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{esc(rel(page_dir, 'assets/fonts/inter-latin-400-normal.woff2'))}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{esc(css)}">
<link rel="stylesheet" href="{esc(rel(page_dir, 'assets/css/editorial.css'))}">
<link rel="stylesheet" href="{esc(rel(page_dir, 'assets/css/storefront.css'))}">
{structured_block}</head>
<body class="{esc(body_class)}">
<a class="skip" href="#main">Skip to content</a>
{masthead(page_dir, active)}
{disclosure_strip(page_dir)}
<main id="main">
{body}
</main>
{footer(page_dir)}
<script src="{esc(js)}" defer></script>
<script src="{esc(rel(page_dir, 'assets/js/discover.js'))}" defer></script>
<script src="{esc(rel(page_dir, 'assets/js/analytics.js'))}" defer></script>
</body>
</html>
"""


def eyebrow(text):
    return f'<p class="eyebrow">{esc(text)}</p>'


def section(inner, *, cls="", sid=None):
    ident = f' id="{esc(sid)}"' if sid else ""
    return f'<section class="section {esc(cls)}"{ident}><div class="wrap">{inner}</div></section>'


def pagehead(kicker, title, dek, meta=None):
    meta_html = f'<p class="page-meta">{meta}</p>' if meta else ""
    return f"""<header class="pagehead"><div class="wrap">
  {eyebrow(kicker)}
  <h1>{title}</h1>
  <p class="dek">{dek}</p>
  {meta_html}
</div></header>"""


def table(headers, rows, *, cls="", caption=None, note=None):
    head = "".join(f"<th scope=\"col\">{h}</th>" for h in headers)
    body = []
    for row in rows:
        cells = []
        for cell in row:
            # A dict carries raw HTML; a string is escaped text. A list is a
            # bug: iterating it would emit one cell per character, which is
            # exactly the kind of silent corruption this build refuses to ship.
            if isinstance(cell, dict):
                tag = cell.get("tag", "td")
                attrs = cell.get("attrs", "")
                cells.append(f"<{tag}{(' ' + attrs) if attrs else ''}>{cell['html']}</{tag}>")
            elif isinstance(cell, str):
                cells.append(f"<td>{esc(cell)}</td>")
            else:
                raise TypeError(f"table cell must be str or dict, got {type(cell).__name__}: {cell!r}")
        body.append("<tr>" + "".join(cells) + "</tr>")
    caption_html = f"<caption>{esc(caption)}</caption>" if caption else ""
    note_html = f'<p class="table-note">{note}</p>' if note else ""
    return (
        f'<div class="table-scroll"><table class="{esc(cls)}">{caption_html}'
        f"<thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div>"
        f"{note_html}"
    )


def blank(value, why="not confirmed"):
    if value in (None, "", []):
        return f'<span class="blank" title="{esc(why)}">&mdash;</span>'
    return esc(value)
