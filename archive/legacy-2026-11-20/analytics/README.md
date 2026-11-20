# First-party measurement: deployment gate

The maintained Crisp & Counter client is disabled on GitHub Pages. [GitHub
Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
is static and cannot host the collector. Do not enable tracking on the Pages
edition or proxy it to an unrelated origin.

On a future first-party HTTPS host, serve the staged publication and reverse
proxy `POST /api/e` to the loopback service. Set `ANALYTICS_ORIGIN` to the exact
HTTPS origin (no path or trailing slash), `ANALYTICS_DATABASE` to a writable
private SQLite file outside the checkout and web root, and optionally
`ANALYTICS_PORT` (default 8765). Run `python3 analytics/endpoint.py` from a
checkout of the same release. Only after reviewing notice, consent, retention,
backup deletion and proxy logging, arrange for `window.CC_ANALYTICS_ENABLED`
to be set to `true` before the deferred client runs. Disable request-body and
identifying access logs for the collection route. Configure proxy rate and
concurrency limits; origin validation is not authentication and public counts
are not fraud-proof.

| Counter | Trigger | Stored dimensions beyond UTC day and event |
|---|---|---|
| `page_view` | Maintained page loads | Allowlisted page |
| `outbound_product_click` | Sponsored Amazon listing link activation | Allowlisted page and observed ASIN |
| `guide_read_75` | Viewport reaches the 75% point in the guide's main section | Allowlisted guide page |
| `compare_view` | Comparison opens | Comparison page |
| `flag_page_view` | Flagged for Review opens | Review page |

The collector increments daily totals, not raw visitor records. Neither query
strings nor referrer URLs are submitted. The client omits credentials and
honors DNT and GPC; the collector also honors those headers. Counts represent
page loads, scroll depth and click signals, not unique sessions, completed
reading, conversions or orders. This implementation does not collect search
queries; use authorized Search Console data for editorial decisions and
[Associates reports](https://affiliate-program.amazon.com/home/reports) for
reported orders. Keep the campaign ledger empty until provenance is available.

Run `python3 -m unittest discover -s analytics` before deployment. Test the same
five events on staging, plus opt-out and a failed collector, before enabling
production. Set and enforce retention for the aggregate table before launch.

For the staged Pages edition, run `python3 tools/preview.py`. To exercise the
actual collector locally, run `python3 tools/preview.py --measurement-demo`,
then visit `http://127.0.0.1:4173/`. The second command enables all five counters
only in a temporary loopback preview; it removes the SQLite file on exit and
never changes production HTML. The normal preview and GitHub Pages do not send
beacons.
