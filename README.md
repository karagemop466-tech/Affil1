# Crisp & Counter

A static Amazon affiliate publication about air fryers and thermometers.
Live at **https://karagemop466-tech.github.io/Affil1/**

It is built to be a shop a reader can act on, with one rule underneath:
**claim nothing that cannot be sourced.** So there are no prices, ratings, review
counts or test results — and a review page that publishes every gap instead of
hiding it.

## Build and test

## The site, in one table

The brief had five parts. This is where each one lives:

| The ask | Where it is answered |
|---|---|
| `index.html` | Publication front page: the edit, two categories, three decision paths, a seasonal feature, the journal |
| `products/` | The shop: five picks in two categories, plus one note per product |
| `guides/` | Nine question-shaped buying guides, clustered by the decision they answer |
| `compare/` | Every product side by side, with blank columns left blank |
| `questions/` | 22 questions a real decision depends on: what is known, what is missing, what would close it |
| `suggestions/` | Three paths and 18 proposals, 8 already implemented, with a decision control per row |
| `review/` | Flagged for review, image policy, measurement plan |
| `about/` | Rules, disclosure, privacy, and the full source list with quoted wording |
| `operations/` | The empty campaign ledger and its provenance rule |
| `brief/` | Executive summary |
| `src/data/` | The single source of truth. Every fact on the site comes from here |
| `tools/` | `build.py` renders the site; `check.py` verifies it |
| `archive/legacy-2026-11-20/` | The superseded edition, kept with `noindex` on every page |

## Layout

```
index.html            publication front page          ← generated
guides/<slug>/index.html  9 buyer guides              ← generated
compare/ products/ topics/ about/                     ← generated
sources/ suggestions/ questions/ flagged/              ← generated
dashboard/            entries, verification, ledger    ← generated
404.html              not-found page                   ← generated
assets/css/site.css   the only stylesheet
assets/js/events.js   the five defined events, inert until an endpoint exists
assets/js/shortlist.js  "Save" on a product card; localStorage only, nothing sent
assets/img/*.jpg      commissioned illustrations (not product photography)
src/data/*.json       every fact the site publishes, with its source
tools/build.py        data → HTML (one template for nav, disclosure, footer)
tools/check.py        the gate: links, images, disclosure, sponsored marking, the
                      Associates tag on every served page, price prohibition,
                      sitemap/feed agreement, and the one-event-per-request rule
tools/check_deploy_paths.py  resolves every reference over HTTP at the /Affil1/ mount
tools/verify_links.py re-resolve the register against Amazon and report drift
archive/              five earlier competing surfaces (four storefronts and a parallel
                      integration pass), preserved untouched and non-indexable
```

The Python server serves **only** `dist` on port 8000. It enables five same-origin events, honors DNT/GPC, and writes daily aggregate counts to SQLite outside the web root. `PORT` and `COUNTER_DB` are configurable. Use a durable non-public database for an authorized production host. No raw event ingestion, cookies, visitor IDs, referral strings or IP logging by the collector. Do not import preview tests into the campaign ledger.

GitHub Pages serves static HTML. Its client sends no analytics requests. Native branch publishing uses `_config.yml` exclusions to avoid publishing historical editions or source data. Workflow-based Pages uses `tools/stage.py`. Keep both scopes aligned. No other domains or editions are submitted in the sitemap.

## Editorial cadence

1. **The disclosure strip is above `<main>` on every page** and repeated in the
   footer. Required by Associates Operating Agreement §5; placed high because the
   FTC says the closer a disclosure is to the recommendation, the better.
2. **Every Amazon product link carries the Associates tag** `?tag=shopnow047c-20`
   *and* `rel="sponsored nofollow noopener"`, and opens in a new tab. The tag is
   required by Program Policies §2(b); `sponsored` is the marker Google documents
   for paid links.
3. **No price, star rating, review count or stock phrase appears in visible text.**
   Program Policies §2(b) permits those only from Amazon-served data or the
   Creators API / Product Advertising API. Neither is connected.
4. **No test or ranking claim.** Nothing on this site was tested, so no page may
   say otherwise.
5. **No root-absolute internal links.** GitHub Pages serves this repository from
   `/Affil1/`, so `/about/` would 404. Every link is relative and resolved.
6. **No external resource loading.** Fonts are self-hosted from `assets/fonts`.
   There is no CDN, no analytics script, no third-party request of any kind.
7. **Every internal link and anchor resolves**, the sitemap matches the built
   pages exactly, and every feed item points at a real page.
8. **One `<h1>` per page**, every image has alt text, and no inline event handlers.
9. **One site only.** Any `.html` file in the tree that this build did not
   generate, and that is not under `archive/`, fails the build.
10. **The published artifact is the generated set.** `tools/stage.py` copies only
    generated pages plus assets into `_site`, so archived editions can stay in
    the repository without being published.

## The rules this site publishes under

Each rule below is enforced by `tools/check.py`, not just asserted in prose:

Product identity lives in `src/data/products.json`. The `intended_asin` and
`observed_asin` fields are deliberately separate and must never be merged — see
`review/index.html#FLG-001` for why. Buy destinations are built in exactly one
place, `layout.buy_url()`, so the tag cannot be forgotten on one page and
remembered on the next.

## What is verified, and how

Five supplied links were opened on 2026-11-20 and each resolved to a live Amazon
listing. The ASIN, page title and category breadcrumb were transcribed:

| Ref | Submitted | Landed on |
|---|---|---|
| P-01 | link.amazon/B04G1MEwY | B0CDY277D3 — CHEFMAN 6 Quart Dual Basket |
| P-02 | link.amazon/B02NbDxp3 | B09B7SB46R — Emeril Lagasse 26QT French Door |
| P-03 | link.amazon/B00hJ57DV | B08DKYBTPH — Chefman 8 Qt TurboFry |
| P-04 | link.amazon/B0c8moW59 | B0DHZTCNR5 — ThermoMaven digital meat thermometer |
| P-05 | link.amazon/B0f3GKalj | B0DZFD6R9Z — CHEF iQ Sense wireless probes |

Policy wording was read from the Operating Agreement §5, the Program Policies
§2(a)/(b), the FTC's endorsement FAQ and Google's outbound-link documentation in
the same session. All four are quoted, with links, on `about/index.html#sources`.

## The one finding that decides whether this site can earn

- No Amazon Product Advertising API / Creators API credentials.
- No Associates account access, so no confirmed click attribution, rate card or
  click report.
- No analytics endpoint. `assets/js/analytics.js` is inert by default.
- No Search Console property.
- No named author.
- No mailing list; RSS is the only return channel.

## Design layer

Typefaces are self-hosted (Fraunces for display, Inter for text) — no external font
request, so nothing leaks a reader's visit to a third party and the page paints without
a network round trip. Editorial art is generated for this publication, shipped in
width variants with `srcset`, and captioned on every use as an illustration: never a
listing photo, never a brand mark, never in a slot that imitates one. The rule and the
reason sit in `src/data/images.json`, carried over from the parallel integration pass
whose artwork and typography this site adopted.

## Open questions and blockers

Twenty-two are listed at [/questions/](https://karagemop466-tech.github.io/Affil1/questions/)
with the information each one needs. Five were answered by this pass. The ones that
block everything else, in order:

1. **Enrolment** — is `shopnow047c-20` an active tracking ID, and is this site listed
   in the account? No claim is made either way here.
2. **Special Links** — regenerate all five destinations in Associates Central and
   confirm one click in the report before publishing more.
3. **Search Console** — verify the property. Until then, every statement about what
   readers want is reasoning, not evidence.
4. **An author** — a named human with two true biographical sentences. Bylines stay at
   desk level because inventing a person who tested these machines would be a
   fabricated endorsement.

## Editorial rule, in one line

A capability sentence is published only when it quotes the seller's own listing title,
attributed as such; nothing on this site claims a product was tested, and no figure
appears that cannot be traced to an official source.

## Licence and trademark note

Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates. This
site is not endorsed by or affiliated with Amazon beyond participation in the Associates
Program. All listing titles are quoted for identification and are the property of their
sellers. Illustrations were made for this publication and are captioned as such.
