#!/usr/bin/env python3
"""Package only the maintained edition; never upload the repository itself."""
import shutil
import sys
from pathlib import Path

from build import GENERATED, ROOT


def stage(destination):
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise SystemExit(f"Staging directory must be empty: {destination}")
    files = GENERATED | {'.nojekyll'}
    files |= {
        str(path.relative_to(ROOT)) for path in (ROOT / 'assets').rglob('*')
        if path.is_file() and (path.suffix in {'.woff2', '.svg'} or
           path.name in {'site.css', 'storefront.css', 'site.js', 'analytics.js'} or
           path.stem.endswith(('-w560', '-w760', '-w900', '-w1280')))
    }
    for name in sorted(files):
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)


if __name__ == '__main__':
    stage(Path(sys.argv[1]))
