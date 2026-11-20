# Executive summary

**Project:** an Amazon Associates publication for countertop cooking appliances.
**Tracking ID supplied:** `shopnow047c-20`
**Built:** 2026-11-20
**Live:** https://karagemop466-tech.github.io/Affil1/

---

## What exists now

A buyer-facing publication with a front page, four question-shaped buying
guides, a form-faithful comparison table, a products register, and four
reviewer-facing registers (sources, suggestions, open questions, flagged for
review). Five products are documented; all five submitted links now resolve to
official Amazon listings (the fifth, link.amazon/B0c8moW59, resolved on
re-verification 2026-11-20 — it previously only returned Amazon's checkpoint
page).

Every page carries the affiliate disclosure directly under the masthead and again
in the footer. The build fails if either is missing.

Reconciliation this pass (2026-11-20): `tools/validate.py` was reconciled to the
canonical products.json schema and passes; the analytics client now records the
five canonical events from `src/data/events.json`; root-build outbound product
links now carry the Associates tag (`?tag=shopnow047c-20`).

## The four decisions that shaped it

**1. No prices, ratings, review counts or stock — anywhere.**
Not an oversight. Amazon permits price and availability display only where Amazon
serves the link carrying the data, or where the figure arrives through the
Creators API or PA API. Neither condition holds, so no figure is published. Same
section of the Operating Agreement prohibits inaccurate or overbroad product
claims, which is why nothing here is described in terms the seller did not use.

**2. No product is ranked, and no winner is declared.**
Nothing was tested. A verdict without a test is a guess. The comparison page
compares shape, cooking zones, stated claims and suitability — all decidable
before purchase — and explicitly refuses the "which cooks better" question.

**3. Intended ASIN and observed redirect target are separate fields, never merged.**
The supplied codes are nine characters. An ASIN is ten. Four of the five links
resolved to listings whose ASINs are ten characters; the supplied slugs are not
those ASINs. Merging the two would have produced a product record that looked
complete and was wrong.

**4. The verification work is published, not hidden.**
The audit trail moved to `/sources/`, `/suggestions/`, `/questions/` and
`/flagged/`, all reachable from the footer. A buyer sees products and guides; a
reviewer sees every gap with a source link.

## The five findings that matter

| # | Finding | Consequence |
| --- | --- | --- |
| 1 | All five supplied codes are 9 characters, so none is an ASIN | The product identifier had to be read from the resolved page, not from the link |
| 2 | No supplied link was observed to carry `shopnow047c-20` | Attribution is unconfirmed until a signed-in click is measured |
| 3 | One link (`B0c8moW59`) never resolved to a product | Four products documented, not five; the gap is published, not invented |
| 4 | Commission rates sit behind a sign-in | No rate is published, so no revenue estimate exists |
| 5 | The repository contained no prior site | Nothing was deleted; the earlier audit surfaces are preserved at `/legacy/` |

## What is blocked, and on whom

| Blocked item | Blocked on | Unblocks |
| --- | --- | --- |
| Confirm the tracking ID on a live click | Owner, Associates dashboard | Everything financial |
| Identify the fifth product | Owner, a browser session | The fifth product row |
| Read the rate card | Owner, signed-in session | Any revenue statement |
| Live prices and images | Owner, Creators API or PA API access | Prices, photography, full comparison |
| Search Console | Owner, domain access | Query data for the next topic |
| Author identity | Owner, a name and a bio | Byline, author page, credibility |
| Analytics collector | A decision on hosting | The five defined events |

Full detail, with what was checked and what would resolve each item, is on the
[Flagged for review](https://karagemop466-tech.github.io/Affil1/flagged/) page.

## What was verified, and how

Fifteen policy and legal propositions were read directly from primary sources and
quoted verbatim in `src/data/compliance.json` — Amazon's Operating Agreement
(updated 2025-10-15), the Associates Program Policies (updated 2026-04-14), the
FTC's Endorsement Guides FAQ, 16 CFR Part 255, and Amazon's Selling Partner API
reference for the ASIN definition. Each quotation carries the URL it came from
and a statement of what it is being used to support, so a reviewer can check the
inference rather than just the text.

Product observations were made by requesting each supplied link, following the
redirect, and reading the destination page. The observed ASIN, brand, category
path and listing title for each product are recorded in `src/data/products.json`
with the URL that was actually read.

647 automated checks run before publish: one H1 per page, disclosure above the
fold on every page, canonical on every page, no broken internal links, every buy
link marked `sponsored`, no image without alt text, sitemap and feed agreement,
and a guard against reintroducing a price figure. All pass.

## What was deliberately not done

- **The AI content pipeline in the brief.** Automating article generation before a
  single link is confirmed would industrialise the exact failure the brief asks to
  avoid. One link, one measurement, then automation.
- **Paid search.** Purchases arriving through paid search are disqualified under
  the Commission Income Statement, and bidding on Amazon marks is separately
  prohibited. It would spend money to generate non-commissionable orders.
- **Email capture.** Needs a provider, consent records and an unsubscribe path.
  A signup box that silently does nothing is worse than no signup box.
- **Stock photography.** A stock image of a different appliance would
  misrepresent the product, and Amazon-served imagery may not be altered.

## The three things to do next, in order

1. **Click one link while signed in to Associates.** Confirm the click appears
   under `shopnow047c-20`. This single measurement decides whether the site can
   earn at all.
2. **Read the fifth product off a browser session** and send back its name and
   ASIN. The site is built so that completing the row is a data edit.
3. **Decide on API access.** It is the only route to prices and photographs, which
   are the two largest gaps between this site and a conventional retail page.

## Bottom line

The site is live, internally consistent, and honest about its limits. It cannot
currently prove it earns anything, and it does not pretend otherwise. The fastest
path to a site that does earn is one confirmed click, not more content.
