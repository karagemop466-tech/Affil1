#!/usr/bin/env python3
"""Policy-gated editorial research & topic prioritization engine.

Selects candidate buyer-guide topics strictly from authorized Search Console
query exports (Clicks, Impressions, CTR, Average position) and verified catalog
records — never from scraped Amazon prices, star ratings, or BSR lists.
"""

from __future__ import annotations

import csv
import io
import json
import pathlib
from typing import Any

PLATFORM_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = PLATFORM_DIR / "data"


def rank_search_console_queries(csv_text: str, *, min_impressions: int = 20) -> list[dict[str, Any]]:
    """Identify high-impression, low-CTR buyer queries from a Search Console Queries CSV export."""
    reader = csv.DictReader(io.StringIO(csv_text))
    opportunities: list[dict[str, Any]] = []
    for row in reader:
        query = (row.get("Top queries") or row.get("query") or "").strip()
        if not query:
            continue
        impressions = int(float(row.get("Impressions") or row.get("impressions") or 0))
        clicks = int(float(row.get("Clicks") or row.get("clicks") or 0))
        if impressions < min_impressions:
            continue
        ctr = clicks / impressions if impressions else 0.0
        position = float(row.get("Position") or row.get("position") or 0.0)
        opportunities.append(
            {
                "query": query,
                "impressions": impressions,
                "clicks": clicks,
                "measured_ctr": round(ctr, 4),
                "average_position": round(position, 2),
                "opportunity_gap": impressions - clicks,
            }
        )
    opportunities.sort(key=lambda item: (item["opportunity_gap"], item["impressions"]), reverse=True)
    return opportunities


def build_compliant_article_brief(
    topic_question: str,
    product_ids: list[str],
    *,
    data_dir: pathlib.Path = DATA_DIR,
) -> dict[str, Any]:
    """Assemble a human-reviewable editorial brief constrained by Associates & FTC rules."""
    products_doc = json.loads((data_dir / "products.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in products_doc["products"]}
    selected = []
    for pid in product_ids:
        if pid not in by_id:
            raise KeyError(f"Unknown product ID: {pid}")
        p = by_id[pid]
        selected.append(
            {
                "id": p["id"],
                "submitted_url": p["submitted_url"],
                "observed_asin": p["observed_redirect"]["observed_asin"],
                "intended_asin": p["intent_confirmation"]["intended_asin"],
                "listing_title_verbatim": p["observed_redirect"]["listing_title_verbatim"],
                "stated_capacity": p["editorial"]["stated_capacity"],
            }
        )

    return {
        "working_title": topic_question,
        "status": "draft_brief_requires_human_review",
        "tracking_id": products_doc["tracking_id_selected"],
        "selected_products": selected,
        "hard_policy_constraints": [
            "Include verbatim 'As an Amazon Associate I earn from qualifying purchases.' above <main> and in <footer> (S01).",
            "Mark every outbound product link rel='sponsored nofollow noopener' with visible 'Paid link' microcopy (S04, S06).",
            "Do not state prices, star ratings, customer review counts, stock availability, or price-tracking claims without Creators API / PA API (S02 §2(b), §6(t), §6(y)).",
            "Do not merge intended_asin with observed_asin; state capabilities strictly as seller-title claims unless physically tested (S03, S05).",
        ],
    }
