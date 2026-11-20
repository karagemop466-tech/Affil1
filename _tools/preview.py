#!/usr/bin/env python3
"""Serve the exact staged publication. Optional local-only analytics smoke preview."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

from stage import stage

ROOT = Path(__file__).resolve().parents[1]
# 'analytics' became '_analytics' when the working trees were moved under an underscore
# so Pages could not serve them; this path was left behind, which made the documented
# --measurement-demo command die on import. Corrected 2026-11-20 (arena/769ee00d-affil1)
sys.path.insert(0, str(ROOT / '_analytics'))
from endpoint import Collector  # noqa: E402


class Preview(Collector, SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/healthz':
            return Collector.do_GET(self)
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if not self.server.site_origin:
            return self.reply(404)
        return Collector.do_POST(self)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=4173)
    parser.add_argument('--measurement-demo', action='store_true', help='bind only to loopback; discard all demo counts on exit')
    args = parser.parse_args()
    with TemporaryDirectory(prefix='crisp-preview-') as tmp:
        site = Path(tmp) / 'site'
        stage(site)
        if args.measurement_demo:
            for page in site.rglob('*.html'):
                text = page.read_text().replace('</head>', '<script>window.CC_ANALYTICS_ENABLED = true;</script>\n</head>')
                text = text.replace('<main id="main">', '<main id="main"><p class="wrap">Local demo only: aggregate counts are stored until this process exits.</p>')
                page.write_text(text)
        host = '127.0.0.1' if args.measurement_demo else '0.0.0.0'
        handler = partial(Preview, directory=site)
        with ThreadingHTTPServer((host, args.port), handler) as server:
            server.site_origin = f'http://127.0.0.1:{args.port}' if args.measurement_demo else None
            server.database = str(Path(tmp) / 'demo.sqlite')
            print(f'Publication preview on port {args.port}', flush=True)
            server.serve_forever()


if __name__ == '__main__':
    main()
