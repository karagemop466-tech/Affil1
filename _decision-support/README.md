# Decision Desk

Working papers that sit **beside** the shop, not inside it: the executive summary, the product
shelf and its confirmation register, a 28-row suggestion board, the open questions that block
decisions, a 49-entry source register, and a twelve-guide publishing plan.

Plain HTML, CSS and JavaScript. No build step, no dependencies, no network calls, no analytics,
no cookies. The only state is your own adopt/park/reject selections, kept in `localStorage`.

## Pages

| Page | For | Contains |
| --- | --- | --- |
| `index.html` | orientation | KPI row, the three blocking unknowns, the overlap map of the repository, method |
| `executive-summary.html` | the decision maker | priorities scored, inventory, economics with the gated numbers left blank, six ranked risks, four-week plan |
| `products.html` | the shop floor | five products, the product-intent confirmation register (intent and observation in **separate** columns), the five compliance rules that decide the copy |
| `suggestions.html` | choosing a path | 28 suggestions across three paths, each with files, hours and a gate; adopt / park / reject; export to markdown; six refused ideas |
| `questions.html` | unblocking | 14 questions with what we have, what is missing, how to find out, who can answer; 9 answers already settled |
| `verification.html` | the sceptic | 49 source entries with verbatim official text, per-marketplace product evidence, 10 irregularities, reproduction commands |
| `editorial-plan.html` | the reader | three clusters, twelve guides, per-page findability checklist, cadence with stop conditions, six slop checks |

## Check it

```bash
python3 _decision-support/validate.py --json
```

Exit `0` means all six check families hold:

1. every local reference resolves to a file that exists (plus every in-page `#fragment`);
2. the exact Associates disclosure sentence appears above the masthead **and** in the footer of
   every page, and every page is structurally sound (balanced markup, `<title>`, viewport, `alt`);
3. every outbound storefront product link carries `rel="sponsored nofollow noopener"`, and no
   live link embeds an Associates `tag=` while enrolment is unconfirmed;
4. no price-like figure appears in reader text, and the promotional phrasings this project refuses
   are absent from prose (quoted policy text and the lint list itself are exempt);
5. every register row cites something a person can open — an official URL, a file path, or a
   command that reproduces it;
6. counts asserted in prose are recomputed from the tables, so the numbers cannot rot.

`--json` rewrites `_data/decision-desk.json` **from the same HTML a human reads** — the
machine-readable registers are derived, never hand-maintained, so they cannot drift.

## Deliberate absences

- **No prices, ratings, review counts, ranks or "best" badges.** Program Policies permit price and
  availability only where Amazon serves the link containing that data or via the Creators/PA API.
  Prices visible in captured listing snapshots were discarded rather than published.
- **No revenue forecast, conversion score or traffic promise.** There is no authorised report data.
- **No claim that the submitted short links are invalid.** Their compliance status is unresolved and
  stays unresolved; they are described as unobserved from this environment.
- **No tagged Special Links.** Enrolment for `shopnow047c-20` is unconfirmed, so outbound product
  links here are plain editorial links marked `sponsored`.

## Conventions

- Registers are keyed so a claim can be walked back to a sentence: `P-0n` products,
  `A-/F-/G-/R-` sources (Amazon, FTC, Google, repo), `IRR-0n` irregularities, `Q-0n` questions,
  `S-0n` suggestions.
- Anything an agent cannot verify from an official source is left **blank and flagged**, never inferred.
- `assets/desk.css` and `assets/desk.js` are scoped to this directory on purpose: other sessions own
  the root stylesheet and navigation, so nothing here can collide with them.
