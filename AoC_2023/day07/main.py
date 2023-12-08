import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from utilities import time_duration

from typing import Tuple, List
from collections import Counter, namedtuple


DRAW = namedtuple('DRAW', ['rank', 'cards', 'bid'])


@time_duration
def parse() -> Tuple[List[DRAW], List[DRAW]]:
    cards = "23456789TJQKA"

    def letters_to_nums(letters: str):
        return [cards.index(l) + 2 for l in letters]

    def get_rank(cards: List[int], mode2: bool = False) -> int:
        if mode2:
            j = cards.count(11)
            cards = [c for c in cards if c != 11]
            if len(cards) == 0:
                return 7
        else:
            j = 0

        rep = sorted(Counter(cards).values(), reverse=True)
        max_rep = max(rep)

        if max_rep + j == 5:
            return 7
        if max_rep + j == 4:
            return 6
        if max_rep + j == 3:
            if rep[1] == 2:
                return 5
            return 4
        if max_rep + j == 2:
            if rep[1] == 2:
                return 3
            return 2
        return 1

    p1, p2 = [], []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            _line = line.strip().split(" ")

            _l2n1 = letters_to_nums(_line[0])
            _l2n2 = [c if c != 11 else 1 for c in _l2n1]

            _rank1 = get_rank(_l2n1, mode2=False)
            _rank2 = get_rank(_l2n1, mode2=True)
            _bid = int(_line[1])

            p1.append(DRAW(_rank1, _l2n1, _bid))
            p2.append(DRAW(_rank2, _l2n2, _bid))

    return p1, p2


# part 1 & 2 ----------------

@time_duration
def solve(draws: List[DRAW]) -> int:
    draws.sort()
    return sum([i * d.bid for i, d in enumerate(draws, 1)])


@time_duration
def all():
    puzzle1, puzzle2  = parse()

    p1 = solve(puzzle1)
    p2 = solve(puzzle2)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    all()
