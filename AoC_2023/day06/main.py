import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from utilities import time_duration, prod

from typing import Tuple, List
import re


@time_duration
def parse() -> Tuple[List[Tuple[int, int]], Tuple[int, int]]:
    num = re.compile(r"\d+")

    with open("input.txt", mode="r", encoding="utf-8") as f:
        line1, line2 = f.readline().strip(), f.readline().strip()

        time_list = [int(n.group()) for n in num.finditer(line1)]
        dist_list = [int(n.group()) for n in num.finditer(line2)]

        time_dist_1 = [(t, d) for t, d in zip(time_list, dist_list)]
        time_dist_2 = int("".join(num.findall(line1))), int("".join(num.findall(line2)))

    return time_dist_1, time_dist_2


def win_ways(lap_time: int, lap_dist: int) -> int:
    return len([1 for hold in range(lap_time) if hold * (lap_time - hold) > lap_dist])


# part 1 ----------------

@time_duration
def part1(time_dist: List[Tuple[int, int]]) -> int:
    return prod([win_ways(*lap) for lap in time_dist])


# part 2 ----------------

@time_duration
def part2(time_dist2: Tuple[int, int]) -> int:
    return win_ways(*time_dist2)


@time_duration
def all():
    time_dist1, time_dist2 = parse()

    p1 = part1(time_dist1)
    p2 = part2(time_dist2)
    
    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    all()
