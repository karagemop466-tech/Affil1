#!/usr/bin/env python3
"""Check every internal link in the repository, including archived prior work.

`scripts/check_site.py` gates the published site. This script is wider: it walks
every HTML file in the repository, including the archived sessions, and reports any
internal reference that does not resolve. Archived work is preserved rather than
published, so it still has to render without a broken link.

Exit status is 0 when every link resolves, 1 otherwise.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The site is served from a subpath (e.g. /Affil1/). Root-absolute links in the
# generated HTML carry that prefix, so strip it before resolving on disk.
sys.path.insert(0, ROOT)
try:
    from urllib.parse import urlparse
    import site_data as D
    BASE_PATH = urlparse(D.SITE["origin"].rstrip("/")).path.rstrip("/")
except Exception:
    BASE_PATH = ""

LINK_RE = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"', re.I)
SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__", "_site", ".venv"}
SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "//", "#")


def html_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(base, f)


def main():
    broken = []
    checked = 0
    for path in html_files():
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        try:
            body = open(path, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError):
            continue
        for href in LINK_RE.findall(body):
            href = href.strip()
            if not href or href.startswith(SKIP_SCHEMES):
                continue
            target = href.split("#")[0].split("?")[0]
            if not target:
                continue
            checked += 1
            if target.startswith("/"):
                if BASE_PATH and (target == BASE_PATH or target.startswith(BASE_PATH + "/")):
                    target = target[len(BASE_PATH):] or "/"
                resolved = os.path.normpath(os.path.join(ROOT, target.lstrip("/")))
            else:
                resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(resolved):
                broken.append((rel, href))

    print("Checked %d internal references across the repository." % checked)
    if broken:
        print("FAILED: %d broken reference(s)" % len(broken))
        for rel, href in broken[:50]:
            print("  %s -> %s" % (rel, href))
        return 1
    print("Every internal reference resolves.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
