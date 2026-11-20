"""Open questions: what is known, what is missing, and what would close it."""

from layout import esc, eyebrow, outbound, page, pagehead, rel, section, table


def build(page_dir, questions, meta):
    d = page_dir
    qs = questions["questions"]
    answered = [q for q in qs if q.get("answered")]
    open_ = [q for q in qs if not q.get("answered")]
    blocking = [q for q in open_ if str(q.get("blocking", "")).startswith("yes")]

    def card(q, n):
        state = ('<span class="pill pill-ok">Answered</span>' if q.get("answered")
                 else '<span class="pill pill-warn">Open</span>')
        blk = ""
        if str(q.get("blocking", "")).startswith("yes"):
            blk = ' <span class="pill pill-block">Blocks work</span>'
        answer = ""
        if q.get("answered"):
            answer = f'<div class="q-answer"><p class="q-label">Answer</p><p>{esc(q.get("answer", ""))}</p></div>'
        else:
            answer = f"""<div class="q-answer"><p class="q-label">What would close it</p><p>{esc(q.get('how_to_close', ''))}</p></div>"""
        return f"""<article class="qcard" id="{esc(q['id'])}">
  <div class="qcard-top"><span class="q-num">{esc(q['id'])}</span>{state}{blk}</div>
  <h3>{esc(q['question'])}</h3>
  <dl class="q-dl">
    <div><dt>What we have</dt><dd>{esc(q['what_we_have'])}</dd></div>
    <div><dt>What is missing</dt><dd>{esc(q['what_is_missing'])}</dd></div>
  </dl>
  {answer}
</article>"""

    q_rows = []
    for q in qs:
        state = '<span class="pill pill-ok">Answered</span>' if q.get("answered") else '<span class="pill pill-warn">Open</span>'
        blk = "Yes" if str(q.get("blocking", "")).startswith("yes") else "No"
        q_rows.append([
            {"html": f'<a href="#{esc(q["id"])}"><strong>{esc(q["id"])}</strong></a>'},
            {"html": esc(q["question"])},
            {"html": state},
            {"html": blk},
        ])
    count_caption = "%d questions raised, %d answered" % (len(qs), len(answered))
    q_table = table(["Ref", "Question", "Status", "Blocks work"], q_rows,
                    cls="qtable", caption=count_caption)

    # How a missing answer is supposed to be found. This is the part the brief
    # asked for: not just "we do not know", but the discovery route for each gap.
    discovery = [
        ("Ask the account holder", "Attribution, intended ASINs, commission rates and any reported orders. None of these can be observed from outside the Associates account, and no amount of site work substitutes for one look inside it.", "Q-01, Q-03, Q-14, and FLG-002"),
        ("Read the policy text", "Disclosure placement, link markup and whether a price may be shown. These are published and were read directly; where a policy is ambiguous, the ambiguity is quoted rather than resolved by assumption.", "Q-04, Q-05, and SRC-01 to SRC-05"),
        ("Measure a click end to end", "The only test that distinguishes a working Special Link from a link that merely looks like one. One click from the owner's device, then the Associates click report for that day.", "FLG-003, S-01"),
        ("Read a search report", "Topics, demand and whether anyone arrives. Search Console and Bing Webmaster both report queries without a script on the page, which also keeps the site free of third-party code.", "Q-16, S-06, S-07, S-13"),
        ("Do the thing, then write about it", "Testing, photographs and first-hand measurements. Every item here is currently answered with an absence; the only honest way to fill them is to buy, use, measure and photograph, and to say so when the result is unflattering.", "Q-07, S-04, S-12"),
    ]
    discovery_rows = [
        [{"html": "<strong>%s</strong>" % esc(title)}, {"html": esc(body)}, {"html": "<code class=\"code\">%s</code>" % esc(refs)}]
        for title, body, refs in discovery
    ]
    discovery_tbl = table(["Way to find out", "What it settles, and why nothing else does", "Questions and flags"], discovery_rows, cls="discovery")

    body = f"""{pagehead(
        'Before you decide',
        'What has to be answered<br>before any decision',
        f'{len(qs)} questions. {len(answered)} have an answer with a source. {len(open_)} do not, and each one names the specific document, dashboard or decision that would close it. {len(blocking)} of those block real work.',
        meta='Nothing here is a forecast &middot; every answer carries a source, or says it has none',
    )}
{section(f'''
<div class="sec-head"><div>{eyebrow('At a glance')}<h2>Every question in one table</h2></div><p>A one-line answer and where it stands. The cards below carry the detail.</p></div>
{q_table}
''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('How a gap gets closed')}<h2>Five ways to find out, in order of cost</h2></div>
<p>Every open question on this page has at least one of these routes. None of them is "think about it harder", which is why none of the gaps below has been filled by guesswork.</p></div>
{discovery_tbl}''', cls='section-tint')}
{section(f'''
<div class="stat-row">
  <div class="stat"><span class="stat-n">{len(qs)}</span><span class="stat-l">questions raised</span></div>
  <div class="stat"><span class="stat-n">{len(answered)}</span><span class="stat-l">answered with a source</span></div>
  <div class="stat stat-warn"><span class="stat-n">{len(open_)}</span><span class="stat-l">still open</span></div>
  <div class="stat stat-warn"><span class="stat-n">{len(blocking)}</span><span class="stat-l">blocking other work</span></div>
</div>
<p class="lede-prose">The distinction that matters: "we do not know yet" is a finding, and "we assumed" is not. Every open question below has been left open deliberately, and the column that would normally hold a plausible guess instead names the thing that would settle it.</p>''', cls='')}
{section(f'''
{{BLOCKING}}
''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The rest of the list')}<h2>Open, not blocking</h2></div><p>These affect quality, speed or usefulness. None of them affects whether the site is currently accurate.</p></div>
<div class="q-grid">{''.join(card(q, i) for i, q in enumerate([q for q in open_ if not str(q.get('blocking','')).startswith('yes')]))}</div>''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Closed')}<h2>Answered, with the source</h2></div><p>These did not need an account or a dashboard to settle. Two needed the policy text; two are conclusions about what this build actually contains. The evidence column says which is which, so an internal conclusion is never mistaken for a citation.</p></div>
<div class="q-grid">{''.join(card(q, i) for i, q in enumerate(answered))}</div>''', cls='')}
"""
    blocking_html = f"""<div class="sec-head"><div>{eyebrow('Answer these first')}<h2>Blocking questions</h2></div><p>Until one of these is answered, work that depends on it is either guesswork or wasted.</p></div>
<div class="q-grid">{''.join(card(q, i) for i, q in enumerate(blocking))}</div>"""
    body = body.replace("{BLOCKING}", blocking_html)

    return page(
        d,
        title="Open questions \u2014 Crisp & Counter",
        description=f"{len(qs)} questions a buyer-side decision depends on: what is known, what is missing, and the specific artefact that would settle each one.",
        body=body,
        active="questions/index.html",
        canonical="questions/",
    )
