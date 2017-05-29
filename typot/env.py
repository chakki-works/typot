import os
import json
from datetime import datetime, timedelta
import jwt
import requests


def get_private_pem():
    key = os.environ.get("PRIVATE_KEY", "")
    if not key:
        default_path = os.path.join(os.path.dirname(__file__), "../typot.pem")
        if os.path.exists(default_path):
            with open(default_path, "r", encoding="utf-8") as f:
                key = f.readlines()
                key = "".join(key)

    return key


def get_client_id():
    return _get_env("CLIENT_ID")


def get_client_secret():
    return _get_env("CLIENT_SECRET")

def make_auth_header(installation_id):
    utcnow = datetime.utcnow() + timedelta(seconds=-5)
    duration = timedelta(seconds=30)
    payload = {
        "iat": utcnow,
        "exp": utcnow + duration,
        "iss": 2510
    }
    pem = get_private_pem()
    encoded = jwt.encode(payload, pem, "RS256")
    headers = {
        "Authorization": "Bearer " + encoded.decode("utf-8"),
        "Accept": "application/vnd.github.machine-man-preview+json"
        }
    
    auth_url = "https://api.github.com/installations/{}/access_tokens".format(installation_id)
    r = requests.post(auth_url, headers=headers)

    if not r.ok:
        print(r.json()["message"])
        r.raise_for_status()
    token = r.json()["token"]
    return {
        "Authorization": "token {}".format(token)
    }

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
