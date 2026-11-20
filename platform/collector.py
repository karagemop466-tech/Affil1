#!/usr/bin/env python3
"""Self-hosted privacy-preserving 5-event analytics endpoint (zero cookies, zero IP storage)."""

from __future__ import annotations

import datetime as dt
import json
import pathlib
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

ALLOWED_EVENTS: dict[str, set[str]] = {
    "page_view": {"page"},
    "product_card_click": {"page", "product_id"},
    "guide_to_product_click": {"page", "guide_slug", "product_id"},
    "comparison_filter_use": {"page", "filter_key"},
    "suggestion_decision": {"page", "suggestion_id", "decision"},
}

SAFE_TOKEN_RE = re.compile(r"^[A-Za-z0-9_./:-]{1,80}$")


class AggregateCounterStore:
    """Thread-safe aggregate daily counter store with zero PII."""

    def __init__(self, storage_path: pathlib.Path | None = None) -> None:
        self._lock = threading.Lock()
        self.storage_path = storage_path
        self.counts: dict[str, int] = {}
        if storage_path and storage_path.is_file():
            self.counts = json.loads(storage_path.read_text(encoding="utf-8"))

    def validate_and_record(self, payload: dict[str, Any], *, today: str | None = None) -> tuple[bool, str]:
        if not isinstance(payload, dict):
            return False, "Payload must be a JSON object."
        event = payload.get("event")
        if event not in ALLOWED_EVENTS:
            return False, f"Unknown event: {event!r}"
        expected_keys = ALLOWED_EVENTS[event] | {"event"}
        extra_keys = set(payload.keys()) - expected_keys
        if extra_keys:
            return False, f"Disallowed fields: {sorted(extra_keys)}"
        missing_keys = expected_keys - set(payload.keys())
        if missing_keys:
            return False, f"Missing required fields: {sorted(missing_keys)}"

        parts = [today or dt.date.today().isoformat(), str(event)]
        for k in sorted(ALLOWED_EVENTS[event]):
            val = str(payload[k])
            if not SAFE_TOKEN_RE.match(val):
                return False, f"Invalid token format for {k}"
            parts.append(f"{k}={val}")

        bucket = "|".join(parts)
        with self._lock:
            self.counts[bucket] = self.counts.get(bucket, 0) + 1
            if self.storage_path:
                self.storage_path.parent.mkdir(parents=True, exist_ok=True)
                self.storage_path.write_text(json.dumps(self.counts, indent=2, sort_keys=True), encoding="utf-8")
        return True, bucket

    def snapshot(self) -> dict[str, int]:
        with self._lock:
            return dict(self.counts)


def make_handler(store: AggregateCounterStore, allowed_origins: set[str] | None = None):
    origins = allowed_origins or {"https://karagemop466-tech.github.io", "http://127.0.0.1", "http://localhost"}

    def origin_ok(origin: str | None) -> bool:
        if not origin:
            return True
        return any(origin == allowed or origin.startswith(allowed + ":") for allowed in origins)

    class CollectorHandler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            # Suppress default BaseHTTPRequestHandler client-IP logging for visitor privacy.
            return

        def _send_json(self, code: int, body: dict[str, Any], origin: str | None = None) -> None:
            raw = json.dumps(body).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            if origin and origin_ok(origin):
                self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_OPTIONS(self) -> None:  # noqa: N802
            origin = self.headers.get("Origin")
            if not origin_ok(origin):
                self._send_json(403, {"error": "origin_not_allowed"})
                return
            self.send_response(204)
            if origin:
                self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, DNT, Sec-GPC")
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/healthz":
                self._send_json(200, {"status": "ok", "events_supported": sorted(ALLOWED_EVENTS)})
                return
            if self.path == "/summary":
                self._send_json(200, {"counts": store.snapshot()})
                return
            self._send_json(404, {"error": "not_found"})

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/collect":
                self._send_json(404, {"error": "not_found"})
                return
            origin = self.headers.get("Origin")
            if not origin_ok(origin):
                self._send_json(403, {"error": "origin_not_allowed"})
                return
            if self.headers.get("DNT") == "1" or self.headers.get("Sec-GPC") == "1":
                self.send_response(204)
                self.end_headers()
                return
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 2048:
                self._send_json(400, {"error": "invalid_body_length"}, origin)
                return
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
            except json.JSONDecodeError:
                self._send_json(400, {"error": "invalid_json"}, origin)
                return
            ok, detail = store.validate_and_record(payload)
            if not ok:
                self._send_json(400, {"error": detail}, origin)
                return
            self._send_json(202, {"accepted": True, "bucket": detail}, origin)

    return CollectorHandler


def serve(host: str = "127.0.0.1", port: int = 8787, storage: str = "/tmp/countertop-events.json") -> None:
    store = AggregateCounterStore(pathlib.Path(storage))
    httpd = ThreadingHTTPServer((host, port), make_handler(store))
    print(f"Privacy-first 5-event collector listening on http://{host}:{port}/collect")
    httpd.serve_forever()


if __name__ == "__main__":
    serve()
