#!/usr/bin/env python3
"""Package only what readers may fetch; never upload the repository itself.

The list comes from `_tools/publish.py`, which is the single allow-list that
`_config.yml`, this script and `_tools/check.py` all read. Before it existed the
workflow build uploaded a slice while the legacy branch build served the whole
repository, so `/src/data/products.json`, `/tools/build.py` and a second storefront
under `/archive/` were all reachable on the public URL.
"""
import shutil
import sys
from pathlib import Path

from publish import public_tree

ROOT = Path(__file__).resolve().parent.parent


def stage(destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise SystemExit(f"Staging directory must be empty: {destination}")
    files = public_tree()
    missing = []
    for name in sorted(files):
        source = ROOT / name
        if not source.is_file():
            missing.append(name)
            continue
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    if missing:
        raise SystemExit(f"stage: the allow-list names files that do not exist: {missing}")
    print(f"staged {len(files)} files")


if __name__ == '__main__':
    stage(Path(sys.argv[1]))
