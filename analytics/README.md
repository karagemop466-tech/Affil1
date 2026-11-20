# Aggregate measurement

GitHub Pages does not enable the analytics client. To test the exact staged
edition, run `python3 tools/preview.py`. To exercise the opt-in collector on a
local machine, run `python3 tools/preview.py --measurement-demo` and visit
`http://127.0.0.1:4173/`. The second command binds only to loopback, discards
its aggregate database on graceful exit, and does not edit production pages.

The client sends five allowlisted events to same-origin `POST /api/e`; DNT and
GPC skip collection. The endpoint stores UTC-day totals, not raw events,
visitor IDs, referrers, or query strings. Citations aren't counted as approved
affiliate clicks. Before enabling on a permitted HTTPS host, review consent,
notice, retention and upstream logging. Configure `ANALYTICS_ORIGIN`,
`ANALYTICS_DATABASE` outside the web root, and a same-origin proxy to the
collector. Treat browser signals as page activity only, not sessions or orders.
The campaign ledger must use authorized, dated first-party reports.
