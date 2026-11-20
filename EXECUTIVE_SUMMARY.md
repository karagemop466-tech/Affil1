# Affil1 — Executive summary

**Project:** Amazon Associates site for countertop cooking appliances (Air fryers, accessories, multi-function appliances)
**Branch:** `arena/4772a1e3-affil1` (base `4ee0e7b`, main after PR #21)
**Tracking ID:** `shopnow047c-20`
**Prepared:** 2026-11-20 (reconciled by session arena/4772a1e3-affil1)

## What this is
A buyer-facing affiliate publication — **Good Measure — Kitchen Notes** — with a sister
editorial edition (**Crisp & Counter**, under `crisp/`). It reads like a shop, not an audit:
products lead the front page, every page carries an above-the-fold disclosure, and every
outbound product link is marked sponsored.

## Products submitted (5) — what we actually know
Two independent verification passes were run on 2026-11-20. They disagree for three of the
five links. Both are recorded in full and are **never merged**.

| # | Submitted code | Pass 1 (04:xx–05:0xZ) | Pass 2 (05:15–05:22Z) | Status |
|---|---|---|---|---|
| 1 | `B04G1MEwY` | listed `dp/B0CDY277D3` (CHEFMAN 6 Quart Dual Basket) | same listing | observed, unconfirmed |
| 2 | `B02NbDxp3` | unresolved / checkpoint (crisp FLG-005 agrees) | listed `dp/B09B7SB46R` (Emeril Lagasse 26QT) | **conflict logged** |
| 3 | `B00hJ57DV` | Amazon homepage reached | listed `dp/B08DKYBTPH` (Chefman 8 Qt TurboFry) | **conflict logged** |
| 4 | `B0c8moW59` | Amazon checkpoint gate | Amazon checkpoint gate | **unresolved** |
| 5 | `B0f3GKalj` | Amazon homepage reached | listed `dp/B0DZFD6R9Z` (CHEF iQ Sense wireless meat thermometer — **not an air fryer**) | **conflict logged · IR-5** |

Intended ASIN is unknown for all five: the submitted codes are 9 characters; Amazon defines an
ASIN as 10. The submitter's intent is **never inferred**. Identity, tracking and commission
rates all require the enrolled Associates account and remain blank.

**Never do:** assert the supplied links are invalid; merge pass-1 and pass-2 records; display
prices/ratings/review counts/stock (Amazon serves those only via a live feed we do not have);
claim order volume or revenue.

## What is live
- `/` — rebuilt 2026-11-20: products-first front page (original generated hero art), seasonal
  reading band, open-questions strip, empty campaign ledger, how-we-work, full footer map.
- `/guides/` index + question-led guides (basket vs oven · capacity · cleanup · multi-function ·
  oven-or-air-fryer · accessories · holiday-hosting · **holiday-gift-checklist (new)**);
  one question per guide, working titles labelled as hypotheses.
- `/products.html` · `/dashboard.html` · `/categories/air-fryers.html` — register, ledger, category findings.
- `/suggestions.html` — decision queue S-001…S-014 (nothing ships unreviewed).
- `/questions.html` — open-question register Q1…Q20 (missing items say “Missing”).
- `/reviews/flagged.html` — Flagged for Review with source links. `/reviews/verification-audit.html` — pass-2 audit.
- `/design-prompt-pack.html` — **new**: the decision-gated pack to brief the next redesign
  (brand system, tokens, page inventory, editorial hypotheses H1–H6, anti-slop rules).
- `/sitemap.xml` · `/rss.xml` · `/feed.xml` — every canonical URL, stubs removed; duplicates
  consolidated via redirect stubs (nothing deleted). CI reference check now scans **all** HTML
  except `archive/`.

## Design & marketing directives (2026-11-20)
- One brand voice storefront-wide (Good Measure — Kitchen Notes; sage token system; favicon;
  shared shell unified). Remaining: retire the last legacy skins and get owner sign-off (S-007).
- Cadence proposal: one question-led guide per fortnight, chosen from measured queries once
  Search Console + analytics are live (S-008, Q14) — until then, hypotheses only.
- Original imagery only (hero + seasonal art shipped); no scraped manufacturer images (S-009).
- Reader capture stays gated on provider + privacy review (S-013, Q19); RSS is the capture path today.

## Compliance gate
Disclosure above the fold on every page + footer repeat; `rel="sponsored nofollow noopener"` on
all outbound product links; PUBLISHING_WORKFLOW.md governs publishing; FTC Endorsement Guides
and the Associates Operating Agreement (updated Oct 15, 2025) are the controlling references.

## Flagged irregularities (see `/reviews/flagged.html` + COORDINATION.md)
- FLG-001/IR-1: submitted codes are not ASINs; labels relabeled site-wide.
- FLG-002: no supplied link was observed carrying `shopnow047c-20`.
- FLG-003: compliance status of the supplied short links unresolved.
- FLG-004: commission rates require sign-in; blank by design.
- FLG-009/FLG-010: analytics endpoint designed, not deployed; ledger empty.
- FLG-011/FLG-012: Search Console and email capture require account access.
- IR-2: same-date observations disagree for 3 of 5 links (both passes retained).
- IR-5: one observed listing is a wireless meat thermometer, not an air fryer (S-012 decides).
- IR-13 (new): `js/analytics.js` (style.css pages) uses a legacy event list inconsistent with
  the canonical five events; marked with a warning comment, not silently rewritten.

## Awaiting owner decisions
S-002 (test one Special Link per product) · S-003 (analytics host) · S-007 (brand sign-off) ·
S-008 (cadence) · S-010 (Search Console) · S-012 (thermometer scope) · S-013 (email) · S-014
(redesign via the prompt pack). Full list with paths: `/suggestions.html`.

## Measurement (turned on in design, not in data)
Five defined events: `page_view`, `outbound_click`, `guide_read`, `suggestion_review`,
`session_start`. Self-hosted collector designed (`server/collect.js`); nothing deployed without
a first-party host. No cookies, no IPs, no personal data client-side.

## Bottom line
The site is launchable, honest and now internally consistent. The binding constraints are not
design — they are account access (Associates workflow, Search Console, analytics host) and a
handful of owner decisions. Everything measurable is measured empty, not guessed.
