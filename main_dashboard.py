import os
import subprocess
import json
import tkinter as tk
from tkinter import messagebox

#  Dashboard စပွင့်ချင်း Background က Defender Process အဟောင်းများကို အလိုအလျောက် အမြစ်ပြတ် ရှင်းလင်းမည်
os.system("pkill -9 -f defender_detector.py > /dev/null 2>&1")

root = tk.Tk()
root.title(" Enterprise Ransomware Defense & SOC Monitor")
root.geometry("850x630")
root.configure(bg="#0f172a")

defender_process = None

# Title Bar
title_frame = tk.Frame(root, bg="#1e293b", pady=10)
title_frame.pack(fill="x")

title = tk.Label(
    title_frame, 
    text=" CANARY-BASED REAL-TIME RANSOMWARE DEFENSE SYSTEM", 
    font=("Arial", 14, "bold"), 
    fg="#38bdf8", 
    bg="#1e293b"
)
title.pack()

# Visual Status Cards Frame
card_frame = tk.Frame(root, bg="#0f172a", pady=15)
card_frame.pack(fill="x", padx=20)

# Card 1: Engine Status
status_card = tk.Frame(card_frame, bg="#1e293b", bd=1, relief="solid", padx=15, pady=12)
status_card.pack(side="left", expand=True, fill="x", padx=5)
lbl_status_title = tk.Label(status_card, text="DEFENSE ENGINE", font=("Arial", 9, "bold"), fg="#94a3b8", bg="#1e293b")
lbl_status_title.pack()
lbl_status_val = tk.Label(status_card, text="STANDBY (OFF)", font=("Arial", 12, "bold"), fg="#f59e0b", bg="#1e293b")
lbl_status_val.pack()

# Card 2: Canary File Status
canary_card = tk.Frame(card_frame, bg="#1e293b", bd=1, relief="solid", padx=15, pady=12)
canary_card.pack(side="left", expand=True, fill="x", padx=5)
lbl_canary_title = tk.Label(canary_card, text="CANARY INTEGRITY", font=("Arial", 9, "bold"), fg="#94a3b8", bg="#1e293b")
lbl_canary_title.pack()
lbl_canary_val = tk.Label(canary_card, text="SECURE (SAFE)", font=("Arial", 12, "bold"), fg="#10b981", bg="#1e293b")
lbl_canary_val.pack()

# Log Terminal Box
log_box = tk.Text(root, height=10, width=90, bg="#020617", fg="#38bdf8", font=("Courier", 10), bd=1, relief="solid")
log_box.pack(pady=10, padx=20)
log_box.insert(tk.END, "[SOC MONITOR INITIALIZED] System ready for demonstration...\n")

def log(text):
    log_box.insert(tk.END, text + "\n")
    log_box.see(tk.END)

# Canary Status Checker
def check_canary_status():
    if os.path.exists("test_files"):
        files = os.listdir("test_files")
        has_locked = any(f.endswith(".locked") for f in files)
        if has_locked:
            lbl_canary_val.config(text=" ATTACK BLOCKED!", fg="#ef4444")
        else:
            lbl_canary_val.config(text="SECURE (SAFE)", fg="#10b981")
    root.after(1000, check_canary_status)

# Defender Toggle Logic
def toggle_defender():
    global defender_process
    if defender_process is None:
        defender_process = subprocess.Popen(["python3", "defender_detector.py"])
        log("[ ACTIVATED] Defender Watchdog Engine is now RUNNING.")
        lbl_status_val.config(text="ACTIVE (MONITORING)", fg="#10b981")
        btn_def.config(text="STOP DEFENDER ENGINE", bg="#ef4444")
    else:
        defender_process.terminate()
        defender_process.kill()
        defender_process = None
        # ပိတ်လိုက်သည့်အခါ Process ကျန်မနေစေရန် Auto-Kill ပြုလုပ်မည်
        os.system("pkill -9 -f defender_detector.py > /dev/null 2>&1")
        log("[ STOPPED] Defender Watchdog Engine Deactivated.")
        lbl_status_val.config(text="STANDBY (OFF)", fg="#f59e0b")
        btn_def.config(text="1. START DEFENDER ENGINE", bg="#10b981")

def run_attacker():
    log("[ ATTACK DETECTED] Simulating Ransomware Attack...")
    subprocess.Popen(["python3", "attacker_ransomware.py"])

def open_decryptor():
    log("[ RECOVERY] Launching Admin Decryption Suite...")
    subprocess.Popen(["python3", "admin_decryptor.py"])

def open_file_manager():
    if not os.path.exists("test_files"):
        os.makedirs("test_files")
    subprocess.Popen(["xdg-open", "test_files"])
    log("[ EXPLORER] Opened test_files directory.")

def view_report():
    if os.path.exists("incident_report.json"):
        with open("incident_report.json", "r") as f:
            data = json.load(f)
        report_str = json.dumps(data, indent=4)
        messagebox.showinfo(" SOC Forensic Incident Report", report_str)
    else:
        messagebox.showwarning("No Report", "No attack incident recorded yet.")

def reset_files():
    target_dir = "test_files"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    else:
        for f in os.listdir(target_dir):
            file_path = os.path.join(target_dir, f)
            if os.path.isfile(file_path):
                os.remove(file_path)

    with open(os.path.join(target_dir, "000_Canary.docx"), "w") as f:
        f.write("Canary File Data for Early Ransomware Detection")

    with open(os.path.join(target_dir, "financial_report.docx"), "w") as f:
        f.write("Student Financial Records and Confidential Budget Data")

    with open(os.path.join(target_dir, "exam_questions.pdf"), "w") as f:
        f.write("Confidential Final Exam Question Papers 2026")

    if os.path.exists("incident_report.json"):
        os.remove("incident_report.json")

    lbl_canary_val.config(text="SECURE (SAFE)", fg="#10b981")
    log("[ RESET] Test Environment Cleaned and Files Re-generated.")

# Window ပိတ်လိုက်ပါက Background Process အားလုံးကို အပြီးသတ် သတ်ပေးမည်
def on_closing():
    os.system("pkill -9 -f defender_detector.py > /dev/null 2>&1")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Buttons Layout
frame_btn = tk.Frame(root, bg="#0f172a")
frame_btn.pack(pady=10)

btn_def = tk.Button(frame_btn, text="1. START DEFENDER ENGINE", command=toggle_defender, bg="#10b981", fg="white", font=("Arial", 10, "bold"), width=28, pady=5)
btn_def.grid(row=0, column=0, pady=5, padx=8)

btn_atk = tk.Button(frame_btn, text="2. SIMULATE RANSOMWARE ATTACK", command=run_attacker, bg="#f59e0b", fg="white", font=("Arial", 10, "bold"), width=28, pady=5)
btn_atk.grid(row=0, column=1, pady=5, padx=8)

btn_dec = tk.Button(frame_btn, text="3. OPEN ADMIN RECOVERY PANEL", command=open_decryptor, bg="#3b82f6", fg="white", font=("Arial", 10, "bold"), width=28, pady=5)
btn_dec.grid(row=1, column=0, pady=5, padx=8)

btn_report = tk.Button(frame_btn, text=" VIEW FORENSIC REPORT", command=view_report, bg="#8b5cf6", fg="white", font=("Arial", 10, "bold"), width=28, pady=5)
btn_report.grid(row=1, column=1, pady=5, padx=8)

btn_folder = tk.Button(frame_btn, text=" OPEN TEST_FILES FOLDER", command=open_file_manager, bg="#0284c7", fg="white", font=("Arial", 10, "bold"), width=28, pady=5)
btn_folder.grid(row=2, column=0, pady=5, padx=8)

btn_rst = tk.Button(frame_btn, text="RESET TEST ENVIRONMENT", command=reset_files, bg="#64748b", fg="white", font=("Arial", 10, "bold"), width=28, pady=5)
btn_rst.grid(row=2, column=1, pady=5, padx=8)

check_canary_status()
root.mainloop()