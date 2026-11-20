# Archived edition — do not publish

This directory holds the superseded edition(s) of the Crisp & Counter site,
moved here on 2026-11-20 so that the repository serves **one** canonical site
rather than two competing ones.

- Nothing here is built by `tools/build.py`.
- Every HTML file here carries `<meta name="robots" content="noindex, follow">`.
- The canonical sitemap (`/sitemap.xml`) does not list any of these URLs.
- Relative asset paths in these files point at their original locations, so some
  may 404 on the live site. That is expected: these pages are a record, not a
  destination.

The two editions agreed on all five product identities. The surviving edition is
the generated one at the repository root, because it can be rebuilt and checked.

Removed from the served tree in the same pass: `crisp/`, `reviews/`,
`categories/`, `data/`, `js/`, `css/`, `server/`, `analytics/`, `docs/`, and the
duplicate root pages (`products.html`, `questions.html`, `suggestions.html`,
`guides.html`, `dashboard.html`, `disclosure.html`, `executive-summary.html`,
`flagged-for-review.html`, `privacy.html`, `categories.html`).
