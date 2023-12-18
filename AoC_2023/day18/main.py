import sys
from collections import namedtuple

sys.path.append("../..")
from utilities import time_duration, SetRange2D

from typing import List
import re


Action = namedtuple("Action", "dir n color")
Data = List[Action]


@time_duration
def parse() -> Data:
    data = []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            g = re.findall(r"([A-Z]) (\d+) \(#(\w{6})\)", line.strip())[0]
            data.append(Action(g[0], int(g[1]), g[2]))
    return data


DIRECTION = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}


def play(data: Data, show_table: bool = False) -> int:
    curr_y, curr_x = 0, 0
    outline_grid = SetRange2D().add(curr_y, curr_x, curr_x)

    for action in data:
        _iy, _ix = DIRECTION[action.dir]

        _nx = curr_x + action.n * _ix
        for _ in range(action.n):
            curr_y += _iy
            outline_grid.add(curr_y, curr_x, _nx)
        curr_x = _nx

    ff = outline_grid.flood_fill()

    if show_table:
        print(str(ff))

    return ff.get_total_occupied()


# part 1 ----------------

@time_duration
def part1(data: Data) -> int:
    return play(data, show_table=False)


# part 2 ----------------

@time_duration
def part2(data: Data) -> int:
    DU = {"0": "R", "1": "D", "2": "L", "3": "U"}
    data = [Action(dir=DU[action.color[-1]], n=int(action.color[:-1], 16), color=action.color) for action in data]
    return play(data)


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
