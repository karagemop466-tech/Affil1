"""The decision register: every question that stands between the site as it is
and a decision the owner can make with confidence."""

import json
import pathlib

from layout import (breadcrumb_schema, esc, eyebrow, page, pagehead, rel,
                    section, table)


def _sources():
    root = pathlib.Path(__file__).resolve().parent.parent
    doc = json.loads((root / "src/data/sources.json").read_text(encoding="utf-8"))
    return {s["id"]: s for s in doc["sources"]}


def _evidence_html(refs, sources):
    if not refs:
        return ""
    out = []
    for ref in [r.strip() for r in str(refs).split(",") if r.strip()]:
        s = sources.get(ref)
        if s:
            out.append(f'<a href="{esc(s["url"])}" rel="noopener" target="_blank">{esc(ref)}</a>')
        else:
            out.append(esc(ref))
    return f'<p class="q-evidence">Source: {", ".join(out)}</p>'


def build(page_dir, questions, meta):
    d = page_dir
    qs = questions["questions"]
    sources = _sources()
    answered = [q for q in qs if q.get("answered")]
    open_ = [q for q in qs if not q.get("answered")]
    blocking = [q for q in open_ if str(q.get("blocking", "")).startswith("yes")]

    def card(q):
        state = ('<span class="pill pill-ok">Answered</span>' if q.get("answered")
                 else '<span class="pill pill-warn">Open</span>')
        blk = ""
        if str(q.get("blocking", "")).startswith("yes"):
            blk = ' <span class="pill pill-block">Blocks work</span>'
        if q.get("answered"):
            tail = f'<div class="q-answer"><p class="q-label">Answer</p><p>{esc(q.get("answer", ""))}</p>{_evidence_html(q.get("evidence"), sources)}</div>'
        else:
            tail = f'<div class="q-answer"><p class="q-label">What would close it</p><p>{esc(q.get("how_to_close", ""))}</p></div>'
        return f"""<article class="qcard" id="{esc(q['id'])}">
  <div class="qcard-top"><span class="q-num">{esc(q['id'])}</span>{state}{blk}</div>
  <h3>{esc(q['question'])}</h3>
  <dl class="q-dl">
    <div><dt>What we have</dt><dd>{esc(q['what_we_have'])}</dd></div>
    <div><dt>What is missing</dt><dd>{esc(q['what_is_missing'])}</dd></div>
  </dl>
  {tail}
</article>"""

    rows = []
    for q in qs:
        state = '<span class="pill pill-ok">Answered</span>' if q.get("answered") else '<span class="pill pill-warn">Open</span>'
        blk = "Yes" if str(q.get("blocking", "")).startswith("yes") else "No"
        rows.append([
            {"html": f'<a href="#{esc(q["id"])}"><strong>{esc(q["id"])}</strong></a>'},
            {"html": esc(q["question"])},
            {"html": state},
            {"html": blk},
        ])
    q_table = table(["Ref", "Question", "Status", "Blocks work"], rows, cls="qtable",
                    caption=f"{len(qs)} questions: {len(answered)} answered, {len(open_)} open")

    blocking_html = "".join(card(q) for q in blocking)
    open_html = "".join(card(q) for q in open_ if not str(q.get("blocking", "")).startswith("yes"))
    answered_html = "".join(card(q) for q in answered)

    body = f"""{pagehead(
        'Questions',
        'What has to be decided<br>before anything else changes',
        f'{len(qs)} questions the site cannot answer on its own. {len(answered)} are closed with a source or a reproducible check; {len(open_)} are open, and each one names the specific document, dashboard or decision that would settle it.',
        meta='No forecasts &middot; no invented answers &middot; every closed row carries its evidence',
    )}
{section(f'''
<div class="sec-head"><div>{eyebrow('The register')}<h2>Everything in one table</h2></div>
<p>Scan the status column. The cards below carry the detail and the way out.</p></div>
{q_table}
<div class="stat-row">
  <div class="stat"><span class="stat-n">{len(qs)}</span><span class="stat-l">questions raised</span></div>
  <div class="stat"><span class="stat-n">{len(answered)}</span><span class="stat-l">answered with evidence</span></div>
  <div class="stat stat-warn"><span class="stat-n">{len(open_)}</span><span class="stat-l">still open</span></div>
  <div class="stat stat-warn"><span class="stat-n">{len(blocking)}</span><span class="stat-l">blocking other work</span></div>
</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Answer these first')}<h2>Blocking questions</h2></div>
<p>Until one of these is answered, the work that depends on it is guesswork.</p></div>
<div class="q-grid">{blocking_html}</div>''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Open, not blocking')}<h2>The rest of the list</h2></div>
<p>These affect quality, pace or reach. None of them affects whether the site is accurate today.</p></div>
<div class="q-grid">{open_html}</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Closed')}<h2>Answered, with the evidence</h2></div>
<p>Each row here links to the policy it quotes, or to the check that can be re-run.</p></div>
<div class="q-grid">{answered_html}</div>''', cls='section-tint')}
{section(f'''
<div class="callout">
  <h2>The most useful thing on this page</h2>
  <p>Not the answered questions. The blocking ones: whether a click is credited to the tag, and whether there is a lawful way to measure. Everything else can wait; those two decide whether the rest is worth doing.</p>
  <p class="callout-links"><a class="tlink" href="{esc(rel(d, 'suggestions/index.html'))}">Decide a path <span aria-hidden="true">&rarr;</span></a></p>
</div>''', cls='')}"""
    return page(
        d,
        title="Questions and what would close them | Crisp & Counter",
        description=f"{len(qs)} questions the site cannot answer alone: what is known, what is missing, and the specific artefact that would settle each one.",
        body=body,
        active="questions/index.html",
        canonical="questions/",
        index=False,
        structured=breadcrumb_schema([], "Questions", "questions/"),
    )
