#!/usr/bin/env python3
"""Quarantine the superseded edition: noindex, keep the files.

Parallel sessions published a second edition at crisp/, reviews/, categories/
and at root-level pages such as products.html and dashboard.html. Those files
belong to those sessions and are not deleted here. What this script does is stop
them competing with the canonical site in search results:

  * adds <meta name="robots" content="noindex, follow"> to every HTML file that
    this build does not generate
  * adds a small, dismissible-free banner at the top of each one pointing at the
    current page, so a reader who lands there is not stranded

It is idempotent: running it twice changes nothing. It never edits a file in
_tools/build.py's GENERATED set, and it refuses to run if that list cannot be
imported, because guessing which pages are "ours" is how you delete someone
else's work.

Usage:  python3 _tools/quarantine_legacy.py [--dry-run]
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "_tools"))

from build import GENERATED  # noqa: E402  (the single definition of "ours")

MARK = "<!-- legacy-edition-quarantined -->"
META = '<meta name="robots" content="noindex, follow">'


def banner(depth: int) -> str:
    up = "../" * depth
    return (
        f'{MARK}<div role="note" style="background:#17251f;color:#f5efe2;'
        'font:14px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;'
        'padding:10px 16px;text-align:center">'
        "This page is from an earlier edition of the site and is kept for reference. "
        f'<a href="{up}index.html" style="color:#e9b44c;text-decoration:underline">'
        "Go to the current site</a>.</div>"
    )


def candidates():
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in {".git", "node_modules"}:
            continue
        if rel.as_posix() in GENERATED:
            continue
        yield path, rel


def main() -> int:
    dry = "--dry-run" in sys.argv
    changed, skipped, failed = [], [], []
    for path, rel in candidates():
        text = path.read_text(encoding="utf-8", errors="replace")
        if MARK in text:
            skipped.append(rel.as_posix())
            continue
        depth = len(rel.parts) - 1
        if "<head>" not in text:
            failed.append((rel.as_posix(), "no <head>"))
            continue
        text = text.replace("<head>", "<head>\n" + META, 1)
        if "<body" in text:
            idx = text.find(">", text.find("<body")) + 1
            text = text[:idx] + "\n" + banner(depth) + text[idx:]
        else:
            failed.append((rel.as_posix(), "no <body>"))
            continue
        if not dry:
            path.write_text(text, encoding="utf-8")
        changed.append(rel.as_posix())

    print(f"quarantined: {len(changed)}")
    for c in changed:
        print("  " + c)
    if skipped:
        print(f"already quarantined: {len(skipped)}")
    if failed:
        print(f"could not quarantine: {len(failed)}")
        for name, why in failed:
            print(f"  {name}: {why}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
