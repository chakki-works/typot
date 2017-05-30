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
        diff_contents = pr.get_added() 
        print(diff_contents)
        self.assertEqual(len(diff_contents), 1)

    def test_make_review(self):
        pr = PullRequest.create("chakki-works", "typot-demo", "3")
        pr.installation_id = INSTALLATION_ID
        m = Modification("README.md", 1, "hoge", ["hoge-1", "hoge-2", "hoge-3"])
        r_id = pr.make_review([m])
        self.assertTrue(r_id)
        # you have to delete yourself!

    def test_read_modification(self):
        comment_hook_body = json.loads(dd.review_changed)
        pr = PullRequest.create_from_hook(comment_hook_body)
        modification = pr.read_modification(comment_hook_body)
        self.assertTrue(modification)
        self.assertEqual(modification.target_word, "hoge")
        self.assertEqual(modification.candidates[0], "hoge-2")

    def test_push_modification(self):
        pr_body = json.loads(dd.fix_target_pr)
        pr = PullRequest.create_from_hook(pr_body)
        pr.installation_id = INSTALLATION_ID
        m = Modification("content.md", 3, "relase", ["release"])
        pr.push_modification(m)


if __name__ == "__main__":
    unittest.main()
