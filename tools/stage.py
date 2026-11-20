"""Stage only the canonical publication, never the repo or raw campaign data."""
from build import ROOT, GENERATED
from shutil import copy2, copytree, rmtree

out = ROOT / 'dist'
rmtree(out, ignore_errors=True)
for name in GENERATED:
    dest = out / name
    dest.parent.mkdir(exist_ok=True, parents=True)
    copy2(ROOT / name, dest)
copytree(ROOT / 'assets', out / 'assets')
