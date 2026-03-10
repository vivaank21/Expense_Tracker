# 📊 Data Flow Diagram (DFD) — Expense Tracker Pro

---

## Level 0 — Context Diagram

```
                         ┌─────────────────────────┐
                         │                         │
  User ──── Credentials ─►   Expense Tracker Pro   ◄─── System Date/Time
            Profile Info │                         │
            Transactions │   (Single Process)      │
                    ◄────┤                         ├────► Reports / PDF
                         │                         │
                         └─────────────────────────┘
```

**External Entities:**
| Entity | Description |
|---|---|
| **User** | The person using the application |
| **System Clock** | Provides current date/time for defaults |
| **File System** | Stores the SQLite database and exported PDFs |

---

## Level 1 — Major Processes

```
                           ┌──────────────────────┐
                           │   D1: Users Table    │
                           └──────────┬───────────┘
         ┌─────────────┐              │ User Record
  User ──► 1.0         ├──── Auth ───►│
         │ Authentication│            │
         │ & User Mgmt  ◄────────────┘
         └──────┬───────┘
                │ User ID / Session
                │
         ┌──────▼───────┐    ┌─────────────────────┐
         │ 2.0           │    │  D2: Transactions   │
  User ──► Transaction   ├───►│  Table              │
         │ Management   ◄────│                     │
         └──────┬───────┘    └─────────────────────┘
                │                   ▲
                │ Filtered Data      │
         ┌──────▼───────┐    ┌──────┴──────────────┐
         │ 3.0           │    │  D3: Categories     │
         │ Category      ├───►│  Table              │
         │ Management   ◄────│                     │
         └──────┬───────┘    └─────────────────────┘
                │
         ┌──────▼───────┐    ┌─────────────────────┐
         │ 4.0           │    │  D4: Settings Table │
  User ──► Reporting &   │    │                     │
         │ Analytics    ├───►│                     │
         └──────┬───────┘    └─────────────────────┘
                │
         ┌──────▼───────┐
         │ 5.0           │
         │ PDF Export    ├───► File System (PDF)
         └──────────────┘
```

---

## Level 2 — Process 1: Authentication & User Management

```
  User                Process 1.0: Authentication
  ─────               ────────────────────────────
  username        ──► 1.1 Validate Credentials
  password            │   - Hash password (SHA-256)
                       │   - Compare with DB record
                       ▼
                      1.2 Session Management
                       │   - Store user_id in memory
                       │   - Load user preferences
                       ▼
  email           ──► 1.3 Registration
  full_name           │   - Validate uniqueness
  security_q          │   - Hash password
  security_a          │   - Create default categories
                       ▼
                      1.4 Password Reset
  email           ──►     - Verify email exists
  security_answer         - Compare hashed answer
  new_password            - Update password hash
```

---

## Level 2 — Process 2: Transaction Management

```
  User                Process 2.0: Transaction Management
  ─────               ─────────────────────────────────────
  amount          ──► 2.1 Add Transaction
  category            │   - Validate amount > 0
  description         │   - Validate date format
  date                │   - Link to category
  notes               │   - Insert into DB
                       ▼
  transaction_id  ──► 2.2 Edit Transaction
  new_data            │   - Verify ownership
                       │   - Update record
                       ▼
  transaction_id  ──► 2.3 Delete Transaction
                       │   - Verify ownership
                       │   - Remove from DB
                       ▼
  filters         ──► 2.4 Filter & View
  (date range,        │   - Apply WHERE clauses
   category,          │   - Sort by date DESC
   type)              │   - Return records
```

---

## Level 2 — Process 4: Reporting & Analytics

```
  User             Process 4.0: Reporting & Analytics
  ─────            ────────────────────────────────────
  year         ──► 4.1 Fetch Monthly Data
  chart_type       │   - GROUP BY month
                    │   - Separate income/expense
                    ▼
                   4.2 Compute Aggregates
                    │   - SUM per category
                    │   - Calculate balance
                    │   - Profit/Loss per month
                    ▼
                   4.3 Render Chart
                    │   - Bar Chart (monthly)
                    │   - Pie Chart (category)
                    │   - Line/Fill (trend)
                    ▼
                   Chart (Tkinter Canvas widget)
```

---

## Data Stores Summary

| Store | Table | Description |
|---|---|---|
| D1 | users | User accounts and credentials |
| D2 | transactions | All financial transactions |
| D3 | categories | Income/expense categories |
| D4 | settings | Per-user preferences |
| D5 | security_questions | Password recovery data |
