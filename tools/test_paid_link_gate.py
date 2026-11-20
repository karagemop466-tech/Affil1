"""The paid-link gate: public observation never creates a tag.

This file could not run from the repository root until now. It imported
``layout`` by bare name, which only resolves when the current directory is
``tools/``; run as ``python3 -m unittest tools.test_paid_link_gate`` it failed at
import with ModuleNotFoundError, so the one test that proves the gate works was
never executed by anyone following the README. The path insert below fixes the
harness, not the rule.
"""
import sys
from datetime import date
from pathlib import Path
from unittest import TestCase

sys.path.insert(0, str(Path(__file__).resolve().parent))

from layout import approved_amazon_urls, buy_url, product_link  # noqa: E402
from paid_link_gate import eligible  # noqa: E402


class PaidLinkGateTest(TestCase):
    def test_public_observations_do_not_create_tags(self):
        # A tagged destination is allowed (Program Policies 2(b) requires it) but
        # it is not evidence: no intent record exists, so nothing may be called
        # account-confirmed.
        from paid_link_gate import approved_links
        import json
        products = json.loads((Path(__file__).resolve().parents[1] / 'src/data/products.json').read_text())['products']
        self.assertEqual(approved_links(products, 'shopnow047c-20'), {})
        asin = products[0]['observed_asin']
        self.assertTrue(buy_url(asin).endswith('?tag=shopnow047c-20'))
        url = f'https://www.amazon.com/dp/{asin}'
        self.assertIn('rel="sponsored nofollow noopener"', product_link('', buy_url(asin), 'Listing source'))
        with self.assertRaises(ValueError):
            product_link('', url + '?tag=someone-else-20', 'Unapproved candidate')

    def test_requires_exact_approved_link_and_evidence(self):
        tag = 'shopnow047c-20'
        listing = 'https://www.amazon.com/dp/TEST000001'
        record = dict(intended_asin='TEST000001', official_listing_url=listing,
                      approved_special_link=listing + '?tag=' + tag, tracking_report_reference='SYNTHETIC-NO-REPORT',
                      confirmation_source='https://affiliate-program.amazon.com/home/reports', confirmation_date=date.today().isoformat())
        self.assertTrue(eligible(record, tag))
        for change in [{'tracking_report_reference': None}, {'intended_asin': 'TEST000002'},
                       {'approved_special_link': listing + '?tag=' + tag + '&tag=other'},
                       {'confirmation_source': 'https://example.com/reports'},
                       {'confirmation_date': '2999-01-01'}]:
            self.assertFalse(eligible(record | change, tag))
