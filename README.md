# Crisp & Counter

A static Amazon affiliate publication about air fryers and one meat thermometer.
Live at **https://karagemop466-tech.github.io/Affil1/**

It is built to one rule: **claim nothing that cannot be sourced.** That shows up
as an absence of prices, ratings, test results and winners, and as a review page
that publishes every gap instead of hiding it.

---

## What is here

| Path | What it is |
|---|---|
| `index.html` | Front page. Leads with products and guides. |
| `guides/` | Four question-shaped buying guides. |
| `products/` | The five-link register plus one record per product. |
| `compare/` | Every product side by side, with blank columns left blank. |
| `questions/` | 15 questions, 4 answered with evidence, 11 open with the artefact that would close each. |
| `suggestions/` | 12 proposals with an accept / hold / reject control per row. |
| `review/` | Flagged for review, image policy, measurement plan. |
| `about/` | Rules, disclosure, privacy, and the source list with quoted wording. |
| `operations/` | The empty campaign ledger and its provenance rule. |
| `brief/` | Executive summary. |
| `src/data/` | The single source of truth. Every fact on the site comes from here. |
| `tools/` | `build.py` renders the site; `check.py` verifies it. |

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
   FTC says a footer-only disclosure is easy to miss.
2. **Every Amazon product link carries `rel="sponsored nofollow noopener"`** and
   opens in a new tab. Google documents `sponsored` as the marker for paid links.
3. **No price, star rating, review count or stock phrase appears in visible text.**
   Associates Program Policies §2(b) permits those only from Amazon-served data or
   the Creators API / Product Advertising API. Neither is connected.
4. **No test or ranking claim.** Nothing on this site was tested, so no page may
   say otherwise.
5. **No root-absolute internal links.** GitHub Pages serves this repository from
   `/Affil1/`, so `/about/` would 404. Every link is relative and resolved.
6. **No external resource loading.** Fonts are self-hosted from `assets/fonts`.
   There is no CDN, no analytics script, no third-party request of any kind.
7. **Every internal link and anchor resolves**, the sitemap matches the built
   pages exactly, and every feed item points at a real page.
8. **One `<h1>` per page**, every image has alt text, and no inline event handlers.

## Editing content

Change `src/data/*.json` or `tools/content.py`, then rebuild. Never edit a
generated `.html` file: the CI reproducibility step will fail, which is exactly
the intent.

Product identity lives in `src/data/products.json`. The `intended_asin` and
`observed_asin` fields are deliberately separate and must never be merged — see
`review/index.html#FLG-001` for why.


## Coexistence with the merged parallel edition

`main` also contains a second edition built by a parallel session: a `crisp/`
sub-site plus root pages such as `products.html`, `questions.html`,
`dashboard.html` and `flagged-for-review.html`. It independently reached the same
five link resolutions recorded here, which is why the two data files agree.

This build owns the site **root** and writes only its own generated files; the
other edition's pages are untouched and remain reachable. Running
`python3 tools/build.py` therefore cannot damage them. Merging the two editions
into one was deliberately not attempted here: it is a design decision, and the
brief says shared navigation and index files change only in a final integration
pass.

## What is not connected

- No Amazon Product Advertising API / Creators API credentials.
- No Associates account access, so no intended ASINs, rate card or click report.
- No analytics endpoint. `assets/js/analytics.js` is inert by default.
- No Search Console property.
- No named author.

Every one of those is published on the review page rather than described here as
a future intention.

### Publication edition and release order

The custom Actions deployment (when selected as the Pages source) packages only the maintained edition (`python3 tools/stage.py _site` after building). Older parallel editions remain in Git, not in that artifact. While legacy branch publishing is configured, GitHub still serves the committed root; the sitemap and navigation point to the maintained edition only. The sitemap and RSS feed are generated by the build; never edit them by hand.

1. Establish measurement first: deploy the collector outside Pages, document retention and consent, and verify test events before enabling the client. Orders belong in authorized Associates reports, not browser events. Until then there is no conversion baseline.
2. Validate one Special Link per intended ASIN in the enrolled Associates account. Record intended ASIN, official URL, confirmation date and source independently of the observed redirect. Release a replacement only after the destination and click report agree. `shopnow047c-20` is supplied, not confirmed.
3. After measurement is live, review Search Console queries and click counts every two weeks. Draft one guide per review cycle only when the query and reader need warrant it. Good hypotheses: “Will a tray air fryer fit under my cabinets?” and “One basket or two for dinner and a side?” Neither has verified demand. Add each accepted guide to the generated sitemap and feed.
4. Use AI for outlines and evidence-gap checks, not for claims or automatic publication. A reviewer must check each claim against a linked official source, check nearby disclosure and API permissions, and approve the draft before release. Do not call a product trending or profitable until the underlying data exists.
