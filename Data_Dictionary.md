# 📖 Data Dictionary — Expense Tracker Pro

---

## Overview

This document defines all data elements used in the Expense Tracker Pro application, including database fields, data types, constraints, and business rules.

---

## Table: `users`

| Field | Data Type | Size | Nullable | Default | Constraint | Description |
|---|---|---|---|---|---|---|
| id | INTEGER | — | No | AUTO | PK | Unique auto-incremented user ID |
| username | TEXT | 50 | No | — | UNIQUE | Alphanumeric login name; case-sensitive |
| email | TEXT | 100 | No | — | UNIQUE | Valid email address format |
| password | TEXT | 64 | No | — | NOT NULL | SHA-256 hex digest of user's password |
| full_name | TEXT | 100 | No | — | NOT NULL | User's display name |
| phone | TEXT | 20 | Yes | NULL | — | Optional contact number |
| currency | TEXT | 10 | No | 'USD' | — | ISO 4217 currency code |
| created_at | TEXT | 20 | No | datetime('now') | — | ISO 8601 timestamp |
| avatar_path | TEXT | 255 | Yes | NULL | — | Filesystem path to avatar image |

**Business Rules:**
- `username` must be unique across the system
- `email` must be unique across the system
- `password` is NEVER stored in plaintext; always SHA-256 hashed
- `currency` must be one of: USD, EUR, GBP, INR, JPY, CAD, AUD, CHF

---

## Table: `security_questions`

| Field | Data Type | Size | Nullable | Default | Constraint | Description |
|---|---|---|---|---|---|---|
| id | INTEGER | — | No | AUTO | PK | Record identifier |
| user_id | INTEGER | — | No | — | FK → users.id | Owner of this security question |
| question | TEXT | 255 | No | — | NOT NULL | Full text of chosen security question |
| answer | TEXT | 64 | No | — | NOT NULL | SHA-256 hash of lowercase trimmed answer |

**Business Rules:**
- Each user has exactly one security question record
- `answer` is stored hashed using SHA-256 (lowercased and trimmed before hashing)
- Deletion of user cascades to delete this record

---

## Table: `categories`

| Field | Data Type | Size | Nullable | Default | Constraint | Description |
|---|---|---|---|---|---|---|
| id | INTEGER | — | No | AUTO | PK | Category identifier |
| user_id | INTEGER | — | No | — | FK → users.id | Owning user |
| name | TEXT | 50 | No | — | NOT NULL | Category label |
| type | TEXT | 10 | No | — | CHECK | Must be 'income' or 'expense' |
| color | TEXT | 7 | No | '#4A90D9' | — | Hex color code (#RRGGBB) |
| icon | TEXT | 10 | No | '💰' | — | Single emoji character |

**Business Rules:**
- `type` must be exactly 'income' or 'expense'
- `color` must be a valid 6-digit hex color
- Default categories are auto-created on user registration
- Deleting a category sets `category_id` to NULL on related transactions (preserves history)

---

## Table: `transactions`

| Field | Data Type | Size | Nullable | Default | Constraint | Description |
|---|---|---|---|---|---|---|
| id | INTEGER | — | No | AUTO | PK | Transaction identifier |
| user_id | INTEGER | — | No | — | FK → users.id | Owning user |
| category_id | INTEGER | — | Yes | NULL | FK → categories.id | Linked category (nullable) |
| type | TEXT | 10 | No | — | CHECK | Must be 'income' or 'expense' |
| amount | REAL | — | No | — | CHECK > 0 | Positive monetary value |
| description | TEXT | 255 | Yes | NULL | — | Brief transaction label |
| date | TEXT | 10 | No | — | NOT NULL | Date in YYYY-MM-DD format |
| notes | TEXT | 1000 | Yes | NULL | — | Extended free-form notes |
| created_at | TEXT | 20 | No | datetime('now') | — | Record creation timestamp |
| updated_at | TEXT | 20 | No | datetime('now') | — | Last modification timestamp |

**Business Rules:**
- `amount` must always be greater than 0
- `date` must follow ISO format YYYY-MM-DD
- `type` must be exactly 'income' or 'expense'
- `updated_at` is updated by application logic on every edit
- Deleting a user cascades to delete all their transactions

---

## Table: `settings`

| Field | Data Type | Size | Nullable | Default | Constraint | Description |
|---|---|---|---|---|---|---|
| id | INTEGER | — | No | AUTO | PK | Settings record ID |
| user_id | INTEGER | — | No | — | FK, UNIQUE | One-to-one with user |
| theme | TEXT | 10 | No | 'light' | — | 'dark' or 'light' |
| currency | TEXT | 10 | No | 'USD' | — | ISO 4217 currency code |
| date_format | TEXT | 20 | No | '%Y-%m-%d' | — | Python strftime format string |
| notifications | INTEGER | — | No | 1 | — | 1=enabled, 0=disabled |
| budget_limit | REAL | — | No | 0 | — | Monthly limit (0=unlimited) |

**Business Rules:**
- Each user has exactly one settings record (created at registration)
- `theme` must be 'dark' or 'light'
- `notifications` is treated as boolean (1/0)
- `budget_limit` of 0 means no limit is set

---

## Enumerated Values

### Transaction / Category `type`
| Value | Description |
|---|---|
| `income` | Money received by the user |
| `expense` | Money spent by the user |

### Supported Currencies
| Code | Symbol | Currency Name |
|---|---|---|
| USD | $ | US Dollar |
| EUR | € | Euro |
| GBP | £ | British Pound |
| INR | ₹ | Indian Rupee |
| JPY | ¥ | Japanese Yen |
| CAD | CA$ | Canadian Dollar |
| AUD | A$ | Australian Dollar |
| CHF | CHF | Swiss Franc |

### UI Themes
| Value | Description |
|---|---|
| `dark` | Dark background, light text (default for new users) |
| `light` | Light background, dark text |

---

## Derived / Computed Values

These values are NOT stored in the database but are computed at runtime:

| Derived Value | Formula | Usage |
|---|---|---|
| `total_income` | SUM(amount) WHERE type='income' | Dashboard summary cards |
| `total_expense` | SUM(amount) WHERE type='expense' | Dashboard summary cards |
| `net_balance` | total_income – total_expense | Balance display |
| `monthly_profit_loss` | monthly_income – monthly_expense | Reports trend chart |
| `category_percentage` | (category_total / type_total) * 100 | Pie chart labels |

---

## Security Specifications

| Data Element | Storage Method | Algorithm |
|---|---|---|
| User password | Hashed | SHA-256 (hashlib) |
| Security answer | Hashed | SHA-256 (lowercased, trimmed) |
| PDF password | Encryption | AES-128 (via PyPDF/pypdf) |
| Session data | In-memory only | Python dict |

---

## Date & Time Formats

| Format | Example | Usage |
|---|---|---|
| `YYYY-MM-DD` | 2025-03-15 | Database storage, default display |
| `DD/MM/YYYY` | 15/03/2025 | UK/EU date format option |
| `MM/DD/YYYY` | 03/15/2025 | US date format option |
| `YYYY-MM-DD HH:MM:SS` | 2025-03-15 14:30:00 | Timestamp fields |
