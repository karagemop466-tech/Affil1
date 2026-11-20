"""The suggestion queue: choose a path, then accept or reject the rows inside it.

The page is deliberately ordered the other way round from a to-do list. A
reviewer picks a strategy first, because a single row approved in isolation
is how sites end up with half a plan.
"""

from layout import esc, eyebrow, page, pagehead, rel, section, table


def _impact_class(impact):
    return {"High": "pill-ok", "Medium": "pill-warn", "Low": "pill-none"}.get(impact, "pill")


def _card(s):
    status = ""
    if s.get("status") == "implemented":
        status = '<span class="pill pill-ok">implemented 2026-11-20</span>'
    return f"""<article class="scard" id="{esc(s['id'])}" data-path="{esc(s['path'])}" data-impact="{esc(s['impact'])}">
  <div class="scard-head">
    <span class="scard-id">{esc(s['id'])}</span>
    <h3>{esc(s['title'])}</h3>
    <span class="scard-effort">{esc(s['effort'])}</span>
  </div>
  <div class="scard-body">
    <div class="scard-why"><p class="q-label">Why</p><p>{esc(s['why'])}</p></div>
    <dl class="scard-meta">
      <div><dt>Path</dt><dd>{esc(s['path'])}</dd></div>
      <div><dt>Impact</dt><dd><span class="pill {_impact_class(s['impact'])}">{esc(s['impact'])}</span></dd></div>
      <div><dt>Risk</dt><dd>{esc(s['risk'])}</dd></div>
      <div><dt>Reversible</dt><dd>{esc(s['reversible'])}</dd></div>
      <div><dt>Depends on</dt><dd>{esc(s['depends_on'])}</dd></div>
      <div><dt>Recommendation</dt><dd class="rec">{esc(s['recommendation'])} {status}</dd></div>
    </dl>
  </div>
  <div class="scard-foot">
    <span class="decide-label">Decision</span>
    <button type="button" class="decide" data-decision="accept" aria-pressed="false">Accept</button>
    <button type="button" class="decide" data-decision="hold" aria-pressed="false">Hold</button>
    <button type="button" class="decide" data-decision="reject" aria-pressed="false">Reject</button>
    <span class="decide-note" data-note>Undecided</span>
  </div>
</article>"""


def build(page_dir, suggestions, meta):
    d = page_dir
    items = suggestions["suggestions"]
    by_id = {s["id"]: s for s in items}
    paths = suggestions["paths"]

    path_rows = []
    for p in paths:
        path_rows.append([
            {"html": f'<strong>Path {esc(p["id"])}</strong><br><span class="tiny">{len(p["items"])} proposals</span>'},
            {"html": f'<strong>{esc(p["name"])}</strong><br>{esc(p["summary"])}'},
            {"html": esc(p["time"])},
            {"html": esc(p["cash"])},
            {"html": esc(p["signal"])},
            {"html": esc(p["risk"])},
            {"html": esc(p["choose_when"])},
        ])

    path_cards = "".join(
        f"""<article class="path">
  <span class="path-n">{esc(p['id'])}</span>
  <h3>{esc(p['name'])}</h3>
  <p>{esc(p['summary'])}</p>
  <dl class="scard-meta">
    <div><dt>Time to signal</dt><dd>{esc(p['time'])}</dd></div>
    <div><dt>Cash</dt><dd>{esc(p['cash'])}</dd></div>
    <div><dt>What you give up</dt><dd>{esc(p['gives_up'])}</dd></div>
    <div><dt>Proposals</dt><dd>{', '.join(esc(i) for i in p['items'])}</dd></div>
  </dl>
</article>""" for p in paths
    )

    grouped = []
    for p in paths:
        cards = "".join(_card(by_id[i]) for i in p["items"] if i in by_id)
        grouped.append(section(f"""
<div class="sec-head"><div>{eyebrow('Path ' + p['id'])}<h2>{esc(p['name'])}</h2></div>
<p>{esc(p['signal'])}</p></div>
{cards}""", cls='section-tint' if p["id"] == "B" else ''))

    body = f"""{pagehead(
        'Suggestions',
        'Three paths.<br>Twenty proposals.',
        'Each proposal says what it would change, what it costs, what could go wrong, whether it can be undone, and which open question has to be answered before it makes sense. Nothing here is a promise that the site will do it.',
        meta=f'Nothing on this page changes the site &middot; decisions are stored in your browser only, never sent anywhere &middot; {len(items)} proposals, 3 implemented',
    )}
{section(f'''
<div class="decide-intro">
  <div>
    <h2>Choose a path before choosing a row</h2>
    <p>The rows are not independent. Approving the eighth one while the first is open produces a bigger site
    with the same problem. So pick a strategy from the three below, then work through its rows. The
    preconditions for every row are written out on
    <a href="{esc(rel(d, 'questions/decisions.html'))}">Before you decide</a>.</p>
    <p>Marking a row writes to this browser's own storage. There is no account, no backend and nothing is
    transmitted. <strong>Copy decisions</strong> turns the marks into plain text you can paste into a message:
    that is the hand-off, a human deciding and then instructing.</p>
  </div>
  <div class="decide-tools">
    <button type="button" class="btn btn-small" data-action="copy">Copy decisions</button>
    <button type="button" class="btn btn-ghost btn-small" data-action="reset">Clear all</button>
    <p class="decide-count" data-count>0 of {len(items)} decided</p>
  </div>
</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The three paths')}<h2>Different costs, different bets</h2></div>
<p>All three are consistent with Amazon's policies. They are not equally consistent with each other.</p></div>
{table(['Path', 'What it is', 'Time to signal', 'Cash', 'Signal you get', 'Main risk', 'Choose it when'], path_rows, cls='paths')}
<div class="path-grid">
{path_cards}
</div>''', cls='')}
{section(f'''
<div class="callout">
  <h2>The recommendation, stated plainly</h2>
  <p><strong>Path A first, and only Path A.</strong> Two of its four rows are already done in the build and the
  remaining two cost one click and one template change. Until a click appears in the Associates report, a fifth
  guide is a guess about demand and a tested product is a guess about interest.</p>
  <p>Then Path B, because publishing without measurement is how a site arrives at forty pages and no readers.
  Path C is the only one that produces something a competitor cannot copy, and it should start the week you
  decide you are still doing this in a year.</p>
</div>''', cls='')}
{''.join(grouped)}
{section(f'''
<div class="callout">
  <h2>The one recommendation to read twice</h2>
  <p>Everything else on this page adds something. S-11 says stop: do not commission more AI-written guides until
  either a real test or real search data exists. More synthetic prose makes the site bigger, not better, and
  Amazon's own review process says it looks for content that would stand up with the advertising removed.</p>
  <p>The five guides that exist are defensible because they claim little. That is a narrow advantage, and it
  survives by not being diluted.</p>
</div>''', cls='')}"""

    return page(
        d,
        title="Suggestions \u2014 three paths, twenty proposals \u2014 Crisp & Counter",
        description=("A decision queue for this site: three coherent strategies, twenty proposals, each with its "
                     "cost, its risk, whether it is reversible and the open question it depends on, plus a "
                     "decision control per row."),
        body=body,
        active="suggestions/index.html",
        canonical="suggestions/",
    )
