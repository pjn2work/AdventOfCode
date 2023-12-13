import sys

sys.path.append("../..")
from utilities import time_duration

from typing import List


Map = List[str]


@time_duration
def parse() -> List[Map]:
    maps, _map = [], []

    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                _map.append(line)
            else:
                maps.append(_map)
                _map = []
        maps.append(_map)

    return maps


def show_map(_map: Map):
    print()
    print("-"*80)
    for row in _map:
        print(row)
    print("-"*80)


def transpose(_map: Map) -> Map:
    return ["".join(column) for column in zip(*_map)]


def not_symmetrical_by(s1: str, s2: str) -> int:
    return sum([1 for l1, l2 in zip(reversed(s1), s2) if l1 != l2])


def get_reflection_column(_map: Map, threshold: int = 0) -> int:
    for x in range(len(_map[0]) - 1):
        smudge = sum(not_symmetrical_by(row[:x + 1], row[x + 1:]) for row in _map)
        if smudge == threshold:
            return x+1
    return 0


def calc_reflections(_map: Map, threshold: int = 0) -> int:
    return get_reflection_column(_map, threshold) + 100*get_reflection_column(transpose(_map), threshold)


# part 1 ----------------

@time_duration
def part1(maps: List[Map]) -> int:
    return sum([calc_reflections(_map, 0) for _map in maps])


# part 2 ----------------

@time_duration
def part2(maps: List[Map]) -> int:
    return sum([calc_reflections(_map, 1) for _map in maps])


@time_duration
def all():
    maps = parse()

    p1 = part1(maps)
    p2 = part2(maps)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    all()
