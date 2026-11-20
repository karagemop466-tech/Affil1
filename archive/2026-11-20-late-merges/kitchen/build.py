#!/usr/bin/env python3
"""Build the editorial-only Pages edition. Never emits a Special Link."""
from html import escape as e
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
BASE = 'https://karagemop466-tech.github.io/Affil1/kitchen/'
AGREEMENT = 'https://affiliate-program.amazon.com/help/operating/agreement'
POLICY = 'https://affiliate-program.amazon.com/help/operating/policies'
ASIN = 'https://sell.amazon.com/blog/what-is-an-asin'
FTC = 'https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking#affiliateornetwork'
OUTBOUND = 'https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links'
HOST = 'https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits#usage-limits'
SEARCH = 'https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview'
CONSOLE = 'https://support.google.com/webmasters/answer/7576553'
FSIS = 'https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers'
RECORDS = json.loads((HERE / 'records.json').read_text())
ROWS = RECORDS['products']
DATE = RECORDS['checked_on']
DISCLOSURE = 'As an Amazon Associate I earn from qualifying purchases.'


def external(href, label, product=False):
    rel = ' rel="sponsored nofollow noopener"' if product else ''
    return f'<a href="{e(href, quote=True)}"{rel}>{e(label)}</a>'


def table(head, rows, caption):
    return '<div class="table-wrap" tabindex="0" role="region" aria-label="' + e(caption, quote=True) + '"><table><caption>' + e(caption) + '</caption><thead><tr>' + ''.join(f'<th scope="col">{e(h)}</th>' for h in head) + '</tr></thead><tbody>' + ''.join('<tr><th scope="row">'+r[0]+'</th>'+''.join(f'<td>{v}</td>' for v in r[1:])+'</tr>' for r in rows) + '</tbody></table></div>'


DESK = [('desk.html', 'Executive summary'), ('flagged.html', 'Flagged for Review'), ('suggestions.html', 'Suggestions'), ('desk.html#questions', 'Open questions'), ('desk.html#ledger', 'Campaign ledger'), ('../reviews/verification-audit.html', 'Previous audit'), ('../dashboard.html', 'Historical dashboard'), ('../categories.html', 'Historical categories'), ('../review/index.html', 'Primary review desk'), ('../about/index.html', 'Primary publication about'), ('feed.xml', 'RSS feed'), ('sitemap.xml', 'Sitemap')]


def links(items):
    return ''.join(f'<a href="{p}">{e(t)}</a>' for p, t in items)


def page(slug, title, desc, body, *, kind='', noindex=False):
    canonical = BASE + ('' if slug == 'index' else slug + '.html')
    primary = [('compare', 'Compare gear'), ('guides', 'Buying guides')]
    current = slug if slug in ('compare', 'guides') else 'guides' if kind == 'guide' else ''
    nav = ''.join(f'<a href="{p}.html"' + (' aria-current="page"' if p == current else '') + f'>{t}</a>' for p,t in primary)
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ''
    (HERE / f'{slug}.html').write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | Good Measure Kitchen Notes</title><meta name="description" content="{e(desc, quote=True)}">{robots}
<link rel="canonical" href="{canonical}"><link rel="alternate" href="feed.xml" type="application/rss+xml" title="Good Measure Kitchen Notes">
<link rel="stylesheet" href="style.css"><link rel="icon" href="media/mark.svg" type="image/svg+xml"><meta property="og:title" content="{e(title, quote=True)}"><meta property="og:image" content="{BASE}media/counter.jpg">
<script src="measure.js" defer></script></head><body data-page="{slug}" data-kind="{kind}">
<a class="skip" href="#main">Skip to content</a>
<header class="mast"><div class="wrap mast-row"><a class="brand" href="./"><img src="media/mark.svg" width="42" height="42" alt=""><span>Good Measure<small>KITCHEN NOTES</small></span></a><nav aria-label="Main navigation">{nav}<details><summary>Editorial desk</summary><div class="dropdown">{links(DESK)}</div></details></nav></div></header>
<div class="notice"><div class="wrap">{DISCLOSURE} <a href="desk.html#policy">About our links</a></div></div>
<main class="wrap" id="main">{body}</main>
<footer><div class="wrap footer-grid"><div><a href="./" class="footer-brand">Good Measure</a><p>Kitchen notes for everyday cooks.</p><p>{DISCLOSURE}</p></div><nav aria-label="Editorial and reference pages">{links(DESK)}</nav></div><div class="wrap footnote">2026 · Good Measure Kitchen Notes <span>Editorial supplement to <a href="../">Crisp &amp; Counter</a></span></div></footer>
</body></html>\n''', encoding='utf-8')


def head(kicker, title, desc):
    return f'<div class="inside"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lede">{desc}</p></div>'


TOPICS = [
    ('AIR FRYERS', 'Basket or countertop oven?', 'Start with the meals you repeat and the counter you have.', 'compare.html#air-fryers', 'fryer'),
    ('THERMOMETERS', 'Instant-read or leave-in?', 'Find the kind of thermometer you’ll actually reach for.', 'probe.html', 'probe'),
    ('FIT & CLEANUP', 'Will it fit your counter?', 'Leave room to open, lift, wash and put it away.', '../crisp/guides/cleanup-and-counter-space/', 'ruler'),
    ('SEASONAL', 'Can it help you host?', 'Sketch out the last half hour before dinner.', '../guides/holiday-hosting.html', 'sun'),
]
ICONS = {
    'fryer': '<rect x="5" y="3" width="14" height="18" rx="4"/><path d="M5 10h14M10 14h4m-2 0v3"/><circle cx="12" cy="7" r=".5"/>',
    'probe': '<path d="m9 15 8-8a3 3 0 0 1 4 4l-8 8m-4-4 4 4m-4-4-6 6m3-3 2 2m7-11 4 4"/>',
    'ruler': '<path d="m3 16 13-13 5 5L8 21zM7 12l3 3m1-7 3 3m1-7 3 3"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v3m0 14v3M2 12h3m14 0h3M5 5l2 2m10 10 2 2M5 19l2-2M17 7l2-2"/>',
}


def topics():
    return '<div class="tiles">' + ''.join(f'<a class="tile {icon}" href="{url}"><span class="tile-top"><svg viewBox="0 0 24 24" width="27" height="27" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[icon]}</svg><span class="arrow" aria-hidden="true">↗</span></span><span class="tile-label">{label}</span><h3>{title}</h3><p>{text}</p></a>' for label,title,text,url,icon in TOPICS) + '</div>'


page('index','Kitchen gear worth the counter space','Practical buying guides for basket and oven-style air fryers, kitchen thermometers, and the countertop you already have.',f'''
<section class="hero"><div class="hero-text"><p class="eyebrow"><span></span> THE COUNTERTOP EDIT</p><h1>Make room for<br> <em>better cooking.</em></h1><p class="lede">From air fryers to meat thermometers, compare kitchen gear by how you actually cook. Start with your counter, your favorite meals, and the washing up.</p><div class="hero-actions"><a class="button" href="compare.html">Compare kitchen gear <span aria-hidden="true">↗</span></a><a class="subtle" href="guides.html">Explore the guides <span aria-hidden="true">→</span></a></div></div><figure class="hero-image"><img src="media/counter.jpg" width="1200" height="900" alt="Generic basket air fryer on a kitchen counter beside a plate of roasted potatoes" fetchpriority="high"><figcaption>Illustrative image · Not a product photo</figcaption></figure></section>
<section class="section" aria-labelledby="topic-title"><div class="section-head"><div><p class="eyebrow">THE BUYER’S NOTEBOOK</p><h2 id="topic-title">Shop by question.</h2></div><a class="subtle" href="guides.html">All buying guides <span aria-hidden="true">→</span></a></div>{topics()}</section>
<section class="feature section"><img src="media/probe.jpg" width="1200" height="900" loading="lazy" alt="Generic kitchen thermometer on a chopping board"><div><p class="eyebrow">THE LATEST GUIDE</p><h2>Do you need a wireless meat thermometer?</h2><p>Picture your next Sunday roast. Would you rather check it near the end, or follow it from the next room? Start there, not with the app.</p><a class="subtle" href="probe.html">Read the guide <span aria-hidden="true">→</span></a></div></section>
''')


def comparison(kind):
    return table(['Model observed', 'What to check', 'Source'], [(e(r['name']), e(r['question']), external(r['observed_redirect_target'], 'Amazon listing evidence ↗', True)) for r in ROWS if r['kind'] == kind], 'Observed listings · not ranked or tested')


page('compare','Compare air fryers and meat thermometers','Compare observed models by cooking workflow, counter space and cleanup rather than by invented rankings.',head('THE COMPARISON DESK','Compare kitchen gear.','Start with the job, then check the model. Listed capacities are part of the observed listing names, not a test of how much food fits.')+f'''
<div class="jump"><a href="#air-fryers">Air fryers ↓</a><a href="#thermometers">Thermometers ↓</a></div>
<section class="section" id="air-fryers"><h2>Air fryers</h2><p>For a weeknight meal you make on repeat, measure the largest thing that needs to fit. Then compare usable basket or tray dimensions, open-drawer or open-door depth, ventilation and cleaning instructions in the manufacturer’s manual.</p>{comparison('air-fryers')}<p><a class="subtle" href="../crisp/guides/air-fryer-capacity-checklist/">Use the air fryer capacity checklist →</a></p></section>
<section class="section" id="thermometers"><h2>Meat thermometers</h2><p>For fast spot checks, consider a handheld model. If you need to follow a long cook without standing at the oven, look into a leave-in probe and check its manual for how it can be used.</p>{comparison('thermometers')}<p><a class="subtle" href="probe.html">Read the thermometer guide →</a></p></section>
<p class="byline">Listing evidence checked <time datetime="{DATE}">November 20, 2026</time>. Links are untagged evidence citations, not validated purchase links. <a href="flagged.html">See the verification notes</a>.</p>''',kind='compare')

page('guides','Kitchen buying guides','Find kitchen buying guides by format, capacity, cleanup, thermometers and holiday hosting.',head('THE BUYER’S NOTEBOOK','Buying guides.','Pick the question you’re trying to answer before adding anything to your counter.')+topics()+'''
<section class="reading section"><h2>More kitchen questions</h2><ul><li><a href="../crisp/guides/basket-or-oven-air-fryer/">Basket or oven-style air fryer: what should you compare?</a></li><li><a href="../crisp/guides/air-fryer-capacity-checklist/">What does air fryer capacity mean in practice?</a></li><li><a href="../crisp/guides/multi-function-kitchen-appliance-questions/">Which functions would you actually use?</a></li></ul><p><a class="subtle" href="feed.xml">Follow new guides via RSS →</a></p></section>''')

page('probe','Instant-read or wireless meat thermometer?','Work through three cooking situations to decide between an instant-read and a leave-in meat thermometer.',head('BUYING GUIDE / THERMOMETERS','Instant-read or wireless meat thermometer?','Start with when you want the answer: once, at the counter, or repeatedly through a long cook.')+f'''
<article class="reading guide"><p class="byline">By Good Measure Kitchen Notes · <time datetime="{DATE}">November 20, 2026</time> · Research-based, not hands-on testing</p><img class="article-image" src="media/probe.jpg" alt="A generic metal food thermometer on a chopping board"><p class="byline">Illustrative image, not a model reviewed in this guide.</p>
<h2>For weeknight checks, try the simpler option first</h2><p>If you mostly check chicken pieces or burgers just before serving, think about how quickly you can open the drawer, read the display, and check the next piece. Check the manual for insertion depth, how to clean the probe and whether it can be left in the food. Don’t assume an instant-read device can stay in the oven.</p>
<h2>For a longer roast, ask what you need to monitor</h2><p>If you frequently move between the kitchen and the dining table while cooking a roast, a leave-in probe may be worth comparing. Check which parts are designed to stay in your appliance, what happens if connectivity drops, and whether you need a phone or an account. Read the manual for the exact variant rather than assuming every probe in a range works the same way.</p>
<h2>Make a choice before opening a listing</h2><p>Write down one meal you’d use it for this week. If the job is checking several pieces near the end, compare handheld probes first. If the job is following a slow roast while you do something else, compare leave-in models. If you already have a thermometer that handles both jobs you need, keep it.</p>
<aside class="callout"><strong>For food safety:</strong> Follow the {external(FSIS, 'USDA’s guidance on thermometer placement and safe temperatures')} and the manufacturer’s instructions. Appearance alone does not establish that meat is safe.</aside><p><a class="button" href="compare.html#thermometers">Compare observed models →</a></p></article>''',kind='guide')

questions = [
    ('Are these the products we meant to feature?', 'Unverified. Five destination listings observed, zero intended ASINs confirmed.', 'Verify each exact variant and retain a dated first-party confirmation.', AGREEMENT),
    ('Will these links earn credit for shopnow047c-20?', 'Unverified. None of the observed destination URLs showed that tag; its absence does not establish a failure.', 'Generate one Special Link per confirmed product in the enrolled workflow and reconcile its destination and reported click before scale. Do not make a test purchase.', POLICY),
    ('Can we show price, stock, stars or reviews?', 'No approved data path in this build. No values shown.', 'Confirm API eligibility, display rules, licensed fields and refresh behavior before any integration.', POLICY),
    ('Which guide should come next?', 'No verified query evidence.', 'Verify Search Console ownership and compare landing-page impressions and queries over a fixed period. Use them to select one question to answer well.', CONSOLE),
    ('Can Pages host the monetized edition?', 'Not the launch target for a primarily commercial site. This supplement is editorial.', 'Use hosting that supports the commercial use and a same-origin collector; verify policy, security and privacy before launch.', HOST),
    ('Do outbound clicks mean purchases?', 'No. There are no authorized order reports in this repo.', 'Import a dated Associates report for the same marketplace, tracking ID and period. Keep first-party click observations and Amazon’s reported metrics separate.', POLICY),
]
q_table = table(['Decision question', 'What we know', 'How to close the gap', 'Official source'], [(e(q),e(a),e(n),external(s,'Read source ↗')) for q,a,n,s in questions], 'Pre-decision questions')
ledger = table(['Report timestamp (UTC)', 'Source', 'Channel', 'Eligible sessions', 'Clicks', 'Reported orders', 'Provenance'], [], 'Campaign ledger · no authorized rows yet')
page('desk','Executive summary and measurement','The outcome of five product link checks and the evidence still needed before monetization, measurement and publication decisions.',head('EDITORIAL DESK','Executive summary.','An editorial edition is ready to read. Monetization and production measurement are not yet validated.')+f'''
<div class="summary"><div><strong>5</strong><span>listing destinations observed</span></div><div><strong>0</strong><span>confirmed product intents</span></div><div><strong>0</strong><span>validated Special Links</span></div></div>
<section class="section reading" id="policy"><h2>What shipped</h2><p>Buying guides and comparisons for air fryers and meat thermometers, a line-by-line confirmation record, and an evidence-first launch checklist. Listing checks found a fifth destination with a previously inconsistent redirect history. They do not validate attribution to <code>shopnow047c-20</code>.</p><h2>What stays behind the gate</h2><p>Marketing links, account data, prices, reviews and commission figures are not published here. Review the {external(AGREEMENT,'Associates Operating Agreement')}, {external(POLICY,'Program Policies')}, {external(FTC,'FTC affiliate guidance')} and {external(OUTBOUND,'Google’s outbound link guidance')} before publishing. The {external(HOST,'GitHub Pages usage limits')} rule out using Pages for a site primarily directed at commercial transactions. Reader capture is deferred; use RSS without asking for an email address.</p></section>
<section class="section" id="questions"><h2>Questions before decisions</h2>{q_table}</section>
<section class="section" id="ledger"><h2>Campaign ledger</h2><p>The schema is public; no authorized first-party reports were available. Missing values are not zero. No estimate or conversion score is computed.</p>{ledger}<p>Before adding a row, retain report ID, report window, pull timestamp, marketplace, tracking ID and authorized source. Treat local page and click totals as engagement, not as Amazon sessions or orders. See the {external(POLICY,'Amazon commission and participation rules')}.</p></section>
<section class="section reading"><h2>Proposed publishing cadence</h2><p>Every other Thursday: review available query data and propose a single buying question. Publish or revise a sourced guide only after evidence and compliance review. Update canonical URLs, scope sitemap and feed in the same build. If there are no measured queries yet, label topics as editorial hypotheses instead of inventing demand. Check crawl coverage in {external(CONSOLE,'Search Console')}; a {external(SEARCH,'sitemap helps discovery')} but is not proof of indexing.</p>
<h2>Measurement and privacy</h2><p>No measurement is enabled on this Pages edition. A self-hosted companion can count five events without cookies or stored visitor identifiers after the hosting and privacy review. It does not record purchases or collect email addresses.</p></section>''',noindex=True)

record_rows = []
for r in ROWS:
    record_rows.append((e(r['id']), external(r['submitted'], r['submitted'].split('/')[-1], True), '', '', '', '', external(r['observed_redirect_target'], r['observed_asin'] + ' ↗', True), 'Unverified intent. '+e(r['history'])))
confirmation_table = table(['Record','Submitted link','Intended ASIN','Confirmed official listing URL','Confirmation date','Confirmation source','Observed destination','Flag'], record_rows, 'Product-intent confirmation records')
page('flagged','Flagged for Review','See the five Amazon redirect observations and what remains unverified for each submitted link.',head('EDITORIAL DESK','Flagged for Review.','Known gaps and conflicting observations, kept separate from buyer guidance.')+f'''
<section class="section"><h2>Which product was intended?</h2><p>{e(RECORDS['method'])} Amazon defines an {external(ASIN,'ASIN as a ten-character identifier')}. The five supplied codes are nine-character short-link slugs, not ASINs.</p>{confirmation_table}<p>Blank fields are unverified. None of the five links is certified as a Special Link here; their exact compliance remains unresolved (FLG-003). The <a href="../reviews/verification-audit.html">earlier observations</a> are retained as historical records. In this pass <strong>P-04</strong> reached the ThermoMaven thermometer and <strong>P-05</strong> reached the CHEF iQ thermometer. <a href="../review/index.html#FLG-016">Another session observed the reverse mapping</a>. Neither pass overrides the other or confirms which variant was intended.</p></section>
<section class="section reading"><h2>Before enabling any purchase link</h2><ol><li>Confirm the intended ASIN and official listing in the enrolled account and date the confirmation.</li><li>Generate the proper Special Link and verify both destination and attribution through the account workflow.</li><li>Review hosting, link-level disclosure placement and policy before publication.</li></ol><p>{external(AGREEMENT,'Amazon Associates agreement')} · {external(POLICY,'Program policies')} · {external(FTC,'FTC endorsement guidance')}</p><h2>Other review items</h2><p>Search Console ownership, production analytics and reader capture are not configured here. No real conversion, trend or commission data was obtained. <a href="desk.html#questions">See the next evidence to collect →</a></p></section>''',kind='flag',noindex=True)

suggestions = [
    ('S1 · Validate account links first', 'High / small account workflow', 'Retain intended variant, one tested Special Link per product and dated click-report evidence.', AGREEMENT),
    ('S2 · Choose commercial hosting before monetization', 'High / infrastructure', 'Pick a host that permits affiliate operation and same-origin collection; validate hosting terms and run a privacy review.', HOST),
    ('S3 · Pick one follow-up guide from measured demand', 'Medium / dependent on data', 'Verify the Search Console property, compare recent query/page impressions, and choose one unanswered question. Until then: “What fits in one basket?” is a draft hypothesis.', CONSOLE),
    ('S4 · Add exact-model evidence and original tests', 'High / editorial effort', 'Collect manufacturer manuals, document open-door clearance, usable dimensions and cleanup steps. Publish testing methodology only if tests actually happen.', FTC),
    ('S5 · Automate suggestions, not publication', 'Medium / after reporting', 'Use authorized catalog and reporting inputs; generate drafts with sources and blanks for missing facts. Require a human release gate. Do not score a niche from missing data.', POLICY),
    ('S6 · Offer email only after privacy review', 'Later / vendor review', 'Start with RSS. Before adding email, review the consent flow, retention and unsubscribe process; avoid third-party trackers by default.', SEARCH),
]
s_rows = [(e(a),e(b),e(c),external(s,'Read source ↗'),f'<label class="sr" for="choice-{i}">Decision for suggestion {i}</label><select id="choice-{i}" data-choice="{i}"><option value="">Not reviewed</option><option>Prioritize</option><option>Hold</option><option>Decline</option></select>') for i,(a,b,c,s) in enumerate(suggestions,1)]
page('suggestions','Suggestions for review','Review proposed editorial and commercial improvements without deploying any changes.',head('EDITORIAL DESK','Choose the next move.','Proposals only. Mark the path you prefer and download a shortlist; nothing here changes the site or submits data.')+table(['Proposal','Priority / effort estimate','Evidence or next action','Official source','Your decision'],s_rows,'Suggestions for review')+'''
<p><button class="button" type="button" id="export">Download decisions ↓</button> <span id="decision-status" role="status"></span></p><p>Decisions stay in this tab until you download them. Priorities above are editorial judgments, not sales forecasts.</p>
<section class="section reading"><h2>Brief for the next design pass</h2><blockquote>Design a buyer-first kitchen journal. Lead with one seasonal question and a clear route to compare gear. Use original or clearly illustrative imagery, short household scenarios, and a transparent byline. Show the shortlist and what to check, not a list of invented winners. Put the register, ledger and open questions behind one editorial desk. Never describe a listing as tested or trending unless there is evidence.</blockquote></section><script src="decisions.js" defer></script>''',noindex=True)

rss = ET.Element('rss',version='2.0')
channel = ET.SubElement(rss,'channel')
for tag,value in [('title','Good Measure Kitchen Notes'),('link',BASE),('description','Question-led kitchen buying guides.')]:
    ET.SubElement(channel,tag).text = value
# Include only articles, not decision pages. The hosting guide predates this supplement.
for title,loc,desc in [
    ('Instant-read or wireless meat thermometer?',BASE+'probe.html','Pick a thermometer by the way you actually cook.'),
    ('Can a countertop appliance help you host?',BASE+'../guides/holiday-hosting.html','Plan the last half hour before serving.'),
]:
    item = ET.SubElement(channel,'item')
    for tag,value in [('title',title),('link',loc.replace('/kitchen/../','/')),('guid',loc.replace('/kitchen/../','/')),('pubDate','Fri, 20 Nov 2026 00:00:00 GMT'),('description',desc)]:
        ET.SubElement(item,tag).text = value
ET.indent(rss)
ET.ElementTree(rss).write(HERE/'feed.xml',encoding='utf-8',xml_declaration=True)
site = ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
for path in ('','compare.html','guides.html','probe.html'):
    ET.SubElement(ET.SubElement(site,'url'),'loc').text = BASE+path
ET.indent(site)
ET.ElementTree(site).write(HERE/'sitemap.xml',encoding='utf-8',xml_declaration=True)
