# Crisp & Counter — an Amazon affiliate publication for countertop cooking

One site, one brand, one stylesheet. Question-led buying guides for air fryers and
countertop cooking appliances, a shortlist assembled from links that were actually
resolved by hand, and a public register of everything that could not be confirmed.

**Live:** https://karagemop466-tech.github.io/Affil1/  ·  **33 pages**
**Associates tracking ID supplied by the owner:** `shopnow047c-20` (enrolment and
attribution are **not** verified — see [Open questions](#open-questions-and-blockers))
**Prepared:** 2026-11-20 by session `arena/359baa16-affil1` (integration pass)

---

## What this repository is for

The brief had five parts. This is where each one lives:

| The ask | Where it is answered |
|---|---|
| Read like a shop, not an audit | The generated front page: seasonal feature, shortlist, topics, guides. The registers are one click from the footer, never the front door. |
| Make it findable | `sitemap.xml`, `feed.xml`, `robots.txt`, canonical tags, Open Graph images, `Article` + `FAQPage` + `BreadcrumbList` structured data, topic clusters with internal links |
| Make the machinery trustworthy | `tools/build.py` generates every page from `src/data/`; `tools/validate.py` is the gate; two GitHub Actions workflows run it (deploy + weekly audit) |
| Lead with products, disclose above the fold, mark every link | One `disclosure()` template, one `product_link()` template — a page cannot ship without either |
| Suggestions and questions before decisions | `/suggestions/` (29 scored proposals, 2 rejected on policy grounds), `/questions/` (22 questions, 5 answered by this pass), `/flagged/` (irregularities with sources), `/dashboard/` (entries, verification log, empty ledger) |

## Layout

```
index.html            publication front page          ← generated
guides/<slug>/index.html  9 buyer guides              ← generated
compare/ products/ topics/ about/                     ← generated
sources/ suggestions/ questions/ flagged/              ← generated
dashboard/            entries, verification, ledger    ← generated
404.html              not-found page                   ← generated
assets/css/site.css   the only stylesheet
assets/js/events.js   the five defined events, inert until an endpoint exists
assets/js/shortlist.js  "Save" on a product card; localStorage only, nothing sent
assets/img/*.jpg      commissioned illustrations (not product photography)
src/data/*.json       every fact the site publishes, with its source
tools/build.py        data → HTML (one template for nav, disclosure, footer)
tools/check.py        a gate: links, images, disclosure, sponsored marking,
                      price prohibition, sitemap/feed agreement
tools/validate.py     a second gate over the published tree; prints its own check count
tools/check_deploy_paths.py  resolves every reference over HTTP at the /Affil1/ mount
tools/verify_links.py re-resolve the register against Amazon and report drift
archive/              five earlier competing surfaces (four storefronts and a parallel
                      integration pass), preserved untouched and non-indexable
```

Nothing in the tree is hand-edited except `assets/`, `tools/`, `src/data/`, `docs/`
and the markdown files. If you edit a generated `.html` directly, the drift check in
CI fails and tells you so.

## Build, check, publish

```bash
python3 tools/build.py            # regenerate every page from src/data
python3 tools/validate.py         # the gate; exits non-zero on any violation
python3 -m http.server 8207 --bind 0.0.0.0   # preview; open /Affil1/ after linking the parent dir
```

Deploy is automatic: pushing to `main` runs
[`.github/workflows/pages.yml`](.github/workflows/pages.yml), which rebuilds, runs
the gate, fails if the committed HTML differs from the build, resolves every
reference at the Pages project mount, and uploads the artifact.

**That workflow is not currently what serves the site.** The repository's Pages
settings report `build_type: legacy` with `source.path: "/"`, so GitHub publishes the
repository root directly and the staged artifact is never used. This was confirmed on
2026-11-20 by fetching `https://karagemop466-tech.github.io/Affil1/tools/build.py` and
`.../archive/notes-edition/index.html` — both resolve publicly. The effect is that the
live host serves the build scripts, the data registers and five retired storefronts.
The fix is one setting (Settings → Pages → Source: GitHub Actions), and it is logged as
OFF-02 on [/offers/](https://karagemop466-tech.github.io/Affil1/offers/). The text
above describes the workflow; it does not describe the current deployment. A weekly
audit (`weekly-audit.yml`) re-runs the same gate against a live snapshot so a page
cannot quietly fall out of compliance.

## The rules this site publishes under

Each rule below is enforced by `tools/check.py` and `tools/validate.py`, not just asserted in prose:

1. **Disclosure above the fold on every page, and again in the footer.** The strip
   carries Amazon's required sentence verbatim — *"As an Amazon Associate I earn from
   qualifying purchases."* — followed by a plain-language version, because the FTC's
   test is whether a reader understands the relationship, not whether they found a
   legal page. Source: [Associates Program Operating Agreement §5](https://affiliate-program.amazon.com/help/operating/agreement)
   (retrieved 2026-11-20) and [FTC Endorsement Guides](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking).
2. **No price, star rating, review count or stock figure anywhere.** Amazon permits
   those only in a link it serves itself or through the Creators/PA API. This site has
   no feed, so it has no numbers — and a validator fails the build if a `$` + digit
   appears in a page. Source: [Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies).
3. **No price tracking or price alerts.** The Participation Requirements prohibit
   price-tracking or price-alerting functionality on an Associate site. Recorded as a
   rejected suggestion ([/suggestions/](docs note: SUG-25, SUG-26)) so the next session
   does not "improve" the site into a violation.
4. **Buy buttons only where a listing was actually reached**, with
   `rel="sponsored nofollow noopener"` and a visible "Paid link" note. A row whose
   destination never resolved has no button at all.
5. **Intended identifier and observed redirect are separate fields, never merged.**
   The five submitted codes are 9 characters; the destinations this project reached
   are 10-character ASINs. `intended_asin` stays null — see `src/data/products.json`.
6. **Every factual cell carries its source**, and an unconfirmed value is left blank
   and listed on `/flagged/`. Blanks are the honest state, not a gap to fill in.

## Verification of the five submitted links

Every link was fetched twice by two different sessions on 2026-11-20; the second pass
is recorded in `src/data/reverification.json`. Values below are what the destination
page returned; none of it is a product recommendation and none of it was tested here.

| Entry | Submitted | Destination reached | Note |
|---|---|---|---|
| P-01 | `link.amazon/B04G1MEwY` | `amazon.com/dp/B0CDY277D3` — CHEFMAN 6 Quart Dual Basket | unstable: interstitial on one attempt |
| P-02 | `link.amazon/B02NbDxp3` | `amazon.com/dp/B09B7SB46R` — Emeril Lagasse 26QT French Door | unstable: second attempt only |
| P-03 | `link.amazon/B00hJ57DV` | `amazon.com/dp/B08DKYBTPH` — Chefman Air Fryer 8 Qt | an earlier archived register wrongly logged this as the homepage |
| P-04 | `link.amazon/B0c8moW59` | **none** — Amazon continue-shopping interstitial | published as unresolved; no buy button |
| P-05 | `link.amazon/B0f3GKalj` | `amazon.com/dp/B0DZFD6R9Z` — CHEF iQ Sense thermometer | not an air fryer; gets its own guide |

Manual review entry points: [verification log](https://karagemop466-tech.github.io/Affil1/dashboard/#verification)
· [source register](https://karagemop466-tech.github.io/Affil1/sources/)
· [flagged register](https://karagemop466-tech.github.io/Affil1/flagged/)

## The one finding that decides whether this site can earn

None of the five submitted URLs carries a `tag` parameter, and each reaches Amazon through
an intermediate redirect. Under the Commission Income Statement, a purchase reached through
a "Redirecting Link" is disqualified, as is any purchase "not correctly tracked or reported
because the links … are not properly formatted" — so in that form they cannot be attributed
to `shopnow047c-20` at all.

The site is therefore **gated, not guessed**. Publishing a tracking tag asserts that this
site is listed on an enrolled Associates account for that ID, which nothing in this
repository can confirm. So:

- every buy button is a **reference link** to the official listing, with no tag, labelled
  as such, and the disclosure strip's plain-language sentence says plainly that no link
  earns anything today;
- the required Associates sentence stays verbatim on every page, above the fold and in the
  footer, because the obligation is not conditional on that state;
- `src/data/product-intent.json` holds the gate (`associate_enrollment_confirmed`,
  `site_registered`, `one_link_test_completed`, and `approved_special_link` per product);
- `tools/validate.py` fails the build if a tag is published while those flags are false, so
  the safe state is enforced rather than hoped for;
- `tools/arm_links.py` is the owner's switch: `--checklist` prints the steps, and it refuses
  to arm the site unless `--i-am-the-owner` is passed, so no future automated session can
  start claiming a relationship with Amazon on its own.

One of the five destinations (`P-04`) resolved only on a third attempt and arrived with
Amazon's `plpRedirect=mhFallback` marker, and `P-05` carries it too. That is Amazon's own
signal for a merchandised fallback, which is why the register publishes each destination as
a dated observation, keeps `intended_asin` null, and flags the pair as
[FLG-018](https://karagemop466-tech.github.io/Affil1/flagged/#FLG-018) rather than presenting the mapping as
confirmed. Read each one in a signed-in browser before arming anything.

## Open questions and blockers

Twenty-two are listed at [/questions/](https://karagemop466-tech.github.io/Affil1/questions/)
with the information each one needs. Five were answered by this pass. The ones that
block everything else, in order:

1. **Enrolment** — is `shopnow047c-20` an active tracking ID, and is this site listed
   in the account? No claim is made either way here.
2. **Special Links** — generate them in Associates Central, paste each into
   `approved_special_link` via `tools/arm_links.py --i-am-the-owner --link P-01 "<url>"`,
   and confirm one click in the report before arming the other four.
3. **Search Console** — verify the property. Until then, every statement about what
   readers want is reasoning, not evidence.
4. **An author** — a named human with two true biographical sentences. Bylines stay at
   desk level because inventing a person who tested these machines would be a
   fabricated endorsement.

## Editorial rule, in one line

A capability sentence is published only when it quotes the seller's own listing title,
attributed as such; nothing on this site claims a product was tested, and no figure
appears that cannot be traced to an official source.

## Licence and trademark note

Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates. This
site is not endorsed by or affiliated with Amazon beyond participation in the Associates
Program. All listing titles are quoted for identification and are the property of their
sellers. Illustrations were made for this publication and are captioned as such.
