"""Generate reproducible fake customers, products, orders and order items.

No real personal data is used: names come from small lists and emails use example.com.
"""
import random
from datetime import date, timedelta

FIRST_NAMES = ["Aarav", "Anaya", "Rohan", "Diya", "Kabir", "Meera", "Ishaan", "Sara",
               "Vihaan", "Nisha", "Arjun", "Priya", "Neil", "Tara", "Dev", "Zoya"]
LAST_NAMES = ["Sharma", "Patel", "Khan", "Das", "Singh", "Reddy", "Mehta", "Nair",
              "Gupta", "Iyer", "Bose", "Joshi"]
CITIES = ["Mumbai", "Delhi", "Bengaluru", "Kolkata", "Chennai", "Pune", "Hyderabad", "Jaipur"]
PRODUCTS = [
    ("Wireless Mouse", "Electronics", 799), ("Mechanical Keyboard", "Electronics", 3499),
    ("USB-C Hub", "Electronics", 1899), ("Laptop Stand", "Accessories", 1299),
    ("Notebook Pack", "Stationery", 249), ("Gel Pen Set", "Stationery", 149),
    ("Desk Lamp", "Home", 999), ("Water Bottle", "Home", 449),
    ("Backpack", "Accessories", 1599), ("Webcam", "Electronics", 2499),
    ("Headphones", "Electronics", 2999), ("Phone Stand", "Accessories", 349),
]
STATUSES = ["delivered"] * 8 + ["shipped", "cancelled"]


def generate(n_customers=200, n_orders=1000, seed=42):
    rng = random.Random(seed)
    today = date(2026, 10, 1)

    customers = []
    for i in range(1, n_customers + 1):
        first, last = rng.choice(FIRST_NAMES), rng.choice(LAST_NAMES)
        signup = today - timedelta(days=rng.randint(60, 700))
        customers.append((f"{first} {last}", f"{first}.{last}{i}@example.com".lower(),
                          rng.choice(CITIES), signup))

    products = [(name, category, price) for name, category, price in PRODUCTS]

    orders, items = [], []
    for order_id in range(1, n_orders + 1):
        customer_id = rng.randint(1, n_customers)
        order_date = today - timedelta(days=rng.randint(0, 330))
        orders.append((customer_id, order_date, rng.choice(STATUSES)))
        for product_id in rng.sample(range(1, len(products) + 1), rng.randint(1, 3)):
            items.append((order_id, product_id, rng.randint(1, 3), products[product_id - 1][2]))

    return customers, products, orders, items
