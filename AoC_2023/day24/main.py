import sys
sys.path.append("../..")
from utilities import time_duration

from collections import namedtuple
from dataclasses import dataclass
from typing import List, Tuple
import re


Point = namedtuple("Point", "x y z")
@dataclass
class Hailstone:
    pos: Point
    vel: Point
    m: float
    y_at_x_0: float
Data = List[Hailstone]


@time_duration
def parse() -> Data:
    num = re.compile(r"-?\d+")
    data = []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            pos, vel = line.strip().split("@")

            pos = Point(*[int(p.group()) for p in num.finditer(pos)])
            vel = Point(*[int(v.group()) for v in num.finditer(vel)])
            m = vel.y/vel.x
            y_at_x_0 = pos.y - m * pos.x  # y = y0 + m * (x - x0), when x = 0 => y = y0 - m*x0

            data.append(Hailstone(pos, vel, m, y_at_x_0))
    return data


def is_time_positive(pos: Point, vel: Point, x: float, y: float) -> bool:
    return abs(pos.x - x + vel.x) <= abs(pos.x - x) and abs(pos.y - y + vel.y) <= abs(pos.y - y)


def collide_within_bounds(h1: Hailstone, h2: Hailstone, bounds: Tuple[int, int]) -> bool:
    # They are parallel
    if h1.m == h2.m:
        return False

    x = (h2.y_at_x_0 - h1.y_at_x_0) / (h1.m - h2.m)
    y = h1.y_at_x_0 + h1.m * x

    return bounds[0] <= x <= bounds[1] and \
        bounds[0] <= y <= bounds[1] and \
        is_time_positive(h1.pos, h1.vel, x, y) and \
        is_time_positive(h2.pos, h2.vel, x, y)


# part 1 ----------------

@time_duration
def part1(data: Data, bounds: Tuple[int, int]) -> int:
    res = 0
    for i, pd1 in enumerate(data):
        for pd2 in data[i+1:]:
            if collide_within_bounds(pd1, pd2, bounds):
                res += 1
    return res


# part 2 ----------------

@time_duration
def part2(data: Data) -> int:
    return 0


@time_duration
def run_all():
    data = parse()

    p1 = part1(data, (200000000000000, 400000000000000))
    #p2 = part2(data)

    print(f"Result for {p1 = }")
    #print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
