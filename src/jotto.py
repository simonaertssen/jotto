# -*- coding: utf-8 -*-

import os
from collections import defaultdict
from typing import TextIO

from tqdm import tqdm


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


def no_common_letters(this: int, that: int) -> bool:
    """Compute the AND of a and b, considering they have a leading 1."""
    return (this & that) == 0


def recursive_search(bitgraph: dict, rosetta: dict, chain: set, chainhash: int, word: int) -> set:
    """
    Recursively search solutions by testing words that could fit onto the chain.
    bitgraph    (dict): stores the mapping from a word to all other words that have no letter in common.
    rosetta     (dict): translate the word as an integer to the word as a string.
    word        (int): the current word under review.
    chain       (set): the chain of words that share no letters.
    chainhash   (int): the hash of the current chain of words.
    """
    solutions: set = set()
    for nghbr in bitgraph[word]:
        if no_common_letters(nghbr, chainhash):
            chain.add(rosetta[nghbr])

            if len(chain) == 5:
                encode: str = (str(link) for link in sorted(chain))
                solutions.add(':'.join(encode))

            result: set = recursive_search(bitgraph, rosetta, chain, nghbr & chainhash, nghbr)
            solutions.union(result)

    return solutions


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
            if no_common_letters(thisbitword, thatbitword):
                bitgraph[thisbitword].add(thatbitword)

    solution: set = set()
    for (anchor, chain) in tqdm(bitgraph.items()):
        for link in chain:
            chainset: set = {anchor, link}
            chainsethash: int = (anchor & link)
            solution.union(recursive_search(bitgraph, anagrams, chain=chainset,
                                            chainhash=chainsethash, word=link))

    print(len(solution))

    # res = encode('dwarf')
    # print(bitgraph[res])
    # print(bitgraph[anagrams[res]])
