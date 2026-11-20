#!/usr/bin/env python3
"""Re-run the audit rows that can be re-run, and prove the register is honest.

Three modes:

  --jsonld       every application/ld+json block on every published page parses
  --single-site  no crawlable competing surface: robots.txt disallows archive/
                 and decision-support/, and every .html file there declares
                 noindex
  (default)      the register itself is well formed: unique ids, four known
                 result values, a source link on every row that is not marked
                 unverified, and -- the part that matters -- every row in
                 src/data/audit.json appears on the published review/audit.html
                 page, so a row cannot be quietly dropped from publication.

Exit code is 0 only when all selected checks pass.
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESULTS = {"pass", "fixed", "unverified", "open"}


def jsonld():
    bad = []
    n = 0
    for f in sorted(ROOT.rglob("*.html")):
        rel = f.relative_to(ROOT).as_posix()
        if rel.startswith(("archive/", "decision-support/")):
            continue
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                                f.read_text(encoding="utf-8"), re.S):
            n += 1
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                bad.append(f"{rel}: {exc}")
    print(f"json-ld blocks parsed: {n}, failures: {len(bad)}")
    for b in bad:
        print("  ", b)
    return not bad


def single_site():
    problems = []
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    for need in ("Disallow: /archive/", "Disallow: /decision-support/"):
        if need not in robots:
            problems.append(f"robots.txt is missing {need!r}")
    for section in ("archive", "decision-support"):
        for f in sorted((ROOT / section).rglob("*.html")):
            text = f.read_text(encoding="utf-8")
            if not re.search(r'<meta[^>]+name="robots"[^>]+noindex', text):
                problems.append(f"{f.relative_to(ROOT)} has no noindex meta tag")
    print(f"single-site surfaces checked: robots.txt plus every .html under archive/ and decision-support/")
    print(f"problems: {len(problems)}")
    for p in problems[:20]:
        print("  ", p)
    if len(problems) > 20:
        print(f"   ... and {len(problems) - 20} more")
    return not problems


def register():
    doc = json.loads((ROOT / "src/data/audit.json").read_text(encoding="utf-8"))
    rows = doc["rows"]
    problems = []
    seen = set()
    for r in rows:
        if r["id"] in seen:
            problems.append(f"duplicate id {r['id']}")
        seen.add(r["id"])
        if r["result"] not in RESULTS:
            problems.append(f"{r['id']}: unknown result {r['result']!r}")
        src = (r.get("source") or "").strip()
        if r["result"] != "unverified" and not src:
            problems.append(f"{r['id']}: claims {r['result']} but cites no source")
        if src.startswith("repo:"):
            target = ROOT / src[len("repo:"):]
            if not target.exists():
                problems.append(f"{r['id']}: cites a repository path that does not exist: {src[5:]}")
        elif src and not src.startswith("http"):
            problems.append(f"{r['id']}: source is neither an https URL nor a repo: path")
        for field in ("claim", "evidence", "verify", "area"):
            if not str(r.get(field, "")).strip():
                problems.append(f"{r['id']}: empty {field}")
    page = ROOT / "review/audit.html"
    if page.exists():
        text = page.read_text(encoding="utf-8")
        missing = [r["id"] for r in rows if f'id="{r["id"]}"' not in text]
        if missing:
            problems.append(f"rows in the data file but not on the page: {missing}")
    else:
        problems.append("review/audit.html does not exist")
    counts = {k: sum(1 for r in rows if r["result"] == k) for k in sorted(RESULTS)}
    print(f"audit rows: {len(rows)} {counts}")
    print(f"problems: {len(problems)}")
    for p in problems:
        print("  ", p)
    return not problems


def published_counts():
    """Every number on review/audit.html must equal the number computed now.

    The first draft of this page said "30 pages" in three rows while the build
    was already producing 31, which is the exact failure mode the register was
    written to expose. Rows therefore quote the command, not a count, and the
    counts that do appear in the header are checked here.
    """
    doc = json.loads((ROOT / "src/data/audit.json").read_text(encoding="utf-8"))
    rows = doc["rows"]
    page = (ROOT / "review/audit.html").read_text(encoding="utf-8")
    counts = {k: sum(1 for r in rows if r["result"] == k) for k in RESULTS}
    problems = []
    import re
    for pattern, expected in (
        (r"makes (\d+) claims about itself", len(rows)),
        (r"(\d+) claims audited", len(rows)),
        (r"(\d+) pass &middot;", counts["pass"]),
        (r"(\d+) fixed in this pass &middot;", counts["fixed"]),
        (r"(\d+) unverified &middot;", counts["unverified"]),
        (r"(\d+) open<", counts["open"]),
    ):
        m = re.search(pattern, page)
        if not m:
            problems.append(f"page does not state {pattern!r}")
        elif int(m.group(1)) != expected:
            problems.append(f"{pattern!r} says {m.group(1)}, computed {expected}")
    print(f"published counts: claims={len(rows)} {counts} -> {'ok' if not problems else 'mismatch'}")
    for p in problems:
        print("  ", p)
    return not problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonld", action="store_true")
    ap.add_argument("--single-site", action="store_true")
    ap.add_argument("--counts", action="store_true")
    args = ap.parse_args()
    if args.jsonld:
        ok = jsonld()
    elif args.single_site:
        ok = single_site()
    elif args.counts:
        ok = published_counts()
    else:
        ok = register()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
