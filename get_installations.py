import os
import argparse
from datetime import datetime, timedelta
import requests
import jwt


def get_private_pem(file_path):
    key = os.environ.get("PRIVATE_KEY", "")
    if not key:
        default_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(default_path):
            with open(default_path, "r", encoding="utf-8") as f:
                key = f.readlines()
                key = "".join(key)

    return key


parser = argparse.ArgumentParser(description="Get Installations count of your App.")
parser.add_argument("app_id", help="app_id of Your apps")
parser.add_argument("--pem", default="", help="path to pem file")


if __name__ == "__main__":
    url = "https://api.github.com/app/installations"

    args = parser.parse_args()

    pem_path = args.pem
    if not pem_path:
        path = os.path.abspath(os.path.dirname(__file__))
        app_name = os.path.basename(path)
        pem_path = app_name + ".pem"
    
    if not os.path.exists(pem_path):
        raise Exception("Pem file {} does not exist".format(pem_path))

    utcnow = datetime.utcnow() + timedelta(seconds=-5)
    duration = timedelta(seconds=10)
    payload = {
        "iat": utcnow,
        "exp": utcnow + duration,
        "iss": args.app_id
    }
    pem = get_private_pem(pem_path)
    encoded = jwt.encode(payload, pem, "RS256")
    headers = {
        "Authorization": "Bearer " + encoded.decode("utf-8"),
        "Accept": "application/vnd.github.machine-man-preview+json"
        }
    
    r = requests.get(url, headers=headers)
    if r.ok:
        print(len(r.json()))
    else:
        r.raise_for_status()
