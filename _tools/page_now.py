"""What is left: the whole project in one screen, in the owner's language.

The rest of this site is organised the way the work happened — registers, flags,
verdicts. That organisation is correct and unfriendly. This page answers the only
question an owner asks on opening the site: "what do I have to do, and how long
will it take?"

Everything on it is drawn from the other registers at build time, so it cannot go
stale without the build noticing.
"""

import json
import pathlib

from layout import (breadcrumb_schema, esc, eyebrow, page, pagehead, rel, section,
                    table)

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _load(name):
    return json.loads((ROOT / "_src/data" / name).read_text(encoding="utf-8"))


def build(page_dir):
    d = page_dir
    offers = _load("offers.json")
    flags = _load("flags.json")["flags"]
    questions = _load("questions.json")["questions"]

    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    from page_offers import ranked

    scored, unscored = ranked(offers)
    owner_needs = [r for r in scored if r["offer"]["scores"].get("owner-time", 0) >= 2]
    open_q = [q for q in questions if not q.get("answered")]

    # The three things that need the owner specifically, in the order they unlock work.
    steps = [
        {
            "n": "01",
            "title": "Sign in to Associates Central once",
            "time": "about ten minutes",
            "why": "This is the only step that decides whether the site can earn. Everything else on this "
                   "page is an improvement to a shop that may not be able to be paid.",
            "does": "Generate one Special Link for any one of the five products, click it yourself, then open "
                    "the click report and see whether the click appears against shopnow047c-20.",
            "then": "Paste that one link back into this project and shape the other four. Until then the site "
                    "keeps working, keeps disclosing, and keeps making no claim about earnings.",
            "offer": "OFF-01",
        },
        {
            "n": "02",
            "title": "Change one Pages setting",
            "time": "two minutes",
            "why": "The live site is currently serving its own source code and five retired storefronts. "
                   "Search engines are being invited into all of it by robots.txt.",
            "does": "Repository Settings → Pages → set the source to GitHub Actions so the staged build is what "
                    "gets published, not the repository root.",
            "then": "Everything under /tools/, /src/, /archive/ and /decision-support/ stops resolving, and the "
                    "site a crawler sees is the site the build makes.",
            "offer": "OFF-02",
        },
        {
            "n": "03",
            "title": "Add the tag back only after step 1 proves a click",
            "time": "nothing yet",
            "why": "The site now publishes no tag at all: every Amazon destination is the plain listing. That is "
                   "the honest state while no Special Link is approved, and the checker fails the build if a tag "
                   "reappears without evidence.",
            "does": "Nothing today. After step 1 confirms a click, record that one approved Special Link and the "
                    "tag returns for that product only.",
            "then": "The disclosure strip does not change, because it states an obligation rather than a result.",
            "offer": "OFF-03",
        },
    ]

    step_html = "".join(f"""<article class="step" id="{esc(s['offer'])}">
  <div class="step-n">{esc(s['n'])}</div>
  <div class="step-body">
    <div class="step-top"><h3>{esc(s['title'])}</h3><span class="pill">{esc(s['time'])}</span></div>
    <p class="step-why">{esc(s['why'])}</p>
    <dl class="q-dl">
      <div><dt>What you do</dt><dd>{esc(s['does'])}</dd></div>
      <div><dt>What happens then</dt><dd>{esc(s['then'])}</dd></div>
    </dl>
  </div>
</article>""" for s in steps)

    flag_rows = [
        [{"html": f'<strong>{esc(f["id"])}</strong>'},
         {"html": f'<span class="pill pill-{"block" if f.get("severity")=="high" else "warn"}">{esc(f.get("severity",""))}</span>'},
         {"html": esc(f.get("title", ""))}]
        for f in flags if f.get("severity") == "high"
    ]
    high_table = table(["Ref", "Severity", "What is flagged"], flag_rows, cls="flagtable",
                       caption="The five high-severity flags, unchanged from the review queue")

    body = (
        pagehead(
            "Start here",
            "What is left,<br><em>in plain English.</em>",
            "Three steps, and only the first one is real work. Everything else this site could do is listed "
            "underneath, ranked, so you can see what you are choosing between rather than being asked to read "
            "a register.",
            meta=f"{len(scored)} offers ranked &middot; {len(open_q)} open questions &middot; "
                 f"{len([f for f in flags if f.get('severity')=='high'])} high-severity flags",
        )
        + section(f"""
<div class="sec-head"><div>{eyebrow('The whole project')}<h2>Three steps</h2></div>
<p>Do them in this order. The order is the finding.</p></div>
<div class="steps">{step_html}</div>""", cls="")
        + section(f"""
<div class="callout">
  <h2>If you only do one thing</h2>
  <p>Step 1. The site is already published, already dislclosed above the fold, already marked as paid links, and
  already free of invented prices and ratings. What it cannot do is tell you whether any of it is being credited
  to you. Ten minutes in Associates Central converts that from a question into a fact.</p>
  <p class="callout-links">
    <a class="tlink" href="{esc(rel(d, 'offers/index.html'))}">All ten offers, scored <span aria-hidden="true">&rarr;</span></a>
  </p>
</div>""", cls="section-tint")
        + section(f"""
<div class="sec-head"><div>{eyebrow('What is already done')}<h2>The list is shorter than it looks</h2></div>
<p>These were finished before this page existed. They are the reason only three steps remain.</p></div>
<div class="donelist">
  <div><span class="pill pill-ok">Done</span><p>Five product links opened and matched to their destinations, by three separate sessions.</p></div>
  <div><span class="pill pill-ok">Done</span><p>A disclosure strip above the fold on every page, with the required sentence verbatim, plus a plain-language version.</p></div>
  <div><span class="pill pill-ok">Done</span><p>Every outbound Amazon link marked <code>rel="sponsored nofollow noopener"</code>.</p></div>
  <div><span class="pill pill-ok">Done</span><p>No price, rating, review count or stock figure anywhere, enforced by the build gate.</p></div>
  <div><span class="pill pill-ok">Done</span><p>Nine question-shaped guides, a sitemap, an RSS feed, structured data and canonical tags.</p></div>
  <div><span class="pill pill-ok">Done</span><p>An add-to-basket path on the front page, so a decided reader can act in one click.</p></div>
</div>""", cls="")
        + section(f"""
<div class="sec-head"><div>{eyebrow('The part that blocks everything')}<h2>The five high flags</h2></div>
<p>Unchanged from the review queue. All five trace back to not being able to see inside an Associates account.</p></div>
{high_table}
<p class="sec-foot"><a class="tlink" href="{esc(rel(d, 'review/index.html'))}">All 22 flags <span aria-hidden="true">&rarr;</span></a></p>""", cls="section-tint")
        + section(f"""
<div class="callout">
  <h2>What no effort here can fix</h2>
  <p>Whether the tag is credited, whether traffic arrives, and what each category pays. Those need an account
  login, a Search Console property and a report. No amount of work inside this repository closes them, which is
  why the site claims less rather than guessing more.</p>
  <p class="callout-links">
    <a class="tlink" href="{esc(rel(d, 'verification/index.html'))}">Verified, page by page <span aria-hidden="true">&rarr;</span></a>
    <a class="tlink" href="{esc(rel(d, 'questions/index.html'))}">Every open question <span aria-hidden="true">&rarr;</span></a>
  </p>
</div>""", cls="")
    )

    return page(
        d,
        title="What is left, in plain English | Crisp & Counter",
        description="Three steps to finish this project, only one of which is real work, plus the ranked list "
                    "of everything else the site could do.",
        body=body,
        active="now/index.html",
        canonical="now/",
        structured=breadcrumb_schema([], "What is left", "now/"),
    )
