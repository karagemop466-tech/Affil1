# First-party measurement (not enabled on GitHub Pages)

The editorial edition uses `kitchen/measure.js`. Its five events are `page_view`,
`outbound_product_click`, `guide_read_75`, `compare_view` and `flag_page_view`.
Payloads contain only the fixed page/event names and, for an approved link, a
product record ID. We intentionally omit referrer, viewport, URL, session ID,
click position and user agent. No local storage, cookies or fingerprinting.
The collector persists daily aggregate counts (90-day rolling window; purge on
write, plus schedule a purge during inactivity if deploying). Page views and
scroll depth are not unique visits, confirmed reads or Amazon sessions. Click
counts are best effort: not every browser/navigation permits delivery, and the
public endpoint is not resistant to all fabricated traffic. No order event.

## Runbook for a production host

1. Choose commercial-permitted hosting and a same-origin TLS reverse proxy. Do
   not put a collector URL or tracking integration on the GitHub Pages copy.
2. Review the deployed privacy notice, consent/opt-out requirements, request-limit
   configuration and infrastructure logging before collecting anything. The
   application does not store IPs; disable IP/user-agent/access logs in the
   proxy and WSGI server as well, and set body/time and global rate limits.
3. Keep the SQLite path on a private persistent volume (never publish the file).
   Set `MEASURE_ORIGIN` to the exact public origin, with no trailing slash, and
   `MEASURE_DB` to the private SQLite path. Serve the WSGI factory
   `measurement.collector:configured_app()` (for example with Gunicorn) behind
   the proxy, routing only `/api/e`. Backups must use the same retention policy.
4. Once those gates pass, configure only the dynamic host to set
   `data-measure="on"` on the document element. GPC and DNT skip sending and
   storage. Keep the static Pages HTML unchanged.
5. Use one validated Special Link per product before enabling paid CTAs. An
   approved anchor must carry `rel="sponsored"` and `data-special-product` with
   its approved record ID. Compare the aggregate click count with authorized
   reports at the marketplace/tag/date-window level; don't join a visitor to an
   order. Never use a personal test purchase to demonstrate attribution.

Run synthetic event tests: `PYTHONPATH=measurement python3 -m unittest discover -s measurement`.
The tests cover all five event types; they do not assert there are any real
visitors or orders. Inspect counts on the host with the SQLite CLI, not a public
read endpoint. Search Console property ownership and reader capture are separate
work items; neither is configured here.
