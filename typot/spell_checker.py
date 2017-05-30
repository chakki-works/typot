import enchant
from typot.model import DiffContent, Modification


class SpellChecker():

    def __init__(self, lang="en_US"):
        self.checker = enchant.Dict(lang)
    
    def check(self, target):
        if isinstance(target, DiffContent):
            return self.check_diff_content(target)
        else:
            return self.check_sentence(target)

    def check_sentence(self, sentence):
        words = self.tokenize(sentence)
        miss = {}
        if len(words) > 0:
            for w in words:
                if w and not self.checker.check(w):
                    miss[w] = self.checker.suggest(w)[:5]  # up to five
        
        return miss

    def check_diff_content(self, diff_content):
        modifications = []
        file_path = diff_content.file_path
        for c in diff_content.contents:
            result = self.check_sentence(c.text)
            if len(result) > 0:
                for r in result:
                    m = Modification(file_path, c.line_no, c.relative_no, r, result[r])
                    modifications.append(m)
        
        return modifications

    @classmethod
    def strip(cls, word):
        _w = word.strip()
        return _w.replace("\"", "").replace("'", "").replace(".", "").replace("?", "").replace("!", "")

    @classmethod
    def tokenize(cls, sentence):
        words = sentence.strip().split(" ")
        words = [cls.strip(w) for w in words]
        words = [w for w in words if w]
        return words
