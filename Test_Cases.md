# 🧪 Test Cases — Expense Tracker Pro

---

## Test Environment
- **Application:** Expense Tracker Pro
- **Platform:** Python 3.8+ / Windows / macOS / Linux
- **Database:** SQLite3
- **Testing Type:** Functional / Black-box

---

## Module 1: Authentication

### TC-001: Valid User Registration
| Field | Value |
|---|---|
| **Test ID** | TC-001 |
| **Module** | Authentication — Sign Up |
| **Description** | Register a new user with valid data |
| **Precondition** | Application launched, database initialised |
| **Input** | Full Name: "John Doe", Username: "johndoe", Email: "john@example.com", Phone: "1234567890", Password: "Pass@123", Confirm: "Pass@123", Security Q+A set |
| **Expected Output** | Success message shown; user redirected to login |
| **Status** | PASS |

### TC-002: Duplicate Username Registration
| Field | Value |
|---|---|
| **Test ID** | TC-002 |
| **Module** | Authentication — Sign Up |
| **Description** | Attempt to register with an already-taken username |
| **Precondition** | User "johndoe" already exists |
| **Input** | Username: "johndoe", all other fields valid |
| **Expected Output** | Error: "Username already exists." |
| **Status** | PASS |

### TC-003: Password Mismatch on Signup
| Field | Value |
|---|---|
| **Test ID** | TC-003 |
| **Module** | Authentication — Sign Up |
| **Description** | Passwords don't match |
| **Input** | Password: "Pass@123", Confirm: "Pass@456" |
| **Expected Output** | Error: "Passwords do not match." |
| **Status** | PASS |

### TC-004: Password Too Short
| Field | Value |
|---|---|
| **Test ID** | TC-004 |
| **Module** | Authentication — Sign Up |
| **Description** | Password has fewer than 6 characters |
| **Input** | Password: "abc", Confirm: "abc" |
| **Expected Output** | Error: "Password must be at least 6 characters." |
| **Status** | PASS |

### TC-005: Valid Login
| Field | Value |
|---|---|
| **Test ID** | TC-005 |
| **Module** | Authentication — Login |
| **Description** | Successful login with correct credentials |
| **Precondition** | User "johndoe" is registered |
| **Input** | Username: "johndoe", Password: "Pass@123" |
| **Expected Output** | Dashboard loads with user's name displayed |
| **Status** | PASS |

### TC-006: Invalid Login Credentials
| Field | Value |
|---|---|
| **Test ID** | TC-006 |
| **Module** | Authentication — Login |
| **Description** | Login with wrong password |
| **Input** | Username: "johndoe", Password: "wrongpass" |
| **Expected Output** | Error: "Invalid username or password." |
| **Status** | PASS |

### TC-007: Login with Empty Fields
| Field | Value |
|---|---|
| **Test ID** | TC-007 |
| **Module** | Authentication — Login |
| **Description** | Submit login form with empty fields |
| **Input** | Username: "", Password: "" |
| **Expected Output** | Warning: "Please fill in all fields." |
| **Status** | PASS |

### TC-008: Forgot Password — Valid Email
| Field | Value |
|---|---|
| **Test ID** | TC-008 |
| **Module** | Forgot Password |
| **Description** | Verify email shows security question |
| **Precondition** | User registered with email "john@example.com" |
| **Input** | Email: "john@example.com" |
| **Expected Output** | Security question displayed in Step 2 |
| **Status** | PASS |

### TC-009: Forgot Password — Unknown Email
| Field | Value |
|---|---|
| **Test ID** | TC-009 |
| **Module** | Forgot Password |
| **Description** | Verify email with non-existent account |
| **Input** | Email: "nobody@nowhere.com" |
| **Expected Output** | Error: "No account found with that email." |
| **Status** | PASS |

### TC-010: Forgot Password — Wrong Security Answer
| Field | Value |
|---|---|
| **Test ID** | TC-010 |
| **Module** | Forgot Password |
| **Description** | Provide wrong answer to security question |
| **Input** | Correct email, wrong security answer |
| **Expected Output** | Error: "Security answer is incorrect." |
| **Status** | PASS |

### TC-011: Forgot Password — Successful Reset
| Field | Value |
|---|---|
| **Test ID** | TC-011 |
| **Module** | Forgot Password |
| **Description** | Successfully reset password |
| **Input** | Correct email, correct answer, new password "NewPass@123" |
| **Expected Output** | Success message; redirect to login |
| **Status** | PASS |

---

## Module 2: Income Management

### TC-012: Add Income — Valid Data
| Field | Value |
|---|---|
| **Test ID** | TC-012 |
| **Module** | Income |
| **Description** | Add a valid income transaction |
| **Input** | Amount: 5000, Category: Salary, Description: "Monthly salary", Date: 2025-03-01 |
| **Expected Output** | Transaction appears in income list; totals updated |
| **Status** | PASS |

### TC-013: Add Income — Zero Amount
| Field | Value |
|---|---|
| **Test ID** | TC-013 |
| **Module** | Income |
| **Description** | Attempt to add income with zero amount |
| **Input** | Amount: 0 |
| **Expected Output** | Error: "Amount must be a positive number." |
| **Status** | PASS |

### TC-014: Add Income — Negative Amount
| Field | Value |
|---|---|
| **Test ID** | TC-014 |
| **Module** | Income |
| **Description** | Attempt to add income with negative amount |
| **Input** | Amount: -500 |
| **Expected Output** | Error: "Amount must be a positive number." |
| **Status** | PASS |

### TC-015: Add Income — Non-Numeric Amount
| Field | Value |
|---|---|
| **Test ID** | TC-015 |
| **Module** | Income |
| **Description** | Text entered in amount field |
| **Input** | Amount: "abc" |
| **Expected Output** | Error: "Amount must be a positive number." |
| **Status** | PASS |

### TC-016: Edit Income Transaction
| Field | Value |
|---|---|
| **Test ID** | TC-016 |
| **Module** | Income |
| **Description** | Edit an existing income transaction |
| **Precondition** | At least one income transaction exists |
| **Input** | Click edit icon, change amount to 5500 |
| **Expected Output** | Transaction updated; list refreshes with new amount |
| **Status** | PASS |

### TC-017: Delete Income Transaction
| Field | Value |
|---|---|
| **Test ID** | TC-017 |
| **Module** | Income |
| **Description** | Delete an existing income transaction |
| **Input** | Click delete icon, confirm deletion |
| **Expected Output** | Transaction removed from list; totals updated |
| **Status** | PASS |

---

## Module 3: Expense Management

### TC-018: Add Expense — Valid Data
| Field | Value |
|---|---|
| **Test ID** | TC-018 |
| **Module** | Expense |
| **Description** | Add a valid expense transaction |
| **Input** | Amount: 250.50, Category: Food & Dining, Description: "Groceries", Date: 2025-03-05 |
| **Expected Output** | Transaction in expense list; totals updated |
| **Status** | PASS |

### TC-019: Add Expense — Missing Required Fields
| Field | Value |
|---|---|
| **Test ID** | TC-019 |
| **Module** | Expense |
| **Description** | Attempt to add expense without required fields |
| **Input** | Amount: (blank), Category: selected, Date: (blank) |
| **Expected Output** | Warning: "Amount, Category, Date required." |
| **Status** | PASS |

### TC-020: Filter Expenses by Date Range
| Field | Value |
|---|---|
| **Test ID** | TC-020 |
| **Module** | Expense |
| **Description** | Filter transactions within a date range |
| **Input** | From: 2025-03-01, To: 2025-03-31 |
| **Expected Output** | Only March 2025 expenses displayed |
| **Status** | PASS |

### TC-021: Filter Expenses by Category
| Field | Value |
|---|---|
| **Test ID** | TC-021 |
| **Module** | Expense |
| **Description** | Filter by a specific category |
| **Input** | Category: "Food & Dining" |
| **Expected Output** | Only food transactions shown |
| **Status** | PASS |

---

## Module 4: Category Management

### TC-022: Add New Category
| Field | Value |
|---|---|
| **Test ID** | TC-022 |
| **Module** | Categories |
| **Description** | Create a new income category |
| **Input** | Name: "Bonus", Type: income, Icon: 🎉, Color: #FF9900 |
| **Expected Output** | Category appears in income categories list |
| **Status** | PASS |

### TC-023: Add Category — Empty Name
| Field | Value |
|---|---|
| **Test ID** | TC-023 |
| **Module** | Categories |
| **Description** | Attempt to save category without a name |
| **Input** | Name: (blank) |
| **Expected Output** | Warning: "Category name required." |
| **Status** | PASS |

### TC-024: Edit Category
| Field | Value |
|---|---|
| **Test ID** | TC-024 |
| **Module** | Categories |
| **Description** | Edit an existing category's name and color |
| **Input** | New Name: "Groceries", New Color: #00CC66 |
| **Expected Output** | Category updated in list |
| **Status** | PASS |

### TC-025: Delete Category with Transactions
| Field | Value |
|---|---|
| **Test ID** | TC-025 |
| **Module** | Categories |
| **Description** | Delete category that has linked transactions |
| **Input** | Delete "Food & Dining" |
| **Expected Output** | Category deleted; existing transactions remain with NULL category |
| **Status** | PASS |

---

## Module 5: Reports

### TC-026: Load Monthly Bar Chart
| Field | Value |
|---|---|
| **Test ID** | TC-026 |
| **Module** | Reports |
| **Description** | Display monthly income vs expense chart |
| **Input** | Year: 2025, Chart: Monthly |
| **Expected Output** | Bar chart renders with 12 month groups |
| **Status** | PASS |

### TC-027: Load Income Pie Chart
| Field | Value |
|---|---|
| **Test ID** | TC-027 |
| **Module** | Reports |
| **Description** | Show income breakdown by category |
| **Input** | Year: 2025, Chart: Income Pie |
| **Expected Output** | Pie chart renders with category slices and percentages |
| **Status** | PASS |

### TC-028: Pie Chart with No Data
| Field | Value |
|---|---|
| **Test ID** | TC-028 |
| **Module** | Reports |
| **Description** | Pie chart when no data exists for selected year |
| **Input** | Year: 2030 (no data) |
| **Expected Output** | "No data" message shown in chart area |
| **Status** | PASS |

### TC-029: Profit/Loss Trend Chart
| Field | Value |
|---|---|
| **Test ID** | TC-029 |
| **Module** | Reports |
| **Description** | Display trend line with profit/loss fill |
| **Input** | Year: 2025, Chart: Trend |
| **Expected Output** | Line chart with green (profit) and red (loss) fills |
| **Status** | PASS |

---

## Module 6: PDF Export

### TC-030: Export PDF Without Password
| Field | Value |
|---|---|
| **Test ID** | TC-030 |
| **Module** | PDF Export |
| **Description** | Export transactions to PDF without password protection |
| **Input** | Password fields left blank, valid save path |
| **Expected Output** | PDF file created; opens without password |
| **Status** | PASS |

### TC-031: Export PDF With Password
| Field | Value |
|---|---|
| **Test ID** | TC-031 |
| **Module** | PDF Export |
| **Description** | Export with password protection |
| **Input** | Password: "Secret@123", Confirm: "Secret@123" |
| **Expected Output** | PDF created; requires password to open |
| **Status** | PASS |

### TC-032: Export PDF — Password Mismatch
| Field | Value |
|---|---|
| **Test ID** | TC-032 |
| **Module** | PDF Export |
| **Description** | Passwords don't match in export dialog |
| **Input** | Password: "abc123", Confirm: "xyz789" |
| **Expected Output** | Error: "Passwords don't match." |
| **Status** | PASS |

---

## Module 7: Profile

### TC-033: Update Profile Info
| Field | Value |
|---|---|
| **Test ID** | TC-033 |
| **Module** | Profile |
| **Description** | Update full name and phone number |
| **Input** | Full Name: "Jane Smith", Phone: "9876543210" |
| **Expected Output** | Profile updated; sidebar greeting updates |
| **Status** | PASS |

### TC-034: Change Password — Correct Current Password
| Field | Value |
|---|---|
| **Test ID** | TC-034 |
| **Module** | Profile |
| **Description** | Change password with correct current password |
| **Input** | Current: "Pass@123", New: "NewPass@456", Confirm: "NewPass@456" |
| **Expected Output** | Password changed; success message shown |
| **Status** | PASS |

### TC-035: Change Password — Wrong Current Password
| Field | Value |
|---|---|
| **Test ID** | TC-035 |
| **Module** | Profile |
| **Description** | Enter wrong current password |
| **Input** | Current: "wrong", New: "NewPass@456", Confirm: "NewPass@456" |
| **Expected Output** | Error: "Current password is incorrect." |
| **Status** | PASS |

---

## Module 8: Settings

### TC-036: Change Theme to Dark
| Field | Value |
|---|---|
| **Test ID** | TC-036 |
| **Module** | Settings |
| **Description** | Switch UI theme to dark mode |
| **Input** | Theme: Dark, Save |
| **Expected Output** | UI background changes to dark; settings persisted |
| **Status** | PASS |

### TC-037: Change Currency
| Field | Value |
|---|---|
| **Test ID** | TC-037 |
| **Module** | Settings |
| **Description** | Change display currency to INR |
| **Input** | Currency: INR, Save |
| **Expected Output** | All amounts now display with ₹ symbol |
| **Status** | PASS |

### TC-038: Set Budget Limit
| Field | Value |
|---|---|
| **Test ID** | TC-038 |
| **Module** | Settings |
| **Description** | Set a monthly budget limit |
| **Input** | Budget Limit: 3000, Save |
| **Expected Output** | Setting saved; persists across sessions |
| **Status** | PASS |

---

## Summary

| Module | Total Tests | Pass | Fail |
|---|---|---|---|
| Authentication | 11 | 11 | 0 |
| Income Management | 6 | 6 | 0 |
| Expense Management | 4 | 4 | 0 |
| Categories | 4 | 4 | 0 |
| Reports | 4 | 4 | 0 |
| PDF Export | 3 | 3 | 0 |
| Profile | 3 | 3 | 0 |
| Settings | 3 | 3 | 0 |
| **Total** | **38** | **38** | **0** |
