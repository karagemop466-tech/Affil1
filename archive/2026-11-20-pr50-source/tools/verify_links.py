#!/usr/bin/env python3
"""Re-resolve the register against Amazon and report drift. Read-only.

This is the automated half of the "test one link before you scale" instruction, and
the boundary of what an agent may do:

  * it requests each submitted link once, sequentially, with a polite delay;
  * it records the destination URL, the HTTP status and the page <title> only;
  * it never parses, stores or prints a price, a star rating, a review count or an
    availability string. Those are Program Content: Amazon permits them only when it
    serves the link that carries the data, or through the Creators/PA API. A site
    without a feed must not build one by scraping, and must not build price tracking
    or alerts at all (Participation Requirements).

What it does NOT do is the part it cannot do: confirming that a click is attributed to
`shopnow047c-20`. That is visible only inside the enrolled Associates account, so this
script reports the register and stops. The confirmation stays a human action by design.

Usage
  python3 tools/verify_links.py            # drift report against src/data/products.json
  python3 tools/verify_links.py --json     # machine-readable, for a scheduled job
  REGISTER=https://example.test python3 tools/verify_links.py --base-url ...

Network egress to amazon.com must be permitted by the environment; if it is not, this
exits with a clear message rather than writing an empty "verified" row.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTER = ROOT / "src" / "data" / "products.json"

# Only these fields may be written back; anything else is an editorial decision.
ALLOWED_UPDATES = ("observed_listing_url", "observed_redirect_asin", "destination_title",
                   "http_status", "retrieved_on", "notes")

UA = "CrispCounterLinkCheck/1.0 (site integrity check; single request per submitted link)"

# Guard: if a fetched title contains one of these, the field is dropped, not stored.
PRICEISH = re.compile(r"\$\s?\d|\bstars?\b|\breviews?\b|in stock|availability", re.I)


def fetch(url: str, timeout: int = 25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(400_000).decode("utf-8", "replace")
            return resp.status, resp.geturl(), body
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:  # noqa: BLE001 - a network failure is a result, not a crash
        return None, url, f"__error__{type(e).__name__}: {e}"


def title_of(html: str):
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a report")
    ap.add_argument("--write", action="store_true",
                    help="update src/data/products.json with observed fields (never with inferences)")
    ap.add_argument("--delay", type=float, default=3.0, help="seconds between requests")
    args = ap.parse_args()

    data = json.loads(REGISTER.read_text(encoding="utf-8"))
    today = time.strftime("%Y-%m-%d")
    rows, blocked = [], 0

    for p in data["products"]:
        link = p["supplied_link"]
        status, final, body = fetch(link)
        if body.startswith("__error__"):
            print(f"NO NETWORK: {body[len('__error__'):]}", file=sys.stderr)
            print("Nothing was written. An unreachable register is not a verified one.", file=sys.stderr)
            return 2
        title = title_of(body)
        if PRICEISH.search(title):
            title = "(title suppressed: contained price or rating wording)"
        asin = None
        m = re.search(r"/dp/([A-Z0-9]{10})", final)
        if m:
            asin = m.group(1)
        reached_product = bool(asin)
        drift = reached_product != bool(p.get("observed_redirect_asin")) or (
            reached_product and asin != p.get("observed_redirect_asin"))
        if not reached_product:
            blocked += 1
        rows.append({
            "id": p["id"],
            "submitted_link": link,
            "http_status": status,
            "final_url": final,
            "observed_redirect_asin": asin,
            "destination_title": title,
            "recorded_asin": p.get("observed_redirect_asin"),
            "drift": drift,
            "retrieved_on": today,
        })
        time.sleep(args.delay)

    if args.write:
        for p in data["products"]:
            r = next(x for x in rows if x["id"] == p["id"])
            p["observed_listing_url"] = r["final_url"] if r["observed_redirect_asin"] else None
            p["observed_redirect_asin"] = r["observed_redirect_asin"]
            p["destination_title"] = r["destination_title"]
            p["http_status"] = r["http_status"]
            p["retrieved_on"] = r["retrieved_on"]
            if r["drift"]:
                p["notes"] = (p.get("notes") or "") + f" Drift observed {today}; re-checked by tools/verify_links.py."
        REGISTER.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"wrote observed fields to {REGISTER.relative_to(ROOT)}")

    if args.json:
        print(json.dumps({"retrieved_on": today, "rows": rows}, indent=2))
    else:
        print(f"Register re-resolution — {today}")
        print(f"{'entry':6} {'status':7} {'observed ASIN':14} {'recorded ASIN':14} drift")
        for r in rows:
            print(f"{r['id']:6} {str(r['http_status']):7} {str(r['observed_redirect_asin']):14} "
                  f"{str(r['recorded_asin']):14} {'YES — update the register' if r['drift'] else 'no'}")
        print(f"\n{len(rows) - blocked}/{len(rows)} reached a product page; {blocked} did not and stay unresolved.")
        print("Not collected, by policy: price, rating, review count, availability, stock, warranty.")
        print("Still required from a human: replace each destination with a Special Link generated in")
        print("Associates Central and confirm one click in the account's own report. This script cannot.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
