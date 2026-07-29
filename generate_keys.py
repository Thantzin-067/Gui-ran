import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keys():
    # 1. RSA Private Key ထုတ်ယူခြင်း (2048-bit)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # 2. Public Key ကို ခွဲထုတ်ယူခြင်း
    public_key = private_key.public_key()

    # 3. Private Key ကို PEM Format ဖြင့် Serialization လုပ်ပြီး File အဖြစ် သိမ်းခြင်း
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # 4. Public Key ကို PEM Format ဖြင့် Serialization လုပ်ပြီး File အဖြစ် သိမ်းခြင်း
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # File များအဖြစ် keys/ Folder ထဲ သိမ်းဆည်းခြင်း
    os.makedirs("keys", exist_ok=True)
    
    with open("keys/private_key.pem", "wb") as f:
        f.write(pem_private)

    with open("keys/public_key.pem", "wb") as f:
        f.write(pem_public)

    print("[SUCCESS] RSA Keys (Public & Private) များကို keys/ Folder ထဲတွင် အောင်မြင်စွာ ထုတ်ယူသိမ်းဆည်းပြီးပါပြီ။")

if __name__ == "__main__":
    generate_rsa_keys()