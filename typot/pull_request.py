from io import StringIO
import re
import base64
import requests
from unidiff import PatchSet
from unidiff.constants import LINE_TYPE_ADDED
from typot.env import make_auth_header
from typot.model import Line, DiffContent, Modification
from typot.spell_checker import SpellChecker


class PullRequest():
    API_ROOT = "https://api.github.com"

    def __init__(self, 
        title="", 
        no=-1, 
        owner="",
        repo="",
        head_owner="",
        head_repo="",
        head_ref="",
        diff_url="",
        installation_id=""
        ):
        
        self.title = title
        self.no = no
        self.owner = owner
        self.repo = repo
        self.head_owner = head_owner
        self.head_repo = head_repo
        self.head_ref = head_ref
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
        head_ref = pr["head"]["ref"]
        diff_url = pr["diff_url"]

        return PullRequest(title, no, owner, repo, head_owner, head_repo, head_ref, diff_url)

    def get_added(self):
        diff = requests.get(self.diff_url).content.decode("utf-8")
        return self._get_added(diff)
    
    @classmethod
    def _get_added(cls, diff):
        patches = PatchSet(StringIO(diff))
        
        diff_contents = []
        for p in patches:
            if p.added > 0:
                contents = []
                for h in p:
                    added = []
                    for i, line in enumerate(h):
                        if line.is_added:
                            added_line = Line(line.target_line_no, line.value, i + 1)
                            added.append(added_line)
                    contents += added
                diff_contents.append(
                    DiffContent(p.path, contents)
                    )

        return diff_contents        

    def make_review(self, modifications):
        url = self.API_ROOT + "/repos/{}/{}/pulls/{}/reviews".format(
            self.owner, self.repo, self.no
        )

        comments = []
        for m in modifications:
            body = "\"{}\" at {} is typo? \n".format(m.target_word, m.line_no)
            body += "\n".join(["- [ ] {}".format(c) for c in m.candidates])

            # comment should be done by relative no
            c = {
                "path": m.file_path,
                "position": m.relative_no,
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
            print(payload)
            print(r.json())
            r.raise_for_status()
        else:
            review_id = r.json()["id"]

        return review_id
    
    @classmethod
    def read_modification(cls, review_comment_hook):
        if "comment" not in review_comment_hook:
            return None
        comment_body = review_comment_hook["comment"]
        file_path = comment_body["path"]
        relative_no = int(comment_body["position"])
        body = comment_body["body"]
        r = requests.get(comment_body["url"])
        if r.ok:
            body = r.json()["body"]  # get latest body

        target_word = ""
        candidates = []

        line_no = re.search("at\s\d+\sis", body)
        if line_no is not None:
            line_no = int(line_no.group(0).split()[1])
        else:
            line_no =relative_no
        words = re.search("\"(\w|-|_)+(\.|\?|\!)?\"", body)
        if words is not None:
            target_word = words.group(0).replace("\"", "")
        mods = re.search("\[x\]\s(\w|-|_)+\n", body)
        if mods is not None:
            c = mods.group(0)
            c = c.strip().replace("[x] ", "")
            candidates = [c]

        if target_word and len(candidates) > 0:
            m = Modification(file_path, line_no, relative_no, target_word, candidates)
            return m
        else:
            return None

    def push_modification(self, modification):
        url = self.API_ROOT + "/repos/{}/{}/contents/{}".format(
            self.head_owner, self.head_repo, modification.file_path
        )

        r = requests.get(url, params={"ref": self.head_ref})
        if not r.ok:
            raise Exception("Can not access to the {}/{}'s content.".format(
                self.head_owner, self.head_repo
            ))
        encoding = r.encoding
        body = r.json()
        content = body["content"]
        content = base64.b64decode(content).decode(encoding)
        sha = body["sha"]
        fix_position = int(modification.line_no) - 1  # read file lines start with 0
        fixed = content
        with StringIO(content) as c:
            lines = c.readlines()
            words = lines[fix_position].split(" ")
            for i, w in enumerate(words):
                _w = SpellChecker.strip(w.strip())
                if _w == modification.target_word:
                    words[i] = words[i].replace(_w, modification.candidates[0])
            
            fixed = " ".join(words) + "\n"
            lines[fix_position] = fixed
            fixed = "".join(lines)
        
        if content != fixed:
            encoded = base64.b64encode(fixed.encode(encoding)).decode(encoding)
            message = "fix typo: {} to {}, line {}".format(
                modification.target_word,
                modification.candidates[0],
                modification.line_no
                )

            payload = {
                "message": message,
                "content": encoded,
                "sha": sha,
                "branch": self.head_ref
            }
            r = requests.put(url, json=payload,headers=make_auth_header(self.installation_id))

            if not r.ok:
                print(r.json())
                r.raise_for_status()
            return True
        
        return False
