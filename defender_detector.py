# import time
# import os
# import psutil
# import json
# import subprocess
# from datetime import datetime

# TARGET_DIR = "test_files"
# REPORT_FILE = "incident_report.json"

# def notify_user(pid_killed):
#     try:
#         subprocess.run([
#             "notify-send", 
#             "-u", "critical", 
#             "-i", "security-low", 
#             " RANSOMWARE BLOCKED!", 
#             f"Canary file tampered! Attack process (PID: {pid_killed}) killed instantly."
#         ])
#     except Exception:
#         pass

# def generate_forensic_report(killed_pid):
#     report_data = {
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "status": "THREAT BLOCKED",
#         "detected_by": "Canary Integrity Monitor",
#         "compromised_canary": "000_Canary.docx",
#         "terminated_process_pid": killed_pid,
#         "action_taken": "Process Terminated & Protection Enforced"
#     }
#     with open(REPORT_FILE, "w") as f:
#         json.dump(report_data, f, indent=4)

# def kill_attacker():
#     for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
#         try:
#             cmdline = proc.info['cmdline']
#             if cmdline and any("attacker_ransomware.py" in arg for arg in cmdline):
#                 pid = proc.info['pid']
#                 proc.kill()
#                 print(f"[ DEFENDER] KILLED RANSOMWARE PROCESS PID: {pid}")
#                 notify_user(pid)
#                 generate_forensic_report(pid)
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass

# def start_watchdog():
#     print("[ DEFENDER] Engine Running. Monitoring Canary File...")
#     while True:
#         if os.path.exists(TARGET_DIR):
#             files = os.listdir(TARGET_DIR)
#             for file in files:
#                 if file.endswith(".locked"):
#                     kill_attacker()
#                     break
#         time.sleep(0.1)

# if __name__ == "__main__":
#     start_watchdog()
from datetime import datetime
import json
import os
import shutil  # <-- Quarantine အတွက် ထပ်တိုး import
import subprocess
import time
import psutil

TARGET_DIR = "test_files"
REPORT_FILE = "incident_report.json"
QUARANTINE_DIR = "Quarantine_Vault"  # <-- Quarantine Vault Folder နာမည်
ATTACKER_SCRIPT = "attacker_ransomware.py"


def notify_user(pid_killed):
    try:
        subprocess.run([
            "notify-send",
            "-u",
            "critical",
            "-i",
            "security-low",
            " RANSOMWARE BLOCKED!",
            (
                f"Canary file tampered! Attack process (PID: {pid_killed})"
                " killed instantly."
            ),
        ])
    except Exception:
        pass


def quarantine_malware():
    """Ransomware Payload Script/File ကို Quarantine Vault ထထဲသို့ အလိုအလျောက် ရွှေ့ပေးသည့် Function"""
    try:
        # Quarantine Vault Folder မရှိသေးရင် ဆောက်မယ်
        if not os.path.exists(QUARANTINE_DIR):
            os.makedirs(QUARANTINE_DIR)

        # Attacker Script သို့မဟုတ် Malware File ရှိနေရင် Vault ထဲ ရွှေ့မယ်
        if os.path.exists(ATTACKER_SCRIPT):
            dest_path = os.path.join(QUARANTINE_DIR, ATTACKER_SCRIPT)
            shutil.copy(ATTACKER_SCRIPT, dest_path)
            print(
                f"[ DEFENDER] QUARANTINED MALWARE FILE: {ATTACKER_SCRIPT} ->"
                f" {dest_path}"
            )
            return True
    except Exception as e:
        print(f"[ DEFENDER ERROR] Quarantine Failed: {e}")
    return False


def generate_forensic_report(killed_pid):
    report_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "THREAT BLOCKED",
        "detected_by": "Canary Integrity Monitor",
        "compromised_canary": "000_Canary.docx",
        "terminated_process_pid": killed_pid,
        "action_taken": (
            "Process Terminated, Payload Quarantined & Protection Enforced"
        ),
    }
    with open(REPORT_FILE, "w") as f:
        json.dump(report_data, f, indent=4)


def kill_attacker():
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmdline = proc.info["cmdline"]
            if cmdline and any("attacker_ransomware.py" in arg for arg in cmdline):
                pid = proc.info["pid"]
                proc.kill()  # ၁။ Process ကို သတ်မယ်
                print(f"[ DEFENDER] KILLED RANSOMWARE PROCESS PID: {pid}")

                quarantine_malware()  # ၂။ Malware File ကို Quarantine Vault ထဲ ရွှေ့မယ်
                notify_user(pid)  # ၃။ အကြောင်းကြားစာ ပို့မယ်
                generate_forensic_report(pid)  # ၄။ Forensic Report ထုတ်ပေးမယ်
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def start_watchdog():
    print("[ DEFENDER] Engine Running. Monitoring Canary File...")
    while True:
        if os.path.exists(TARGET_DIR):
            files = os.listdir(TARGET_DIR)
            for file in files:
                if file.endswith(".locked"):
                    kill_attacker()
                    break
        time.sleep(0.1)


if __name__ == "__main__":
    start_watchdog()