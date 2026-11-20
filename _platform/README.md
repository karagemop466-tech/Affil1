# Countertop Almanac — Policy-Gated Affiliate Platform (`platform/` & `edition/`)

Session scope owned by `arena/44f81bcd-affil1` (Tracking ID: `shopnow047c-20`).

## Architecture

- `platform/data/*.json` — Line-by-line verified data records keeping `intent_confirmation` (`intended_asin`, `official_listing_url`, `confirmation_date`, `confirmation_source`, `validated_special_link_url`) strictly separate from `observed_redirect` (`observed_asin`, `observed_redirect_url`, `observed_tag_param`, `observed_date`).
- `platform/compliance_gate.py` — Enforces Amazon Associates Operating Agreement §5, Program Policies §2(a)–(b), §6(t), §6(y), 16 CFR Part 255, Google `rel="sponsored"`, and zero hallucinated values.
- `platform/build_edition.py` — Deterministic generator producing all 22 HTML pages, `sitemap.xml`, `feed.xml`, `robots.txt`, and SVG diagrams in `edition/`.
- `platform/verify_edition.py` — Line-by-line HTML, link, anchor, table-row official-source-link, disclosure, and `rel="sponsored"` verifier.
- `platform/collector.py` — Self-hosted zero-cookie HTTP collector for the 5 defined events (`page_view`, `product_card_click`, `guide_to_product_click`, `comparison_filter_use`, `suggestion_decision`).
- `platform/ledger.py` — Provenance-gated Campaign Ledger importer requiring SHA-256 hashes of signed-in Associates CSV exports and rejecting synthetic forecasts or conversion scores.
- `platform/research_engine.py` — Search Console query opportunity ranker and compliance-locked editorial brief builder.

## Commands

```bash
python3 platform/build_edition.py
python3 platform/verify_edition.py
python3 -m unittest discover -s platform -p 'test_*.py' -v
```
