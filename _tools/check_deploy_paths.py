#!/usr/bin/env python3
"""Resolve every internal link, image and asset over HTTP, from a simulated
GitHub Pages project mount (https://host/Affil1/).

The point of this check is the mount path. A root-absolute href like "/about/"
looks correct in a local preview served at "/" and 404s in production under
"/Affil1/", which is exactly how the earlier surfaces in this repository broke.
Filesystem checks cannot see that class of bug, because on disk "/about/" simply
does not exist as a project path at all.

Usage:
  python3 -m http.server 8207 --directory <parent-of-Affil1>   # serves /Affil1/
  MOUNT=http://127.0.0.1:8207/Affil1 python3 _tools/check_deploy_paths.py
"""

import os
import posixpath
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOUNT = os.environ.get("MOUNT", "http://127.0.0.1:8207/Affil1")
SKIP_DIRS = {"_archive", ".git", ".github", "node_modules"}


class Refs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.refs.append(a["href"])
        elif tag == "img" and a.get("_src"):
            self.refs.append(a["_src"])
        elif tag == "script" and a.get("_src"):
            self.refs.append(a["_src"])
        elif tag == "link" and a.get("href") and a.get("rel") in ("stylesheet", "icon", "alternate"):
            self.refs.append(a["href"])


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.relative_to(ROOT).parts) & SKIP_DIRS:
            continue
        yield p


def main():
    checked = 0
    failures = []
    for page in pages():
        parser = Refs()
        parser.feed(page.read_text(encoding="utf-8"))
        for ref in sorted(set(parser.refs)):
            if ref.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:", "javascript:")):
                continue
            target = ref.split("#")[0]
            if not target:
                continue
            if target.startswith("/"):
                # root-absolute: works only when the site owns the domain root
                url = MOUNT + target
                note = " (root-absolute: resolves above the project mount)"
            else:
                rel = posixpath.normpath(posixpath.join(str(page.parent.relative_to(ROOT)), target))
                url = MOUNT + "/" + rel.lstrip("./")
                note = ""
            checked += 1
            try:
                with urllib.request.urlopen(url, timeout=8) as resp:
                    if resp.status >= 400:
                        failures.append(f"{page.name}: {ref} -> HTTP {resp.status}")
            except urllib.error.HTTPError as e:
                failures.append(f"{page.name}: {ref} -> HTTP {e.code}{note}")
            except Exception as e:  # noqa: BLE001
                failures.append(f"{page.name}: {ref} -> {e}{note}")
    print(f"mount: {MOUNT}")
    print(f"internal references resolved over HTTP: {checked}")
    if failures:
        print(f"\nFAILED: {len(failures)} reference(s) do not resolve at the mount path")
        for f in failures[:40]:
            print("  ", f)
        sys.exit(1)
    print("every internal reference resolves at the project mount path")


if __name__ == "__main__":
    main()
