# -*- coding: utf-8 -*-
import unittest
from string import ascii_lowercase

from src.jotto import encode, iscandidate, no_common_letters


class TestJottoHelperFunctions(unittest.TestCase):
    """Test some helper functions which help solve the jotto problem."""

    def setUp(self) -> None:
        self.words: list[str] = ['wacko', 'ceils', 'funky', 'ziplo']

    def test_candidate(self) -> None:
        """Test whether the word is a good candidate for the solution."""
        self.assertTrue(iscandidate('wacko'))
        self.assertFalse(iscandidate('wacko\n'))
        self.assertFalse(iscandidate('abarambo'))
        for word in self.words:
            self.assertTrue(iscandidate(word))

    def test_word_encoding(self) -> None:
        """Test the correct encoding of a word."""
        for word in self.words:
            testword: str = ''.join(sorted(word))
            bitword: int = encode(word)
            self.assertIsInstance(bitword, int)
            self.assertEqual(bitword, encode(testword))
            self.assertEqual(len(f"{bitword:b}"), len(ascii_lowercase) + 1)

    def test_no_common_letters(self) -> None:
        """Test whether we have seen this value before."""
        this: int = encode('wacko')
        that: int = encode('hufel')
        self.assertTrue(no_common_letters(this, that))
        self.assertFalse(no_common_letters(this, this))
        self.assertFalse(no_common_letters(that, that))

    def test_existing_solution(self) -> None:
        """Test an existing solution to see if it can be detected with our current tools."""
        words: list[str] = ['dwarf', 'glyph', 'jocks', 'muntz', 'vibex']
        result: int = 0
        for word in words:
            result |= encode(word)

        self.assertEqual(bin(result).count('1'), 25)

    def test_recursive_search(self) -> None:
        """Test whether the rec"""


if __name__ == "__main__":
    unittest.main()
