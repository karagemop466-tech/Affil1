# Crisp & Counter

A static Amazon affiliate publication about five kitchen products: two air
fryers, one French-door air-fryer oven and two meat thermometers.

**Live:** <https://karagemop466-tech.github.io/Affil1/>

It is built to one rule: **claim nothing that cannot be sourced.** That shows up
as an absence of prices, star ratings, test results and winners, and as a review
page that publishes every gap instead of hiding it.

---

## What is here

| Path | What it is |
|---|---|
| `index.html` | Shop front. Products led by the job each one does, then guides. |
| `products/` | The five-product register plus one record per product. |
| `categories/` | Air fryers and thermometers, generated from the same register. |
| `guides/` | Six question-shaped buying guides. |
| `compare/` | Every product side by side, with blank columns left blank. |
| `calendar/` | The publishing calendar: dated slots, a state per slot, one slot reserved for a measured query. |
| `questions/` | 16 questions, 5 answered with a source, 11 open with the artefact that would close each, plus five discovery routes. |
| `suggestions/` | 17 proposals in one decision table with an ordered path and an accept / hold / reject control per row. |
| `review/` | 19 flags, image policy, measurement plan. |
| `about/` | Editorial rules, disclosure, sources with quoted wording. |
| `operations/` | The empty campaign ledger and its provenance rule. |
| `brief/` | Executive summary. |
| `privacy.html` | Generated from the collector's own field list. |
| `src/data/` | The single source of truth. Every fact on the site comes from here. |
| `tools/` | `build.py` renders the site; `check.py` verifies it. |
| `analytics/` | The self-hosted collector. Off, and documented as off. |

## Build

No dependencies. Python 3.9+ and nothing else.

```bash
python3 tools/build.py    # regenerate every page from src/data
python3 tools/check.py    # verify the rules below; exits non-zero on failure
python3 tools/check_local_links.py   # relative links and assets across every served page
```

`.github/workflows/pages.yml` runs all three on every push and pull request, then
fails the build if the output is not reproducible from `src/data` — which is how
a hand-edited page gets caught.

## The rules `check.py` enforces

Each rule exists because the site makes a matching claim somewhere.

1. **The disclosure strip is above `<main>` on every page** and repeated in the
   footer. Required by Associates Operating Agreement §5; placed high because the
   FTC says a footer-only disclosure is easy to miss.
2. **Every Amazon product link carries `?tag=shopnow047c-20`** (Program Policies
   §2(b) requires the Associates ID as a URL parameter) **and**
   `rel="sponsored nofollow noopener"`, and opens in a new tab. Google documents
   `sponsored` as the marker for paid links. A link missing either fails the
   build — this was a real defect once; see FLG-018.
3. **No price, star rating, review count or stock phrase appears in visible text.**
   Associates Program Policies §2(b) permits those only from Amazon-served data or
   the Creators / Product Advertising API. Neither is connected.
4. **No test or ranking claim.** Nothing on this site was tested, so no page may
   say otherwise.
5. **No root-absolute internal links.** GitHub Pages serves this repository from
   `/Affil1/`, so `/about/` would 404. Every link is relative and resolved.
6. **No external resource loading.** Fonts are self-hosted. There is no CDN, no
   third-party analytics, no third-party request of any kind.
7. **Every internal link and anchor resolves**, the sitemap matches the built
   pages exactly, and every feed item points at a real page.
8. **One `<h1>` per page**, every image has alt text, no inline event handlers.
9. **The publishing calendar cannot promise a page that does not exist**, and
   every guide appears on it.
10. **The privacy notice describes the collector that exists**, field by field.
11. **The analytics client honours Global Privacy Control and Do Not Track** and
    stores no persistent identifier.

## Editing content

Change `src/data/*.json` or `tools/content.py`, then rebuild. Never edit a
generated `.html` file: the CI reproducibility step will fail, which is exactly
the intent.

Product identity lives in `src/data/products.json`. Three pairs of fields are
deliberately separate and must never be merged:

| Pair | What each side is |
|---|---|
| `intended_asin` / `observed_asin` | What the publisher meant to ship vs. what the link actually opened |
| `listing_url` / `special_link` | The URL that was observed vs. the tagged URL the site now serves |
| `submitted_link` / `listing_url` | The short link supplied vs. the listing it reached |

## What is not connected

- No Amazon Product Advertising API / Creators API credentials.
- No Associates account access, so no confirmed intended ASINs, rate card or
  click report.
- No analytics endpoint deployed. `assets/js/analytics.js` is inert by default,
  and the collector in `analytics/collect.py` has been tested but is not hosted.
- No Search Console property. No Bing Webmaster property.
- No named author.

Every one of those is on the review page rather than described here as a future
intention.

## Earlier editions

`main` also carries a second edition (`crisp/`) and a set of root-level pages
(`products.html`, `dashboard.html`, `guides.html`, …) built by parallel sessions.
They are kept as a record: nothing was deleted. They are excluded from the
sitemap and from `robots.txt`, and each carries a one-line banner pointing at the
current version. The maintained edition is the site root.
