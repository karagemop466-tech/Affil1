# Publishing workflow — compliance gate

No page or guide publishes until every check below passes. Record the check, date and reviewer in the pull request.

## 1. Disclosure placement (S01 · S07 · S24)
- [x] Affiliate disclosure strip present under the masthead, above the fold
- [x] Disclosure repeated in the footer
- [x] Full statement at /disclosure.html with Associates tracking ID shopnow047c-20

## 2. Link marking
- [ ] Every outbound product link carries `rel="nofollow sponsored"` and a visible “sponsored” label
- [ ] No unverified destination is linked outbound (flagged items link to /reviews/flagged.html instead)

## 3. Endorsement context
- [ ] No language implying Amazon endorsement
- [ ] Product findings labeled as findings, not endorsements; prices/ratings left blank when unconfirmed
- [ ] Reviewed against Amazon Associates Program Operating Agreement and FTC Endorsement Guides

## 4. Verification
- [ ] Every table row has a source link to the official source (Amazon.com)
- [ ] Unconfirmed values left blank and flagged; nothing inferred
- [ ] Intended ASIN and observed redirect target in separate fields

## 5. Measurement
- [ ] Outbound click counter active on sponsored links
- [ ] Five defined events instrumented (page_view, outbound_click, guide_read, suggestion_review, session_start)

## 6. Publish
- [ ] Guide added to sitemap.xml and rss.xml
- [ ] PR created from feature branch to main; review recorded in COORDINATION.md
- [ ] After merge: confirm GitHub Pages deploy; check for broken links

Reviewer / date / decision: ____________________
