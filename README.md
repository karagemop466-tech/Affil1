# The Crisp Counter

A publication-style shop for four kitchen appliances, built as a static site and
deployed to GitHub Pages — with the verification layer published next to the
shop rather than filed away from it.

**Live site:** https://karagemop466-tech.github.io/Affil1/
**Associates ID:** `shopnow047c-20`

> As an Amazon Associate I earn from qualifying purchases.

---

## What this repository contains

| Path | What it is |
|---|---|
| `index.html` | Front page: masthead, disclosure strip, seasonal feature, product shelf, guides |
| `shop/` | Shop index, four product pages, and one held-link page |
| `guides/` | Guide index and four question-shaped buying guides |
| `about/` | Disclosure, sourcing policy, and what the site deliberately does not publish |
| `summary/` | Executive summary |
| `records/` | The verification layer: source register, product intent, compliance, measurement, campaign ledger, open questions, suggestions, flagged for review |
| `data/` | The source of truth. Every table on the site renders from these files |
| `content/` | Product and guide copy, as data |
| `lib/` | Site config and rendering primitives |
| `scripts/build.mjs` | Generates every HTML page, plus sitemap, feed and robots |
| `scripts/check.mjs` | The build gate. Fails the build on a compliance or link violation |
| `scripts/test-gate.mjs` | Injects deliberate violations and asserts the gate catches them |
| `COORDINATION.md` | The shared task board, including the integration log for three parallel sessions |
| `analytics/endpoint.py` | Self-hosted collector contributed by a parallel session; the candidate host for the click counter |
| `archive/` | Superseded pages from parallel sessions, preserved rather than deleted. Excluded from the gate |
| `docs/` | Parallel-session documents kept for review (legacy privacy notice, their executive summary) |

Everything under `shop/`, `guides/`, `records/`, `about/`, `summary/`,
`index.html`, `404.html`, `sitemap.xml`, `feed.xml` and `robots.txt` is
**generated**. Edit `content/`, `data/`, `lib/` or `scripts/build.mjs`, never the
generated output.

## Commands

```bash
npm run build    # regenerate the whole site
npm run check    # run the compliance and link gate
npm test         # prove the gate catches deliberate violations
npm run verify   # all three, in order (this is what CI runs)
npm run serve    # local preview on http://localhost:4321
```

No dependencies. Node 20+, standard library only.

## The five verification commitments

1. **Every table row has a source link.** `records/source-register/` carries a
   link to the official page behind each claim.
2. **Unconfirmed values are blank, not guessed.** A row that could not be
   verified has an empty value cell and an `unverified` badge.
3. **Intent and observation are separate fields.** `data/product-intent.json`
   keeps `intended_asin` apart from `observed_redirect_target` and never merges
   them.
4. **The ledger is empty on purpose.** `data/campaign-ledger.json` has defined
   columns and zero rows. No conversion score, no revenue forecast.
5. **Every open question is published.** `records/questions/` lists the fourteen
   gaps, what each one blocks, and how to close it.

## What the site deliberately does not publish

- **Prices.** Amazon permits showing a price only when Amazon serves it or when
  it comes from an approved API, and a copied price is wrong within the hour.
- **Star ratings and review quotes.** Restricted to data obtained through
  Amazon's APIs.
- **Hands-on testing claims.** No product here has been tested by this desk, and
  the FTC is explicit that you cannot describe experience you have not had.
- **Rankings and "best of" lists.** A ranking implies a comparison that was
  actually performed.

Each of these is enforced by the gate, not just by good intentions.

## The five submitted links, as verified on 2026-11-20

| Submitted | Observed destination | Status |
|---|---|---|
| `link.amazon/B04G1MEwY` | `amazon.com/dp/B0CDY277D3` — Chefman 6 Qt dual basket | observed only |
| `link.amazon/B02NbDxp3` | `amazon.com/dp/B09B7SB46R` — Emeril Lagasse 26QT French door | observed only |
| `link.amazon/B00hJ57DV` | `amazon.com/dp/B08DKYBTPH` — Chefman TurboFry 8 Qt | observed only |
| `link.amazon/B0c8moW59` | none reached | **unresolved — held** |
| `link.amazon/B0f3GKalj` | `amazon.com/dp/B0DZFD6R9Z` — CHEF iQ Sense thermometer | observed only |

No intended ASIN has been confirmed for any link. The observations above record
what each link *did*, which is not the same as what it was *meant* to do.

## Repository history note

Three agent sessions worked this repository in parallel on 2026-11-20. Their
work was merged into `main` while this session was building, which produced two
competing surfaces for the same site. The integration kept this session's
generated shop as the canonical site and moved the other surface into
`archive/legacy-surface/`, because publishing both would create exactly the
duplicate-site problem the brief asks to avoid — and the gate found 129 rule
violations across the superseded pages. Nothing was deleted. The full account,
including which of their artifacts were kept live, is in `COORDINATION.md`.
Where the two surfaces disagree on facts, this session's dated observation is
newer: it resolved **4 of 5** submitted links; the earlier table recorded 2 of 5.

## Open items

See `records/flagged/` for the eight flagged items, and `records/questions/` for
what each one blocks. The two that need a person rather than an engineering
session are the unconfirmed intended ASINs and the unresolved question of
whether the submitted short-link format is a compliant Special Link.

## Deployment

GitHub Pages publishes this repository from the **main branch root** (legacy
build type), so the generated HTML is committed. Because of that,
`.github/workflows/deploy-pages.yml` is a **gate rather than a deployer**: on
every push and pull request it

1. rebuilds the site from `data/` and `content/`,
2. fails if the committed output differs from that clean build, so generated
   pages cannot drift from their source of truth,
3. runs the compliance gate, and
4. runs the gate's own negative test.

A red run means the published site should not be trusted. To move to a
workflow-driven deploy instead, change Settings → Pages → Build and deployment →
Source to *GitHub Actions* and restore the `upload-pages-artifact` /
`deploy-pages` steps.

## Licence

Content and code in this repository are unpublished work product. No licence is
granted. Amazon product names and trademarks belong to their respective owners.

---

## Integration state (2026-11-20, final integration session)

This repository has seen several parallel sessions. Their work is **preserved, not
replaced**:

| Path | What it is |
|---|---|
| *(root — the paths above)* | The canonical site: one publication, one sitemap, one feed. |
| `crisp/` | S-96012762's "Crisp & Counter" section, kept at its original path with its own build and feed. `robots.txt` disallows it so one site is indexed; it is excluded from the published-page gate with a printed note. |
| `src/`, `tools/`, `docs/MEASUREMENT.md`, `docs/EXECUTIVE-SUMMARY.md` | S-96012762's registers, builder and documents, kept at their original paths. |
| `archive/legacy-surface/` | The earlier root surface (dashboard, legacy guides, legacy registers), relocated with rename history intact. |
| `archive/session-*/` | Earlier sessions' own snapshots, where they left them. |
| `docs/*-parallel-session.md`, `docs/COORDINATION-PR15-integration.md` | Session documents kept for review. |
| `analytics/endpoint.py`, `data/confirmations.json`, `data/products.json`, `data/ledger.json` | Preserved records; supersession notes point at the canonical registers (`data/product-intent.json`, `data/campaign-ledger.json`). |

Workflow: `.github/workflows/deploy-pages.yml` rebuilds the site from source,
fails if committed output has drifted, runs the compliance gate, and runs the
gate's negative self-test. GitHub Pages publishes from the `main` branch root
(legacy build type); a red gate run means the site should not be published further.

Verification: `data/sources.json` carries the row-level spot-check notes of the
2026-11-20 integration pass (16 clauses re-read verbatim from the official pages;
3 rows left blank and flagged unverified). Every product row in
`data/product-intent.json` keeps intended and observed identifiers in separate
fields and never merges them.
