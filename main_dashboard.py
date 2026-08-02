import json
import os
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
import phishing_entry

from snapshot_manager import create_snapshot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILES_DIR = os.path.join(BASE_DIR, "test_files")
REPORT_FILE = os.path.join(BASE_DIR, "incident_report.json")

root = None
log_box = None
lbl_status_val = None
lbl_canary_val = None
btn_def = None
defender_process = None


def log(text):
    if log_box is not None:
        log_box.insert(tk.END, text + "\n")
        log_box.see(tk.END)


def get_project_path(*parts):
    return os.path.join(BASE_DIR, *parts)


def ensure_test_files_dir():
    os.makedirs(TEST_FILES_DIR, exist_ok=True)


def check_canary_status():
    ensure_test_files_dir()
    files = os.listdir(TEST_FILES_DIR)
    has_locked = any(f.endswith(".locked") for f in files)

    if lbl_canary_val is not None:
        if has_locked:
            lbl_canary_val.config(text="ATTACK BLOCKED!", fg="#ef4444")
        else:
            lbl_canary_val.config(text="SECURE (SAFE)", fg="#10b981")

    if root is not None:
        root.after(1000, check_canary_status)


def start_defender_process():
    global defender_process

    if defender_process is not None and defender_process.poll() is None:
        return defender_process

    defender_script = get_project_path("defender_detector.py")
    defender_process = subprocess.Popen(
        [sys.executable, defender_script],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    log("[ACTIVATED] Defender Watchdog Engine is now RUNNING.")
    if lbl_status_val is not None:
        lbl_status_val.config(text="ACTIVE (MONITORING)", fg="#10b981")
    if btn_def is not None:
        btn_def.configure(bg="#ef4444", text="STOP DEFENDER ENGINE")
    return defender_process


def toggle_defender():
    global defender_process

    if defender_process is None or defender_process.poll() is not None:
        start_defender_process()
    else:
        defender_process.terminate()
        try:
            defender_process.kill()
        except Exception:
            pass
        defender_process = None
        os.system("pkill -9 -f defender_detector.py > /dev/null 2>&1")
        log("[STOPPED] Defender Watchdog Engine Deactivated.")
        if lbl_status_val is not None:
            lbl_status_val.config(text="STANDBY (OFF)", fg="#f59e0b")
        if btn_def is not None:
            btn_def.configure(bg="#10b981", text="1. START DEFENDER ENGINE")


def run_attacker():
    log("[SNAPSHOT] Creating a fresh backup before the attack simulation...")
    create_snapshot(
        target_dir=TEST_FILES_DIR,
        snapshot_root=get_project_path("snapshots"),
        label="pre_attack",
    )
    # Defender will NOT automatically turn on here anymore.
    # If it is already running, it will detect and block. If off, attack proceeds.
    log("[ATTACK] Simulating Ransomware Attack...")
    attacker_script = get_project_path("attacker_ransomware.py")
    subprocess.Popen(
        [sys.executable, attacker_script],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def open_decryptor():
    log("[RECOVERY] Launching Admin Decryption Suite...")
    decryptor_script = get_project_path("admin_decryptor.py")
    subprocess.Popen(
        [sys.executable, decryptor_script],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def open_file_manager():
    ensure_test_files_dir()
    subprocess.Popen(["xdg-open", TEST_FILES_DIR])
    log("[EXPLORER] Opened test_files directory.")


# def open_snapshot_manager():
#     log("[SNAPSHOT] Opening snapshot management window...")
#     snapshot_gui = get_project_path("snapshot_gui.py")
#     subprocess.Popen(
#         [sys.executable, snapshot_gui],
#         cwd=BASE_DIR,
#         stdout=subprocess.DEVNULL,
#         stderr=subprocess.DEVNULL,
#         start_new_session=True,
#     )
def open_snapshot_manager():
    log("[SNAPSHOT] Opening snapshot management window...")
    snapshot_gui = get_project_path("snapshot_gui.py")
    subprocess.Popen(
        [sys.executable, snapshot_gui],
        cwd=BASE_DIR,
        start_new_session=True,
    )


def view_report():
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        report_str = json.dumps(data, indent=4)
        messagebox.showinfo("SOC Forensic Incident Report", report_str)
    else:
        messagebox.showwarning("No Report", "No attack incident recorded yet.")


def reset_files():
    ensure_test_files_dir()

    for item in os.listdir(TEST_FILES_DIR):
        item_path = os.path.join(TEST_FILES_DIR, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    with open(os.path.join(TEST_FILES_DIR, "000_Canary.docx"), "w", encoding="utf-8") as f:
        f.write("Canary File Data for Early Ransomware Detection")

    with open(os.path.join(TEST_FILES_DIR, "financial_report.docx"), "w", encoding="utf-8") as f:
        f.write("Student Financial Records and Confidential Budget Data")

    with open(os.path.join(TEST_FILES_DIR, "exam_questions.pdf"), "w", encoding="utf-8") as f:
        f.write("Confidential Final Exam Question Papers 2026")

    if os.path.exists(REPORT_FILE):
        os.remove(REPORT_FILE)

    if lbl_canary_val is not None:
        lbl_canary_val.config(text="SECURE (SAFE)", fg="#10b981")
    log("[RESET] Test Environment Cleaned and Files Re-generated.")


def on_closing():
    if defender_process is not None:
        try:
            defender_process.terminate()
            defender_process.kill()
        except Exception:
            pass
    os.system("pkill -9 -f defender_detector.py > /dev/null 2>&1")
    if root is not None:
        root.destroy()


def build_dashboard():
    global root, log_box, lbl_status_val, lbl_canary_val, btn_def

    root = tk.Tk()
    root.title("Enterprise Ransomware Defense & SOC Monitor")

    window_width = 1200
    window_height = 820

    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = max(0, (screen_width // 2) - (window_width // 2))
    y = max(0, (screen_height // 2) - (window_height // 2))

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.minsize(850, 600)
    root.configure(bg="#07111f")
    root.option_add("*Font", "Sans 10")

    header_frame = tk.Frame(root, bg="#111c31", bd=1, relief="raised", padx=20, pady=12)
    header_frame.pack(fill="x", padx=16, pady=(12, 6))

    title = tk.Label(header_frame, text="CANARY-BASED REAL-TIME RANSOMWARE DEFENSE", bg="#111c31", fg="#7dd3fc", font="Sans 16 bold")
    title.pack(anchor="w")
    subtitle = tk.Label(header_frame, text="Enterprise monitoring, detection, recovery, and snapshot rollback workflow", bg="#111c31", fg="#94a3b8", font="Sans 9")
    subtitle.pack(anchor="w", pady=(2, 0))

    card_frame = tk.Frame(root, bg="#07111f", padx=16, pady=4)
    card_frame.pack(fill="x")

    status_card = tk.Frame(card_frame, bg="#111c31", bd=1, relief="raised", padx=16, pady=10)
    status_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=4)

    canary_card = tk.Frame(card_frame, bg="#111c31", bd=1, relief="raised", padx=16, pady=10)
    canary_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=4)

    card_frame.columnconfigure(0, weight=1)
    card_frame.columnconfigure(1, weight=1)

    lbl_status_title = tk.Label(status_card, text="DEFENSE ENGINE", bg="#111c31", fg="#94a3b8", font="Sans 9")
    lbl_status_title.pack(anchor="w")
    lbl_status_val = tk.Label(status_card, text="STANDBY (OFF)", bg="#111c31", fg="#f59e0b", font="Sans 12 bold")
    lbl_status_val.pack(anchor="w", pady=(4, 0))

    lbl_canary_title = tk.Label(canary_card, text="CANARY INTEGRITY", bg="#111c31", fg="#94a3b8", font="Sans 9")
    lbl_canary_title.pack(anchor="w")
    lbl_canary_val = tk.Label(canary_card, text="SECURE (SAFE)", bg="#111c31", fg="#10b981", font="Sans 12 bold")
    lbl_canary_val.pack(anchor="w", pady=(4, 0))

    frame_btn = tk.Frame(root, bg="#07111f", padx=16, pady=6)
    frame_btn.pack(side="bottom", fill="x", pady=(0, 8))

    log_frame = tk.Frame(root, bg="#111c31", bd=1, relief="raised", padx=12, pady=10)
    log_frame.pack(side="top", fill="both", expand=True, padx=16, pady=6)

    log_box = tk.Text(log_frame, height=6, width=100, bg="#020617", fg="#7dd3fc", font="Monospace 10", bd=0, relief="flat", wrap="word")
    log_box.pack(fill="both", expand=True)
    log_box.insert(tk.END, "[SOC MONITOR INITIALIZED] System ready for demonstration...\n")

    btn_def = tk.Button(frame_btn, text="1. START DEFENDER ENGINE", command=toggle_defender, bg="#10b981", fg="white", font="Sans 10 bold", pady=5, width=30)
    btn_def.grid(row=0, column=0, padx=6, pady=4, sticky="ew")

    btn_atk = tk.Button(frame_btn, text="2. SIMULATE RANSOMWARE ATTACK", command=lambda: phishing_entry.show_attack_options(root, run_attacker), bg="#f59e0b", fg="white", font="Sans 10 bold", pady=5, width=30)
    btn_atk.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

    btn_dec = tk.Button(frame_btn, text="3. OPEN ADMIN RECOVERY PANEL", command=open_decryptor, bg="#3b82f6", fg="white", font="Sans 10 bold", pady=5, width=30)
    btn_dec.grid(row=1, column=0, padx=6, pady=4, sticky="ew")

    btn_report = tk.Button(frame_btn, text="4.VIEW FORENSIC REPORT", command=view_report, bg="#8b5cf6", fg="white", font="Sans 10 bold", pady=5, width=30)
    btn_report.grid(row=1, column=1, padx=6, pady=4, sticky="ew")

    btn_folder = tk.Button(frame_btn, text="5. OPEN TEST FILES FOLDER", command=open_file_manager, bg="#0ea5e9", fg="white", font="Sans 10 bold", pady=5, width=30)
    btn_folder.grid(row=2, column=0, padx=6, pady=4, sticky="ew")

    btn_snap = tk.Button(frame_btn, text="6. OPEN SNAPSHOT MANAGER", command=open_snapshot_manager, bg="#0ea5e9", fg="white", font="Sans 10 bold", pady=5, width=30)
    btn_snap.grid(row=2, column=1, padx=6, pady=4, sticky="ew")

    btn_rst = tk.Button(frame_btn, text="7. RESET TEST ENVIRONMENT", command=reset_files, bg="#64748b", fg="white", font="Sans 10 bold", pady=5, width=30)
    btn_rst.grid(row=3, column=0, columnspan=2, padx=6, pady=4, sticky="ew")

    for col in range(2):
        frame_btn.columnconfigure(col, weight=1)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    check_canary_status()
    return root


def main():
    build_dashboard()
    root.mainloop()


if __name__ == "__main__":
    main()