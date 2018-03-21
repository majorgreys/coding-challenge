#!/usr/bin/env python

def test_display_cart():
    import cart as c
    
    
    # Create application with databases
    product_database = { 
        1: c.Product(name="Black Jacobins", price_cents=20.00),
        2: c.Product(name="Freedom Is a Constant Struggle", price_cents=15.00)
    } 
    discount_database = { 
        1: c.Discount(code="WELCOME", percentage=50, type="all", product_ids=None), # this discount gives 50% off any product
        2: c.Discount(code="JAC75", percentage=75, type="product_list", product_ids=[1]) # this discount gives a 75% discount off of "Black Jacobins"
    } 
    application = c.Application(products=product_database,
                                        discounts=discount_database)
    # Simple example
    order = c.Order(line_items=[c.LineItem(product_id=1, quantity=1)],
                   discount_code=None)
    expected = """Your cart:

1 copy of "Black Jacobins" for $20.00
---
Total $20.00"""
    assert c.display_cart(application, order) == expected
    
    # Example with a discount
    order = c.Order(
        line_items=[
            c.LineItem(product_id=1, quantity=1),
            c.LineItem(product_id=2, quantity=1)
        ],
        discount_code="WELCOME"
    )
    expected = """Your cart:

$10.00 (Original Price $20.00) for 1 copy of "Black Jacobins"
 $7.50 (Original Price $15.00) for 1 copy of "Freedom Is a Constant Struggle"
---
Total $17.50"""
    assert c.display_cart(application, order) == expected

    # Example with a product_list discount
    order = c.Order(
        line_items=[
            c.LineItem(product_id=1, quantity=1),
            c.LineItem(product_id=2, quantity=1)
        ],
        discount_code="JAC75"
    )
    expected = """Your cart:

 $5.00 (Original Price $20.00) for 1 copy of "Black Jacobins"
$15.00                         for 1 copy of "Freedom Is a Constant Struggle"
---
Total $20.00"""
    assert c.display_cart(application, order) == expected

    # Extra: Example with a product_list discount on multiple quantities
    order = c.Order(
        line_items=[
            c.LineItem(product_id=1, quantity=2),
            c.LineItem(product_id=2, quantity=1)
        ],
        discount_code="JAC75"
    )
    expected = """Your cart:

$10.00 (Original Price $40.00) for 2 copy of "Black Jacobins"
$15.00                         for 1 copy of "Freedom Is a Constant Struggle"
---
Total $25.00"""
    assert c.display_cart(application, order) == expected
