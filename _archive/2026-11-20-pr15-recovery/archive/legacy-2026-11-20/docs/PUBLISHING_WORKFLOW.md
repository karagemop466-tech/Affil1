# Publishing workflow — compliance gate (integration version)

The workflow that was previously a checklist is now enforced by the build gate
(`scripts/check.mjs`) and its negative self-test (`scripts/test-gate.mjs`).
Nothing publishes on a red run. CI runs all three steps on every push to `main`
and every pull request (`.github/workflows/deploy-pages.yml`).

## Gate rules and the policy each one traces to

| Rule | Check | Source |
|---|---|---|
| C01 | Disclosure present in the exact required wording, directly under the masthead (above the fold), plus footer repeat | Operating Agreement §5 (S01); FTC placement guidance (S18) |
| C03 | Every outbound Amazon product anchor carries the Associates tag (`shopnow047c-20`) as a URL parameter | Program Policies, Participation Requirements §2 (S02) |
| C04 | Every outbound product link carries `rel="sponsored"` and a visible destination label | Program Policies §1(w) + FTC (S03, S18) |
| C05 | No shortener or redirect on published controls; the anchor's href is the Amazon URL | Program Policies §1(w), §1(v), §1(r) (S03, S08, S09) |
| C06 | No price is published | Program Policies §2(b) (S05) |
| C07 | No star rating or review text is published | Program Policies §1(t) (S04) |
| C08 | No hands-on testing claim appears | FTC endorsement guidance (S19) |
| LNK | No broken internal link | — |
| SM | Sitemap covers every published page; canonicals absolute and self-referencing | Google sitemap docs (S20) |

## Before publishing a new page or guide

1. Add the content to `content/` or `data/`, never to generated HTML.
2. Run `npm run verify` (build + gate + negative self-test).
3. Confirm the new page is in `sitemap.xml` and, if it is an article, in `feed.xml`
   (both are generated — the build does this).
4. Records changes (new flags, new register rows) go in `data/` with a source URL
   for every claim; unconfirmed values stay blank and flagged.
5. Merge to `main`. GitHub Pages publishes from `main`; a green gate is the
   publish precondition.

Reviewer / date / decision: ____________________
