"""The suggestion queue: paths, proposals, and a decision control per row.

Nothing here is implemented by pressing a button. The buttons record a choice in
the reader's own browser, which can then be copied out as text. The point is that
the owner can choose a path before anything changes.
"""

from release_panels import render as release_panel

from layout import esc, eyebrow, page, pagehead, rel, section

PATHS_CLASS = {"PATH-A": "path-card", "PATH-B": "path-card", "PATH-C": "path-card"}


def _row(s):
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
    <span class="decide-label">Your decision</span>
    <button type="button" class="decide" data-decision="accept" aria-pressed="false">Accept</button>
    <button type="button" class="decide" data-decision="hold" aria-pressed="false">Hold</button>
    <button type="button" class="decide" data-decision="reject" aria-pressed="false">Reject</button>
    <span class="decide-note" data-note>Undecided</span>
  </div>
</article>"""


def build(page_dir, suggestions, meta):
    d = page_dir
    items = suggestions["suggestions"]
    open_items = [s for s in items if s.get("status") != "implemented"]
    done = [s for s in items if s.get("status") == "implemented"]
    paths = suggestions.get("paths", [])
    rec = suggestions.get("meta", {}).get("recommended_path", {})

    def _path_row(p):
        rec_cell = ""
        if rec.get("path") == p.get("id"):
            rec_cell = ' <span class="pill pill-ok">Recommended</span>'
        return f"""<tr>
  <td><strong>{esc(p['id'])}</strong> · {esc(p['name'])}{rec_cell}</td>
  <td>{esc(p.get('verdict', ''))}</td>
  <td>{esc(p.get('first_moves', p.get('needs', '')))}</td>
  <td>{esc(p.get('good_if', ''))}</td>
</tr>"""

    choice_table = f"""<div class="table-scroll"><table class="register">
<thead><tr><th scope="col">Path</th><th scope="col">Verdict</th><th scope="col">First moves</th><th scope="col">Good if</th></tr></thead>
<tbody>{"".join(_path_row(p) for p in paths)}</tbody></table></div>"""

    path_cards = "".join(f"""<article class="path-card">
  <p class="scard-id">{esc(p['id'])}</p>
  <h3>{esc(p['name'])}</h3>
  <p class="path-summary">{esc(p['summary'])}</p>
  <dl class="scard-meta">
    <div><dt>Needs</dt><dd>{esc(p['needs'])}</dd></div>
    <div><dt>Before you choose</dt><dd>{esc(p['before_you_choose'])}</dd></div>
    <div><dt>Good if</dt><dd>{esc(p['good_if'])}</dd></div>
  </dl>
</article>""" for p in paths)

    done_rows = "".join(f"""<tr>
  <td><strong>{esc(s['id'])}</strong></td>
  <td>{esc(s['title'])}</td>
  <td>{esc(s.get('implemented_on', ''))}</td>
  <td>{esc(s.get('evidence', ''))}</td>
</tr>""" for s in done)

    body = f"""{pagehead(
        'Suggestions',
        'Choose a direction,<br>then choose the rows',
        f'{len(paths)} coherent paths and {len(open_items)} individual proposals. Each proposal says what it changes, what it costs, what could go wrong, and which open question has to be answered before it makes sense to approve. Nothing here has been implemented by pressing a button.',
        meta='Decisions are stored in your browser only &middot; nothing transmitted &middot; no account',
    )}
{section(f'''
<div class="decide-intro">
  <div>
    <h2>Read this first</h2>
    <p>The rows below are individually sensible and collectively contradictory. Product photography is pointless without an author; a publishing cadence is pointless without a name behind it; analytics is pointless if nobody reads the report. That is why the three paths come before the queue.</p>
    <p>Pick one path, then read only the rows it needs. Everything else can wait without the site getting worse.</p>
  </div>
  <div class="decide-tools">
    <button type="button" class="btn btn-small" data-action="copy">Copy decisions</button>
    <button type="button" class="btn btn-ghost btn-small" data-action="reset">Clear all</button>
    <p class="decide-count" data-count>0 of {len(open_items)} decided</p>
  </div>
</div>''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Three ways forward')}<h2>Pick a path, not a pile</h2></div>
<p>Each path needs a different set of rows. Choosing one is the decision this page exists for — and nothing is implemented until you choose.</p></div>
<div class="callout"><h2>The best path first: {esc(rec.get('name', ''))} ({esc(rec.get('path', ''))})</h2>
<p>{esc(rec.get('why', ''))}</p>
<p><strong>If you can only do one thing:</strong> {esc(rec.get('if_you_can_only_do_one_thing', ''))}</p>
<p>{esc(rec.get('review_note', ''))}</p></div>
{choice_table}
<div class="path-grid paths-three">{path_cards}</div>''', cls='section-tint')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The queue')}<h2>Open proposals</h2></div>
<p>Ordered so the cheap, unblocking rows come first.</p></div>
{"".join(_row(s) for s in open_items)}''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('Already done')}<h2>Implemented on 20 November 2026</h2></div>
<p>Kept visible, with evidence, so the record of what changed is not only a commit log.</p></div>
<div class="table-scroll"><table class="register">
<thead><tr><th scope="col">Ref</th><th scope="col">Change</th><th scope="col">Date</th><th scope="col">Evidence</th></tr></thead>
<tbody>{done_rows}</tbody></table></div>
<p class="table-note">An implemented row is not a suggestion any more. It is here because the owner should be able to see what changed without reading the repository.</p>''', cls='section-tint')}
{section(f'''
<div class="callout">
  <h2>The one recommendation to read twice</h2>
  <p>Everything else on this page adds something. S-07 says stop: beyond the seasonal edit the operator asked for on 20 November, do not commission more guides until either a real test or real search data exists. More synthetic prose makes the publication bigger, not better, and it raises the chance the whole site is treated as one undifferentiated block.</p>
  <p>Seventeen guides now exist: ten general, three from the parallel journal pass, and the four the operator's seasonal brief asked for on 20 November. They are defensible because they claim little. That is a narrow advantage, and it survives by not being diluted.</p>
</div>''', cls='')}"""
    return page(
        d,
        title="Suggestions and decisions | Crisp & Counter",
        description=f"{len(open_items)} proposed changes with cost, risk and the question each depends on, grouped into three paths a reviewer can choose between before anything is built.",
        body=body + release_panel(d, "suggestions/"),
        active="suggestions/index.html",
        canonical="suggestions/",
        structured={"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://karagemop466-tech.github.io/Affil1/"},
            {"@type": "ListItem", "position": 2, "name": "Suggestions", "item": "https://karagemop466-tech.github.io/Affil1/suggestions/"},
        ]},
    )
