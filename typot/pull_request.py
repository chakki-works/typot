from io import StringIO
import requests
from unidiff import PatchSet
from unidiff.constants import LINE_TYPE_ADDED


class PullRequest():

    def __init__(self, title="", diff_url=""):
        self.title = title
        self.diff_url = diff_url

    @classmethod
    def create(cls, webhook_body):
        if "pull_request" not in webhook_body:
            return None
        pr = webhook_body["pull_request"]
        title = pr["title"]
        diff_url = pr["diff_url"]

        return PullRequest(title, diff_url)
    
    def get_added(self):
        diff = requests.get(self.diff_url).content.decode("utf-8")
        patches = PatchSet(StringIO(diff))
        
        added_content = {}
        for p in patches:
            if p.added > 0:
                total = []
                for h in p:
                    added = [
                        (ln.target_line_no, ln.value) for ln in h.target_lines() if ln.line_type == LINE_TYPE_ADDED
                        ]
                    total += added
                added_content[p.path] = total

        return added_content
    
    def make_review_comment(self, descriptions):
        """
        make review comments provided by typo checking
        """
        pass
    
    def apply_fix(self, description):
        """
        apply fix
        """
        pass
