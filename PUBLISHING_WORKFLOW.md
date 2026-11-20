# Publishing workflow — the compliance gate

No page or guide publishes until the build passes. The gate is not this document;
the gate is `tools/check.py`, which runs in GitHub Actions before deployment and
exits non-zero on any failure. This document says what the gate enforces and why.

## 1. Disclosure placement — S01 · S03

- [x] Associates sentence on every page: **"As an Amazon Associate I earn from qualifying purchases."**
- [x] Present in a strip under the masthead, **above `<main>`**, and repeated in the footer
- [x] Checker fails the build if the strip is missing, appears after `<main>`, or the sentence is absent
- [x] FTC guidance reason: a disclosure must be where it easily catches attention; footer-only is easy to miss

## 2. Link marking and tagging — S02 · S05

- [x] Every Amazon product link is a tagged Special Link: `/dp/ASIN?tag=shopnow047c-20`
      (Program Policies §2(b): the Associates ID must appear as a URL parameter)
- [x] Every one carries `rel="sponsored nofollow noopener"` and opens in a new tab
- [x] Checker fails on an Amazon retail URL without `sponsored`, `nofollow` or `noopener`
- [x] Policy pages (`affiliate-program.amazon.com`) are citations and must **not** be marked sponsored
- [x] `listing_url` (observed) and `affiliate_url` (tagged) are separate fields

## 3. Endorsement context — S03 · S07

- [x] No language implying Amazon endorses, sponsors or supports this site
- [x] Product facts label the seller as the source ("the seller states…")
- [x] No price, star rating, review count or stock phrase anywhere in visible text
- [x] No test, ranking, winner or best-seller claim anywhere
- [x] Checker fails on each of the above by pattern

## 4. Verification — every table row

- [x] Every product row links the Amazon listing it came from
- [x] Every policy quote links the official document and records the retrieval date
- [x] Unconfirmed values are blank and listed on `review/index.html`
- [x] `intended_asin` and `observed_asin` are never merged; the checker fails if they are

## 5. Measurement — before optimising anything

- [x] Five events defined: `page_view`, `guide_open`, `outbound_click`, `search_query_referral`, `report_import`
- [x] Outbound-click counter listens for clicks on sponsored links and records the product reference only
- [ ] A first-party endpoint deployed — **not done**: GitHub Pages cannot run a collector (FLG-017)
- [x] Privacy position published: no cookie, no storage, no identifier, no third party
- [x] Campaign ledger empty with a defined schema and a provenance rule

## 6. Publish

- [x] Guide added to `sitemap.xml` and `feed.xml` by the build, not by hand
- [ ] Confirm the deployed site has no broken links — checked after merge against the live URL
- [x] Superseded edition marked `noindex` and excluded from the sitemap (FLG-018)

## Reviewer record

Reviewer / date / decision: this build, 2026-11-20, automated gate green
(`24 pages, 0 errors, 0 warnings`). Open items are published at `review/index.html`
and do not block the release.
