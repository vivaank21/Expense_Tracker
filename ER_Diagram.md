# 🗄️ Entity-Relationship (ER) Diagram — Expense Tracker Pro

---

## Entities and Relationships

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│   ┌───────────────────┐        ┌───────────────────────────┐    │
│   │      USERS        │        │   SECURITY_QUESTIONS      │    │
│   ├───────────────────┤  1   1 ├───────────────────────────┤    │
│   │ PK id             ├────────┤ PK id                     │    │
│   │    username (UQ)  │        │ FK user_id                │    │
│   │    email (UQ)     │        │    question               │    │
│   │    password       │        │    answer (hashed)        │    │
│   │    full_name      │        └───────────────────────────┘    │
│   │    phone          │                                         │
│   │    currency       │                                         │
│   │    created_at     │                                         │
│   │    avatar_path    │                                         │
│   └────────┬──────────┘                                         │
│            │                                                     │
│            │ 1:N                                                 │
│            │                                                     │
│   ┌────────▼──────────┐        ┌───────────────────────────┐    │
│   │    CATEGORIES     │        │        SETTINGS           │    │
│   ├───────────────────┤  1   1 ├───────────────────────────┤    │
│   │ PK id             │        │ PK id                     │    │
│   │ FK user_id        ├────────┤ FK user_id (UQ)           │    │
│   │    name           │        │    theme                  │    │
│   │    type (enum)    │        │    currency               │    │
│   │    color          │        │    date_format            │    │
│   │    icon           │        │    notifications          │    │
│   └────────┬──────────┘        │    budget_limit          │    │
│            │                   └───────────────────────────┘    │
│            │ 1:N                                                 │
│            │                                                     │
│   ┌────────▼──────────┐                                         │
│   │   TRANSACTIONS    │                                         │
│   ├───────────────────┤                                         │
│   │ PK id             │                                         │
│   │ FK user_id        │                                         │
│   │ FK category_id    │  (nullable — ON DELETE SET NULL)        │
│   │    type (enum)    │                                         │
│   │    amount         │                                         │
│   │    description    │                                         │
│   │    date           │                                         │
│   │    notes          │                                         │
│   │    created_at     │                                         │
│   │    updated_at     │                                         │
│   └───────────────────┘                                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Cardinality & Relationships

| Relationship | Type | Rule |
|---|---|---|
| User → Security Questions | 1 : 1 | Each user has exactly one security question |
| User → Categories | 1 : N | One user owns many categories |
| User → Transactions | 1 : N | One user has many transactions |
| User → Settings | 1 : 1 | Each user has one settings record |
| Category → Transactions | 1 : N | One category applies to many transactions |

---

## Entity Details

### USERS
| Attribute | Type | Constraint | Description |
|---|---|---|---|
| id | INTEGER | PK, AUTO | Unique user identifier |
| username | TEXT | NOT NULL, UNIQUE | Login identifier |
| email | TEXT | NOT NULL, UNIQUE | Contact email |
| password | TEXT | NOT NULL | SHA-256 hash of password |
| full_name | TEXT | NOT NULL | Display name |
| phone | TEXT | NULLABLE | Optional phone number |
| currency | TEXT | DEFAULT 'USD' | Preferred currency code |
| created_at | TEXT | DEFAULT now | Account creation timestamp |
| avatar_path | TEXT | NULLABLE | Path to profile image |

### CATEGORIES
| Attribute | Type | Constraint | Description |
|---|---|---|---|
| id | INTEGER | PK, AUTO | Category identifier |
| user_id | INTEGER | FK → users.id | Owner of this category |
| name | TEXT | NOT NULL | Display name |
| type | TEXT | CHECK income/expense | Category type |
| color | TEXT | DEFAULT '#4A90D9' | Hex color for charts |
| icon | TEXT | DEFAULT '💰' | Emoji icon |

### TRANSACTIONS
| Attribute | Type | Constraint | Description |
|---|---|---|---|
| id | INTEGER | PK, AUTO | Transaction identifier |
| user_id | INTEGER | FK → users.id | Owner |
| category_id | INTEGER | FK → categories.id | Category (nullable) |
| type | TEXT | CHECK income/expense | Transaction type |
| amount | REAL | CHECK > 0 | Amount (always positive) |
| description | TEXT | NULLABLE | Short label |
| date | TEXT | NOT NULL | Date in YYYY-MM-DD format |
| notes | TEXT | NULLABLE | Extended notes |
| created_at | TEXT | DEFAULT now | Record creation time |
| updated_at | TEXT | DEFAULT now | Last edit time |

### SETTINGS
| Attribute | Type | Constraint | Description |
|---|---|---|---|
| id | INTEGER | PK, AUTO | Settings record id |
| user_id | INTEGER | FK, UNIQUE | One-to-one with user |
| theme | TEXT | DEFAULT 'light' | UI theme |
| currency | TEXT | DEFAULT 'USD' | Display currency |
| date_format | TEXT | DEFAULT '%Y-%m-%d' | Date display format |
| notifications | INTEGER | DEFAULT 1 | Budget alerts on/off |
| budget_limit | REAL | DEFAULT 0 | Monthly spending limit |

### SECURITY_QUESTIONS
| Attribute | Type | Constraint | Description |
|---|---|---|---|
| id | INTEGER | PK, AUTO | Record identifier |
| user_id | INTEGER | FK → users.id | Associated user |
| question | TEXT | NOT NULL | Security question text |
| answer | TEXT | NOT NULL | SHA-256 hash of answer |
