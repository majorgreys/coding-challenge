#!/usr/bin/env python

from collections import namedtuple

# Application data model
LineItem = namedtuple('LineItem', ['product_id', 'quantity'])
Order = namedtuple('Order', ['line_items', 'discount_code'])
Discount = namedtuple('Discount', ['code', 'percentage', 'type', 'product_ids'])
Product = namedtuple('Product', ['name', 'price_cents'])
Application = namedtuple('CartApplication', ['products', 'discounts'])

# Internal class for cart calculations
ItemPrice = namedtuple('ItemPrice', ['lineitem', 'product', 'price'])

def get_product(application, product_id):
    """ Return the Product instance for a product id. """
    return application.products[product_id]

def get_discount(application, discount_code):
    """ Return the Discount instance for a code. """
    if discount_code:
        discount = [
            d 
            for d in application.discounts.values() 
            if d.code == discount_code
        ]
        return discount[0]

def format_price_dollars_cents(price):
    """ Format a price as dollars with 2 decimals. """
    return "${:.2f}".format(price)

def format_originalprice(itemprice):
    """ Format the original price if discount applied. """
    originalprice = itemprice.product.price_cents * itemprice.lineitem.quantity
    if originalprice != itemprice.price:
        return "(Original Price ${:.2f})".format(originalprice)
    else:
        return ""
  
def format_itemprice(itemprice, discount_code):
    """ Format the display of an ItemPrice. """
    if not discount_code:
        return "{} copy of \"{}\" for ${:.2f}".format(
            itemprice.lineitem.quantity, 
            itemprice.product.name,
            itemprice.price
        )
    else:
        # We use right aligned format strings for price and original price to get formatting done right
        return "{:>6} {:>23} for {} copy of \"{}\"".format(
            format_price_dollars_cents(itemprice.price),
            format_originalprice(itemprice),
            itemprice.lineitem.quantity, 
            itemprice.product.name
        )
    
def apply_product_discount(lineitem, discount, price):
    """ Apply the discount for a product if applicable. """
    if lineitem.product_id in discount.product_ids:
        return price * (1.0 - (discount.percentage / 100))
    else:
        return price
    
def apply_discount(discount, itemprices):
    """ Apply discount for all applicable products. """
    if discount and discount.type == 'all':
        # TODO: Currently handled separately from product-specific discounts but the two could be consolidated  
        return [
            ItemPrice(lineitem=p.lineitem,
                      product=p.product,
                      price=p.price * (1.0 - (discount.percentage / 100)))
            for p in itemprices
        ]
    elif discount and discount.type == 'product_list':
        return [
            ItemPrice(lineitem=p.lineitem,
                      product=p.product,
                      price=apply_product_discount(p.lineitem, discount, p.price))
            for p in itemprices
        ]
    else:
        # No discounts applied
        return itemprices

def display_cart(application, order):
    """ Process items in an order and output formatted string of cart. """
    itemprices = [
        ItemPrice(lineitem=lineitem,
                  product=get_product(application, lineitem.product_id),
                  price=get_product(application, lineitem.product_id).price_cents * lineitem.quantity)
        for lineitem in order.line_items
        if lineitem.product_id in application.products
    ]
    discount = get_discount(application, order.discount_code)
    itemprices = apply_discount(discount, itemprices)
    display_prices = [format_itemprice(i, order.discount_code) for i in itemprices]
    total_price = sum([x.price for x in itemprices])
    return """Your cart:

{}
---
Total ${:.2f}""".format(
    '\n'.join(display_prices),
    total_price
)
