"""
app.py - Entry point for Expense Tracker Pro
"""
import database as db
import auth_window
from main_app import ExpenseTrackerApp


def on_login_success(user: dict):
    ExpenseTrackerApp(user)


def main():
    db.initialize_db()
    auth_window.AuthWindow(on_login_success)


if __name__ == "__main__":
    main()
