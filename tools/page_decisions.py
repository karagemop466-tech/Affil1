"""The decision dossier: what must be known before anything is built.

This page exists because the suggestion queue is only as good as the questions
underneath it. Every row names one decision, the information already held, the
information missing, and the specific artefact that would close the gap. Rows
marked answered carry a source link; rows marked open do not pretend otherwise.
"""

from layout import (blank, esc, eyebrow, outbound, page, pagehead, rel, section,
                    table)


def _state(d):
    if d.get("answered"):
        return '<span class="pill pill-ok">Answered</span>'
    return '<span class="pill pill-warn">Open</span>'


def _known_list(items):
    return "".join(
        f'<li>{esc(k["fact"])} <span class="tiny">({esc(k["source"])})</span></li>'
        for k in items
    )


def _card(d, sec_dir, sources_by_id):
    known = _known_list(d.get("known", []))
    answer = ""
    if d.get("answered"):
        answer = f"""<div class="dec-answer">
      <p class="q-label">The answer on record</p>
      <p>{esc(d.get('answer'))}</p>
      <p class="tiny">Evidence: {esc(d.get('evidence'))}</p>
    </div>"""
    return f"""<article class="flag dec" id="{esc(d['id'])}">
  <div class="flag-top">
    <span class="flag-id">{esc(d['id'])}</span>
    {_state(d)}
  </div>
  <h3>{esc(d['question'])}</h3>
  <dl class="flag-dl">
    <div><dt>Why this is on the list</dt><dd>{esc(d['why_now'])}</dd></div>
    <div><dt>What we already have</dt><dd><ul class="tight">{known}</ul></dd></div>
    <div><dt>What is missing</dt><dd>{esc(d['missing'])}</dd></div>
    <div><dt>How to find it out</dt><dd>{esc(d['how_to_find'])}</dd></div>
    <div><dt>The artefact that closes it</dt><dd>{esc(d['artefact'])}</dd></div>
    <div><dt>Who can supply it</dt><dd>{esc(d['who'])}</dd></div>
    <div><dt>Cost</dt><dd>{esc(d['cost'])}</dd></div>
    <div><dt>What it unblocks</dt><dd>{esc(d['unblocks'])}</dd></div>
  </dl>
  {answer}
</article>"""


def build(page_dir, decisions, sources, meta):
    d = page_dir
    items = decisions["decisions"]
    by_id = {x["id"]: x for x in items}
    open_n = sum(1 for x in items if not x.get("answered"))
    done_n = len(items) - open_n

    gate_blocks = []
    for g in decisions["gates"]:
        rows = []
        for did in g["decisions"]:
            x = by_id[did]
            rows.append([
                {"html": f'<a href="#{esc(x["id"])}"><strong>{esc(x["id"])}</strong></a>'},
                {"html": esc(x["question"])},
                {"html": esc(x["missing"]) if not x.get("answered") else esc(x.get("answer", ""))},
                {"html": esc(x["who"])},
                {"html": _state(x)},
            ])
        gate_blocks.append(section(f"""
<div class="sec-head"><div>{eyebrow(g['id'])}<h2>{esc(g['name'])}</h2></div>
<p>{esc(g['why'])}</p></div>
{table(['Ref', 'The question', 'What is missing', 'Who can supply it', 'State'], rows, cls='decisions')}
<div class="dec-stack">
{''.join(_card(by_id[did], d, {}) for did in g['decisions'])}
</div>""", cls='section-tint' if g["id"] in ("G-2", "G-4") else ''))

    body = f"""{pagehead(
        'Before you decide',
        'Everything that has to be<br>known first',
        f'{len(items)} decisions, {open_n} of them still open. Each one shows the information already held with its source, the information that is missing, and the artefact that would supply it. Nothing here is a forecast.',
        meta='Written 2026-11-20 &middot; a decision is only marked answered when a source can be opened',
    )}
{section(f'''
<div class="decide-intro">
  <div>
    <h2>Why this page exists</h2>
    <p>A suggestion queue that does not name its own preconditions is a wish list. Each proposal on the
    <a href="{esc(rel(d, 'suggestions/index.html'))}">suggestions page</a> points back to one of the rows below,
    so a reviewer can see what has to be true before a proposal is worth approving.</p>
    <p>The rule is the same one the rest of the site runs on. An answer counts when an outside reader can
    open the source and check it. Where no source exists yet, the row says what would create one &mdash;
    usually a screenshot, a sentence from the operator, or a single test click.</p>
  </div>
  <dl class="reg-stats">
    <div><dt>Decisions</dt><dd>{len(items)}</dd></div>
    <div><dt>Answered</dt><dd>{done_n}</dd></div>
    <div><dt>Still open</dt><dd>{open_n}</dd></div>
    <div><dt>Gates</dt><dd>{len(decisions['gates'])}</dd></div>
  </dl>
</div>

<div class="callout">
  <h2>Read the gates in order</h2>
  <p>Gate one asks whether a click can be credited to this site at all. Gate two asks what the site is
  allowed to show. Gate three asks whether a publication exists behind it. Gate four asks whether anything
  is being measured. Doing gate three work while gate one is open is how affiliate sites end up looking
  finished and earning nothing.</p>
</div>''', cls='')}
{''.join(gate_blocks)}
{section(f'''
<div class="sec-head"><div>{eyebrow('The short answer')}<h2>What can be decided today</h2></div>
<p>Four rows need nothing but a decision. Everything else needs an artefact first.</p></div>
{table(
    ['Decision', 'Needs', 'Time'],
    [
        [{'html': '<a href="#D-05">D-05</a> &mdash; may the site show prices?'}, 'Nothing. The policy is the answer.', 'Decided: no'],
        [{'html': '<a href="#D-06">D-06</a> &mdash; is the disclosure in the right place?'}, 'A human read of the wording', 'Decided: placement yes, wording open'],
        [{'html': '<a href="#D-11">D-11</a> &mdash; one site or two?'}, 'A sentence: keep noindexed, redirect, or delete', 'An hour'],
        [{'html': '<a href="#D-16">D-16</a> &mdash; who checks the links?'}, 'A named owner and a cadence', 'Ten minutes a month'],
    ],
    cls='decisions')}
<p class="table-note">The rows that <em>cannot</em> be decided today are not blocked by research. They are
blocked by account access or by an operator decision, which is why the site publishes them instead of
guessing.</p>''', cls='')}"""

    return page(
        d,
        title="Before you decide \u2014 what must be known first \u2014 Crisp & Counter",
        description=("Sixteen decisions behind this site, each with the information already held, the "
                     "information missing, and the artefact that would close the gap. Two are answered; "
                     "the rest are open and say why."),
        body=body,
        active="questions/index.html",
        canonical="questions/decisions.html",
    )
