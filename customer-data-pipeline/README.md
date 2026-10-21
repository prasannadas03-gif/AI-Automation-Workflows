# Customer Data Pipeline (Python + MySQL)

A small data pipeline that generates sample e-commerce data, loads it into a cloud MySQL database (Aiven) over SSL, and reports business metrics using SQL and a web dashboard (Streamlit). The scripts can run anywhere with Python; I ran the load and report steps on an Oracle Cloud VM, and the dashboard connects straight to the database.

## What it does

1. **Schema:** creates four related tables (`cdp_customers`, `cdp_products`, `cdp_orders`, `cdp_order_items`) with primary and foreign keys.
2. **Load:** generates reproducible fake data (200 customers, 12 products, 1000 orders, about 2000 order items) and bulk-inserts it with `executemany`.
3. **Analyse:** runs SQL queries with joins, grouping and a subquery, and prints text tables.

## Tech

- Python 3, `mysql-connector-python`, `python-dotenv`
- MySQL 8.4 on Aiven, connected over SSL with a CA certificate
- Streamlit for the web dashboard (hosted on Streamlit Community Cloud)
- Load and report scripts run in a Python virtual environment (I used an Oracle Cloud VM)

## Project layout

| File | Purpose |
|---|---|
| `schema.sql` | Table definitions |
| `generate_data.py` | Reproducible fake data (no real personal data) |
| `load_data.py` | Creates the schema and loads the data |
| `analytics.sql` | Five analytics queries |
| `report.py` | Runs the queries and prints the results |
| `dashboard.py` | Streamlit web dashboard |
| `db.py` | Connection helper, credentials from environment variables |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env     # then fill in your own database details
```

Download your database provider's CA certificate and save it as `ca.pem` (or set `DB_SSL_CA`).

## Run

```bash
python load_data.py   # drops and recreates only the cdp_* tables, then loads data
python report.py      # read-only analytics report
```

Never commit `.env` or `ca.pem`. The `.gitignore` already excludes them.

## Dashboard

`dashboard.py` is a Streamlit web dashboard over the same queries (KPIs, monthly revenue trend, category and city charts, top customers).

```bash
streamlit run dashboard.py
```

To publish it on Streamlit Community Cloud, deploy this repo with `customer-data-pipeline/dashboard.py` as the main file, and paste your database settings into the app's Secrets box using `secrets.example.toml` as a template. Use a read-only database user for any public deployment.

## Sample output

All data is synthetic, so these figures are made up by the generator.

```
=== Revenue by product category ===
category     units_sold  revenue
-----------  ----------  ----------
Electronics  1588        3795412.00
Accessories  873         977777.00
Home         565         407135.00
Stationery   604         118996.00

=== Repeat customer rate ===
customers_with_orders  repeat_customers  repeat_rate_pct
---------------------  ----------------  ---------------
196                    186               94.9
```

## SQL concepts shown

- Multi-table `JOIN`s across four tables
- `GROUP BY` with aggregates (`SUM`, `COUNT DISTINCT`)
- Date formatting for monthly trends
- A derived-table subquery for the repeat-customer rate
- Foreign keys and referential integrity
