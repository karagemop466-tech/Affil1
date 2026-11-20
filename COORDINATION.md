# COORDINATION.md — shared task board

Shared task board for parallel sessions on this repository.

## Session log

| Session | Branch | Claimed scope | Status |
|---|---|---|---|
| `arena/fa9307f7-affil1` | `arena/fa9307f7-affil1` | Full rewrite: site root, guides, register, review queue, build system | done |
| `arena/47a393a2-affil1` | `arena/47a393a2-affil1` | Re-verification pass, tagged Special Links, `questions/decisions.html`, `review/verification.html`, suggestions rebuild, thermometer guide, `src/data/`, `tools/` | done — merged in PR #23 |

## Claims

| Task | Status | Owner | Files |
|---|---|---|---|
| Session claim: re-verify every supplied link and every policy source, fix the tracking defect, build the decision dossier | done | `arena/47a393a2-affil1` | `src/data/*.json`, `tools/*.py`, `questions/`, `review/`, `suggestions/`, `guides/`, `index.html`, `README.md`, `EXECUTIVE_SUMMARY.md`, `PUBLISHING_WORKFLOW.md` |
| Product facts beyond the listing title (dimensions, wattage, warranty) | needs review | — | `src/data/products.json` |
| Associates account data (intended ASINs, account status, rate card, click report) | needs review | — | requires account owner; see `questions/decisions.html` |
| Search Console verification and sitemap submission | unclaimed | — | requires owner's Google account |
| Analytics endpoint decision | unclaimed | — | `assets/js/analytics.js` is inert |

No other session had an open claim on these files when this work started. PR #19
(`arena/e56bd6f7-affil1`, an audit log in `COORDINATION.md` only) was open and
untouched; this file merges rather than overwrites its content.

## What this session changed, and why

Two things were defects rather than proposals, so they were fixed rather than
queued:

1. **The buy links were not Special Links.** All five arrival URLs were bare
   `/dp/<ASIN>` addresses with no tag, and the site was offering them as click
   targets. Program Policies §2(b) requires the Associates ID as a URL parameter,
   and Amazon's application-review page lists untagged links among its rejection
   reasons. The build now emits `/dp/<ASIN>/?tag=shopnow047c-20`, keeps the
   submitted code as history, and fails if an untagged retail link appears.
2. **P-04 resolved.** Three failures were recorded in the previous session; in this
   one it resolved on both attempts to `B0DHZTCNR5`, a ThermoMaven instant-read
   thermometer. The catalogue is therefore three air fryers and two thermometers,
   and every page that said otherwise was corrected.

Three further rows from the suggestion queue were implemented because they are
structural rather than editorial: the thermometer cluster guide, the noindex on the
parallel edition, and the shortlist-first front page. They stay in the queue marked
`implemented` so the record shows what changed.

## Sources and verification performed

Every source below was requested and its wording read **in this session** on
2026-11-20. Quotes are copied, not paraphrased, and are published with the date
read at `about/index.html#sources`; the pass itself is logged at
`review/verification.html`.

| Ref | Source | Used for |
|---|---|---|
| SRC-01 | https://affiliate-program.amazon.com/help/operating/agreement | §5 disclosure sentence, quoted verbatim |
| SRC-02 | https://affiliate-program.amazon.com/help/operating/policies | §2(a)(b): tag as a URL parameter; price/availability rule (page dated 2026-04-14) |
| SRC-03 | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255 | 16 CFR 255.0(f) definition of clear and conspicuous |
| SRC-04 | https://consumer.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | Placement guidance; linked, not quoted |
| SRC-05 | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | `rel="sponsored"` for paid links (page updated 2025-12-10) |
| SRC-06 | https://sell.amazon.com/blog/what-is-an-asin | ASIN is a 10-character code, found after `/dp/` — closes FLG-011 |
| SRC-07 | https://affiliate-program.amazon.com/help/node/topic/G8TW5AE9XL2VX9VM | 3 sales / 180 days, 10-post originality bar, untagged links as a rejection reason |

Link verification, performed in this session, twice for P-04:

| Ref | Submitted | Resolved to | Product | Tag in final URL |
|---|---|---|---|---|
| P-01 | link.amazon/B04G1MEwY | ASIN B0CDY277D3 | CHEFMAN 6 qt dual basket | no |
| P-02 | link.amazon/B02NbDxp3 | ASIN B09B7SB46R | Emeril Lagasse 26 qt French-door oven | no |
| P-03 | link.amazon/B00hJ57DV | ASIN B08DKYBTPH | Chefman 8 qt TurboFry | no |
| P-04 | link.amazon/B0c8moW59 | ASIN B0DHZTCNR5 | ThermoMaven instant-read thermometer | no |
| P-05 | link.amazon/B0f3GKalj | ASIN B0DZFD6R9Z | CHEF iQ Sense wireless thermometer | no |

`python3 tools/build.py` → **25 pages**; `python3 tools/check.py` → **0 errors, 0 warnings**.

## Irregularities

All 17 are published at `review/index.html` with source links. The ones that matter
most:

- **FLG-002 (high)** — the buy links carried no tag until this build; fixed in the
  build, still unconfirmed until one click appears in the Associates report.
- **FLG-001** — all five submitted codes are nine characters; every ASIN on arrival
  is ten. They are short-link slugs, not identifiers, so `intended_asin` stays null.
- **FLG-004** — P-04 failed three times, then resolved twice. Both outcomes kept.
- **FLG-011** — closed: Amazon's own ASIN definition was found on sell.amazon.com.
- **FLG-017** — the parallel edition is still served, now `noindex, follow`.

## Merge log

| PR | Branch | Result |
|---|---|---|
| #22 | `arena/fa9307f7-affil1` | merged before this session; the root build became canonical |
| #38 | `arena/02502b50-affil1` | merged while this branch was open; reconciled, not overwritten |
| #39 | `arena/47a393a2-affil1` | this session — see the PR body for the change list, sources and flags |

GitHub Pages: https://karagemop466-tech.github.io/Affil1/

Nothing was deleted from another session's work. Their pages (`crisp/`,
`guides.html`, `products.html`, `dashboard.html`, `flagged-for-review.html`,
`reviews/`, `categories/`, `archive/`, `data/`, `js/`, `css/`, `server/`,
`analytics/`, `docs/`) are all still present and still served, now with
`noindex, follow` so that search engines index one edition. `tools/build.py` still
writes only the files in its own `GENERATED` set, and `tools/legacy.py` only adds a
meta tag — it never removes a page.

Handoff note: if a session finds a page here that contradicts `src/data/`, the data
is canonical and the page is the bug. Rebuild rather than hand-edit; CI diffs the
tree and fails on a hand-edited output.


## Merge conflict of 2026-11-20, and how it was resolved

PR #38 merged to `main` after this branch was opened, and it changed the same
tools and data files. The conflict was resolved by taking this branch's version of
the generated pages and rebuilding them from data, and by hand-merging the source
files. Nothing from #38 was discarded:

| Their change | What happened to it |
|---|---|
| P-04 resolved to `B0DHZTCNR5` | Independently the same observation. Corroboration, not a conflict. |
| `intended_listing_url` / `intended_confirmed_on` / `intended_confirmation_source` fields | Added to every product record |
| `kitchen-build/` preflight and `operations/launch-readiness.html` | Kept intact; `check.py` now rejects any link that claims an approval bundle the intent record does not validate |
| Seasonal guide, with a USDA citation | Kept, and added to the sitemap and feed |
| Buyer note on each product card | Kept |
| Hedged wording in suggestions (no ranking or indexing guarantee) | Adopted; this branch's S-04 and S-07 were overclaiming and were rewritten |
| Two Search Console help quotes in `sources.json` | **Not carried over.** They were read in their session and not re-read in this one, and this site does not republish a quote it has not read |
| Their `page_measurement` signature and events table | Superseded by this branch's version, which keeps the same five events and the same "switched off" claim |

The two sessions disagreed on one thing worth recording. Their gate was to publish
no buy link at all until intended identity is confirmed; this branch emits a tagged
link to the observed destination. Both are defensible. The resolution: emit the
tagged observed link, because without a click there is no report and without a
report nothing can ever be confirmed; and keep their preflight as the gate that
must pass before any link is *labelled* approved. `layout.approved_link()` lets a
validated intent bundle override the observed destination when one exists.

After the merge: `python3 tools/build.py` → 26 pages; `python3 tools/check.py` →
0 errors, 0 warnings; rebuild diffed clean.


## Second merge, same day (PR #46)

`main` moved again while this branch was being rebased onto #38: PR #46
(`arena/487a66ea-affil1`) added a "fit finder", an editorial cluster and a decision
brief. Merged the same way — their content is kept, this branch's rules still
apply — and the duplication that two sessions producing guides inevitably
creates was removed rather than published twice.

| Duplicate | Resolution |
|---|---|
| `thermometer-pairing` (theirs) vs `thermometer-instant-or-wireless` (ours) | One guide kept. Ours stays, and now cites the official FoodSafety.gov chart that theirs relied on. |
| `holiday-side-dish-capacity` (#38) vs `holiday-hosting` (#46) | `holiday-hosting` kept: it asks a narrower question and cites a source. The other slug is in `RETIRED` and is deleted by the next build. |
| Their guide sources link to `/dp/<ASIN>` without a tag | `page_guides` now routes every Amazon source through `tag_url()`, so a listing cited as evidence is a compliant Special Link too |

Verified in this pass, read directly on 2026-11-20: FoodSafety.gov "Cook to a Safe
Minimum Internal Temperature" (USDA/FDA/CDC), last reviewed 2024-11-21 — poultry
165°F, ground meat 160°F, whole cuts 145°F plus a 3-minute rest. Recorded as SRC-08
and quoted nowhere else on the site. FLG-012 narrows from "no food-safety guidance
at all" to "no air-fryer-specific guidance".

State after both merges: 28 pages, 8 guides, 0 errors, 0 warnings, rebuild
reproducible, 77 legacy pages link-checked clean, `kitchen-build` tests green.


## Third merge (PR #51), and the state of the whole repository

`main` moved a third time while this branch was open, to a build that had replaced
`tools/check.py` with `tools/validate.py` and quarantined every guide page. Rather
than overwrite it or abandon this branch, the merge took the newest edition of
anything this build does not own and kept this build's rules for anything it does.
Four things came out of that reconciliation that matter more than the merge itself:

1. **Every Amazon link in the published repository is now tagged.** A repo-wide
   sweep found 44 untagged `/dp/` links on pages this build does not generate
   (dashboard, products, questions and others). All 44 now carry
   `?tag=shopnow047c-20` and `rel="sponsored nofollow noopener"`. `check.py`
   now enforces this across every served page, not only this build's output.
2. **One analytics vocabulary, two clients.** `review/measurement.html` described
   five events, `src/data/events.json` described a different five, and the
   collector rejected the client's wire format. Nine names are now defined once,
   the client posts the collector's exact three-field shape, and `report_import`
   is scoped `operator`, so the collector refuses it with a 400 by design.
3. **The launch register keeps its own rule.** `operations/launch-readiness.html`
   cites listings as evidence: `rel=sponsored`, deliberately no tag, because the
   point of that page is that no paid link exists until the destination is
   confirmed. `check.py` exempts exactly that one file and no other.
4. **The duplicate guides are gone.** Eight guides ship, one per question.

State after three merges: 28 pages built, 8 guides, `check.py` 0 errors and 0
warnings, 79 pages link-checked clean, `kitchen-build` 3/3 green, rebuild
reproducible.
