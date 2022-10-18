# -*- coding: utf-8 -*-

import os
from collections import defaultdict
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

    anagrams: defaultdict[set] = defaultdict(set)
    for word in filestream:
        word = word.strip()
        if not iscandidate(word):
            continue

        intword: int = encode(word)
        anagrams[intword].add(word)

    filestream.close()

    # Now build a graph of words using the registered anagrams
    bitgraph: defaultdict[set] = defaultdict(set)

    bitwords: list[int] = sorted(anagrams.keys())
    for i, thisbitword in enumerate(bitwords):
        for thatbitword in bitwords[i + 1:]:
            # If this and that word do not have bits in common,
            # save them in the same set.
            if not (thisbitword & thatbitword):
                bitgraph[thisbitword].add(thatbitword)

    # solutions: set = set()
    # for k, s in bitgraph.items():

    # def recursive_search(bitgraph: dict, word: int, neighbours: set[int], chain: int, length: int) -> set:
    #     """
    #     Recursively search solutions by testing words that could fit onto the chain.

    #     bitgraph    (dict): stores the mapping from a word to all other words that have no letter in common.
    #     word        (int): the current word.
    #     neighbours  (set): words that have no letters in common with the word.
    #     chain       (int): the hash of the current chain of words.
    #     length      (int): the length of the current chain of words.
    #     """
    #     for nghbr in bitgraph[word]:
    #         if not (nghbr & chain):

    res = encode('dwarf')
    print(bitgraph[res])
    # print(bitgraph[anagrams[res]])
