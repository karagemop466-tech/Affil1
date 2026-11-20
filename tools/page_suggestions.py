"""The suggestion queue: proposals a reviewer can accept or reject one at a time."""

from layout import esc, eyebrow, page, pagehead, rel, section


def build(page_dir, suggestions, meta):
    d = page_dir
    items = suggestions["suggestions"]
    recommended = [s for s in items if s["id"] in ("S-01", "S-02", "S-03")]

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
{''.join(row(s, i) for i, s in enumerate([x for x in items if x['id'] not in ('S-01','S-02','S-03')]))}''', cls='')}
{section(f'''
<div class="callout">
  <h2>A brief for the next issue</h2>
  <p><strong>Proposed follow-up:</strong> “Will my quarter-sheet pan fit behind French doors?” Start with the dish the reader wants to cook. Compare the width of their pan with the model’s usable rack or basket dimensions. If neither the listing nor the manual supplies that measurement, say so; a quart figure is not a substitute.</p>
  <p><strong>Design prompt:</strong> Use a single annotated format illustration, a two-column fit checklist, and a link to the model record beside the decision. Label the illustration. Don’t add a medal, sale price, star score or invented test result.</p>
  <p><strong>Decision gate:</strong> This is a seasonal hypothesis, not a trend. Review the verified property’s <a href="https://support.google.com/webmasters/answer/7576553">query report</a> monthly. Commission the piece only if a query or a documented reader question supports it and a primary source can answer it. Otherwise revise an existing guide.</p>
</div>''', cls='')}"""
    return page(
        d,
        title="Suggestions \u2014 Crisp & Counter",
        description="Twelve proposed changes to this site, each with its cost, its risk and the open question it depends on \u2014 with a decision control for each so a reviewer can choose a path before anything is built.",
        body=body,
        active="suggestions/index.html",
        canonical="suggestions/",
    )
