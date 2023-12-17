import sys
sys.path.append("../..")
from utilities import time_duration

from typing import List
from heapq import heappop, heappush


Data = List[List[int]]


@time_duration
def parse() -> Data:
    data = []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            data.append([int(v) for v in line.strip()])
    return data


DIRECTION = ((0, 1), (1, 0), (0, -1), (-1, 0))


def play(data: Data, min_consecutive: int, max_consecutive: int) -> int:
    ly, lx = len(data), len(data[0])
    goal = (ly-1, lx-1)

    # (acc_heat, (y, x), direction, steps)
    moves = [ (0, (0, 0), 0, 0), (0, (0, 0), 1, 0) ]
    visited = set()

    while moves:
        # get point_y_x with less heat
        acc_heat, p, direction, steps = heappop(moves)

        if p == goal and steps >= min_consecutive:
            return acc_heat

        if (p, direction, steps) not in visited:
            visited.add((p, direction, steps))

            y, x = p[0] + DIRECTION[direction][0], p[1] + DIRECTION[direction][1]
            if 0 <= y < ly and 0 <= x < lx:
                acc_heat += data[y][x]
                steps += 1

                if steps >= min_consecutive:
                    heappush(moves, (acc_heat, (y, x), (direction+1)%4, 0))
                    heappush(moves, (acc_heat, (y, x), (direction-1)%4, 0))

                if steps < max_consecutive:
                    heappush(moves, (acc_heat, (y, x), direction, steps))

    return -1


# part 1 ----------------

@time_duration
def part1(data: Data) -> int:
    return play(data, 1, 3)


# part 2 ----------------

@time_duration
def part2(data: Data) -> int:
    return play(data, 4, 10)


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
