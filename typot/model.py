class Line():

    def __init__(self, line_no, text):
        self.line_no = line_no
        self.text = text


class FileContent():

    def __init__(self, file_path, contents=()):
        self.file_path = file_path
        self.contents = contents

    def __repr__(self):
        return "{}<{}:{} lines>".format(
            self.__class__.__name__,
            self.file_path,
            len(self.contents))


class Modification():

    def __init__(self, file_path, line_no, target_word, candidates):
        self.file_path = file_path
        self.line_no = line_no
        self.target_word = target_word
        self.candidates = candidates

    def __repr__(self):
        return "{}<{}, {}@{}>".format(
            self.__class__.__name__,
            self.file_path, self.target_word, self.line_no)
