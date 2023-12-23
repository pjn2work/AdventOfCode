import sys
sys.path.append("../..")
from utilities import time_duration

from collections import namedtuple
from typing import List, Tuple

Point = namedtuple("Point", "y x")
Data = List[str]
MOVES = {
    "^": [Point(-1, 0)],
    "<": [Point(0, -1)],
    "v": [Point(1, 0)],
    ">": [Point(0, 1)],
    ".": [Point(-1, 0), Point(0, -1), Point(1, 0), Point(0, 1)]
}


@time_duration
def parse() -> Tuple[Data, Point, Point]:
    data = []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            data.append(line.strip())
    return data, Point(0, data[0].index(".")), Point(len(data)-1, data[-1].index("."))


def get_max_path_len(data: Data, curr_pos: Point, goal: Point) -> int:
    ly, lx = len(data), len(data[0])
    res = 0
    queue_next = [(curr_pos, {curr_pos})]

    while queue_next:
        curr_pos, visited = queue_next.pop()

        if curr_pos == goal:
            res = max(res, len(visited))

        for inc in MOVES[data[curr_pos.y][curr_pos.x]]:
            cp = Point(curr_pos.y + inc.y, curr_pos.x + inc.x)
            if 0 <= cp.y < ly and 0 <= cp.x < lx and data[cp.y][cp.x] != "#" and cp not in visited:
                queue_next.append((cp, visited | {cp}))

    return res-1


# part 1 ----------------

@time_duration
def part1(data: Data, start: Point, goal: Point) -> int:
    return get_max_path_len(data, start, goal)


# part 2 ----------------

@time_duration
def part2(data: Data, start: Point, goal: Point) -> int:
    data = [row.replace("^", ".").replace("v", ".").replace("<", ".").replace(">", ".") for row in data]
    return get_max_path_len(data, start, goal)


@time_duration
def run_all():
    data, start, goal = parse()

    p1 = part1(data, start, goal)
    #p2 = part2(data, start, goal)

    print(f"Result for {p1 = }")
    #print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
