from datetime import date
from unittest import TestCase

from layout import approved_amazon_urls, buy_url, permitted_amazon_urls, product_link
from paid_link_gate import eligible

TAG = 'shopnow047c-20'


class PaidLinkGateTest(TestCase):
    def test_no_account_approved_special_link_exists_yet(self):
        # The approved register is empty until an Associates-generated Special Link
        # with a complete evidence bundle is recorded. Observations never fill it.
        self.assertEqual(approved_amazon_urls(), {})

    def test_observed_listing_is_a_plain_sponsored_reference_link(self):
        asin = 'B0CDY277D3'  # observed on P-01
        url = f'https://www.amazon.com/dp/{asin}'
        self.assertEqual(buy_url(asin), url)
        self.assertIn(url, permitted_amazon_urls())
        html = product_link('', url, 'See it on Amazon')
        self.assertIn('rel="sponsored nofollow noopener"', html)
        self.assertNotIn('tag=', html)

    def test_no_tag_is_synthesised_for_an_observed_listing(self):
        self.assertNotIn(f'https://www.amazon.com/dp/B0CDY277D3?tag={TAG}', permitted_amazon_urls())

    def test_unapproved_tags_and_short_links_are_refused(self):
        asin = 'B0CDY277D3'
        for bad in [f'https://www.amazon.com/dp/{asin}?tag={TAG}',
                    f'https://www.amazon.com/dp/{asin}?tag=someone-else-20',
                    'https://link.amazon/B04G1MEwY']:
            with self.assertRaises(ValueError, msg=bad):
                product_link('', bad, 'Unapproved candidate')

    def test_unobserved_asin_is_refused(self):
        with self.assertRaises(ValueError):
            product_link('', 'https://www.amazon.com/dp/B0000000ZZ', 'Invented')

    def test_requires_exact_approved_link_and_evidence(self):
        tag = TAG
        listing = 'https://www.amazon.com/dp/TEST000001'
        record = dict(intended_asin='TEST000001', official_listing_url=listing,
                      approved_special_link=listing + '?tag=' + tag, tracking_report_reference='SYNTHETIC-NO-REPORT',
                      confirmation_source='https://affiliate-program.amazon.com/home/reports', confirmation_date=date.today().isoformat())
        self.assertTrue(eligible(record, tag))
        for change in [{'tracking_report_reference': None}, {'intended_asin': 'TEST000002'},
                       {'approved_special_link': listing + '?tag=' + tag + '&tag=other'}]:
            self.assertFalse(eligible(record | change, tag))
