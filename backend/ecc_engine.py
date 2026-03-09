from tinyec import registry
import secrets

curve = registry.get_curve("secp256r1")


# ==============================
# Generate ECC keys
# ==============================

def generate_keys():

    private_key = secrets.randbelow(curve.field.n)

    public_key = private_key * curve.g

    return private_key, public_key


# ==============================
# Encrypt AES key
# ==============================

def encrypt_key(aes_key, public_key):

    k = secrets.randbelow(curve.field.n)

    shared = k * public_key

    cipher = bytes([a ^ (shared.x % 256) for a in aes_key])

    return cipher, k * curve.g


# ==============================
# Decrypt AES key
# ==============================

def decrypt_key(cipher, private_key, point):

    shared = private_key * point

    aes_key = bytes([c ^ (shared.x % 256) for c in cipher])

    return aes_key