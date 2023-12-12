import sys

sys.path.append("../..")
from utilities import time_duration

from collections import namedtuple
from typing import List, Tuple
from functools import cache


SpringRow = namedtuple("SpringRow", ["springs", "springs_damaged_seq"])


@time_duration
def parse() -> List[SpringRow]:
    map = []

    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().split(" ")
            map.append(SpringRow(line[0], tuple([int(d) for d in line[1].split(",")])))

    return map


@cache
def possibilities(springs: str, springs_damaged_seq: Tuple[int], must_be_damaged: int | None = None) -> int:
    if must_be_damaged is None:
        if springs == "":
            return len(springs_damaged_seq) == 0
        if springs[0] == "#":
            if len(springs_damaged_seq) == 0:
                return 0
            else:
                return possibilities(springs[1:], springs_damaged_seq[1:], springs_damaged_seq[0] - 1)
        if springs[0] == ".":
            return possibilities(springs[1:], springs_damaged_seq, None)
        # spring == ?
        if len(springs_damaged_seq) == 0:
            return possibilities(springs[1:], springs_damaged_seq, None)
        return (possibilities(springs[1:], springs_damaged_seq[1:], springs_damaged_seq[0] - 1) +
                possibilities(springs[1:], springs_damaged_seq, None))

    if springs == "":
        if must_be_damaged + sum(springs_damaged_seq) == 0:
            return 1
        return 0
    else:
        # the unknowns + damaged springs can't be enough to fulfill the damaged springs
        if springs.count("?") + springs.count("#") < must_be_damaged + sum(springs_damaged_seq):
            return 0

    # deal with the current spring
    spring, rest = springs[0], springs[1:]

    if spring == "#":
        if must_be_damaged >= 1:
            return possibilities(rest, springs_damaged_seq, must_be_damaged - 1)
        return 0

    if spring == ".":
        if must_be_damaged == 0:
            return possibilities(rest, springs_damaged_seq, None)
        return 0

    if spring == "?":
        if must_be_damaged == 0:  # ? = .
            return possibilities(rest, springs_damaged_seq, None)
        if must_be_damaged >= 1:  # ? = #
            return possibilities(rest, springs_damaged_seq, must_be_damaged - 1)
        return 0


# part 1 ----------------

@time_duration
def part1(puzzle: List[SpringRow]) -> int:
    return sum([
        possibilities(
            springs=sr.springs,
            springs_damaged_seq=sr.springs_damaged_seq
        ) for sr in puzzle])


# part 2 ----------------

@time_duration
def part2(puzzle: List[SpringRow]) -> int:
    return sum([
        possibilities(
            springs="?".join([sr.springs for _ in range(5)]),
            springs_damaged_seq=(sr.springs_damaged_seq * 5)
        ) for sr in puzzle])


@time_duration
def all():
    puzzle = parse()

    p1 = part1(puzzle)
    p2 = part2(puzzle)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    all()
