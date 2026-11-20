"""The question register: what is known, what is missing, and who holds it."""

from layout import cite_or_product, esc, eyebrow, page, pagehead, rel, section, table
from content import CLUSTERS


def _evidence(links):
    if not links:
        return ""
    items = "".join(
        f'<li>{cite_or_product(None, l["url"], l["label"])}</li>' for l in links
    )
    return f'<ul class="evidence">{items}</ul>'


def build(page_dir, questions, meta):
    d = page_dir
    qs = questions["questions"]
    answered = [q for q in qs if q.get("answered")]
    openq = [q for q in qs if not q.get("answered")]
    blocking = [q for q in openq if str(q.get("blocking", "")).startswith("yes")]

    def card(q):
        if q.get("answered"):
            state = '<span class="pill pill-ok">Answered</span>'
            body = f'''<div class="q-answer"><p class="q-label">Answer</p><p>{esc(q.get("answer", ""))}</p>{_evidence(q.get("evidence"))}</div>'''
        else:
            state = '<span class="pill pill-warn">Open</span>'
            body = f'''<div class="q-answer"><p class="q-label">What would close it</p>
      <p>{esc(q.get("how_to_close", ""))}</p>
      <p class="q-owner">Held by: {esc(q.get("owner") or "unknown")}</p></div>'''
        return f'''<article class="qcard" id="{esc(q['id'])}">
  <div class="qcard-top"><span class="q-num">{esc(q['id'])}</span>{state}</div>
  <h3>{esc(q['question'])}</h3>
  <p class="q-short">{esc(q.get('short') or '')}</p>
  <dl class="q-dl">
    <div><dt>What we have</dt><dd>{esc(q['what_we_have'])}</dd></div>
    <div><dt>What is missing</dt><dd>{esc(q['what_is_missing'])}</dd></div>
  </dl>
  {body}
</article>'''

    info_rows = []
    for q in qs:
        status = ('<span class="pill pill-ok">Answered</span>' if q.get("answered")
                  else ('<span class="pill pill-block">Blocking</span>' if str(q.get("blocking", "")).startswith("yes")
                        else '<span class="pill pill-warn">Open</span>'))
        info_rows.append([
            {"html": f'<a href="#{esc(q["id"])}"><strong>{esc(q["id"])}</strong></a>'},
            {"html": esc(q["question"])},
            {"html": esc(q.get("what_is_missing") or "nothing")},
            {"html": esc(q.get("owner") or "")},
            {"html": status},
        ])
    info_tbl = table(["Ref", "Question", "Information needed", "Who holds it", "Status"], info_rows,
                     cls="register", caption="The information register: sixteen questions and the missing piece for each")

    buyer = "".join(f'''<a class="path" href="{esc(rel(d, 'guides/' + c['slug'] + '.html'))}">
    <h3>{esc(c['question'])}</h3>
    <p>{esc(c['dek'])}</p>
    <span class="tlink">The guide answers this <span aria-hidden="true">&rarr;</span></span></a>''' for c in CLUSTERS)

    body = f"""{pagehead(
        'Open questions',
        'What has to be settled<br>before the next move',
        f'{len(qs)} questions. {len(answered)} have an answer with a source in this repository. {len(openq)} do not, and each one names '
        'the document, dashboard or decision that would close it.',
        meta='No forecasts &middot; no estimated values &middot; "unknown" is recorded as unknown',
    )}
{section(f'''
<div class="stat-row">
  <div class="stat"><span class="stat-n">{len(qs)}</span><span class="stat-l">questions raised</span></div>
  <div class="stat"><span class="stat-n">{len(answered)}</span><span class="stat-l">answered with a source</span></div>
  <div class="stat stat-warn"><span class="stat-n">{len(openq)}</span><span class="stat-l">still open</span></div>
  <div class="stat stat-warn"><span class="stat-n">{len(blocking)}</span><span class="stat-l">holding up other work</span></div>
</div>
<div class="lede-prose">
  <p>Three kinds of question are mixed in a decision: what a policy actually requires, what the account actually says, and what a
  reader actually wants. The first kind can be answered by reading a published document, and this build answered six of them that
  way. The second needs access only the account owner has. The third needs either measurement or a conversation.</p>
  <p>Nothing here is padded with a plausible guess. Where the answer needs a dashboard, the row says which dashboard.</p>
</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The information register')}<h2>Every question and the missing piece</h2></div>
<p>This is the table to work down if you have an hour and the accounts. Each row closes with one export or one screenshot.</p></div>
{info_tbl}''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Answer these first')}<h2>Blocking questions</h2></div>
<p>Until one of these is settled, work that depends on it is either guesswork or wasted.</p></div>
<div class="q-grid">{''.join(card(q) for q in blocking)}</div>''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Open, not blocking')}<h2>The rest of the list</h2></div>
<p>These affect quality, speed or earning power. None of them affects whether the site is currently accurate.</p></div>
<div class="q-grid">{''.join(card(q) for q in openq if q not in blocking)}</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Closed')}<h2>Answered, with the source</h2></div>
<p>Each of these was settled by reading a published document, or by stating what this build itself did. The evidence column says which.</p></div>
<div class="q-grid">{''.join(card(q) for q in answered)}</div>''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow("The reader's questions")}<h2>What this site can answer without any account</h2></div>
<p>The buyer-side questions do not need a dashboard. They are answered in the guides, as checklists.</p></div>
<div class="path-grid">{buyer}</div>''', cls='')}
{section(f'''
<div class="callout">
  <h2>Five ways to find the missing information</h2>
  <p>Each of these produces a fact this site currently does not have. All five are free, and four of them are faster than writing
  another article.</p>
  <ol class="tight">
    <li><strong>Ask Amazon in writing.</strong> Whether the short links are Special Links, what a valid tag looks like, and whether the ID
    is active, are three answerable questions for the programme's own support channel.</li>
    <li><strong>Verify Search Console and wait 28 days.</strong> Impressions by query is the only honest substitute for the volume data
    this site does not have.</li>
    <li><strong>Watch one click land in the report.</strong> A single tagged click settles whether the machinery works end to end.</li>
    <li><strong>Ask five readers one question:</strong> "what did you nearly buy, and what stopped you?" Five answers beat any keyword tool
    for knowing which guide to write next.</li>
    <li><strong>Read the manual for one product.</strong> Dimensions, wattage and care instructions are the facts most often missing from a
    listing title, and the manufacturer publishes them.</li>
  </ol>
</div>''', cls='')}
"""
    return page(
        d,
        title="Open questions and the information register | Crisp & Counter",
        description=(f"{len(qs)} questions the next decision depends on: what is known with a source, what is missing, who holds "
                     "it, and the specific export or document that would close each one."),
        body=body,
        active="questions/index.html",
        canonical="questions/",
        breadcrumb=[("Home", ""), ("Questions", "questions/")],
    )
