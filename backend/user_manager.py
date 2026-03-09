import json
import os
import bcrypt

from tinyec import registry
from tinyec.ec import Point

from backend.ecc_engine import generate_keys


USER_FILE = "storage/users.json"


class UserManager:

    def __init__(self):

        # create user file if not exists
        if not os.path.exists(USER_FILE):

            os.makedirs("storage", exist_ok=True)

            with open(USER_FILE, "w") as f:
                json.dump({}, f)

    # ====================================
    # Load Users
    # ====================================

    def load_users(self):

        with open(USER_FILE, "r") as f:
            return json.load(f)

    # ====================================
    # Save Users
    # ====================================

    def save_users(self, users):

        with open(USER_FILE, "w") as f:
            json.dump(users, f, indent=4)

    # ====================================
    # Register User
    # ====================================

    def register(self, username, password):

        users = self.load_users()

        if username in users:
            return False

        # hash password
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # generate ECC keys
        private_key, public_key = generate_keys()

        users[username] = {
            "password": hashed,
            "public_key_x": public_key.x,
            "public_key_y": public_key.y
        }

        self.save_users(users)

        # save private key locally
        os.makedirs("keys", exist_ok=True)

        with open(f"keys/{username}_private.pem", "w") as f:
            f.write(str(private_key))

        return True

    # ====================================
    # Login
    # ====================================

    def login(self, username, password):

        users = self.load_users()

        if username not in users:
            return False

        stored = users[username]["password"].encode()

        return bcrypt.checkpw(password.encode(), stored)

    # ====================================
    # Get Public Key (FIXED)
    # ====================================

    def get_public_key(self, username):

        users = self.load_users()

        data = users[username]

        curve = registry.get_curve("secp256r1")

        x = data["public_key_x"]
        y = data["public_key_y"]

        # FIXED: create Point object correctly
        public_key = Point(curve, x, y)

        return public_key