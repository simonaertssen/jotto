# -*- coding: utf-8 -*-

import time
from collections import defaultdict

# from src.jotto import solve


def solve():
    with open(r'data/words_alpha.txt', 'r') as f:
        words = f.read().split()

    def can_be_used(word):
        return len(word) == len(set(word)) == 5

    words = list(filter(can_be_used, words))

    def word_to_int(word):
        return sum(1 << (ord(c) - 97) for c in word)  # 97 = ord('a')

    def int_to_letters(n):
        return ''.join(chr(i + 97) for i in range(26) if n >> i & 1)

    # A list of all our int-encoded words.
    ints = sorted(set(map(word_to_int, words)))

    # For each letter, find `has[letter]`, the list of words that
    # contain that letter. This way we don't have to look through
    # the entire word list just to find a word with an 'X' in it.
    has = [[n for n in ints if n >> i & 1] for i in range(26)]

    # Count how many times each letter occurs in the word list in
    # total. That way we can start with the least common letters.
    counts = list(map(len, has))

    # Using `counts` we find the list of int-encodings for every
    # letter, when those letters are sorted from rare to common.
    alphabet = sorted(range(26), key=lambda letter: counts[letter])
    # To get check that this list is correct, uncomment this:
    # print([int_to_word(1<<i) for i in alphabet])
    # It should print a list, starting with rare letters like 'q'
    # and 'j', and ending with common ones, like 'a' and 'e'.

    solutions = []

    deconstructions = defaultdict(list)

    # The main loop.
    # The basic idea is to start by trying to include the
    # least common letters in the solution. This keeps
    # early branching to a minimum.
    # We start with a single candidate (partial solution)
    # which we represent as (0, 0).
    # The first zero is the int-encoding of the empty string
    # and the second zero is the number of letters we've
    # skipped. This means:
    #  - Our search space is all strings that contain
    #    the empty string (i.e. all of them for now).
    #  - In this search space, we skip at least 0 of
    #    the letters in our alphabet.
    # Of course, we cannot skip more than 1 letter, because
    # our solution will be 25 letter, and there are only 26
    # letters in the alphabet. So if the `skipped` number
    # ever exceeds 1, we can stop exploring that candidate.
    # During each iteration, we refine our search space
    # by splitting it off into different possibilities--
    # new, more specific candidates--by adding words to the
    # candidates, or skipping letters.
    # You may think of "candidate" and "part of the search space"
    # interchangeably.
    # If we find a solution, we add it to the solutions list
    # and stop exploring that candidate, because there are
    # no solutions that are strict supersets of other solutions.
    candidates = [(0, 0)]
    for i in alphabet:  # i is the int-encoding of a letter
        # The next, more refined part the search space
        new_candidates = []
        for cand, skipped in candidates:
            # Check if a solution has been found
            if bin(cand).count('1') == 25:
                solutions.append(cand)
                # Continue = stop searching in this candidate
                continue
            # Check if we've skipped too many letters
            if skipped > 26 - 25:
                continue
            # Sometimes, the letter is already in our candidate.
            # If so, just carry it over to the next search space.
            if cand >> i & 1:
                new_candidates.append((cand, skipped))
                continue
            # If the letter is not in the candidate, one option
            # is to just skip it.
            new_candidates.append((cand, skipped + 1))
            # But we can also find a word that has the letter in it,
            # and add that word to the candidate.
            for other in has[i]:
                # Such a word must not share letters with our candidate
                if (cand & other):
                    continue
                new_cand = cand | other
                # Here were using `deconstructions` to simultaneously
                # keep track of whether we've seen this candidate already
                # (if so, we don't want to search it again), and to keep
                # track of the different ways we've built the candidate.
                if new_cand not in deconstructions:
                    new_candidates.append((new_cand, skipped))
                # Reminder: the point of `deconstructions` is so we know
                # how to build our solution when we've found it.
                deconstructions[new_cand].append((cand, other))
        candidates = new_candidates
        # To diagnose which loops take the longest:
        # print(len(candidates), set(bin(cand).count('1') for cand, _ in candidates))

    # Find `sources[n]`, the list of words in our word list
    # which have n as their int-encoding.
    sources = defaultdict(list)
    for word in words:
        if len(word) == len(set(word)) == 5:
            sources[word_to_int(word)].append(word)

    # We can now find every way to deconstruct a solution
    # or candidate into words. We use `deconstructions`
    # to find every possible way to deconstruct into ints,
    # and then `sources` to find every possible way to get
    # those ints from words.

    def deconstruct(s):
        if bin(s).count('1') == 5:
            for src in sources[s]:
                yield [src]
            return
        for left, right in deconstructions[s]:
            for left_d in deconstruct(left):
                for right_d in deconstruct(right):
                    yield left_d + right_d

    # Print all the ways to build of all the solutions
    solutions = sorted([
        ' '.join(dec)
        for a in solutions
        for dec in deconstruct(a)
    ])
    for sol in solutions:
        print(sol)


if __name__ == "__main__":
    start: float = time.time()
    solve()
    print(f"Solved in {time.time() - start}s")

    # import re

    # vowels = {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"}
    # pattern = re.compile("[AEIOUaeiou]")

    # def intersection():
    #     return bool(vowels.intersection("TWYNDYLLYNGS"))

    # def any_version():
    #     return any(char in vowels for char in "TWYNDYLLYNGS")

    # def re_version():
    #     return bool(pattern.search("TWYNDYLLYNGS"))

    # def disjoint():
    #     return vowels.isdisjoint("TWYNDYLLYNGS")

    # from timeit import timeit

    # print(timeit("encode('wacko')", "from src.jotto import encode"))
    # print(timeit("letter_set('wacko')", "from src.jotto import letter_set"))
