# -*- coding: utf-8 -*-

import os
from itertools import combinations
from typing import TextIO

import numpy as np
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
    filename: str = os.path.join('data', 'test.txt')
    filestream: TextIO = open(filename, 'r', newline=None)

    # anagrams: defaultdict[set] = defaultdict(set)
    anagrams: dict = {}

    for word in filestream:
        word = word.strip()
        if not iscandidate(word):
            continue

        intword: int = encode(word)
        if intword not in anagrams:
            anagrams[intword] = word

    filestream.close()

    # Now build a graph of words using the registered anagrams
    numwords: int = len(anagrams)
    graph: np.ndarray = np.zeros((numwords, numwords), dtype=np.uint8)
    allwords: list[int] = [*anagrams.keys()]
    for i, thisbitword in enumerate(allwords):
        for j, thatbitword in enumerate(allwords[i + 1:]):
            # If this and that word do not have bits in common, save them in the same set.
            if no_common_letters(thisbitword, thatbitword):
                graph[i, j + i + 1] = graph[j + i + 1, i] = 1

    # Now traverse the graph and detect cycles that consist of five steps
    print(graph)

    solutions: list[list[int]] = []
    nosolutions: list[set[int]] = []

    subgraph = np.zeros((5, 5), dtype=np.uint8)

    for i in tqdm(range(numwords)):  # Go word by word
        neighbours = np.where(graph[i, :] == 1)[0]
        for group in combinations(neighbours - 1, 5):  # -1 because the indices in the main graph change
            # Take links, but this first row can be excluded because we expect a fully filled first row
            subgraph[0, 1] = graph[group[0], group[1]]
            subgraph[0, 2] = graph[group[0], group[2]]
            subgraph[0, 3] = graph[group[0], group[3]]
            subgraph[0, 4] = graph[group[0], group[4]]

            subgraph[1, 2] = graph[group[1], group[2]]
            subgraph[1, 3] = graph[group[1], group[3]]
            subgraph[1, 4] = graph[group[1], group[4]]

            subgraph[2, 3] = graph[group[2], group[3]]
            subgraph[2, 4] = graph[group[2], group[4]]

            subgraph[3, 4] = graph[group[3], group[4]]

            print(subgraph)
            test = subgraph @ subgraph @ subgraph @ subgraph @ subgraph
            print(test)
            print(test.sum(0))

            # print(group)
            # print(next(product(group, group)))
            break

        break

    print(len(solutions))
