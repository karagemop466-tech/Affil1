"""One place that decides what a page shell looks like.

The disclosure strip, the masthead, the navigation and the footer are generated
here and nowhere else. A page cannot be added without them because there is no
other way to produce a page.

Two rules are enforced by construction rather than remembered:

  * every Amazon destination is built by buy_url(), so it always carries the
    Associates tag that Program Policies 2(b) requires;
  * every internal link is relative and computed with posixpath.relpath,
    because GitHub Pages serves this repository from /Affil1/.
"""

import html
import json
import pathlib
import posixpath

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE_NAME = "Crisp & Counter"
SITE_TAGLINE = "Air fryer & thermometer notes"
SITE_URL = "https://karagemop466-tech.github.io/Affil1"
TRACKING_ID = "shopnow047c-20"
BUILD_DATE = "2026-11-20"

DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."

# Amazon serves the price; this site does not hold price data.
AMAZON_NOTE = "Price, rating and delivery are shown on Amazon, where they are always current."

# One navigation group. Everything else is reachable from the footer.
NAV = [
    ("products/index.html", "Shop the edit"),
    ("guides/index.html", "Guides"),
    ("compare/index.html", "Compare"),
    ("questions/index.html", "Questions"),
    ("suggestions/index.html", "Suggestions"),
]

FOOTER_GROUPS = [
    ("Shop", [
        ("products/index.html", "All five picks"),
        ("products/p-01.html", "Dual-basket air fryer"),
        ("products/p-02.html", "French-door oven"),
        ("products/p-03.html", "Single-basket air fryer"),
        ("products/p-04.html", "Instant-read thermometer"),
        ("products/p-05.html", "Wireless probe set"),
    ]),
    ("Read", [
        ("guides/index.html", "All guides"),
        ("compare/index.html", "Side-by-side table"),
        ("feed.xml", "RSS feed"),
    ]),
    ("The desk", [
        ("questions/index.html", "Open questions"),
        ("suggestions/index.html", "Suggestions & decisions"),
        ("brief/index.html", "Executive summary"),
        ("operations/ledger.html", "Campaign ledger"),
    ]),
    ("Trust", [
        ("about/index.html", "About & how we link"),
        ("about/index.html#sources", "Sources"),
        ("review/index.html", "Flagged for review"),
        ("review/images.html", "Image policy"),
        ("review/measurement.html", "Measurement plan"),
    ]),
]


def esc(value):
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def rel(page_dir, target):
    """Relative URL from a page's directory to a target path at the repo root."""
    return posixpath.relpath(target, page_dir) if page_dir else target


def buy_url(asin):
    """The only place an Amazon click destination is constructed.

    Program Policies 2(b): every Special Link must carry the Associates ID as a
    tag parameter. Putting that in one function means it cannot be forgotten on
    one page and remembered on the next.
    """
    return f"https://www.amazon.com/dp/{asin}?tag={TRACKING_ID}"


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


def buy_button(page_dir, product, label="See it on Amazon", *, cls="btn"):
    """The primary call to action on a product card or page."""
    return product_link(
        page_dir,
        buy_url(product["observed_asin"]),
        f'{label} <span aria-hidden="true">&#8599;</span>',
        cls=cls,
        aria=f"Open the Amazon listing for {product['brand']} {product['format_label']} (paid link, opens in a new tab)",
    )


def note(summary, body):
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
    <span class="disclosure-tag">Paid links</span>
    <p>{DISCLOSURE} Links to Amazon here are affiliate links: if you buy through one, this site may earn a commission and you pay the same price.
      <a href="{esc(rel(page_dir, 'about/index.html'))}#disclosure">How that works</a>.</p>
  </div>
</div>"""


def masthead(page_dir, active=None):
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
      <span class="brand-tag">{esc(SITE_TAGLINE)}</span>
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
      <p>Affiliate tag on every product link: <code>{esc(TRACKING_ID)}</code>. Attribution is not yet confirmed in an Associates report.</p>
      <p class="foot-meta">{esc(SITE_NAME)} &middot; static site &middot; last built {esc(BUILD_DATE)} &middot; no cookies, no trackers, no third-party requests</p>
    </div>
  </div>
</footer>"""


def page(page_dir, *, title, description, body, active=None, canonical=None,
         body_class="", structured=None, og_type="website", og_image=None,
         index=True):
    css = rel(page_dir, "assets/css/site.css")
    js = rel(page_dir, "assets/js/site.js")
    feed = rel(page_dir, "feed.xml")
    canon = canonical or ""
    blocks = []
    if isinstance(structured, list):
        blocks = structured
    elif structured:
        blocks = [structured]
    structured_block = ""
    for block in blocks:
        structured_block += (
            '<script type="application/ld+json">'
            + json.dumps(block, ensure_ascii=False)
            + "</script>\n"
        )
    image = og_image or f"{SITE_URL}/assets/img/hero-counter-w1280.jpg"
    robots = "" if index else '<meta name="robots" content="noindex, follow">\n'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(SITE_URL + '/' + canon)}">
{robots}<link rel="icon" href="{esc(rel(page_dir, 'assets/img/favicon.svg'))}" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="{esc(SITE_NAME)} notes" href="{esc(feed)}">
<meta property="og:type" content="{esc(og_type)}">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(SITE_URL + '/' + canon)}">
<meta property="og:image" content="{esc(image)}">
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


def breadcrumbs(page_dir, trail):
    """trail: [(target, label), ...] excluding the current page."""
    items = [f'<li><a href="{esc(rel(page_dir, "index.html"))}">Home</a></li>']
    for target, label in trail:
        items.append(f'<li><a href="{esc(rel(page_dir, target))}">{esc(label)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>{"".join(items)}</ol></div></nav>'


def breadcrumb_schema(trail, current_label, current_path):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"}]
    pos = 2
    for _, label in trail:
        items.append({"@type": "ListItem", "position": pos, "name": label})
        pos += 1
    items.append({"@type": "ListItem", "position": pos, "name": current_label, "item": f"{SITE_URL}/{current_path}"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def _src_cell(url):
    if not url:
        return '<span class="src-none">no single document</span>'
    host = url.split("//", 1)[-1].split("/", 1)[0].replace("www.", "")
    return f'<a rel="noopener" href="{esc(url)}">{esc(host)}</a>'


def table(headers, rows, *, cls="", caption=None, note=None, sources=None):
    """Render a table. ``sources`` adds a final Source column.

    Pass a single URL for a table where every row rests on the same document, or
    a list with one URL per row. A row without a source link fails the build.
    """
    if sources is not None:
        headers = list(headers) + ["Source"]
        per_row = sources if isinstance(sources, (list, tuple)) else [sources] * len(rows)
        rows = [list(r) + [{"html": _src_cell(u)}] for r, u in zip(rows, per_row)]
    head = "".join(f"<th scope=\"col\">{h}</th>" for h in headers)
    body = []
    for row in rows:
        cells = []
        for cell in row:
            # A dict carries raw HTML; a string is escaped text. A list is a
            # bug: iterating it would emit one cell per character.
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


def blank(value, why="not confirmed from an official source"):
    if value in (None, "", []):
        return f'<span class="blank" title="{esc(why)}">&mdash;</span>'
    return esc(value)
