"""Streamlit dashboard for the customer data pipeline (read-only).

Run:  streamlit run dashboard.py
Reuses the SQL in analytics.sql, so the dashboard and report.py always agree.
"""
from decimal import Decimal
from pathlib import Path

import pandas as pd
import streamlit as st

from db import get_connection
from report import load_queries

st.set_page_config(page_title="Customer Data Pipeline", layout="wide")


@st.cache_data(ttl=600)
def run_queries():
    """Run every query in analytics.sql and return {title: DataFrame}."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        results = {}
        for title, sql in load_queries(Path(__file__).with_name("analytics.sql")):
            cursor.execute(sql)
            columns = [d[0] for d in cursor.description]
            rows = [[float(v) if isinstance(v, Decimal) else v for v in row]
                    for row in cursor.fetchall()]
            results[title] = pd.DataFrame(rows, columns=columns)
        return results
    finally:
        conn.close()


st.title("Customer Data Pipeline Dashboard")
st.caption("Synthetic e-commerce data in MySQL (Aiven), queried with Python. Cancelled orders are excluded.")

data = run_queries()
monthly = data["Monthly revenue"]
repeat = data["Repeat customer rate"].iloc[0]

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total revenue", f"{monthly['revenue'].sum():,.0f}")
kpi2.metric("Orders", f"{int(monthly['orders'].sum()):,}")
kpi3.metric("Customers with orders", f"{int(repeat['customers_with_orders']):,}")
kpi4.metric("Repeat customer rate", f"{repeat['repeat_rate_pct']:.1f}%")

st.subheader("Monthly revenue")
st.line_chart(monthly.set_index("month")["revenue"])

left, right = st.columns(2)
with left:
    st.subheader("Revenue by product category")
    st.bar_chart(data["Revenue by product category"].set_index("category")["revenue"])
with right:
    st.subheader("Revenue by city")
    st.bar_chart(data["Revenue by city"].set_index("city")["revenue"])

st.subheader("Top 5 customers by spend")
st.dataframe(data["Top 5 customers by spend"], hide_index=True, use_container_width=True)
