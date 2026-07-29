import time
import os
import psutil

TARGET_DIR = "test_files"

def kill_attacker():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any("attacker_ransomware.py" in arg for arg in cmdline):
                proc.kill()
                print(f"[ DEFENDER] KILLED RANSOMWARE PROCESS PID: {proc.info['pid']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def start_watchdog():
    print("[ DEFENDER] Engine Running. Monitoring Canary File...")
    while True:
        if os.path.exists(TARGET_DIR):
            files = os.listdir(TARGET_DIR)
            # test_files ထဲမှာ .locked ဖိုင် တွေ့ရင် တန်းသတ်မည်
            for file in files:
                if file.endswith(".locked"):
                    kill_attacker()
                    break
        time.sleep(0.1)

if __name__ == "__main__":
    start_watchdog()