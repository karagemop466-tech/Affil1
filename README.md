# Crisp & Counter

A static Amazon affiliate publication about three air fryers and two thermometers.
Live at **https://karagemop466-tech.github.io/Affil1/**

It is built to one rule: **claim nothing that cannot be sourced.** That shows up
as an absence of prices, ratings, test results and winners, and as a review page
that publishes every gap instead of hiding it.

---

## What is here

| Path | What it is |
|---|---|
| `index.html` | Front page. Leads with products and guides. |
| `guides/` | Five question-shaped buying guides, including the two-thermometer decision. |
| `products/` | The five-link register plus one record per product. |
| `compare/` | Every product side by side, with blank columns left blank. |
| `questions/` | 15 research questions, 6 answered with a source, 9 open with the artefact that would close each. |
| `questions/decisions.html` | **Before you decide.** 16 decisions in four ordered gates: what is known, what is missing, who can supply it, what closes it. |
| `suggestions/` | Three coherent paths and 20 proposals, each with impact, effort, risk, reversibility and the decision it depends on, plus an accept / hold / reject control per row. |
| `review/` | Flagged for review, verification log, image policy, measurement plan. |
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
   opens in a new tab, and **every retail URL carries `tag=shopnow047c-20`** as a
   parameter. The tag is not decoration: Program Policies §2(b) requires it in the
   URL of each link, and Amazon lists untagged links among its reasons for rejecting
   an application. Google documents `sponsored` as the marker for paid links.
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
   pages exactly, every feed item points at a real page, and every parallel-edition
   page is `noindex, follow` so search engines see one site.
8. **One `<h1>` per page**, every image has alt text, and no inline event handlers.

## Editing content

Change `src/data/*.json` or `tools/content.py`, then rebuild. Never edit a
generated `.html` file: the CI reproducibility step will fail, which is exactly
the intent.

Product identity lives in `src/data/products.json`. The `intended_asin` and
`observed_asin` fields are deliberately separate and must never be merged — see
`review/index.html#FLG-001` for why.


## One edition, one index

`main` also carries a second edition built by a parallel session: a `crisp/`
sub-site plus root pages such as `products.html`, `questions.html`,
`dashboard.html` and `flagged-for-review.html`. The two editions independently
reached the same five link resolutions, which is why their product facts agree.

The root build is canonical. Rather than delete another session's work,
`tools/legacy.py` marks every page outside this build's `GENERATED` set with
`noindex, follow` and points its canonical at the site root. Nothing 404s, nothing
is destroyed, and a crawler sees one shop. Whether to redirect or delete those
pages outright is decision D-11, for the owner.

## What is not connected

- No Amazon Product Advertising API / Creators API credentials.
- No Associates account access, so the intended ASIN per link, the account status,
  the rate card and the click report are all unverified.
- No analytics endpoint. `assets/js/analytics.js` is inert by default.
- No Search Console property.
- No named author.

Every one of those is published on `/questions/decisions.html` rather than
described here as a future intention.
