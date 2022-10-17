# -*- coding: utf-8 -*-
import unittest
from string import ascii_lowercase

from src.jotto import encode, iscandidate, remove_leading_bit


class TestJottoHelperFunctions(unittest.TestCase):
    """Test some helper functions which help solve the jotto problem."""

    def setUp(self) -> None:
        self.words: list[str] = ['wacko', 'ceils', 'funky', 'zippo']

    def test_candidate(self) -> None:
        """Test whether the word is a good candidate for the solution."""
        self.assertTrue(iscandidate('wacko'))
        self.assertFalse(iscandidate('abarambo'))

    def test_remove_leading_bit(self) -> None:
        """Test whether we can correctly remove the first bit."""
        bitword: str = '101101101001011010010011001'
        value: int = int(bitword, base=2)
        result: int = remove_leading_bit(value)
        self.assertEqual(result, int(bitword[1:], 2))

    def test_word_encoding(self) -> None:
        """Test the correct encoding of a word."""
        for word in self.words:
            testword: str = ''.join(sorted(word))
            bitword: int = encode(word)
            self.assertIsInstance(bitword, int)
            self.assertEqual(bitword, encode(testword))
            self.assertEqual(len(f"{bitword:b}"), len(ascii_lowercase) + 1)


if __name__ == "__main__":
    unittest.main()
