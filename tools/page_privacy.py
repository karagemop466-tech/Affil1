"""The privacy notice, generated so it cannot drift from the collector.

A privacy page that describes a different analytics system from the one in the
repository is worse than no privacy page. This one is built from the same list
of allowed fields that analytics/collect.py enforces, and the checker fails if
the two lists diverge.
"""

from layout import esc, eyebrow, page, pagehead, rel, section, table

# Must stay identical to ALLOWED_EVENTS in analytics/collect.py; the checker
# compares the two.
EVENTS = [
    ("page_view", "A page was rendered.", "The page path, with the query string removed. The date."),
    ("outbound_product_click", "A reader activated a link to an Amazon listing.", "The page path, the product ASIN, the date. Not the destination, not the outcome."),
    ("guide_read_75", "A reader scrolled to 75% of a guide's height.", "The page path, the date."),
    ("compare_view", "The comparison page was rendered.", "The page path, the date."),
    ("flag_page_view", "The review queue was opened.", "The page path, the date."),
]

NOT_COLLECTED = [
    ("IP address", "Not read by the collector and not written anywhere. No forwarding header is trusted or stored."),
    ("Cookies", "None are set. The client never touches document.cookie."),
    ("Local or session storage", "Not used. There is no persistent identifier, so two visits cannot be linked."),
    ("Query strings", "Stripped before anything is sent, so a search term in a URL is never transmitted."),
    ("Referrer URL", "Not collected. The site does not attempt to reconstruct search queries; Search Console does that properly."),
    ("User agent, screen size, device model", "Not collected."),
    ("Anything after a click", "Amazon's site is not observable from here. This site never claims to know whether a purchase happened."),
]


def build(page_dir, meta):
    d = page_dir
    rows = [[{"html": '<code class="code">%s</code>' % esc(n)}, esc(t), esc(w)] for n, t, w in EVENTS]
    neg = [[{"html": "<strong>%s</strong>" % esc(t)}, {"html": esc(w)}] for t, w in NOT_COLLECTED]

    body = f"""{pagehead(
        'Privacy',
        'What this site knows<br>about you, which is almost nothing',
        'No cookies, no advertising identifiers, no third-party scripts and no analytics running. This page describes exactly what would be collected if measurement were switched on, because a notice added after the fact is not a notice.',
        meta='Current state: analytics switched off &middot; 0 cookies &middot; 0 third-party requests',
    )}
{section(f'''
<h2>Today</h2>
<p>Right now this site collects nothing. There is no analytics endpoint configured, no form, no account, no newsletter and no comment system. The pages are static files served by GitHub Pages, which keeps its own server logs under its own policy; that is outside this site's control and is not something this site can read.</p>
<p>Loading any page here makes exactly two kinds of request: for the HTML file itself, and for files in this repository (styles, fonts, images, one script). No request goes to a third party.</p>

<h2>If measurement is switched on</h2>
<p>The repository contains a measurement client and a self-hosted collector. Both are written and tested; neither is deployed. If the site's owner deploys the collector and sets one line of configuration, the following would be recorded:</p>
{table(['Event', 'Recorded when', 'What is stored'], rows, cls='events')}
<p>That is the whole payload: four fields per event, an aggregate count per day. There is no visitor record to retain, so there is no retention period to expire, and nothing that could be joined to a person.</p>

<h2>What would never be collected</h2>
{table(['Never collected', 'Why'], neg, cls='negative')}

<h2>Opting out</h2>
<p>If Global Privacy Control or Do Not Track is set in your browser, the client sends nothing at all, including page views. There is no consent banner because there is no profiling, no advertising network and no cross-site tracking to consent to; a banner in front of an integer count would be theatre.</p>

<h2>Amazon links</h2>
<p>Clicking a product link takes you to Amazon, which has its own privacy policy and its own cookies. This site is not told what you do there, and makes no claim about it. Links carry the site's Associates tag so that a qualifying purchase can be attributed; the tag identifies the site, not you.</p>

<h2>Changes</h2>
<p>If the collector is deployed, this page changes in the same commit, and the change is dated in the <a href="{esc(rel(d, 'calendar/index.html'))}">publishing calendar</a>. A privacy notice that changes silently is not worth reading, so this one is generated from the collector's own field list and the build fails if the two disagree.</p>

<div class="callout">
  <h2>The one thing to take from this page</h2>
  <p>The reason the site can say this plainly is that it does not run a third-party analytics product. That is a design choice with a cost: no traffic data means no data-driven decision, which is why measurement is the first item in the <a href="{esc(rel(d, 'suggestions/index.html'))}">decision queue</a>.</p>
</div>''', cls='')}"""
    return page(
        d,
        title="Privacy \\u2014 Crisp & Counter",
        description="What this site collects, which is nothing today: no cookies, no third-party scripts, no analytics running. What would be collected if the self-hosted collector were deployed, field by field.",
        body=body,
        active="privacy.html",
        canonical="privacy.html",
    )
