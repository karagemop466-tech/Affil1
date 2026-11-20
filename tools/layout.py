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
SITE_TAGLINE = "The countertop edit"
SITE_URL = "https://karagemop466-tech.github.io/Affil1"
TRACKING_ID = "shopnow047c-20"
BUILD_DATE = "2026-11-20"

DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."

# A retail destination is an affiliate link; a policy page is a citation.
AFFILIATE_HINT = __import__("re").compile(
    r"^https?://(?:(?:[a-z0-9-]+\.)*amazon\.[a-z.]+/(?:dp|gp/product)/|link\.amazon/)", __import__("re").I)

# The only navigation group. Everything else lives in the footer.
NAV = [
    ("products/index.html", "Shop"),
    ("guides/index.html", "Guides"),
    ("compare/index.html", "Compare"),
    ("questions/index.html", "Ask"),
]

FOOTER_GROUPS = [
    ("Shop", [
        ("products/index.html", "All five products"),
        ("categories/air-fryers.html", "Air fryers"),
        ("categories/thermometers.html", "Meat thermometers"),
        ("products/p-01.html", "Dual-basket air fryer"),
        ("products/p-02.html", "French-door oven"),
        ("products/p-03.html", "Single-basket air fryer"),
        ("compare/index.html", "Compare everything"),
    ]),
    ("Read", [
        ("guides/index.html", "Every guide"),
        ("guides/basket-or-oven-air-fryer.html", "Basket or oven?"),
        ("guides/air-fryer-capacity-checklist.html", "Capacity checklist"),
        ("guides/batch-cooking-for-the-week.html", "Batch cooking for the week"),
        ("guides/hosting-season-air-fryer.html", "Hosting season"),
    ]),
    ("Follow", [
        ("feed.xml", "RSS feed"),
        ("calendar/index.html", "Publishing calendar"),
        ("questions/index.html", "Ask a question"),
        ("about/index.html#editorial", "How we write"),
        ("about/index.html#disclosure", "Disclosure"),
        ("privacy.html", "Privacy"),
    ]),
    ("Desk", [
        ("suggestions/index.html", "Suggestions queue"),
        ("review/index.html", "Flagged for review"),
        ("review/images.html", "Image policy"),
        ("review/measurement.html", "Measurement plan"),
        ("operations/ledger.html", "Campaign ledger"),
        ("brief/index.html", "Executive summary"),
        ("about/index.html", "Sources"),
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


def tagged(url):
    """Return an Amazon product URL carrying the Associates tag.

    Program Policies 2(b) requires the tag as a URL parameter in the link
    itself, and the Commission Income Statement excludes purchases that are not
    correctly tracked because a link was not properly formatted. Every product
    link on this site therefore passes through here.

    The tag is *appended by this function*, so the value in the URL is the
    supplied tracking ID and nothing else. It is a constructed value, not an
    observed one: no supplied link showed a tag on arrival (FLG-002), and a
    tagged link has still not been confirmed inside the Associates account
    (FLG-018). The build says so on the review page rather than implying
    otherwise.
    """
    if not url or "tag=" in url:
        return url
    m = re.match(r"^(https?://(?:(?:[a-z0-9-]+\.)*amazon\.[a-z.]+/(?:dp|gp/product)/[A-Z0-9]{10}))([?#].*)?$", url, re.I)
    if not m:
        return url
    return f"{m.group(1)}?tag={TRACKING_ID}"


def product_link(page_dir, url, label, **kw):
    """A link to Amazon. Always tagged, always marked sponsored, always new tab."""
    return link(page_dir, tagged(url), label, sponsored=True, **kw)


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
    <span class="disclosure-tag">Disclosure</span>
    <p><strong>{DISCLOSURE}</strong> Every Amazon link on this page is a paid link, marked
      <code class="disclosure-code">rel="sponsored"</code>, and the price you pay is the same either way.
      <a href="{esc(rel(page_dir, 'about/index.html'))}#disclosure">How the links work</a>.</p>
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
      <span class="brand-name">Crisp <span class="brand-amp">&amp;</span> Counter</span>
      <span class="brand-tag">{SITE_TAGLINE}</span>
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
      <p class="foot-meta">{esc(SITE_NAME)} &middot; a buying guide, not a review site &middot; last updated {esc(BUILD_DATE)} &middot; no cookies, no trackers, no third-party requests</p>
      <p class="foot-meta">Tracking ID <code>{esc(TRACKING_ID)}</code> supplied by the publisher; attribution is not yet confirmed in the Associates account. <a href="{esc(rel(page_dir, 'review/index.html'))}#FLG-002">What that means</a>.</p>
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
