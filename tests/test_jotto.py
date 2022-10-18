# -*- coding: utf-8 -*-
import unittest
from string import ascii_lowercase

from src.jotto import encode, iscandidate, remove_leading_bit, seen_before


class TestJottoHelperFunctions(unittest.TestCase):
    """Test some helper functions which help solve the jotto problem."""

    def setUp(self) -> None:
        self.words: list[str] = ['wacko', 'ceils', 'funky', 'ziplo']

    def test_candidate(self) -> None:
        """Test whether the word is a good candidate for the solution."""
        self.assertTrue(iscandidate('wacko'))
        self.assertFalse(iscandidate('wacko\n'))
        self.assertFalse(iscandidate('abarambo'))
        self.assertFalse(iscandidate('bcdfg'))
        for word in self.words:
            self.assertTrue(iscandidate(word))

    def test_remove_leading_bit(self) -> None:
        """Test whether we can correctly remove the first bit."""
        bitword: str = '100000000000101001000000000'
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

    def test_seen_before(self) -> None:
        """Test whether we have seen this value before."""
        bitval1: int = int('101101101001011010010011001', 2)
        bitval2: int = int('110010010110100101101100110', 2)
        self.assertFalse(seen_before(bitval1, bitval2))
        self.assertTrue(seen_before(bitval1, bitval1))
        self.assertTrue(seen_before(bitval2, bitval2))

        bitval1: int = int('100000001001011010010011001', 2)
        bitval2: int = int('100000000110100101101100110', 2)
        self.assertFalse(seen_before(bitval1, bitval2))
        self.assertTrue(seen_before(bitval1, bitval1))
        self.assertTrue(seen_before(bitval2, bitval2))

    def test_existing_solution(self) -> None:
        """Test an existing solution to see if it can be detected with our current tools."""
        words: list[str] = ['dwarf', 'glyph', 'jocks', 'muntz', 'vibex']
        result: int = 0
        for word in words:
            result |= encode(word)

        result = remove_leading_bit(result)
        self.assertEqual(bin(result).count('1'), 25)


if __name__ == "__main__":
    unittest.main()
