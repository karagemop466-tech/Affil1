# Publishing workflow

How a page gets from an idea to the live site, and what stops it.

## Cadence

One guide a fortnight. Eight exist. The pace is deliberately slower than the
category average because each guide has to be written from listing facts and
general reasoning rather than from a test that did not happen.

A guide is not published to fill a slot. If there is nothing honest to say about
a topic, the slot is skipped and the RSS feed stays quiet.

## The gate

Every change passes through this order. A step that fails stops the chain.

| Step | Check | Who |
|---|---|---|
| 1 | Claim: does a source exist for this sentence? If not, cut the sentence, not the standard. | Editor |
| 2 | Product facts: transcribed from the listing title reached, or blank. | Editor |
| 3 | Marketing language: no price, rating, review count, stock phrase, or superlative. | `tools/check.py` |
| 4 | Disclosure: strip above `<main>`, repeated in the footer, "Paid links" label present. | `tools/check.py` |
| 5 | Links: every Amazon destination tagged, sponsored, nofollow, new tab. | `tools/check.py` |
| 6 | Structure: one `<h1>`, alt text, resolving internal links and anchors, canonical, description. | `tools/check.py` |
| 7 | One site: no stray `.html` outside the generated set or `archive/`. | `tools/check.py` |
| 8 | Reproducible: rebuild and diff — a hand-edited page fails CI. | `.github/workflows/pages.yml` |
| 9 | Human read of the rendered page on a phone. | Editor |

## What cannot be automated

Three things need a person, and the build does not pretend otherwise:

- **Whether a sentence is true.** The checker catches patterns, not meaning.
- **Whether a claim is supported.** A sentence can pass every regex and still be
  an unsupported opinion dressed as a fact.
- **Whether the disclosure is prominent enough.** The FTC frames this as a
  judgement about the reader, not a markup rule.

## Disclosure review

Reviewed at each publication against:

- Associates Program Operating Agreement §5 (required sentence);
- Associates Program Policies §2(b) (price/availability, and no misleading
  claims);
- FTC Endorsement Guides FAQ, affiliate section (placement and wording).

The rule the site applies: the disclosure sits under the masthead on every page,
the footer repeats it, and every product card carries its own one-line affiliate
note next to the button. That is one more placement than the minimum, because the
FTC's guidance is that the closer the disclosure is to the recommendation, the
better.

## When a link changes destination

1. Open the link. Record the new `/dp/` ASIN, page title and category.
2. If the ASIN changed, update `observed_asin` in `src/data/products.json`. The
   buy URL is derived from it, so nothing else needs editing.
3. Never overwrite `intended_asin` with an observation. The two fields are
   separate by design.
4. Rebuild. `check.py` will confirm the new link is tagged and sponsored.
5. Add a line to the campaign ledger's provenance trail if the change came from a
   report rather than a manual check.

## When a new product is submitted

1. Open the link once, record where it lands.
2. If it does not land, publish it as unresolved — a blank row with a flag — not
   as a guess.
3. Write the note from the listing title only: what it is, who it suits, what
   trade the shape implies.
4. Add it to a category in `products.json` `meta.categories`; the front page and
   the register both read that list.
5. Do not write a guide around it until there is something true to say that is
   not already on the product page.
