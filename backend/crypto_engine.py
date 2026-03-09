import os
import uuid
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_key():
    return AESGCM.generate_key(bit_length=256)


# ======================================
# Encrypt File
# ======================================

def encrypt_file(file_path):

    key = generate_key()

    with open(file_path, "rb") as f:
        data = f.read()

    aes = AESGCM(key)

    nonce = os.urandom(12)

    encrypted = aes.encrypt(nonce, data, None)

    os.makedirs("storage", exist_ok=True)

    # generate unique encrypted filename
    encrypted_name = f"{uuid.uuid4().hex}_encrypted.bin"

    encrypted_path = os.path.join("storage", encrypted_name)

    with open(encrypted_path, "wb") as f:
        f.write(nonce + encrypted)

    return key, encrypted_path


# ======================================
# Decrypt File
# ======================================

def decrypt_file(encrypted_path, key):

    with open(encrypted_path, "rb") as f:
        data = f.read()

    nonce = data[:12]
    encrypted = data[12:]

    aes = AESGCM(key)

    decrypted = aes.decrypt(nonce, encrypted, None)

    os.makedirs("storage", exist_ok=True)

    output = os.path.join("storage", "decrypted_file")

    with open(output, "wb") as f:
        f.write(decrypted)

    return output