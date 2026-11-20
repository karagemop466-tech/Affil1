# Crisp &amp; Counter

An Amazon affiliate publication about three air fryers and two thermometers.
Live at **https://karagemop466-tech.github.io/Affil1/**

It is built to one rule: **claim nothing that cannot be sourced.** That shows up as
no prices, no ratings, no test results and no winners — and as a review page that
publishes its own gaps instead of hiding them.

---

## What is here

| Path | What it is |
|---|---|
| `index.html` | Front page. Products first, then the question-shaped guides, then the machinery. |
| `guides/` | Five guides in four topic clusters (shape, size, upkeep, thermometers). |
| `products/` | The shortlist plus one record per product, with the blanks left blank. |
| `compare/` | Every product side by side, with nothing measured. |
| `questions/` | 16 questions, 6 answered with a source, 10 open with the artefact that would close each. |
| `suggestions/` | 15 proposals with cost, risk, evidence and dependencies, 7 already implemented, each with accept / hold / reject. |
| `review/` | Flagged for review, image policy, measurement plan. |
| `sources/` | Every quotation, its URL, its page date and the retrieval date. |
| `about/` | Rules, disclosure, privacy, the publishing gate. |
| `operations/` | The empty campaign ledger and its provenance rule. |
| `brief/` | Executive summary. |
| `src/data/` | The single source of truth. Every fact on the site comes from here. |
| `tools/` | `build.py` renders the site; `check.py` verifies it; `quarantine_legacy.py` de-indexes the superseded edition. |

## Build

No dependencies. Python 3.9+ and nothing else.

```bash
python3 tools/build.py    # regenerate every page from src/data
python3 tools/check.py    # verify the rules below; exits non-zero on failure
```

`.github/workflows/pages.yml` runs both on every push and pull request, then fails
if the output is not reproducible from `src/data` — which is how a hand-edited page
gets caught.

## The rules `check.py` enforces

Each rule exists because the site makes a matching claim somewhere.

1. **The disclosure strip is above `<main>` on every page** and repeated in the
   footer. Required by Associates Operating Agreement §5; placed high because the
   FTC says a footer-only disclosure is easy to miss.
2. **Every Amazon product link carries `rel="sponsored nofollow noopener"`** and
   opens in a new tab. Google documents `sponsored` as the marker for paid links.
3. **No price, star rating, review count or stock phrase in visible text.**
   Program Policies §2(b) allows those only from Amazon-served data or the
   Creators API / PA-API. Neither is connected.
4. **No test or ranking claim.** Nothing here was tested, so no page may say otherwise.
5. **No root-absolute internal links.** GitHub Pages serves this repository from
   `/Affil1/`, so `/about/` would 404. Every link is relative and resolved.
6. **No external resource loading.** Fonts are self-hosted. No CDN, no third-party
   request of any kind.
7. **Every internal link and anchor resolves**, the sitemap matches the built pages
   exactly, and every feed item points at a real page.
8. **One `<h1>` per page**, every image has alt text, no inline handlers.

## The affiliate links

Every outbound product URL is the observed ASIN with the Associates tag attached:

```
https://www.amazon.com/dp/<observed ASIN>?tag=shopnow047c-20
```

Program Policies §2(b) requires the Associates ID as a URL parameter on each link
to an Amazon Site. `src/data/products.json` keeps `listing_url` (the bare address
that was observed) and `affiliate_url` (the tagged Special Link that is actually
used) in **separate fields**, and `check.py` fails if `intended_asin` and
`observed_asin` are ever merged.

## Editing content

Change `src/data/*.json` or `tools/content.py`, then rebuild. Never edit a
generated `.html` file: the CI reproducibility step will fail, which is the point.

## The superseded edition

`main` also contains a second edition built by parallel sessions: a `crisp/`
sub-site plus root pages such as `products.html`, `questions.html` and
`dashboard.html`. It independently reached the same five link resolutions, which is
noted on the review page as corroboration rather than copied.

Those files are **not deleted**. `tools/quarantine_legacy.py` adds
`<meta name="robots" content="noindex, follow">` and a banner pointing at the
current page, so search engines index one site while the other session's work
stays intact and reachable. Running `tools/build.py` cannot damage them: it writes
only the files in its own `GENERATED` set.

## What is not connected

- No Amazon Product Advertising API / Creators API credentials.
- No Associates account access, so no intended ASINs, rate card or click report.
- No analytics endpoint. `assets/js/analytics.js` is inert by default.
- No Search Console property.
- No named author.

Every one of those is published on the review page rather than described here as a
future intention.
