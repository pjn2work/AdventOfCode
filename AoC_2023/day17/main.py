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


def get_3_directions(direction) -> List[int]:
    # don't add opposite side (where I came from)
    return [d for d in range(4) if d == direction or d % 2 != direction % 2]


def play(data: Data, min_consecutive: int = 1, max_consecutive: int = 3):
    ly, lx = len(data), len(data[0])
    goal = (ly-1, lx-1)

    # (acc_heat, (y, x), direction, steps)
    moves = [ (0, (0, 0), 0, 0), (0, (0, 0), 1, 0) ]

    # visited [y][x][direction] having the least heat values
    visited = [[[-1, -1, -1, -1] for x in range(lx)] for y in range(ly)]
    for d in range(4):
        visited[0][0][d] = 0

    while moves:
        # get point with less heat
        acc_heat, p, direction, steps = heappop(moves)

        if p == goal:
            return acc_heat

        for _dir in get_3_directions(direction):
            _y, _x = p
            _curr_heat = acc_heat
            _steps = steps if _dir == direction else 0

            # only go with this direction if it can do min_consecutive steps without leaving the board bounds
            __pyx, __dyx, __max_size = (_x, 1, lx) if _dir%2 == 0 else (_y, 0, ly)
            if 0 <= __pyx + (min_consecutive - _steps) * DIRECTION[_dir][__dyx] < __max_size:

                for _ in range(_steps, max_consecutive):
                    _y, _x = _y + DIRECTION[_dir][0], _x + DIRECTION[_dir][1]
                    if 0 <= _y < ly and 0 <= _x < lx:
                        _curr_heat += data[_y][_x]
                        _steps += 1
                        _v_heat = visited[_y][_x][_dir]
                        if _v_heat == -1 or _curr_heat < _v_heat:
                            visited[_y][_x][_dir] = _curr_heat
                            if _steps >= min_consecutive:
                                # will sort - have the points with less heat at the beginning
                                heappush(moves, (_curr_heat, (_y, _x), _dir, _steps))
                    else:
                        break

    return -1


# part 1 ----------------

@time_duration
def part1(data: Data) -> int:
    return play(data)


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
