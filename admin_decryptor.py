import os
import glob
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

TARGET_DIR = "test_files"
PRIVATE_KEY_PATH = "keys/private_key.pem"

root = tk.Tk()
root.title("Admin Decryption Dashboard")
root.geometry("820x580")
root.configure(bg="#1e1e2e")

# Title Label
label = tk.Label(
    root, 
    text="ADMIN FILE RECOVERY DASHBOARD", 
    font=("Arial", 14, "bold"), 
    fg="#00FF7F", 
    bg="#1e1e2e"
)
label.pack(pady=15)

# Status Log Window
log_box = tk.Text(
    root, 
    height=15, 
    width=65, 
    bg="#181825", 
    fg="#00FF00", 
    font=("Courier", 10)
)
log_box.pack(pady=10)
log_box.insert(tk.END, "--- SYSTEM STATUS: Waiting for Decryption Key... ---\n")

def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)

def start_decryption():
    if not os.path.exists(PRIVATE_KEY_PATH):
        messagebox.showerror("Error", "Private Key File Missing!")
        return

    key_file_path = os.path.join(TARGET_DIR, "encrypted_aes_key.bin")
    if not os.path.exists(key_file_path):
        log("[INFO] No encrypted key found in test_files.")
        return

    try:
        with open(PRIVATE_KEY_PATH, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        with open(key_file_path, "rb") as f:
            encrypted_aes_key = f.read()

        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        fernet = Fernet(aes_key)
        locked_files = glob.glob(os.path.join(TARGET_DIR, "*.locked"))

        if not locked_files:
            log("[INFO] No .locked files found.")
            return

        for file_path in locked_files:
            with open(file_path, "rb") as f:
                encrypted_data = f.read()

            decrypted_data = fernet.decrypt(encrypted_data)
            original_path = file_path.replace(".locked", "")

            with open(original_path, "wb") as f:
                f.write(decrypted_data)

            os.remove(file_path)
            log(f"[SUCCESS RESTORED] {os.path.basename(original_path)}")

        os.remove(key_file_path)
        log("\n[ ALL FILES SUCCESSFULLY RECOVERED!]")
        messagebox.showinfo("Success", "All locked files have been restored!")

    except Exception as e:
        log(f"[ERROR] Decryption Failed: {e}")
        messagebox.showerror("Error", f"Failed to decrypt: {e}")

# Button
btn = tk.Button(
    root, 
    text="DECRYPT & RESTORE FILES", 
    command=start_decryption, 
    bg="#2b5c8f", 
    fg="white", 
    font=("Arial", 11, "bold"),
    padx=10, 
    pady=5
)
btn.pack(pady=10)

root.mainloop()