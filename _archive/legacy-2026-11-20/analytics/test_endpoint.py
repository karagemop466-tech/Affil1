import http.client
import json
import sqlite3
import tempfile
import threading
import unittest
from contextlib import closing
from pathlib import Path

from endpoint import Collector, EVENTS, PRODUCTS, ThreadingHTTPServer


class CollectorTest(unittest.TestCase):
    def test_daily_aggregation_and_rejection(self):
        with tempfile.TemporaryDirectory() as directory, ThreadingHTTPServer(('127.0.0.1', 0), Collector) as server:
            server.site_origin = 'https://publication.example'
            server.database = Path(directory) / 'counts.sqlite'
            worker = threading.Thread(target=server.serve_forever)
            worker.start()
            try:
                def send(items, **overrides):
                    headers = {'Content-Type': 'application/json', 'Origin': server.site_origin}
                    headers.update(overrides)
                    with closing(http.client.HTTPConnection(*server.server_address)) as client:
                        client.request('POST', '/api/e', json.dumps(items), headers)
                        return client.getresponse().status

                items = [dict(event=event, page=page, product=product) for event, page, product in [
                    ('page_view', '', None), ('compare_view', 'compare/', None),
                    ('flag_page_view', 'review/', None),
                    ('guide_read_75', 'guides/basket-or-oven-air-fryer.html', None),
                    ('outbound_product_click', '', sorted(PRODUCTS)[0]),
                ]]
                self.assertEqual({e['event'] for e in items}, EVENTS)
                self.assertEqual(send(items, Origin='https://other.example'), 403)
                self.assertEqual(send(items, **{'Sec-GPC': '1'}), 204)
                self.assertEqual(send(items, DNT='1'), 204)
                self.assertFalse(server.database.exists())
                self.assertEqual(send(items + [dict(items[0], page='?email=example')]), 400)
                self.assertEqual(send(items + [dict(items[0], email='example')]), 400)
                self.assertEqual(send(items + [dict(items[0], page=[])]), 400)
                self.assertEqual(send(['a' * 5000]), 413)
                self.assertEqual(send(items), 204)
                self.assertEqual(send(items), 204)
                with closing(sqlite3.connect(server.database)) as db:
                    self.assertEqual(dict(db.execute('SELECT event,total FROM counts')), dict.fromkeys(EVENTS, 2))
            finally:
                server.shutdown()
                worker.join()
