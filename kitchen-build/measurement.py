"""Optional first-party host for the generated edition. Not used by GitHub Pages."""
import argparse
import csv
from contextlib import closing
from datetime import date, datetime, timedelta, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import sqlite3
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build import GENERATED, readiness

READINESS_PAGE = "/Affil1/operations/launch-readiness.html"

BROWSER = {e['name'] for e in json.loads((ROOT/'src/data/events.json').read_text())['events'] if e.get('scope') != 'operator'}
PAGES = {'/Affil1/' + p for p in GENERATED if p.endswith('.html') and p != '404.html'}
PAGES.add(READINESS_PAGE)
PAGES |= {p.removesuffix('index.html') for p in PAGES if p.endswith('/index.html')}
MAX_BYTES = 4096


def today():
    return datetime.now(timezone.utc).date()


def open_db(path):
    db = sqlite3.connect(path)
    db.executescript('''
      CREATE TABLE IF NOT EXISTS counts (
        day TEXT, event TEXT, page TEXT, ref TEXT, count INTEGER NOT NULL,
        PRIMARY KEY(day,event,page,ref));
      CREATE TABLE IF NOT EXISTS reports (
        imported_at TEXT, source TEXT, source_reference TEXT, window_start TEXT, window_end TEXT,
        channel TEXT, eligible_sessions INTEGER, clicks INTEGER, reported_orders INTEGER,
        UNIQUE(source,source_reference,window_start,window_end,channel));''')
    return db


def increment(db, day, event, page='', ref=''):
    db.execute('''INSERT INTO counts VALUES (?, ?, ?, ?, 1)
                  ON CONFLICT(day,event,page,ref) DO UPDATE SET count=count+1''', (str(day), event, page, ref))


def prune(db, retention_days):
    db.execute('DELETE FROM counts WHERE day < ?', (str(today() - timedelta(days=retention_days-1)),))


def record(db, item, retention_days):
    if not isinstance(item, dict) or set(item) != {'event', 'path', 'ref'}:
        raise ValueError('unexpected payload')
    name, page, ref = (item[k] for k in ('event', 'path', 'ref'))
    if not isinstance(name, str) or name not in BROWSER or not isinstance(page, str) or page not in PAGES:
        raise ValueError('unexpected event or page')
    if name == 'guide_read_75' and not (page.startswith('/Affil1/guides/') and not page.endswith('/index.html') and page.endswith('.html')):
        raise ValueError('unexpected guide path')
    if name == 'compare_view' and page not in ('/Affil1/compare/', '/Affil1/compare/index.html'):
        raise ValueError('unexpected comparison path')
    if name == 'flag_page_view' and page not in ('/Affil1/review/', '/Affil1/review/index.html'):
        raise ValueError('unexpected review path')
    if name == 'outbound_product_click':
        if not isinstance(ref, str) or not re.fullmatch(r'[A-Z0-9]{10}', ref):
            raise ValueError('invalid product reference')
    elif ref is not None:
        raise ValueError('unexpected product reference')
    with db:
        prune(db, retention_days)
        canonical = page.removesuffix('index.html') if page.endswith('/index.html') else page
        increment(db, today(), name, canonical, ref or '')


REPORT_FIELDS = ('source_reference', 'window_start', 'window_end', 'channel', 'eligible_sessions', 'clicks', 'reported_orders')


def import_report(db, path):
    """Operator-attested, normalized aggregate CSV; no reader-level export accepted."""
    accepted = []
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != REPORT_FIELDS:
            raise ValueError('incorrect report columns')
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise ValueError('incomplete row')
            start, end = [date.fromisoformat(row[key]) for key in ('window_start', 'window_end')]
            if not start <= end <= today():
                raise ValueError('invalid date window')
            reference = row['source_reference']
            if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,79}', reference):
                raise ValueError('use an internal non-sensitive report reference')
            if row['channel'] not in ('all', 'organic', 'direct', 'referral', 'email'):
                raise ValueError('invalid channel')
            counts = [None if row[k] == '' else int(row[k]) for k in REPORT_FIELDS[4:]]
            if counts == [None]*3 or any(n is not None and not 0 <= n <= 2**31-1 for n in counts):
                raise ValueError('invalid counts')
            accepted.append((reference, str(start), str(end), row['channel'], *counts))
    if not accepted:
        raise ValueError('empty report')
    with db:
        db.executemany('INSERT INTO reports VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       [(datetime.now(timezone.utc).isoformat(), 'Amazon Associates', *r) for r in accepted])
        increment(db, today(), 'report_import')


class Handler(SimpleHTTPRequestHandler):
    analytics_enabled = False

    def log_message(self, *args):
        pass  # Do not write IPs, request URLs or headers to application logs.

    def respond(self, status):
        self.send_response(status)
        self.send_header('Cache-Control', 'no-store')
        if status == 405:
            self.send_header('Allow', 'POST')
        self.send_header('Content-Length', '0')
        self.end_headers()

    def do_POST(self):
        if self.path != '/api/e' or not self.analytics_enabled:
            return self.respond(404)
        if (self.headers.get('Origin') != self.origin
            or self.headers.get('Sec-Fetch-Site') not in (None, 'same-origin')
            or self.headers.get('Sec-GPC') == '1' or self.headers.get('DNT') == '1'):
            return self.respond(403)
        try:
            length = int(self.headers.get('Content-Length', '-1'))
        except ValueError:
            length = -1
        if not 0 < length <= MAX_BYTES or self.headers.get('Transfer-Encoding'):
            return self.respond(413)
        if self.headers.get_content_type() != 'application/json':
            return self.respond(415)
        try:
            values = json.loads(self.rfile.read(length))
            if not isinstance(values, list) or len(values) != 1:
                raise ValueError('expected one event')
            value = values[0]
            if not isinstance(value, dict) or set(value) != {'event','page','product'} or not isinstance(value['page'], str):
                raise ValueError('invalid event')
            with closing(self.db()) as db:
                record(db, {'event': value['event'], 'path': '/Affil1/' + value['page'],
                            'ref': value['product']}, self.retention_days)
        except (ValueError, RecursionError):
            return self.respond(400)
        self.respond(204)

    def do_GET(self):
        return self.serve_public()

    def do_HEAD(self):
        return self.serve_public(head=True)

    def serve_public(self, head=False):
        path = urlsplit(self.path).path
        if path in ('/', '/Affil1'):
            self.send_response(302)
            self.send_header('Location', '/Affil1/')
            self.end_headers()
            return
        if path == '/api/e':
            return self.respond(405 if self.analytics_enabled else 404)
        if path == '/Affil1/assets/js/analytics.js' and self.analytics_enabled:
            data = b'window.CC_ANALYTICS_ENABLED = true;\n' + (ROOT / 'assets/js/analytics.js').read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'text/javascript; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            if not head:
                self.wfile.write(data)
            return
        allowed = (path in PAGES or path in {'/Affil1/sitemap.xml', '/Affil1/feed.xml', '/Affil1/robots.txt',
                   '/Affil1/reviews/verification-audit.html', '/Affil1/guides/holiday-hosting.html'}
                   or bool(re.fullmatch(r'/Affil1/assets/(img|js|css|fonts)/[A-Za-z0-9._-]+\.(jpg|svg|js|css|woff2)', path)))
        if not allowed or not (ROOT / path.removeprefix('/Affil1/')).exists():
            return self.respond(404)
        self.path = path.removeprefix('/Affil1')
        return super().do_HEAD() if head else super().do_GET()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(required=True, dest='command')
    serve = commands.add_parser('serve')
    serve.add_argument('--port', type=int, default=8080)
    serve.add_argument('--origin')
    serve.add_argument('--retention-days', type=int, default=30, choices=range(1, 91), metavar='1-90')
    serve.add_argument('--database', type=Path)
    for command in ('counts', 'prune', 'import-report'):
        p = commands.add_parser(command)
        p.add_argument('--database', type=Path, required=True)
        if command == 'prune':
            p.add_argument('--retention-days', type=int, required=True, choices=range(1, 91), metavar='1-90')
        if command == 'import-report':
            p.add_argument('file', type=Path)
            p.add_argument('--authorized', action='store_true', required=True,
                           help='attest that the source is an authorized first-party Associates report')
    args = parser.parse_args()
    if args.database and args.database.resolve().is_relative_to(ROOT):
        parser.error('database must be outside the checkout and web root')
    if args.command == 'serve':
        if bool(args.origin) != bool(args.database):
            parser.error('enable measurement only with both --origin and --database')
        if args.origin:
            u = urlsplit(args.origin)
            if (u.scheme not in ('https', 'http') or not u.hostname or u.path or u.fragment or u.query or u.username
                or (u.scheme == 'http' and u.hostname not in ('localhost', '127.0.0.1'))):
                parser.error('use an HTTPS origin (HTTP allowed only for development on localhost) without a path')
        class Configured(Handler):
            analytics_enabled = bool(args.origin)
            origin = args.origin
            retention_days = args.retention_days

            def setup(self):
                self.request.settimeout(8)
                super().setup()

            def __init__(self, *a, **kw):
                super().__init__(*a, directory=str(ROOT), **kw)

            def db(self):
                return open_db(args.database)
        if args.database:
            with closing(open_db(args.database)):
                pass
        with ThreadingHTTPServer(('0.0.0.0', args.port), Configured) as server:
            server.serve_forever()
    else:
        with closing(open_db(args.database)) as db, db:
            if args.command == 'import-report':
                import_report(db, args.file)
            elif args.command == 'prune':
                prune(db, args.retention_days)
            else:
                db.row_factory = sqlite3.Row
                print(json.dumps([dict(r) for r in db.execute('SELECT * FROM counts ORDER BY day,event,page,ref')], indent=2))


if __name__ == '__main__':
    main()
