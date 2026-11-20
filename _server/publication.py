"""Serve the staged publication and an opt-out, aggregate-only first-party counter."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit
import datetime, json, os, sqlite3

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'dist'
PAGES = {p.relative_to(PUBLIC).as_posix() for p in PUBLIC.rglob('*.html')}
PRODUCTS = json.loads((ROOT/'_src/data/products.json').read_text())['products']
EVENTS = {e['name'] for e in json.loads((ROOT/'_src/data/events.json').read_text())['events']}
ASINS = {p['observed_asin'] for p in PRODUCTS}
STORE = os.environ.get('COUNTER_DB', '/tmp/crisp-counter.sqlite3')

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs): super().__init__(*args, directory=PUBLIC, **kwargs)
    def log_message(self, *args): pass
    def list_directory(self, path): return self.send_error(404)
    def do_GET(self):
        if self.path == '/assets/js/counter-config.js':
            self.send_response(200); self.send_header('Content-Type','text/javascript'); self.end_headers(); self.wfile.write(b'window.CC_COUNTER=true;'); return
        super().do_GET()
    def do_POST(self):
        if self.path != '/api/e': return self.send_error(404)
        if self.headers.get('DNT')=='1' or self.headers.get('Sec-GPC')=='1': return self.send_error(403)
        if urlsplit(self.headers.get('Origin','')).netloc != self.headers.get('Host'): return self.send_error(403)
        try:
            size = int(self.headers.get('Content-Length','0'))
            if not 0 < size <= 512: raise ValueError()
            event,page,asin = json.loads(self.rfile.read(size))
            if event not in EVENTS or page not in PAGES or (asin != '' and (event != 'outbound_product_click' or asin not in ASINS)): raise ValueError()
        except (ValueError,TypeError): return self.send_error(400)
        with sqlite3.connect(STORE) as db:
            db.execute('CREATE TABLE IF NOT EXISTS totals(day TEXT,event TEXT,page TEXT,asin TEXT,n INTEGER,PRIMARY KEY(day,event,page,asin))')
            db.execute("DELETE FROM totals WHERE day < date('now','-89 days')")
            db.execute("INSERT INTO totals VALUES(date('now'),?,?,?,1) ON CONFLICT DO UPDATE SET n=n+1",(event,page,asin))
        self.send_response(204); self.end_headers()

if __name__ == '__main__':
    if not PAGES: raise SystemExit('Stage the site with _tools/stage.py first')
    ThreadingHTTPServer(('0.0.0.0',int(os.getenv('PORT','8000'))),Handler).serve_forever()
