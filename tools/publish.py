#!/usr/bin/env python3
"""What GitHub Pages is allowed to serve, and nothing else.

There are two ways to publish this repository:

  * **legacy branch build** (what the repository is configured for today:
    `pages` → `build_type: legacy`, source `main` `/`). GitHub runs Jekyll over
    the branch and publishes every file except what `_config.yml` excludes.
  * **workflow build** (`build_type: workflow`): the workflow uploads exactly the
    directory `tools/stage.py` produced, so nothing else can leak.

Only the second is safe by construction. The first has been publishing the whole
repository: `/src/data/products.json`, `/tools/build.py`, `/data/confirmations.json`
and a second full storefront at `/archive/notes-edition/` are all reachable on the
public site (observed 2026-11-20). That contradicts the site's own claim to be
"one site" and it puts unreviewed drafts in front of readers.

This module is the single list of files a reader may fetch. Both `tools/stage.py`
(workflow build) and `tools/check.py` (gate) read it, and `_config.yml`'s `exclude`
list is derived from it so the legacy build agrees. A file that is not listed here
is published by neither route.

Adding a page therefore takes three edits, all in code a reviewer can diff:
`tools/build.py` GENERATED, a generator, and this file.
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Directories a reader may never reach. Derived from the repository layout, not
# from a hand-kept list of files, so a new tool or a new archive is excluded by
# default rather than by remembering.
PRIVATE_DIRS = (
    ".github", "_includes", "_layouts", "_sass", "analytics", "archive",
    "decision-support", "docs", "kitchen", "kitchen-build",
    "legacy", "measurement", "node_modules", "server", "src", "tools", "vendor",
    "reviews", "dashboard", "flagged", "topics",
)

# Files at the repository root that are working papers or build inputs.
PRIVATE_ROOT_FILES = (
    ".gitignore", "COORDINATION.md", "EXECUTIVE_SUMMARY.md", "LICENSE",
    "PUBLISHING_WORKFLOW.md", "README.md", "requirements.txt", "package.json",
    "package-lock.json",
)

# Public files that are not generated pages: stylesheets, scripts, images, the
# feed and the robots file. Images and fonts are matched by name pattern because
# `assets/img` only ever contains editorial illustrations the image policy covers.
PUBLIC_ASSET_PATTERNS = (
    "assets/css/site.css",
    "assets/css/storefront.css",
    "assets/css/editorial.css",
    "assets/css/fit.css",
    "assets/js/site.js",
    "assets/js/analytics.js",
    "assets/js/fit.js",
    "assets/js/discover.js",
    "assets/js/counter-config.js",
)


# Served, internally linked, and deliberately absent from sitemap.xml.
#
# A sitemap is a list of what you want in search results. These pages are the
# working register behind the shop: the review queue, the open questions, the
# suggestions a reviewer has not chosen between, the decision gate, the executive
# brief and the campaign ledger. Until 2026-11-20 they were 21 of the 30 sitemap
# entries, so the only thing a crawler was told this site is about was its own
# audit trail. They remain crawlable (no `noindex` on most, canonical present) and
# every one is reachable from the footer groups "The desk" and "Trust".
SITEMAP_EXCLUDE = (
    "brief/", "decide/", "operations/", "questions/", "review/", "suggestions/",
)


def in_sitemap(path):
    """True when a generated page belongs in sitemap.xml."""
    if path == "404.html":
        return False
    return not path.startswith(SITEMAP_EXCLUDE)


def generated_pages():
    """Exactly the paths tools/build.py writes. Imported, never re-typed."""
    import sys
    if str(ROOT / "tools") not in sys.path:
        sys.path.insert(0, str(ROOT / "tools"))
    import build
    return set(build.GENERATED)


def public_tree():
    """The complete set of repo-relative paths GitHub Pages may serve."""
    files = set(generated_pages())
    for pattern in PUBLIC_ASSET_PATTERNS:
        if (ROOT / pattern).exists():
            files.add(pattern)
    for path in (ROOT / "assets/img").glob("*"):
        if path.is_file():
            files.add(path.relative_to(ROOT).as_posix())
    for path in (ROOT / "assets/fonts").glob("*"):
        if path.is_file():
            files.add(path.relative_to(ROOT).as_posix())
    files.add(".nojekyll")
    return {f for f in files if (ROOT / f).exists()}


def jekyll_exclude():
    """The complement of public_tree, in the form `_config.yml` wants.

    Jekyll excludes paths, not "everything but these", so this returns every
    top-level entry plus every private subdirectory and every root-level file
    that is not public. Anything new at the root is therefore excluded until it
    is deliberately added to the allow-list above.
    """
    files = public_tree()
    public_top = {f.split("/")[0] for f in files if "/" in f}
    entries = set(PRIVATE_DIRS)
    entries |= set(PRIVATE_ROOT_FILES)
    for path in ROOT.iterdir():
        if path.name.startswith(".") and path.name != ".nojekyll":
            continue
        if path.is_file() and path.name not in files:
            entries.add(path.name)
        if path.is_dir() and path.name not in public_top and path.name != ".git":
            entries.add(path.name)
    # Never exclude a directory that still contains a public file, and never
    # exclude a path nested inside a directory that is published whole.
    entries -= public_top
    entries = {e for e in entries
               if not any(e.startswith(top + "/") for top in public_top)}
    return sorted(e for e in entries if (ROOT / e).exists())


def stale_notes():
    """Generated pages that still contain their build-input breadcrumbs.

    Not an error by itself, but a page that mentions `src/data/` in visible text
    is telling a reader about files they can no longer open, so the gate warns.
    """
    hits = []
    for f in sorted(generated_pages()):
        p = ROOT / f
        if not p.exists():
            continue
        text = re.sub(r"<script.*?</script>", " ", p.read_text(encoding="utf-8"), flags=re.S)
        for m in re.finditer(r"\b(src/data|tools|archive)/[A-Za-z0-9_./-]+", text):
            hits.append((f, m.group(0)))
    return hits


def write_config(path=None):
    """Rewrite `_config.yml`'s exclude list from the allow-list."""
    path = path or (ROOT / "_config.yml")
    text = path.read_text(encoding="utf-8")
    head = text.split("exclude:", 1)[0]
    body = "exclude:\n" + "".join(f"  - {e}\n" for e in jekyll_exclude())
    path.write_text(head + body, encoding="utf-8")
    print(f"wrote {len(jekyll_exclude())} exclude entries to {path.name}")


if __name__ == "__main__":
    import sys as _sys
    if "--write-config" in _sys.argv:
        write_config()
    else:
        tree = public_tree()
        print(f"public files: {len(tree)}")
        for f in sorted(tree):
            print("  " + f)
        print("\n_config.yml exclude:")
        for e in jekyll_exclude():
            print("  - " + e)
