# -*- coding: utf-8 -*-

import time

from src.jotto import solve

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
