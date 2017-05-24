import os
import json


def get_private_key():
    key = os.environ.get("PRIVATE_KEY", "")
    if not key:
        default_path = os.path.join(os.path.dirname(__file__), "../typot.pem")
        if os.path.exists(default_path):
            with open(default_path, "r", encoding="utf-8") as f:
                key = f.readlines()

    return key


def get_client_id():
    return _get_env("CLIENT_ID")


def get_client_secret():
    return _get_env("CLIENT_SECRET")


def _get_env(key_name, default_value=""):
    env = os.environ.get(key_name, "")
    if not env:
        env_path = os.path.join(os.path.dirname(__file__), "../envs.json")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                envs = json.load(f)
                if key_name in envs:
                    env = envs[key_name]
    return env
