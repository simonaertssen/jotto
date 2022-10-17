# -*- coding: utf-8 -*-

import os
import re
from string import ascii_lowercase
from typing import Generator, TextIO


def iscandidate(word: str, wordlen: int = 5) -> bool:
    """
    Idenitfy whether the word is a candidate for our solution.
    Assume the word is lowercase.
    """
    return len(word) == wordlen and len(set(word)) == wordlen


def remove_leading_bit(x: int) -> int:
    """
    Remove the leading 1 that encodes front trailing zeros.
    This is done using a bitwise and with hex(2**26 - 1) = 0x3ffffff.
    """
    return x & 0x3ffffff


def encode(word: str) -> int:
    """
    Encode a word for fast comparisons: index which letters are being used.
    Assume the word is lowercase and consists of 5 letters.
    """
    sortword: str = [ascii_lowercase.index(letter) for letter in sorted(word)]
    bitword: str = '1' + '0' * sortword[0] + '1'  # Prepend with a one, otherwise we cannot store leading zeros
    bitword += '0' * (sortword[1] - sortword[0] - 1) + '1'
    bitword += '0' * (sortword[2] - sortword[1] - 1) + '1'
    bitword += '0' * (sortword[3] - sortword[2] - 1) + '1'
    bitword += '0' * (sortword[4] - sortword[3] - 1) + '1'
    bitword += '0' * (26 - sortword[4] - 1)   # Pad with 0's
    return int(bitword, base=2)


def seen_before(a: int, b: int) -> bool:
    """Compute the AND of a and b, considering they have a leading 1."""
    return (a & b) ^ (2**26 - 1)


def decode(intword: str) -> int:
    """
    Decode an integer to a string: index which letters are being used.
    Assume the word is lowercase and consists of 5 letters.
    """
    print(f"{intword:b}")
    maskedword: int = intword & (2**26 - 1)  # Mask the leading bit
    print(f"{maskedword:b}")

    ones: Generator = re.finditer('1', f"{intword:b}")
    next(ones)  # Skip the leading 1

    ones = list(ones)
    print([m.start() - 1 for m in ones])
    letters: list = [ascii_lowercase[i.start() - 1] for i in ones]
    return ''.join(letters)


def solve() -> None:
    """
    Solve the jotto problem: find five english words that are each five letters longs
    and which use 25 different letters of the western alphabet.

    filename: str = path to the file containing English words
    """

    # Find the file and open it, start
    filename: str = os.path.join('data', 'words_alpha.txt')
    filestream: TextIO = open(filename, 'r', newline=None)

    # Initialise an empty set of solutions and start solving
    solutions: set = set()
    letters_taken: int = 0
    for word in filestream:
        word = word.strip()

        if not iscandidate(word):
            continue

        bitword: int = encode(word)
        if not seen_before(bitword, letters_taken):
            print(word)
            print("{:b}".format(bitword))
            print("{:b}".format(letters_taken))

            solutions.add(word)
            letters_taken ^= bitword

            input()

    # Cleanup
    filestream.close()

    print(solutions)
    print(len(solutions))
    assert len(solutions) == 538
