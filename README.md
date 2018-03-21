# Coding Exercise

The solution provided here for the
[Discounts](https://github.com/positiondev/website/blob/master/exercises/discounts.md)
coding exercise includes two sources files, [cart.py](cart.py) and
[test_cart.py](test_cart.py), and a [Pipfile](Pipfile) to be used with `pipenv`.

To run the tests:

```
$ pipenv install --dev
$ pipenv run pytest
```

I defined the data model using `namedtuple` subclasses. The cart application is
treated as an instance of `cart.Application` namedtuple with fields for the
product and discount databases. The `cart.display_cart()` function takes as an
instance of `cart.Application` (the global state) and an instance of
`cart.Order`. The only function that needs to know the global state is
`display_cart` whereas other functions are called with lists of `cart.ItemPrice`
built up from the line items in an order.

I liberally made use of list comprehensions here as a way to code in Python in a
more functional style. I generally find them easier to read but they do present
problems for debugging in Python and other programmers might not agree they are
as readable as for loops.
