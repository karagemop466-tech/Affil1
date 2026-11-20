#!/usr/bin/env python3
"""Every image a reader can load must have a row in the image register.

The shop publishes an image policy (review/images.html) whose whole claim is that
each asset here is commissioned, unbranded and labelled. That claim is only true
if the list under it is complete, and it was not: a merge on 2026-11-20 left one
guide's illustration out of _src/data/images.json while the page still loaded it.

So the rule is checked instead of remembered. Two directions, two severities:
an asset a page loads but the register does not describe is an error, because the
policy page is then incomplete on a live surface; a registered asset that nothing
loads is a warning, because it is only stale bookkeeping.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REF = re.compile(r'(?:src|href|content)="[^"]*assets/img/([a-z0-9-]+?)(?:-w\d+)?\.(?:jpg|png|svg)"')
# Interface furniture, not editorial imagery. The register's claim is about pictures
# a shopper might mistake for the product; a favicon is not one, and neither is a
# logo mark, so they are excluded by name rather than left out and wondered about.
NOT_IMAGERY = {"favicon"}


def referenced():
    """Asset stems referenced by the generated, served pages of the shop."""
    from build import GENERATED
    out = {}
    for rel in GENERATED:
        if not rel.endswith(".html"):
            continue
        path = ROOT / rel
        if not path.is_file():
            continue
        for stem in REF.findall(path.read_text(encoding="utf-8")):
            if stem in NOT_IMAGERY:
                continue
            out.setdefault(stem, set()).add(rel)
    return out


def main():
    register = json.loads((ROOT / "_src" / "data" / "images.json").read_text())
    registered = {a["file"] for a in register["assets"]}
    refer = referenced()
    errors, warnings = [], []

    for stem, pages in sorted(refer.items()):
        if stem not in registered:
            errors.append(f"{stem}: loaded by {', '.join(sorted(pages))} but absent from "
                          f"the image register (_src/data/images.json)")

    for a in register["assets"]:
        f = a["file"]
        # An asset may exist only as responsive variants (storefront-hero-w1280.jpg),
        # which is how the build ships them, so the widths are part of the search.
        on_disk = (list((ROOT / "assets" / "img").glob(f + ".*"))
                   + list((ROOT / "assets" / "img").glob(f + "-w*.*")))
        if not on_disk:
            errors.append(f"{f}: registered but no such file on disk")
        if f not in refer:
            warnings.append(f"{f}: registered but not referenced by any generated page")

    print(f"image register: {len(registered)} rows, {len(refer)} assets referenced by "
          f"the generated pages")
    for e in errors:
        print("  ERR ", e)
    for w in warnings:
        print("  warn", w)
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
