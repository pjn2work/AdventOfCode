from dataclasses import dataclass
from functools import cmp_to_key
import math


def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


@dataclass
class Puzzle:
    pairs_idx: int
    pairs_list: list
    answer1: list
    answer2: list


def read_input(line: str, p: Puzzle):
    if line == "":
        p.pairs_idx = 0
    else:
        p.pairs_idx += 1
        p.pairs_list.append(eval(line))
        if p.pairs_idx == 2:
            if compare(p.pairs_list[-2], p.pairs_list[-1]) == -1:
                p.answer1.append(len(p.pairs_list)//2)


def compare(l1: list, l2: list) -> int:
    if isinstance(l1, list):
        if not isinstance(l2, list):
            return compare(l1, [l2])
    elif isinstance(l2, list):
        return compare([l1], l2)
    else:
        return (l1 > l2) - (l1 < l2)

    for a1, a2 in zip(l1, l2):
        if cmp := compare(a1, a2):
            return cmp
    return compare(len(l1), len(l2))


if __name__ == "__main__":
    puzzle = Puzzle(pairs_idx=0, pairs_list=[], answer1=[], answer2=[])
    parser(read_input, p=puzzle)

    print("Answer 1:", sum(puzzle.answer1), puzzle.answer1)

    divider_packets = [[2]], [[6]]
    puzzle.pairs_list += divider_packets
    puzzle.pairs_list.sort(key=cmp_to_key(compare))
    puzzle.answer2 = [i for i, x in enumerate(puzzle.pairs_list, start=1) if x in divider_packets]
    print("Answer 2:", math.prod(puzzle.answer2), puzzle.answer2)
