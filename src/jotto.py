# -*- coding: utf-8 -*-

import os
from typing import TextIO


def iscandidate(word: str, wordlen: int = 5) -> bool:
    """
    Idenitfy whether the word is a candidate for our solution.
    Assume the word is lowercase.
    """
    return len(word) == wordlen and not {"a", "e", "i", "o", "u"}.isdisjoint(word)


def encode(word: str) -> int:
    """
    Encode a word for fast comparisons: index which letters are being used.
    Assume the word is lowercase and consists of 5 letters.
    """
    ret: int = 0
    a: int = ord("a")
    ret |= 1 << (ord(word[0]) - a)
    ret |= 1 << (ord(word[1]) - a)
    ret |= 1 << (ord(word[2]) - a)
    ret |= 1 << (ord(word[3]) - a)
    ret |= 1 << (ord(word[4]) - a)
    return ret


def solve() -> None:
    """
    Solve the jotto problem: find five english words that are each five letters longs
    and which use 25 different letters of the western alphabet.
    """

    # Find the file and open it, start building a database of words
    filename: str = os.path.join('data', 'words_alpha.txt')
    filestream: TextIO = open(filename, 'r', newline=None)

    anagrams: dict[list] = {}
    for word in filestream:
        word = word.strip()
        if not iscandidate(word):
            continue

        intword: int = encode(word)
        if word not in anagrams:
            anagrams[intword] = [word]
        else:
            anagrams[intword].append(word)

    # Initialise an empty set of solutions and start solving
    solutions: set = set()

    for word in filestream:
        word = word.strip()

        if not iscandidate(word):
            continue

        bitword: int = encode(word)
        # print(f"{bitword:b}")
        # print(ascii_lowercase)
        # print(f'candidate {word} = {bitword:b}: {seen_before(bitword, letters_taken):b}')
        if not seen_before(bitword, letters_taken):
            # print("{:b}".format(seen_before(bitword, letters_taken)))
            # print("{:b}".format(bitword))

            solutions.add(word)
            # print(f"{bitword:b}")
            # input()

    # Cleanup
    filestream.close()
    print(solutions)
    print(len(solutions))
    assert len(solutions) == 538
