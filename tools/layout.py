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
    ("index.html", "Home"),
    ("guides/index.html", "Buying guides"),
    ("products/index.html", "Product shortlist"),
    ("compare/index.html", "Compare"),
    ("brief/index.html", "Site desk"),
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
         aria=None, title=None):
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
    """A link to Amazon. Always marked sponsored, always in a new tab."""
    return link(page_dir, url, label, sponsored=True, **kw)


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
    <span class="disc-icon" aria-hidden="true">i</span>
    <p>{DISCLOSURE} <a href="{esc(rel(page_dir, 'about/index.html'))}#disclosure">Affiliate disclosure</a></p>
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
    return f"""<header class="masthead">
  <div class="wrap masthead-inner">
    <a class="brand" href="{esc(rel(page_dir, 'index.html'))}">
      <svg class="brand-mark" width="39" height="39" viewBox="0 0 40 40" fill="none" aria-hidden="true"><rect x="1" y="1" width="38" height="38" rx="10" fill="#35233c"/><g stroke="#f9db9a" stroke-width="1.8" stroke-linecap="round"><path d="M7 24h21c-1 5-6 7-11 7s-9-2-10-7Zm20-1 6-4M10 20h14M14 17c-4-4 4-5 0-9m6 9c-4-4 4-5 0-9"/></g></svg>
      <span class="brand-name">Crisp <span class="brand-amp">&amp;</span> Counter</span>
    </a>
    <nav class="nav" aria-label="Sections">
      {"".join(items)}
    </nav>
  </div>
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
    destination_note = '' if not canonical else f'''<div class="wrap" role="note"><p><strong>Destination update:</strong> Checks of P-04 and P-05 produced differing destinations. Product records are observations, not confirmed intended destinations. <a href="{esc(rel(page_dir, 'review/index.html'))}#FLG-016">See the review flag and sources</a>.</p></div>'''
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
<link rel="stylesheet" href="{esc(rel(page_dir, 'assets/css/storefront.css'))}">
{structured_block}</head>
<body class="{esc(body_class)}">
<a class="skip" href="#main">Skip to content</a>
{masthead(page_dir, active)}
{disclosure_strip(page_dir)}
<main id="main">
{destination_note}
{body}
</main>
{footer(page_dir)}
<script src="{esc(js)}" defer></script>
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
