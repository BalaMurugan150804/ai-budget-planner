import sqlite3
import pandas as pd
from datetime import datetime

import os
os.makedirs("data", exist_ok=True)
DB_PATH = "data/budget.db"

def init_db():
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            mood TEXT,
            payment_mode TEXT DEFAULT 'UPI',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS regret_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_id INTEGER,
            regret INTEGER DEFAULT 0,
            checked_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(expense_id) REFERENCES expenses(id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            target_days INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            active INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def add_expense(date, amount, category, description, mood, payment_mode):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO expenses (date, amount, category, description, mood, payment_mode)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, amount, category, description, mood, payment_mode))
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM expenses ORDER BY date DESC", conn
    )
    conn.close()
    return df

def get_expenses_by_month(year, month):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT * FROM expenses
        WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
        ORDER BY date DESC
    """, conn, params=(str(year), f"{month:02d}"))
    conn.close()
    return df

def get_monthly_summary():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT strftime('%Y-%m', date) as month,
               SUM(amount) as total,
               COUNT(*) as count
        FROM expenses
        GROUP BY month
        ORDER BY month DESC
        LIMIT 6
    """, conn)
    conn.close()
    return df

def save_regret(expense_id, regret):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO regret_scores (expense_id, regret, checked_at)
        VALUES (?, ?, ?)
    """, (expense_id, regret, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def add_challenge(category, title, target_days):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO challenges (category, title, target_days, start_date)
        VALUES (?, ?, ?, ?)
    """, (category, title, target_days, datetime.now().date().isoformat()))
    conn.commit()
    conn.close()

def get_active_challenges():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM challenges WHERE active = 1", conn
    )
    conn.close()
    return df
