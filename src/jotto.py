# -*- coding: utf-8 -*-

import os
from string import ascii_lowercase
from typing import TextIO


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


def seen_before(a: int, b: int) -> bool:
    """Compute the AND of a and b, considering they have a leading 1."""
    return remove_leading_bit(a & b) != 0


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


def solve() -> None:
    """
    Solve the jotto problem: find five english words that are each five letters longs
    and which use 25 different letters of the western alphabet.
    """

    # Find the file and open it, start
    filename: str = os.path.join('data', 'words_alpha.txt')
    filestream: TextIO = open(filename, 'r', newline=None)

    # Initialise an empty set of solutions and start solving
    solutions: set = set()
    letters_taken: int = 0

    count = 0
    for word in filestream:
        word = word.strip()

        if not iscandidate(word):
            continue

        bitword: int = encode(word)
        # print(f'candidate {word} = {bitword:b}: {seen_before(bitword, letters_taken):b}')
        if not seen_before(bitword, letters_taken):
            # print("{:b}".format(seen_before(bitword, letters_taken)))
            # print("{:b}".format(bitword))

            solutions.add(word)
            letters_taken |= bitword
            print("letters_taken:    {:b}".format(letters_taken))
            input()

    # Cleanup
    filestream.close()
    print(count)
    print(solutions)
    print(len(solutions))
    assert len(solutions) == 538
