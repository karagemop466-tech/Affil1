# Crisp & Counter

[The Countertop Edit](https://karagemop466-tech.github.io/Affil1/) · [Executive summary](EXECUTIVE_SUMMARY.md) · [Coordination](COORDINATION.md)

A kitchen buying publication with a filterable and bookmarkable product shortlist. `src/data/products.json` separates the submitted URL, observed destination, intended product and account confirmation. Blank means unknown, not zero. The editorial desk links every decision surface without making a shopper start at the audit.

## Build and test

```sh
python3 tools/build.py
python3 tools/check.py
python3 tools/check_local_links.py
python3 tools/stage.py dist  # destination must be empty
python3 server/publication.py
```

The Python server serves **only** `dist` on port 8000. It enables five same-origin events, honors DNT/GPC, and writes daily aggregate counts to SQLite outside the web root. `PORT` and `COUNTER_DB` are configurable. Use a durable non-public database for an authorized production host. No raw event ingestion, cookies, visitor IDs, referral strings or IP logging by the collector. Do not import preview tests into the campaign ledger.

GitHub Pages serves static HTML. Its client sends no analytics requests. Native branch publishing uses `_config.yml` exclusions to avoid publishing historical editions or source data. Workflow-based Pages uses `tools/stage.py`. Keep both scopes aligned. No other domains or editions are submitted in the sitemap.

## Editorial cadence

Monday: review authorized, sanitized query aggregates. `editorial.yml` gates AI drafting on approved public-use Search Console data in `src/data/editorial-signals.json` (query, impressions, source, retrieved_on, provenance, approved_for_public_use). With no reports the job selects no topic. With data, it attaches an unpublished draft using GitHub Models; it cannot write to the repository. Every proposal requires an editorial decision and policy review. Do not upload raw reports or customer data. Review product destinations monthly and on redirect changes. Publish at most one approved guide per week through `tools/content.py`; the build updates the guide desk, sitemap and RSS together. A schedule is not a promise to publish without evidence.

Review [Amazon's agreement](https://affiliate-program.amazon.com/help/operating/agreement), [Program Policies](https://affiliate-program.amazon.com/help/operating/policies), the [FTC's endorsement guidance](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) and [Google's paid-link guidance](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) before release. No hand-built tagged URL is treated as an account-validated Special Link.
