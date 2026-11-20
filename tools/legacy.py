#!/usr/bin/env python3
"""Mark the parallel editions noindex so search engines see one shop.

Two editions of this site were built in parallel on this repository. The root
build owns index.html, sitemap.xml and feed.xml and is treated as canonical.
The other edition (crisp/ and several root-level pages) is still served, and
deleting it would break any existing link and destroy another session's work.

So the other edition is left in place and marked noindex, follow. That is the
reversible half of "one site for search engines to index": the pages still work
for a reader who has the URL, and Google is told not to index them twice.

Idempotent by construction: if the meta tag is already there, nothing changes.
That matters because CI rebuilds the tree and diffs it against a copy.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

TAG = '<meta name="robots" content="noindex, follow">'
NOTE = ("<!-- Parallel edition: retained for link stability, excluded from the index.\n"
        "     The canonical publication is the site root. See COORDINATION.md. -->")


def legacy_pages():
    from build import GENERATED  # imported lazily: build imports this module

    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", "node_modules/")):
            continue
        if rel in GENERATED:
            continue
        yield path, rel


def mark(path):
    text = path.read_text(encoding="utf-8")
    if 'content="noindex' in text[:2000]:
        return False
    if "<head>" not in text:
        return False
    text = text.replace("<head>", "<head>\n" + TAG + "\n" + NOTE, 1)
    # A legacy page that claims a canonical for itself would contradict the
    # noindex. Point it at the root of the canonical edition instead.
    text = re.sub(
        r'<link rel="canonical" href="[^"]*Affil1/[^"]*">',
        '<link rel="canonical" href="https://karagemop466-tech.github.io/Affil1/">',
        text, count=1)
    path.write_text(text, encoding="utf-8")
    return True


def main():
    changed = [rel for path, rel in legacy_pages() if mark(path)]
    total = sum(1 for _ in legacy_pages())
    print(f"legacy pages: {total} ({len(changed)} newly marked noindex)")
    for rel in changed:
        print("  noindex  " + rel)


if __name__ == "__main__":
    main()
