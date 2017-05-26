import os
import json


def get():
    path = os.path.join(os.path.dirname(__file__), "./test_installation_id.json")
    if not os.path.exists(path):
        raise Exception(
            "You have to prepare test_installation_id.json in tests folder. \n That has 'installation_id': (your test app's installation id)"
            )
    installation_id = ""
    with open(path, encoding="utf-8") as f:
        body = json.load(f)
        installation_id = body["installation_id"]
    
    return installation_id
