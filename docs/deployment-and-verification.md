# Deployment and verification runbook

**Status:** repository implementation complete; live Pages deployment, Search Console ownership, and analytics hosting must be verified separately. This runbook is not evidence that those external services are active.

## 1. GitHub Pages

1. In repository Settings → Pages, select GitHub Actions as the publishing source (if not already selected).
2. Merge the site change to `main`; `.github/workflows/pages.yml` runs a local-link/disclosure/feed check, builds `_site/`, and deploys that artifact.
3. Confirm the Actions run succeeds and record the published environment URL. Do not treat the workflow file alone as proof of deployment.
4. Open the home page, four guides, product register, suggestion page, ledger, and flagged page from the deployed URL. Test mobile layout and all internal links.
5. If using a custom domain, update every canonical URL, sitemap URL, RSS link, robots sitemap line, and the analytics allowed origin together, then re-run validation.

Official source: [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## 2. Product identity and Special Links gate

For each submitted URL, do not overwrite the blank fields until confirmed:

1. Get the intended product/model from the owner or another authorized record.
2. Confirm the exact item/ASIN and official Amazon listing in the enrolled Associates workflow. Record the listing URL, confirmation date, and source in the intent fields.
3. Separately test the supplied link and record its actual destination as an observed redirect target. Do not infer this target from the URL string.
4. Verify the selected tracking ID `shopnow047c-20` is associated with the account and that the controlled test is attributed in an authorized report.
5. Keep the source and date for each observation. Stop on a mismatch; resolve the discrepancy before adding more product links.

The submitted short links' exact compliance status is unresolved; this runbook does not label them invalid. Review current [Amazon Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) and [Program Policies](https://affiliate-program.amazon.com/help/operating/policies). The current [Creators API onboarding](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/onboarding) requires Associates enrollment and API credentials. Amazon's [PA-API 5 deprecation notice](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation) identifies Creators API as its successor; do not implement a retired integration.

## 3. Search Console

1. Verify ownership of the deployed site in Google Search Console.
2. Submit `https://karagemop466-tech.github.io/Affil1/sitemap.xml` (replace with the confirmed deployed/canonical property if changed).
3. Check indexing and sitemap processing reports. After impressions begin, review the Search performance report by query and page. No search-demand or organic-traffic results are currently available from this repository.

Official sources: [Search Console getting started](https://developers.google.com/search/docs/monitor-debug/search-console-start) and [sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).

## 4. Optional analytics endpoint

GitHub Pages serves static files and cannot execute `analytics/server.mjs`. Deploy the endpoint separately to an operator-controlled Node.js 20+ host with a durable writable data path.

Example environment:

```sh
PORT=8787 \
HOST=0.0.0.0 \
ALLOWED_ORIGIN='https://karagemop466-tech.github.io' \
EVENTS_FILE='/var/lib/countertop-notes/events.ndjson' \
node analytics/server.mjs
```

`ALLOWED_ORIGIN` must be the exact browser origin of the published site (origin only; no path). Provide TLS through the hosting platform. Run `GET /health`, then use a test page to send one test event and confirm one sanitized line appears in the private data file. Configure `assets/analytics-config.js` by setting `window.SITE_ANALYTICS_ENDPOINT` to the endpoint's HTTPS `/events` URL; this small script is loaded before `assets/site.js` on every page. Keep the endpoint URL same-origin via a proxy if available, or set the exact CORS allowed origin.

The allowlisted events are:

| Event | Trigger | Stored dimensions |
|---|---|---|
| `page_view` | Non-guide page opens | Sanitized path, server receive time |
| `guide_open` | Guide opens | Sanitized path, server receive time |
| `outbound_product_click` | Supplied product link clicked | Sanitized path, internal submission code, server receive time |
| `comparison_tool_use` | Comparison checklist submitted | Sanitized path, server receive time |
| `suggestion_choice` | Editorial path selected | Sanitized path, internal path code, server receive time |

No names, account IDs, query text, cookies, user IDs, referrers, client timestamps, or product page details are accepted. The application does not write IP address or user agent to its event rows. A hosting provider may retain network logs; review its settings, terms, retention, and applicable privacy requirements before deployment. Protect the event file, set a retention plan, and apply host-level rate limiting/abuse controls (the endpoint does not persist or throttle by IP). The endpoint is deliberately not an order/conversion source: reported orders and commissions must come from authorized Associates reports and be entered separately in the ledger with date and provenance.

## 5. Editorial schedule and review

A proposed cadence is one well-sourced guide every two weeks for the first eight weeks, followed by a monthly editorial review using actual Search Console queries, reader usefulness, evidence readiness, and compliance review. This is a suggested schedule, not a traffic forecast. Add each actual published guide to both `sitemap.xml` and `feed.xml`, update `lastmod`, run `python3 tools/check_site.py --build`, and inspect the deployed page.

## 6. Pre-publication disclosure check

The Amazon Associate statement appears below the masthead and in each footer. Keep link-level disclosure adjacent to each affiliate link and review context against the current [Amazon requirements](https://affiliate-program.amazon.com/help/operating/agreement) and [FTC endorsement guidance](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking). Confirm program enrollment and site approval separately; displaying the statement is not proof of approval.
