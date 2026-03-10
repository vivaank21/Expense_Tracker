# 💰 Expense Tracker Pro

A full-featured personal finance management desktop application built with **Python**, **Tkinter**, **SQLite**, and **Matplotlib**.

---

## 📋 Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Modules Overview](#modules-overview)
- All screenshots are in img folder

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 Authentication | Signup, Login, Forgot Password via security question |
| 💵 Income Management | Add, Edit, Delete income transactions with categories |
| 💸 Expense Management | Add, Edit, Delete expense transactions with categories |
| 🏷️ Categories | Custom categories with icons and colors for both types |
| 📊 Reports & Charts | Monthly bar charts, pie charts, profit/loss trend lines |
| 📥 PDF Export | Password-protected PDF export of transaction history |
| 👤 Profile | Edit personal info and change password |
| ⚙️ Settings | Theme (dark/light), currency, date format, budget limits |
| 🌙 Dark/Light Theme | Full dark and light mode support |
| 💱 Multi-Currency | USD, EUR, GBP, INR, JPY, CAD, AUD, CHF |

---

## 🖥️ Requirements

- Python 3.8+
- tkinter (included with Python)
- matplotlib
- reportlab
- pypdf

---

## 📦 Installation

```bash
# Clone or download the project
cd expense_tracker

# Install dependencies
pip install matplotlib reportlab pypdf pillow

# Run the application
python app.py
```

---

## 🚀 Usage

### First Run
1. Run `python app.py`
2. Click **"Create one"** to sign up
3. Fill in your details and set a security question
4. Log in with your credentials

### Adding Transactions
- Navigate to **Income** or **Expenses** from the sidebar
- Click **"＋ Add Income/Expense"**
- Fill in amount, category, description, and date

### Viewing Reports
- Go to **Reports** from the sidebar
- Select a year and chart type (Monthly, Pie, Trend)
- Click **Refresh** to update

### Exporting PDF
- Go to **Income** or **Expenses**
- Click **"📥 Export PDF"**
- Set an optional password and choose save location

---

## 📁 Project Structure

```
expense_tracker/
├── app.py              # Entry point
├── database.py         # SQLite database layer
├── auth_window.py      # Login / Signup / Forgot Password UI
├── main_app.py         # Main application window (all pages)
├── expense_tracker.db  # SQLite database (auto-created)
├── README.md
├── DFD.md
├── ER_Diagram.md
├── Data_Dictionary.md
└── Test_Cases.md
```

---

## 🗃️ Modules Overview

### `database.py`
All SQLite operations: user management, transactions, categories, settings.

### `auth_window.py`
Tkinter UI for login, registration, and forgot-password flow.

### `main_app.py`
Main application with sidebar navigation and all feature pages.

### `app.py`
Entry point — initialises DB and launches auth window.

---

## 🔒 Security
- Passwords are stored as **SHA-256 hashes** (never plain text)
- Security question answers are also hashed
- PDF exports can be **AES-encrypted** with a user-chosen password
- SQLite foreign key constraints enforce data integrity

---

## 📊 Charts Available
1. **Monthly Bar Chart** – Income vs Expense per month
2. **Income Pie Chart** – Breakdown by category
3. **Expense Pie Chart** – Breakdown by category
4. **Profit/Loss Trend** – Line chart with filled profit/loss areas

---

## 🛠️ Built With
- **Python 3** — Core language
- **Tkinter** — Desktop GUI
- **SQLite3** — Embedded database
- **Matplotlib** — Charts and graphs
- **ReportLab** — PDF generation
- **PyPDF** — PDF encryption

---

## 📄 License
MIT License — Free for personal and educational use.
