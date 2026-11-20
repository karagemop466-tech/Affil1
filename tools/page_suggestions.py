"""The suggestion queue: proposals a reviewer can accept or reject one at a time."""

from layout import esc, eyebrow, outbound, page, pagehead, rel, section, table


def build(page_dir, suggestions, meta):
    d = page_dir
    items = suggestions["suggestions"]
    recommended = [s for s in items if s["id"] in ("S-01", "S-02", "S-03")]
    proposed = [s for s in items if s.get("status") != "implemented"]
    shipped = [s for s in items if s.get("status") == "implemented"]

    rows = []
    for s in items:
        dep = s["depends_on"] if s["depends_on"] != "nothing" else '<span class="tiny">nothing</span>'
        state = ('<span class="pill pill-ok">Implemented</span>' if s.get("status") == "implemented"
                 else '<span class="pill pill-warn">Proposed</span>')
        rows.append([
            {"html": '<a href="#%s"><strong>%s</strong></a>' % (esc(s["id"]), esc(s["id"]))},
            {"html": esc(s["title"])},
            {"html": esc(s["recommendation"])},
            {"html": esc(s["effort"])},
            {"html": esc(s["risk"])},
            {"html": dep},
            {"html": state},
        ])
    queue_table = table(
        ["Ref", "Proposal", "Recommendation", "Effort", "Risk", "Depends on", "State"],
        rows, cls="queue",
        caption="%d proposals, ordered by what they unlock" % len(items),
        note="Depends-on is the column that matters. A proposal depending on an unanswered question cannot be evaluated until that question is answered, however cheap it looks.",
    )

    path = [
        ("1", "Tag and check the links", "S-14", "Without a tracked link, everything downstream measures nothing. It is done and enforced by the build."),
        ("2", "Confirm one click in the Associates report", "S-01", "The only permitted source of truth for attribution. One click answers what no amount of site work can."),
        ("3", "Get the site into two indexes", "S-07, S-13", "Search Console and Bing both accept a sitemap and report queries without adding a script to the page."),
        ("4", "Name the editor, honestly", "S-03", "The cheapest credibility available, provided the biography describes work that actually happened."),
        ("5", "Then, and only then, commission more guides", "S-06, S-11", "New topics should come from measured queries, not from another round of guesses."),
    ]
    path_html = ""
    for n, title, refs, why in path:
        path_html += ('<li><span class="step-n">%s</span><div><h3>%s</h3><p>%s</p>'
                      '<p class="step-refs">%s</p></div></li>') % (n, esc(title), esc(why), esc(refs))

    def shipped_row(s, d):
        src = ""
        if s.get("source"):
            src = '<p class="tiny">Source: <a href="%s" target="_blank" rel="noopener">%s</a></p>' % (
                esc(s["source"]), esc(s.get("source_label") or s["source"]))
        return ('<article class="ship" id="%s"><div class="ship-head"><span class="scard-id">%s</span>'
                '<span class="pill pill-ok">Implemented</span></div><h3>%s</h3><p>%s</p>'
                '<p class="tiny"><strong>Risk:</strong> %s</p>%s</article>') % (
            esc(s['id']), esc(s['id']), esc(s['title']), esc(s['why']), esc(s['risk']), src)

    def row(s, n):
        return f"""<article class="scard" id="{esc(s['id'])}">
  <div class="scard-head">
    <span class="scard-id">{esc(s['id'])}</span>
    <h3>{esc(s['title'])}</h3>
    <span class="scard-effort">{esc(s['effort'])}</span>
  </div>
  <div class="scard-body">
    <div class="scard-why"><p class="q-label">Why</p><p>{esc(s['why'])}</p></div>
    <dl class="scard-meta">
      <div><dt>Risk</dt><dd>{esc(s['risk'])}</dd></div>
      <div><dt>Depends on</dt><dd>{esc(s['depends_on'])}</dd></div>
      <div><dt>Recommendation</dt><dd class="rec">{esc(s['recommendation'])}</dd></div>
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

    body = f"""{pagehead(
        'Suggestions',
        'Twelve proposals,<br>one decision each',
        'Each row says what it would change, what it costs, what could go wrong, and which open question has to be answered before it makes sense to approve. Nothing here has been implemented.',
        meta='Nothing on this page changes the site &middot; decisions are stored in your browser only, never sent anywhere',
    )}
{section(f'''
{queue_table}''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('If you only do five things')}<h2>An order that holds up</h2></div>
<p>Each step makes the next one cheaper. Skipping step two means steps three to five are measuring a channel that may not pay.</p></div>
<ol class="path-list">{path_html}</ol>''', cls='section-tint')}
{section(f'''
<div class="decide-intro">
  <div>
    <h2>How to use this page</h2>
    <p>Work down the list and mark each row. The buttons record your decision in this browser's own storage so you can come back to it. Nothing is transmitted, there is no account, and no one is notified &mdash; the site has no backend by design.</p>
    <p>When you are ready, use <strong>Copy decisions</strong> to get a plain-text summary you can paste into a message. That is the hand-off: a human deciding, then instructing.</p>
  </div>
  <div class="decide-tools">
    <button type="button" class="btn btn-small" data-action="copy">Copy decisions</button>
    <button type="button" class="btn btn-ghost btn-small" data-action="reset">Clear all</button>
    <p class="decide-count" data-count>0 of {len(items)} decided</p>
  </div>
</div>
<p class="lede-prose">Order matters more than it looks. Two of these are free and unblock the others, and one of them is a recommendation not to do something. That last one is included because a suggestion queue that only ever says yes is not a decision tool.</p>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Start here')}<h2>The first three</h2></div><p>Cheap, reversible, and they make the later items worth doing.</p></div>
{''.join(row(s, i) for i, s in enumerate(recommended))}''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The full queue')}<h2>Everything else</h2></div><p>Ordered by what they unlock, not by size.</p></div>
{''.join(row(s, i) for i, s in enumerate([x for x in proposed if x['id'] not in ('S-01','S-02','S-03')]))}''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Already shipped')}<h2>Done in the latest pass, with a source</h2></div>
<p>Recorded rather than deleted, so the queue keeps a history of what was decided and built.</p></div>
{''.join(shipped_row(s, d) for s in shipped)}''', cls='section-tint')}
{section(f'''
<div class="callout">
  <h2>The one recommendation to read twice</h2>
  <p>Everything else on this page adds something. S-11 says stop: do not commission more AI-written guides until either a real test or real search data exists. More synthetic prose makes the site bigger, not better, and it raises the chance the whole publication is treated as one undifferentiated block.</p>
  <p>The four guides that exist are defensible because they claim little. That is a narrow advantage, and it survives by not being diluted.</p>
</div>''', cls='')}"""
    return page(
        d,
        title="Suggestions \u2014 Crisp & Counter",
        description="Twelve proposed changes to this site, each with its cost, its risk and the open question it depends on \u2014 with a decision control for each so a reviewer can choose a path before anything is built.",
        body=body,
        active="suggestions/index.html",
        canonical="suggestions/",
    )
