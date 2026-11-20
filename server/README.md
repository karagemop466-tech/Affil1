# Analytics deployment gate

GitHub Pages cannot run this process ([GitHub Pages overview](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)). The maintained site's beacon is off. This collector replaces the previous raw-event protocol for that edition; do not expose the older parallel collectors alongside it.

1. Provision a single Node.js process behind HTTPS with `ANALYTICS_ORIGIN=https://karagemop466-tech.github.io` and `ANALYTICS_DIRECTORY` set to an absolute, private persistent directory outside the checkout or public root. `PORT` defaults to 8080 and `HOST` defaults to loopback for a local reverse proxy.
2. Rate-limit the route at the proxy and disable or minimize access logs there. The collector records only daily event totals, but hosting infrastructure can still see connection metadata. Origin checks are not authentication; bot traffic can inflate totals. Operate a single writer per directory and automate deletion under an approved retention policy.
3. Review the privacy notice and any consent obligations before setting `window.CC_ANALYTICS_ENDPOINT` to the HTTPS `/analytics/collect` URL ahead of the deferred client. Verify the five browser events and opt-outs in a staging environment first. Leave the setting absent if a gate is unresolved.
4. Reconcile reported orders only with authorized [Amazon Associates reports](https://affiliate-program.amazon.com/home/reports). Record the dated `report_import` event in the campaign ledger provenance trail only after a real import. The public endpoint rejects it. Outbound clicks are neither confirmed Amazon clicks nor conversions.

Run the collector contract test with `node --test server/collect.test.js`. No production account, tracking report, or visitor data is required by the test.
