"""Create the schema in MySQL and load generated sample data.

Only the cdp_* tables are dropped and recreated (see schema.sql).
"""
from pathlib import Path

from db import get_connection
from generate_data import generate


def run_schema(cursor, path):
    sql = Path(path).read_text(encoding="utf-8")
    for statement in sql.split(";"):
        lines = [l for l in statement.splitlines() if not l.strip().startswith("--")]
        statement = "\n".join(lines).strip()
        if statement:
            cursor.execute(statement)


def main():
    customers, products, orders, items = generate()
    conn = get_connection()
    try:
        cursor = conn.cursor()
        run_schema(cursor, Path(__file__).with_name("schema.sql"))
        cursor.executemany(
            "INSERT INTO cdp_customers (full_name, email, city, signup_date) VALUES (%s, %s, %s, %s)",
            customers)
        cursor.executemany(
            "INSERT INTO cdp_products (name, category, price) VALUES (%s, %s, %s)", products)
        cursor.executemany(
            "INSERT INTO cdp_orders (customer_id, order_date, status) VALUES (%s, %s, %s)", orders)
        cursor.executemany(
            "INSERT INTO cdp_order_items (order_id, product_id, quantity, unit_price) "
            "VALUES (%s, %s, %s, %s)", items)
        conn.commit()
        print(f"Loaded {len(customers)} customers, {len(products)} products, "
              f"{len(orders)} orders, {len(items)} order items.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
