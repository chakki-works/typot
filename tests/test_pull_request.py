import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import json
import unittest
from typot.pull_request import PullRequest
import dummy_data as dd



class TestPullRequest(unittest.TestCase):

    def test_create_instance(self):
        pr_body = json.loads(dd.pull_request_created)
        pr = PullRequest.create(pr_body)
        self.assertTrue(pr.title)
        self.assertTrue(pr.diff_url)

    def test_get_added(self):
        pr_body = json.loads(dd.pull_request_created)
        pr = PullRequest.create(pr_body)
        added = pr.get_added() 
        print(added)
        self.assertEqual(len(added), 1)


if __name__ == "__main__":
    unittest.main()
