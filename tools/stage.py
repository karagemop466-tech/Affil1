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
    # The artifact is prebuilt. Branch-based Pages can still use the repository's
    # Jekyll exclusions; this marker belongs to the artifact, not the checkout.
    (destination / '.nojekyll').touch()
    files = GENERATED | {str(path.relative_to(ROOT)) for path in (ROOT / 'assets').rglob('*') if path.is_file()}
    for name in sorted(files):
        if not (ROOT / name).exists():
            print(f"stage: skipping missing {name}")
            continue
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)


if __name__ == '__main__':
    stage(Path(sys.argv[1]))
