"""The offer page: a scored list a reviewer can actually choose from.

The problem this page fixes is not a shortage of ideas. The repository already has
three registers of them. The problem is that none of them answers "which one
first", so a reader has to hold twenty rows in their head and compare prose.

Here every candidate is scored against the same six factors, the arithmetic is
shown, and the reviewer can change a weight and see the order move. That is a
decision surface rather than a to-do list.

Run `python3 _tools/page_offers.py --check` to print the arithmetic without
building a page. It is the same function the page uses, so the numbers on the page
cannot drift from the numbers in the terminal.
"""

import json
import pathlib
import sys

from layout import (breadcrumb_schema, esc, eyebrow, page, pagehead, rel, section,
                    table)

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load():
    return json.loads((ROOT / "_src/data/offers.json").read_text(encoding="utf-8"))


def score(offer, factors):
    """Weighted sum. Inverted factors score (3 - raw) so a low cost is good."""
    total, used, missing = 0.0, [], []
    for f in factors:
        raw = offer["scores"].get(f["id"])
        if raw == "needs":
            missing.append(f["id"])
            continue
        value = (3 - raw) if f.get("inverted") else raw
        total += value * f["weight"]
        used.append(f"{f['id']}={(3 - raw) if f.get('inverted') else raw}x{f['weight']}")
    return total, used, missing


def ranked(doc):
    factors = doc["factors"]
    rows = []
    for o in doc["offers"]:
        total, used, missing = score(o, factors)
        rows.append({"offer": o, "total": total, "used": used, "missing": missing})
    scored = [r for r in rows if not r["missing"]]
    unscored = [r for r in rows if r["missing"]]
    scored.sort(key=lambda r: -r["total"])
    return scored, unscored


def check():
    doc = load()
    scored, unscored = ranked(doc)
    max_possible = sum(f["weight"] * 3 for f in doc["factors"])
    print(f"factors: {len(doc['factors'])}  max possible score: {max_possible}")
    print()
    for r in scored:
        o = r["offer"]
        print(f"{o['id']}  {r['total']:>4.0f}  {o['title']}")
        print(f"        {' + '.join(r['used'])}")
    if unscored:
        print()
        for r in unscored:
            print(f"{r['offer']['id']}  NEEDS   {r['offer']['title']}")
            print(f"        unscored until: {', '.join(r['missing'])}")
    return 0


def _factor_cells(offer, factors):
    cells = []
    for f in factors:
        raw = offer["scores"].get(f["id"])
        if raw == "needs":
            cells.append({"html": '<span class="blank" title="depends on data this repository does not hold">?</span>'})
        else:
            kind = "pill-ok" if raw >= 2 else ("pill-warn" if raw == 1 else "pill-none")
            cells.append({"html": f'<span class="pill {kind}">{raw}</span>'})
    return cells


def build(page_dir, meta=None):
    d = page_dir
    doc = load()
    factors = doc["factors"]
    scored, unscored = ranked(doc)
    max_possible = sum(f["weight"] * 3 for f in factors)

    headers = ["Offer", "What it is"] + [f["label"] for f in factors] + ["Score"]
    rows = []
    for r in scored:
        o = r["offer"]
        rows.append(
            [{"html": f'<strong>{esc(o["id"])}</strong>'}, {"html": esc(o["one_line"])}]
            + _factor_cells(o, factors)
            + [{"html": f'<strong>{r["total"]:.0f}</strong>'}]
        )
    score_table = table(
        headers, rows, cls="offertable",
        caption=f"{len(scored)} offers scored out of {max_possible:.0f} possible",
        note="A ? means the factor depends on a fact this repository does not hold, so the offer is "
             "held out of the ranking rather than scored as zero. Weights are judgements, not measurements.",
    )

    factor_rows = [
        [{"html": f'<strong>{esc(f["label"])}</strong>'},
         {"html": f'<span class="pill">{f["weight"]}</span>'},
         {"html": esc(f["question"])}]
        for f in factors
    ]
    factor_table = table(["Factor", "Weight", "What it asks"], factor_rows, cls="factortable",
                         caption="How the score is built")

    def card(r, *, unscored=False):
        o = r["offer"]
        total = ('<span class="pill pill-warn">Needs data</span>' if unscored
                 else f'<span class="pill pill-ok">Score {r["total"]:.0f}</span>')
        ev = ""
        if o.get("evidence_url"):
            ev = (f'<p class="offer-ev"><a rel="noopener" target="_blank" href="{esc(o["evidence_url"])}">'
                  f'Check the source &nearr;</a></p>')
        else:
            ev = '<p class="offer-ev offer-ev-none">No single document settles this one; it rests on the observation recorded on this page.</p>'
        return f"""<article class="offer-card" id="{esc(o['id'])}">
  <div class="offer-top"><span class="offer-id">{esc(o['id'])}</span>{total}</div>
  <h3>{esc(o['title'])}</h3>
  <p class="offer-lede">{esc(o['one_line'])}</p>
  <dl class="q-dl">
    <div><dt>What changes</dt><dd>{esc(o['what_changes'])}</dd></div>
    <div><dt>Why this rests on evidence</dt><dd>{esc(o['evidence_for'])}</dd></div>
    <div><dt>What the owner does</dt><dd>{esc(o['owner_does'])}</dd></div>
    <div><dt>If it goes wrong</dt><dd>{esc(o['if_it_fails'])}</dd></div>
    <div><dt>What it unlocks</dt><dd>{esc(o['blocks'])}</dd></div>
  </dl>
  {ev}
  <div class="offer-choose">
    <button type="button" class="btn btn-small offer-pick" data-offer="{esc(o['id'])}">Choose this</button>
    <span class="offer-picked" aria-live="polite"></span>
  </div>
</article>"""

    cards = "".join(card(r) for r in scored)
    unscored_html = ""
    if unscored:
        unscored_html = section(f"""
<div class="sec-head"><div>{eyebrow('Held back')}<h2>Not scored until a fact exists</h2></div>
<p>A zero would be a lie here. These are unknown, not worthless.</p></div>
<div class="offer-grid">{''.join(card(r, unscored=True) for r in unscored)}</div>""",
                                cls="section-tint")

    path_cards = []
    for p in doc["paths"]:
        ids = ", ".join(p["offers"])
        path_cards.append(f"""<article class="path-card">
  <p class="path-id">{esc(p['id'])}</p>
  <h3>{esc(p['name'])}</h3>
  <p class="path-sum">{esc(p['summary'])}</p>
  <p class="path-why">{esc(p['why'])}</p>
  <p class="path-meta"><strong>Offers:</strong> {esc(ids)}<br><strong>Cost:</strong> {esc(p['cost'])}</p>
  <button type="button" class="btn btn-small offer-pick" data-path="{esc(p['id'])}">Take this path</button>
</article>""")
    paths_html = section(f"""
<div class="sec-head"><div>{eyebrow('Three directions')}<h2>Pick a path, then pick rows</h2></div>
<p>Individually sensible, collectively contradictory. The paths exist so the choice is one decision, not ten.</p></div>
<div class="path-grid3">{''.join(path_cards)}</div>""", cls="")

    top = scored[0]
    callout = section(f"""
<div class="callout">
  <h2>The arithmetic says start with {esc(top['offer']['id'])}</h2>
  <p><strong>{esc(top['offer']['title'])}.</strong> {esc(top['offer']['one_line'])}</p>
  <p>It scores highest on the heaviest factor and ties the maximum on the second, which is why the
  order puts it first. It also costs more owner time than anything else here, which is exactly why it
  has not happened yet — and why nothing else moves far until it does.</p>
  <p class="callout-links"><a class="tlink" href="#{esc(top['offer']['id'])}">Read that offer <span aria-hidden="true">&rarr;</span></a></p>
</div>""", cls="")

    body = (
        pagehead(
            "Offers · decision surface",
            "Ten changes,<br><em>scored and ranked.</em>",
            "Every candidate change scored on the same six factors, with the arithmetic shown. "
            + (f"{len(scored)} are ranked; {len(unscored)} are held back because a fact is missing."
               if unscored else
               f"All {len(scored)} are ranked. Nothing is held back, because every factor now has a value "
               "this repository can actually see.")
            + " Change a weight in your head and the order moves — that is the point.",
            meta="Weights are judgements &middot; scores are arithmetic &middot; no revenue forecast",
        )
        + section(f"""
<div class="sec-head"><div>{eyebrow('The board')}<h2>Everything, ranked</h2></div>
<p>Scan the score column. The cards below say what each one costs.</p></div>
{score_table}
{factor_table}""", cls="")
        + callout
        + section(f"""
<div class="sec-head"><div>{eyebrow('The offers')}<h2>What each one actually changes</h2></div>
<p>Read 'what the owner does' first. That column is usually the reason a row is still open.</p></div>
<div class="offer-grid">{cards}</div>""", cls="")
        + paths_html
        + unscored_html
        + section(f"""
<div class="callout">
  <h2>What this page cannot decide</h2>
  <p>Whether any of it earns. That is OFF-01, and it needs a login this repository does not have.
  Everything else on this page is sequenced around that single unknown.</p>
  <p class="callout-links">
    <a class="tlink" href="{esc(rel(d, 'verification/index.html'))}">What is verified, and what is not <span aria-hidden="true">&rarr;</span></a>
    <a class="tlink" href="{esc(rel(d, 'questions/index.html'))}">The open questions <span aria-hidden="true">&rarr;</span></a>
  </p>
</div>""", cls="")
    )

    return page(
        d,
        title="Offers, scored and ranked | Crisp & Counter",
        description="Ten candidate changes scored against six weighted factors, with the arithmetic shown: "
                    "what unblocks money, what removes an unprovable claim, and what each one costs the owner.",
        body=body,
        active="offers/index.html",
        canonical="offers/",
        structured=breadcrumb_schema([], "Offers", "offers/"),
    )


if __name__ == "__main__":
    if "--check" in sys.argv:
        raise SystemExit(check())
    print(build("offers"))
