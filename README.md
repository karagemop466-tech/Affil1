# Good Measure Kitchen

A static, reader-first affiliate editorial site focused on practical kitchen buying guides. Product facts and submitted link destinations remain explicitly unverified until checked through authorized official sources.

## Preview locally

Run `python3 -m http.server 8080 --bind 0.0.0.0` and open the preview. The site is plain HTML/CSS/JS and has no build dependencies.

## Deployment

`.github/workflows/pages.yml` deploys to GitHub Pages on pushes to `main` and on manual workflow dispatch. Enable GitHub Pages with **GitHub Actions** as the source in repository settings. Update `sitemap.xml` and `feed.xml` if the canonical Pages URL differs from `https://karagemop466-tech.github.io/Affil1/`. Search Console and analytics require account/property setup and are not falsely represented as connected.

## Editorial and compliance limits

- Top-of-page and footer Associates disclosure on each page.
- Submitted outbound product links use `rel="sponsored nofollow noopener"`.
- No product features, price, reviews, rank, popularity, commission, conversion, or revenue claims are populated without evidence.
- See [Flagged for review](guides/flagged-for-review.html) for missing data, official source references, and next steps.
