"""Run every query in analytics.sql (read-only) and print the results as text tables."""
from pathlib import Path

from db import get_connection


def load_queries(path):
    queries = []
    for block in Path(path).read_text(encoding="utf-8").split("-- name:")[1:]:
        title, _, sql = block.partition("\n")
        queries.append((title.strip(), sql.strip().rstrip(";")))
    return queries


def print_table(title, columns, rows):
    print(f"\n=== {title} ===")
    widths = [max(len(str(v)) for v in [col] + [r[i] for r in rows]) for i, col in enumerate(columns)]
    print("  ".join(col.ljust(w) for col, w in zip(columns, widths)))
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print("  ".join(str(v).ljust(w) for v, w in zip(row, widths)))


def main():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        for title, sql in load_queries(Path(__file__).with_name("analytics.sql")):
            cursor.execute(sql)
            columns = [d[0] for d in cursor.description]
            print_table(title, columns, cursor.fetchall())
    finally:
        conn.close()


if __name__ == "__main__":
    main()
