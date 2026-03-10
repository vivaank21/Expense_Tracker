"""
auth_window.py - Login, Signup, and Forgot Password screens
"""
import tkinter as tk
from tkinter import ttk, messagebox
import database as db

SECURITY_QUESTIONS = [
    "What was the name of your first pet?",
    "What is your mother's maiden name?",
    "What city were you born in?",
    "What was the name of your elementary school?",
    "What is your oldest sibling's middle name?",
    "What was the make of your first car?",
]

# ── Colour palette ────────────────────────────────────────────────────────────
BG        = "#0F172A"
CARD      = "#1E293B"
ACCENT    = "#6366F1"
ACCENT2   = "#818CF8"
SUCCESS   = "#22C55E"
DANGER    = "#EF4444"
TEXT      = "#F1F5F9"
SUBTEXT   = "#94A3B8"
BORDER    = "#334155"
ENTRY_BG  = "#0F172A"


def styled_entry(parent, show=None, width=30):
    e = tk.Entry(parent, bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
                 relief="flat", font=("Segoe UI", 11),
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT, width=width)
    if show:
        e.config(show=show)
    return e


def styled_btn(parent, text, command, color=ACCENT, fg=TEXT, width=20):
    return tk.Button(parent, text=text, command=command,
                     bg=color, fg=fg, font=("Segoe UI", 10, "bold"),
                     relief="flat", cursor="hand2",
                     activebackground=ACCENT2, activeforeground=TEXT,
                     padx=10, pady=8, width=width)


def label(parent, text, size=11, color=TEXT, bold=False):
    font = ("Segoe UI", size, "bold") if bold else ("Segoe UI", size)
    return tk.Label(parent, text=text, bg=CARD, fg=color, font=font)


# ─────────────────────────────────────────────────────────────────────────────
class AuthWindow:
    def __init__(self, on_login_success):
        self.on_login_success = on_login_success
        self.root = tk.Tk()
        self.root.title("Expense Tracker Pro - Login")
        self.root.geometry("480x600")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self._center()
        self._show_login()
        self.root.mainloop()

    def _center(self):
        self.root.update_idletasks()
        w = self.root.winfo_width() or 480
        h = self.root.winfo_height() or 600
        x = (self.root.winfo_screenwidth()  // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"+{x}+{y}")

    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ── LOGIN ────────────────────────────────────────────────────────────────
    def _show_login(self):
        self._clear()
        self.root.title("Expense Tracker Pro - Login")

        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=40, pady=30)

        # Header
        tk.Label(outer, text="💰", font=("Segoe UI", 40), bg=BG, fg=ACCENT).pack(pady=(10, 0))
        tk.Label(outer, text="Expense Tracker Pro",
                 font=("Segoe UI", 18, "bold"), bg=BG, fg=TEXT).pack()
        tk.Label(outer, text="Sign in to your account",
                 font=("Segoe UI", 10), bg=BG, fg=SUBTEXT).pack(pady=(2, 20))

        card = tk.Frame(outer, bg=CARD, highlightthickness=1,
                        highlightbackground=BORDER)
        card.pack(fill="x", pady=5)

        inner = tk.Frame(card, bg=CARD)
        inner.pack(padx=30, pady=30, fill="x")

        label(inner, "Username", 10, SUBTEXT).pack(anchor="w")
        self.login_user = styled_entry(inner)
        self.login_user.pack(fill="x", pady=(2, 12))

        label(inner, "Password", 10, SUBTEXT).pack(anchor="w")
        pw_frame = tk.Frame(inner, bg=CARD)
        pw_frame.pack(fill="x", pady=(2, 4))
        self.login_pw = styled_entry(pw_frame, show="•")
        self.login_pw.pack(side="left", fill="x", expand=True)
        self._show_pw = False

        def toggle_pw():
            self._show_pw = not self._show_pw
            self.login_pw.config(show="" if self._show_pw else "•")
            eye_btn.config(text="🙈" if self._show_pw else "👁")
        eye_btn = tk.Button(pw_frame, text="👁", command=toggle_pw,
                            bg=CARD, fg=SUBTEXT, relief="flat",
                            font=("Segoe UI", 12), cursor="hand2",
                            activebackground=CARD, borderwidth=0)
        eye_btn.pack(side="right", padx=2)

        tk.Button(inner, text="Forgot Password?", command=self._show_forgot,
                  bg=CARD, fg=ACCENT2, relief="flat", font=("Segoe UI", 9),
                  cursor="hand2", activebackground=CARD).pack(anchor="e", pady=4)

        styled_btn(inner, "Sign In", self._do_login, width=30).pack(fill="x", pady=8)

        sep = tk.Frame(inner, bg=BORDER, height=1)
        sep.pack(fill="x", pady=8)

        reg_frame = tk.Frame(inner, bg=CARD)
        reg_frame.pack()
        tk.Label(reg_frame, text="Don't have an account? ",
                 bg=CARD, fg=SUBTEXT, font=("Segoe UI", 9)).pack(side="left")
        tk.Button(reg_frame, text="Create one", command=self._show_signup,
                  bg=CARD, fg=ACCENT2, relief="flat", font=("Segoe UI", 9, "bold"),
                  cursor="hand2", activebackground=CARD).pack(side="left")

        self.login_user.focus()
        self.root.bind("<Return>", lambda e: self._do_login())

    def _do_login(self):
        username = self.login_user.get().strip()
        password = self.login_pw.get()
        if not username or not password:
            messagebox.showwarning("Missing Fields", "Please fill in all fields.", parent=self.root)
            return
        user = db.login_user(username, password)
        if user:
            self.root.destroy()
            self.on_login_success(user)
        else:
            messagebox.showerror("Login Failed",
                                 "Invalid username or password.", parent=self.root)

    # ── SIGNUP ───────────────────────────────────────────────────────────────
    def _show_signup(self):
        self._clear()
        self.root.title("Expense Tracker Pro - Sign Up")
        self.root.geometry("500x720")
        self._center()

        canvas = tk.Canvas(self.root, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        outer = tk.Frame(canvas, bg=BG)
        canvas_window = canvas.create_window((0, 0), window=outer, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        outer.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        pad = tk.Frame(outer, bg=BG)
        pad.pack(padx=40, pady=20, fill="x")

        tk.Label(pad, text="💰", font=("Segoe UI", 32), bg=BG, fg=ACCENT).pack()
        tk.Label(pad, text="Create Account", font=("Segoe UI", 17, "bold"),
                 bg=BG, fg=TEXT).pack()
        tk.Label(pad, text="Fill in your details below",
                 font=("Segoe UI", 9), bg=BG, fg=SUBTEXT).pack(pady=(2, 15))

        card = tk.Frame(pad, bg=CARD, highlightthickness=1,
                        highlightbackground=BORDER)
        card.pack(fill="x")
        inner = tk.Frame(card, bg=CARD)
        inner.pack(padx=28, pady=28, fill="x")

        fields = {}
        defs = [
            ("Full Name *", "full_name", None),
            ("Username *",  "username",  None),
            ("Email *",     "email",     None),
            ("Phone",       "phone",     None),
            ("Password *",  "password",  "•"),
            ("Confirm Password *", "confirm", "•"),
        ]
        for lbl_text, key, show in defs:
            label(inner, lbl_text, 10, SUBTEXT).pack(anchor="w")
            e = styled_entry(inner, show=show)
            e.pack(fill="x", pady=(2, 10))
            fields[key] = e

        label(inner, "Security Question *", 10, SUBTEXT).pack(anchor="w")
        self.sq_var = tk.StringVar(value=SECURITY_QUESTIONS[0])
        sq_combo = ttk.Combobox(inner, textvariable=self.sq_var,
                                values=SECURITY_QUESTIONS,
                                state="readonly", font=("Segoe UI", 10))
        sq_combo.pack(fill="x", pady=(2, 10))

        label(inner, "Answer *", 10, SUBTEXT).pack(anchor="w")
        fields["answer"] = styled_entry(inner)
        fields["answer"].pack(fill="x", pady=(2, 10))

        self.signup_fields = fields

        styled_btn(inner, "Create Account", self._do_signup, width=30).pack(fill="x", pady=8)

        back_f = tk.Frame(inner, bg=CARD)
        back_f.pack()
        tk.Label(back_f, text="Already have an account? ",
                 bg=CARD, fg=SUBTEXT, font=("Segoe UI", 9)).pack(side="left")
        tk.Button(back_f, text="Sign In", command=self._show_login,
                  bg=CARD, fg=ACCENT2, relief="flat", font=("Segoe UI", 9, "bold"),
                  cursor="hand2", activebackground=CARD).pack(side="left")

    def _do_signup(self):
        f = self.signup_fields
        full_name = f["full_name"].get().strip()
        username  = f["username"].get().strip()
        email     = f["email"].get().strip()
        phone     = f["phone"].get().strip()
        password  = f["password"].get()
        confirm   = f["confirm"].get()
        question  = self.sq_var.get()
        answer    = f["answer"].get().strip()

        if not all([full_name, username, email, password, confirm, answer]):
            messagebox.showwarning("Missing Fields",
                                   "Please fill in all required fields (*).", parent=self.root)
            return
        if len(password) < 6:
            messagebox.showerror("Weak Password",
                                 "Password must be at least 6 characters.", parent=self.root)
            return
        if password != confirm:
            messagebox.showerror("Password Mismatch",
                                 "Passwords do not match.", parent=self.root)
            return
        if "@" not in email:
            messagebox.showerror("Invalid Email",
                                 "Please enter a valid email address.", parent=self.root)
            return

        ok, msg = db.register_user(username, email, password, full_name,
                                   phone, question, answer)
        if ok:
            messagebox.showinfo("Success", f"{msg}\nYou can now log in.", parent=self.root)
            self._show_login()
        else:
            messagebox.showerror("Registration Failed", msg, parent=self.root)

    # ── FORGOT PASSWORD ──────────────────────────────────────────────────────
    def _show_forgot(self):
        self._clear()
        self.root.title("Expense Tracker Pro - Forgot Password")
        self.root.geometry("480x560")
        self._center()

        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(outer, text="🔐", font=("Segoe UI", 40), bg=BG, fg=ACCENT).pack()
        tk.Label(outer, text="Reset Password", font=("Segoe UI", 17, "bold"),
                 bg=BG, fg=TEXT).pack()
        tk.Label(outer, text="We'll verify your identity first",
                 font=("Segoe UI", 9), bg=BG, fg=SUBTEXT).pack(pady=(2, 15))

        card = tk.Frame(outer, bg=CARD, highlightthickness=1,
                        highlightbackground=BORDER)
        card.pack(fill="x")
        inner = tk.Frame(card, bg=CARD)
        inner.pack(padx=28, pady=28, fill="x")

        # Step 1 – Enter email
        self.fp_step1 = tk.Frame(inner, bg=CARD)
        self.fp_step1.pack(fill="x")
        label(self.fp_step1, "Registered Email *", 10, SUBTEXT).pack(anchor="w")
        self.fp_email = styled_entry(self.fp_step1)
        self.fp_email.pack(fill="x", pady=(2, 12))
        styled_btn(self.fp_step1, "Verify Email", self._verify_email, width=30).pack(fill="x")

        # Step 2 – Answer security question (hidden initially)
        self.fp_step2 = tk.Frame(inner, bg=CARD)
        self.fp_q_label   = label(self.fp_step2, "", 10, SUBTEXT)
        self.fp_q_label.pack(anchor="w")
        self.fp_answer = styled_entry(self.fp_step2)
        self.fp_answer.pack(fill="x", pady=(2, 12))
        label(self.fp_step2, "New Password *", 10, SUBTEXT).pack(anchor="w")
        self.fp_new_pw = styled_entry(self.fp_step2, show="•")
        self.fp_new_pw.pack(fill="x", pady=(2, 12))
        label(self.fp_step2, "Confirm Password *", 10, SUBTEXT).pack(anchor="w")
        self.fp_confirm = styled_entry(self.fp_step2, show="•")
        self.fp_confirm.pack(fill="x", pady=(2, 12))
        styled_btn(self.fp_step2, "Reset Password", self._do_reset, width=30).pack(fill="x")

        sep = tk.Frame(inner, bg=BORDER, height=1)
        sep.pack(fill="x", pady=12)
        tk.Button(inner, text="← Back to Login", command=self._show_login,
                  bg=CARD, fg=ACCENT2, relief="flat", font=("Segoe UI", 10),
                  cursor="hand2", activebackground=CARD).pack()

    def _verify_email(self):
        email = self.fp_email.get().strip()
        if not email:
            messagebox.showwarning("Missing", "Please enter your email.", parent=self.root)
            return
        q = db.get_security_question(email)
        if not q:
            messagebox.showerror("Not Found",
                                 "No account found with that email.", parent=self.root)
            return
        self.fp_email_val = email
        self.fp_q_label.config(text=f"Security Question: {q}")
        self.fp_step2.pack(fill="x", pady=(16, 0))

    def _do_reset(self):
        answer  = self.fp_answer.get().strip()
        new_pw  = self.fp_new_pw.get()
        confirm = self.fp_confirm.get()
        if not answer or not new_pw or not confirm:
            messagebox.showwarning("Missing Fields",
                                   "Please fill in all fields.", parent=self.root)
            return
        if new_pw != confirm:
            messagebox.showerror("Mismatch", "Passwords do not match.", parent=self.root)
            return
        if len(new_pw) < 6:
            messagebox.showerror("Weak Password",
                                 "Password must be at least 6 characters.", parent=self.root)
            return
        ok, msg = db.reset_password_via_security(self.fp_email_val, answer, new_pw)
        if ok:
            messagebox.showinfo("Success", f"{msg}\nYou can now log in.", parent=self.root)
            self._show_login()
        else:
            messagebox.showerror("Failed", msg, parent=self.root)
