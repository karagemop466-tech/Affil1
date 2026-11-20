#!/usr/bin/env python3
"""verify_links.py — repeatable observation runbook for the submitted product links.

Part of the Affil1 verification layer (session arena/a4ab7faf-affil1, 2026-11-20).

What this tool does (and deliberately does not do):
  * Fetches each submitted short link, follows redirects, and records the final
    URL, HTTP status and document <title> as one observation.
  * Appends observations to an append-only NDJSON log. It NEVER edits
    data/confirmations.json, data/product-intent.json or any other register.
    Observations are evidence; confirmation of submitter intent may only come
    from the enrolled Amazon Associates workflow (a tracking report or an
    explicit submitter statement). See reviews/verification-audit.html.

Usage:
    python3 tools/verify_links.py                  # observe all registered links
    python3 tools/verify_links.py --out PATH       # NDJSON output path (default
                                                   # data/verification-observations.ndjson)
    python3 tools/verify_links.py --url https://... [--url https://...]
    python3 tools/verify_links.py --timeout 25
    python3 tools/verify_links.py --stability      # also compare vs the last
                                                   # observation of each link

Exit codes: 0 = all fetches completed (any outcome, including fetch_error),
            1 = unexpected internal error, 2 = usage error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

SUBMITTED_LINKS = [
    "https://link.amazon/B04G1MEwY",
    "https://link.amazon/B02NbDxp3",
    "https://link.amazon/B00hJ57DV",
    "https://link.amazon/B0c8moW59",
    "https://link.amazon/B0f3GKalj",
]

DEFAULT_OUT = Path("data/verification-observations.ndjson")
USER_AGENT = ("Affil1-verification-runbook/1.0 (observation-only; not a crawler; "
              "records are evidence, not confirmations)")
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
MAX_REDIRECTS = 10


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def clean_title(html: str) -> str | None:
    m = TITLE_RE.search(html)
    if not m:
        return None
    title = re.sub(r"\s+", " ", m.group(1)).strip()
    return title or None


def observe(url: str, timeout: float) -> dict:
    """Fetch one URL, following redirects. Returns an observation record."""
    rec: dict = {
        "observed_at_utc": now_iso(),
        "submitted_link": url,
        "tool": "tools/verify_links.py 1.0",
        "outcome": None,
        "http_status": None,
        "final_url": None,
        "redirect_chain": [],
        "page_title": None,
        "fetch_error": None,
        "note": "Observation only. Not a confirmation of submitter intent. "
                "Status of submitted links remains unresolved (FLG-003).",
    }
    chain: list[str] = []
    req = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310
            body = resp.read(262144).decode("utf-8", "replace")
            rec["http_status"] = resp.status
            rec["final_url"] = resp.geturl()
            chain = [r.geturl() for r in resp.history] if hasattr(resp, "history") else []
            rec["page_title"] = clean_title(body)
            final = rec["final_url"] or ""
            if "/checkpoint/" in final:
                rec["outcome"] = "checkpoint_gate"
            elif re.search(r"/(?:dp|gp/product)/([A-Z0-9]{10})(?:[/?]|$)", final):
                rec["outcome"] = "product_page"
                rec["observed_dp_code"] = re.search(
                    r"/(?:dp|gp/product)/([A-Z0-9]{10})(?:[/?]|$)", final
                ).group(1)
            else:
                rec["outcome"] = "non_product_page"
    except urllib.error.HTTPError as e:
        rec["outcome"] = "http_error"
        rec["http_status"] = e.code
        rec["fetch_error"] = f"HTTPError: {e.code} {e.reason}"
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
        rec["outcome"] = "fetch_error"
        rec["fetch_error"] = f"{type(e).__name__}: {e}"
    rec["redirect_chain"] = chain
    return rec


def last_observation(path: Path, link: str) -> dict | None:
    if not path.exists():
        return None
    found = None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            print(f"  ! skipping malformed NDJSON line in {path}", file=sys.stderr)
            continue
        if rec.get("submitted_link") == link:
            found = rec
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--url", action="append", default=[],
                    help="observe this URL instead of the registered list (repeatable)")
    ap.add_argument("--out", default=str(DEFAULT_OUT),
                    help=f"NDJSON output path (default {DEFAULT_OUT})")
    ap.add_argument("--timeout", type=float, default=20.0,
                    help="per-request timeout in seconds (default 20)")
    ap.add_argument("--stability", action="store_true",
                    help="compare each result with the last observation of the same link")
    args = ap.parse_args()

    links = args.url or SUBMITTED_LINKS
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Observation run — {now_iso()} — {len(links)} link(s) -> {out_path}")
    print("Reminder: an observation is evidence, not a confirmation. Only the\n"
          "enrolled Associates workflow (tracking report / submitter statement)\n"
          "may set intended ASINs or change a register's status fields.\n")

    for link in links:
        rec = observe(link, args.timeout)
        outcome = rec["outcome"]
        detail = rec.get("observed_dp_code") or rec.get("fetch_error") or ""
        print(f"  {link}\n    -> {outcome} {detail} "
              f"(status={rec['http_status']}, title={bool(rec['page_title'])})")
        if args.stability:
            prev = last_observation(out_path, link)
            if prev:
                same = prev.get("outcome") == outcome and (
                    prev.get("observed_dp_code") == rec.get("observed_dp_code")
                )
                print(f"    stability: {'SAME as last observation' if same else 'CHANGED vs last observation ' + str(prev.get('observed_at_utc'))}")
            else:
                print("    stability: no prior observation recorded")
        with out_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"\nAppended {len(links)} observation(s) to {out_path}. "
          "The log is append-only; no register was modified.")
    print("Next human step: test one link per product in the enrolled Associates\n"
          "workflow and record destination + tracking-report evidence separately.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
