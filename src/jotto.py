# -*- coding: utf-8 -*-

import os
from typing import TextIO


def iscandidate(word: str, wordlen: int = 5) -> bool:
    """
    Idenitfy whether the word is a candidate for our solution.
    Assume the word is lowercase.
    """

    return len(set(word)) == len(word) == wordlen


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


def has_letter(bitword: int, letter: int):
    """Test whether a word has a certain letter by simple bit operations."""
    return (bitword >> letter & 1) == 1


def no_common_letters(this: int, that: int) -> bool:
    """Compute the AND of a and b, considering they have a leading 1."""
    return (this & that) == 0


def build_graph(wordmap: dict[int: str]) -> dict[int: set[int]]:
    """
    Build a map from the different bitwords that exist in the dataset.
    This can be done by visiting all other words in the vector with
    encoded words. Hence, we only map a directed graph.
    """
    allwords: list[int] = [*wordmap.keys()]
    graph: dict[int: set[int]] = {}
    for bitword in allwords:
        graph[bitword] = set()

    for i, thisbitword in enumerate(allwords):
        for thatbitword in allwords[i + 1:]:
            # If this and that word do not have bits in common, save them in the same set.
            if no_common_letters(thisbitword, thatbitword):
                graph[thisbitword].add(thatbitword)

    return graph


def solve() -> None:
    """
    Solve the jotto problem: find five english words that are each five letters longs
    and which use 25 different letters of the western alphabet.
    """

    # Find the file and open it, start building a database of words
    filename: str = os.path.join('data', 'words_alpha.txt')
    filestream: TextIO = open(filename, 'r', newline=None)

    # anagrams: defaultdict[set] = defaultdict(set)
    anagrams: dict = {}

    # To prevent looking through the entire dataset to find a word with a certain
    # letter, we can identify which letters appear in what words.
    words_with: list[list[int]] = [[] * 26]

    for word in filestream:
        word = word.strip()
        if not iscandidate(word):
            continue

        intword: int = encode(word)
        if intword not in anagrams:
            anagrams[intword] = word

        # Find integer of letter by subtracting with ord('a') = 97
        words_with[ord(word[0]) - 97].append(intword)
        words_with[ord(word[1]) - 97].append(intword)
        words_with[ord(word[2]) - 97].append(intword)
        words_with[ord(word[3]) - 97].append(intword)
        words_with[ord(word[4]) - 97].append(intword)

    filestream.close()

    # Now we need to build a few datastructures to help us understand the data.
    # Build a graph of words using the registered anagrams:
    # bitgraph: dict[int: set(int)] = build_graph(anagrams)

    solutions: list[list[int]] = []
    solutionhashes: list[int] = []

    candidates: list[int] = []
    newcandidates: list[int] = []
    for i in range(26):  # Loop over the index of the letters in the alphabet
        newcandidates.clear()

        for tryme in candidates:  # Test the currently available candidates

            for word_with_i in words_with[i]:
                # Such a word must not share letters with our candidate
                if no_common_letters(tryme, word_with_i):
                    continue
                new_cand = tryme | word_with_i
                # Here were using `deconstructions` to simultaneously
                # keep track of whether we've seen this candidate already
                # (if so, we don't want to search it again), and to keep
                # track of the different ways we've built the candidate.
                if new_cand not in deconstructions:
                    new_candidates.append((new_cand, skipped))
