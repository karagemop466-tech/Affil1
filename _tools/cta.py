"""The buy-now layer: one decision, two doors, and a price note that cannot lie.

Every other page on this site asks the reader to open a product page. That is the
right door for a reader who is still deciding and the wrong door for one who has
decided. This module adds the second door — a cart permalink — without touching
the tag mechanism that the paid-link gate governs.

Rules enforced here, not just documented in prose:

  * a cart link is only emitted for an ASIN that was observed in this session's
    register, so a typo cannot ship a link to a different product;
  * a cart link is emitted only when the paid-link gate holds an account-approved
    Special Link for that ASIN. A cart permalink is an outbound Amazon URL a
    reader can buy through, so it is subject to Program Policies 2(a)-(b) exactly
    like a product link: it must be the account's own link, carrying the tag.
    Until the account issues one, the pair degrades to the single detail-page
    door and says "Basket link withheld" instead of shipping an unattributable
    buy path. (Prior behaviour appended a tag to a URL built from an observed
    redirect, which the gate exists to prevent -- see /decisions/ D-01.)
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


def cart_eligible(asin, doc=None):
    """True only when the paid-link gate has approved this ASIN.

    A cart permalink is an outbound Amazon URL a reader can buy through, so it is
    governed by the same rule as every other link on the site: it may be published
    only for an ASIN whose account-approved Special Link the register holds. A cart
    URL built from an *observed* redirect carries no attribution and would be
    indistinguishable from a link this project invented, which Program Policies
    2(a)-(b) do not permit. Until the account issues the Special Link, the
    add-to-basket door is withheld and only the detail-page door is rendered.
    """
    from layout import approved_amazon_urls
    return asin in approved_amazon_urls()


def pair(page_dir, product, *, cls="cta-pair", sub=True):
    """The buy doors, rendered from what the gate actually permits.

    Three states, in order of preference:

      1. Cart door permitted (account-approved Special Link exists) -- the reader
         came to shop, so "Add to basket" leads and the buyer note follows.
      2. No approved link: the primary door becomes the official listing for the
         observed ASIN, which the gate does permit as a plain reference link. It
         is still marked sponsored, because it is a paid link in the FTC/Google
         sense. A one-line note explains why there is no one-click basket.
      3. Never a cart URL built from an observed redirect: that would be a link
         this project invented, carrying a tag the account did not issue.
    """
    asin = product["observed_asin"]
    cart = cart_url(asin) if cart_eligible(asin) else None
    detail_href = rel(page_dir, f'products/{product["ref"].lower()}.html')
    detail_line = "Read the buyer note" if not sub else (
        'Read the buyer note <span class="cta-sub">Sizes and trade-offs</span>')
    detail_a = link(page_dir, f'products/{product["ref"].lower()}.html',
                    detail_line, cls="cta cta-note", aria=(
                        f'Read the note on the {product["brand"]} {product["format_label"]}'))

    if cart:
        cart_line = "Add to basket" if not sub else (
            'Add to basket <span class="cta-sub">Opens your Amazon cart</span>')
        buy_a = (
            f'<a class="cta cta-buy" href="{esc(cart)}" rel="sponsored nofollow noopener"'
            f' target="_blank" data-affiliate-ref="{esc(asin)}" data-cta="cart"'
            f' aria-label="Add the {esc(product["brand"])} {esc(product["format_label"])}'
            f' to your Amazon cart (paid link, opens in a new tab)">{cart_line}</a>'
        )
        return f'<div class="{esc(cls)}">{buy_a}{detail_a}</div>'

    # State 2: the permitted door. buy_url() returns the account-approved Special
    # Link when one exists and the plain official listing otherwise; it never
    # synthesises a tag. This is the same gate every other link on the site uses.
    listing = buy_url(asin)
    view_line = "View it on Amazon" if not sub else (
        'View it on Amazon <span class="cta-sub">Live price and stock</span>')
    buy_a = (
        f'<a class="cta cta-buy" href="{esc(listing)}" rel="sponsored nofollow noopener"'
        f' target="_blank" data-affiliate-ref="{esc(asin)}" data-cta="listing"'
        f' aria-label="Open the Amazon listing for the {esc(product["brand"])} '
        f'{esc(product["format_label"])} (paid link, opens in a new tab)">{view_line}</a>'
    )
    note = ('' if not sub else
            '<p class="cta-note-line">One-click basket needs a link the Associates '
            'account has confirmed. Until then this goes to the listing.</p>')
    return f'<div class="{esc(cls)}">{buy_a}{detail_a}</div>{note}'



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
