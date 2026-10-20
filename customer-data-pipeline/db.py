"""Database connection helper.

Settings come from environment variables (.env) first. When they are missing, for
example on Streamlit Community Cloud, they are read from Streamlit secrets instead.
"""
import os
import tempfile

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def _setting(name, default=None):
    value = os.environ.get(name)
    if value is not None:
        return value
    try:
        import streamlit as st
        return st.secrets.get(name, default)
    except Exception:
        return default


def _required(name):
    value = _setting(name)
    if value is None:
        raise KeyError(f"Missing setting: {name}")
    return value


def _ca_path():
    """Return the CA certificate path, writing it from DB_SSL_CA_PEM if that is provided."""
    pem = _setting("DB_SSL_CA_PEM")
    if pem:
        path = os.path.join(tempfile.gettempdir(), "db-ca.pem")
        with open(path, "w", encoding="utf-8") as f:
            f.write(pem)
        return path
    return _setting("DB_SSL_CA", "ca.pem")


def get_connection():
    return mysql.connector.connect(
        host=_required("DB_HOST"),
        port=int(_setting("DB_PORT", "3306")),
        user=_required("DB_USER"),
        password=_required("DB_PASSWORD"),
        database=_required("DB_NAME"),
        ssl_ca=_ca_path(),
    )
