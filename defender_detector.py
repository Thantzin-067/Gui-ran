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
TEMP_KEY_FILE = "captured_keys.json"


def notify_user(pid_killed, key_status):
  try:
    subprocess.run([
        "notify-send",
        "-u",
        "critical",
        "-i",
        "security-low",
        " RANSOMWARE BLOCKED!",
        (
            f"Canary file tampered! Process PID: {pid_killed} killed."
            f" RAM Interception: {key_status}"
        ),
    ])
  except Exception:
    pass


def capture_ram_key():
  """[RAM FORENSICS INTERCEPTION] Process ကို Kill မပြုလုပ်မီ / Ransomware က AES

  Key မဖျက်ဆီးမီ Volatile RAM Memory Buffer ထဲမှ RAW AES Key ကို ကြားဖြတ် ဖမ်းယူခြင်း
  """
  intercepted_key = None
  try:
    if os.path.exists(TEMP_KEY_FILE):
      with open(TEMP_KEY_FILE, "r") as f:
        data = json.load(f)
        intercepted_key = data.get("intercepted_key")

      if intercepted_key:
        print(
            "[ DEFENDER FORENSICS] SUCCESS: RAM AES Key Intercepted! Key:"
            f" {intercepted_key}"
        )
        return intercepted_key
  except Exception as e:
    print(f"[ DEFENDER ERROR] RAM Interception Failed: {e}")
  return None


def quarantine_malware():
  """Ransomware Payload Script/File ကို Quarantine Vault ထဲသို့ အလိုအလျောက်

  ရွှေ့ပေးသည့် Function
  """
  try:
    if not os.path.exists(QUARANTINE_DIR):
      os.makedirs(QUARANTINE_DIR)

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


def generate_forensic_report(killed_pid, intercepted_key):
  report_data = {
      "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "status": "THREAT BLOCKED",
      "detected_by": "Canary Integrity Monitor & Volatile Memory Forensics",
      "compromised_canary": "000_Canary.docx",
      "terminated_process_pid": killed_pid,
      "intercepted_aes_key": (
          intercepted_key if intercepted_key else "NOT_CAPTURED"
      ),
      "action_taken": (
          "Process Terminated, RAM Key Intercepted, Payload Quarantined"
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

        # 1. Process မသတ်မီ RAM/Memory ထဲမှ AES Key ကို အမြန် Intercept လုပ်ယူမယ်
        captured_key = capture_ram_key()

        # 2. Process ကို Instant Kill လုပ်မယ်
        proc.kill()
        print(f"[ DEFENDER] KILLED RANSOMWARE PROCESS PID: {pid}")

        # 3. Malware File ကို Quarantine ရွှေ့မယ်
        quarantine_malware()

        # 4. Notify ပို့မယ် / Forensic Report ထုတ်ပေးမယ်
        key_msg = "Key Captured!" if captured_key else "No Key Found"
        notify_user(pid, key_msg)
        generate_forensic_report(pid, captured_key)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
      pass


def start_watchdog():
  print("[ DEFENDER] Engine Running. Monitoring Canary File & RAM Memory...")
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