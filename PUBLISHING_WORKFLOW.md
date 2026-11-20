# Publishing workflow — the compliance gate

No page or guide publishes until every item below is true. Each line names where
it is enforced, so the gate is a script rather than a habit.

## 1. Disclosure (Operating Agreement §5, 16 CFR 255.0(f))
- [x] Required sentence present on every page, above `<main>` — enforced by `tools/check.py`
- [x] Repeated in the footer — same check
- [x] Full statement at `/about/#disclosure`
- [x] Placement rationale recorded with the regulation quoted on `/about/#sources`

## 2. Link integrity (Program Policies §2(a)(b), Google paid-link guidance)
- [x] Every Amazon retail link carries `rel="sponsored nofollow noopener"` and opens in a new tab — enforced
- [x] Every Amazon retail link carries `tag=shopnow047c-20` as a URL parameter — enforced in this pass
- [x] Policy citations are *not* marked sponsored — enforced
- [x] No `link.amazon` short link is offered as a click target — enforced
- [ ] One click confirmed in the Associates click report — **outstanding, needs account access (D-01)**

## 3. Claims
- [x] No price, star rating, review count or stock phrase in visible text — enforced
- [x] No test, ranking or "best" claim — enforced
- [x] Product attributes only as the seller's own wording, transcribed from the listing title
- [x] Every illustration labelled as an illustration at the point of use

## 4. One site for search engines
- [x] Canonical URLs on every generated page
- [x] `sitemap.xml` matches the built pages exactly — enforced
- [x] `feed.xml` items all resolve to real pages — enforced
- [x] Parallel-edition pages marked `noindex, follow` — enforced by `tools/legacy.py` and checked
- [ ] Search Console verified and sitemap submitted — **needs the owner's Google account (S-07)**

## 5. Measurement
- [ ] Analytics endpoint chosen and running — **decision D-13**
- [ ] Five defined events recorded at the endpoint — client exists and is inert
- [ ] No cookie, no third-party request — currently true and enforced

## 6. Publish
- [x] New guide added to the sitemap and the feed automatically
- [x] Build reproducible: CI rebuilds and diffs the tree
- [x] Every internal link and anchor resolves — enforced
- [ ] Record the reviewer, the date and the decision on the row being approved

**Rule:** an unchecked box is not a blocker for the site being live. It is a
blocker for claiming the thing the box describes.
