import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import unittest
from typot.pull_request import PullRequest
from typot.model import DiffContent, Line
import dummy_data as dd


class TestDiffContent(unittest.TestCase):

    def test_get_added(self):
        sample_diff = dd.diff_sample
        diff_contents = PullRequest._get_added(sample_diff)
        self.assertEqual(len(diff_contents), 1)
        modified = diff_contents[0]
        self.assertEqual(len(modified.contents), 3)

    def test_line_position(self):
        sample_diff = dd.diff_from_middle
        diff_contents = PullRequest._get_added(sample_diff)
        self.assertEqual(len(diff_contents), 1)
        line = diff_contents[0].contents[-1]
        self.assertEqual(line.line_no, 7)
        self.assertEqual(line.relative_no, 5)


if __name__ == "__main__":
    unittest.main()
