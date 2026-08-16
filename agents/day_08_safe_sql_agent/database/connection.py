"""Database connection management and execution routines."""

import psycopg2
import sqlite3
from agents.day_08_safe_sql_agent.config import DATABASE_URL

_demo_conn = None

def get_demo_connection():
    global _demo_conn
    if _demo_conn is None:
        _demo_conn = sqlite3.connect(":memory:", check_same_thread=False)
        cursor = _demo_conn.cursor()
        cursor.execute("""
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                total_amount NUMERIC NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)
        cursor.executemany("INSERT INTO customers VALUES (?, ?, ?)", [
            (1, "Alice Johnson", "alice@example.com"),
            (2, "Bob Smith", "bob@example.com"),
            (3, "Charlie Brown", "charlie@example.com"),
            (4, "Diana Prince", "diana@example.com"),
        ])
        cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", [
            (101, 1, 450.00, "2026-01-10"),
            (102, 1, 850.00, "2026-02-15"),
            (103, 2, 300.00, "2026-02-20"),
            (104, 3, 1200.00, "2026-03-01"),
            (105, 1, 200.00, "2026-03-10"),
            (106, 4, 950.00, "2026-03-15"),
        ])
        _demo_conn.commit()
    return _demo_conn


def get_connection():
    return psycopg2.connect(DATABASE_URL)




