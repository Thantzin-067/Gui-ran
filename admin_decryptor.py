import glob
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

TARGET_DIR = "test_files"
REPORT_FILE = "incident_report.json"
TEMP_KEY_FILE = "captured_keys.json"
PRIVATE_KEY_PATH = "keys/private_key.pem"
QUARANTINE_DIR = "Quarantine_Vault"

root = tk.Tk()
root.title("SOC Enterprise Protection & Recovery Dashboard")
root.geometry("850x730")
root.configure(bg="#1e1e2e")

# Title Label
label = tk.Label(
    root,
    text="SOC ADMIN DATA RECOVERY DASHBOARD",
    font=("Arial", 16, "bold"),
    fg="#00FF7F",
    bg="#1e1e2e",
)
label.pack(pady=15)

# Status Log Window
log_box = tk.Text(
    root, height=11, width=80, bg="#181825", fg="#00FF00", font=("Courier", 10)
)
log_box.pack(pady=10)
log_box.insert(
    tk.END, "--- SYSTEM STATUS: Waiting for Decryption Key Input... ---\n"
)


def log(msg):
  log_box.insert(tk.END, msg + "\n")
  log_box.see(tk.END)


# -------------------------------------------------------------------
# 1. RAM Intercepted Key ကို ရှာဖွေပြသပေးသည့် Function
# -------------------------------------------------------------------
def scan_ram_key():
  intercepted_key = None

  if os.path.exists(REPORT_FILE):
    try:
      with open(REPORT_FILE, "r") as f:
        report = json.load(f)
        intercepted_key = report.get("intercepted_aes_key")
    except Exception:
      pass

  if not intercepted_key or intercepted_key == "NOT_CAPTURED":
    if os.path.exists(TEMP_KEY_FILE):
      try:
        with open(TEMP_KEY_FILE, "r") as f:
          data = json.load(f)
          intercepted_key = data.get("intercepted_key")
      except Exception:
        pass

  if (
      intercepted_key
      and intercepted_key != "NOT_CAPTURED"
      and intercepted_key is not None
  ):
    key_display_var.set(intercepted_key)
    manual_key_entry.delete(0, tk.END)
    manual_key_entry.insert(0, intercepted_key)
    log(f"[RAM FORENSICS] Intercepted Key Found: {intercepted_key}")
    messagebox.showinfo(
        "RAM Key Found",
        f"Intercepted AES Key captured by Defender:\n\n{intercepted_key}",
    )
  else:
    key_display_var.set("NO KEY CAPTURED (Defender was OFF)")
    log(
        "[WARNING] No Intercepted Key found in volatile memory/report."
        " Permanent Data Loss!"
    )
    messagebox.showwarning(
        "Warning",
        "No Intercepted Key Found!\nDefender might have been OFF during attack.",
    )


# -------------------------------------------------------------------
# 1.1 VOLATILE MEMORY HEX DUMP INSPECTOR FUNCTION (ADDED)
# -------------------------------------------------------------------
def inspect_ram_hex_dump():
  user_key = key_display_var.get()

  if (
      not user_key
      or "NO KEY" in user_key
      or "Click" in user_key
      or "OFF" in user_key
  ):
    messagebox.showwarning(
        "Forensics Warning",
        "No active RAM key captured to inspect!\nRun attack with Defender ON"
        " first, then click 'Scan RAM Key'.",
    )
    return

  hex_window = tk.Toplevel(root)
  hex_window.title(" RAM Forensics - Volatile Memory Hex Dump")
  hex_window.geometry("720x450")  # Window Width ကို နည်းနည်း ချဲ့ပေးထားပါတယ်
  hex_window.configure(bg="#11111B")

  title = tk.Label(
      hex_window,
      text=" VOLATILE MEMORY (RAM) RAW BYTES INSPECTOR",
      font=("Arial", 11, "bold"),
      fg="#F9E2AF",
      bg="#11111B",
  )
  title.pack(pady=8)

  text_area = tk.Text(
      hex_window,
      height=18,
      width=82,
      bg="#1E1E2E",
      fg="#CDD6F4",
      font=("Courier", 10),
  )
  text_area.pack(pady=5, padx=10)

  key_bytes = user_key.encode()

  # Bytes များကို Format လုပ်ခြင်း
  hex_list = [f"{b:02X}" for b in key_bytes]

  line1 = " ".join(hex_list[:16])
  line2 = " ".join(hex_list[16:32])
  line3 = " ".join(hex_list[32:])

  ascii1 = user_key[:16]
  ascii2 = user_key[16:32]
  ascii3 = user_key[32:]

  text_area.insert(
      tk.END, "OFFSET    00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F  ASCII\n"
  )
  text_area.insert(
      tk.END,
      "-------------------------------------------------------------------\n",
  )
  text_area.insert(
      tk.END,
      f"0x7FFF00  41 53 53 45 54 5F 4B 45 59 5F 53 54 41 52 54 00"
      "  [RAM_HEADER]\n",
  )
  text_area.insert(
      tk.END, f"0x7FFF10  {line1:<47}  |{ascii1}|\n"
  )  # RAW_AES_KEY Part 1
  text_area.insert(
      tk.END, f"0x7FFF20  {line2:<47}  |{ascii2}|\n"
  )  # RAW_AES_KEY Part 2
  if line3:
    text_area.insert(
        tk.END, f"0x7FFF30  {line3:<47}  |{ascii3}|\n"
    )  # RAW_AES_KEY Part 3

  text_area.insert(
      tk.END,
      "0x7FFF40  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  [FREE_RAM]\n",
  )
  text_area.insert(
      tk.END,
      "-------------------------------------------------------------------\n",
  )
  text_area.insert(
      tk.END,
      f" EXTRACTED AES KEY: {user_key}\nSTATUS: MATCHED & UNCORRUPTED IN"
      " VOLATILE RAM",
  )

  text_area.config(state="disabled")


# Key Frame Display
key_frame = tk.Frame(root, bg="#1e1e2e")
key_frame.pack(pady=5)

key_display_label = tk.Label(
    key_frame,
    text="RAM Intercepted Key: ",
    font=("Arial", 10, "bold"),
    fg="#CBA6F7",
    bg="#1e1e2e",
)
key_display_label.pack(side=tk.LEFT, padx=5)

key_display_var = tk.StringVar(value="Click 'Scan RAM Key' to search...")
key_display_entry = tk.Entry(
    key_frame,
    textvariable=key_display_var,
    width=35,
    font=("Courier", 10),
    state="readonly",
    bg="#313244",
    fg="#F5E0DC",
)
key_display_entry.pack(side=tk.LEFT, padx=5)

btn_scan = tk.Button(
    key_frame,
    text="Scan RAM Key",
    command=scan_ram_key,
    bg="#89B4FA",
    fg="#11111B",
    font=("Arial", 9, "bold"),
)
btn_scan.pack(side=tk.LEFT, padx=3)

# Hex Dump Button (ADDED)
btn_hex = tk.Button(
    key_frame,
    text="Hex Dump",
    command=inspect_ram_hex_dump,
    bg="#F9E2AF",
    fg="#11111B",
    font=("Arial", 9, "bold"),
)
btn_hex.pack(side=tk.LEFT, padx=3)

# Manual Decryption Input Field
input_frame = tk.Frame(root, bg="#1e1e2e")
input_frame.pack(pady=10)

input_label = tk.Label(
    input_frame,
    text="Enter AES Key for Decryption: ",
    font=("Arial", 11, "bold"),
    fg="#89B4FA",
    bg="#1e1e2e",
)
input_label.pack(anchor="w")
manual_key_entry = tk.Entry(
    input_frame, width=60, font=("Courier", 11), bg="#313244", fg="#A6E3A1"
)
manual_key_entry.pack(pady=5)


# -------------------------------------------------------------------
# 2. Key Input ဖြင့် Decrypt ပြုလုပ်သည့် Normal Function
# -------------------------------------------------------------------
def start_decryption():
  user_key = manual_key_entry.get().strip()

  if not user_key:
    messagebox.showerror(
        "Input Error", "Please enter/paste an AES key to decrypt files!"
    )
    log("[ERROR] Decryption aborted: No AES Key provided.")
    return

  locked_files = glob.glob(os.path.join(TARGET_DIR, "*.locked"))

  if not locked_files:
    log("[INFO] No .locked files found.")
    messagebox.showinfo("Info", "No .locked files found to restore.")
    return

  try:
    fernet = Fernet(user_key.encode())
    restored_count = 0
    for file_path in locked_files:
      with open(file_path, "rb") as f:
        encrypted_data = f.read()

      decrypted_data = fernet.decrypt(encrypted_data)
      original_path = file_path.replace(".locked", "")

      with open(original_path, "wb") as f:
        f.write(decrypted_data)

      os.remove(file_path)
      log(f"[SUCCESS RESTORED] {os.path.basename(original_path)}")
      restored_count += 1

    key_file_path = os.path.join(TARGET_DIR, "encrypted_aes_key.bin")
    if os.path.exists(key_file_path):
      os.remove(key_file_path)

    log(f"\n[SUCCESS] {restored_count} Files Restored via AES Key!")
    messagebox.showinfo(
        "Success",
        f"All {restored_count} locked file(s) restored successfully!",
    )

  except Exception as e:
    log(f"[ERROR] Decryption Failed! Invalid AES Key: {e}")
    messagebox.showerror(
        "Decryption Failed", "Invalid AES Key! Check your key and try again."
    )# -------------------------------------------------------------------
# 3. MASTER RSA AUTO-DECRYPT FUNCTION
# -------------------------------------------------------------------
def master_auto_decrypt():
  key_file_path = os.path.join(TARGET_DIR, "encrypted_aes_key.bin")
  locked_files = glob.glob(os.path.join(TARGET_DIR, "*.locked"))

  if not locked_files:
    log("[INFO] No .locked files found to auto-decrypt.")
    messagebox.showinfo("Info", "No .locked files found.")
    return

  if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(key_file_path):
    log("[ERROR] Master Private Key or Encrypted Key file missing!")
    messagebox.showerror("Error", "Private Key missing for Auto-Decrypt!")
    return

  try:
    with open(PRIVATE_KEY_PATH, "rb") as f:
      private_key = serialization.load_pem_private_key(f.read(), password=None)

    with open(key_file_path, "rb") as f:
      encrypted_aes_key = f.read()

    raw_aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    fernet = Fernet(raw_aes_key)
    for file_path in locked_files:
      with open(file_path, "rb") as f:
        encrypted_data = f.read()

      decrypted_data = fernet.decrypt(encrypted_data)
      original_path = file_path.replace(".locked", "")

      with open(original_path, "wb") as f:
        f.write(decrypted_data)

      os.remove(file_path)
      log(f"[MASTER RESTORED] {os.path.basename(original_path)}")

    os.remove(key_file_path)
    log("\n[MASTER RECOVERY] All Files Force Decrypted via RSA Key!")
    messagebox.showinfo(
        "Master Reset Success",
        "Files Force Decrypted! Ready for next demo run.",
    )
  except Exception as e:
    log(f"[ERROR] Master Decryption Failed: {e}")
    messagebox.showerror("Error", f"Master Decryption Failed: {e}")


# -------------------------------------------------------------------
# 4. QUARANTINE VAULT INSPECTOR FUNCTION
# -------------------------------------------------------------------
def open_quarantine_inspector():
  q_window = tk.Toplevel(root)
  q_window.title("Quarantine Vault Inspector")
  q_window.geometry("550x350")
  q_window.configure(bg="#181825")

  title = tk.Label(
      q_window,
      text="ISOLATED MALWARE PAYLOADS",
      font=("Arial", 12, "bold"),
      fg="#F38BA8",
      bg="#181825",
  )
  title.pack(pady=10)

  # Treeview Table
  cols = ("File Name", "Size (Bytes)", "Status")
  tree = ttk.Treeview(q_window, columns=cols, show="headings", height=8)

  for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=160, anchor="center")

  tree.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

  if os.path.exists(QUARANTINE_DIR):
    files = os.listdir(QUARANTINE_DIR)
    if files:
      for file in files:
        file_path = os.path.join(QUARANTINE_DIR, file)
        size = os.path.getsize(file_path)
        tree.insert("", tk.END, values=(file, f"{size} B", "ISOLATED"))
      log(
          f"[QUARANTINE INSPECTOR] Displaying {len(files)} quarantined"
          " payload(s)."
      )
    else:
      tree.insert("", tk.END, values=("No files isolated", "0", "CLEAN"))
      log("[QUARANTINE INSPECTOR] Vault is empty.")
  else:
    tree.insert("", tk.END, values=("Vault Directory Missing", "0", "N/A"))


# Buttons Frame
btn_frame = tk.Frame(root, bg="#1e1e2e")
btn_frame.pack(pady=10)

btn_decrypt = tk.Button(
    btn_frame,
    text="DECRYPT WITH KEY",
    command=start_decryption,
    bg="#A6E3A1",
    fg="#11111B",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=6,
)
btn_decrypt.pack(side=tk.LEFT, padx=5)

btn_master = tk.Button(
    btn_frame,
    text="MASTER RESET",
    command=master_auto_decrypt,
    bg="#F38BA8",
    fg="#11111B",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=6,
)
btn_master.pack(side=tk.LEFT, padx=5)
btn_quarantine = tk.Button(
    btn_frame,
    text="VIEW QUARANTINE",
    command=open_quarantine_inspector,
    bg="#FAB387",
    fg="#11111B",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=6,
)
btn_quarantine.pack(side=tk.LEFT, padx=5)

root.mainloop()