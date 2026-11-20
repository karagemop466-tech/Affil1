# Crisp & Counter

A static Amazon affiliate publication about air fryers and thermometers.
Live at **https://karagemop466-tech.github.io/Affil1/**

It is built to be a shop a reader can act on, with one rule underneath:
**claim nothing that cannot be sourced.** So there are no prices, ratings, review
counts or test results — and a review page that publishes every gap instead of
hiding it.

---

## The site, in one table

| Path | What it is |
|---|---|
| `index.html` | Publication front page: the edit, two categories, three decision paths, a seasonal feature, the journal |
| `products/` | The shop: five picks in two categories, plus one note per product |
| `guides/` | Eight question-shaped buying guides, clustered by the decision they answer |
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

## Build

No dependencies. Python 3.9+ and nothing else.

```bash
python3 tools/build.py    # regenerate every page from src/data
python3 tools/check.py    # verify the rules below; exits non-zero on failure
```

`.github/workflows/pages.yml` runs both on every push and pull request, then
fails the build if the output is not reproducible from `src/data` — which is how
a hand-edited page gets caught.

## The rules `check.py` enforces

Each rule exists because the site makes a matching claim somewhere.

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

## Editing content

Change `src/data/*.json` or `tools/content.py`, then rebuild. Never edit a
generated `.html` file: the CI reproducibility step will fail, which is exactly
the intent.

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

## What is not connected

- No Amazon Product Advertising API / Creators API credentials.
- No Associates account access, so no confirmed click attribution, rate card or
  click report.
- No analytics endpoint. `assets/js/analytics.js` is inert by default.
- No Search Console property.
- No named author.
- No mailing list; RSS is the only return channel.

Every one of those is published on the review page rather than described here as
a future intention.

### Publication edition and release order

The custom Actions deployment (when selected as the Pages source) packages only the maintained edition (`python3 tools/stage.py _site` after building). Older parallel editions remain in Git, not in that artifact. While legacy branch publishing is configured, GitHub still serves the committed root; the sitemap and navigation point to the maintained edition only. The sitemap and RSS feed are generated by the build; never edit them by hand.

1. Establish measurement first: deploy the collector outside Pages, document retention and consent, and verify test events before enabling the client. Orders belong in authorized Associates reports, not browser events. Until then there is no conversion baseline.
2. Validate one Special Link per intended ASIN in the enrolled Associates account. Record intended ASIN, official URL, confirmation date and source independently of the observed redirect. Release a replacement only after the destination and click report agree. `shopnow047c-20` is supplied, not confirmed.
3. After measurement is live, review Search Console queries and click counts every two weeks. Draft one guide per review cycle only when the query and reader need warrant it. Good hypotheses: “Will a tray air fryer fit under my cabinets?” and “One basket or two for dinner and a side?” Neither has verified demand. Add each accepted guide to the generated sitemap and feed.
4. Use AI for outlines and evidence-gap checks, not for claims or automatic publication. A reviewer must check each claim against a linked official source, check nearby disclosure and API permissions, and approve the draft before release. Do not call a product trending or profitable until the underlying data exists.
