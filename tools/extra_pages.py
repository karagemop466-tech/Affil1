"""Pages added by the integration pass: publication front page, topics index,
operations dashboard.

Imported by build.py from main() after the base pages are built, so it can
replace the front page and reuse the same component functions. One template, one
navigation group, one disclosure strip: a new page cannot ship without them,
because it is rendered by the same page() function as everything else.
"""

import json
import pathlib

from build import (BUILD_DATE, COMPARE_ROWS, EVENTS, FLAGS, GUIDES, PRICE_BLANK_NOTE,
                   PRODUCT_BY_ID, PRODUCTS, QUESTIONS, ROOT, SITE_NAME, SITE_URL, SUGGESTIONS,
                   TOPICS, TRACKING_ID, esc, guide_rows, page, product_card,
                   product_link, tagged_listing_url)

DATA = ROOT / "src" / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


REVERIF = load("reverification.json")
LEDGER = load("ledger.json")

# The five new guides this pass added, so the front page can lead with one.
NEW_SLUGS = ["air-fryer-thanksgiving-overflow", "frozen-food-nights", "dual-basket-math",
             "smart-probe-thermometer", "first-week-checklist"]

IMG = "/assets/img"   # root-absolute: page() rewrites it per directory depth

CREDIT = ("Illustration made for this publication. It is not product photography, not an image "
          "from any listing, and not a representation of the item a link leads to.")

QUEUE = [
    ("Preheating: does your machine actually need it?", "Live with it", "Every manual answers this differently and the answer changes cook times. Needs the manufacturer's documents for each unit we carry."),
    ("Air fryer vs toaster oven: when is the fan the point?", "Choose the shape", "The clearest question readers ask in comments elsewhere; answerable from listings plus a manufacturer spec, no testing required."),
    ("What actually fits: 6, 8 and 26 quarts in one-layer terms", "Size it right", "Extends the capacity guide with the three cavities in our register."),
    ("Basket coatings: what a listing can and cannot tell you about nonstick", "Live with it", "Materials and dishwasher wording are listing-level facts; durability is not, and we would say so."),
    ("A probe for everything, not just turkey", "Buy smart", "Second piece in the thermometer thread; pairs with the one non-fryer row in the register."),
    ("Holiday leftovers: the reheating problem, sized", "Cook with it", "Seasonal follow-up to the overflow guide, publishable in the week the traffic actually exists."),
]


def guide_card(slug, image=None, kicker=None):
    g = GUIDES[slug]
    media = ""
    if image:
        media = (f'<div class="card-media"><img src="{IMG}/{image}" alt="{esc(g["title"])} — editorial illustration" '
                 f'loading="lazy" width="960" height="640"></div>')
    return f"""<a class="feature-card" href="/guides/{slug}/">
  {media}
  <div class="feature-body">
    <p class="kicker">{esc(kicker or g['cluster'])}</p>
    <h3>{esc(g['title'])}</h3>
    <p>{esc(g['deck'])}</p>
    <p class="feature-meta">{g['minutes']} min read &middot; {esc(SITE_NAME)} editorial &middot; updated {BUILD_DATE}</p>
  </div>
</a>"""


def save_button(pid):
    """Local-only shortlist. Nothing leaves the browser, so nothing needs a privacy claim."""
    return (f'<button class="save-btn" type="button" data-save="{esc(pid)}" '
            f'aria-label="Save this item to your shortlist in this browser">Save</button>')


def product_card_with_save(p, rank=None):
    html = product_card(p, rank)
    return html.replace('<div class="card-foot">', f'<div class="card-foot">{save_button(p["id"])}')


# ------------------------------------------------------------------ front page

def build_front():
    ids = [p["id"] for p in PRODUCTS["products"]]
    resolved = [i for i in ids if PRODUCT_BY_ID[i].get("official_listing_url")]
    cards = "".join(product_card_with_save(PRODUCT_BY_ID[i], f"{n:02d}")
                    for n, i in enumerate(ids, start=1))
    feature = guide_card(NEW_SLUGS[0], image="feature-holiday.jpg", kicker="This week’s feature")
    secondary = "".join(guide_card(s, image=img) for s, img in
                        [(NEW_SLUGS[1], "topic-frozen.jpg"), (NEW_SLUGS[3], "topic-probe.jpg"),
                         (NEW_SLUGS[4], "topic-firstweek.jpg")])
    topic_chips = "".join(
        f'<a class="topic-chip" href="/topics/#{esc(t["name"])}"><strong>{esc(t["name"])}</strong>'
        f'<span>{esc(t["blurb"])}</span></a>' for t in TOPICS)

    schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": SITE_URL + "/",
        "description": "Question-led buying guides for air fryers and countertop cooking appliances, "
                      "with a public verification register.",
        "publisher": {"@type": "Organization", "name": SITE_NAME},
    }

    body = f"""
<div class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <p class="kicker">Issue 02 &middot; countertop cooking &middot; {BUILD_DATE}</p>
        <h1>The air fryer that survives your kitchen.</h1>
        <p class="deck">Nine guides, five links we actually checked, and not one invented star rating.
        We tell you what each seller claims, what the listing cannot tell you, and which question to
        answer before you spend anything.</p>
        <div class="byline">
          <span>Updated {BUILD_DATE}</span><span class="dot">&middot;</span>
          <span>{len(GUIDES)} guides</span><span class="dot">&middot;</span>
          <span>{len(resolved)} of {len(ids)} listings identified</span><span class="dot">&middot;</span>
          <span>0 prices published, on purpose</span>
        </div>
        <p class="hero-cta">
          <a class="btn" href="/guides/{NEW_SLUGS[0]}/">Read this week’s feature<span aria-hidden="true"> &rarr;</span></a>
          <a class="btn ghost" href="/compare/">Compare the range</a>
        </p>
      </div>
      <div class="hero-media">
        <img src="{IMG}/hero-counter.jpg" width="960" height="720"
             alt="A countertop air fryer on a warm kitchen counter with a tray of vegetables beside it, illustrated for this publication.">
        <figcaption>{esc(CREDIT)}</figcaption>
      </div>
    </div>
  </div>
</div>

<section class="strip">
  <div class="wrap strip-inner">
    <span><strong>{len(GUIDES)}</strong> guides, written as questions</span>
    <span><strong>{len(ids)}</strong> submitted links checked by hand</span>
    <span><strong>1</strong> never resolved &mdash; <a href="/flagged/">see it published, not hidden</a></span>
    <span class="strip-end"><a href="/topics/">Browse by topic</a></span>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>This week’s feature</h2>
      <p>The November argument for a second heat source is not health or speed. It is oven geometry.</p>
    </div>
    {feature}
  </div>
</section>

<section class="section section-tight">
  <div class="wrap">
    <div class="section-head">
      <h2>The shortlist</h2>
      <p>Every product we were given, described in the seller’s own words. Save one to a list in this
      browser — nothing is uploaded, and there is no account.</p>
    </div>
    <div class="product-grid" id="shortlist">{cards}</div>
    <div class="saved-list" id="saved-list" hidden>
      <div class="saved-head">
        <p><b data-saved-count>0</b> saved in this browser &middot; nothing is uploaded, and clearing site data removes the list.</p>
        <button class="save-btn" type="button" id="clear-saved">Clear list</button>
      </div>
      <ul data-saved-items></ul>
    </div>
    <p class="footnote">Brand, category and ASIN were read from the page each submitted link resolved to
    on {BUILD_DATE}. Capability wording belongs to the seller, not to us. Price, rating, review count and
    stock are blank because Amazon permits them only in a link it serves or through its API.
    <a href="/about/#why-blank">Why we leave them blank</a> &middot;
    <a href="/sources/">Full source register</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>New this issue</h2>
      <p>Written for the questions people actually arrive with — and each one ends by naming what it does not claim.</p>
    </div>
    <div class="card-rail">{secondary}</div>
  </div>
</section>

<section class="section section-tight">
  <div class="wrap">
    <div class="section-head">
      <h2>Every guide</h2>
      <p>Five decisions: shape, size, living with it, cooking with it, buying smart.</p>
    </div>
    {guide_rows()}
    <p class="footnote"><a class="btn ghost" href="/guides/">All {len(GUIDES)} guides &rarr;</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Browse by topic</h2>
      <p>The same questions, grouped the way a decision arrives.</p></div>
    <div class="topic-rail">{topic_chips}</div>
  </div>
</section>

<section class="section section-tight">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>The one thing we will not do</h2>
        <p style="max-width:60ch">Amazon allows a site to show a price only when Amazon serves the link that
        carries it, or when the figure comes through the Creators API or PA API. This site has neither, so it
        shows no price, no star rating, no review count and no stock status. A price that was true last month is
        a lie this month, and an unearned five stars is worse than none.</p>
        <p style="max-width:60ch">The same discipline applies to the writing. Every capability sentence is either
        quoted from a seller’s listing title or left out. We have not tested these machines, so we do not tell you
        which cooks better. We would be making that up.</p>
        <p><a class="btn ghost" href="/about/">How this site works &rarr;</a></p>
      </div>
      <div class="fp-panel">
        <p class="kicker" style="margin-bottom:12px">New every fortnight</p>
        <p style="margin-top:0">One question-shaped guide, published and added to the feed and the sitemap on the
        same day. No email address required — subscribe to the feed and nothing about you is stored.</p>
        <p class="subscribe">
          <a class="btn" href="/feed.xml">RSS feed</a>
          <a class="btn ghost" href="/topics/#queue">What is in the queue</a>
        </p>
        <p class="footnote" style="margin-bottom:0">A reader-email list is a <a href="/suggestions/">proposed
        change awaiting a decision</a>, not a feature that exists.</p>
      </div>
    </div>
  </div>
</section>

<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
"""
    return page("/", f"{SITE_NAME} — air fryer and countertop buying guides",
                "Question-led buying guides for air fryers, dual baskets and countertop cooking appliances. "
                "Every listing checked by hand, every claim attributed, no prices or ratings we cannot stand behind.",
                body, active="/")


# ------------------------------------------------------------------ topics

def build_topics():
    by_cluster = {}
    for slug, g in GUIDES.items():
        by_cluster.setdefault(g["cluster"], []).append((slug, g))

    blocks = []
    for t in TOPICS:
        rows = by_cluster.get(t["name"], [])
        if not rows:
            continue
        items = "".join(
            f'<li><a href="/guides/{s}/">{esc(g["title"])}</a><span>{esc(g["deck"])}</span>'
            f'<span class="tmeta">{g["minutes"]} min</span></li>' for s, g in rows)
        blocks.append(f'<section class="topic-block" id="{esc(t["name"])}">'
                      f'<h2>{esc(t["name"])}</h2><p>{esc(t["blurb"])}</p><ul>{items}</ul></section>')

    queue = "".join(
        f'<tr><td>{esc(t)}</td><td>{esc(c)}</td><td>{esc(why)}</td>'
        f'<td><span class="badge none">not started</span></td></tr>' for t, c, why in QUEUE)

    body = f"""
<div class="wrap">
  <div class="page-head">
    <h1>Topics</h1>
    <p>Every guide on this site answers one of five questions. Read the one that matches the problem you can
    already describe; skip the ones you cannot.</p>
  </div>
  {''.join(blocks)}

  <section class="topic-block" id="queue">
    <h2>What is in the queue, and why</h2>
    <p>These are editorial hypotheses, not claims about search volume, popularity or product superiority.
    A topic earns its place by answering a question a reader can already ask. After two published issues,
    the queue gets re-ordered by measured arrivals rather than by our instincts — which is exactly what the
    <a href="/dashboard/#measurement">measurement status</a> on the dashboard is for.</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Working title</th><th>Topic</th><th>Why it is here</th><th>Status</th></tr></thead>
        <tbody>{queue}</tbody>
      </table>
    </div>
    <p class="footnote">Nothing in this table is written, scheduled or guaranteed. Publishing cadence is a
    proposal the owner has not approved; see <a href="/suggestions/">the suggestion board</a>.</p>
  </section>
</div>"""
    return page("/topics/", f"Topics — {SITE_NAME}",
                "Buying guides for countertop cooking appliances, grouped by the decision they support, "
                "with the editorial queue published in the open.",
                body, active="/topics/",
                crumbs=[("/", "Home"), (None, "Topics")])


# ------------------------------------------------------------------ dashboard

def status_badge(ok, yes="verified", no="unverified"):
    return f'<span class="badge {"ok" if ok else "warn"}">{esc(yes if ok else no)}</span>'


def reverify_rows():
    out = []
    for r in REVERIF["rows"]:
        listing = (f'<a href="{esc(r["observed_listing_url"])}" rel="nofollow noopener" target="_blank">'
                   f'{esc(r["observed_asin"])}</a>') if r.get("observed_asin") else \
            '<span class="asin missing">not identified</span>'
        flag = ('<span class="badge bad">correction</span>' if r.get("contradicts_archived_register")
                else status_badge(r["agrees_with_current_register"], "agrees", "needs review"))
        out.append(f"""<tr>
  <td><span class="mono">{esc(r['id'])}</span></td>
  <td class="mono small">{esc(r['submitted_link'])}<br><span style="color:var(--ink-3)">path code {esc(r['path_code'])} · {r['path_code_length']} chars</span></td>
  <td>{listing}</td>
  <td>{esc(r['status'])}</td>
  <td>{flag}</td>
</tr>""")
    return "".join(out)


def findings_rows():
    out = []
    for p in PRODUCTS["products"]:
        src = p.get("observed_source_url") or p.get("source")
        cells = {
            "brand": p.get("brand") or "",
            "listing": p.get("listing_title") or "",
            "asin": p.get("observed_redirect_asin") or "",
            "price": "", "rating": "", "availability": "", "wattage": "", "dimensions": "",
        }
        out.append(f"""<tr>
  <td><span class="mono">{esc(p['id'])}</span></td>
  <td>{esc(p.get('brand') or '—')}</td>
  <td class="title-cell" title="{esc(p.get('listing_title') or '')}">{esc((p.get('listing_title') or 'No listing reached')[:88])}{'…' if len(p.get('listing_title') or '') > 88 else ''}</td>
  <td>{f'<span class="asin">{esc(p["observed_redirect_asin"])}</span>' if p.get('observed_redirect_asin') else '<span class="asin missing">not identified</span>'}</td>
  <td>{('<a href="' + esc(src) + '" rel="nofollow noopener" target="_blank">official page</a>') if src and src.startswith('http') else '<span class="asin missing">no source reached</span>'}</td>
  <td><span class="badge none">not published</span></td>
  <td><span class="badge none">not published</span></td>
</tr>""")
    return "".join(out)


def ledger_rows():
    if LEDGER["rows"]:
        return "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in LEDGER["rows"])
    span = 8
    return (f'<tr><td colspan="{span}" class="empty-cell">{esc(LEDGER["empty_note"])}</td></tr>')


def build_dashboard():
    ev = "".join(
        f'<tr><td><span class="mono">{esc(e["name"])}</span> <span class="mono" style="color:var(--ink-3)">{esc(e["id"])}</span></td>'
        f'<td>{esc(e["fires_when"])}</td>'
        f'<td>{esc(e["answers"])}</td>'
        f'<td>{esc(", ".join(e["not_collected"]))}</td>'
        f'<td><span class="badge ok">client shipped</span> <span class="badge warn">storage pending</span></td></tr>'
        for e in EVENTS["events"])

    sev = {"high": "bad", "medium": "warn", "low": "none"}
    flags = "".join(
        f'<tr><td><span class="mono">{esc(f["id"])}</span></td><td>{esc(f["title"])}</td>'
        f'<td><span class="badge {sev.get(f.get("severity", "low"), "none")}">{esc(f.get("severity", "low"))}</span></td>'
        f'<td><a href="/flagged/#{esc(f["id"])}">review action</a></td></tr>' for f in FLAGS["flags"])

    checks = "".join(
        f'<tr><td>{esc(c["check"])}</td><td>{"enforced by tools/validate.py in CI" if c.get("automated") else "human review before publish"}</td>'
        f'<td><span class="badge {"ok" if c.get("state") == "pass" else "warn"}">{esc(c.get("state", "open"))}</span></td></tr>'
        for c in LEDGER["compliance_checks"])

    body = f"""
<div class="wrap">
  <div class="page-head">
    <h1>Operations dashboard</h1>
    <p>The working side of the publication: what was entered, what was verified, what is still blank and why,
    what is measured, and what a reviewer has to decide. Every row carries its source. Nothing here is a
    performance claim, and no revenue figure appears because no authorized report has been read.</p>
  </div>

  <div class="stat-row">
    <div class="stat"><strong>{len(PRODUCTS['products'])}</strong><span>links submitted</span></div>
    <div class="stat"><strong>{REVERIF['summary']['links_resolved']}</strong><span>reached a product page</span></div>
    <div class="stat"><strong>{REVERIF['summary']['links_unresolved']}</strong><span>unresolved, published as such</span></div>
    <div class="stat"><strong>{len(GUIDES)}</strong><span>guides live</span></div>
    <div class="stat"><strong>{len(FLAGS['flags'])}</strong><span>items flagged for review</span></div>
    <div class="stat"><strong>{len(SUGGESTIONS['suggestions'])}</strong><span>suggestions awaiting a decision</span></div>
  </div>

  <section id="entries">
    <h2>1 · Entries and findings</h2>
    <p class="section-sub">One row per submitted link. A blank cell means the value could not be confirmed from an
    official source, and was left blank rather than inferred.</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Entry</th><th>Brand</th><th>Listing reached</th><th>ASIN</th>
        <th>Source</th><th>Price</th><th>Rating</th></tr></thead>
        <tbody>{findings_rows()}</tbody>
      </table>
    </div>
    <p class="footnote">{esc(PRICE_BLANK_NOTE)}</p>
  </section>

  <section id="verification">
    <h2>2 · Verification log</h2>
    <p class="section-sub">{esc(REVERIF['meta']['method'])}</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Entry</th><th>Submitted link</th><th>Observed destination</th><th>Finding</th><th>vs. register</th></tr></thead>
        <tbody>{reverify_rows()}</tbody>
      </table>
    </div>
    <div class="callout">
      <span class="callout-label">Irregularities found while re-verifying</span>
      <p>{esc(REVERIF['summary']['conclusion'])}</p>
      <p>{esc(REVERIF['summary']['attribution_conclusion'])}</p>
      <p>Corrections applied this pass: an archived register recorded rows P-03 and P-05 as reaching only the
      Amazon homepage; both reach product pages, and P-05 is a meat thermometer rather than a fryer. The
      archived file is preserved unchanged at
      <span class="mono">archive/2026-11-20-integration/data/confirmations.json</span> so the disagreement stays reviewable.</p>
    </div>
  </section>

  <section id="campaigns">
    <h2>3 · Campaign ledger</h2>
    <p class="section-sub">A ledger is only worth having if it cannot be padded. Rows are added from authorized
    first-party reports — never from an estimate, and never from a self-recorded click count standing in for a sale.</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Timestamp</th><th>Source</th><th>Channel</th><th>Eligible sessions</th><th>Clicks</th>
        <th>Reported orders</th><th>Provenance report</th><th>Notes</th></tr></thead>
        <tbody>{ledger_rows()}</tbody>
      </table>
    </div>
    <h3>Provenance trail</h3>
    <ul class="tick">
      {''.join(f'<li><span class="mono">{esc(e["timestamp"])}</span> — {esc(e["action"])} <em>({esc(e["note"])})</em></li>' for e in LEDGER['provenance_trail'])}
    </ul>
  </section>

  <section id="measurement">
    <h2>4 · Measurement status</h2>
    <p class="section-sub">Five events are defined in the shipped client. Counting clicks is honest only while it is
    clear that a click is not a conversion: attribution lives in Amazon’s reports, not in our logs.</p>
    <div class="table-wrap">
      <table><thead><tr><th>Event</th><th>Fires when</th><th>What it answers</th><th>Never collected</th><th>Status</th></tr></thead>
      <tbody>{ev}</tbody></table>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Instrument</th><th>State</th><th>What would change it</th></tr></thead>
        <tbody>
          <tr><td>Self-hosted collector</td><td><span class="badge warn">code shipped, not deployed</span></td><td>Static GitHub Pages cannot run it. Deploy <span class="mono">analytics/endpoint.py</span> anywhere with storage, then point the client at it.</td></tr>
          <tr><td>Search Console</td><td><span class="badge warn">not verified</span></td><td>Needs the property owner to verify <span class="mono">karagemop466-tech.github.io/Affil1</span>. Nobody has claimed it in this repository, and verifying it is not an agent task.</td></tr>
          <tr><td>Associates reports</td><td><span class="badge warn">no account access</span></td><td>Clicks and orders only ever come from the enrolled account’s own reports. Until then the ledger above stays empty.</td></tr>
          <tr><td>Cookies / consent banner</td><td><span class="badge ok">not needed</span></td><td>No cookies, no third-party scripts, no cross-site identifiers — see <a href="/about/#privacy">privacy</a>.</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section id="gate">
    <h2>5 · Compliance gate</h2>
    <p class="section-sub">What a page has to pass before it publishes. The automated half runs in CI on every push;
    the human half is a review someone performs, and this table is where an unfinished review is visible.</p>
    <div class="table-wrap">
      <table><thead><tr><th>Check</th><th>How it is enforced</th><th>State</th></tr></thead>
      <tbody>{checks}</tbody></table>
    </div>
  </section>

  <section id="registers">
    <h2>6 · Registers</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Register</th><th>Holds</th><th>Open</th></tr></thead>
        <tbody>
          <tr><td>Source register</td><td>Every observation and policy quotation, with its official link</td><td><a href="/sources/">Source register</a></td></tr>
          <tr><td>Flagged for review</td><td>{len(FLAGS['flags'])} irregularities and unverified values, with the source that would settle each</td><td><a href="/flagged/">Flagged register</a></td></tr>
          <tr><td>Suggestion board</td><td>{len(SUGGESTIONS['suggestions'])} scored proposals, each with what it costs and what blocks it</td><td><a href="/suggestions/">Suggestion board</a></td></tr>
          <tr><td>Open questions</td><td>{len(QUESTIONS['questions'])} questions that must be answered before a decision is reasonable</td><td><a href="/questions/">Open questions</a></td></tr>
          <tr><td>Re-verification data</td><td>This pass’s independent fetch log, as machine-readable JSON</td><td><a href="/src/data/reverification.json" rel="nofollow">reverification.json</a></td></tr>
        </tbody>
      </table>
    </div>
  </section>
</div>"""
    return page("/dashboard/", f"Operations dashboard — {SITE_NAME}",
                "Entries, verification log, empty campaign ledger, measurement status and the compliance gate "
                "for a hand-checked affiliate publication.",
                body, active="/dashboard/", crumbs=[("/", "Home"), (None, "Dashboard")])


def build_all():
    build_front()
    build_topics()
    build_dashboard()
