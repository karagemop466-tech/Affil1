"""The decision gate.

questions/index.html is the question register. This page is the decision view of
the same evidence, and it exists because a question register answers "what do we
not know" but not "who can find out, what does it cost, and what do we ship
meanwhile". Those three columns are the difference between a list of unknowns and
something an owner can act on.

Every value comes from _src/data/decisions.json. Nothing is computed from prose.
"""

import json
import pathlib

from layout import (breadcrumb_schema, esc, eyebrow, page, pagehead, rel,
                    section, table)


def _source_docs():
    root = pathlib.Path(__file__).resolve().parent.parent
    src = {s["id"]: s for s in json.loads(
        (root / "_src/data/sources.json").read_text(encoding="utf-8"))["sources"]}
    flags = {f["id"]: f for f in json.loads(
        (root / "_src/data/flags.json").read_text(encoding="utf-8"))["flags"]}
    return src, flags


def _status_pill(text):
    t = text.lower()
    if t.startswith("yes"):
        return '<span class="pill pill-ok">Decidable now</span>'
    if t.startswith("partly"):
        return '<span class="pill pill-warn">Partly decided</span>'
    return '<span class="pill pill-block">Open</span>'


def build(page_dir, decisions, meta):
    d = page_dir
    items = decisions["decisions"]
    sources, flags = _source_docs()

    decidable = [x for x in items if x["decided"].lower().startswith("yes")]
    partly = [x for x in items if x["decided"].lower().startswith("partly")]
    open_ = [x for x in items if not x["decided"].lower().startswith(("yes", "partly"))]
    owner_only = [x for x in items if "owner" in x["who"].lower()]

    def ref_links(x):
        """Source, flag and question cross-references, each pointing somewhere real."""
        out = []
        for ref in [r.strip() for r in str(x.get("sources", "")).replace(",", " ").split() if r.strip()]:
            if ref in sources:
                out.append(f'<a href="{esc(sources[ref]["url"])}" rel="noopener" target="_blank">{esc(ref)}</a>')
            elif ref in flags:
                out.append(f'<a href="{esc(rel(d, "review/index.html"))}#{esc(ref)}">{esc(ref)}</a>')
            elif ref.startswith("S-"):
                out.append(f'<a href="{esc(rel(d, "suggestions/index.html"))}#{esc(ref)}">{esc(ref)}</a>')
            else:
                out.append(esc(ref))
        qs = [q.strip() for q in str(x.get("questions", "")).split(",") if q.strip()]
        if qs:
            href = esc(rel(d, "questions/index.html"))
            out.append("questions " + ", ".join(
                f'<a href="{href}#{esc(q)}">{esc(q)}</a>' for q in qs))
        if not out:
            return '<span class="blank">&mdash;</span>'
        return " &middot; ".join(out)

    def card(x):
        return f"""<article class="qcard" id="{esc(x['id'])}">
  <div class="qcard-top"><span class="q-num">{esc(x['id'])}</span>{_status_pill(x['decided'])}</div>
  <h3>{esc(x['decision'])}</h3>
  <dl class="q-dl">
    <div><dt>What we already have</dt><dd>{esc(x['what_we_have'])}</dd></div>
    <div><dt>What we do not have</dt><dd>{esc(x['what_we_lack'])}</dd></div>
    <div><dt>How to find it out</dt><dd>{esc(x['how_to_find_out'])}</dd></div>
    <div><dt>Who can do that</dt><dd>{esc(x['who'])}</dd></div>
    <div><dt>Cost of finding out</dt><dd>{esc(x['cost'])}</dd></div>
  </dl>
  <div class="q-answer"><p class="q-label">What the site ships meanwhile</p><p>{esc(x['default'])}</p></div>
  <p class="q-evidence">Sources: {ref_links(x)}</p>
</article>"""

    rows = [[
        {"html": f'<a href="#{esc(x["id"])}"><strong>{esc(x["id"])}</strong></a>'},
        {"html": esc(x["decision"])},
        {"html": _status_pill(x["decided"])},
        {"html": esc(x["who"])},
        {"html": esc(x["cost"])},
    ] for x in items]

    overview = table(
        ["Ref", "The decision", "Status", "Who can settle it", "Cost to find out"],
        rows, cls="qtable",
        caption=f"{len(items)} decisions: {len(decidable)} decidable now, "
                f"{len(partly)} partly decided, {len(open_)} open")

    gating = ("D-03", "D-02", "D-01", "D-04")
    gating_cards = "".join(card(x) for x in items if x["id"] in gating)
    rest_cards = "".join(card(x) for x in items if x["id"] not in gating)

    body = f"""{pagehead(
        'Decision gate',
        'What has to be known<br>before anything is decided',
        f'{len(items)} decisions turn this project. {len(decidable)} can be made today from published sources, '
        f'{len(partly)} are half answered and {len(open_)} are open &mdash; each one naming the artefact, '
        f'dashboard or person that would close it, what finding out costs, and what the site ships meanwhile.',
        meta='Nothing here is a forecast &middot; every “what we have” is sourced &middot; no value is filled in by inference',
    )}\
{section(f'''
<div class="lede-prose">
  <p>“We do not know yet” is only useful if it says what would tell us. Each row below separates three things that are usually blurred together: what is already established and where it came from, what is genuinely missing, and the concrete step that would retrieve it.</p>
  <p>Read the <strong>who can settle it</strong> column first. {len(owner_only)} of the {len(items)} decisions need an Associates dashboard this project cannot sign in to, and no amount of work inside the repository will close them. The rest are answerable from published sources or from a decision the owner simply has not made yet.</p>
  <p>This page complements <a href="{esc(rel(d, 'questions/index.html'))}">the question register</a> rather than repeating it: that page lists what is known and missing per question; this one adds who, cost and default per decision.</p>
</div>
{overview}
<div class="stat-row">
  <div class="stat"><span class="stat-n">{len(items)}</span><span class="stat-l">decisions identified</span></div>
  <div class="stat"><span class="stat-n">{len(decidable)}</span><span class="stat-l">decidable now</span></div>
  <div class="stat stat-warn"><span class="stat-n">{len(open_)}</span><span class="stat-l">open</span></div>
  <div class="stat stat-warn"><span class="stat-n">{len(owner_only)}</span><span class="stat-l">need the account owner</span></div>
</div>''', cls='')}\
{section(f'''
<div class="sec-head"><div>{eyebrow('Settle these first')}<h2>The decisions that gate the others</h2></div>
<p>Until D-03 is answered, any work that assumes a click is paid is guesswork, and everything downstream inherits that uncertainty.</p></div>
<div class="q-grid">{gating_cards}</div>''', cls='section-tint')}\
{section(f'''
<div class="sec-head"><div>{eyebrow('Everything else')}<h2>The remaining decisions</h2></div>
<p>Content, structure, measurement, imagery and money. None is blocked by the four above, though two get easier once those are answered.</p></div>
<div class="q-grid">{rest_cards}</div>''', cls='')}\
{section(f'''
<div class="callout">
  <h2>The one thing worth doing before anything on this page</h2>
  <p>D-03 is the whole project in one question: does a click on a supplied link get credited to <code class="code">{esc(meta.get('tracking') or '')}</code>? One click from the owner's own device and one look at the Associates click report answers it, and that report is the only permitted source for the answer. Until then the site can send readers somewhere that pays nothing, and no amount of design or content work changes that.</p>
  <p>The second is cheaper still and needs no account at all: verifying the property in Search Console and submitting the sitemap. That is the only route to real query data, and real query data is what turns D-05 from an opinion into a decision.</p>
  <p class="callout-links"><a class="tlink" href="{esc(rel(d, 'suggestions/index.html'))}">See the proposals these decisions gate <span aria-hidden="true">&rarr;</span></a></p>
</div>''', cls='')}"""

    return page(
        d,
        title="Decision gate | Crisp & Counter",
        description=f"{len(items)} decisions this affiliate site turns on: what is already known and sourced, what is missing, the step that would find it out, who can take it, what it costs, and what the site ships meanwhile.",
        body=body,
        active="decide/index.html",
        canonical="decide/",
        structured=breadcrumb_schema([], "Decision gate", "decide/"),
    )
