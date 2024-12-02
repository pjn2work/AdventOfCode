import bisect
from typing import Tuple, List

from utilities import time_duration


Data = Tuple[List, List]


@time_duration
def parse() -> Data:
    l1, l2 = [], []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            n1, n2 = line.strip().split("   ")
            bisect.insort(l1, int(n1))
            bisect.insort(l2, int(n2))
    return l1, l2


@time_duration
def part1(l1: List, l2: List) -> int:
    return sum([abs(n2 - n1) for n1, n2 in zip(l1, l2)])


@time_duration
def part2(l1: List, l2: List) -> int:
    n1, n2 = l1.pop(0), l2.pop(0)
    seen = {}
    total = 0

    while n2:
        if n1 in seen:
            total += n1 * seen[n1]
        else:
            qtd = 0
            while n1 == n2:
                qtd += 1
                if len(l2) == 0:
                    n2 = 0
                    break
                n2 = l2.pop(0)
            total += n1 * qtd
            seen[n1] = qtd

        if len(l1) == 0:
            break
        n1 = l1.pop(0)

        while n1 > n2:
            if len(l2) == 0:
                n2 = 0
                break
            n2 = l2.pop(0)

    return total


@time_duration
def run_all():
    l1, l2 = parse()

    p1 = part1(l1, l2)
    p2 = part2(l1, l2)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
