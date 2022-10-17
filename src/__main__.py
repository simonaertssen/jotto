# -*- coding: utf-8 -*-

import time

from src.jotto import solve

if __name__ == "__main__":
    start: float = time.time()
    solve()
    print(f"Solved in {time.time() - start}s")
