# Crisp & Counter — design brief & suggestion register

**Status:** proposal. Nothing in this file is implemented, and nothing should be implemented
until its row in the decision register (`suggestions/`, fed from `src/data/suggestions.json`)
is accepted. This document is the upstream input to that register and to the design prompt.

**Author:** session `arena/812a8198-affil1` · **Prepared:** 2026-11-20 · **Tracking ID supplied:** `shopnow047c-20` (unconfirmed on any link — FLG-002)

---

## 0. What this is grounded in (read first)

This brief was prepared against `main` @ 92a3509 (2026-11-20, PRs #22–#27). `main` has since advanced
through PR #64+ within the same hour; statements marked "verified 2026-11-20" were true at preparation
time — re-run `tools/check.py` / `check_local_links.py` before acting on counts.

| Fact (verified 2026-11-20) | Source |
|---|---|
| Maintained edition at `/`; static, build-generated; no JS frameworks, no CDN, self-hosted fonts | `README.md`; `tools/` |
| `python3 tools/check.py` → 0 errors, 0 warnings (reported with 22 pages at preparation; 30 pages later) | run by this session, 2026-11-20 |
| `python3 tools/check_local_links.py` → 65 served HTML files, 0 broken relative references | run by this session, 2026-11-20 |
| `tools/validate.py` → fails with `KeyError: 'supplied_path_code_length'` (schema drift; needs reconciliation, not a claim of success) | run by this session, 2026-11-20 |
| Front page leads with products + guides; disclosure strip above `<main>` on every page | `tools/page_home.py`, `tools/layout.py` |
| Design tokens: paper `#fbf9f4`, ink `#17251f`, forest `#1f3a30`, sage `#7d947f`, amber `#b8762b`; Fraunces (serif) + Inter (sans), self-hosted woff2 | `assets/css/site.css`, `assets/fonts/` |
|Five submitted links resolve (as of pass-2 and this session's pass-3, 2026-11-20) to product pages; P-04/P-05 mapping is disputed between sessions (FLG-016) | `COORDINATION.md`; `src/data/products.json` |
|No price, rating, review count or stock figure is published; Program Policies §2(b) permits those only from Amazon-served data or the PA/Creators API, neither of which is connected | `src/data/compliance.json`; Policies §2(b) |
| Analytics is inert; no collector is deployed; campaign ledger is empty by design | `review/measurement.html`; `operations/ledger.html`; `assets/js/analytics.js` |
| Three new static guides (`meal-prep-sunday`, `small-kitchen-counter`, `thermometer-pairing`) are NOT in the generated sitemap/feed — build inputs, not stray files | `tools/content.py` GUIDES (owner: prior/parallel session) |

**Design job:** make a careful, compliance-first register feel like a shop a buyer trusts and a
publication a search engine can rank — without inventing a single fact the site does not have.

---

## 1. Non-negotiable constraints (official sources, re-checked 2026-11-20)

1. **Disclosure placement (Amazon Associates Operating Agreement §5, updated 2025-10-15):**
   "You must clearly and prominently state the following… 'As an Amazon Associate I earn from
   qualifying purchases.'" Keep it above the fold and in the footer — footer-only is explicitly
   insufficient in the FTC's framing ("closer to the recommendation is better").
   https://affiliate-program.amazon.com/help/operating/agreement
2. **Special Links (Agreement §1):** outbound product links must use the "tagged" link formats
   Amazon provides (`…/dp/<ASIN>?tag=shopnow047c-20` on this site). Attribution in the resolved
   URLs is observed but unconfirmed; the supplied `link.amazon/*` links' compliance is
   unresolved (FLG-003) and must never be declared invalid.
3. **Program Policies (Agreement §12 incorporates by reference), §2(b):** prices/availability
   only if Amazon-served or via Creators API / PA API. Both absent ⇒ **no price, rating, review
   count or stock may ever appear** until one is connected.
   https://affiliate-program.amazon.com/help/operating/policies
4. **FTC Endorsement Guides: What People Are Asking** (revised 2023): material connections
   must be "clearly and conspicuously" disclosed; dedicated affiliate-marketing section.
   https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
   (15 CFR Part 255: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255)
5. **Google Search Central — qualify outbound links:** `rel="sponsored"` for paid placements;
   multiple rel values permitted (site uses `sponsored nofollow noopener`).
   https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
6. **ASIN = Amazon Standard Identification Number,** a unique 10-character alphanumeric code,
   found after `/dp/`; the five submitted path codes are 9 characters and are **not** ASINs.
   https://sell.amazon.com/blog/what-is-an-asin
7. **Trademark:** Amazon marks used nominatively, unaltered, no implied endorsement (Program
   Policies, IP License). Brand photos/logos: do not hotlink Amazon imagery without a licence;
   the site uses its own generated/placeholder imagery by design (`review/images.html`).
8. **Claims discipline:** nothing tested ⇒ no "best", "#1", "winner", rating or performance
   claim. Editorial hypotheses are labelled as hypotheses (FLG-013).
9. **Privacy:** no cookie, no persistent id, no IP, no user agent anywhere; DNT/GPC honoured;
   analytics inert until a first-party collector host exists (`review/measurement.html`).
10. **Every generated page ships with:** disclosure strip, footer repeat, one `<h1>`, alt text,
    no inline handlers, relative links only (`/Affil1/` project path), sitemap/feed conformance —
    enforced by `tools/check.py`. Any new design must keep all ten check rules green.

---

## 2. Design principles (the "reads like a shop, ranks like a publication" set)

1. **Products first, process second.** The register leads; the verification story is one click
   away (`/products/`, `/review/`), never the headline.
2. **One shop, one voice.** A single publication identity (Crisp & Counter), one navigation
   group, one footer system. The parallel legacy editions stay reachable but unmerged and
   clearly labelled until the owner consolidates (design decision, not an agent decision).
3. **Honest specificity beats adjectives.** Copy says what the seller's listing claims, what a
   reader should measure, and what this site does not know. That *is* the brand.
4. **The page must work at 2 seconds.** System fonts are deliberately avoided; the self-hosted
   Fraunces/Inter stack costs ~60 KB total and is already wired. Keep LCP < 1.8 s on 4G.
5. **Every block answers a buyer question.** If a section cannot be phrased as a question a
   buyer asks in a store, cut it.
6. **Blank is a feature.** Empty spec cells are styled as "not confirmed yet" with a tooltip,
   never as zeros, dashes that look like data, or filler.
7. **Seasons and clusters, not dribbles.** Publishing follows a calendar (§6) and hub pages
   (clusters), each internally linked; orphans are a build failure, not a judgement call.
8. **Disclosure is furniture, not a banner.** Same position, same wording, every page.
9. **Accessibility is a floor:** 4.5:1 contrast (paper/ink passes), visible focus, skip link,
   semantic landmarks, no colour-only meaning, reduced-motion respect.
10. **Fast, static, survivable.** No build-time frameworks; a page you can read from a usb
    stick in 2045. Resilience is the aesthetic.
11. **Editorial accountability.** Every guide carries author (or "Crisp & Counter desk" until a
    named editor exists), published/updated dates, and a sources box. Named-byline decision is
    the owner's (FLG-013 adjacent).
12. **Calm urgency only.** Scarcity language is banned. The only pressure the site applies is
    the buyer's own deadline.

---

## 3. Suggestion register (DB-01 … DB-30) — for review, not implementation

Effort: S ≤ 1 h · M = half day · L = 1–3 days. Impact: expected effect on buyer utility /
findability. Files listed are the *touch points*; generated files change via `tools/` +
`src/data/`, never by hand. "Owner" = who must decide.

### 3.1 Brand & identity
| ID | Suggestion | Why | Effort | Impact | Touches | Owner |
|---|---|---|---|---|---|---|
| DB-01 | Commission a bespoke Crisp & Counter logomark + favicon set (the current wordmark is typeset only) | Brand recall; publication legitimacy | M | M | `assets/img/`, `tools/layout.py` | owner |
| DB-02 | Named editor byline + `/about/` author page with credentials and review history (even if pseudonymous-but-accountable) | E-E-A-T; trust | M | H | `about/`, `tools/content.py` | owner |
| DB-03 | Written voice guide (tone, taboo words, "claims we never make", reading age ≤ 9) | Kills AI-slop drift across contributors | S | M | `docs/` | desk |
| DB-04 | Original illustration system for guides (single illustrator or consistent generative-prompt spec + human edit) | Imagery honesty; replaces CSS stamps | L | M | `assets/img/`, `review/images.html` | owner |

### 3.2 Information architecture & navigation
| ID | Suggestion | Why | Effort | Impact | Touches | Owner |
|---|---|---|---|---|---|---|
| DB-05 | One primary nav group everywhere: Guides · Shortlist · Compare · Desk (current) — freeze it; move all legacy/parallel-edition links to footer "Other editions" with a one-line disclaimer | Matches the brief; stops edition confusion | S | M | `tools/layout.py` | done?→verify | desk |
| DB-06 | Category clusters as hubs: `/guides/air-fryers/` hub linking every air-fryer guide + products table; `/guides/thermometers/` twin hub | Topical authority; crawl paths | M | H | `tools/`, `src/data/` | desk |
| DB-07 | Breadcrumbs + `BreadcrumbList` JSON-LD on all guides/products | SERP real estate; orientation | S | M | `tools/layout.py` | desk |
| DB-08 | "Start here" 3-question decision tree on the front page (format → capacity → cleanup) wired to the compare table | Buyer task completion | M | H | `tools/page_home.py`, `tools/page_compare.py` | desk |
| DB-09 | Footer: add "This site" disclosure summary + "Corrections" link (corrections inbox or mailto) | Accountability; trust | S | M | `tools/layout.py` | desk |

### 3.3 Front page & conversion surface
| ID | Suggestion | Why | Effort | Impact | Touches | Owner |
|---|---|---|---|---|---|---|
| DB-10 | Replace generic hero art with a real, own-photo or own-illustration hero (air fryer in a real kitchen, no hands-with-flour cliché) | First impression; bounce | M | M | `tools/page_home.py`, `assets/img/` | owner |
| DB-11 | Product cards: add "Good if / Skip if" two-line verdicts sourced strictly from listing titles + buyer guide framing; keep blanks blank | Decision utility without unverified claims | M | H | `tools/page_products.py`, `src/data/` | desk |
| DB-12 | Sticky mobile CTA bar on product and compare pages: "Check price on Amazon" (sponsored rel, disclosure adjacent) | Mobile conversion path | M | M | `assets/css/`, `tools/` | desk |
| DB-13 | "What changed this week" micro-ledger on the front page (verification updates, new guides) | Return visits; transparency | S | M | `tools/page_home.py`, `src/data/` | desk |
| DB-14 | Compare table: freeze header row + highlight the two thermometer rows as "new" with date stamp | Scannability | S | L | `assets/css/`, `tools/page_compare.py` | desk |

### 3.4 Findability & SEO
| ID | Suggestion | Why | Effort | Impact | Touches | Owner |
|---|---|---|---|---|---|---|
| DB-15 | **Wire the 3 orphaned guides into the generated sitemap + feed + nav** (`meal-prep-sunday`, `small-kitchen-counter`, `thermometer-pairing`) | They are invisible to crawlers today | S | H | `tools/content.py` GUIDES; rebuild | desk (blocked on owner of tools/ claim) |
| DB-16 | Submit sitemap in Search Console; verify property; Bing Webmaster too | Index coverage; query data for topic selection | S | H | out-of-repo | owner |
| DB-17 | `FAQPage` JSON-LD on the question-shaped guides (only questions actually answered on-page) | Rich results eligibility; honest AEO | S | M | `tools/page_guides.py` | desk |
| DB-18 | `ItemList` JSON-LD on Shortlist + `Article` JSON-LD with `datePublished/dateModified/author` on guides | Structured-data clarity | S | M | `tools/` | desk |
| DB-19 | Programmatic internal links: every guide links ≥2 sister guides + 1 product record; enforce via check | Crawl depth; topical clusters | S | M | `tools/check.py` rule | desk |
| DB-20 | OG/Twitter cards with per-page titles (already partially present); audit every route renders a valid card | CTR from shares | S | L | `tools/layout.py` | desk |

### 3.5 Measurement & decisions
| ID | Suggestion | Why | Effort | Impact | Touches | Owner |
|---|---|---|---|---|---|---|
| DB-21 | Deploy the inert analytics collector on a small first-party host; set `CC_ANALYTICS_ENDPOINT`; verify 5 events in the legacy client + counts endpoint; publish retention/consent note first | The brief's measurement step is the only blocker left | M | H | `assets/js/analytics.js`, `analytics/endpoint.py` or Worker, `review/measurement.html` | owner |
| DB-22 | Run the one-link test: P-01 via enrolled Special Link; confirm click appears attributed to `shopnow047c-20` in the Associates report; only then scale links | Pass/fail for the whole programme (see `docs/MEASUREMENT.md`) | S | H | out-of-repo account | owner |
| DB-23 | Weekly 15-minute measurement review ritual (queries, clicks per page, ledger rows only from authorized reports) | Data-driven cadence | S (recurring) | M | `operations/ledger.html` | desk |
| DB-24 | Reconcile `tools/validate.py` to the new product schema so CI covers legacy editions again, or retire it explicitly with a note | CI honesty | S | M | `tools/validate.py` | desk |

### 3.6 Trust & editorial ops
| ID | Suggestion | Why | Effort | Impact | Touches | Owner |
|---|---|---|---|---|---|---|
| DB-25 | Publish a "Corrections & verification log" (what we got wrong, when, what changed) — the flagged page already holds raw material | Radical trust; differentiates from AI slop | S | M | `review/`, build | desk |
| DB-26 | Pre-publish compliance gate as CI: sponsored-rel audit, disclosure-in-first-200-words check, no-price-regex check, no-root-absolute-link check (check.py already covers most; add the first three) | The gate that makes automation safe | M | H | `tools/check.py` | desk |
| DB-27 | Editorial calendar Q4-2026 → Q1-2027 (see §6) published as `/about/` section or `docs/` roadmap | Predictable cadence; feed freshness | S | M | `docs/` | desk |
| DB-28 | Prune or archive the parallel legacy editions behind one labelled `/legacy/` index (delete nothing; re-point nav only) | One site story for users + crawlers | M | M | build + legacy nav | owner (design decision) |
| DB-29 | Image policy enforcement: generated illustration only, or seller images with written licence — audit current front-page art against `review/images.html` | Legal hygiene | S | M | `review/images.html` | desk |
| DB-30 | Quarterly content refresh SLA: every guide reviewed ≤ 90 days; `dateModified` bumped honestly only when content changed | Freshness without dishonesty | S (recurring) | M | build, `src/data/` | desk |

---

## 4. The design prompt (paste-ready)

Use this as the prompt for a designer, an LLM design tool, or a front-end agent. It is
self-contained and assumes no other context.

> **Role:** Senior editorial product designer + front-end engineer for a compliant Amazon
> Associates publication.
>
> **Site:** "Crisp & Counter" — a buying-guide publication about countertop cooking
> appliances (air fryers, multi-function toaster ovens) and meat thermometers. Static site,
> served from GitHub Pages under `/Affil1/`. Build system: Python templates
> (`tools/page_*.py`) fed by `src/data/*.json`; **never hand-edit generated HTML — change
> templates and data, rebuild, `tools/check.py` must stay at 0 errors.**
>
> **Audience:** home cooks (25–55) choosing one countertop appliance; skim-readers deciding
> in under 90 seconds; they distrust hype and fine print alike.
>
> **Brand tokens (existing, keep):** paper `#fbf9f4`, card `#fffefb`, ink `#17251f`, forest
> `#1f3a30`, sage `#7d947f`, muted `#5d6f66`, amber `#b8762b` / soft `#f2e2cb`, line
> `#e2ded2`, warn `#a8451f`. Type: Fraunces (serif, display + pull quotes) and Inter (sans,
> body + UI), self-hosted woff2, no CDN. Radius 3px. Wrap 1160px. Generous whitespace,
> hairline rules, print-like rhythm. Mood: a well-run test kitchen's notebook, not a coupon
> site.
>
> **Layout system:** 12-col grid; 8-pt spacing scale; max line length 68ch; masthead + single
> disclosure strip above `<main>` on every page; footer with 3 link groups + disclosure +
> "© 2026 Crisp & Counter · As an Amazon Associate I earn from qualifying purchases."
>
> **Components to design (all states: default/hover/focus/visited):** masthead with logomark;
> disclosure strip; product card (image, name from listing, "Good if / Skip if", sponsored
> CTA button amber, `rel="sponsored nofollow noopener" target="_blank"`, "price unknown — not
> published yet" line in muted small caps); spec/comparison table (sticky first column, blank
> cells styled "not confirmed yet" with dotted underline + tooltip); guide card (question as
> headline, 6-min read badge, updated date); callout "What we don't know yet" (warn-tinted,
> links to `/review/`); ledger table (empty-state design — zero rows, beautifully); decision
> tree (3 steps); seasonal banner (thin, dismissible, no motion).
>
> **Pages to redesign (keep routes identical):** `/` front; `/guides/` hub + 7 guides;
> `/products/` + 5 product records; `/compare/`; `/questions/`; `/suggestions/` (accept / hold
> / reject cards); `/review/` (flagged-for-review as first-class transparency page);
> `/review/measurement.html`; `/about/`; `/operations/ledger.html`; `/brief/` executive summary;
> `/404.html`. Every page: skip-link, one `<h1>`, alt'd imagery, disclosure strip, footer.
>
> **Motion:** none beyond 150 ms opacity/translate on hover and a reduced-motion-safe
> accordion; no carousels, no countdowns, no ticker animation.
>
> **Imagery:** own illustration (consistent flat, warm, paper-grain style) or seller-licence
> product photos only; never Amazon hotlinks; never fake "lifestyle" stock with readable text;
> seasonal hero refreshable (Nov–Dec hosting, January meal-prep, May grilling).
>
> **Copy rules:** questions as headlines; ≤9 reading age; British-or-American English picked
> and held; banned words: "best", "ultimate", "game-changer", "in today's fast-paced world",
> "look no further", "unlock", "elevate", "delve"; no superlatives without a cited source;
> every claim of fact carries an inline source link or is framed as a question.
>
> **Compliance (hard gates, reject any output that violates):** §5 disclosure above the fold and
> in footer; outbound Amazon links tagged `?tag=shopnow047c-20`, `rel="sponsored nofollow
> noopener"`, new tab, disclosure within 200 words of each CTA; NO price/rating/review-count/
> stock anywhere; no endorsement of unverified identity; intended vs observed identifiers never
> merged; no analytics script; no cookie banner (there is nothing to consent to); no third-party
> requests.
>
> **Deliverables:** Figma library (tokens as variables) + static HTML snippets per component +
> a 1-page "front page" comp at 1440/834/375 + an imagery style frame + accessibility notes.

---

## 5. Organic-traffic plan (honest sequence)

There is **no legitimate traffic today** — the ledger is empty and Search Console is not
connected, so query demand is unmeasured. Anyone promising rankings now is guessing. The plan:

| Phase | Weeks | Actions | Gate to next phase |
|---|---|---|---|
| 1. Instrument | 1–2 | Owner decides collector host; deploy; verify 5 events + DNT/GPC; publish retention note | DB-21 + DB-22 pass (one attributed click) |
| 2. Index | 1–2 | Search Console + Bing; submit sitemap; fix coverage errors; DB-15 (orphan guides) | ≥90% indexed |
| 3. Foundation topics | 2–6 | Publish from the 4 existing question-shaped hypotheses + meal-prep/small-kitchen/thermometer guides; internal link clusters (DB-06/19) | 4 guides live + linked |
| 4. Observe | 4–8 | Weekly 20-query review; log ledger rows only from authorized reports (DB-23) | ≥1 query with impressions > 25 |
| 5. Compound | 8–12 | Topic selection switches to measured queries; one guide/cycle; refresh SLAs (DB-30) | click-through baseline set |
| 6. Amplify (optional) | 12+ | Repurpose top guides as a genuinely useful PDF cheat-sheet; pitch to one newsletter per month; Pinterest pins of own illustrations | permission + disclosure intact |

Expected shape of results: modest, compounding, and dominated by long-tail questions ("do I need
a thermometer for turkey") rather than head terms ("best air fryer") — which is fine: the whole
site is built for decision questions, and head terms are unwinnable without authority the site
does not yet have.

### Editorial calendar (proposed; hypotheses, not demand claims)
| Month | Slot | Working title | Cluster |
|---|---|---|---|
| Nov–Dec 2026 | Season | Holiday hosting: what should a counter appliance do for you? (live) | air fryers |
| Jan 2027 | Season/New-year | Meal-prep Sunday: is a 6-qt basket enough? (live) | air fryers |
| Jan 2027 | New-year | Small-kitchen counters: measure twice, buy once (live) | air fryers |
| Feb 2027 | Valentine | Two-zone dinners without tears (dual-basket angle) | air fryers |
| Mar 2027 | Spring | Whole-bird turkey/chicken without oven space — thermometer-first guide (live) | thermometers |
| May 2027 | Grilling season | Instant-read vs wireless probe: what a thermometer actually changes | thermometers |
| Jun 2027 | Summer | Small-batch frozen snacks: capacity myths | air fryers |
| Nov 2027 | Holiday | Holiday hosting, 2nd edition — refresh with measured queries | air fryers |

Cadence rule: **one guide per review cycle, only if a query or reader-need warrants it.** No
fixed volume targets.

---

## 6. Decision-making improvements (how to pick without guessing)

1. **Evidence gate before score.** A suggestion enters scoring only with (a) a linked source,
   (b) a measurable success condition, (c) a falsifier ("we'll know it failed if…").
2. **Score on two axes only** — buyer utility, findability — then effort. Ties break toward
   compliance-risk reduction. No "alignment/adjacency" vibes scoring.
3. **Blanks stay blank.** If a field cannot be sourced (price, rating, commission, search
   volume), it renders "not confirmed" — never interpolated.
4. **Two-person rule for anything touching links:** one builds, one verifies the rel, tag, and
   URL in the rendered page (CI catches most; humans catch the rest).
5. **Weekly 15-minute review** against `operations/ledger.html`; monthly pruning of accepted-but-
   stalled items back to `hold`.
6. **Stop-loss:** if after DB-15/16/21/22 the site records zero impressions and zero indexed
   errors in 45 days, halt new publishing and fix discoverability before anything else.

---

## 7. Anti-patterns this brief forbids (the "AI slop" checklist in reverse)

- Stock-photo heroes of hands sprinkling flour · countdown timers · "Only X left in stock"
- "In today's fast-paced world…" · "Looking for the best X? Look no further!" · unlock/elevate/delve
- Superlatives without sources · unverified "10,000+ five-star reviews" claims
- Walls of keyword-stuffed FAQ · unlabelled AI-generated "reviews" of hands-on experience
- Carousel dependence · auto-playing video · newsletter modals over content
- Hiding or shrinking the disclosure; adding prices without an Amazon-served feed
- "Verified purchase" language for products nobody verified
- Merge-happy "comprehensive 4,000-word guide" padding; instead: cut until only buyer questions remain

---

## 8. What only the owner can decide (not agents, not the desk)

1. **Consolidation:** merge/retire the parallel editions (`crisp/`, legacy root pages) — one
   site or two? Design and nav depend on this.
2. **Associates reality:** enrollment status, intended ASINs, rate card, click/conversion
   reports. Everything in the ledger and "trending" analysis waits on this.
3. **Authorship:** named human editor (recommended, even if a shared byline) vs anonymous desk.
4. **Collector host & privacy notice** for analytics (DB-21), and Search Console verification (DB-16).
5. **Brand consolidation & imagery budget** (DB-01/04/28).
6. **Decision on the Special Links** to ship publicly once the one-link test passes (DB-22).

---

## 9. Sources (fetched 2026-11-20 by this session or cited from the register)

- Amazon Associates Operating Agreement — updated 2025-10-15 (§1 Special Links; §5 disclosure verbatim; §12 incorporation of Program Policies): https://affiliate-program.amazon.com/help/operating/agreement
- Amazon Associates Program Policies (§2(b) price/availability; incorporated via §12): https://affiliate-program.amazon.com/help/operating/policies
- FTC Endorsement Guides: What People Are Asking (2023 rev.; affiliate marketing Q&A): https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
- FTC Endorsement Guides, 16 CFR Part 255: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255
- Google Search Central — Qualify your outbound links (`sponsored`): https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
- Amazon (Sell on Amazon) — Understanding ASINs, 2025-06-04 (10-character alphanumeric; after `/dp/`): https://sell.amazon.com/blog/what-is-an-asin
- Repo-internal evidence: `src/data/products.json`, `src/data/compliance.json`, `src/data/flags.json`, `review/index.html` (FLG-001…FLG-017), `docs/MEASUREMENT.md`, `COORDINATION.md`

*No claim in this brief about demand, price, rating, availability, commission, or search volume
is a fact; all are marked as hypotheses or blocked on account access.*
