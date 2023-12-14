import sys

sys.path.append("../..")
from utilities import time_duration

from typing import List


Map = List[List[str]]


@time_duration
def parse() -> Map:
    _map = []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            _map.append(list(line.strip()))
    return _map


# Affects current map
def tilt_north(_map: Map):
    for x in range(len(_map[0])):
        for y_row in range(1, len(_map), 1):
            for y in range(y_row, 0, -1):
                if _map[y][x] == "O" and _map[y-1][x] == ".":
                    _map[y][x], _map[y-1][x] = _map[y-1][x], _map[y][x]


def rotate_right(_map: Map) -> Map:
    return [list(reversed(column)) for column in zip(*_map)]


def calc_load(_map: Map) -> int:
    return sum("".join(row).count("O") * (len(_map) - y) for y, row in enumerate(_map))


# part 1 ----------------

@time_duration
def part1(_map: Map) -> int:
    tilt_north(_map)
    return calc_load(_map)


# part 2 ----------------

def spin_and_tilt(_map: Map) -> Map:
    tilt_north(_map)                                # North
    _map = rotate_right(_map); tilt_north(_map)     # West
    _map = rotate_right(_map); tilt_north(_map)     # South
    _map = rotate_right(_map); tilt_north(_map)     # East
    _map = rotate_right(_map)                       # put North back again
    return _map


@time_duration
def part2(_map: Map, cycles: int) -> int:
    map_cache = dict()
    for cycle in range(cycles):
        _map = spin_and_tilt(_map)

        _hash = hash("".join("".join(row) for row in _map))
        if _hash in map_cache:
            cycle_pattern_started = map_cache[_hash]
            cycle_pattern_length = cycle - cycle_pattern_started
            cycles_saved_because_pattern = ((cycles - cycle_pattern_started) // cycle_pattern_length) * cycle_pattern_length
            cycles_missing = cycles - cycle_pattern_started-1 - cycles_saved_because_pattern
            print(f"At {cycle=} repetition pattern was found at {cycle_pattern_started}, with {cycle_pattern_length} spins.\nSaved {cycles_saved_because_pattern:,} cycles, still need to do {cycles_missing} spins to finish.")

            for _ in range(cycles_missing):
                _map = spin_and_tilt(_map)
            return calc_load(_map)

        map_cache[_hash] = cycle
    return calc_load(_map)


@time_duration
def all():
    p1 = part1(parse())
    p2 = part2(parse(), cycles=1000000000)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    all()
