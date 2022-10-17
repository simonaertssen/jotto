# -*- coding: utf-8 -*-
import unittest
from string import ascii_lowercase

from src.jotto import decode, encode, iscandidate, remove_leading_bit


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
        self.assertEqual(int('1' * 26, 2), remove_leading_bit(int('1' * 27, 2)))

    def test_word_encoding(self) -> None:
        """Test the correct encoding of a word."""
        for word in self.words:
            testword: str = ''.join(sorted(word))
            bitword: int = encode(word)
            self.assertIsInstance(bitword, int)
            self.assertEqual(bitword, encode(testword))
            self.assertEqual(len(f"{bitword:b}"), len(ascii_lowercase) + 1)

    # def test_encoding_leading_mask(self) -> None:
    #     """Test whether we can remove the leading 1 from a number."""
    #     for word in ['wacko', 'ceils', 'funky']:
    #         bitword: int = encode(word)

    def test_word_decoding(self) -> None:
        """Test the correct decoding of a word."""
        for w in self.words:
            print(w)
            self.assertEqual(set(w), set(decode(encode(w))))


if __name__ == "__main__":
    unittest.main()
