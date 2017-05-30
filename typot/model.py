class Line():

    def __init__(self, line_no, text, relative_no=-1):
        self.line_no = line_no
        self.text = text
        self.relative_no = line_no if relative_no == -1 else relative_no


class DiffContent():

    def __init__(self, file_path, contents=()):
        self.file_path = file_path
        self.contents = contents

    def __repr__(self):
        return "{}<{}:{} lines>".format(
            self.__class__.__name__,
            self.file_path,
            len(self.contents))


class Modification():

    def __init__(self, file_path, line_no, relative_no, target_word, candidates):
        self.file_path = file_path
        self.line_no = line_no  # line no starts from 1
        self.relative_no = relative_no  # line no starts from 1
        self.target_word = target_word
        self.candidates = candidates

    def __repr__(self):
        return "{}<{}, {}@{}>".format(
            self.__class__.__name__,
            self.file_path, self.target_word, self.line_no)
