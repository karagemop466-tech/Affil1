import json
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.error import HTTPError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen
from html.parser import HTMLParser

import measurement as m
import readiness as r


class LaunchChecks(unittest.TestCase):
    def test_empty_confirmation_and_subpath_links(self):
        doc = json.loads(r.INTENT.read_text())
        r.validate(doc)
        self.assertTrue(all(not r.eligible(p, doc['tracking_id_supplied']) for p in doc['records']))
        self.assertEqual(r.render(doc), r.OUTPUT.read_text())
        self.assertEqual(r.render(doc).count(r.DISCLOSURE), 2)
        discovered = []
        class Links(HTMLParser):
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                for key in ('href', 'src'):
                    if key in attrs:
                        discovered.append((attrs[key], attrs.get('rel','')))
        Links().feed(r.OUTPUT.read_text())
        for value, rel in discovered:
            if value.startswith('https://www.amazon.com/dp/'):
                self.assertIn('sponsored', rel.split())
                self.assertFalse(urlsplit(value).query)
            if value.startswith(('#', 'https:')):
                continue
            self.assertFalse(value.startswith('/'))
            url = urljoin('/Affil1/operations/launch-readiness.html', value)
            target = r.ROOT / urlsplit(url).path.removeprefix('/Affil1/')
            self.assertTrue(target.exists(), url)

    def test_confirmation_can_match_observation_but_requires_independent_fields(self):
        doc = json.loads(r.INTENT.read_text())
        p, tag = doc['records'][0], doc['tracking_id_supplied']
        p.update(intended_asin='B0CDY277D3', official_listing_url=p['observed_redirect_target'],
                 confirmation_date=str(m.today()), confirmation_source='https://affiliate-program.amazon.com/help',
                 approved_special_link=p['observed_redirect_target']+'?tag='+tag,
                 tracking_report_reference='private-report-ref')
        self.assertTrue(r.eligible(p, tag))
        p['approved_special_link'] += '&tag=wrong-20'
        self.assertFalse(r.eligible(p, tag))
        p['approved_special_link'] = p['observed_redirect_target']+'?tag='+tag
        p['tracking_report_reference'] = None
        self.assertFalse(r.eligible(p, tag))
        with self.assertRaises(ValueError):
            r.validate(doc)

    def test_http_collection_and_authorized_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / 'private.sqlite'
            with socket.socket() as sock:
                sock.bind(('127.0.0.1', 0))
                port = sock.getsockname()[1]
            origin = f'http://127.0.0.1:{port}'
            cmd = [sys.executable, m.__file__, 'serve', '--port', str(port), '--origin', origin, '--database', str(db_path)]
            with subprocess.Popen(cmd) as proc:
                try:
                    for _ in range(100):
                        try:
                            with urlopen(origin + '/Affil1/operations/launch-readiness.html', timeout=0.5) as res:
                                self.assertEqual(res.status, 200)
                            break
                        except OSError:
                            time.sleep(0.03)
                    else:
                        self.fail('local test server did not start')
                    def post(payload, **overrides):
                        if not isinstance(payload, bytes):
                            item = dict(payload)
                            item['page'] = item.pop('path').removeprefix('/Affil1/')
                            item['product'] = item.pop('ref')
                            payload = json.dumps([item]).encode()
                        headers = {'Origin': origin, 'Content-Type': 'application/json', **overrides}
                        req = Request(origin+'/api/e', data=payload, headers=headers)
                        try:
                            with urlopen(req) as res:
                                return res.status
                        except HTTPError as e:
                            with e:
                                return e.code
                    page = {'event':'page_view','path':'/Affil1/index.html','ref':None}
                    self.assertEqual(post(page), 204)
                    self.assertEqual(post(dict(page, path='/Affil1/')), 204)
                    self.assertEqual(post(dict(page, event='compare_view', path='/Affil1/compare/')), 204)
                    self.assertEqual(post(dict(page, event='guide_read_75', path='/Affil1/guides/basket-or-oven-air-fryer.html')), 204)
                    self.assertEqual(post(dict(page, event='outbound_product_click', ref='B0CDY277D3')), 204)
                    self.assertEqual(post(dict(page, event='flag_page_view', path='/Affil1/review/')), 204)
                    self.assertEqual(post(dict(page, event='report_import')), 400)
                    self.assertEqual(post(dict(page, path='/Affil1/?key=private')), 400)
                    self.assertEqual(post(dict(page, extra='pii')), 400)
                    self.assertEqual(post(page, Origin='https://example.org'), 403)
                    self.assertEqual(post(page, **{'Sec-GPC':'1'}), 403)
                    self.assertEqual(post(b'x' * 4097), 413)
                    for hidden in ('/Affil1/kitchen-build/intent.json', '/Affil1/.git/config', '/Affil1/assets/js/%2e%2e/'):
                        with self.assertRaises(HTTPError) as e:
                            urlopen(origin+hidden)
                        self.assertEqual(e.exception.code, 404)
                    with urlopen(origin+'/Affil1/assets/js/analytics.js') as res:
                        self.assertIn(b'/api/e', res.read())
                finally:
                    proc.terminate()
                    proc.wait(timeout=5)
            report = Path(tmp) / 'report.csv'
            report.write_text(','.join(m.REPORT_FIELDS)+'\nunit-test,2026-01-01,2026-01-02,all,,1,0\n')
            command = [sys.executable, m.__file__, 'import-report', '--database', str(db_path), str(report)]
            self.assertNotEqual(subprocess.run(command,capture_output=True).returncode, 0)
            subprocess.run(command + ['--authorized'], check=True)
            self.assertNotEqual(subprocess.run(command + ['--authorized'],capture_output=True).returncode, 0)
            with sqlite3.connect(db_path) as db:
                self.assertEqual(dict(db.execute('SELECT event,count FROM counts')),
                                 dict(page_view=2,outbound_product_click=1,guide_read_75=1,compare_view=1,flag_page_view=1,report_import=1))
                self.assertEqual(db.execute('SELECT eligible_sessions,clicks,reported_orders FROM reports').fetchall(), [(None,1,0)])
                db.execute("INSERT INTO counts VALUES ('2001-01-01','page_view','/Affil1/','',1)")
                m.prune(db, 7)
                self.assertEqual(db.execute("SELECT count(*) FROM counts WHERE day='2001-01-01'").fetchone(), (0,))


if __name__ == '__main__':
    unittest.main()
