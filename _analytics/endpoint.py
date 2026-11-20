"""Opt-in first-party daily counters. Run behind a same-origin HTTPS proxy."""
import json
import os
import sqlite3
import sys
from contextlib import closing
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# The generator directories were underscore-prefixed on 2026-11-20 so that legacy
# Pages (which serves this branch root) stops publishing them. This line still
# said 'tools', so the module did not import at all — and CI only ever ran
# py_compile over this file, which checks syntax and never executes an import.
# `python3 -m unittest test_endpoint` was failing for that reason alone.
sys.path.insert(0, str(ROOT / '_tools'))
from build import GENERATED

DATA = ROOT / '_src/data'
EVENTS = {e['name'] for e in json.loads((DATA / 'events.json').read_text())['events']}
PRODUCTS = {p['observed_asin'] for p in json.loads((DATA / 'products.json').read_text())['products']} - {None}
PAGES = {p.removesuffix('index.html') for p in GENERATED if p.endswith('.html')}


def valid(item):
    if not isinstance(item, dict) or set(item) != {'event', 'page', 'product'}:
        return False
    event, page, product = (item[k] for k in ('event', 'page', 'product'))
    if not isinstance(event, str) or event not in EVENTS or not isinstance(page, str) or page not in PAGES:
        return False
    if event == 'outbound_product_click':
        return isinstance(product, str) and product in PRODUCTS
    return product is None and (
        event == 'page_view' or
        event == 'guide_read_75' and page.startswith('guides/') and page.endswith('.html') or
        event == 'compare_view' and page == 'compare/' or
        event == 'flag_page_view' and page == 'review/'
    )


class Collector(BaseHTTPRequestHandler):
    def setup(self):
        self.request.settimeout(5)
        super().setup()

    def reply(self, status):
        self.send_response(status)
        self.send_header('Content-Length', '0')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()

    def do_GET(self):
        self.reply(204 if self.path == '/healthz' else 404)

    def do_POST(self):
        if self.path != '/api/e':
            return self.reply(404)
        if self.headers.get('Origin') != self.server.site_origin:
            return self.reply(403)
        if self.headers.get('DNT') == '1' or self.headers.get('Sec-GPC') == '1':
            return self.reply(204)
        if self.headers.get_content_type() != 'application/json':
            return self.reply(415)
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 4096:
                return self.reply(413)
            events = json.loads(self.rfile.read(size))
        except (ValueError, OSError, RecursionError):
            return self.reply(400)
        if not isinstance(events, list) or not 1 <= len(events) <= 10 or not all(map(valid, events)):
            return self.reply(400)
        day = datetime.now(timezone.utc).date().isoformat()
        try:
            with closing(sqlite3.connect(self.server.database)) as db, db:
                db.execute('''CREATE TABLE IF NOT EXISTS counts (
                    day TEXT, event TEXT, page TEXT, product TEXT, total INTEGER,
                    PRIMARY KEY (day, event, page, product))''')
                db.executemany('''INSERT INTO counts VALUES (?, ?, ?, ?, 1)
                    ON CONFLICT(day, event, page, product) DO UPDATE SET total = total + 1''',
                    [(day, e['event'], e['page'], e['product'] or '') for e in events])
        except sqlite3.Error:
            return self.reply(503)
        self.reply(204)

    def log_message(self, *_):
        pass


def main():
    with ThreadingHTTPServer(('127.0.0.1', int(os.environ.get('ANALYTICS_PORT', '8765'))), Collector) as server:
        server.site_origin = os.environ['ANALYTICS_ORIGIN']
        server.database = os.environ['ANALYTICS_DATABASE']
        server.serve_forever()


if __name__ == '__main__':
    main()
