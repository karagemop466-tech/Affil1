"""The buy-now layer: one decision, two doors, and a price note that cannot lie.

Every other page on this site asks the reader to open a product page. That is the
right door for a reader who is still deciding and the wrong door for one who has
decided. This module adds the second door — a cart permalink — without touching
the tag mechanism that the paid-link gate governs.

Rules enforced here, not just documented in prose:

  * a cart link is only emitted for an ASIN that was observed in this session's
    register, so a typo cannot ship a link to a different product;
  * the tag is always present, because Program Policies 2(b) requires the
    Associates ID as a URL parameter;
  * price is never guessed. Where a price was seen on a listing it is rendered as
    a dated observation and labelled as such, because the site is not permitted to
    present an Amazon price as its own current data.
"""

import json
import pathlib

from layout import buy_url, esc, link, rel

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _load():
    return json.loads((ROOT / "_src/data/links.json").read_text(encoding="utf-8"))


def cart_url(asin, doc=None):
    """The cart permalink for one ASIN. Raises on an ASIN not in the register."""
    doc = doc or _load()
    for row in doc["links"]:
        if row["asin"] == asin:
            return doc["cta"]["cart_endpoint"] + row["cart_path"]
    raise ValueError(f"no cart permalink registered for {asin!r}")


def detail_url(asin):
    """The detail-page door, built by the same gate as every other Amazon link.

    buy_url returns the account-approved Special Link when the register holds one,
    and the plain listing otherwise. It never synthesises a tag, which is why this
    function no longer builds a URL by hand.
    """
    return buy_url(asin)


def pair(page_dir, product, *, cls="cta-pair", sub=True):
    """The two doors, side by side. Cart first, because the reader came to shop."""
    asin = product["observed_asin"]
    cart = cart_url(asin)
    detail = detail_url(asin)
    cart_line = "Add to basket" if not sub else (
        'Add to basket <span class="cta-sub">Opens your Amazon cart</span>')
    detail_line = "Read the buyer note" if not sub else (
        'Read the buyer note <span class="cta-sub">Sizes and trade-offs</span>')
    cart_a = (
        f'<a class="cta cta-buy" href="{esc(cart)}" rel="sponsored nofollow noopener"'
        f' target="_blank" data-affiliate-ref="{esc(asin)}" data-cta="cart"'
        f' aria-label="Add the {esc(product["brand"])} {esc(product["format_label"])}'
        f' to your Amazon cart (paid link, opens in a new tab)">{cart_line}</a>'
    )
    detail_a = link(page_dir, f'products/{product["ref"].lower()}.html',
                    detail_line, cls="cta cta-note", aria=(
                        f'Read the note on the {product["brand"]} {product["format_label"]}'))
    return f'<div class="{esc(cls)}">{cart_a}{detail_a}</div>'


def price_note(price, observed_on, where):
    """A dated, attributed price observation — never a live price claim."""
    return (
        '<p class="price-note"><span class="price-note-k">Price seen</span>'
        f' <strong>{esc(price)}</strong> on {esc(observed_on)}, on the Amazon listing'
        f' for {esc(where)}. It is a dated observation, not a live price:'
        ' Amazon shows the current one when you open the link.</p>'
    )


def badge(text, kind="ok"):
    return f'<span class="pill pill-{esc(kind)}">{esc(text)}</span>'
