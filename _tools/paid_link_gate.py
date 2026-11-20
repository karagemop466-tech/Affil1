"""Publish only exact, account-confirmed Special Links; never synthesize them."""
from datetime import date
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlsplit

INTENT = Path(__file__).resolve().parents[1] / '_src/data/product-intent.json'
FIELDS = ('intended_asin', 'official_listing_url', 'confirmation_date', 'confirmation_source',
          'approved_special_link', 'tracking_report_reference')


def eligible(record, tag):
    if not all(isinstance(record.get(k), str) and record[k].strip() for k in FIELDS):
        return False
    asin = record['intended_asin']
    try:
        day = date.fromisoformat(record['confirmation_date'])
        source = urlsplit(record['confirmation_source'])
        url = urlsplit(record['approved_special_link'])
    except ValueError:
        return False
    return bool(re.fullmatch(r'[A-Z0-9]{10}', asin)
                and day.isoformat() == record['confirmation_date'] and day <= date.today()
                and source.scheme == 'https' and source.netloc == 'affiliate-program.amazon.com'
                and source.path.strip('/') and not source.query and not source.fragment
                and record['official_listing_url'] == f'https://www.amazon.com/dp/{asin}'
                and (url.scheme, url.netloc, url.path) == ('https', 'www.amazon.com', f'/dp/{asin}')
                and parse_qs(url.query, keep_blank_values=True).get('tag') == [tag] and not url.fragment
                and re.fullmatch(r'[A-Za-z0-9._-]{1,80}', record['tracking_report_reference']))


def approved_links(products, tag):
    data = json.loads(INTENT.read_text())
    if data['tracking_id_supplied'] != tag:
        raise ValueError('The intent register must use the selected tracking ID')
    by_id = {p['ref']: p for p in products}
    seen = set()
    approved = {}
    for record in data['records']:
        ref = record['ref']
        if ref in seen or ref not in by_id or record['submitted_link'] != by_id[ref]['submitted_link']:
            raise ValueError(f'{ref}: intent record does not correspond to the supplied link')
        seen.add(ref)
        if not record.get('approved_special_link'):
            continue
        if not eligible(record, tag) or record['intended_asin'] != by_id[ref].get('observed_asin'):
            raise ValueError(f'{ref}: proposed affiliate link is missing evidence or does not match the item shown')
        approved[record['intended_asin']] = record['approved_special_link']
    if seen != by_id.keys():
        raise ValueError('The intent register is missing product references')
    return approved
