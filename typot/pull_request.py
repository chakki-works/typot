from io import StringIO
import requests
from unidiff import PatchSet
from unidiff.constants import LINE_TYPE_ADDED
from typot.env import make_auth_header
from typot.model import Line, FileContent


class PullRequest():
    API_ROOT = "https://api.github.com"

    def __init__(self, 
        title="", 
        no=-1, 
        owner="",
        repo="",
        head_owner="", 
        head_repo="",
        diff_url="",
        installation_id=""
        ):
        
        self.title = title
        self.no = no
        self.owner = owner
        self.repo = repo
        self.head_owner = head_owner
        self.head_repo = head_repo
        self.diff_url = diff_url
        self.installation_id = installation_id
    
    @classmethod
    def create(cls, owner, repo, pull_id):
        url = cls.API_ROOT + "/repos/{}/{}/pulls/{}".format(owner, repo, pull_id)
        r = requests.get(url)
        return cls._create_from_json(r.json())

    @classmethod
    def create_from_hook(cls, webhook_body):
        if "pull_request" not in webhook_body:
            return None
        pr = webhook_body["pull_request"]
        ins = cls._create_from_json(pr)
        ins.installation_id = webhook_body["installation"]["id"]
        return ins
    
    @classmethod
    def _create_from_json(cls, pr):
        title = pr["title"]
        no = pr["number"]
        owner = pr["base"]["repo"]["owner"]["login"]
        repo = pr["base"]["repo"]["name"]
        head_owner = pr["head"]["repo"]["owner"]["login"]
        head_repo = pr["head"]["repo"]["name"]
        diff_url = pr["diff_url"]

        return PullRequest(title, no, owner, repo, head_owner, head_repo, diff_url)

    def get_added(self):
        diff = requests.get(self.diff_url).content.decode("utf-8")
        patches = PatchSet(StringIO(diff))
        
        file_contents = []
        for p in patches:
            if p.added > 0:
                contents = []
                for h in p:
                    added = [
                        Line(ln.target_line_no, ln.value) 
                        for ln in h.target_lines() 
                        if ln.line_type == LINE_TYPE_ADDED
                        ]
                    contents += added
                file_contents.append(
                    FileContent(p.path, contents)
                    )

        return file_contents
    
    def make_review(self, modifications):
        url = self.API_ROOT + "/repos/{}/{}/pulls/{}/reviews".format(
            self.owner, self.repo, self.no
        )

        comments = []
        for m in modifications:
            body = "\"{}\" is typo? \n".format(m.target_word)
            body += "\n".join(["- [ ] {}".format(c) for c in m.candidates])

            c = {
                "path": m.file_path,
                "position": m.line_no,
                "body": body
            }
            comments.append(c)
        
        review_id = None
        payload = {
            "body": "Review from typot",
            "event": "COMMENT",
            "comments": comments
        }
        r = requests.post(url, json=payload, headers=make_auth_header(self.installation_id))
        if not r.ok:
            print(r.json())
            r.raise_for_status()
        else:
            review_id = r.json()["id"]

        return review_id
    
    def apply_fix(self, description):
        CONTENT_API = self.API_ROOT + "/repos/{}/{}/{}"

        req = []
        for m in modifications:
            api = CONTENT_API.format(self.head_owner, self.head_repo, m.file_path)
            r = requests.get(api)
        pass
