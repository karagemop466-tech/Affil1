# Affiliate launch, measurement and AI drafting

The maintained edition is the GitHub Pages root. The launch register under
`operations/launch-readiness.html` is generated with it and intentionally noindexed. It holds the dated
five-link observation separately from Associates confirmation. It does not supersede
historical observations or validate the short-link service. Legacy editions may still
display previously published links or language; do not use them as attribution evidence.

## Publish gate

1. Collect the exact intent and official US listing for each proposed CTA in the enrolled
   Amazon Associates workflow. Generate the Special Link there, validate the intended
   variant and attribution in an authorized report without making a qualifying self-purchase,
   and keep the actual report off Git. Do not append a tag to an observation as a shortcut.
2. Record the dated evidence in `intent.json`. Only a complete bundle for a matching
   long-form destination, validated with `python3 kitchen-build/readiness.py --require-approved P-01`,
   can produce a root product-page CTA. This command is a mechanical check, **not proof** that
   a report actually exists. An authorized reviewer must attest to provenance, policy and disclosures.
3. Build with `python3 tools/build.py`; run `python3 tools/check.py` and `python3 -m unittest discover -s kitchen-build -v`.
   Paid links are marked sponsored, receive a proximate disclosure and carry a product reference for the counter.
   Editorial citations remain untagged and are never counted as paid clicks.
4. Inspect the current [Amazon Program Policies](https://affiliate-program.amazon.com/help/operating/policies)
   before adding any API-backed fields. This release does not collect or publish price, stock,
   ratings, review counts, commission estimates, search volume, performance rankings or forecasts.

## Measurement deployment

GitHub Pages cannot host the runtime. To preview without analytics, run
`python3 kitchen-build/measurement.py serve --port 8080`. For local measurement testing,
add `--origin http://127.0.0.1:8080 --database /tmp/cc-development.sqlite` and open the
site from that exact origin. The preview and that database are not production.

For production, after approval, run the optional receiver behind your existing reviewed HTTPS
proxy, setting `--origin https://your-reviewed-host` and `--database /private/path/cc.sqlite`.
Serving the edition and collector on the same origin is required. Do not publish a second indexable
copy alongside the canonical Pages site: arrange a single canonical production host first. The
stdlib HTTP process is a reference runtime; set request/rate limits at the proxy, keep logs
privacy-reviewed, add restricted filesystem permissions and backups, and schedule the `prune`
subcommand. Select retention explicitly (default 30 days when enabled). The application does not
store IPs, query parameters, cookies, user agents, referrers, or session IDs. Proxies and GitHub
have their own logging and must be considered separately. The browser honors GPC and DNT and has
no checkout event. Page views are not unique visitors or eligible sessions. Anonymous counts are
operational signals, subject to blocking and abuse, not attribution evidence.

The five browser events are `page_view`, `outbound_product_click`, `guide_read_75`,
`compare_view` and `flag_page_view`. A separate private report-import audit count is recorded only
after a successful import. Search queries come from Search Console, not the collector.
The importer accepts an **operator-normalized aggregate** CSV, not arbitrary Amazon reports:

```text
source_reference,window_start,window_end,channel,eligible_sessions,clicks,reported_orders
```

Leave missing values blank, not zero. Use only measurements actually present in an authorized
report and a non-sensitive report reference. Never put impression or page-view totals into
eligible sessions. The CLI `import-report --database /private/path/cc.sqlite --authorized report.csv`
requires explicit provenance attestation, rejects duplicate rows transactionally, and does not
publish any data. The public campaign ledger remains empty until authorized evidence is reviewed
for release. Run `counts --database /private/path/cc.sqlite` for aggregate event counts. `prune`
with the approved `--retention-days` removes old event aggregates; apply a separate retention
rule to campaign report rows and backups.

## Editorial loop and draft prompt

Verify the canonical Pages URL-prefix property and submit its sitemap in Search Console. Weekly,
review the query/page pairs and note date range and any report limitations; if a buyer question is
repeated, consider one article or revision per two-week cycle. Compare the same windows before
changing copy, and record the decision, not a causal or revenue claim. RSS is the existing reader
subscription path; email, Search Console verification, and an ongoing automated model/research job
are not connected by this release.

Draft prompt: “Write for one real kitchen decision. Open with what a reader can do before buying.
Use the supplied official source packet, cite each product claim, say which facts come from a seller,
and keep observations separate from approved claims. If a field or measurement is unknown, leave it
blank and say what evidence would close it. Use one question-shaped headline, one realistic worked
example, and one relevant guide as the next action. Do not invent a test, byline, review statistic,
ranking, demand signal, trend, product image, or Special Link. Output a draft and a separate evidence
checklist. Do not publish.”
