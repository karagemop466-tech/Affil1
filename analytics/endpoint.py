"""Good Measure Kitchen — self-hosted analytics endpoint.

A minimal, dependency-free HTTP collector for the privacy-preserving client-side
analytics in analytics.js. It accepts POST /analytics/collect and appends the
event batch to analytics/events.jsonl.

Privacy design: no IP addresses, User-Agents, cookies or personal data are
stored. Only the event payload sent by the browser is retained. The endpoint
must be deployed on the operator's own infrastructure (it is not part of the
GitHub Pages static site). Set window.__GMK_ANALYTICS_ENABLED = true on pages
only after the endpoint is live, a privacy notice is published, and any
applicable consent obligations are reviewed.
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STORE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'events.jsonl')
HOST = '127.0.0.1'
PORT = 8765


class Collector(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def _send(self, status, body=b''):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):  # health check
        if self.path == '/healthz':
            self._send(200, b'{"ok":true}')
        else:
            self._send(404, b'{"error":"not found"}')

    def do_POST(self):
        if self.path != '/analytics/collect':
            self._send(404, b'{"error":"not found"}')
            return
        try:
            length = int(self.headers.get('Content-Length') or 0)
            raw = self.rfile.read(length) if length else b''
            payload = json.loads(raw.decode('utf-8')) if raw else {}
        except Exception:
            self._send(400, b'{"error":"invalid json"}')
            return

        events = payload.get('events', [])
        if not isinstance(events, list):
            self._send(400, b'{"error":"events must be a list"}')
            return

        with open(STORE_PATH, 'a', encoding='utf-8') as fh:
            for event in events:
                fh.write(json.dumps(event, ensure_ascii=False) + '\n')

        self._send(200, b'{"accepted":' + str(len(events)).encode() + b'}')

    def log_message(self, fmt, *args):  # silence default request logging
        return


def main():
    server = ThreadingHTTPServer((HOST, PORT), Collector)
    print('analytics endpoint listening on http://%s:%d' % (HOST, PORT))
    server.serve_forever()


if __name__ == '__main__':
    main()