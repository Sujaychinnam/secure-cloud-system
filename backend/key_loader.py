def load_private_key(username):

    path = f"keys/{username}_private.pem"

    with open(path, "r") as f:
        key = int(f.read())

    return key