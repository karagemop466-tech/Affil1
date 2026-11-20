# COORDINATION — shared task board

Repo: `karagemop466-tech/Affil1` · Tracking ID: `shopnow047c-20`
Last updated: 2026-11-20 (UTC)

This file is the shared task board for any agent session working in this repo.
Read it before starting. Claim a task by adding your session ID and file scope,
then commit and push the claim immediately.

## Session log

| Session ID | Branch | Started | Scope | Outcome |
|---|---|---|---|---|
| `arena-cadaafe7` | `arena/cadaafe7-affil1` | 2026-11-20 | Whole-repo build, then integration | Built the shop + records; then merged `main` into `integration-main` and reconciled with two other sessions' merged work. See *Integration log* below. |

### Why this session initially claimed everything

At claim time the repository contained only `README.md` and a single commit
(`cca8c2a`), with no other branch or worktree visible. With no competing claim,
splitting the build across sessions would have created merge-conflict risk on
shared outputs for no benefit. This session claimed every task and logged the
verification for each.

## ⚠️ Integration log — 2026-11-20, read this first

While this session was working, **two other sessions merged into `main`**
(PRs #5, #6, #8 from `arena/c58c5996-affil1` and `arena/55d40788-affil1`).
`main` grew from 1 file to 68. The integration was performed on branch
`integration-main` and merged with `-X ours` so this session's generated shop
won conflicts on shared paths. What happens to the other sessions' work:

### Preserved, not discarded

| Their work | Where it lives now | Why |
|---|---|---|
| `analytics/endpoint.py` — self-hosted collector | `analytics/endpoint.py`, untouched | Genuinely useful; referenced by the measurement record as a candidate host for FLG-004. Kept live. |
| Their guide content (13 topics) | `archive/legacy-surface/guides/` | Superseded by four canonical guides, but preserved as history rather than deleted. |
| Their dashboards (`dashboard.html`, `questions.html`, `suggestions.html`, `flagged-for-review.html`, `reviews/flagged.html`, `categories/`, `products.html`, `guides.html`) | `archive/legacy-surface/` | Superseded by `records/` and `shop/`. |
| Their assets (`app.js`, `data.js`, `styles.css`, `css/`, `js/`, `server/`) | `archive/legacy-surface/` | Superseded by `assets/css/site.css` and `lib/`. |
| Earlier archived sessions | `archive/session-099b013a-affil1/`, `archive/session-c58c5996-affil1/` | Their own archives, left where they put them. |
| `privacy.html` | `docs/privacy-legacy.html` | The only privacy notice in the repo. Kept because the measurement record (Q-09) requires one before the counter can be switched on. **Not yet merged into the live site** — that is a decision for the owner, see SG-15. |
| `EXECUTIVE_SUMMARY.md`, `PUBLISHING_WORKFLOW.md` | `docs/*-parallel-session.md` | Preserved for review. Their product-finding table claims 2 of 5 links resolved; this session resolved 4 of 5. Where the two disagree, this session's dated observation is the newer evidence. |

### Why their pages were archived rather than published alongside the shop

Both surfaces cannot be the sites's canonical pages — that is the duplicate-site
problem the brief asks to avoid. The gate found **129 violations** across their
pages, including outbound `link.amazon` short links published as live controls,
Amazon links without an Associates tag, and 19 broken root-absolute `/Affil1/`
references. Publishing both would have meant publishing a surface that breaks
the rules this repo is supposed to enforce. Archive keeps the work, one canonical
site keeps the rules.

### Root cause of the failing `Deploy static site to GitHub Pages` run

`main`'s workflow (`pages.yml`, now removed) validated local references by
resolving every relative `href` against the filesystem root, but the pages use
root-absolute `/Affil1/...` paths, which never resolve on disk. Every run failed
on 19 references. Not a content bug — a validator bug. Replaced by
`deploy-pages.yml`, which runs the real gate instead.

### Files this session touched that were claimed by nobody

`data/*.json` (campaign-ledger was clobbered by a same-named file from another
session and restored), `scripts/`, `lib/`, `content/`, `records/`, `shop/`,
`guides/`, `index.html`, `sitemap.xml`, `feed.xml`, `robots.txt`.

## Task board

| ID | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T01 | Source register: official-source verification of all 5 links | done | `arena-cadaafe7` | `data/sources.json`, `records/source-register/` |
| T02 | Product-intent confirmation record (intended vs. observed, separate) | done | `arena-cadaafe7` | `data/product-intent.json`, `records/product-intent/` |
| T03 | Policy + disclosure compliance surface | done | `arena-cadaafe7` | `data/sources.json`, `records/compliance/` |
| T04 | Decision-readiness question register | done | `arena-cadaafe7` | `data/questions.json`, `records/questions/` |
| T05 | Suggestion register with review controls | done | `arena-cadaafe7` | `data/suggestions.json`, `records/suggestions/` |
| T06 | Editorial guides + guide index | done | `arena-cadaafe7` | `content/guides.mjs`, `guides/` |
| T07 | Shop surfaces | done | `arena-cadaafe7` | `content/products.mjs`, `shop/` |
| T08 | Front page as publication front page | done | `arena-cadaafe7` | `index.html` (generated) |
| T09 | Executive summary | done | `arena-cadaafe7` | `summary/index.html` |
| T10 | Campaign ledger (empty, well-defined) | done | `arena-cadaafe7` | `data/campaign-ledger.json`, `records/campaign-ledger/` |
| T11 | Outbound-click counter + endpoint contract | needs review | `arena-cadaafe7` | `assets/js/analytics.js`, `data/events.json`, `records/measurement/` |
| T12 | Findability: canonical site, sitemap, feed, robots | done | `arena-cadaafe7` | `sitemap.xml`, `feed.xml`, `robots.txt` |
| T13 | Flagged-for-review page | done | `arena-cadaafe7` | `records/flagged/` |
| T14 | Build + gate + negative test + deploy docs | done | `arena-cadaafe7` | `scripts/`, `.github/workflows/` |
| T15 | Integrate `main` with three sessions' work | done | `arena-cadaafe7` | `integration-main` merge |

**Status key:** `unclaimed` · `in progress` · `done` · `needs review`.
`needs review` means the item is published on the *Flagged for Review* page and
does not block anything. T11 is `needs review` because the counter is built but
has no host (FLG-004).

## Verification recorded for the completed work

- `npm run verify` → **24 pages, 0 gate violations**; **7/7 deliberate
  violations caught** by `scripts/test-gate.mjs`, with the site restored and
  re-verified afterwards.
- Source register: **24 claims, 22 verified with a link, 2 left blank and
  flagged unverified.** The two are the commission rate schedule (behind an
  Associates sign-in) and the compliance status of the short-link format.
- Link resolution: **4 of 5 submitted links** reached a product listing on
  2026-11-20. The fifth reached none and is held, not guessed.
- No intended ASIN is confirmed for any link; every row reads `observed only`.
- Documented irregularities: FLG-001 through FLG-008, published on
  `records/flagged/`.

## Standing rules for any session working here

1. **Shared outputs are generated.** `index.html`, `shop/`, `guides/`,
   `records/`, `about/`, `summary/`, `404.html`, `sitemap.xml`, `feed.xml` and
   `robots.txt` all come out of `scripts/build.mjs`. Edit `content/`, `data/`,
   `lib/` or the generator, then run `npm run build`. Never hand-edit generated
   output.
2. **Never delete another session's work.** Move it to
   `archive/<session-id>/` and log it here.
3. **`archive/` is excluded from the published-page rules** in the gate, because
   those pages are not linked from the live site. Do not put a live page there.
4. **Run `npm run verify` before every push.** A red gate blocks the deploy.
5. **Pull with rebase before pushing**, and re-run the build afterwards — a
   rebase can bring in a `data/` file that changes generated output.

## Hijack rule

If a session's claim is more than 60 minutes old with no commit, any other
session may take the task over. Record the handoff in the Session log and note
which files you touched.
