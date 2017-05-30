import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import unittest
from typot.model import DiffContent, Line
from typot.spell_checker import SpellChecker


class TestSpellChecker(unittest.TestCase):

    def test_spell_check(self):
        s = "My name iss John. I'm aesome singer."
        checker = SpellChecker()
        missed = checker.check(s)
        self.assertGreater(len(missed), 0)
        print(missed)

    def test_spell_check(self):
        f1 = DiffContent("test1.md", [
            Line(0, "I'm John."),
            Line(1, "I'm awesme singer."),
            Line(2, "Singer mst be star."),
        ])
        checker = SpellChecker()
        missed = checker.check(f1)
        self.assertGreater(len(missed), 0)
        print(missed)

if __name__ == "__main__":
    unittest.main()
