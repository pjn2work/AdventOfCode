import sys
sys.path.append("../..")
from utilities import time_duration

from collections import namedtuple
from typing import Set, List, Tuple


Data = List[str]
Point = namedtuple("Point", "y x")
MOVES = (Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0))


@time_duration
def parse() -> Data:
    with open("input.txt", mode="r", encoding="utf-8") as f:
        return [line.strip() for line in f]


def get_start_pos(data: Data) -> Tuple[int, int]:
    for y, row in enumerate(data):
        if "S" in row:
            return y, row.index("S")


def get_n_pos(data: Data, cycles: int, positions: Set[Point]) -> int:
    ly, lx = len(data), len(data[0])

    cached_cycles = set(tuple(positions))
    c = 0
    not_found = True
    while c < cycles:
        c += 1

        _pos = set()
        while positions:
            y, x = positions.pop()
            for mv in MOVES:
                _ry, _rx = y + mv.y, x + mv.x
                _y, _x = _ry % ly, _rx % lx
                if data[_y][_x] != "#":
                    _pos.add((_y, _x))
        positions = _pos

        if not_found:
            cp = tuple(sorted(tuple(positions)))
            if cp in cached_cycles:
                not_found = False
                print(f"loop after {c} cycles")
                c = (cycles // c) * c
                continue
            cached_cycles.add(cp)

    return len(positions)


# part 1 ----------------

@time_duration
def part1(data: Data) -> int:
    return get_n_pos(data, 64, {get_start_pos(data)})


# part 2 ----------------

@time_duration
def part2(data: Data) -> int:
    return get_n_pos(data, 26501365, {get_start_pos(data)})


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
