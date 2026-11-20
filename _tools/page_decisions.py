"""The decision registry: every open proposal, its source, its blocker, and a
recorded decision.

Why this page exists. The owner asked for "a clear list of questions,
information and answers that need to be addressed before any decision can be
reasonably made", and for suggestions to be reviewable before implementation.
The site already had a suggestions queue and an open-questions page, but a
reviewer could not see, in one place, which item was blocked by which missing
fact, who owns closing it, and what the last recorded decision was.

So each row here carries five things and no more:

  * the proposal and what it changes;
  * the official source that makes it safe or unsafe to act on;
  * the one missing fact that blocks a decision, or "none" if nothing blocks it;
  * the owner who has to close that missing fact;
  * a decision control that records accept / hold / reject in the reader's own
    browser.

Nothing here is implemented by pressing a button. The buttons write to
localStorage and can be copied out as text. That is deliberate: a decision about
what a publication does needs a person, not a build step.
"""

import json
import pathlib

from layout import esc, eyebrow, page, pagehead, rel, section

DATA = pathlib.Path(__file__).resolve().parent.parent / "_src" / "data"

# Official documents each proposal is checked against. A row may only cite a
# document that is actually loadable and that says what the row claims.
SOURCES = {
    "amazon-policies": ("Amazon Associates Program Policies",
                        "https://affiliate-program.amazon.com/help/operating/policies"),
    "amazon-agreement": ("Amazon Associates Operating Agreement",
                         "https://affiliate-program.amazon.com/help/operating/agreement"),
    "ftc-faq": ("FTC Endorsement Guides FAQ",
                "https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking"),
    "google-outbound": ("Google: qualify your outbound links",
                        "https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links"),
    "google-query": ("Google Search Console: query report",
                     "https://support.google.com/webmasters/answer/7576553"),
    "pages-limits": ("GitHub Pages usage limits",
                     "https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits"),
}

# Each row: id, proposal, source key, the missing fact, its owner, and whether
# acting now would break a rule this build enforces.
ROWS = [
    {"id": "D-01",
     "proposal": "Put the Associates tag on the five buy links now, so the site starts earning immediately.",
     "changes": "Every outbound product URL.",
     "source": "amazon-policies",
     "quote": "Participation Requirements 2(a)\u20132(b): Special Links must use your Associates ID as a URL parameter, and must be the links your account issued.",
     "missing": "An account-generated Special Link, per ASIN, from SiteStripe or the Associates dashboard.",
     "owner": "Account owner (needs the Associates login).",
     "blocked": "Yes. The tag can only be attached to a link the account issued. Tagging a URL rebuilt from a redirect observation would be a link the site invented.",
     "verdict": "Not until the account confirms each ASIN."},
    {"id": "D-02",
     "proposal": "Show price, star rating and review count on the cards and in the comparison table.",
     "changes": "The product cards, the compare table and the registry table.",
     "source": "amazon-policies",
     "quote": "Participation Requirements 2(b): a site may show prices and availability only where Amazon serves the link carrying that data, or where it arrives via the Creators API or the PA API.",
     "missing": "Either a Special Link that renders Amazon's own price widget, or Creators/PA API credentials and the qualifying-sales history those APIs require.",
     "owner": "Account owner; the API path also needs the sales history.",
     "blocked": "Yes. A static page has no permitted source for the number.",
     "verdict": "Keep linking to the live listing. The price cells now do that explicitly."},
    {"id": "D-03",
     "proposal": "Replace the illustrations with photographs of the actual products.",
     "changes": "Every image asset and its caption.",
     "source": "amazon-policies",
     "quote": "The IP License and Usage Requirements govern use of Amazon product imagery; the Program Policies incorporate them by reference.",
     "missing": "Either the operator's own photographs of units actually bought, or a documented licence for each image used.",
     "owner": "Operator (own photography) or the Amazon IP Licence (product imagery).",
     "blocked": "Partly. The current images are labelled illustrations, which is truthful; a photograph without a licence would not be.",
     "verdict": "Only after a licence or a real unit exists."},
    {"id": "D-04",
     "proposal": "Add a mailing list capture form to the front page.",
     "changes": "The capture card and a new backend endpoint.",
     "source": "pages-limits",
     "quote": "GitHub Pages is a static host: it serves files and does not run a server-side form handler.",
     "missing": "A chosen email provider, its data-processing terms, and a privacy page naming retention.",
     "owner": "Operator (vendor choice and consent wording).",
     "blocked": "Yes, on hosting: a static host cannot receive the submission.",
     "verdict": "RSS stands in until a provider is chosen."},
    {"id": "D-05",
     "proposal": "Verify the site in Search Console and submit the sitemap, so the next topic is chosen from measured queries.",
     "changes": "Nothing on the page. It opens a data source.",
     "source": "google-query",
     "quote": "The Performance report's Queries tab shows the searches that returned the site in results, with impressions and position.",
     "missing": "Access to a Google account that can verify the domain or the repository Pages URL.",
     "owner": "Operator (Google account).",
     "blocked": "Yes, on account access. No page change can substitute for it.",
     "verdict": "The single highest-value unblocked-by-nobody item on this list."},
    {"id": "D-06",
     "proposal": "Show a contact address and a named editor, as a publication does.",
     "changes": "The masthead, the about page and the footer.",
     "source": "amazon-agreement",
     "quote": "Participation Requirements 3 requires the site to be the operator's own responsibility, and 1 requires the application's site details to be accurate.",
     "missing": "A name the operator is willing to publish, and an address that will be monitored.",
     "owner": "Operator.",
     "blocked": "Yes, on the operator's decision, not on a rule.",
     "verdict": "Cannot be automated. Needs a person's consent."},
    {"id": "D-07",
     "proposal": "Publish a new question-shaped guide every fortnight.",
     "changes": "The guides directory, the sitemap and the RSS feed.",
     "source": "google-outbound",
     "quote": "Google's guidance on outbound links and on helpful content rewards original value, not volume.",
     "missing": "A measured query set to choose the topic, and an author to stand behind it.",
     "owner": "Operator (author) plus Search Console (topic choice).",
     "blocked": "Partly. Ten guides exist and are already in the sitemap and the feed; adding more without measurement adds volume, not value.",
     "verdict": "Hold until D-05 gives a measured topic."},
]


def _source_cell(key):
    label, url = SOURCES[key]
    return (f'<a rel="noopener" target="_blank" href="{esc(url)}">{esc(label)} '
            f'<span aria-hidden="true">&#8599;</span></a>')


def _row(r):
    blocked = r["blocked"].startswith("Yes")
    return f"""<article class="scard" id="{esc(r['id'])}">
  <div class="scard-head">
    <span class="scard-id">{esc(r['id'])}</span>
    <h3>{esc(r['proposal'])}</h3>
    <span class="scard-effort">{'Blocked' if blocked else 'Partly blocked'}</span>
  </div>
  <div class="scard-body">
    <div class="scard-why">
      <p class="q-label">What it changes</p><p>{esc(r['changes'])}</p>
      <p class="q-label" style="margin-top:.9rem">What the source says</p>
      <p>{esc(r['quote'])}</p>
      <p class="tiny" style="margin-top:.5rem">{_source_cell(r['source'])}</p>
    </div>
    <dl class="scard-meta">
      <div><dt>Missing before a decision</dt><dd>{esc(r['missing'])}</dd></div>
      <div><dt>Who closes it</dt><dd>{esc(r['owner'])}</dd></div>
      <div><dt>Blocked by a rule?</dt><dd>{esc(r['blocked'])}</dd></div>
      <div><dt>Recommendation</dt><dd class="rec">{esc(r['verdict'])}</dd></div>
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


def build(page_dir):
    d = page_dir
    blocked = sum(1 for r in ROWS if r["blocked"].startswith("Yes"))

    table_rows = "".join(
        "<tr>"
        f"<td><strong>{esc(r['id'])}</strong></td>"
        f"<td>{esc(r['proposal'])}</td>"
        f"<td>{esc(r['missing'])}</td>"
        f"<td>{esc(r['owner'])}</td>"
        f"<td>{'Blocked' if r['blocked'].startswith('Yes') else 'Partly'}</td>"
        "</tr>" for r in ROWS)

    body = f"""{pagehead(
        'Decision registry',
        'What we know,<br>what we do not,<br>and what it blocks',
        f'{len(ROWS)} proposals under consideration. {blocked} cannot be decided yet, because a fact is missing that no page change can supply. Each row names the official document it is checked against, the one missing fact, and the person who has to close it. Record a decision per row; nothing is implemented by pressing a button.',
        meta='Decisions are stored in your browser only &middot; nothing transmitted &middot; every source is an official document',
    )}
{section(f'''
<div class="sec-head"><div>{eyebrow('The blocking list')}<h2>Every open decision, and what holds it</h2></div>
<p>Read the "missing" column before the proposal. Anything blocked there cannot be approved first, however sensible it looks.</p></div>
<div class="table-scroll"><table class="register">
<caption>Decisions, their missing fact, and the owner who can close it</caption>
<thead><tr><th scope="col">Ref</th><th scope="col">Proposal</th><th scope="col">Missing before a decision</th><th scope="col">Who closes it</th><th scope="col">Blocked</th></tr></thead>
<tbody>{table_rows}</tbody></table></div>
<p class="table-note">A blank in the "missing" column would mean nothing blocks the row. No row is blank: every proposal on this site currently waits on an account, a licence or a person.</p>''', cls='')}
{section(f'''
<div class="decide-intro">
  <div>
    <h2>Record a decision</h2>
    <p>Each card below repeats one row in full: the source, the quote, the missing fact and a recommendation. Mark accept, hold or reject. The choice is kept in this browser and can be copied out as text, which is the only way it leaves this page.</p>
  </div>
  <div class="decide-tools">
    <button type="button" class="btn btn-small" data-action="copy">Copy decisions</button>
    <button type="button" class="btn btn-ghost btn-small" data-action="reset">Clear all</button>
    <p class="decide-count" data-count>0 of {len(ROWS)} decided</p>
  </div>
</div>
{''.join(_row(r) for r in ROWS)}''', cls='section-tint')}
{section(f'''
<div class="callout">
  <h2>The one decision that unblocks the most</h2>
  <p>D-05, Search Console, changes nothing a reader can see. It is also the only item on this page that turns guesswork into evidence: until it is on, every choice about what to write next is an assumption. It needs one thing the build cannot supply, a Google account, and nothing else on this list gets easier until it is done.</p>
  <p class="callout-links"><a class="tlink" href="{esc(rel(d, 'questions/index.html'))}">The remaining question register <span aria-hidden="true">&rarr;</span></a></p>
</div>''', cls='')}"""
    return page(
        d,
        title="Decision registry \u2014 what blocks each change | Crisp & Counter",
        description=f"{len(ROWS)} proposals, the official source each is checked against, the one missing fact that blocks a decision, and who can close it.",
        body=body,
        active="decisions/index.html",
        canonical="decisions/",
        structured={"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": "https://karagemop466-tech.github.io/Affil1/"},
            {"@type": "ListItem", "position": 2, "name": "Decision registry",
             "item": "https://karagemop466-tech.github.io/Affil1/decisions/"},
        ]},
    )
