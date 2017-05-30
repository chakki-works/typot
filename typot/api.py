import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import hug
from typot.pull_request import PullRequest
from typot.spell_checker import SpellChecker


version = 1


@hug.get("/ping", versions=version)
@hug.local()
def ping():
    return {"ping": "works fine!"}


@hug.post("/typot", versions=version)
@hug.local()
def typot(body=None):
    if not body:
        return {}
    
    response = {}
    if body["action"] == "opened" and "pull_request" in body:
        # open the pull request
        pr = PullRequest.create_from_hook(body)
        diff_contents = pr.get_added()
        checker = SpellChecker()

        modifications = []
        for c in diff_contents:
            file_modifications = checker.check(c)
            if len(file_modifications) > 0:
                modifications += file_modifications
        
        if len(modifications) > 0:
            pr.make_review(modifications)
            response = {"message": "create pull request review"}

    elif body["action"] == "edited" and "pull_request" in body and "comment" in body:
        commented_user = body["comment"]["user"]["login"]
        if commented_user == "typot[bot]":
            pr = PullRequest.create_from_hook(body)
            modification = pr.read_modification(body)
            if modification:
                result = pr.push_modification(modification)
                if result:
                    response = {"message": "apply modification"}
                else:
                    response = {"message": "apply is not adopted"}

    return response
