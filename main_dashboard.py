import os
import subprocess
import tkinter as tk

root = tk.Tk()
root.title(" Enterprise Ransomware Defense & SOC Monitor")
root.geometry("1250x800")
root.configure(bg="#0f172a")

# Defender Process ကို ထိန်းချုပ်မည့် Variable (စစချင်းမှာ None ဖြစ်ရမည်)
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
card_frame = tk.Frame(root, bg="#0f172a", pady=10)
card_frame.pack(fill="x", padx=20)

# Card 1: Engine Status
status_card = tk.Frame(card_frame, bg="#1e293b", bd=1, relief="solid", padx=15, pady=10)
status_card.pack(side="left", expand=True, fill="x", padx=5)
lbl_status_title = tk.Label(status_card, text="DEFENSE ENGINE", font=("Arial", 9, "bold"), fg="#94a3b8", bg="#1e293b")
lbl_status_title.pack()
lbl_status_val = tk.Label(status_card, text="STANDBY (OFF)", font=("Arial", 12, "bold"), fg="#f59e0b", bg="#1e293b")
lbl_status_val.pack()

# Card 2: Canary File Status
canary_card = tk.Frame(card_frame, bg="#1e293b", bd=1, relief="solid", padx=15, pady=10)
canary_card.pack(side="left", expand=True, fill="x", padx=5)
lbl_canary_title = tk.Label(canary_card, text="CANARY INTEGRITY", font=("Arial", 9, "bold"), fg="#94a3b8", bg="#1e293b")
lbl_canary_title.pack()
lbl_canary_val = tk.Label(canary_card, text="SECURE (SAFE)", font=("Arial", 12, "bold"), fg="#10b981", bg="#1e293b")
lbl_canary_val.pack()

# Log Terminal Box
log_box = tk.Text(root, height=12, width=90, bg="#020617", fg="#38bdf8", font=("Courier", 10), bd=1, relief="solid")
log_box.pack(pady=10, padx=20)
log_box.insert(tk.END, "[SOC MONITOR INITIALIZED] System ready for demonstration...\n")

def log(text):
    log_box.insert(tk.END, text + "\n")
    log_box.see(tk.END)

# Defender Toggle Logic (ခလုတ်နှိပ်မှသာ ပွင့်မည်/ပိတ်မည်)
def toggle_defender():
    global defender_process
    if defender_process is None:
        # ခလုတ်နှိပ်လိုက်မှသာ Process အဖြစ် စတင်ဖွင့်မည်
        defender_process = subprocess.Popen(["python3", "defender_detector.py"])
        log("[ ACTIVATED] Defender Watchdog Engine is now RUNNING.")
        lbl_status_val.config(text="ACTIVE (MONITORING)", fg="#10b981")
        btn_def.config(text="STOP DEFENDER ENGINE", bg="#ef4444")
    else:
        # ခလုတ်ပြန်နှိပ်ပါက Defender Process ကို အပြီးသတ် သတ်ပစ်မည်
        defender_process.terminate()
        defender_process.kill()
        defender_process = None
        log("[ STOPPED] Defender Watchdog Engine Deactivated.")
        lbl_status_val.config(text="STANDBY (OFF)", fg="#f59e0b")
        btn_def.config(text="1. START DEFENDER ENGINE", bg="#10b981")

def run_attacker():
    log("[ ATTACK DETECTED] Simulating Ransomware Attack...")
    subprocess.Popen(["python3", "attacker_ransomware.py"])

def open_decryptor():
    log("[ RECOVERY] Launching Admin Decryption Suite...")
    subprocess.Popen(["python3", "admin_decryptor.py"])

def reset_files():
    os.system("rm -rf test_files && mkdir -p test_files")
    os.system('echo "Canary File Data" > test_files/000_Canary.docx')
    os.system('echo "Student Financial Records" > test_files/financial_report.docx')
    os.system('echo "Confidential Exam Paper" > test_files/exam_questions.pdf')
    lbl_canary_val.config(text="SECURE (SAFE)", fg="#10b981")
    log("[ RESET] Test Environment Cleaned and Files Re-generated.")

# Buttons Layout
frame_btn = tk.Frame(root, bg="#0f172a")
frame_btn.pack(pady=10)

btn_def = tk.Button(frame_btn, text="1. START DEFENDER ENGINE", command=toggle_defender, bg="#10b981", fg="white", font=("Arial", 10, "bold"), width=32, pady=6)
btn_def.grid(row=0, column=0, pady=5, padx=10)

btn_atk = tk.Button(frame_btn, text="2. SIMULATE RANSOMWARE ATTACK", command=run_attacker, bg="#f59e0b", fg="white", font=("Arial", 10, "bold"), width=32, pady=6)
btn_atk.grid(row=0, column=1, pady=5, padx=10)
btn_dec = tk.Button(frame_btn, text="3. OPEN ADMIN RECOVERY PANEL", command=open_decryptor, bg="#3b82f6", fg="white", font=("Arial", 10, "bold"), width=32, pady=6)
btn_dec.grid(row=1, column=0, pady=5, padx=10)

btn_rst = tk.Button(frame_btn, text="RESET TEST ENVIRONMENT", command=reset_files, bg="#64748b", fg="white", font=("Arial", 10, "bold"), width=32, pady=6)
btn_rst.grid(row=1, column=1, pady=5, padx=10)

root.mainloop()