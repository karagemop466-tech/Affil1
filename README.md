# Good Measure Kitchen

A reader-first affiliate publication for four confirmed kitchen products and one unresolved
record, with a public evidence desk behind it.

Every value on the site is read from an official source and carries a link to it. Where a value
could not be confirmed, the cell says so, the item is flagged, and the flag appears on a
**Flagged for review** page that names what would settle it. No price, rating, review count,
search-volume, click, order or revenue figure appears on any reader-facing page.

## Layout

| Path | What it is |
| --- | --- |
| `index.html` | The publication front page. Leads with the shelf. |
| `shop/` | The catalogue: `index.html` (everything), `compare.html` (side by side), and one page per category. |
| `guides/` | Six question-shaped buyer guides, grouped into six clusters. |
| `desk/` | The evidence desk: executive summary, product records, suggestions register, open questions, campaign ledger, publishing gate, method, flagged for review. |
| `assets/` | The tracker and its configuration. |
| `api/` | The self-hosted collector (Node server and Cloudflare Worker). |
| `scripts/` | The renderer and the publishing gate. |
| `site_data.py` | The single source of truth for every record, question, suggestion and flag. |
| `archive/` | Preserved work from earlier parallel sessions. Not published, not deployed. |

## Working on the site

```bash
python3 scripts/build_site.py     # render every page from site_data.py
python3 scripts/check_site.py     # run the publishing gate
```

Edit `site_data.py`, never the generated HTML. The Pages workflow re-renders the site on every
push and fails the deployment if the committed pages have drifted from the renderer, so the
repository and the published site can never disagree.

Preview locally:

```bash
python3 -m http.server 8080 --bind 0.0.0.0
```

## The publishing gate

`scripts/check_site.py` enforces the checks that can be enforced by a machine. The
**Publishing gate** page lists them next to the ones that need a person. Currently enforced:

1. The Associates disclosure sits above the masthead on every page.
2. Every Amazon product link is marked `rel="sponsored nofollow noopener"`, and every link to
   Amazon's documentation or a review page is a plain citation, not a marked placement.
3. Reader-facing pages show no price, rating, review count or availability claim.
4. No unsupportable claim language anywhere on the site. A block may declare a counted
   exemption; the design-direction block uses one, because it names the cliches it forbids.
5. Every table row carries a link, and at least one link to an official source.
6. Every internal link resolves, including the deployment base path.
7. Every page has a title, description, canonical URL and feed link.
8. The sitemap lists every page; the feed lists every guide and category.
9. No template delimiters survive rendering.
10. Every page has exactly one `h1`.

## Compliance notes

- The Associates statement appears above the masthead on every page and again in the footer.
- Outbound product links are canonical Amazon product links built from the tracking ID supplied
  by the site owner, `shopnow047c-20`. Whether that ID is enrolled on an account is **FLG-002**
  and is not asserted anywhere on the site.
- The Associates IP License permits Product Advertising Content (price, availability, ratings)
  only through the Creators API or PA API. That connection has not been made, so no
  reader-facing page displays a price or a rating. Dated observations are recorded on the desk
  with their source and their date, and that distinction is itself flagged (**FLG-013**).
- The IP License also restricts using Special Links or Program Content to develop machine
  learning models without express prior written approval. That is **FLG-008** and is flagged for
  legal review before any assistant is built.
- We have not handled the appliances we write about, and the copy does not imply that we have.
- The comparison table compares shapes, capacities, listed programs and who each machine
  suits. It deliberately does not rank, price, rate or score them.

## Measurement

The tracker (`assets/analytics.js`) and the collector (`api/`) are in the repository and are
**not deployed**. The tracker probes the collector's health endpoint and disables itself if it
does not answer, so the site never implies measurement that is not happening. The campaign
ledger is empty by design and is filled only from authorised first-party reports.

See `api/README.md` for the collector contract, what is and is not collected, and the two
deployment options.

## Deployment

`.github/workflows/pages.yml` renders the site, runs the gate, and deploys to GitHub Pages on
pushes to `main`. The repository's Pages source is currently "Deploy from a branch", so the
legacy branch build also runs; switching the source to "GitHub Actions" would leave a single
path, but that needs a repository administrator (**FLG-014**).

## Sources

Every source the site relies on is listed on `desk/methodology.html` with the specific point it
establishes:

- Amazon Associates Program Operating Agreement — https://affiliate-program.amazon.com/help/operating/agreement
- Amazon Associates Program Policies — https://affiliate-program.amazon.com/help/operating/policies
- Amazon Selling Partner Blog, Understanding ASINs — https://sell.amazon.com/blog/what-is-an-asin
- FTC Endorsement Guides — https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
- GitHub Pages documentation — https://docs.github.com/en/pages
- Google Search Console documentation — https://support.google.com/webmasters/answer/9128668
