import tkinter as tk
from tkinter import messagebox, ttk


class PhishingEmailWindow:
    def __init__(self, parent, attack_callback):
        self.top = tk.Toplevel(parent)
        self.top.title("Outlook Mail - Urgent Message")
        self.top.geometry("600x420")
        self.top.resizable(False, False)
        self.top.configure(bg="#f3f3f3")
        self.attack_callback = attack_callback

        # Make this window stay on top
        self.top.transient(parent)
        self.top.grab_set()

        self.setup_ui()

    def setup_ui(self):
        # Top Bar
        top_bar = tk.Frame(self.top, bg="#0078d4", height=40)
        top_bar.pack(fill="x")
        lbl_title = tk.Label(
            top_bar,
            text="  Inbox - (1) Unread Message",
            font=("Segoe UI", 11, "bold"),
            bg="#0078d4",
            fg="white",
        )
        lbl_title.pack(side="left", padx=10, pady=5)

        # Email Body Frame
        body_frame = tk.Frame(self.top, bg="white", padx=20, pady=15)
        body_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Headers
        lbl_from = tk.Label(
            body_frame,
            text="From: Finance Department <billing@urgent-invoice-service.com>",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            anchor="w",
        )
        lbl_from.pack(fill="x", pady=2)

        lbl_to = tk.Label(
            body_frame,
            text="To: user@company-internal.com",
            font=("Segoe UI", 9),
            fg="#555555",
            bg="white",
            anchor="w",
        )
        lbl_to.pack(fill="x", pady=2)

        lbl_sub = tk.Label(
            body_frame,
            text="Subject:  URGENT: Pending Invoice Payment Overdue",
            font=("Segoe UI", 11, "bold"),
            fg="#d9534f",
            bg="white",
            anchor="w",
        )
        lbl_sub.pack(fill="x", pady=8)

        ttk.Separator(body_frame, orient="horizontal").pack(fill="x", pady=5)

        # Email Text
        email_msg = (
            "Dear User,\n\n"
            "We noticed an unpaid invoice associated with your account. "
            "Failure to process payment within 24 hours will result in legal action and account suspension.\n\n"
            "Please download and review the attached invoice document immediately."
        )
        lbl_body = tk.Label(
            body_frame,
            text=email_msg,
            font=("Segoe UI", 10),
            bg="white",
            justify="left",
            wraplength=530,
        )
        lbl_body.pack(fill="x", pady=10)

        # Attachment Box
        attach_frame = tk.Frame(
            body_frame, bg="#f0f4f8", relief="groove", bd=1, padx=10, pady=8
        )
        attach_frame.pack(fill="x", pady=10)

        lbl_attach_icon = tk.Label(
            attach_frame,
            text=" Attachment:",
            font=("Segoe UI", 9, "bold"),
            bg="#f0f4f8",
        )
        lbl_attach_icon.pack(side="left", padx=5)

        btn_payload = tk.Button(
            attach_frame,
            text=" Invoice_Payment_Details.pdf.exe",
            font=("Segoe UI", 9, "bold"),
            bg="#d9534f",
            fg="white",
            activebackground="#c9302c",
            activeforeground="white",
            cursor="hand2",
            command=self.execute_attack,
        )
        btn_payload.pack(side="left", padx=10)

    def execute_attack(self):
        confirm = messagebox.askyesno(
            "Phishing Attack Simulation",
            " You are about to open a malicious attachment!\n\nSimulate launching Ransomware?",
            parent=self.top,
        )
        if confirm:
            self.top.destroy()
            if self.attack_callback:
                self.attack_callback()

def show_attack_options(parent, direct_attack_callback):
    """Pop-up option window when user clicks Attack Button"""
    opt_win = tk.Toplevel(parent)
    opt_win.title("Select Attack Vector")
    opt_win.geometry("380x200")
    opt_win.resizable(False, False)
    opt_win.transient(parent)
    opt_win.grab_set()

    lbl = tk.Label(
        opt_win,
        text=" Choose How To Launch Attack:",
        font=("Segoe UI", 11, "bold"),
        pady=15,
    )
    lbl.pack()

    def choose_phishing():
        opt_win.destroy()
        # ဒီနေရာမှာ attack_callback= direct_attack_callback ဆိုပြီး တိုက်ရိုက် ညွှန်းပေးလိုက်ပါတယ်
        PhishingEmailWindow(parent, attack_callback=direct_attack_callback)

    def choose_direct():
        opt_win.destroy()
        direct_attack_callback()

    btn_p = tk.Button(
        opt_win,
        text=" 1. Phishing Email Attack (Interactive)",
        font=("Segoe UI", 10, "bold"),
        bg="#0078d4",
        fg="white",
        pady=5,
        command=choose_phishing,
    )
    btn_p.pack(fill="x", padx=20, pady=5)

    btn_d = tk.Button(
        opt_win,
        text=" 2. Direct Execution (Quick Test)",
        font=("Segoe UI", 10),
        bg="#e0e0e0",
        pady=5,
        command=choose_direct,
    )
    btn_d.pack(fill="x", padx=20, pady=5)