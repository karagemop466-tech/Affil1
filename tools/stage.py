#!/usr/bin/env python3
"""Package only the maintained edition; never upload the repository itself.

The list of public files comes from `tools/publish.py`, which is also what
`_config.yml` is derived from and what `tools/check.py` enforces. Before this
existed, the workflow build and the legacy branch build published different sets:
the workflow uploaded a slice, the branch uploaded everything, and the live site
consequently served `/src/data/products.json`, `/tools/build.py` and a second
storefront under `/archive/`.
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
        raise SystemExit(f"stage: public tree lists files that do not exist: {missing}")
    print(f"staged {len(files)} files")


if __name__ == '__main__':
    stage(Path(sys.argv[1]))
