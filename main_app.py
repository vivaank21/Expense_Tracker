"""
main_app.py - Main Expense Tracker Application Window
"""
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog
from datetime import datetime, date, timedelta
import calendar
import os
import database as db

# ── Theme colours ─────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg": "#0F172A", "sidebar": "#1E293B", "card": "#1E293B",
        "card2": "#263044", "text": "#F1F5F9", "subtext": "#94A3B8",
        "border": "#334155", "entry_bg": "#0F172A",
        "income_clr": "#22C55E", "expense_clr": "#EF4444",
    },
    "light": {
        "bg": "#F8FAFC", "sidebar": "#1E293B", "card": "#FFFFFF",
        "card2": "#F1F5F9", "text": "#0F172A", "subtext": "#64748B",
        "border": "#E2E8F0", "entry_bg": "#F8FAFC",
        "income_clr": "#16A34A", "expense_clr": "#DC2626",
    }
}
ACCENT  = "#6366F1"
ACCENT2 = "#818CF8"

CURRENCIES = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹",
              "JPY": "¥", "CAD": "CA₹", "AUD": "A₹", "CHF": "CHF "}
MONTHS = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]


class ExpenseTrackerApp:
    def __init__(self, user: dict):
        self.user     = user
        self.user_id  = user["id"]
        self.settings = db.get_settings(self.user_id)
        self.theme    = THEMES.get(self.settings.get("theme", "dark"), THEMES["dark"])
        self.currency_code = self.settings.get("currency", "USD")
        self.currency_sym  = CURRENCIES.get(self.currency_code, "₹")
        self.current_page  = None

        self.root = tk.Tk()
        self.root.title("Expense Tracker Pro")
        self.root.geometry("1200x750")
        self.root.minsize(900, 600)
        self.root.configure(bg=self.theme["bg"])
        self._center()

        self._build_layout()
        self._nav("dashboard")
        self.root.mainloop()

    def _center(self):
        self.root.update_idletasks()
        w, h = 1200, 750
        x = (self.root.winfo_screenwidth()  // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ── LAYOUT ────────────────────────────────────────────────────────────────
    def _build_layout(self):
        T = self.theme

        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=T["sidebar"], width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand
        brand = tk.Frame(self.sidebar, bg=T["sidebar"])
        brand.pack(fill="x", pady=20, padx=15)
        tk.Label(brand, text="💰 ET Pro", font=("Segoe UI", 16, "bold"),
                 bg=T["sidebar"], fg="#F1F5F9").pack(anchor="w")
        user_name = self.user.get("full_name", "User").split()[0]
        tk.Label(brand, text=f"Hello, {user_name}",
                 font=("Segoe UI", 10), bg=T["sidebar"], fg="#94A3B8").pack(anchor="w")

        sep = tk.Frame(self.sidebar, bg="#334155", height=1)
        sep.pack(fill="x", padx=15, pady=5)

        # Nav items
        self.nav_btns = {}
        nav_items = [
            ("dashboard",    "🏠 Dashboard"),
            ("income",       "💵 Income"),
            ("expense",      "💸 Expenses"),
            ("categories",   "🏷️  Categories"),
            ("reports",      "📊 Reports"),
            ("profile",      "👤 Profile"),
            ("settings",     "⚙️  Settings"),
        ]
        self.nav_frame = tk.Frame(self.sidebar, bg=T["sidebar"])
        self.nav_frame.pack(fill="x", padx=10, pady=5)

        for key, label in nav_items:
            btn = tk.Button(
                self.nav_frame, text=label, anchor="w",
                font=("Segoe UI", 11), relief="flat", cursor="hand2",
                bg=T["sidebar"], fg="#94A3B8",
                activebackground=ACCENT, activeforeground="white",
                padx=15, pady=10,
                command=lambda k=key: self._nav(k)
            )
            btn.pack(fill="x", pady=2)
            self.nav_btns[key] = btn

        # Logout
        tk.Frame(self.sidebar, bg="#334155", height=1).pack(fill="x", padx=15, pady=10)
        tk.Button(self.sidebar, text="🚪 Logout", anchor="w",
                  font=("Segoe UI", 11), relief="flat", cursor="hand2",
                  bg=T["sidebar"], fg="#EF4444",
                  activebackground="#7F1D1D", activeforeground="white",
                  padx=25, pady=10, command=self._logout).pack(fill="x", padx=10)

        # Main content
        self.content = tk.Frame(self.root, bg=T["bg"])
        self.content.pack(side="left", fill="both", expand=True)

    def _nav(self, page):
        T = self.theme
        for k, btn in self.nav_btns.items():
            if k == page:
                btn.config(bg=ACCENT, fg="white")
            else:
                btn.config(bg=T["sidebar"], fg="#94A3B8")
        self.current_page = page
        for w in self.content.winfo_children():
            w.destroy()
        pages = {
            "dashboard":  self._page_dashboard,
            "income":     lambda: self._page_transactions("income"),
            "expense":    lambda: self._page_transactions("expense"),
            "categories": self._page_categories,
            "reports":    self._page_reports,
            "profile":    self._page_profile,
            "settings":   self._page_settings,
        }
        pages.get(page, self._page_dashboard)()

    def _logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?",
                               parent=self.root):
            self.root.destroy()
            import auth_window
            from database import initialize_db
            initialize_db()
            def on_login(u):
                ExpenseTrackerApp(u)
            auth_window.AuthWindow(on_login)

    # ── HELPER WIDGETS ────────────────────────────────────────────────────────
    def _page_header(self, parent, title, subtitle=""):
        T = self.theme
        hdr = tk.Frame(parent, bg=T["bg"])
        hdr.pack(fill="x", padx=25, pady=(20, 10))
        tk.Label(hdr, text=title, font=("Segoe UI", 20, "bold"),
                 bg=T["bg"], fg=T["text"]).pack(anchor="w")
        if subtitle:
            tk.Label(hdr, text=subtitle, font=("Segoe UI", 10),
                     bg=T["bg"], fg=T["subtext"]).pack(anchor="w")
        tk.Frame(parent, bg=T["border"], height=1).pack(fill="x", padx=25, pady=5)

    def _card(self, parent, **kwargs):
        T = self.theme
        c = tk.Frame(parent, bg=T["card"], highlightthickness=1,
                     highlightbackground=T["border"], **kwargs)
        return c

    def _stat_card(self, parent, title, value, icon, color):
        T = self.theme
        f = tk.Frame(parent, bg=T["card"], highlightthickness=1,
                     highlightbackground=T["border"])
        f.pack(side="left", fill="both", expand=True, padx=6, pady=4)
        inner = tk.Frame(f, bg=T["card"])
        inner.pack(padx=16, pady=14, fill="x")
        top = tk.Frame(inner, bg=T["card"])
        top.pack(fill="x")
        tk.Label(top, text=icon, font=("Segoe UI", 22),
                 bg=T["card"], fg=color).pack(side="left")
        tk.Label(top, text=title, font=("Segoe UI", 10),
                 bg=T["card"], fg=T["subtext"]).pack(side="right")
        tk.Label(inner, text=value, font=("Segoe UI", 17, "bold"),
                 bg=T["card"], fg=color).pack(anchor="w", pady=(4, 0))

    def _entry(self, parent, show=None, width=None):
        T = self.theme
        kw = dict(bg=T["entry_bg"], fg=T["text"], insertbackground=T["text"],
                  relief="flat", font=("Segoe UI", 11),
                  highlightthickness=1, highlightbackground=T["border"],
                  highlightcolor=ACCENT)
        if show:
            kw["show"] = show
        if width:
            kw["width"] = width
        return tk.Entry(parent, **kw)

    def _btn(self, parent, text, cmd, color=ACCENT, fg="white", **kw):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg=fg, font=("Segoe UI", 10, "bold"),
                         relief="flat", cursor="hand2",
                         activebackground=ACCENT2, activeforeground="white",
                         padx=10, pady=7, **kw)

    def _fmt_amount(self, amount):
        return f"{self.currency_sym}{amount:,.2f}"

    # ══════════════════════════════════════════════════════════════════════════
    # DASHBOARD
    # ══════════════════════════════════════════════════════════════════════════
    def _page_dashboard(self):
        T = self.theme
        parent = self.content
        self._page_header(parent, "Dashboard",
                          f"Welcome back, {self.user['full_name']}!")

        scroll_canvas = tk.Canvas(parent, bg=T["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical",
                                  command=scroll_canvas.yview)
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        scroll_canvas.pack(fill="both", expand=True)

        body = tk.Frame(scroll_canvas, bg=T["bg"])
        win = scroll_canvas.create_window((0, 0), window=body, anchor="nw")

        def on_configure(e):
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        def on_canvas_resize(e):
            scroll_canvas.itemconfig(win, width=e.width)
        body.bind("<Configure>", on_configure)
        scroll_canvas.bind("<Configure>", on_canvas_resize)

        # Summary cards
        summary = db.get_summary(self.user_id)
        cards_row = tk.Frame(body, bg=T["bg"])
        cards_row.pack(fill="x", padx=19, pady=8)
        self._stat_card(cards_row, "Total Income",
                        self._fmt_amount(summary["income"]),
                        "💵", T["income_clr"])
        self._stat_card(cards_row, "Total Expense",
                        self._fmt_amount(summary["expense"]),
                        "💸", T["expense_clr"])
        balance = summary["balance"]
        bal_clr = T["income_clr"] if balance >= 0 else T["expense_clr"]
        self._stat_card(cards_row, "Net Balance",
                        self._fmt_amount(balance), "💰", bal_clr)

        # This month stats
        today = date.today()
        m_start = f"{today.year}-{today.month:02d}-01"
        m_end   = f"{today.year}-{today.month:02d}-{calendar.monthrange(today.year, today.month)[1]:02d}"
        m_sum   = db.get_summary(self.user_id, m_start, m_end)

        cards_row2 = tk.Frame(body, bg=T["bg"])
        cards_row2.pack(fill="x", padx=19, pady=4)
        self._stat_card(cards_row2, f"{MONTHS[today.month-1]} Income",
                        self._fmt_amount(m_sum["income"]), "📈", T["income_clr"])
        self._stat_card(cards_row2, f"{MONTHS[today.month-1]} Expense",
                        self._fmt_amount(m_sum["expense"]), "📉", T["expense_clr"])
        m_bal = m_sum["balance"]
        m_clr = T["income_clr"] if m_bal >= 0 else T["expense_clr"]
        self._stat_card(cards_row2, "Monthly Balance",
                        self._fmt_amount(m_bal), "🏦", m_clr)

        # Quick-add buttons
        qa = tk.Frame(body, bg=T["bg"])
        qa.pack(fill="x", padx=25, pady=8)
        self._btn(qa, "＋ Add Income",
                  lambda: self._add_transaction_dialog("income"),
                  color=T["income_clr"]).pack(side="left", padx=(0, 8))
        self._btn(qa, "－ Add Expense",
                  lambda: self._add_transaction_dialog("expense"),
                  color=T["expense_clr"]).pack(side="left")
        self._btn(qa, "📊 View Reports",
                  lambda: self._nav("reports"),
                  color="#7C3AED").pack(side="right")

        # Recent transactions
        tk.Frame(body, bg=T["border"], height=1).pack(fill="x", padx=25, pady=8)
        lbl_row = tk.Frame(body, bg=T["bg"])
        lbl_row.pack(fill="x", padx=25, pady=(0, 6))
        tk.Label(lbl_row, text="Recent Transactions",
                 font=("Segoe UI", 13, "bold"),
                 bg=T["bg"], fg=T["text"]).pack(side="left")
        tk.Button(lbl_row, text="View All →",
                  command=lambda: self._nav("expense"),
                  bg=T["bg"], fg=ACCENT2, relief="flat",
                  font=("Segoe UI", 9), cursor="hand2").pack(side="right")

        recent = db.get_transactions(self.user_id, limit=10)
        if not recent:
            tk.Label(body, text="No transactions yet. Add your first one!",
                     font=("Segoe UI", 11), bg=T["bg"], fg=T["subtext"]).pack(pady=20)
        else:
            tx_frame = self._card(body)
            tx_frame.pack(fill="x", padx=25, pady=4)
            self._render_tx_list(tx_frame, recent, compact=True)

    # ══════════════════════════════════════════════════════════════════════════
    # TRANSACTIONS PAGE (Income / Expense)
    # ══════════════════════════════════════════════════════════════════════════
    def _page_transactions(self, tx_type):
        T = self.theme
        parent = self.content
        title = "Income" if tx_type == "income" else "Expenses"
        self._page_header(parent, f"{'💵' if tx_type=='income' else '💸'} {title}")

        # Toolbar
        toolbar = tk.Frame(parent, bg=T["bg"])
        toolbar.pack(fill="x", padx=25, pady=6)

        add_color = T["income_clr"] if tx_type == "income" else T["expense_clr"]
        self._btn(toolbar, f"＋ Add {title[:-1]}",
                  lambda: self._add_transaction_dialog(tx_type),
                  color=add_color).pack(side="left")
        self._btn(toolbar, "📥 Export PDF",
                  lambda: self._export_pdf(tx_type),
                  color="#7C3AED").pack(side="left", padx=8)

        # Filter bar
        filter_bar = self._card(parent)
        filter_bar.pack(fill="x", padx=25, pady=4)
        fb = tk.Frame(filter_bar, bg=T["card"])
        fb.pack(padx=12, pady=10, fill="x")

        tk.Label(fb, text="From:", bg=T["card"], fg=T["subtext"],
                 font=("Segoe UI", 10)).pack(side="left", padx=4)
        self.filter_from = self._entry(fb, width=12)
        self.filter_from.insert(0, f"{date.today().year}-01-01")
        self.filter_from.pack(side="left", padx=4)

        tk.Label(fb, text="To:", bg=T["card"], fg=T["subtext"],
                 font=("Segoe UI", 10)).pack(side="left", padx=4)
        self.filter_to = self._entry(fb, width=12)
        self.filter_to.insert(0, str(date.today()))
        self.filter_to.pack(side="left", padx=4)

        cats = db.get_categories(self.user_id, tx_type)
        cat_options = ["All Categories"] + [c["name"] for c in cats]
        self.filter_cat_var = tk.StringVar(value="All Categories")
        cat_combo = ttk.Combobox(fb, textvariable=self.filter_cat_var,
                                 values=cat_options, state="readonly",
                                 width=18, font=("Segoe UI", 10))
        cat_combo.pack(side="left", padx=8)

        def apply_filter():
            self._load_transactions(tx_list_frame, tx_type)
        self._btn(fb, "🔍 Filter", apply_filter, color=ACCENT).pack(side="left", padx=4)
        self._btn(fb, "↺ Reset", lambda: self._reset_filter(tx_type, tx_list_frame),
                  color=T["card2"]).pack(side="left", padx=4)

        # Summary row
        self.tx_summary_frame = tk.Frame(parent, bg=T["bg"])
        self.tx_summary_frame.pack(fill="x", padx=25, pady=4)

        # Transactions list
        tx_list_frame = tk.Frame(parent, bg=T["bg"])
        tx_list_frame.pack(fill="both", expand=True, padx=25, pady=4)
        self._load_transactions(tx_list_frame, tx_type)

    def _reset_filter(self, tx_type, frame):
        self.filter_from.delete(0, "end")
        self.filter_from.insert(0, f"{date.today().year}-01-01")
        self.filter_to.delete(0, "end")
        self.filter_to.insert(0, str(date.today()))
        self.filter_cat_var.set("All Categories")
        self._load_transactions(frame, tx_type)

    def _load_transactions(self, frame, tx_type):
        T = self.theme
        for w in frame.winfo_children():
            w.destroy()
        for w in self.tx_summary_frame.winfo_children():
            w.destroy()

        start = self.filter_from.get().strip() or None
        end   = self.filter_to.get().strip() or None
        cat_name = self.filter_cat_var.get()
        cat_id   = None
        if cat_name != "All Categories":
            cats = db.get_categories(self.user_id, tx_type)
            for c in cats:
                if c["name"] == cat_name:
                    cat_id = c["id"]
                    break

        txs     = db.get_transactions(self.user_id, tx_type, start, end, cat_id)
        summary = db.get_summary(self.user_id, start, end)

        # Summary row
        clr = T["income_clr"] if tx_type == "income" else T["expense_clr"]
        val = summary["income"] if tx_type == "income" else summary["expense"]
        tk.Label(self.tx_summary_frame,
                 text=f"Total: {self._fmt_amount(val)}  |  {len(txs)} transactions",
                 font=("Segoe UI", 11, "bold"),
                 bg=T["bg"], fg=clr).pack(anchor="w")

        if not txs:
            self._card(frame).pack(fill="x", pady=4)
            tk.Label(frame, text="No transactions found.",
                     font=("Segoe UI", 11), bg=T["bg"], fg=T["subtext"]).pack(pady=30)
            return

        # Scrollable list
        canvas = tk.Canvas(frame, bg=T["bg"], highlightthickness=0)
        vsb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        inner = tk.Frame(canvas, bg=T["bg"])
        cwin = canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_cfg(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def on_canvas_cfg(e):
            canvas.itemconfig(cwin, width=e.width)
        inner.bind("<Configure>", on_cfg)
        canvas.bind("<Configure>", on_canvas_cfg)

        card = self._card(inner)
        card.pack(fill="x", pady=4)
        self._render_tx_list(card, txs, tx_type=tx_type, compact=False)

    def _render_tx_list(self, parent, txs, tx_type=None, compact=False):
        T = self.theme
        # Header
        hdr = tk.Frame(parent, bg=T["card2"])
        hdr.pack(fill="x")
        cols = [("Date", 100), ("Category", 130), ("Description", 0),
                ("Amount", 110), ("Actions", 100)] if not compact else \
               [("Date", 90), ("Type", 80), ("Category", 120),
                ("Description", 0), ("Amount", 110)]
        for col_name, col_w in cols:
            anchor = "e" if col_name == "Amount" else "w"
            kw = dict(text=col_name, font=("Segoe UI", 9, "bold"),
                      bg=T["card2"], fg=T["subtext"], pady=8, padx=8)
            if col_w:
                lbl = tk.Label(hdr, width=col_w//8, anchor=anchor, **kw)
                lbl.pack(side="left")
            else:
                lbl = tk.Label(hdr, anchor=anchor, **kw)
                lbl.pack(side="left", expand=True, fill="x")

        for i, tx in enumerate(txs):
            row_bg = T["card"] if i % 2 == 0 else T["card2"]
            row = tk.Frame(parent, bg=row_bg, cursor="hand2")
            row.pack(fill="x")

            t_type = tx.get("type", tx_type or "expense")
            clr = T["income_clr"] if t_type == "income" else T["expense_clr"]
            icon = tx.get("icon") or ("💵" if t_type == "income" else "💸")
            cat  = tx.get("category_name") or "Uncategorized"

            if not compact:
                tk.Label(row, text=tx["date"][:10], font=("Segoe UI", 10),
                         bg=row_bg, fg=T["text"], pady=9, padx=8,
                         width=12, anchor="w").pack(side="left")
                tk.Label(row, text=f"{icon} {cat}", font=("Segoe UI", 10),
                         bg=row_bg, fg=T["text"], padx=8,
                         width=16, anchor="w").pack(side="left")
                tk.Label(row, text=tx.get("description") or "—",
                         font=("Segoe UI", 10), bg=row_bg, fg=T["subtext"],
                         padx=8, anchor="w").pack(side="left", fill="x", expand=True)
                tk.Label(row, text=self._fmt_amount(tx["amount"]),
                         font=("Segoe UI", 10, "bold"), bg=row_bg, fg=clr,
                         padx=8, width=14, anchor="e").pack(side="left")
                act = tk.Frame(row, bg=row_bg)
                act.pack(side="right", padx=6)
                tk.Button(act, text="✏️", relief="flat", bg=row_bg, fg=T["text"],
                          cursor="hand2", font=("Segoe UI", 11),
                          command=lambda t=tx: self._edit_transaction_dialog(t)
                          ).pack(side="left", padx=2)
                tk.Button(act, text="🗑️", relief="flat", bg=row_bg, fg="#EF4444",
                          cursor="hand2", font=("Segoe UI", 11),
                          command=lambda t=tx: self._delete_transaction(t)
                          ).pack(side="left", padx=2)
            else:
                tk.Label(row, text=tx["date"][:10], font=("Segoe UI", 9),
                         bg=row_bg, fg=T["subtext"], pady=9, padx=8,
                         width=11, anchor="w").pack(side="left")
                type_clr = T["income_clr"] if t_type == "income" else T["expense_clr"]
                tk.Label(row, text=t_type.capitalize(), font=("Segoe UI", 9),
                         bg=row_bg, fg=type_clr, width=8, anchor="w",
                         padx=4).pack(side="left")
                tk.Label(row, text=f"{icon} {cat}", font=("Segoe UI", 9),
                         bg=row_bg, fg=T["text"], width=16,
                         anchor="w", padx=4).pack(side="left")
                tk.Label(row, text=tx.get("description") or "—",
                         font=("Segoe UI", 9), bg=row_bg, fg=T["subtext"],
                         padx=4, anchor="w").pack(side="left", fill="x", expand=True)
                prefix = "+" if t_type == "income" else "-"
                tk.Label(row, text=f"{prefix}{self._fmt_amount(tx['amount'])}",
                         font=("Segoe UI", 9, "bold"), bg=row_bg, fg=clr,
                         padx=8, width=14, anchor="e").pack(side="right")

        tk.Frame(parent, bg=T["border"], height=1).pack(fill="x")

    # ── ADD / EDIT TRANSACTION DIALOG ─────────────────────────────────────────
    def _add_transaction_dialog(self, tx_type, prefill=None):
        T = self.theme
        dlg = tk.Toplevel(self.root)
        dlg.title(f"{'Add' if not prefill else 'Edit'} {tx_type.capitalize()}")
        dlg.geometry("480x520")
        dlg.resizable(False, False)
        dlg.configure(bg=T["bg"])
        dlg.grab_set()
        dlg.transient(self.root)

        outer = tk.Frame(dlg, bg=T["bg"])
        outer.pack(fill="both", expand=True, padx=28, pady=22)

        icon = "💵" if tx_type == "income" else "💸"
        tk.Label(outer, text=f"{icon} {'Add' if not prefill else 'Edit'} {tx_type.capitalize()}",
                 font=("Segoe UI", 15, "bold"), bg=T["bg"], fg=T["text"]).pack(anchor="w", pady=(0,12))

        def lbl(text):
            tk.Label(outer, text=text, font=("Segoe UI", 10),
                     bg=T["bg"], fg=T["subtext"]).pack(anchor="w")

        lbl("Amount *")
        amt_entry = self._entry(outer)
        amt_entry.pack(fill="x", pady=(2, 10))

        lbl("Category *")
        cats = db.get_categories(self.user_id, tx_type)
        cat_names = [f"{c['icon']} {c['name']}" for c in cats]
        cat_var = tk.StringVar(value=cat_names[0] if cat_names else "")
        cat_combo = ttk.Combobox(outer, textvariable=cat_var, values=cat_names,
                                 state="readonly", font=("Segoe UI", 11))
        cat_combo.pack(fill="x", pady=(2, 10))

        lbl("Description")
        desc_entry = self._entry(outer)
        desc_entry.pack(fill="x", pady=(2, 10))

        lbl("Date *")
        date_entry = self._entry(outer)
        date_entry.insert(0, str(date.today()))
        date_entry.pack(fill="x", pady=(2, 10))

        lbl("Notes (optional)")
        notes_text = tk.Text(outer, height=3, bg=T["entry_bg"], fg=T["text"],
                             font=("Segoe UI", 10), relief="flat",
                             insertbackground=T["text"],
                             highlightthickness=1, highlightbackground=T["border"])
        notes_text.pack(fill="x", pady=(2, 14))

        # Prefill for edit
        if prefill:
            amt_entry.insert(0, str(prefill["amount"]))
            desc_entry.insert(0, prefill.get("description") or "")
            date_entry.delete(0, "end")
            date_entry.insert(0, prefill["date"][:10])
            notes_text.insert("1.0", prefill.get("notes") or "")
            pcat = prefill.get("category_name") or ""
            for cn in cat_names:
                if pcat in cn:
                    cat_var.set(cn)
                    break

        def save():
            amt_str = amt_entry.get().strip()
            cat_sel = cat_var.get()
            desc    = desc_entry.get().strip()
            dt      = date_entry.get().strip()
            notes   = notes_text.get("1.0", "end").strip()

            if not amt_str or not cat_sel or not dt:
                messagebox.showwarning("Missing", "Amount, Category, Date required.",
                                       parent=dlg)
                return
            try:
                amt = float(amt_str)
                if amt <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid", "Amount must be a positive number.",
                                     parent=dlg)
                return

            # Find cat_id
            cat_id = None
            sel_name = cat_sel.split(" ", 1)[-1] if " " in cat_sel else cat_sel
            for c in cats:
                if c["name"] == sel_name:
                    cat_id = c["id"]
                    break

            if prefill:
                db.update_transaction(prefill["id"], cat_id, amt, desc, dt, notes)
                messagebox.showinfo("Updated", "Transaction updated.", parent=dlg)
            else:
                db.add_transaction(self.user_id, cat_id, tx_type, amt, desc, dt, notes)
                messagebox.showinfo("Saved", "Transaction added.", parent=dlg)
            dlg.destroy()
            self._nav(self.current_page)

        btn_row = tk.Frame(outer, bg=T["bg"])
        btn_row.pack(fill="x")
        clr = T["income_clr"] if tx_type == "income" else T["expense_clr"]
        self._btn(btn_row, "💾 Save", save, color=clr).pack(side="left")
        self._btn(btn_row, "Cancel", dlg.destroy,
                  color=T["card2"]).pack(side="left", padx=8)

    def _edit_transaction_dialog(self, tx):
        self._add_transaction_dialog(tx["type"], prefill=tx)

    def _delete_transaction(self, tx):
        if messagebox.askyesno("Delete", "Delete this transaction?",
                               parent=self.root):
            db.delete_transaction(tx["id"])
            self._nav(self.current_page)

    # ══════════════════════════════════════════════════════════════════════════
    # CATEGORIES
    # ══════════════════════════════════════════════════════════════════════════
    def _page_categories(self):
        T = self.theme
        parent = self.content
        self._page_header(parent, "🏷️ Categories", "Manage your income & expense categories")

        tab_frame = tk.Frame(parent, bg=T["bg"])
        tab_frame.pack(fill="x", padx=25, pady=6)

        self.cat_type_var = tk.StringVar(value="income")
        for val, label in [("income", "💵 Income"), ("expense", "💸 Expense")]:
            btn = tk.Radiobutton(tab_frame, text=label, variable=self.cat_type_var,
                                 value=val, command=lambda: self._load_categories(cat_list_frame),
                                 bg=T["bg"], fg=T["text"], selectcolor=ACCENT,
                                 font=("Segoe UI", 11), cursor="hand2",
                                 indicatoron=False, padx=16, pady=6,
                                 relief="flat", activebackground=ACCENT,
                                 activeforeground="white")
            btn.pack(side="left", padx=4)

        toolbar = tk.Frame(parent, bg=T["bg"])
        toolbar.pack(fill="x", padx=25, pady=4)
        self._btn(toolbar, "＋ Add Category",
                  lambda: self._add_category_dialog(),
                  color=ACCENT).pack(side="left")

        cat_list_frame = tk.Frame(parent, bg=T["bg"])
        cat_list_frame.pack(fill="both", expand=True, padx=25, pady=8)
        self._load_categories(cat_list_frame)

    def _load_categories(self, frame):
        T = self.theme
        for w in frame.winfo_children():
            w.destroy()
        cat_type = self.cat_type_var.get()
        cats = db.get_categories(self.user_id, cat_type)

        card = self._card(frame)
        card.pack(fill="both", expand=True)

        canvas = tk.Canvas(card, bg=T["card"], highlightthickness=0)
        vsb = ttk.Scrollbar(card, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        inner = tk.Frame(canvas, bg=T["card"])
        cwin = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cwin, width=e.width))

        if not cats:
            tk.Label(inner, text="No categories. Add one!",
                     font=("Segoe UI", 11), bg=T["card"], fg=T["subtext"]).pack(pady=30)
            return

        for i, cat in enumerate(cats):
            row_bg = T["card"] if i % 2 == 0 else T["card2"]
            row = tk.Frame(inner, bg=row_bg)
            row.pack(fill="x", padx=4)
            tk.Label(row, text=f"  {cat['icon']}  {cat['name']}",
                     font=("Segoe UI", 11), bg=row_bg, fg=T["text"],
                     pady=10, anchor="w").pack(side="left", fill="x", expand=True)
            color_box = tk.Label(row, text="  ", bg=cat["color"],
                                 width=3, relief="flat")
            color_box.pack(side="left", padx=8)
            tk.Button(row, text="✏️", relief="flat", bg=row_bg, cursor="hand2",
                      font=("Segoe UI", 11),
                      command=lambda c=cat: self._edit_category_dialog(c)
                      ).pack(side="left", padx=2)
            tk.Button(row, text="🗑️", relief="flat", bg=row_bg, fg="#EF4444",
                      cursor="hand2", font=("Segoe UI", 11),
                      command=lambda c=cat: self._delete_category(c)
                      ).pack(side="left", padx=(2, 8))
            tk.Frame(inner, bg=T["border"], height=1).pack(fill="x")

    def _add_category_dialog(self, prefill=None):
        T = self.theme
        dlg = tk.Toplevel(self.root)
        dlg.title("Add Category" if not prefill else "Edit Category")
        dlg.geometry("420x380")
        dlg.resizable(False, False)
        dlg.configure(bg=T["bg"])
        dlg.grab_set()
        dlg.transient(self.root)

        outer = tk.Frame(dlg, bg=T["bg"])
        outer.pack(fill="both", expand=True, padx=28, pady=22)

        def lbl(text):
            tk.Label(outer, text=text, font=("Segoe UI", 10),
                     bg=T["bg"], fg=T["subtext"]).pack(anchor="w")

        lbl("Name *")
        name_e = self._entry(outer)
        name_e.pack(fill="x", pady=(2, 10))

        lbl("Type *")
        type_var = tk.StringVar(value="expense")
        type_frame = tk.Frame(outer, bg=T["bg"])
        type_frame.pack(fill="x", pady=(2, 10))
        for val, label in [("income", "💵 Income"), ("expense", "💸 Expense")]:
            tk.Radiobutton(type_frame, text=label, variable=type_var, value=val,
                           bg=T["bg"], fg=T["text"], selectcolor=ACCENT,
                           font=("Segoe UI", 10), cursor="hand2",
                           activebackground=T["bg"]).pack(side="left", padx=8)

        lbl("Icon (emoji)")
        icon_e = self._entry(outer, width=5)
        icon_e.insert(0, "💰")
        icon_e.pack(fill="x", pady=(2, 10))

        lbl("Color")
        color_var = tk.StringVar(value="#4A90D9")
        color_frame = tk.Frame(outer, bg=T["bg"])
        color_frame.pack(fill="x", pady=(2, 14))
        color_preview = tk.Label(color_frame, bg="#4A90D9", width=4, relief="flat")
        color_preview.pack(side="left", padx=(0, 8))
        def pick_color():
            c = colorchooser.askcolor(color=color_var.get(), parent=dlg)
            if c[1]:
                color_var.set(c[1])
                color_preview.config(bg=c[1])
        self._btn(color_frame, "Pick Color", pick_color,
                  color=T["card2"]).pack(side="left")

        if prefill:
            name_e.insert(0, prefill["name"])
            type_var.set(prefill["type"])
            icon_e.delete(0, "end")
            icon_e.insert(0, prefill["icon"])
            color_var.set(prefill["color"])
            color_preview.config(bg=prefill["color"])

        def save():
            name  = name_e.get().strip()
            ctype = type_var.get()
            icon  = icon_e.get().strip() or "💰"
            color = color_var.get()
            if not name:
                messagebox.showwarning("Missing", "Category name required.", parent=dlg)
                return
            if prefill:
                db.update_category(prefill["id"], name, color, icon)
            else:
                db.add_category(self.user_id, name, ctype, color, icon)
            dlg.destroy()
            self._nav("categories")

        btn_row = tk.Frame(outer, bg=T["bg"])
        btn_row.pack(fill="x")
        self._btn(btn_row, "💾 Save", save).pack(side="left")
        self._btn(btn_row, "Cancel", dlg.destroy, color=T["card2"]).pack(side="left", padx=8)

    def _edit_category_dialog(self, cat):
        self._add_category_dialog(prefill=cat)

    def _delete_category(self, cat):
        if messagebox.askyesno("Delete",
                               f"Delete '{cat['name']}'? Transactions in this category will remain.",
                               parent=self.root):
            db.delete_category(cat["id"])
            self._nav("categories")

    # ══════════════════════════════════════════════════════════════════════════
    # REPORTS
    # ══════════════════════════════════════════════════════════════════════════
    def _page_reports(self):
        import matplotlib
        matplotlib.use("TkAgg")
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import numpy as np

        T = self.theme
        parent = self.content
        self._page_header(parent, "📊 Reports & Analytics")

        # Controls
        ctrl = tk.Frame(parent, bg=T["bg"])
        ctrl.pack(fill="x", padx=25, pady=6)

        tk.Label(ctrl, text="Year:", bg=T["bg"], fg=T["subtext"],
                 font=("Segoe UI", 10)).pack(side="left")
        year_var = tk.StringVar(value=str(date.today().year))
        years = [str(y) for y in range(date.today().year, date.today().year - 5, -1)]
        ttk.Combobox(ctrl, textvariable=year_var, values=years,
                     state="readonly", width=8, font=("Segoe UI", 10)).pack(side="left", padx=8)

        # Chart tabs
        tab_var = tk.StringVar(value="monthly")
        for val, lbl_t in [("monthly", "📅 Monthly"), ("pie_inc", "🟢 Income Pie"),
                            ("pie_exp", "🔴 Expense Pie"), ("trend", "📈 Trend")]:
            tk.Radiobutton(ctrl, text=lbl_t, variable=tab_var, value=val,
                           bg=T["bg"], fg=T["text"], selectcolor=ACCENT,
                           font=("Segoe UI", 10), cursor="hand2",
                           indicatoron=False, padx=12, pady=5,
                           relief="flat", activebackground=ACCENT,
                           activeforeground="white"
                           ).pack(side="left", padx=3)

        chart_frame = tk.Frame(parent, bg=T["bg"])
        chart_frame.pack(fill="both", expand=True, padx=25, pady=8)

        def draw_chart():
            for w in chart_frame.winfo_children():
                w.destroy()

            year = int(year_var.get())
            chart = tab_var.get()
            bg_hex = T["bg"]
            text_clr = T["text"]

            fig, ax = plt.subplots(figsize=(9, 4.5), facecolor=bg_hex)
            ax.set_facecolor(T["card"])

            if chart == "monthly":
                data = db.get_monthly_data(self.user_id, year)
                months_short = ["Jan","Feb","Mar","Apr","May","Jun",
                                "Jul","Aug","Sep","Oct","Nov","Dec"]
                x = np.arange(12)
                w = 0.35
                bars1 = ax.bar(x - w/2, data["income"], w,
                               label="Income", color="#22C55E", alpha=0.85)
                bars2 = ax.bar(x + w/2, data["expense"], w,
                               label="Expense", color="#EF4444", alpha=0.85)
                ax.set_xticks(x)
                ax.set_xticklabels(months_short, color=text_clr, fontsize=9)
                ax.set_title(f"Monthly Income vs Expense – {year}",
                             color=text_clr, fontsize=12, pad=10)
                ax.legend(facecolor=T["card"], edgecolor=T["border"], labelcolor=text_clr)

            elif chart in ("pie_inc", "pie_exp"):
                t = "income" if chart == "pie_inc" else "expense"
                breakdown = db.get_category_breakdown(self.user_id, t,
                                                      f"{year}-01-01", f"{year}-12-31")
                if not breakdown:
                    ax.text(0.5, 0.5, "No data", ha="center", va="center",
                            color=text_clr, fontsize=14)
                else:
                    labels = [f"{r['icon']} {r['name']}" for r in breakdown]
                    sizes  = [r["total"] for r in breakdown]
                    colors = [r["color"] or "#888" for r in breakdown]
                    wedges, texts, autotexts = ax.pie(
                        sizes, labels=labels, colors=colors,
                        autopct="%1.1f%%", startangle=90,
                        textprops={"color": text_clr, "fontsize": 8})
                    for at in autotexts:
                        at.set_color("white")
                    ax.set_title(
                        f"{'Income' if t=='income' else 'Expense'} Breakdown – {year}",
                        color=text_clr, fontsize=12)

            elif chart == "trend":
                data = db.get_monthly_data(self.user_id, year)
                months_short = ["Jan","Feb","Mar","Apr","May","Jun",
                                "Jul","Aug","Sep","Oct","Nov","Dec"]
                balance = [data["income"][i] - data["expense"][i] for i in range(12)]
                ax.plot(months_short, data["income"], marker="o", color="#22C55E",
                        label="Income", linewidth=2)
                ax.plot(months_short, data["expense"], marker="s", color="#EF4444",
                        label="Expense", linewidth=2)
                ax.fill_between(months_short, 0, balance,
                                where=[b >= 0 for b in balance],
                                alpha=0.2, color="#22C55E", label="Profit")
                ax.fill_between(months_short, 0, balance,
                                where=[b < 0 for b in balance],
                                alpha=0.2, color="#EF4444", label="Loss")
                ax.set_title(f"Profit / Loss Trend – {year}",
                             color=text_clr, fontsize=12)
                ax.legend(facecolor=T["card"], edgecolor=T["border"], labelcolor=text_clr)
                ax.tick_params(colors=text_clr)

            for spine in ax.spines.values():
                spine.set_edgecolor(T["border"])
            ax.tick_params(colors=text_clr, labelsize=9)
            ax.yaxis.label.set_color(text_clr)
            plt.tight_layout()

            canvas_widget = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas_widget.draw()
            canvas_widget.get_tk_widget().pack(fill="both", expand=True)
            plt.close(fig)

        draw_chart()
        self._btn(ctrl, "🔄 Refresh", draw_chart, color=ACCENT).pack(side="right")

    # ══════════════════════════════════════════════════════════════════════════
    # PROFILE
    # ══════════════════════════════════════════════════════════════════════════
    def _page_profile(self):
        T = self.theme
        parent = self.content
        self._page_header(parent, "👤 Profile", "Manage your account information")

        canvas = tk.Canvas(parent, bg=T["bg"], highlightthickness=0)
        vsb = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        body = tk.Frame(canvas, bg=T["bg"])
        win = canvas.create_window((0, 0), window=body, anchor="nw")
        body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))

        outer = tk.Frame(body, bg=T["bg"])
        outer.pack(padx=30, pady=10, fill="x")

        # Avatar section
        avatar_card = self._card(outer)
        avatar_card.pack(fill="x", pady=8)
        av_inner = tk.Frame(avatar_card, bg=T["card"])
        av_inner.pack(padx=24, pady=20, fill="x")

        initials = "".join(w[0].upper() for w in self.user["full_name"].split()[:2])
        av_circle = tk.Label(av_inner, text=initials,
                             font=("Segoe UI", 26, "bold"),
                             bg=ACCENT, fg="white", width=3, height=1,
                             relief="flat")
        av_circle.pack(side="left", padx=(0, 16))

        info = tk.Frame(av_inner, bg=T["card"])
        info.pack(side="left", fill="x", expand=True)
        tk.Label(info, text=self.user["full_name"],
                 font=("Segoe UI", 15, "bold"),
                 bg=T["card"], fg=T["text"]).pack(anchor="w")
        tk.Label(info, text=f"@{self.user['username']}",
                 font=("Segoe UI", 10),
                 bg=T["card"], fg=T["subtext"]).pack(anchor="w")
        tk.Label(info, text=f"Member since {self.user.get('created_at','')[:10]}",
                 font=("Segoe UI", 9),
                 bg=T["card"], fg=T["subtext"]).pack(anchor="w")

        # Edit profile form
        form_card = self._card(outer)
        form_card.pack(fill="x", pady=8)
        form = tk.Frame(form_card, bg=T["card"])
        form.pack(padx=24, pady=20, fill="x")

        tk.Label(form, text="Edit Profile", font=("Segoe UI", 12, "bold"),
                 bg=T["card"], fg=T["text"]).pack(anchor="w", pady=(0, 12))

        fields_data = [
            ("Full Name", "full_name"), ("Email", "email"), ("Phone", "phone"),
        ]
        entries = {}
        for lbl_t, key in fields_data:
            tk.Label(form, text=lbl_t, font=("Segoe UI", 10),
                     bg=T["card"], fg=T["subtext"]).pack(anchor="w")
            e = self._entry(form)
            e.insert(0, self.user.get(key) or "")
            e.pack(fill="x", pady=(2, 10))
            entries[key] = e

        def save_profile():
            ok, msg = db.update_user(
                self.user_id,
                entries["full_name"].get().strip(),
                entries["email"].get().strip(),
                entries["phone"].get().strip(),
                self.currency_code
            )
            if ok:
                self.user = db.get_user(self.user_id)
                messagebox.showinfo("Saved", msg, parent=self.root)
                self._nav("profile")
            else:
                messagebox.showerror("Error", msg, parent=self.root)

        self._btn(form, "💾 Save Profile", save_profile).pack(anchor="w", pady=4)

        # Change password
        pw_card = self._card(outer)
        pw_card.pack(fill="x", pady=8)
        pw_form = tk.Frame(pw_card, bg=T["card"])
        pw_form.pack(padx=24, pady=20, fill="x")

        tk.Label(pw_form, text="Change Password", font=("Segoe UI", 12, "bold"),
                 bg=T["card"], fg=T["text"]).pack(anchor="w", pady=(0, 12))
        pw_entries = {}
        for lbl_t, key in [("Current Password", "old"), ("New Password", "new"),
                            ("Confirm New Password", "confirm")]:
            tk.Label(pw_form, text=lbl_t, font=("Segoe UI", 10),
                     bg=T["card"], fg=T["subtext"]).pack(anchor="w")
            e = self._entry(pw_form, show="•")
            e.pack(fill="x", pady=(2, 10))
            pw_entries[key] = e

        def save_password():
            old = pw_entries["old"].get()
            new = pw_entries["new"].get()
            cnf = pw_entries["confirm"].get()
            if not old or not new or not cnf:
                messagebox.showwarning("Missing", "Fill in all fields.", parent=self.root)
                return
            if new != cnf:
                messagebox.showerror("Mismatch", "New passwords don't match.", parent=self.root)
                return
            if len(new) < 6:
                messagebox.showerror("Weak", "Password must be at least 6 chars.", parent=self.root)
                return
            ok, msg = db.change_password(self.user_id, old, new)
            if ok:
                messagebox.showinfo("Changed", msg, parent=self.root)
                for e in pw_entries.values():
                    e.delete(0, "end")
            else:
                messagebox.showerror("Error", msg, parent=self.root)

        self._btn(pw_form, "🔐 Change Password", save_password, color="#7C3AED").pack(anchor="w")

    # ══════════════════════════════════════════════════════════════════════════
    # SETTINGS
    # ══════════════════════════════════════════════════════════════════════════
    def _page_settings(self):
        T = self.theme
        parent = self.content
        self._page_header(parent, "⚙️ Settings", "Configure your preferences")

        settings = db.get_settings(self.user_id)

        canvas = tk.Canvas(parent, bg=T["bg"], highlightthickness=0)
        vsb = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        body = tk.Frame(canvas, bg=T["bg"])
        win = canvas.create_window((0, 0), window=body, anchor="nw")
        body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))

        outer = tk.Frame(body, bg=T["bg"])
        outer.pack(padx=30, pady=10, fill="x")

        def section(title):
            f = self._card(outer)
            f.pack(fill="x", pady=8)
            inner = tk.Frame(f, bg=T["card"])
            inner.pack(padx=24, pady=20, fill="x")
            tk.Label(inner, text=title, font=("Segoe UI", 12, "bold"),
                     bg=T["card"], fg=T["text"]).pack(anchor="w", pady=(0, 12))
            return inner

        def row(parent, label_text):
            r = tk.Frame(parent, bg=T["card"])
            r.pack(fill="x", pady=5)

            tk.Label(
                r,
                text=label_text,
                font=("Segoe UI", 10),
                bg=T["card"],
                fg=T["subtext"],
                width=20,
                anchor="w"
            ).pack(side="left")

            widget_parent = tk.Frame(r, bg=T["card"])
            widget_parent.pack(side="left", fill="x", expand=True)

            return widget_parent

        # Appearance
        app_sec = section("🎨 Appearance")
        theme_var = tk.StringVar(value=settings.get("theme", "dark"))
        wp = row(app_sec, "Theme:")
        for val, lbl_t in [("dark", "🌙 Dark"), ("light", "☀️ Light")]:
            tk.Radiobutton(wp, text=lbl_t, variable=theme_var, value=val,
                           bg=T["card"], fg=T["text"], selectcolor=ACCENT,
                           font=("Segoe UI", 10), cursor="hand2",
                           activebackground=T["card"]).pack(side="left", padx=8)

        # Currency
        curr_sec = section("💰 Currency & Format")
        curr_var = tk.StringVar(value=settings.get("currency", "USD"))
        wp2 = row(curr_sec, "Currency:")
        ttk.Combobox(wp2, textvariable=curr_var,
                     values=list(CURRENCIES.keys()),
                     state="readonly", width=12,
                     font=("Segoe UI", 10)).pack(side="left")

        date_fmt_var = tk.StringVar(value=settings.get("date_format", "%Y-%m-%d"))
        wp3 = row(curr_sec, "Date Format:")
        ttk.Combobox(wp3, textvariable=date_fmt_var,
                     values=["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"],
                     state="readonly", width=14,
                     font=("Segoe UI", 10)).pack(side="left")

        # Budget
        bud_sec = section("📊 Budget")
        budget_limit_var = tk.StringVar(value=str(settings.get("budget_limit", 0)))
        wp4 = row(bud_sec, "Monthly Budget Limit:")
        e_bud = self._entry(wp4, width=16)
        e_bud.insert(0, budget_limit_var.get())
        e_bud.pack(side="left")

        notif_var = tk.BooleanVar(value=bool(settings.get("notifications", 1)))
        wp5 = row(bud_sec, "Budget Alerts:")
        tk.Checkbutton(wp5, text="Enable alerts when over budget",
                       variable=notif_var,
                       bg=T["card"], fg=T["text"], selectcolor=ACCENT,
                       font=("Segoe UI", 10), activebackground=T["card"],
                       cursor="hand2").pack(side="left")

        def save_settings():
            try:
                budget = float(e_bud.get() or 0)
            except ValueError:
                budget = 0
            db.update_settings(self.user_id, theme_var.get(), curr_var.get(),
                               date_fmt_var.get(), notif_var.get(), budget)
            self.settings = db.get_settings(self.user_id)
            self.theme = THEMES.get(theme_var.get(), THEMES["dark"])
            self.currency_code = curr_var.get()
            self.currency_sym  = CURRENCIES.get(self.currency_code, "₹")
            messagebox.showinfo("Saved", "Settings saved successfully!", parent=self.root)
            self.root.configure(bg=self.theme["bg"])
            self._nav("settings")

        self._btn(outer, "💾 Save Settings", save_settings,
                  color=ACCENT).pack(anchor="w", padx=6, pady=8)

    # ══════════════════════════════════════════════════════════════════════════
    # PDF EXPORT
    # ══════════════════════════════════════════════════════════════════════════
    def _export_pdf(self, tx_type=None):
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                        Table, TableStyle, HRFlowable)
        from reportlab.lib.units import cm
        from pypdf import PdfReader, PdfWriter
        import tempfile, io

        # Ask for password
        dlg = tk.Toplevel(self.root)
        dlg.title("Export PDF")
        dlg.geometry("380x220")
        dlg.resizable(False, False)
        dlg.configure(bg=self.theme["bg"])
        dlg.grab_set()
        dlg.transient(self.root)

        T = self.theme
        outer = tk.Frame(dlg, bg=T["bg"])
        outer.pack(fill="both", expand=True, padx=24, pady=20)
        tk.Label(outer, text="📥 Export Transaction History",
                 font=("Segoe UI", 12, "bold"), bg=T["bg"], fg=T["text"]).pack(anchor="w")
        tk.Label(outer, text="Set a PDF password (optional):",
                 font=("Segoe UI", 10), bg=T["bg"], fg=T["subtext"]).pack(anchor="w", pady=(8,2))
        pw_e = self._entry(outer, show="•")
        pw_e.pack(fill="x", pady=(0, 8))
        tk.Label(outer, text="Confirm password:",
                 font=("Segoe UI", 10), bg=T["bg"], fg=T["subtext"]).pack(anchor="w")
        pw_confirm = self._entry(outer, show="•")
        pw_confirm.pack(fill="x", pady=(0, 12))

        def do_export():
            pw1 = pw_e.get()
            pw2 = pw_confirm.get()
            if pw1 and pw1 != pw2:
                messagebox.showerror("Mismatch", "Passwords don't match.", parent=dlg)
                return
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile="transactions.pdf",
                parent=dlg)
            if not filepath:
                return
            dlg.destroy()
            self._generate_pdf(filepath, tx_type, pw1 if pw1 else None)

        self._btn(outer, "📥 Export", do_export).pack(side="left")
        self._btn(outer, "Cancel", dlg.destroy,
                  color=T["card2"]).pack(side="left", padx=8)

    def _generate_pdf(self, filepath, tx_type, password):
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                        Table, TableStyle, HRFlowable)
        from reportlab.lib.units import cm
        from pypdf import PdfReader, PdfWriter
        import tempfile, io

        W, H = A4
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        tmp.close()

        doc = SimpleDocTemplate(tmp.name, pagesize=A4,
                                leftMargin=2*cm, rightMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle("Title2", parent=styles["Title"],
                                     textColor=colors.HexColor("#6366F1"),
                                     fontSize=20, spaceAfter=6)
        story.append(Paragraph("💰 Expense Tracker Pro", title_style))
        story.append(Paragraph(
            f"Transaction Report – {self.user['full_name']}",
            styles["Heading2"]))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["Normal"]))
        story.append(HRFlowable(width="100%", thickness=1,
                                 color=colors.HexColor("#6366F1"), spaceAfter=12))

        # Summary
        summary = db.get_summary(self.user_id)
        sum_data = [
            ["Metric", "Amount"],
            ["Total Income", f"{self.currency_sym}{summary['income']:,.2f}"],
            ["Total Expense", f"{self.currency_sym}{summary['expense']:,.2f}"],
            ["Net Balance", f"{self.currency_sym}{summary['balance']:,.2f}"],
        ]
        sum_table = Table(sum_data, colWidths=[8*cm, 6*cm])
        sum_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#6366F1")),
            ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0,1), (-1,-1),
             [colors.HexColor("#F1F5F9"), colors.white]),
            ("ALIGN",  (1,0), (1,-1), "RIGHT"),
            ("GRID",   (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ("ROWHEIGHT", (0,0), (-1,-1), 20),
            ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"),
        ]))
        story.append(sum_table)
        story.append(Spacer(1, 0.5*cm))

        # Transactions table
        story.append(Paragraph(
            f"{'All' if not tx_type else tx_type.capitalize()} Transactions",
            styles["Heading3"]))
        txs = db.get_transactions(self.user_id, tx_type)

        tx_data = [["Date", "Type", "Category", "Description", "Amount"]]
        for tx in txs:
            tx_data.append([
                tx["date"][:10],
                tx["type"].capitalize(),
                tx.get("category_name") or "—",
                (tx.get("description") or "")[:35],
                f"{self.currency_sym}{tx['amount']:,.2f}",
            ])

        if len(tx_data) > 1:
            col_w = [2.8*cm, 2*cm, 3.5*cm, 5.5*cm, 3*cm]
            tx_table = Table(tx_data, colWidths=col_w, repeatRows=1)
            row_colors = []
            for i in range(1, len(tx_data)):
                clr = colors.HexColor("#E8F5E9") if tx_data[i][1] == "Income" \
                      else colors.HexColor("#FFEBEE")
                row_colors.append(("BACKGROUND", (0,i), (-1,i), clr))
            tx_table.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#334155")),
                ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
                ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
                ("FONTSIZE",   (0,0), (-1,-1), 8),
                ("ALIGN",  (4,0), (4,-1), "RIGHT"),
                ("GRID",   (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
                ("ROWHEIGHT", (0,0), (-1,-1), 18),
            ] + row_colors))
            story.append(tx_table)
        else:
            story.append(Paragraph("No transactions found.", styles["Normal"]))

        doc.build(story)

        if password:
            reader = PdfReader(tmp.name)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(password, password)
            with open(filepath, "wb") as f:
                writer.write(f)
            os.unlink(tmp.name)
        else:
            import shutil
            shutil.move(tmp.name, filepath)

        messagebox.showinfo("Exported",
                            f"PDF saved to:\n{filepath}" +
                            ("\n\nThis file is password protected." if password else ""),
                            parent=self.root)
