# Set aside by the integration pass (session `arena/359baa16-affil1`, 2026-11-20)

Nothing here was edited, and nothing was deleted. These are the competing surfaces and
generators that parallel sessions merged into `main` while the root publication was being
integrated:

| Path | What it was |
|---|---|
| `kitchen/` | an editorial-only Pages edition (`noindex`, deliberately emits no Special Link), with its own build/check/media files |
| `kitchen-build/` | its launch-readiness checker and unit tests |
| `tools/layout.py`, `tools/stage.py`, `tools/check.py`, `tools/page_*.py` | a second generator writing the same root paths as `tools/build.py` |
| `crisp/`, `brief/`, `review/`, `operations/`, `products/p-0*.html`, `dashboard.html`, `guides/*.html` (flat) | pages those generators published, and the earlier `/crisp/` publication |
| `data/`, `notes/`, `verification-audit*` | two verification registers whose findings disagree with the published one |

Why they are here rather than published: this repository had **six** front pages, three
build systems writing the same files, and three data schemas describing the same five
links. One URL cannot serve two `index.html` files, and a "verified" register cannot be
trusted when two generators disagree about what was checked. One pipeline publishes:
`src/data/` → `tools/build.py` → `tools/validate.py`.

What was **kept** from these passes rather than set aside: the self-hosted Fraunces/Inter
typefaces, the responsive editorial art and its imagery rule (`src/data/images.json`),
`favicon.svg`, the sharper front-page title/description, the P-04 destination
discrepancy (published as `FLG-016` and in `src/data/reverification.json`), and
`assets/js/analytics.js` + `analytics/endpoint.py` for the first-party collector.

Their content is not lost to review: the `kitchen/` edition's seasonal guides and its
"brief for the next design pass" are readable here, and the equivalent buyer questions are
published at `/guides/air-fryer-thanksgiving-overflow/`, `/guides/frozen-food-nights/` and
`/guides/smart-probe-thermometer/`.

To restore any part of it, move the directory back and re-point `tools/build.py` at the
data it needs — or prefer the smaller change: port the page onto the single generator so
one gate still covers it. `.github/workflows/kitchen-check.yml` was rewritten for that
reason; it now runs the published gate instead of a checker whose inputs no longer exist.
