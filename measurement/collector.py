#!/usr/bin/env python3
"""First-party WSGI endpoint. Only UTC day and bounded aggregate counts persist."""
from contextlib import closing
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import sqlite3

PAGES = {'index', 'compare', 'guides', 'probe', 'flagged', 'desk', 'suggestions'}
EVENT_PAGES = {'page_view': PAGES, 'compare_view': {'compare'},
               'flag_page_view': {'flagged'}, 'guide_read_75': {'probe'},
               'outbound_product_click': {'compare', 'probe'}}
RECORDS = Path(__file__).resolve().parent.parent / 'kitchen' / 'records.json'


def eligible_products():
    """Only operator-approved links, never bare observations, can be counted."""
    return {row['id'] for row in json.loads(RECORDS.read_text())['products']
            if all(row.get(k) for k in ('special_link', 'intended_asin', 'official_listing_url',
                                        'confirmation_date', 'confirmation_source', 'tracking_report_ref'))}


def create_app(database, origin, products=None):
    products = frozenset(eligible_products() if products is None else products)
    with closing(sqlite3.connect(database)) as conn, conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS totals (
            day TEXT NOT NULL, event TEXT NOT NULL, page TEXT NOT NULL, product TEXT NOT NULL,
            count INTEGER NOT NULL, PRIMARY KEY (day, event, page, product))''')

    def app(env, start_response):
        def done(status):
            headers = [('Cache-Control', 'no-store')]
            if not status.startswith('204'):
                headers += [('Content-Type', 'text/plain; charset=utf-8'), ('Content-Length', '0')]
            start_response(status, headers)
            return [b'']

        if env.get('PATH_INFO') != '/api/e':
            return done('404 Not Found')
        if env.get('REQUEST_METHOD') != 'POST':
            return done('405 Method Not Allowed')
        if env.get('HTTP_ORIGIN') != origin or env.get('QUERY_STRING'):
            return done('403 Forbidden')
        if env.get('HTTP_SEC_GPC') == '1' or env.get('HTTP_DNT') == '1':
            return done('204 No Content')
        if env.get('CONTENT_TYPE', '').split(';')[0].strip().lower() != 'application/json':
            return done('415 Unsupported Media Type')
        try:
            length = int(env.get('CONTENT_LENGTH') or '0')
        except ValueError:
            return done('400 Bad Request')
        if not 0 < length <= 256:
            return done('413 Content Too Large')
        try:
            data = json.loads(env['wsgi.input'].read(length))
        except (UnicodeDecodeError, ValueError, RecursionError):
            return done('400 Bad Request')
        if not isinstance(data, dict) or not all(isinstance(value, str) for value in data.values()):
            return done('422 Unprocessable Entity')
        event, page = data.get('event'), data.get('page')
        if page not in EVENT_PAGES.get(event, ()):
            return done('422 Unprocessable Entity')
        click = event == 'outbound_product_click'
        if data.keys() != ({'event', 'page', 'product'} if click else {'event', 'page'}):
            return done('422 Unprocessable Entity')
        product = data.get('product', '')
        if click and product not in products:
            return done('422 Unprocessable Entity')
        now = datetime.now(timezone.utc).date()
        try:
            with closing(sqlite3.connect(database)) as conn, conn:
                conn.execute('''INSERT INTO totals VALUES (?, ?, ?, ?, 1)
                    ON CONFLICT(day, event, page, product) DO UPDATE SET count = count + 1''',
                    (now.isoformat(), event, page, product))
                conn.execute('DELETE FROM totals WHERE day < ?', ((now - timedelta(days=89)).isoformat(),))
        except sqlite3.Error:
            return done('503 Service Unavailable')
        return done('204 No Content')
    return app


def configured_app():
    return create_app(os.environ['MEASURE_DB'], os.environ['MEASURE_ORIGIN'])
