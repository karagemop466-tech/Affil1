# Affil1

An Amazon Associates site for countertop cooking appliances. It has two sections,
built by different sessions and merged without either discarding the other.

| Section | URL | Contents |
| --- | --- | --- |
| **Good Measure Kitchen Notes** | https://karagemop466-tech.github.io/Affil1/ | Storefront, guide set, dashboard, categories, flagged review |
| **Crisp & Counter** | https://karagemop466-tech.github.io/Affil1/crisp/ | Publication front page, 4 guides, compare, products, and the register set |

Both disclose the affiliate relationship above the fold and neither publishes a
price without an Amazon-served feed.

## Crisp & Counter (`crisp/`)

Live: https://karagemop466-tech.github.io/Affil1/crisp/

## What this is

Buying guides that state what a product's listing claims, and refuse to state
anything else. No prices, ratings, review counts or stock figures appear
anywhere, because Amazon permits them only when Amazon serves the data or it
arrives through its API — and no such feed is connected here.

## Layout of `crisp/`

```
crisp/index.html           front page (generated)
crisp/guides/              four question-shaped buying guides (generated)
crisp/compare/             form-factor comparison (generated)
crisp/products/            identifier register (generated)
crisp/about/  sources/  suggestions/  questions/  flagged/  legacy/
src/data/*.json            the single source of truth for every figure and claim
src/data/products.json     product observations, intended vs observed identifiers kept apart
src/data/compliance.json   verbatim policy quotations with URLs
src/data/flags.json        every unverified value and irregularity
src/data/suggestions.json  scored proposals awaiting a decision
src/data/questions-open.json  what is needed to answer each open question
tools/build.py             renders every page from the data
tools/content.py           editorial copy
tools/validate.py          647 pre-publish checks
docs/EXECUTIVE-SUMMARY.md  what was found and what to do next
docs/MEASUREMENT.md        the five events, and why none is live
COORDINATION.md            shared task board for parallel sessions
```

All links inside `crisp/` are relative, because GitHub Pages serves this repo
under `/Affil1/` and absolute root paths would 404 there.

Pages are **generated**. Edit the JSON in `src/data/` or the copy in
`tools/content.py`, then:

```bash
python3 tools/build.py      # renders crisp/ from src/data + tools/content.py
python3 tools/validate.py   # 600 checks, scoped to crisp/ only
```

Do not hand-edit the HTML: it is overwritten on the next build. This is
deliberate — the disclosure strip and footer are emitted by one template, so no
page can ship without them.

## Editorial rule

A capability is stated only if it appears in the seller's own listing title.
Everything else is framed as a question the reader should ask, or omitted.

## Compliance

- Affiliate disclosure above the fold on every page, repeated in the footer.
- Every buy link carries `rel="sponsored nofollow noopener"`.
- No price, rating or availability figure anywhere (Program Policies 2(b)).
- No third-party scripts, no cookies, no tracking.
- Policy citations are backed by verbatim quotations with source URLs.

Unverified items are published at `crisp/flagged/` with source links.

`tools/validate.py` validates only `crisp/`. The storefront at the repo root is
another session's scope and is not policed by this tool.

## Known gaps

All five supplied link codes are nine characters; an ASIN is ten. Four links
resolved to identifiable listings whose ASINs are recorded. The fifth never
resolved. Tracking attribution and commission rates require Associates account
access. See `/flagged/`.
