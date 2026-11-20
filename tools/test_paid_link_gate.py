from datetime import date
from unittest import TestCase

from layout import approved_amazon_urls, buy_url, product_link
from paid_link_gate import eligible


class PaidLinkGateTest(TestCase):
    def test_public_observations_do_not_create_tags(self):
        self.assertEqual(approved_amazon_urls(), {})
        asin = 'B0CDY277D3'
        url = f'https://www.amazon.com/dp/{asin}'
        self.assertEqual(buy_url(asin), url)
        self.assertIn('rel="sponsored nofollow noopener"', product_link('', url, 'Listing source'))
        with self.assertRaises(ValueError):
            product_link('', url + '?tag=shopnow047c-20', 'Unapproved candidate')

    def test_requires_exact_approved_link_and_evidence(self):
        tag = 'shopnow047c-20'
        listing = 'https://www.amazon.com/dp/TEST000001'
        record = dict(intended_asin='TEST000001', official_listing_url=listing,
                      approved_special_link=listing + '?tag=' + tag, tracking_report_reference='SYNTHETIC-NO-REPORT',
                      confirmation_source='https://affiliate-program.amazon.com/home/reports', confirmation_date=date.today().isoformat())
        self.assertTrue(eligible(record, tag))
        for change in [{'tracking_report_reference': None}, {'intended_asin': 'TEST000002'},
                       {'approved_special_link': listing + '?tag=' + tag + '&tag=other'}]:
            self.assertFalse(eligible(record | change, tag))
