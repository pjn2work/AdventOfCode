import sys
sys.path.append("../..")
from utilities import time_duration

from collections import namedtuple
from typing import Set, List, Tuple
import numpy as np


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


def quadratic_fit(points: List[Tuple[int, int]], x: int) -> int:
    coeff = np.polyfit(*zip(*points), 2)
    return round(np.polyval(coeff, x))


def get_n_pos(data: Data, cycles: int, positions: Set[Point]) -> int:
    ly, lx = len(data), len(data[0])
    curr_cycle = 0

    # for part 2 vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    loop_cycle = ly // 2
    evolution_pos = []
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    while curr_cycle < cycles:
        curr_cycle += 1

        # make all moves for each cycle
        pos_real = set()
        while positions:
            y, x = positions.pop()
            for mv in MOVES:
                y_real, x_real = y + mv.y, x + mv.x
                y_map, x_map = y_real % ly, x_real % lx
                if data[y_map][x_map] != "#":
                    pos_real.add((y_real, x_real))
        positions = pos_real

        # for part 2 vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        if (curr_cycle - loop_cycle) % ly == 0:
            print(f"At cycle {curr_cycle} there are {len(positions)} possible positions.")
            evolution_pos.append(len(positions))
            if len(evolution_pos) == 3:
                break
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    if curr_cycle < cycles:
        # [(0, 3867), (1, 34253), (2, 94909)]
        return quadratic_fit([(i, pos) for i, pos in enumerate(evolution_pos)], cycles // ly)
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
