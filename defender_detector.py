import time
import os
import psutil
import json
import subprocess
from datetime import datetime

TARGET_DIR = "test_files"
REPORT_FILE = "incident_report.json"

def notify_user(pid_killed):
    try:
        subprocess.run([
            "notify-send", 
            "-u", "critical", 
            "-i", "security-low", 
            " RANSOMWARE BLOCKED!", 
            f"Canary file tampered! Attack process (PID: {pid_killed}) killed instantly."
        ])
    except Exception:
        pass

def generate_forensic_report(killed_pid):
    report_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "THREAT BLOCKED",
        "detected_by": "Canary Integrity Monitor",
        "compromised_canary": "000_Canary.docx",
        "terminated_process_pid": killed_pid,
        "action_taken": "Process Terminated & Protection Enforced"
    }
    with open(REPORT_FILE, "w") as f:
        json.dump(report_data, f, indent=4)

def kill_attacker():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any("attacker_ransomware.py" in arg for arg in cmdline):
                pid = proc.info['pid']
                proc.kill()
                print(f"[ DEFENDER] KILLED RANSOMWARE PROCESS PID: {pid}")
                notify_user(pid)
                generate_forensic_report(pid)
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