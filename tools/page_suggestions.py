"""The suggestion board: a reviewer can accept, hold or reject each row.

Nothing on this page is implemented by pressing a button. The buttons record a
decision in the reader's own browser so it can be copied back out as text. That
is the hand-off point: a human decides, then instructs.
"""

from layout import cite_or_product, esc, eyebrow, page, pagehead, rel, section, table
from content import ARTICLE_IDEAS


def _evidence(links):
    if not links:
        return '<span class="tiny">No external source: this one rests on what the site itself contains.</span>'
    return "<br>".join(cite_or_product(None, l["url"], l["label"]) for l in links)


def build(page_dir, suggestions, meta):
    d = page_dir
    doc = suggestions if isinstance(suggestions, dict) else {"suggestions": suggestions}
    items = doc["suggestions"]
    done = [s for s in items if s["status"] == "done"]
    live = [s for s in items if s["status"] != "done"]

    def row(s):
        status = {
            "done": '<span class="pill pill-ok">Implemented</span>',
            "hold": '<span class="pill pill-warn">Recommend hold</span>',
            "proposed": '<span class="pill">Awaiting decision</span>',
        }.get(s["status"], '<span class="pill">Awaiting decision</span>')
        evidence = "".join(cite_or_product(None, l["url"], l["label"]) + " " for l in s.get("evidence", []))
        return f"""<article class="scard" id="{esc(s['id'])}" data-status="{esc(s['status'])}">
  <div class="scard-head">
    <span class="scard-id">{esc(s['id'])}</span>
    <h3>{esc(s['title'])}</h3>
    <span class="scard-cat">{esc(s.get('category') or '')} &middot; priority {esc(str(s.get('priority') or ''))}</span>
  </div>
  <div class="scard-body">
    <div class="scard-what">
      <p class="q-label">What it changes</p><p>{esc(s['what'])}</p>
      <p class="q-label">Why</p><p>{esc(s['why'])}</p>
    </div>
    <dl class="scard-meta">
      <div><dt>Effort</dt><dd>{esc(s['effort'])}</dd></div>
      <div><dt>Risk</dt><dd>{esc(s['risk'])}</dd></div>
      <div><dt>Depends on</dt><dd>{esc(s['depends_on'])}</dd></div>
      <div><dt>Evidence</dt><dd class="scard-evidence">{evidence or 'none external'}</dd></div>
      <div><dt>Status</dt><dd>{status}</dd></div>
    </dl>
  </div>
  <div class="scard-foot">
    <span class="decide-label">Your call</span>
    <button type="button" class="decide" data-decision="accept" aria-pressed="false">Accept</button>
    <button type="button" class="decide" data-decision="hold" aria-pressed="false">Hold</button>
    <button type="button" class="decide" data-decision="reject" aria-pressed="false">Reject</button>
    <span class="decide-note" data-note>Undecided</span>
  </div>
</article>"""

    rows = [[
        {"html": f'<a href="#{esc(s["id"])}"><strong>{esc(s["id"])}</strong></a>'},
        {"html": esc(s["title"])},
        {"html": esc(s.get("category") or "")},
        {"html": esc(s["effort"])},
        {"html": esc(s["depends_on"])},
        {"html": {'done': "Implemented", 'hold': "Recommended hold", 'proposed': "Awaiting decision"}.get(s["status"], "")},
    ] for s in items]
    tbl = table(["Ref", "Proposal", "Area", "Effort", "Depends on", "State"], rows, cls="register",
                caption="Fifteen proposals, seven already implemented in this build",
                note="Implemented rows are kept on the page rather than deleted, because a decision log that hides its completed items cannot be audited.")

    body = f"""{pagehead(
        'Suggestions',
        'Fifteen proposals,<br>one decision each',
        'Each row says what it would change, what it costs, what could go wrong, and which open question has to be answered first. '
        'Seven are already implemented; the rest are waiting for you.',
        meta='Nothing here needs approval to stay published &middot; decisions are stored in your browser, never sent anywhere',
    )}
{section(f'''
<div class="decide-intro">
  <div>
    <h2>How to use this board</h2>
    <p>Work down the list and mark each row. The buttons record your decision in this browser's own storage so you can come back to
    it. Nothing is transmitted, there is no account, and nobody is notified &mdash; the site has no backend by design.</p>
    <p>When you are ready, use <strong>Copy decisions</strong> to get a plain-text summary to paste into an instruction. That is the
    hand-off: a person chooses, then the next build acts.</p>
  </div>
  <div class="decide-tools">
    <button type="button" class="btn btn-small" data-action="copy">Copy decisions</button>
    <button type="button" class="btn btn-ghost btn-small" data-action="reset">Clear all</button>
    <p class="decide-count" data-count>0 of {len(live)} decided</p>
  </div>
</div>
<p class="lede-prose">Order matters more than it looks. Two of these are free and unblock the others, one is a recommendation not to do
something, and one is a recommendation to stop. A queue that only ever says yes is not a decision tool.</p>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The queue')}<h2>Awaiting your decision</h2></div>
<p>Read the "depends on" line before approving anything.</p></div>
<div class="scard-list">{''.join(row(s) for s in live)}</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Already done')}<h2>Implemented in this build</h2></div>
<p>Published here so the decision log is complete, not to take credit.</p></div>
<div class="scard-list">{''.join(row(s) for s in done)}</div>''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The whole board on one screen')}<h2>Fifteen rows</h2></div></div>
{tbl}''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Editorial ideas, unpublished')}<h2>Six working titles</h2></div>
<p>Hypotheses about what a reader might search for. No volume, difficulty or traffic figure is attached to any of them, because none exists for this site.</p></div>
{table(['Working title', 'Cluster', 'Why it might earn a read', 'What is missing before it can be written'],
       [[{"html": f"<strong>{esc(a['title'])}</strong>"}, esc(a['cluster']), esc(a['why']), esc(a['missing'])] for a in ARTICLE_IDEAS],
       cls="register", caption="Editorial backlog: not written, not scheduled, not measured",
       note="A title moves out of this table and into the guides only when every sentence in it can be written without inventing a fact.")}
<p class="sec-foot">This is the answer to "what should we publish next": six candidates, and not one of them has evidence behind it yet. <a href="{esc(rel(d, 'questions/index.html'))}#Q-12">Q-12</a> is the question that would change that.</p>''', cls='section-tint')}
{section(f'''
<div class="callout">
  <h2>The two rows worth reading twice</h2>
  <p><strong>S-11</strong> says stop: no new guide topics until either a real test or real search data exists. More synthetic prose
  makes the site bigger, not better, and it raises the chance the whole publication is read as one undifferentiated block. The five
  guides that exist are defensible because they claim little; that advantage survives by not being diluted.</p>
  <p><strong>S-15</strong> is the cheapest thing on the page. Three questions to Amazon's own support channel would settle whether the
  links earn, whether the short links are valid, and whether the ID is active &mdash; the three things no page in this repository can
  answer by itself.</p>
</div>''', cls='')}
"""
    return page(
        d,
        title="Suggestions and decisions \u2014 Crisp & Counter",
        description=("Fifteen proposed changes with cost, risk, evidence and dependencies, each with accept / hold / reject, "
                     "so a path can be chosen before anything is built."),
        body=body,
        active="suggestions/index.html",
        canonical="suggestions/",
        breadcrumb=[("Home", ""), ("Suggestions", "suggestions/")],
    )
