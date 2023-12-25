from dataclasses import dataclass
import re
import numpy as np


def parser(filename, method, **kwargs):
    with open(filename, mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.rstrip(), **kwargs)


@dataclass
class Puzzle:
    map: np.ndarray
    directions: list[tuple[int, str]]
    curr_dir = 0
    y: int = 0
    x: int = 0
    my: int = 0
    mx: int = 0


INC = [(0, 1), (1, 0), (0, -1), (-1, 0)]
map_mode = True


def read_input(line: str, p: Puzzle):
    global map_mode
    if len(line) == 0:
        map_mode = False
    else:
        if map_mode:
            p.map.append(line)
        else:
            p.y, p.x = 0, p.map[0].index(".")
            p.my, p.mx = len(p.map), max([len(l) for l in p.map])
            map = np.ndarray((p.my, p.mx), dtype='S1')
            map[:] = " "
            for y in range(len(p.map)):
                for x, e in enumerate(p.map[y]):
                    map[y, x] = e
            p.map = map

            moves = re.findall(r"(\d+)(\w)", line)
            for v, d in moves:
                p.directions.append((int(v), d))
            p.directions.append((int(re.search(r".+(\d+)$", line).group(1)), " "))


def walk2d(p: Puzzle, distance, turn):
    for _ in range(distance):
        iy, ix = INC[p.curr_dir]
        ny = (p.y + iy) % p.my
        nx = (p.x + ix) % p.mx

        while p.map[ny, nx] == b" ":
            ny = (ny + iy) % p.my
            nx = (nx + ix) % p.mx

        if p.map[ny, nx] == b"#":
            break
        p.y, p.x = ny, nx

    if turn != " ":
        p.curr_dir = (p.curr_dir + 1) % 4 if turn == "R" else (p.curr_dir - 1) % 4


def walk3d(p: Puzzle, distance, turn):
    for _ in range(distance):
        iy, ix = INC[p.curr_dir]
        ny = (p.y + iy) % p.my
        nx = (p.x + ix) % p.mx
        nd = p.curr_dir

        if iy < 0:
            if p.y == 0:
                if 50 <= p.x < 100:
                    ny = 150 + p.x - 50
                    nx = 0
                    nd = 0
                else:
                    ny = 199
                    nx = p.x - 100
            elif p.y == 100 and 0 <= p.x < 50:
                ny = 50 + p.x
                nx = 50
                nd = 0
        elif iy > 0:
            if p.y == 49 and 100 <= p.x < 150:
                ny = p.x - 50
                nx = 99
                nd = 2
            elif p.y == 149 and 50 <= p.x < 100:
                ny = p.x - 50 + 150
                nx = 49
                nd = 2
            elif p.y == 199:
                ny = 0
                nx = p.x + 100
                nd = 1
        elif ix < 0:
            if p.x == 0:
                if 100 <= p.y < 150:
                    ny = 100 - p.y + 49
                    nx = 50
                    nd = 0
                else:
                    ny = 0
                    nx = p.y - 150 + 50
                    nd = 1
            elif p.x == 50:
                if 0 <= p.y < 50:
                    ny = 49 - p.y + 100
                    nx = 0
                    nd = 0
                if 50 <= p.y < 100:
                    ny = 100
                    nx = p.y - 50
                    nd = 1
        elif ix > 0:
            if p.x == 149:
                ny = 149 - p.y
                nx = 99
                nd = 2
            elif p.x == 99:
                if 50 <= p.y < 100:
                    ny = 49
                    nx = p.y + 50
                    nd = 3
                elif 100 <= p.y < 150:
                    ny = 149 - p.y
                    nx = 149
                    nd = 2
            elif p.x == 49 and 150 <= p.y:
                ny = 149
                nx = p.y - 100
                nd = 3

        if p.map[ny, nx] == b"#":
            break
        p.y, p.x, p.curr_dir = ny, nx, nd

    if turn != " ":
        p.curr_dir = (p.curr_dir + 1) % 4 if turn == "R" else (p.curr_dir - 1) % 4


def solve(p: Puzzle, method):
    for distance, turn in p.directions:
        method(p, distance, turn)
    return (p.y+1)*1000 + (p.x+1)*4 + p.curr_dir, f"(Final: y = {p.y+1} | x = {p.x+1} | dir = {p.curr_dir})"


if __name__ == "__main__":
    puzzle = Puzzle(map=[], directions=[])
    parser("input.txt", read_input, p=puzzle)

    print("Answer 1:", *solve(puzzle, walk2d))  # Answer 1: 65368  (Final: y = 65  | x = 92  | dir = 0 )
    print("Answer 2:", *solve(puzzle, walk3d))  # Answer 2: 156166 (Final: y = 156 | x = 41 | dir = 2)
