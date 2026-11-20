# Good Measure Kitchen — notes edition

A self-contained, static reader-facing publication inside the Affil1 repository:
shop-style front page (verified shortlist), seven question-first buyer guides, a
decision desk (suggestions queue + pre-decision questions) and a transparency desk.

- Everything here is hand-authored static HTML/CSS/JS — no generator owns it,
  so parallel-session rebuilds of the site root never touch this directory.
- Links to shared machinery (disclosure, privacy, dashboard, executive summary,
  the Crisp & Counter edition) are relative paths into the repository root.
- The verification register it cites lives at `../data/confirmations.json`.

Integration note for the site-root build owner (`tools/build.py`): this edition
is foreign to your build by design. If you link it from the generated root
navigation, point at `notes/`; its self-contained sitemap is `notes/sitemap.xml`.
