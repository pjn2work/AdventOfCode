import sys
sys.path.append("../..")
from utilities import time_duration

from typing import List
import re


def parse(exp_level: int = 2) -> List[List[int]]:
    galaxy = re.compile("#")

    y = 0
    x_busy = set()
    galaxies = []

    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            gg = [[y, g.start()] for g in galaxy.finditer(line.strip())]
            galaxies.extend(gg)

            if gg:
                x_busy = x_busy.union([x for y, x in gg])
                y += 1
            else:
                y += exp_level

    # create correlation dict between column (in map) and column (map + expansion)
    corr, curr_x = dict(), 0
    for x in range(max(x_busy)+1):
        corr[x] = curr_x
        curr_x += 1 if x in x_busy else exp_level

    # shift/fix columns with expansion
    for g in galaxies:
        g[1] = corr[g[1]]

    return galaxies


# part 1 & 2 ----------------

def get_sqr_dist(y1, x1, y2, x2) -> int:
    return abs(y2-y1) + abs(x2-x1)


@time_duration
def get_sum_distances(galaxies: List[List[int]]) -> int:
    acc = 0
    for i in range(len(galaxies)-1):
        for j in range(i+1, len(galaxies)):
            acc += get_sqr_dist(*galaxies[i], *galaxies[j])
    return acc


@time_duration
def all():
    p1 = get_sum_distances(parse(exp_level=2))
    p2 = get_sum_distances(parse(exp_level=1000000))

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    all()
