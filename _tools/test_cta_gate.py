"""A cart permalink is a buy link, so it is governed by the paid-link gate.

These tests exist because cta.py once appended the Associates tag to a cart URL
built from a redirect observation. That is a link the project invented, which
Program Policies 2(a)-(b) do not permit, and it bypassed buy_url() -- the single
place every other Amazon link goes through.
"""
import json
import pathlib
from unittest import TestCase

import layout
from cta import cart_eligible, pair

ROOT = pathlib.Path(__file__).resolve().parents[1]
PRODUCTS = json.loads((ROOT / "_src/data/products.json").read_text(encoding="utf-8"))["products"]
P01 = next(p for p in PRODUCTS if p["ref"] == "P-01")


class CartGateTest(TestCase):
    def test_no_asin_is_cart_eligible_while_the_register_is_empty(self):
        # The approved register is empty until the account issues a Special Link.
        self.assertEqual(layout.approved_amazon_urls(), {})
        for p in PRODUCTS:
            self.assertFalse(cart_eligible(p["observed_asin"]), p["ref"])

    def test_no_cart_url_is_emitted_without_an_approved_link(self):
        html = pair("", P01)
        self.assertNotIn("cart/add.html", html)
        self.assertNotIn("tag=", html)

    def test_the_permitted_door_is_the_official_listing(self):
        html = pair("", P01)
        self.assertIn(f'https://www.amazon.com/dp/{P01["observed_asin"]}', html)
        self.assertIn('rel="sponsored nofollow noopener"', html)
        self.assertIn('target="_blank"', html)

    def test_the_pair_never_emits_a_naked_span_when_a_link_is_available(self):
        # Regressing to "withheld" while a permitted listing exists would cost the
        # reader the buy path for no compliance gain.
        html = pair("", P01)
        self.assertNotIn("withheld", html)
        self.assertIn("cta-buy", html)
