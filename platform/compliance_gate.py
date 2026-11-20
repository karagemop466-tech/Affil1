#!/usr/bin/env python3
"""Automated Associates, FTC, and Data-Integrity Compliance Gate for platform/data/*.json."""

from __future__ import annotations

import json
import pathlib
import re
from typing import Any

PLATFORM_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = PLATFORM_DIR / "data"

EXACT_ASSOCIATES_DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
ASIN_RE = re.compile(r"^[A-Z0-9]{10}$")
DOLLAR_PRICE_RE = re.compile(r"\$\s*\d")
FORBIDDEN_LEDGER_KEYS = {"conversion_score", "revenue_forecast", "projected_revenue", "estimated_commission"}


def load_json(name: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def validate_data_layer(data_dir: pathlib.Path = DATA_DIR) -> list[str]:
    """Return a list of compliance or data-integrity errors (empty list = pass)."""
    errors: list[str] = []

    sources_doc = json.loads((data_dir / "sources.json").read_text(encoding="utf-8"))
    products_doc = json.loads((data_dir / "products.json").read_text(encoding="utf-8"))
    flags_doc = json.loads((data_dir / "flags.json").read_text(encoding="utf-8"))
    questions_doc = json.loads((data_dir / "questions.json").read_text(encoding="utf-8"))
    suggestions_doc = json.loads((data_dir / "suggestions.json").read_text(encoding="utf-8"))
    events_doc = json.loads((data_dir / "events.json").read_text(encoding="utf-8"))
    ledger_doc = json.loads((data_dir / "ledger.json").read_text(encoding="utf-8"))
    guides_doc = json.loads((data_dir / "guides.json").read_text(encoding="utf-8"))

    sources_by_id = {s["id"]: s for s in sources_doc.get("sources", [])}
    if len(sources_by_id) < 10:
        errors.append("sources.json must define all official verified sources.")
    for sid, src in sources_by_id.items():
        if not str(src.get("url", "")).startswith("https://"):
            errors.append(f"{sid}: source URL must use https://")

    if products_doc.get("tracking_id_selected") != "shopnow047c-20":
        errors.append("products.json tracking_id_selected must equal 'shopnow047c-20'.")

    products = products_doc.get("products", [])
    if len(products) != 5:
        errors.append(f"Expected 5 submitted products, found {len(products)}.")

    for prod in products:
        pid = prod.get("id", "<unknown>")
        slug = prod.get("submitted_slug", "")
        if len(slug) != prod.get("submitted_slug_length"):
            errors.append(f"{pid}: submitted_slug_length does not match submitted_slug.")

        intent = prod.get("intent_confirmation")
        observed = prod.get("observed_redirect")
        if not isinstance(intent, dict) or not isinstance(observed, dict):
            errors.append(f"{pid}: intent_confirmation and observed_redirect must be separate dicts.")
            continue

        for req_key in ("intended_asin", "official_listing_url", "confirmation_date", "confirmation_source", "validated_special_link_url"):
            if req_key not in intent:
                errors.append(f"{pid}: missing intent_confirmation.{req_key}")

        intended_asin = intent.get("intended_asin")
        observed_asin = observed.get("observed_asin")
        if intended_asin is not None:
            if not ASIN_RE.match(str(intended_asin)):
                errors.append(f"{pid}: intended_asin '{intended_asin}' is not a valid 10-char ASIN.")
            if not intent.get("confirmation_date") or not intent.get("confirmation_source"):
                errors.append(f"{pid}: intended_asin set without confirmation_date and confirmation_source.")

        if intent.get("official_listing_url") and intent.get("official_listing_url") == observed.get("observed_redirect_url") and not intent.get("confirmation_source"):
            errors.append(f"{pid}: official_listing_url merged with observed_redirect_url without operator confirmation.")

        if observed_asin is not None and not ASIN_RE.match(str(observed_asin)):
            errors.append(f"{pid}: observed_asin '{observed_asin}' must be 10 uppercase alphanumeric chars.")

        if observed.get("source_id") not in sources_by_id:
            errors.append(f"{pid}: observed_redirect.source_id missing from sources.json.")

        for u_key, u_val in prod.get("unverified_fields", {}).items():
            if u_val is not None:
                errors.append(f"{pid}: unverified field '{u_key}' must remain null unless API/manual verified.")

    for flg in flags_doc.get("flags", []) + flags_doc.get("repo_audit", []):
        if not flg.get("source_ids") or any(sid not in sources_by_id for sid in flg["source_ids"]):
            errors.append(f"{flg.get('id')}: every flag row must reference valid official source_ids.")

    flg_003 = next((f for f in flags_doc.get("flags", []) if f["id"] == "FLG-003"), None)
    if not flg_003 or "unresolved" not in flg_003.get("finding", "").lower():
        errors.append("FLG-003 must keep link.amazon Special Link status explicitly unresolved.")

    for q in questions_doc.get("questions", []):
        if not q.get("source_ids") or any(sid not in sources_by_id for sid in q["source_ids"]):
            errors.append(f"{q.get('id')}: every question must reference valid official source_ids.")

    for sg in suggestions_doc.get("suggestions", []):
        if not sg.get("source_ids") or any(sid not in sources_by_id for sid in sg["source_ids"]):
            errors.append(f"{sg.get('id')}: every suggestion must reference valid official source_ids.")

    for g in guides_doc.get("guides", []):
        for row in g.get("checklist_rows", []):
            if row.get("source_id") not in sources_by_id:
                errors.append(f"guide {g.get('slug')}: checklist row missing valid source_id.")
        raw_text = json.dumps(g)
        if DOLLAR_PRICE_RE.search(raw_text):
            errors.append(f"guide {g.get('slug')}: contains prohibited dollar figure.")

    event_names = [e["name"] for e in events_doc.get("events", [])]
    expected_events = [
        "page_view",
        "product_card_click",
        "guide_to_product_click",
        "comparison_filter_use",
        "suggestion_decision",
    ]
    if event_names != expected_events:
        errors.append(f"events.json must define exact 5 events {expected_events}, got {event_names}.")

    req_cols = ["timestamp", "source", "channel", "eligible_sessions", "clicks", "reported_orders"]
    if ledger_doc.get("required_columns") != req_cols:
        errors.append("ledger.json required_columns mismatch.")
    for idx, entry in enumerate(ledger_doc.get("entries", [])):
        if set(entry.keys()) & FORBIDDEN_LEDGER_KEYS:
            errors.append(f"ledger entry {idx}: contains forbidden forecast/score key.")
        if not entry.get("provenance_sha256"):
            errors.append(f"ledger entry {idx}: missing provenance_sha256.")

    return errors


if __name__ == "__main__":
    errs = validate_data_layer()
    if errs:
        for e in errs:
            print(f"FAIL: {e}")
        raise SystemExit(1)
    print("platform/compliance_gate.py: all data-layer checks passed (0 errors)")
