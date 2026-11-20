"""The publishing calendar: a cadence that is published, not promised.

A schedule kept in a chat message is a plan. A schedule kept on a page with
dates, a status per slot and the rule for filling it is a commitment a reader
can check, which is the only version that survives a busy month.

Nothing here claims search volume, popularity or demand. A slot is a topic the
editor intends to write and the reason it is worth writing, not a prediction.
"""

from layout import (SITE_NAME, esc, eyebrow, outbound, page, pagehead, rel,
                    section, table)

# Slots are listed newest-first. A slot is only ever "published" once the page
# exists in the build; the check fails if a published slot has no guide.
SLOTS = [
    {
        "date": "2026-11-20",
        "topic": "Cooking for guests with one countertop appliance",
        "slug": "hosting-season-air-fryer",
        "basis": "Seasonal timing: the question arrives in the last quarter of the year, when people cook for more people than usual.",
        "status": "published",
    },
    {
        "date": "2026-11-20",
        "topic": "Batch cooking for the week: is one big basket enough?",
        "slug": "batch-cooking-for-the-week",
        "basis": "A decision the two basket formats force, and a question the capacity guide raises but does not answer.",
        "status": "published",
    },
    {
        "date": "2026-11-20",
        "topic": "Questions to ask before buying a multi-function kitchen appliance",
        "slug": "multi-function-kitchen-appliance-questions",
        "basis": "A general buying pattern the five-product set forces: preset counts and multi-function claims are the easiest thing to sell and the hardest thing to check.",
        "status": "published",
    },
    {
        "date": "2026-11-20",
        "topic": "How to assess cleanup and counter-space trade-offs",
        "slug": "cleanup-and-counter-space",
        "basis": "The cost of an appliance is paid every time it is washed and moved, and that cost is checkable before purchase.",
        "status": "published",
    },
    {
        "date": "2026-11-20",
        "topic": "A no-hype checklist for comparing air-fryer capacity",
        "slug": "air-fryer-capacity-checklist",
        "basis": "A quart is a volume; people cook on a surface. The single most common source of a regretted purchase in this category.",
        "status": "published",
    },
    {
        "date": "2026-11-20",
        "topic": "Basket or oven-style air fryer: what should you compare?",
        "slug": "basket-or-oven-air-fryer",
        "basis": "The format decision comes before the product decision, and the product set contains one of each shape, so the comparison can be made without inventing anything.",
        "status": "published",
    },
    {
        "date": "2026-11-27",
        "topic": "Will a countertop air fryer fit under my cabinets?",
        "slug": None,
        "basis": "Queued as a hypothesis. It becomes a commitment only when measured height and clearance figures can be sourced from official specification sheets, which this build could not do.",
        "status": "queued",
    },
    {
        "date": "2026-12-04",
        "topic": "One basket or two for a family of four?",
        "slug": None,
        "basis": "Queued as a hypothesis. The two-basket case is argued in the batch-cooking guide; a standalone page needs either measured capacity or real query data to justify itself.",
        "status": "queued",
    },
    {
        "date": "2026-12-11",
        "topic": "Chosen from the first Search Console query report",
        "slug": None,
        "basis": "Reserved, deliberately blank. The topic is not decided in advance because it depends on which queries actually produce impressions. Filling this slot with a guess would defeat the purpose of the slot.",
        "status": "reserved",
    },
]

RULES = [
    ("One guide per slot, and a slot can be empty",
     "A missed slot is published as missed. The calendar is a record, not a marketing claim, and an empty row tells a reader more than a filled row written to hit a date."),
    ("No topic without a reason that can be checked",
     "Every published slot names its basis: a seasonal question, a decision the product set forces, or a measured query. &ldquo;It seemed interesting&rdquo; is not a basis."),
    ("A published slot must exist in the build",
     "The checker fails if a slot marked published has no guide page, so the calendar cannot drift ahead of the site."),
    ("Everything new goes into the sitemap and the feed",
     "Both are generated from the same build, so a new guide is submitted and syndicated in the same commit that publishes it. Nothing is added by hand."),
    ("Nothing is published unreviewed",
     "A draft is checked claim by claim against the source register, and the disclosure placement is checked on the rendered page, before it is committed."),
]


def build(page_dir, meta):
    d = page_dir
    rows = []
    for s in SLOTS:
        if s["status"] == "published" and s["slug"]:
            topic = '<a href="%s">%s</a>' % (
                esc(rel(d, "guides/%s.html" % s["slug"])), esc(s["topic"]))
            state = '<span class="pill pill-ok">Published</span>'
        else:
            topic = esc(s["topic"])
            state = ('<span class="pill pill-warn">Queued</span>' if s["status"] == "queued"
                     else '<span class="pill">Reserved</span>')
        rows.append([
            {"html": "<strong>%s</strong>" % esc(s["date"])},
            {"html": topic},
            {"html": esc(s["basis"])},
            {"html": state},
        ])
    tbl = table(["Date", "Slot", "Why this topic, and what would confirm it", "State"],
                rows, cls="calendar",
                caption="%d slots: %d published, %d queued, 1 reserved" % (
                    len(SLOTS),
                    sum(1 for s in SLOTS if s["status"] == "published"),
                    sum(1 for s in SLOTS if s["status"] == "queued")),
                note="Dates are publication targets, not promises about search performance. No slot in this table has a verified search volume behind it.")

    rules = "".join(
        '<div class="rule"><span class="rule-n">%02d</span><h3>%s</h3><p>%s</p></div>' % (i + 1, esc(t), b)
        for i, (t, b) in enumerate(RULES)
    )

    body = f"""{pagehead(
        'Publishing calendar',
        'A cadence,<br>published rather than promised',
        'One guide per week is the intention. This page records which slots are filled, which are still hypotheses, and which is deliberately left blank for a topic to be chosen from real query data.',
        meta='%d slots &middot; %d published &middot; no slot carrying a popularity claim' % (
            len(SLOTS), sum(1 for s in SLOTS if s["status"] == "published")),
    )}
{section(f'''
<p class="lede-prose">A schedule that lives in a chat message is a wish. A schedule with dates, a state per row and a published reason is something a reader can hold the site to, including when a week is missed.</p>
{tbl}''', cls='')}
{section(f'''
<div class="sec-head"><div>{eyebrow('The rules')}<h2>Five rules the calendar is kept to</h2></div>
<p>Each one exists because the alternative is a page that looks maintained and is not.</p></div>
<div class="rule-grid">{rules}</div>''', cls='section-tint')}
{section(f'''
<div class="callout">
  <h2>Why the last slot has no topic</h2>
  <p>It is reserved for the first topic chosen from a real Search Console query report rather than from editorial instinct. Until that report exists, writing a topic into the slot would make the calendar look complete and would tell a reader nothing true.</p>
  <p><a class="tlink" href="{esc(rel(d, 'questions/index.html'))}">The question that closes it &rarr;</a> <a class="tlink" href="{esc(rel(d, 'feed.xml'))}">Follow the feed &rarr;</a></p>
</div>''', cls='')}"""
    return page(
        d,
        title="Publishing calendar \\u2014 %s" % SITE_NAME,
        description="The publication schedule: which guides are published, which topics are still hypotheses, and the slot reserved for a topic chosen from measured search queries.",
        body=body,
        active="calendar/index.html",
        canonical="calendar/",
    )
