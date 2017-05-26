import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import json
import unittest
from typot.pull_request import PullRequest
from typot.model import Modification
import dummy_data as dd
import get_installation_id 


INSTALLATION_ID = get_installation_id.get()


class TestPullRequest(unittest.TestCase):

    def test_create_instance(self):
        pr_body = json.loads(dd.pull_request_created)
        pr = PullRequest.create_from_hook(pr_body)
        self.assertTrue(pr.title)
        self.assertTrue(pr.diff_url)

    def test_get_added(self):
        pr_body = json.loads(dd.pull_request_created)
        pr = PullRequest.create_from_hook(pr_body)
        file_contents = pr.get_added() 
        print(file_contents)
        self.assertEqual(len(file_contents), 1)

    def test_get_make_comments(self):
        pr = PullRequest.create("chakki-works", "typot-demo", "3")
        pr.installation_id = INSTALLATION_ID
        m = Modification("README.md", 1, "hoge", ["hoge-1", "hoge-2", "hoge-3"])
        r_id = pr.make_review([m])
        self.assertTrue(r_id)
        # you have to delete yourself!


if __name__ == "__main__":
    unittest.main()
