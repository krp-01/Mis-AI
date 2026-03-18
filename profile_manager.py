import json
import os

USERS_FOLDER = "users"
HISTORY_FOLDER = "history"


def ensure_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def get_user_file(username):
    ensure_folder(USERS_FOLDER)
    return os.path.join(USERS_FOLDER, f"{username}.json")


def get_history_file(username):
    ensure_folder(HISTORY_FOLDER)
    return os.path.join(HISTORY_FOLDER, f"{username}_history.json")


def user_exists(username):
    return os.path.exists(get_user_file(username))


def save_profile(username, profile):
    with open(get_user_file(username), "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=4)


def load_profile(username):
    file_path = get_user_file(username)

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(username, history):
    with open(get_history_file(username), "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)


def load_history(username):
    file_path = get_history_file(username)

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
