#!/usr/bin/env python3
"""Self-hosted, privacy-preserving event collector for Crisp & Counter.

This is the counterpart to assets/js/analytics.js. It is deliberately small and
deliberately boring, because a collector that stores nothing personal cannot
leak anything personal.

What arrives:  {"events":[{"event":"page_view","path":"/guides/x.html",
                           "ref":null,"date":"2026-11-20"}]}
What is kept:  an integer count per (date, event, path, ref).
What is not kept, and never written to disk: the client IP address, the user
agent, the referer header, cookies, or any request body field not listed as an
allowed property. The IP is discarded at the socket level by reading no
forwarding header and writing nothing about the connection.

Run it with:

    python3 analytics/collect.py --data analytics/data.ndjson --port 8787

and set the page's endpoint with one line in tools/layout.py:

    window.CC_ANALYTICS_ENDPOINT = "https://your-host.example/api/e"

Retention: raw events are never stored, only aggregate counters, so there is
nothing to expire. Delete the data file and the counters are gone; that is the
whole retention policy.
"""

import argparse
import collections
import datetime
import json
import pathlib
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ALLOWED_EVENTS = {
    "page_view",
    "outbound_product_click",
    "guide_read_75",
    "compare_view",
    "flag_page_view",
}

PATH_RE = re.compile(r"^/[A-Za-z0-9._~\-/]{0,200}$")
ASIN_RE = re.compile(r"^B0[0-9A-Z]{8}$")

lock = threading.Lock()
counts = collections.Counter()


def _clean(event):
    """Return a normalised event, or None if anything about it is unexpected.

    Rejecting is the default. A field that is not on this list is a field the
    site never intended to send, and accepting it would quietly widen the
    privacy claim on the measurement page.
    """
    if not isinstance(event, dict):
        return None
    name = event.get("event")
    path = event.get("path")
    ref = event.get("ref")
    date = event.get("date")
    if name not in ALLOWED_EVENTS:
        return None
    if not isinstance(path, str) or not PATH_RE.match(path) or "?" in path:
        return None
    if ref is not None and (not isinstance(ref, str) or not ASIN_RE.match(ref)):
        return None
    try:
        day = datetime.date.fromisoformat(date).isoformat()
    except (TypeError, ValueError):
        return None
    return (day, name, path, ref or "")


def record(events, destination):
    clean = [c for c in (_clean(e) for e in events) if c]
    if not clean:
        return 0
    with lock:
        counts.update(clean)
        if destination:
            with open(destination, "a", encoding="utf-8") as fh:
                for day, name, path, ref in clean:
                    fh.write(json.dumps({
                        "date": day, "event": name, "path": path, "ref": ref,
                    }, sort_keys=True) + "\n")
    return len(clean)


def summary():
    """Aggregate only: no path is ever joined to a person, because no person
    is representable in this structure."""
    with lock:
        rows = [
            {"date": d, "event": e, "path": p, "ref": r or None, "count": n}
            for (d, e, p, r), n in sorted(counts.items())
        ]
    return rows


class Handler(BaseHTTPRequestHandler):
    data_path = None
    max_body = 16 * 1024

    def log_message(self, fmt, *args):
        # The default logger writes the client address. Do not.
        return

    def _send(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(204, {})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return self._send(400, {"error": "bad length"})
        if length <= 0 or length > self.max_body:
            return self._send(413, {"error": "body too large or empty"})
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return self._send(400, {"error": "bad json"})
        events = payload.get("events") if isinstance(payload, dict) else None
        if not isinstance(events, list) or len(events) > 50:
            return self._send(400, {"error": "bad events"})
        accepted = record(events, self.data_path)
        return self._send(202, {"accepted": accepted})

    def do_GET(self):
        if self.path.split("?")[0] not in ("/api/summary", "/summary"):
            return self._send(404, {"error": "not found"})
        return self._send(200, {"counts": summary()})


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="analytics/data.ndjson",
                    help="aggregate event log (one JSON object per line)")
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--host", default="0.0.0.0")
    opts = ap.parse_args()
    path = pathlib.Path(opts.data)
    path.parent.mkdir(parents=True, exist_ok=True)
    Handler.data_path = str(path)
    server = ThreadingHTTPServer((opts.host, opts.port), Handler)
    print(f"collector listening on http://{opts.host}:{opts.port}  -> {path}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped; counters held in memory are discarded")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
