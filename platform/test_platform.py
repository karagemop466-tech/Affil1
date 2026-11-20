#!/usr/bin/env python3
"""Automated unit & integration tests for platform/ and edition/."""

from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

PLATFORM_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(PLATFORM_DIR))

from build_edition import build_all  # noqa: E402
from collector import AggregateCounterStore, make_handler  # noqa: E402
from compliance_gate import validate_data_layer  # noqa: E402
from ledger import append_verified_entry, import_associates_csv  # noqa: E402
from research_engine import build_compliant_article_brief, rank_search_console_queries  # noqa: E402
from verify_edition import verify_edition  # noqa: E402


class PlatformComplianceTests(unittest.TestCase):
    def test_data_layer_passes(self) -> None:
        self.assertEqual(validate_data_layer(), [])

    def test_edition_build_and_verify(self) -> None:
        pages = build_all()
        self.assertGreaterEqual(len(pages), 22)
        errors, checks = verify_edition()
        self.assertEqual(errors, [])
        self.assertGreater(checks, 250)


class CollectorEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.store = AggregateCounterStore(pathlib.Path(self.tmp.name) / "counts.json")
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.store))
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def _post(self, body: dict, headers: dict[str, str] | None = None) -> int:
        raw = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/collect",
            data=raw,
            method="POST",
            headers={"Content-Type": "application/json", **(headers or {})},
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status
        except urllib.error.HTTPError as exc:
            return exc.code

    def test_records_all_five_defined_events_and_rejects_unknown(self) -> None:
        self.assertEqual(self._post({"event": "page_view", "page": "home"}), 202)
        self.assertEqual(self._post({"event": "product_card_click", "page": "home", "product_id": "P-01"}), 202)
        self.assertEqual(
            self._post(
                {
                    "event": "guide_to_product_click",
                    "page": "guides/basket-or-oven-air-fryer",
                    "guide_slug": "basket-or-oven-air-fryer",
                    "product_id": "P-02",
                }
            ),
            202,
        )
        self.assertEqual(self._post({"event": "comparison_filter_use", "page": "compare", "filter_key": "air-fryers"}), 202)
        self.assertEqual(
            self._post({"event": "suggestion_decision", "page": "suggestions", "suggestion_id": "SG-01", "decision": "approved"}),
            202,
        )
        self.assertEqual(len(self.store.snapshot()), 5)

        # Reject unknown event or extra PII fields
        self.assertEqual(self._post({"event": "scroll_depth", "page": "home"}), 400)
        self.assertEqual(self._post({"event": "page_view", "page": "home", "ip": "1.2.3.4"}), 400)

    def test_honors_dnt_and_gpc_and_origin_allowlist(self) -> None:
        self.assertEqual(self._post({"event": "page_view", "page": "home"}, {"DNT": "1"}), 204)
        self.assertEqual(self._post({"event": "page_view", "page": "home"}, {"Sec-GPC": "1"}), 204)
        self.assertEqual(self.store.snapshot(), {})
        self.assertEqual(
            self._post({"event": "page_view", "page": "home"}, {"Origin": "https://evil.example.com"}),
            403,
        )


class CampaignLedgerTests(unittest.TestCase):
    def test_imports_valid_csv_with_sha256_and_rejects_forecasts(self) -> None:
        csv_raw = b"eligible_sessions,clicks,reported_orders\n120,34,2\n80,16,1\n"
        entry = import_associates_csv(
            csv_raw,
            channel="organic_search",
            report_filename="associates-2026-11.csv",
            imported_on="2026-11-20T05:00:00Z",
        )
        self.assertEqual(entry["eligible_sessions"], 200)
        self.assertEqual(entry["clicks"], 50)
        self.assertEqual(entry["reported_orders"], 3)
        self.assertEqual(len(entry["provenance_sha256"]), 64)

        with tempfile.TemporaryDirectory() as tmp:
            ledger_file = pathlib.Path(tmp) / "ledger.json"
            ledger_file.write_text(json.dumps({"entries": [], "provenance_trail": []}), encoding="utf-8")
            append_verified_entry(ledger_file, entry)
            saved = json.loads(ledger_file.read_text(encoding="utf-8"))
            self.assertEqual(len(saved["entries"]), 1)

        bad_csv = b"clicks,reported_orders,revenue_forecast\n10,1,99.99\n"
        with self.assertRaises(ValueError):
            import_associates_csv(bad_csv, channel="organic", report_filename="bad.csv")


class ResearchEngineTests(unittest.TestCase):
    def test_ranks_search_console_queries_and_generates_brief(self) -> None:
        sample_csv = "Top queries,Clicks,Impressions,CTR,Position\ndual basket vs single air fryer,3,140,2.14%,8.4\nholiday side dish toaster oven,1,85,1.17%,11.2\n"
        ranked = rank_search_console_queries(sample_csv, min_impressions=20)
        self.assertEqual(ranked[0]["query"], "dual basket vs single air fryer")
        brief = build_compliant_article_brief("Which air fryer fits two sides?", ["P-01", "P-03"])
        self.assertEqual(brief["tracking_id"], "shopnow047c-20")
        self.assertEqual(len(brief["selected_products"]), 2)


if __name__ == "__main__":
    unittest.main()
