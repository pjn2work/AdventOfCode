from dataclasses import dataclass


def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


@dataclass
class Puzzle:
    sand_start: tuple[int, int]
    busy: set
    max_y: int
    cnt: int = 0


def read_input(line: str, p: Puzzle):
    points = tuple(tuple(map(int, coords.split(","))) for coords in line.split(" -> "))
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if y > p.max_y:
                p.max_y = y
            for x in range(min(x1, x2), max(x1, x2) + 1):
                p.busy.add((y, x))


def solve(p: Puzzle, mode1: bool = True) -> int:
    sand_moves = ((1, 0), (1, -1), (1, 1))
    mode2 = not mode1
    while True:
        y, x = p.sand_start
        while True:
            for my, mx in sand_moves:
                ny, nx = y + my, x + mx
                if (mode2 and (ny == p.max_y)) or (ny, nx) in p.busy:
                    continue        # move doesn't work, get another move
                if mode1 and ny == p.max_y:
                    return p.cnt    # mode 1, falling into the abyss
                break               # free space
            else:                   # no more moves, sand must rest (no break from for loop)
                p.cnt += 1
                p.busy.add((y, x))
                if y == 0:
                    return p.cnt    # mode2
                break               # no free space found, sand will rest

            y, x = ny, nx           # keep going


if __name__ == "__main__":
    puzzle = Puzzle(sand_start=(0, 500), busy=set(), max_y=0)
    parser(read_input, p=puzzle)

    print("Answer 1:", solve(puzzle, mode1=True))

    puzzle.max_y += 2
    print("Answer 2:", solve(puzzle, mode1=False))
