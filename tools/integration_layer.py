#!/usr/bin/env python3
"""Integration layer: the five added guides and the verification page, in this edition's shapes.

This repository was rebuilt from scratch by a dozen parallel sessions, each shipping its own
front page, stylesheet, build script and data schema. Six competing editions is not a
publication — and it is not verifiable either, because two generators writing the same
`index.html` means the committed HTML and the deployed artifact can disagree. So there is one
build (`tools/build.py`), and this module is a *step* of it rather than a rival site.

It converts the guide copy written during the integration pass (`content_extra.GUIDES`, stored
as rich HTML for the earlier edition) into this edition's structured guide schema at build time,
so the prose has one source and never drifts into a second template:

  * headings and paragraphs map onto `sections` (this edition's renderer escapes paragraph text,
    which is exactly the behaviour a compliant publication wants: nobody can slip markup into
    a claim);
  * every link in the body is lifted out and rendered as a source table row with a real
    outbound URL, because "quote the source" is worth more here than an inline hyperlink;
  * a guide that referenced register rows gets those rows appended as related products, read
    from `src/data/products.json`, never re-typed.

`verification/index.html` is the one surface this edition did not have: a single page of
dashboard-style tables answering "what did you check, against which official source, when, and
what is still blank". It is built from the same JSON as everything else.
"""

from __future__ import annotations

import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data"

# Where a body link pointed in the previous edition → what this edition actually publishes.
# Anything not mapped is dropped from the source table rather than shipped as a 404, and the
# link checker in CI (tools/check.py) fails on a broken local link all the same.
# These pages publish under guides/<slug>.html, so every local target sits one level
# deeper than it looks; the checker resolves links against the file, not the site root.
ROUTE_MAP = {
    "/flagged/": "../review/index.html",
    "/suggestions/": "../suggestions/index.html",
    "/questions/": "../questions/index.html",
    "/sources/": "../review/index.html",
    "/compare/": "../compare/index.html",
    "/products/": "../products/index.html",
    "/about/": "../about/index.html",
    "/dashboard/": "../verification/index.html",
    "/topics/": "../guides/index.html",
    "/guides/": "../guides/index.html",
}


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


# --------------------------------------------------------------------- conversion

BLOCK = re.compile(r"<(h2|h3|p|li|ol|ul)\b[^>]*>(.*?)</\1>", re.S | re.I)
TAG = re.compile(r"<[^>]+>")
ANCHOR = re.compile(r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", re.S | re.I)


def _text(fragment: str) -> str:
    """Strip markup, unescape entities, tidy whitespace. Keeps quotes as written."""
    fragment = re.sub(r"<br\s*/?>", " ", fragment)
    fragment = TAG.sub("", fragment)
    text = html.unescape(fragment)
    return re.sub(r"\s+", " ", text).strip()


def convert(slug: str, g: dict) -> dict:
    """Rich HTML body → this edition's structured guide schema."""
    body = g["body"]
    sections: list[dict] = []
    current: dict | None = None
    sources: dict[str, str] = {}

    def open_section(heading: str):
        nonlocal current
        if current:
            sections.append(current)
        current = {"h": heading, "p": []}
        sections_append = None  # noqa: F841  (kept explicit for readability)

    for match in BLOCK.finditer(body):
        tag, inner = match.group(1).lower(), match.group(2)
        if tag == "h2":
            heading = _text(inner)
            if current:
                sections.append(current)
            current = {"h": heading, "p": []}
            continue
        if current is None:
            current = {"h": "Before you start", "p": []}
        if tag == "p":
            text = _text(inner)
            if not text:
                continue
            # Lift every link out of the sentence and into the source table, leaving
            # the sentence readable on its own.
            for href, label in ANCHOR.findall(inner):
                if href.startswith(("http://", "https://")):
                    sources.setdefault(href, _text(label) or href)
                else:
                    target = ROUTE_MAP.get(href) or ROUTE_MAP.get(href.split("#")[0]) or ROUTE_MAP.get(href.split("#")[0] + "/")
                    if target:
                        sources.setdefault(target, _text(label) or target)
            text = ANCHOR.sub(lambda m: _text(m.group(2)), text)
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                current["p"].append(text)
        elif tag == "li":
            text = _text(inner)
            if text:
                current["p"].append("— " + text)

    if current:
        sections.append(current)

    # A short callout at the end of every guide: what the guide does not claim.
    closing = g.get("closing") or (
        "Nothing here is a test result. Every capability sentence quotes a seller's own listing "
        "title and says so; price, rating, review count and availability are absent because Amazon "
        "permits them only when it serves the link or through its API, and no such feed is connected "
        "to this site. Values that could not be confirmed from an official source are left blank and "
        "listed on the flagged register."
    )

    if sources:
        sections.append({
            "h": "Sources for this guide",
            "table": {
                "headers": ["What it supports", "Source"],
                "caption": "Read on 2026-11-20. A link to an Amazon listing here is a citation used to "
                           "identify a product, not a promotion: only the register's own record decides what "
                           "a product page was observed to be.",
                "rows": [[label, {"url": url, "label": _short(url)}] for url, label in list(sources.items())[:12]],
            },
        })

    photo = "assets/img/" + re.sub(r"\.jpg$", "", g.get("og_image") or "hero-counter")
    return {
        "slug": slug,
        "cluster": g.get("cluster", "Buying"),
        "kicker": g.get("kicker") or g.get("cluster", "Buying").lower(),
        "title": g["title"],
        "dek": g["deck"],
        "read_minutes": g.get("minutes", 6),
        "photo": photo,
        "photo_alt": g["title"] + " — illustration made for this publication",
        "photo_caption": "Illustration made for this publication: not product photography, not an image "
                         "from a listing, and not a depiction of the item a link leads to.",
        "updated": "2026-11-20",
        "related": g.get("products", []),
        "sections": sections,
        "closing": closing,
    }


def _short(url: str) -> str:
    if url.startswith("http"):
        host = re.sub(r"^https?://", "", url).split("/")[0]
        return host.replace("www.", "")
    return url.split("/")[-1] or url


def guides() -> list[dict]:
    """The five added guides, in this edition's schema."""
    import content_extra

    out = []
    for slug, g in content_extra.GUIDES.items():
        if g.get("cluster") not in ("Choosing", "Sizing", "Everyday cost", "Before you buy"):
            g = {**g}
        out.append(convert(slug, g))
    return out


# --------------------------------------------------------------------- verification page

def verification_body() -> str:
    reverify = load("reverification.json")
    products = {p["ref"]: p for p in load("products.json")["products"]}
    flags = load("flags.json")["flags"]
    events = load("events.json")["events"]
    suggestions = load("suggestions.json")["suggestions"]
    questions = load("questions-open.json")["questions"]
    intent = load("product-intent.json")

    def cell(v):
        return html.escape(str(v)) if not isinstance(v, str) else v

    rows = []
    for r in reverify["rows"]:
        asin = r.get("observed_asin")
        dest = (f'<a href="{cell(r["observed_listing_url"])}" rel="sponsored nofollow noopener" target="_blank">'
                f'{cell(asin)}</a>' if asin else "<em>none reached</em>")
        note = r.get("discrepancy") or r.get("status") or ""
        agree = ('<span class="tag ok">agrees</span>' if r.get("agrees_with_current_register")
                 else '<span class="tag warn">review</span>')
        rows.append(f"<tr><td>{cell(r['id'])}</td>"
                    f"<td><a href=\"{cell(r['submitted_link'])}\" rel=\"sponsored nofollow noopener\" target=\"_blank\">"
                    f"{cell(r['path_code'])}</a><span class=\"micro\"> {r['path_code_length']}-char code</span></td>"
                    f"<td>{dest}<span class=\"micro\">{cell(note)}</span></td><td>{agree}</td></tr>")

    flag_rows = "".join(
        f"<tr><td>{cell(f['id'])}</td><td>{cell(f['title'])}</td>"
        f"<td><span class=\"tag {cell(f.get('severity','low'))}\">{cell(f.get('severity','low'))}</span></td>"
        f"<td><a href=\"../review/index.html#{cell(f['id'])}\">source and action</a></td></tr>"
        for f in flags)

    ev_rows = "".join(
        f"<tr><td>{cell(e['name'])}</td><td>{cell(e['fires_when'])}</td><td>{cell(e['answers'])}</td>"
        f"<td>{cell(', '.join(e.get('not_collected', [])[:4]))}</td></tr>" for e in events)

    approved = [r for r in intent["records"] if r.get("approved_special_link")]
    live = bool(intent.get("associate_enrollment_confirmed") and intent.get("site_registered")
                and intent.get("one_link_test_completed"))

    def badge(value):
        return ('<span class="tag ok">true</span>' if value
                else '<span class="tag warn">false — owner action</span>')

    state = ("affiliate links live" if (live or approved)
             else "reference links only — no tracking tag is emitted anywhere on this site")

    official = "".join(
        f'<li><a href="{cell(url)}" rel="nofollow noopener" target="_blank">{cell(name.replace("_", " "))}</a></li>'
        for name, url in reverify["meta"]["official_sources"].items())

    products_rows = "".join(
        f"<tr><td>{cell(p['ref'])}</td><td>{cell(p.get('brand') or '—')}</td>"
        f"<td>{cell((p.get('listing_title') or 'No listing reached')[:110])}</td>"
        f"<td>{'<span>' + cell(p['observed_redirect_asin']) + '</span>' if p.get('observed_redirect_asin') else '<em>none</em>'}</td>"
        f"<td><em>blank — not confirmed from an official source</em></td>"
        f"<td>{'<a href=&quot;' + cell(p.get('observed_source_url') or p.get('source')) + '&quot; rel=&quot;sponsored nofollow noopener&quot;>official page</a>' if (p.get('observed_source_url') or p.get('source', '')).startswith('http') else '<em>no source reached</em>'}</td></tr>"
        for p in products.values())

    return f"""
<section class="section"><div class="wrap">
  <span class="eyebrow">Decision support</span>
  <h1>What was checked, against what, and when</h1>
  <p class="dek">One page of tables for the reviewer: every submitted link, the destination it was observed
  to reach, what disagreed between passes, the monetization gate, and the measurement plan. Every row carries
  the link it was read from. Nothing here is a performance claim, a ranking, or a revenue figure.</p>

  <h2>The three fetch passes</h2>
  <p>{cell(reverify['meta']['method'])}</p>
  <p class="micro">{cell(reverify['meta'].get('why_two_passes', ''))}</p>
  <table class="data">
    <caption class="micro">Each destination is an observation of what the short link returned when it was
    requested, with its timestamp. It is not a confirmation of what the owner intended to enrol.</caption>
    <thead><tr><th>Entry</th><th>Submitted link</th><th>Destination reached 2026-11-20</th><th>Versus the register</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
  <p class="micro">{cell(reverify['summary'].get('independent_confirmation', ''))}</p>
</div></section>

<section class="section tint"><div class="wrap">
  <h2>The register, field by field</h2>
  <table class="data">
    <caption class="micro">A blank cell is a finding, not an omission: the value could not be confirmed from an
    official source, so it is not published.</caption>
    <thead><tr><th>Entry</th><th>Brand</th><th>Listing title as observed</th><th>ASIN</th><th>Price / rating</th><th>Source</th></tr></thead>
    <tbody>{products_rows}</tbody>
  </table>
</div></section>

<section class="section"><div class="wrap">
  <h2>Unresolved, and who can resolve it</h2>
  <table class="data">
    <thead><tr><th>Flag</th><th>Item</th><th>Severity</th><th>Source and action</th></tr></thead>
    <tbody>{flag_rows}</tbody>
  </table>
</div></section>

<section class="section tint"><div class="wrap">
  <h2>The monetization gate</h2>
  <table class="data">
    <caption class="micro">Read from src/data/product-intent.json at build time. Nothing in this table claims
    that an account exists, is enrolled, or is in good standing.</caption>
    <thead><tr><th>Gate field</th><th>Value</th></tr></thead>
    <tbody>
      <tr><td>Tracking ID supplied by the owner</td><td><code>{cell(intent['tracking_id_supplied'])}</code></td></tr>
      <tr><td>Enrolment confirmed</td><td>{badge(intent.get('associate_enrollment_confirmed'))}</td></tr>
      <tr><td>This site registered to the ID</td><td>{badge(intent.get('site_registered'))}</td></tr>
      <tr><td>One-link test completed</td><td>{badge(intent.get('one_link_test_completed'))}</td></tr>
      <tr><td>Special Links recorded</td><td>{len(approved)} of {len(intent['records'])} products</td></tr>
      <tr><td>Published state</td><td><strong>{cell(state)}</strong></td></tr>
    </tbody>
  </table>
  <p class="micro">Closing this gap is a data edit and one owner command
  (<code>python3 tools/arm_links.py --checklist</code>) rather than a code change, and the build fails if a
  tracking tag is ever published while these fields are false.</p>
  <p class="micro"><strong>Correction recorded 2026-11-20:</strong> earlier pages in this repository stated that
  every Amazon destination had been changed to carry <code>?tag=shopnow047c-20</code>. That is not the published
  state, and it is not the safe one: a tag asserts that this site is registered to that ID on an enrolled account,
  which no source in this repository can confirm, and an unregistered or improperly formatted link is the
  publisher&rsquo;s breach. The destinations are untagged listing URLs until the gate above is closed, and
  <code>tools/test_paid_link_gate.py</code> plus <code>tools/check.py</code> now enforce that in CI.</p>
</div></section>

<section class="section"><div class="wrap">
  <h2>Measurement plan, and what it is not</h2>
  <table class="data">
    <thead><tr><th>Event</th><th>Fires when</th><th>What it answers</th><th>Never collected</th></tr></thead>
    <tbody>{ev_rows}</tbody>
  </table>
  <p class="micro">No revenue figure, conversion rate or forecast appears on this page or anywhere on this site,
  because no authorized report has been read. The campaign ledger is published empty, with its schema and a dated
  provenance trail, for the same reason.</p>
</div></section>

<section class="section tint"><div class="wrap">
  <h2>Official sources behind every rule on this site</h2>
  <ul class="source-list">{official}</ul>
  <p class="micro">Program terms were read from these pages directly on 2026-11-20. Third-party SEO and affiliate
  blogs are not cited as authority anywhere on this site, including by this page.</p>

  <h2>Registers</h2>
  <ul>
    <li><a href="../review/index.html">Flagged for review</a> — the same {len(flags)} items with what each one blocks.</li>
    <li><a href="../suggestions/index.html">Suggestions</a> — {len(suggestions)} proposals, including the ones rejected on policy grounds.</li>
    <li><a href="../questions/index.html">Open questions</a> — {len(questions)} questions with the information each still needs.</li>
    <li><a href="../operations/ledger.html">Campaign ledger</a> — empty by design, with its provenance trail.</li>
    <li><a href="../guides/index.html">The journal</a> — every guide, including the five added by this pass.</li>
  </ul>
</div></section>
"""


def build(ctx=None):
    """No-op entry point kept so a future build step can extend this layer safely."""
    return ["guides/*.html (integration set)", "verification/index.html"]
