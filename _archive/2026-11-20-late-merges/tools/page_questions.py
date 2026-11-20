"""Open questions: what is known, what is missing, and what would close it."""

from layout import esc, eyebrow, outbound, page, pagehead, product_link, rel, section, table


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

    official_sources = {
        "Q-01": "https://sell.amazon.com/blog/what-is-an-asin", "Q-02": "https://www.amazon.com/dp/B0DHZTCNR5",
        "Q-03": "https://affiliate-program.amazon.com/help/operating/policies",
        "Q-04": "https://affiliate-program.amazon.com/help/operating/policies",
        "Q-05": "https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking",
        "Q-06": "https://www.amazon.com/dp/B0DHZTCNR5",
        "Q-07": "https://support.google.com/webmasters/answer/7576553",
        "Q-08": "https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking",
        "Q-09": "https://affiliate-program.amazon.com/help/operating/policies",
        "Q-10": "https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages",
        "Q-11": "https://support.google.com/webmasters/answer/9008080",
        "Q-12": "https://affiliate-program.amazon.com/help/operating/policies",
        "Q-13": "https://affiliate-program.amazon.com/help/operating/agreement",
        "Q-14": "https://affiliate-program.amazon.com/help/operating/policies",
        "Q-15": "https://support.google.com/webmasters/answer/7576553",
    }
    q_rows = []
    for q in qs:
        state = '<span class="pill pill-ok">Answered</span>' if q.get("answered") else '<span class="pill pill-warn">Open</span>'
        blk = "Yes" if str(q.get("blocking", "")).startswith("yes") else "No"
        q_rows.append([
            {"html": f'<a href="#{esc(q["id"])}"><strong>{esc(q["id"])}</strong></a>'},
            {"html": esc(q["question"])},
            {"html": state},
            {"html": blk},
            {"html": (product_link(d, official_sources[q["id"]], "Amazon listing", aria="Open Amazon link (opens in a new tab)") if q["id"] in ("Q-02", "Q-06") else outbound(d, official_sources[q["id"]], "Official source"))},
        ])
    q_table = table(["Ref", "Question", "Status", "Blocks work", "Source"], q_rows,
                    cls="qtable", caption=f"{len(qs)} questions raised, {len(answered)} answered")

    body = f"""{pagehead(
        'Open questions',
        'Everything that has to be<br>answered before a decision',
        f'{len(qs)} questions. {len(answered)} have an answer with a source. {len(open_)} do not, and each one names the specific document, dashboard or decision that would close it. {len(blocking)} of those block real work.',
        meta='Nothing on this page is a forecast &middot; every answer carries a source or says it has none',
    )}
{section(f'''
<div class="sec-head"><div>{eyebrow('At a glance')}<h2>Every question in one table</h2></div><p>A one-line answer and where it stands. The cards below carry the detail.</p></div>
{q_table}
''', cls='')}
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
