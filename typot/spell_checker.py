import enchant
from typot.model import FileContent, Modification


class SpellChecker():

    def __init__(self, lang="en_US"):
        self.checker = enchant.Dict(lang)
    
    def check(self, target):
        if isinstance(target, FileContent):
            return self.check_file_content(target)
        else:
            return self.check_sentence(target)

    def check_sentence(self, sentence):
        words = sentence.split(" ")
        words = [w.strip() for w in words]

        miss = {}
        for w in words:
            if not self.checker.check(w):
                miss[w] = self.checker.suggest(w)[:5]  # up to five
        
        return miss

    def check_file_content(self, file_content):
        modifications = []
        file_path = file_content.file_path
        for c in file_content.contents:
            result = self.check_sentence(c.text)
            if len(result) > 0:
                for r in result:
                    m = Modification(file_path, c.line_no, r, result[r])
                    modifications.append(m)
        
        return modifications
