#!/usr/bin/env python3
"""Flip the monetization gate — an owner action, wrapped so it cannot be half-done.

This site publishes reference links until its Associates enrolment is confirmed,
because a tracking tag is an assertion that the site is registered to that ID in an
enrolled account, and only the account owner can know that. This script is the
human-facing switch: it records the confirmations, stores the Special Links that
Associates Central generated, rebuilds, and re-runs the gate.

Run it only after doing the three things in the checklist it prints. It refuses to
arm the site from an agent context unless --i-am-the-owner is passed, so that a
future automated session cannot decide on its own to start claiming a relationship
with Amazon.

  python3 tools/arm_links.py --status
  python3 tools/arm_links.py --checklist
  python3 tools/arm_links.py --i-am-the-owner --confirm-enrollment --confirm-site --confirm-one-link-test
  python3 tools/arm_links.py --i-am-the-owner --link P-01 "https://www.amazon.com/dp/B0CDY277D3?tag=shopnow047c-20&linkCode=..."
"""

import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data" / "product-intent.json"

STEPS = [
    "Sign in to Associates Central and confirm the tracking ID is active on an enrolled account.",
    "Add this site (karagemop466-tech.github.io/Affil1) to the account's listed websites.",
    "For ONE product: generate the Special Link, paste it with --link, publish, click it once,",
    "and confirm the click appears in the account's reports. Only then arm the other four.",
]


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def status():
    d = load()
    approved = [r["ref"] for r in d["records"] if r.get("approved_special_link")]
    print(f"tracking ID supplied: {d['tracking_id_supplied']}")
    for key in ("associate_enrollment_confirmed", "site_registered", "one_link_test_completed"):
        print(f"  {key:34} {d.get(key)}")
    print(f"  approved_special_link filled for:      {', '.join(approved) or 'none'}")
    live = bool(d.get("associate_enrollment_confirmed") and d.get("site_registered")
                and d.get("one_link_test_completed"))
    print(f"\npublished state: {'affiliate links' if live or approved else 'reference links only'}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--checklist", action="store_true")
    ap.add_argument("--confirm-enrollment", action="store_true")
    ap.add_argument("--confirm-site", action="store_true")
    ap.add_argument("--confirm-one-link-test", action="store_true")
    ap.add_argument("--link", nargs=2, action="append", metavar=("REF", "URL"))
    ap.add_argument("--i-am-the-owner", action="store_true")
    ap.add_argument("--no-build", action="store_true")
    args = ap.parse_args(argv)

    if args.checklist:
        print("Before arming a single link:\n")
        for s in STEPS:
            print("  " + s)
        print("\nSources: https://affiliate-program.amazon.com/help/operating/agreement")
        print("         https://affiliate-program.amazon.com/help/operating/policies")
        return 0

    mutating = (args.confirm_enrollment or args.confirm_site or args.confirm_one_link_test
                or bool(args.link))
    if not mutating:
        return status()
    if not args.i_am_the_owner:
        print("REFUSED: publishing a tracking tag asserts an enrolled, registered account.\n"
              "Only the owner can assert that. Re-run with --i-am-the-owner after completing\n"
              "the checklist (python3 tools/arm_links.py --checklist).", file=sys.stderr)
        return 3

    d = load()
    if args.confirm_enrollment:
        d["associate_enrollment_confirmed"] = True
    if args.confirm_site:
        d["site_registered"] = True
    if args.confirm_one_link_test:
        d["one_link_test_completed"] = True
    for ref, url in (args.link or []):
        if "amazon.com" not in url:
            print(f"REFUSED: {ref} -> not an amazon.com URL", file=sys.stderr)
            return 4
        rec = next((r for r in d["records"] if r["ref"] == ref.upper()), None)
        if rec is None:
            print(f"REFUSED: unknown product ref {ref}", file=sys.stderr)
            return 4
        rec["approved_special_link"] = url
        rec["confirmation_date"] = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%MZ"],
                                                   capture_output=True, text=True).stdout.strip()
        rec["confirmation_source"] = "entered by the account owner via tools/arm_links.py"
        print(f"{ref}: Special Link recorded ({rec['confirmation_date']})")

    DATA.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
    print("wrote src/data/product-intent.json")
    if not args.no_build:
        subprocess.run([sys.executable, str(ROOT / "tools" / "build.py")], check=True)
        subprocess.run([sys.executable, str(ROOT / "tools" / "validate.py")], check=True)
        print("\nrebuilt and gated; commit src/data/product-intent.json plus the generated pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
