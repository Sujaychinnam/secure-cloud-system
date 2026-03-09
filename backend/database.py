import bcrypt

users = {}

def create_user(username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users[username] = hashed

def verify_user(username, password):
    if username not in users:
        return False
    return bcrypt.checkpw(password.encode(), users[username])