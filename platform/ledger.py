#!/usr/bin/env python3
"""Provenance-gated Campaign Ledger importer for authorized first-party Associates reports."""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import pathlib
from typing import Any

AUTHORIZED_SOURCES = {
    "amazon_associates_central_csv",
    "self_hosted_first_party_collector",
}
REQUIRED_COLUMNS = (
    "timestamp",
    "source",
    "channel",
    "eligible_sessions",
    "clicks",
    "reported_orders",
)
FORBIDDEN_FIELDS = {
    "conversion_score",
    "revenue_forecast",
    "projected_revenue",
    "estimated_orders",
    "synthetic_score",
}


def sha256_hex(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def import_associates_csv(
    csv_bytes: bytes,
    *,
    channel: str,
    report_filename: str,
    imported_on: str | None = None,
) -> dict[str, Any]:
    """Parse an authorized first-party Associates CSV export into one provenance-stamped ledger row.

    Never fabricates conversion scores or revenue forecasts.
    """
    text = csv_bytes.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    fieldnames = set(reader.fieldnames or [])
    if fieldnames & FORBIDDEN_FIELDS:
        raise ValueError(f"Rejected CSV containing forbidden forecast/score columns: {sorted(fieldnames & FORBIDDEN_FIELDS)}")
    if not {"clicks", "reported_orders"}.issubset(fieldnames):
        raise ValueError("Authorized CSV must include explicit 'clicks' and 'reported_orders' columns.")

    total_sessions = 0
    has_sessions = "eligible_sessions" in fieldnames
    total_clicks = 0
    total_orders = 0
    row_count = 0

    for row in reader:
        row_count += 1
        total_clicks += int(row["clicks"])
        total_orders += int(row["reported_orders"])
        if has_sessions and row.get("eligible_sessions", "") != "":
            total_sessions += int(row["eligible_sessions"])

    if row_count == 0:
        raise ValueError("Authorized CSV contained zero data rows.")

    stamp = imported_on or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    digest = sha256_hex(csv_bytes)

    return {
        "timestamp": stamp,
        "source": "amazon_associates_central_csv",
        "channel": channel,
        "eligible_sessions": total_sessions if has_sessions else None,
        "clicks": total_clicks,
        "reported_orders": total_orders,
        "report_filename": report_filename,
        "provenance_sha256": digest,
    }


def append_verified_entry(ledger_path: pathlib.Path, entry: dict[str, Any]) -> None:
    if set(entry.keys()) & FORBIDDEN_FIELDS:
        raise ValueError("Forbidden forecast or conversion-score field rejected.")
    if entry.get("source") not in AUTHORIZED_SOURCES:
        raise ValueError(f"Unauthorized ledger source: {entry.get('source')!r}")
    if not entry.get("provenance_sha256"):
        raise ValueError("Ledger entry requires provenance_sha256 of the raw first-party export.")
    for col in REQUIRED_COLUMNS:
        if col not in entry:
            raise ValueError(f"Missing required column: {col}")

    doc = json.loads(ledger_path.read_text(encoding="utf-8"))
    doc.setdefault("entries", []).append(entry)
    doc.setdefault("provenance_trail", []).append(
        {
            "date": entry["timestamp"][:10],
            "action": f"Imported {entry['source']} ({entry.get('report_filename', 'first-party-report')})",
            "actor": "operator-verified-import",
            "authorized_report_attached": True,
            "provenance_sha256": entry["provenance_sha256"],
            "source_id": "S14",
        }
    )
    ledger_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
