"""
database.py - SQLite database management for Expense Tracker
"""
import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = "expense_tracker.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def initialize_db():
    conn = get_connection()
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    UNIQUE NOT NULL,
            email       TEXT    UNIQUE NOT NULL,
            password    TEXT    NOT NULL,
            full_name   TEXT    NOT NULL,
            phone       TEXT,
            currency    TEXT    DEFAULT 'USD',
            created_at  TEXT    DEFAULT (datetime('now')),
            avatar_path TEXT
        )
    """)

    # Security questions for forgot password
    c.execute("""
        CREATE TABLE IF NOT EXISTS security_questions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            question    TEXT    NOT NULL,
            answer      TEXT    NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Categories table
    c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            name        TEXT    NOT NULL,
            type        TEXT    NOT NULL CHECK(type IN ('income','expense')),
            color       TEXT    DEFAULT '#4A90D9',
            icon        TEXT    DEFAULT '💰',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Transactions table
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            category_id INTEGER,
            type        TEXT    NOT NULL CHECK(type IN ('income','expense')),
            amount      REAL    NOT NULL CHECK(amount > 0),
            description TEXT,
            date        TEXT    NOT NULL,
            notes       TEXT,
            created_at  TEXT    DEFAULT (datetime('now')),
            updated_at  TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id)     REFERENCES users(id)      ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
        )
    """)

    # Settings table
    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER UNIQUE NOT NULL,
            theme           TEXT    DEFAULT 'light',
            currency        TEXT    DEFAULT 'USD',
            date_format     TEXT    DEFAULT '%Y-%m-%d',
            notifications   INTEGER DEFAULT 1,
            budget_limit    REAL    DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


# ─── USER OPERATIONS ─────────────────────────────────────────────────────────

def register_user(username, email, password, full_name, phone, question, answer):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO users (username, email, password, full_name, phone)
            VALUES (?, ?, ?, ?, ?)
        """, (username.strip(), email.strip(), hash_password(password),
              full_name.strip(), phone.strip()))
        user_id = c.lastrowid

        # Security question
        c.execute("""
            INSERT INTO security_questions (user_id, question, answer)
            VALUES (?, ?, ?)
        """, (user_id, question, hash_password(answer.lower().strip())))

        # Default settings
        c.execute("INSERT INTO settings (user_id) VALUES (?)", (user_id,))

        # Default categories
        default_income = [
            ('Salary', '#27AE60', '💼'), ('Freelance', '#2ECC71', '💻'),
            ('Investment', '#16A085', '📈'), ('Business', '#1ABC9C', '🏢'),
            ('Gift', '#3498DB', '🎁'), ('Other Income', '#2980B9', '💰'),
        ]
        default_expense = [
            ('Food & Dining', '#E74C3C', '🍽️'), ('Transport', '#C0392B', '🚗'),
            ('Housing', '#E67E22', '🏠'), ('Utilities', '#D35400', '💡'),
            ('Healthcare', '#9B59B6', '🏥'), ('Entertainment', '#8E44AD', '🎬'),
            ('Shopping', '#F39C12', '🛍️'), ('Education', '#F1C40F', '📚'),
            ('Travel', '#1ABC9C', '✈️'), ('Other Expense', '#95A5A6', '💸'),
        ]
        for name, color, icon in default_income:
            c.execute("INSERT INTO categories (user_id,name,type,color,icon) VALUES (?,?,?,?,?)",
                      (user_id, name, 'income', color, icon))
        for name, color, icon in default_expense:
            c.execute("INSERT INTO categories (user_id,name,type,color,icon) VALUES (?,?,?,?,?)",
                      (user_id, name, 'expense', color, icon))

        conn.commit()
        return True, "Registration successful!"
    except sqlite3.IntegrityError as e:
        if 'username' in str(e):
            return False, "Username already exists."
        elif 'email' in str(e):
            return False, "Email already registered."
        return False, str(e)
    finally:
        conn.close()


def login_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username.strip(), hash_password(password)))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None


def get_user(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def update_user(user_id, full_name, email, phone, currency):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            UPDATE users SET full_name=?, email=?, phone=?, currency=?
            WHERE id=?
        """, (full_name, email, phone, currency, user_id))
        conn.commit()
        return True, "Profile updated."
    except sqlite3.IntegrityError:
        return False, "Email already in use."
    finally:
        conn.close()


def change_password(user_id, old_pw, new_pw):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE id=? AND password=?",
              (user_id, hash_password(old_pw)))
    if not c.fetchone():
        conn.close()
        return False, "Current password is incorrect."
    c.execute("UPDATE users SET password=? WHERE id=?",
              (hash_password(new_pw), user_id))
    conn.commit()
    conn.close()
    return True, "Password changed successfully."


def reset_password_via_security(email, answer, new_password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email=?", (email.strip(),))
    row = c.fetchone()
    if not row:
        conn.close()
        return False, "Email not found."
    user_id = row['id']
    c.execute("SELECT answer FROM security_questions WHERE user_id=?", (user_id,))
    sq = c.fetchone()
    if not sq or sq['answer'] != hash_password(answer.lower().strip()):
        conn.close()
        return False, "Security answer is incorrect."
    c.execute("UPDATE users SET password=? WHERE id=?",
              (hash_password(new_password), user_id))
    conn.commit()
    conn.close()
    return True, "Password reset successful."


def get_security_question(email):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT sq.question FROM security_questions sq
        JOIN users u ON u.id = sq.user_id
        WHERE u.email=?
    """, (email.strip(),))
    row = c.fetchone()
    conn.close()
    return row['question'] if row else None


# ─── CATEGORY OPERATIONS ─────────────────────────────────────────────────────

def get_categories(user_id, cat_type=None):
    conn = get_connection()
    c = conn.cursor()
    if cat_type:
        c.execute("SELECT * FROM categories WHERE user_id=? AND type=? ORDER BY name",
                  (user_id, cat_type))
    else:
        c.execute("SELECT * FROM categories WHERE user_id=? ORDER BY type,name",
                  (user_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def add_category(user_id, name, cat_type, color='#4A90D9', icon='💰'):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO categories (user_id,name,type,color,icon) VALUES (?,?,?,?,?)",
              (user_id, name.strip(), cat_type, color, icon))
    conn.commit()
    conn.close()


def update_category(cat_id, name, color, icon):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE categories SET name=?,color=?,icon=? WHERE id=?",
              (name.strip(), color, icon, cat_id))
    conn.commit()
    conn.close()


def delete_category(cat_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM categories WHERE id=?", (cat_id,))
    conn.commit()
    conn.close()


# ─── TRANSACTION OPERATIONS ──────────────────────────────────────────────────

def add_transaction(user_id, cat_id, tx_type, amount, description, date, notes=''):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO transactions
            (user_id,category_id,type,amount,description,date,notes)
        VALUES (?,?,?,?,?,?,?)
    """, (user_id, cat_id, tx_type, float(amount),
          description.strip(), date, notes.strip()))
    conn.commit()
    conn.close()


def update_transaction(tx_id, cat_id, amount, description, date, notes=''):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE transactions
        SET category_id=?,amount=?,description=?,date=?,notes=?,
            updated_at=datetime('now')
        WHERE id=?
    """, (cat_id, float(amount), description.strip(), date, notes.strip(), tx_id))
    conn.commit()
    conn.close()


def delete_transaction(tx_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id=?", (tx_id,))
    conn.commit()
    conn.close()


def get_transactions(user_id, tx_type=None, start_date=None, end_date=None,
                     category_id=None, limit=None):
    conn = get_connection()
    c = conn.cursor()
    query = """
        SELECT t.*, c.name AS category_name, c.color, c.icon
        FROM transactions t
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE t.user_id = ?
    """
    params = [user_id]
    if tx_type:
        query += " AND t.type = ?"
        params.append(tx_type)
    if start_date:
        query += " AND t.date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND t.date <= ?"
        params.append(end_date)
    if category_id:
        query += " AND t.category_id = ?"
        params.append(category_id)
    query += " ORDER BY t.date DESC, t.created_at DESC"
    if limit:
        query += f" LIMIT {int(limit)}"
    c.execute(query, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_summary(user_id, start_date=None, end_date=None):
    conn = get_connection()
    c = conn.cursor()
    params = [user_id]
    date_filter = ""
    if start_date:
        date_filter += " AND date >= ?"
        params.append(start_date)
    if end_date:
        date_filter += " AND date <= ?"
        params.append(end_date)

    c.execute(f"""
        SELECT
            COALESCE(SUM(CASE WHEN type='income'  THEN amount ELSE 0 END), 0) AS total_income,
            COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) AS total_expense
        FROM transactions WHERE user_id=? {date_filter}
    """, params)
    row = c.fetchone()
    conn.close()
    income  = row['total_income']
    expense = row['total_expense']
    return {'income': income, 'expense': expense, 'balance': income - expense}


def get_monthly_data(user_id, year):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT strftime('%m', date) AS month,
               type,
               SUM(amount) AS total
        FROM transactions
        WHERE user_id=? AND strftime('%Y', date)=?
        GROUP BY month, type
        ORDER BY month
    """, (user_id, str(year)))
    rows = c.fetchall()
    conn.close()
    data = {'income': [0]*12, 'expense': [0]*12}
    for row in rows:
        idx = int(row['month']) - 1
        data[row['type']][idx] = row['total']
    return data


def get_category_breakdown(user_id, tx_type, start_date=None, end_date=None):
    conn = get_connection()
    c = conn.cursor()
    params = [user_id, tx_type]
    date_filter = ""
    if start_date:
        date_filter += " AND t.date >= ?"
        params.append(start_date)
    if end_date:
        date_filter += " AND t.date <= ?"
        params.append(end_date)
    c.execute(f"""
        SELECT c.name, c.color, c.icon, SUM(t.amount) AS total
        FROM transactions t
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE t.user_id=? AND t.type=? {date_filter}
        GROUP BY t.category_id
        ORDER BY total DESC
    """, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


# ─── SETTINGS ────────────────────────────────────────────────────────────────

def get_settings(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM settings WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else {}


def update_settings(user_id, theme, currency, date_format, notifications, budget_limit):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE settings
        SET theme=?,currency=?,date_format=?,notifications=?,budget_limit=?
        WHERE user_id=?
    """, (theme, currency, date_format, int(notifications), float(budget_limit), user_id))
    conn.commit()
    conn.close()
