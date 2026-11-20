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
    ("guides/index.html", "Guides"),
    ("products/index.html", "Products"),
    ("compare/index.html", "Compare"),
    ("questions/index.html", "Questions"),
    ("suggestions/index.html", "Suggestions"),
]

FOOTER_GROUPS = [
    ("Shop", [
        ("products/index.html", "The shortlist"),
        ("compare/index.html", "Compare the five"),
        ("products/p-02.html", "The oven-style option"),
        ("products/p-05.html", "The thermometers"),
        ("feed.xml", "RSS feed"),
    ]),
    ("Read", [
        ("guides/index.html", "All guides"),
        ("guides/basket-or-oven-air-fryer.html", "Basket or oven"),
        ("guides/air-fryer-capacity-checklist.html", "Capacity checklist"),
        ("guides/instant-read-or-probe-thermometer.html", "Choosing a thermometer"),
    ]),
    ("Review queue", [
        ("review/index.html", "Flagged for review"),
        ("review/measurement.html", "Measurement plan"),
        ("review/images.html", "Image policy"),
        ("sources/index.html", "Sources and quotations"),
    ]),
    ("Desk", [
        ("questions/index.html", "Open questions"),
        ("suggestions/index.html", "Suggestions and decisions"),
        ("operations/ledger.html", "Campaign ledger"),
        ("brief/index.html", "Executive summary"),
        ("about/index.html", "About, disclosure and privacy"),
    ]),
]


def esc(value):
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def rel(page_dir, target):
    """Relative URL from a page's directory to a target path at the repo root."""
    if not target:
        return ""
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


WORDS = ("zero one two three four five six seven eight nine ten eleven twelve "
         "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty "
         "twenty-one twenty-two twenty-three twenty-four twenty-five").split()


def spelled(n):
    """Small integers spelled out, because a page that says '21 flags' reads like a log."""
    return WORDS[n] if 0 <= n < len(WORDS) else str(n)


def _load(name):
    import json
    import pathlib
    return json.loads((pathlib.Path(__file__).resolve().parent.parent / "src" / "data" / name).read_text(encoding="utf-8"))


def flag_count():
    return len(_load("flags.json")["flags"])


def question_count():
    return len(_load("questions.json")["questions"])


TRACKING_TAG = "shopnow047c-20"


def tagged(url):
    """Every Amazon retail URL leaves this site carrying the Associates tag.

    Policies 2(b) (SRC-02) requires the tracking ID as a parameter of the link,
    so a bare /dp/ address is corrected here rather than left to each template.
    A submitted short link is returned unchanged: it is shown as evidence of what
    the owner sent, and the short-link service cannot carry the tag itself.
    """
    import re
    if not AFFILIATE_HINT.search(url) or "link.amazon/" in url:
        return url
    if re.search(r"[?&]tag=", url):
        return url
    return url + ("&" if "?" in url else "?") + "tag=" + TRACKING_TAG


def product_link(page_dir, url, label, **kw):
    """A link to Amazon. Always tagged, always marked sponsored, always a new tab."""
    return link(page_dir, tagged(url), label, sponsored=True, **kw)


def cite_or_product(page_dir, url, label, **kw):
    """An Amazon retail URL is a Special Link; anything else is a citation.

    Getting this wrong in either direction is a real error: an unmarked product
    link breaches the marking claim, and a marked citation misdescribes a policy
    page as a paid link. So the decision is made from the URL, once.
    """
    if AFFILIATE_HINT.search(url):
        return product_link(page_dir, url, label, **kw)
    return outbound(page_dir, url, label, **kw)


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
    <p>{DISCLOSURE} Links to Amazon on this site are affiliate links. If you buy through one, this site may earn a commission at no extra cost to you.
      <a href="{esc(rel(page_dir, 'about/index.html'))}#disclosure">Read the full disclosure</a>.</p>
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
      <p>Tracking ID on this site: <code>{esc(TRACKING_ID)}</code> &mdash; supplied by the operator, attribution not independently confirmed.</p>
      <p class="foot-meta">{esc(SITE_NAME)} &middot; static site &middot; last built {esc(BUILD_DATE)} &middot; no cookies, no trackers, no third-party requests</p>
    </div>
  </div>
</footer>"""


def page(page_dir, *, title, description, body, active=None, canonical=None,
         body_class="", structured=None, og_type="website", breadcrumb=None):
    css = rel(page_dir, "assets/css/site.css")
    js = rel(page_dir, "assets/js/site.js")
    feed = rel(page_dir, "feed.xml")
    home = rel(page_dir, "index.html")
    canon = canonical or ""
    graph = []
    if structured:
        graph.append(structured)
    if breadcrumb:
        graph.append({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": name,
                 "item": SITE_URL + "/" + target}
                for i, (name, target) in enumerate(breadcrumb)
            ],
        })
    structured_block = ""
    if len(graph) == 1:
        structured_block = ('<script type="application/ld+json">'
                            + json.dumps(graph[0], ensure_ascii=False) + "</script>\n")
    elif graph:
        structured_block = ('<script type="application/ld+json">'
                            + json.dumps({"@context": "https://schema.org", "@graph": [
                                {k: v for k, v in item.items() if k != "@context"} for item in graph]},
                                ensure_ascii=False) + "</script>\n")
    crumbs_html = ""
    if breadcrumb:
        items = []
        for i, (name, target) in enumerate(breadcrumb):
            last = i == len(breadcrumb) - 1
            if last:
                items.append(f'<span aria-current="page">{esc(name)}</span>')
            else:
                items.append(f'<a href="{esc(rel(page_dir, target))}">{esc(name)}</a>')
        crumbs_html = ('<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap">'
                       + ' <span aria-hidden="true">/</span> '.join(items)
                       + "</div></nav>\n")
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
{crumbs_html}{body}
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
