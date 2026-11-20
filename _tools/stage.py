#!/usr/bin/env python3
"""Package only the maintained edition; never upload the repository itself.

Legacy Pages ignores this and serves the branch root. The root stays safe to
serve because every working directory is underscore-prefixed (see
PAGE_HOSTING_PATHS in _tools/check.py, and PUBLISHING_WORKFLOW.md). This script
remains the way to preview or move to a workflow-based deploy, where _site, not
the branch, is what gets published.
"""
import json
import shutil
import sys
from pathlib import Path

from build import GENERATED, ROOT


def stage(destination):
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise SystemExit(f"Staging directory must be empty: {destination}")
    (destination / '.nojekyll').touch()
    # Images registered in the image register always ship, at any size: the
    # img() helper falls back to a single-size original when width variants
    # do not exist, so the base .jpg must be staged for that fallback to work.
    registered = {
        a['file'] for a in json.loads(
            (ROOT / '_src/data/images.json').read_text(encoding='utf-8'))['assets']
    }
    files = set(GENERATED)
    files |= {
        str(path.relative_to(ROOT)) for path in (ROOT / 'assets').rglob('*')
        if path.is_file() and (path.suffix in {'.woff2', '.svg'} or
           path.name in {'editorial.css', 'discover.js', 'storefront.css', 'site.css', 'site.js', 'analytics.js', 'fit.css', 'fit.js'} or
           path.stem.endswith(('-w560', '-w760', '-w900', '-w1280')) or
           (path.suffix == '.jpg' and path.stem in registered))
    }
    for name in sorted(files):
        if not (ROOT / name).exists():
            print(f"stage: skipping missing {name}")
            continue
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)


if __name__ == '__main__':
    stage(Path(sys.argv[1]))
