import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from wsgiref.validate import validator
from collector import create_app, eligible_products


class TestAggregateCollector(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db = Path(self.tmp.name) / 'test.sqlite'
        self.origin = 'https://example.invalid'
        self.app = validator(create_app(self.db, self.origin, products={'P-TEST'}))

    def send(self, payload, **overrides):
        body = json.dumps(payload).encode()
        env = {'PATH_INFO':'/api/e','SCRIPT_NAME':'','QUERY_STRING':'','REQUEST_METHOD':'POST',
               'CONTENT_TYPE':'application/json','CONTENT_LENGTH':str(len(body)),
               'HTTP_ORIGIN':self.origin,'SERVER_NAME':'example.invalid','SERVER_PORT':'443',
               'SERVER_PROTOCOL':'HTTP/1.1','wsgi.url_scheme':'https','wsgi.version':(1,0),
               'wsgi.input':io.BytesIO(body),'wsgi.errors':io.StringIO(),
               'wsgi.multithread':False,'wsgi.multiprocess':False,'wsgi.run_once':False}
        env.update(overrides)
        status = []
        result = self.app(env, lambda value, headers, exc_info=None: status.append(value))
        try:
            self.assertEqual(list(result), [b''])
        finally:
            result.close()
        return int(status[0].split()[0])

    def totals(self):
        with sqlite3.connect(self.db) as con:
            return dict(con.execute('SELECT event, count FROM totals'))

    def test_five_events_and_aggregation(self):
        cases = [('page_view','index'),('compare_view','compare'),('flag_page_view','flagged'),
                 ('guide_read_75','probe'),('outbound_product_click','compare')]
        for event,page in cases:
            payload = {'event':event,'page':page}
            if event == 'outbound_product_click':
                payload['product'] = 'P-TEST'
            self.assertEqual(self.send(payload), 204)
            self.assertEqual(self.send(payload), 204)
        self.assertEqual(self.totals(), dict.fromkeys((event for event,_ in cases), 2))

    def test_privacy_and_bad_requests(self):
        payload = {'event':'page_view','page':'index'}
        self.assertEqual(self.send(payload, HTTP_DNT='1'), 204)
        self.assertEqual(self.send(payload, HTTP_SEC_GPC='1'), 204)
        self.assertEqual(self.send(payload, HTTP_ORIGIN='https://other.invalid'), 403)
        self.assertEqual(self.send(payload, CONTENT_LENGTH='257'), 413)
        self.assertEqual(self.send(payload, CONTENT_TYPE='text/plain'), 415)
        self.assertEqual(self.send(dict(payload, referrer='ignored')), 422)
        self.assertEqual(self.send(dict(payload, page='index?q=person')), 422)
        self.assertEqual(self.send(dict(payload, page=[])), 422)
        self.assertEqual(self.send({'event':'outbound_product_click','page':'compare','product':'P-01'}), 422)
        self.assertEqual(self.send({'event':'guide_read_75','page':'compare'}), 422)
        self.assertEqual(self.totals(), {})
        self.assertEqual(eligible_products(), set())


if __name__ == '__main__':
    unittest.main()
