import json
import hashlib

USER_FILE = "data/users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

def authenticate(username, password):
    users = load_users()
    if username not in users:
        return False
    return users[username] == hash_password(password)

# ✅ NEW FUNCTION
def reset_password(username, new_password):
    users = load_users()
    if username not in users:
        return False
    users[username] = hash_password(new_password)
    save_users(users)
    return True
